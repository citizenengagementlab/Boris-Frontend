from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.mail import mail_admins

from proxy.views import rtv_proxy
from registrant.utils import get_branding,empty

from ziplookup.models import ZipCode

import urllib

from django.contrib.localflavor.us import us_states
STATE_NAME_LOOKUP = dict(us_states.US_STATES)
STATE_NAME_LOOKUP['DC'] = "DC" #monkey patch, because "District of Columbia doesn't fit"

def get_locale(request):
    """Util method to determine locale from request. Checks session first, then get parameter.
    Returns 'en' or 'es', for use in context."""
    if request.GET.get('locale'):
        locale = request.GET['locale']
        request.session['django_language'] = locale
        return locale
    elif request.session.has_key('django_language'):
        return request.session['django_language']
    else:
        return "en"

def map(request):
    "Map for state select"
    get_locale(request)

    context = {}
    params = {}
    if request.GET.get('partner'):
        context['partner'] = request.GET.get('partner')
        context = get_branding(context)
        params['partner'] = context['partner']
    if request.GET.get('source'):
        context['source'] = request.GET.get('source')
        params['source'] = context['source']
    if request.GET.get('email_address'):
        context['email_address'] = request.GET.get('email_address')
        params['email_address'] = context['email_address']

    #if state, redirect to the form
    if request.GET.get('state'):
        params['state'] = request.GET.get('state')
        redirect_url = reverse('registrant.views.register')
        redirect_url += "?"+urllib.urlencode(params)
        return redirect(redirect_url)

    return render_to_response('map.html',context,
            context_instance=RequestContext(request))

def register(request):
    "The full form, in a single page format"
    locale = get_locale(request)

    context = {}
    #setup partner id based on get parameter
    if 'partner' in request.GET:
        context['has_partner'] = True
        context['partner'] = request.GET.get('partner')
        context = get_branding(context)
    else:
        #use CEL default
        context['partner'] = 9937
        context['has_partner'] = False
        #so we don't show the param in subsequent links

    if request.GET.get('source'):
        context['source'] = request.GET.get('source')

    #set state based on get parameter
    if 'state' in request.GET:
        state = request.GET.get('state').upper()

        #check for direct submission state
        #if state in ['WA'] and not request.GET.has_key('no_redirect'):
        #    return redirect('/registrants/new/'+state.lower())

        #hit rtv_proxy for staterequirements
        context['state'] = state
        try:
            context['state_name'] = STATE_NAME_LOOKUP[state]
        except KeyError:
            #don't have a state, redirect to the map
            redirect_url = reverse('registrant.views.map')
            params = {}
            if context['has_partner']:
                params['partner'] = context['partner']
            if request.GET.get('email_address'):
                params['email_address'] = request.GET.get('email_address')
            if params:
                redirect_url += "?"+urllib.urlencode(params)
            return redirect(redirect_url)

        #TODO: get language code from localeurl

        staterequirements = rtv_proxy('POST',{'home_state_id':state,'lang':locale},
            '/api/v2/state_requirements.json')
        context['staterequirements'] = staterequirements

        if staterequirements.has_key('error'):
            return render_to_response('ineligible.html',context,
                        context_instance=RequestContext(request))
    else:
        redirect_url = reverse('registrant.views.map')
        params = {}
        if context['has_partner']:
            params['partner'] = context['partner']
        if request.GET.get('email_address'):
                params['email_address'] = request.GET.get('email_address')
        if params:
            redirect_url += "?"+urllib.urlencode(params)
        return redirect(redirect_url) #redirect to the map
    
    return render_to_response('form.html',context,
                context_instance=RequestContext(request))
    
def submit(request):
    "Submit the posted form to the Rocky API"
    get_locale(request)

    if request.method != "POST":
        return redirect('/registrants/new/')
    submitted_form = request.POST.copy()
    #make a mutable copy

    #remove inputs that we needed, but the api will reject
    remove_inputs = ['csrfmiddlewaretoken','facebook']
    for t in remove_inputs:
        if submitted_form.has_key(t):
            submitted_form.pop(t)

    #rename source to source_tracking_id as per api
    if 'source' in submitted_form:
        submitted_form['source_tracking_id'] = submitted_form.pop('source')[0]
    #use partner_tracking_id for referrals
    #TBD

    #convert "on/off" to boolean values expected by api
    booleans = ['first_registration','has_mailing_address',
                'change_of_name','change_of_address',
                'opt_in_sms','opt_in_email','opt_in_volunteer',
                'partner_opt_in_sms','partner_opt_in_email','partner_opt_in_volunteer',
                'us_citizen']
    for b in booleans:
        if submitted_form.has_key(b):
            if submitted_form.get(b)[0] == "off":
                submitted_form[b] = '0'
            if submitted_form.get(b)[0] == "on":
                submitted_form[b] = '1'
    
    #check for required values that aren't defined in the post
    required_fields = ['opt_in_sms','opt_in_email','us_citizen','id_number']
    for r in required_fields:
        if not submitted_form.has_key(r):
            #and fill it in with zero
            submitted_form[r] = '0'

    #fill in none for blank id number
    if empty(submitted_form['id_number']):
        submitted_form['id_number'] = "none"
    
    #fill in missing city/state fields if we have zipcodes
    zip_fields = ['home','mailing','prev']
    for f in zip_fields:
        zipcode = submitted_form.get(f+'_zip_code')
        city = submitted_form.get(f+'_city')
        state = submitted_form.get(f+'_state_id')
        if not empty(zipcode) and (empty(city) and empty(state)):
            try:
                place = ZipCode.objects.get(zipcode=zipcode)
                submitted_form[f+'_city'] = place.city.lower().title()
                submitted_form[f+'_state_id'] = place.state
            except ZipCode.DoesNotExist:
                pass
    #this can happen if the user has to go back and resubmit the form, but the zipcode lookup js doesn't re-run
    #should probably also fix this client side...

    #check for title and replace it if it's an invalid value
    if submitted_form.has_key('name_title'):
        title = submitted_form.get('name_title')
        print "title",title
        if title not in ["Mr.", "Ms.", "Mrs.", "Sr.", "Sra.","Srta."]:
            submitted_form['name_title'] = "Mr." #guess, because we have to send valid data to API

    #check for suffix and clear it if it's an invalid value
    if submitted_form.has_key('name_suffix'):
        suffix = submitted_form.get('name_suffix')
        if suffix not in ["Jr.", "Sr.", "II", "III", "IV"]:
            submitted_form['name_suffix'] = ""

    #force allow rocky to send confirmation emails
    submitted_form['send_confirmation_reminder_emails'] ='1'

    #send questions to api if answers were set
    #defaults first
    question_1 = "If you are in school, where do you go?"
    question_2 = "What issue do you care most about?"

    #then check cobrand and custom form
    branding = get_branding({'partner':submitted_form['partner_id']})
    if branding.get('cobrandform'):
        cobrand = branding['cobrandform']
        if cobrand.question_1:
            question_1 = cobrand.question_1
        if cobrand.question_2:
            question_2 = cobrand.question_2
    elif branding.get('customform'):
        customform = branding.get('customform')
        if customform.question_1:
            question_1 = customform.question_1
        if customform.question_2:
            question_2 = customform.question_2
    if submitted_form['survey_answer_1']:
        submitted_form['survey_question_1'] = question_1
    if submitted_form['survey_answer_2']:
        submitted_form['survey_question_2'] = question_2

    #hit the rocky api
    rtv_response = rtv_proxy('POST',submitted_form,'/api/v2/registrations.json')

    context = {}
    if rtv_response.has_key('pdfurl'):
        context['pdfurl'] = rtv_response['pdfurl']
    if rtv_response.has_key('error'):
        #something went wrong that wasn't caught in the frontend validation
        #clean up error message for human consumption
        try:
            context['error'] = True
            messages.error(request, rtv_response['error']['message'].lower(),
                extra_tags=rtv_response['error']['field_name'].replace('_',' ').title())
        except KeyError:
            context['error'] = True
            messages.error(request, rtv_response['error'],
                extra_tags="Rocky API")
        #also mail the admins to see if there's a persistent problem
        mail_admins('rocky error: validating %s' % rtv_response['error']['field_name'],
            "rtv_response: %s\nsubmitted_form:%s" % (rtv_response,submitted_form))
        
    context['email_address'] = submitted_form.get("email_address")

    try:
        context['state_name'] = STATE_NAME_LOOKUP[submitted_form.get('home_state_id')]
    except KeyError:
        #unrecognized state
        context['error'] = True
        messages.error(request, _("Unrecognized state, please go back and try again."))

    #if a partner, post to their api
    if submitted_form.has_key('partner_id') and bool(submitted_form['opt_in_email']) == True:
        if branding.get('cobrandform'):
            customform = branding['cobrandform'].toplevel_org
            submitted_form['cobrand'] = branding['cobrandform'].name
        elif branding.get('customform'):
            customform = branding['customform']
        else:
            customform = None

        if customform:
            proxy_response = customform.submit(submitted_form)
            if proxy_response.get('error'):
                mail_admins('rocky error: custom form:  %s' % customform.name,
                            "proxy_response: %s\nsubmitted_form:%s" % (proxy_response,submitted_form))
                context['error'] = True
                messages.error(request, _("Unknown error: the web administrators have been contacted."),
                    extra_tags=proxy_response)

    #send branding partner ids to context, for trackable social media links
    context['partner'] = submitted_form.get('partner_id')
    context['source'] = submitted_form.get('partner_tracking_id')
    context = get_branding(context)
    #don't show partner for cel testing links
    if context['partner'] != 9937:
        context['has_partner'] = True

    #TODO, what user id should we use?
    #some hash of email and partner_id?
    context['user_id'] = "TBD"

    if context.has_key('error'):
        return redirect('/registrants/error/')
    else:
        return render_to_response('submit.html', context, context_instance=RequestContext(request))

def wa_direct(request):
    "direct submission to WA state form"
    get_locale(request)

    context = {}
    if request.GET.get('partner'):
        context['partner'] = request.GET.get('partner')
        context = get_branding(context)
    if request.GET.get('source'):
        context['source'] = request.GET.get('source')

    context['state_name'] = "Washington"

    return render_to_response('form_wa_direct.html',context,
            context_instance=RequestContext(request))

def error(request):
    get_locale(request)
    return render_to_response('error.html', {}, context_instance=RequestContext(request))
