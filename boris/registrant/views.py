from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseServerError
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.mail import mail_admins
from django.views.decorators.csrf import csrf_exempt

from proxy.views import rtv_proxy,rtv_proxy_cached
from registrant.utils import get_branding,empty
from registrant.decorators import capture_locale,capture_get_parameters

from ziplookup.models import ZipCode

import json
import urllib

from django.contrib.localflavor.us import us_states
STATE_NAME_LOOKUP = dict(us_states.US_STATES)
STATE_NAME_LOOKUP['DC'] = "DC" #monkey patch, because "District of Columbia doesn't fit"

#states with direct submission forms
DIRECT_SUBMIT_STATES = ['WA','NV','CA']

#if the submission is made using these partner ids, do not display custom branding
DEFAULT_PARTNER_IDS = [1,9937]

@capture_get_parameters(['email_address','home_zip_code','state'])
@capture_locale
def map(request):
    "Map for state select"

    context = {}
    params = request.GET.copy()

    if request.GET.get('clear_location'):
        request.session['state'] = None
        request.session['home_zip_code'] = None

    #check for zipcode
    if request.session.get('home_zip_code'):
        #lookup state from zip
        try:
            place = ZipCode.objects.get(zipcode=request.session['home_zip_code'])
            request.session['state'] = place.state
            params['state'] = place.state
        except ZipCode.DoesNotExist:
            pass

    #if state, redirect to the form
    if request.session.get('state'):
        params['state'] = request.session['state']
        redirect_url = reverse('registrant.views.register')
        redirect_url += "?"+urllib.urlencode(params)
        return redirect(redirect_url)

    return render_to_response('map.html',context,
            context_instance=RequestContext(request))

@capture_get_parameters(['email_address','home_zip_code','state'])
@capture_locale
def register(request):
    "The full form, in a single page format"

    context = {}
    #setup partner id based on get parameter
    if 'partner' in request.GET:
        context['has_partner'] = True
        context['partner'] = request.GET.get('partner')
    else:
        if request.session.has_key('facebook_canvas'):
            if request.session.has_key('facebook_partner_id'):
                context['partner'] = request.session['facebook_partner_id']
                context['has_partner'] = True
            else:
                #use facebook default
                context['partner'] = 19093
        else:
            #use RTV default
            context['partner'] = 1

        if not context.has_key('has_partner'):
            context['has_partner'] = False
            #so we don't show the param in subsequent links

    if request.GET.get('source'):
        context['source'] = request.GET.get('source')
    elif request.session.get('facebook_source'):
        context['source'] = request.session['facebook_source']

    #set state based on get parameter
    if 'state' in request.GET:
        state = request.GET.get('state').upper()

        #check for direct submission state
        if (state in DIRECT_SUBMIT_STATES) and (not request.GET.has_key('no_redirect')):
            #redirect to direct submit form
            params = request.GET.copy()
            if 'state' in params:
                params.pop('state')
            redirect_url = '/registrants/new/'+state.lower()
            redirect_url += "/?"+urllib.urlencode(params)
            return redirect(redirect_url)
        
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

        staterequirements = rtv_proxy_cached('POST',{'home_state_id':state,'lang':request.LANGUAGE_CODE},
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
 
@csrf_exempt #because sometimes cookies can't be set correctly by iframe
def submit(request):
    "Submit the posted form to the Rocky API"

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

    #convert "on/off" to "boolean" values expected by api
    booleans = ['us_citizen','first_registration','has_mailing_address',
                'change_of_name','change_of_address',
                'opt_in_sms','opt_in_email','opt_in_volunteer',
                'partner_opt_in_sms','partner_opt_in_email','partner_opt_in_volunteer']
    for b in booleans:
        if submitted_form.has_key(b):
            try:
                submitted_form[b] = int(submitted_form[b])
            except ValueError:
                if submitted_form.get(b) == "off":
                    submitted_form[b] = 0
                if submitted_form.get(b) == "on":
                    submitted_form[b] = 1
    
    #check for rocky required fields, fill them with defaults
    required_fields = ['opt_in_sms','opt_in_email','us_citizen','id_number']
    for r in required_fields:
        if not submitted_form.has_key(r):
            #and fill it in with zero
            submitted_form[r] = 0

    #strip spaces from id_number, because rocky doesn't like them
    if (' ' in submitted_form['id_number']):
        submitted_form['id_number'] = submitted_form['id_number'].replace(' ','')

    #if id_number blank, fill it in with none
    if empty(submitted_form['id_number']):
        submitted_form['id_number'] = "none"
    
    #fill in missing city/state fields if we have zipcodes
    zip_fields = ['home','mailing','prev']
    for f in zip_fields:
        zipcode = submitted_form.get(f+'_zip_code').strip()
        city = submitted_form.get(f+'_city')
        if empty(city) and not empty(zipcode):
            try:
                place = ZipCode.objects.get(zipcode=zipcode)
                submitted_form[f+'_city'] = place.city.lower().title()
                submitted_form[f+'_state_id'] = place.state
            except (ZipCode.DoesNotExist,ValueError,IndexError):
                pass
    #this can happen if the user has to go back and resubmit the form, but the zipcode lookup js doesn't re-run
    #should probably also fix this client side...

    #check for title and replace it if it's an invalid value
    if submitted_form.has_key('name_title'):
        title = submitted_form.get('name_title')
        if title not in ["Mr.", "Ms.", "Mrs.", "Sr.", "Sra.","Srta."]:
            submitted_form['name_title'] = "Mr." #guess, because we have to send valid data to API

    #check for suffix and clear it if it's an invalid value
    if submitted_form.has_key('name_suffix'):
        suffix = submitted_form.get('name_suffix')
        if suffix not in ["Jr.", "Sr.", "II", "III", "IV"]:
            submitted_form['name_suffix'] = ""

    #check for race and clear it if it's an invalid value
    if submitted_form.has_key('race'):
        race = submitted_form.get('race')
        if race not in ["American Indian / Alaskan Native", "Asian / Pacific Islander",
                        "Black (not Hispanic)", "Hispanic", "Multi-racial",
                        "White (not Hispanic)", "Other", "Decline to State",
                        "Indio Americano / Nativo de Alaska", "Asiatico / Islas del Pacifico",
                        "Negra (no Hispano)", "Hispano", "Blanca (no Hispano)", "Otra", "Declino comentar"]:
            submitted_form['race'] = "Other"

    #rocky api only accepts en/es, clear country specific locales (eg, en-gb)
    if submitted_form.has_key('lang'):
        lang = submitted_form.get('lang')
        if lang.startswith('en'):
            lang = 'en'
        elif lang.startswith('es'):
            lang = 'es'
        else:
            lang = 'en'
    else:
        lang = 'en'
    submitted_form['lang'] = lang


    #force allow rocky to send confirmation emails
    submitted_form['send_confirmation_reminder_emails'] ='1'

    #send questions to api if answers were set
    #defaults first
    question_1 = "If you are in school, where do you go?"
    question_2 = "What issue do you care most about?"

    #then check cobrand and custom form
    branding = get_branding({'partner':submitted_form['partner_id'],'language':lang})
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
    if submitted_form.has_key('survey_answer_1'):
        submitted_form['survey_question_1'] = question_1
    if submitted_form.has_key('survey_answer_2'):
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
            #also mail the admins to see if there's a persistent problem
            mail_admins('rocky error: validating %s' % rtv_response['error']['field_name'],
                "rtv_response: %s\n\nsubmitted_form:%s" % (rtv_response,submitted_form))
        except KeyError:
            context['error'] = True
            messages.error(request, rtv_response['error'],
                extra_tags="Rocky API")
            mail_admins('rocky error: api issue',
                "rtv_response: %s\n\nsubmitted_form:%s" % (rtv_response,submitted_form))

    #check state id against list of valid abbreviations
    try:
        context['state_name'] = STATE_NAME_LOOKUP[submitted_form.get('home_state_id')]
    except KeyError:
        #unrecognized state
        context['error'] = True
        messages.error(request, _("Unrecognized state, please go back and try again."))

    #get toplevel org for partner proxy submit
    if branding.get('cobrandform'):
        customform = branding['cobrandform'].toplevel_org
        submitted_form['cobrand'] = branding['cobrandform'].name
        #If customform and cobrand form, RTV and custom share main optin,
        #so use opt_in_email for partner_proxy_signup
        partner_proxy_signup = submitted_form['opt_in_email']
    elif branding.get('customform'):
        customform = branding['customform']
        #If customform but not cobrand form, set partner_proxy_signup to partner_opt_in_email
        partner_proxy_signup = submitted_form['opt_in_email']
    else:
        customform = None
        partner_proxy_signup = None

    #if a custom form has endpoint, and we got user permission, post to the partner proxy
    if customform and customform.list_signup_endpoint and partner_proxy_signup:
        proxy_response = customform.submit(submitted_form)
        if proxy_response.get('error'):
            mail_admins('rocky error: custom form:  %s' % customform.name,
                        "proxy_response: %s\nsubmitted_form:%s" % (proxy_response,submitted_form))
            context['error'] = True
            messages.error(request, _("Unknown error: the web administrators have been contacted."),
                extra_tags=proxy_response)

    #append branding to context, so partner logos appear in submit page
    context.update(branding)

    #send branding partner ids to context, for trackable social media links
    context['partner'] = submitted_form.get('partner_id')
    context['source'] = submitted_form.get('partner_tracking_id')
    context['email_address'] = submitted_form.get("email_address")

    #don't show partner for testings partner ids
    if context['partner'] in DEFAULT_PARTNER_IDS:
        context['has_partner'] = False

    if context.has_key('error'):
        return redirect('/registrants/error/')
    else:
        return render_to_response('submit.html', context, context_instance=RequestContext(request))

@capture_get_parameters(['email_address','home_zip_code','state'])
@capture_locale
def register_direct(request,state_abbr):
    "direct registration via state website"

    #check for direct submit states
    state = state_abbr.upper()
    if not state in DIRECT_SUBMIT_STATES:
        redirect_url = reverse('registrant.views.register')
        params = request.GET.copy()
        params['state'] = state
        if params:
            redirect_url += "?"+urllib.urlencode(params)
        return redirect(redirect_url) #redirect to the regular form

    context = {}
    context['state'] = state
    context['state_name'] = STATE_NAME_LOOKUP[state]

    if 'partner' in request.GET:
        context['has_partner'] = True
        context['partner'] = request.GET.get('partner')

    return render_to_response('form_%s_direct.html' % state.lower(),context,
            context_instance=RequestContext(request))

@csrf_exempt
def submit_direct(request,state_abbr):
    "save direct info in Rocky, returns json"
    if not request.method == "POST":
        return HttpResponse(json.dumps({'error':'incorrect method','message':'this url expects POST'}))

    submitted_form = request.POST.copy()

    #remove inputs that we needed, but the api will reject
    remove_inputs = ['csrfmiddlewaretoken','facebook','has_state_license','name_suffix']
    for t in remove_inputs:
        if submitted_form.has_key(t):
            submitted_form.pop(t)

    #and add the ones it does
    submitted_form['home_state_id'] = state_abbr
    submitted_form['send_confirmation_reminder_emails'] = '1'

    #rename source to source_tracking_id as per api
    if 'source' in submitted_form:
        submitted_form['source_tracking_id'] = submitted_form.pop('source')[0]


    #convert "on/off" to "boolean" values expected by api
    booleans = ['us_citizen','first_registration','has_mailing_address',
                'change_of_name','change_of_address',
                'opt_in_sms','opt_in_email','opt_in_volunteer',
                'partner_opt_in_sms','partner_opt_in_email','partner_opt_in_volunteer']
    for b in booleans:
        if submitted_form.has_key(b):
            try:
                submitted_form[b] = int(submitted_form[b])
            except ValueError:
                if submitted_form.get(b) == "off":
                    submitted_form[b] = 0
                if submitted_form.get(b) == "on":
                    submitted_form[b] = 1

    #check for title and replace it if it's an invalid value
    if submitted_form.has_key('name_title'):
        title = submitted_form.get('name_title')
        if title not in ["Mr.", "Ms.", "Mrs.", "Sr.", "Sra.","Srta."]:
            submitted_form['name_title'] = "Mr." #guess, because we have to send valid data to API

    #check for suffix and clear it if it's an invalid value
    if submitted_form.has_key('name_suffix'):
        suffix = submitted_form.get('name_suffix')
        if suffix not in ["Jr.", "Sr.", "II", "III", "IV"]:
            submitted_form['name_suffix'] = ""

    #check for race and clear it if it's an invalid value
    if submitted_form.has_key('race'):
        race = submitted_form.get('race')
        if race not in ["American Indian / Alaskan Native", "Asian / Pacific Islander",
                        "Black (not Hispanic)", "Hispanic", "Multi-racial",
                        "White (not Hispanic)", "Other", "Decline to State",
                        "Indio Americano / Nativo de Alaska", "Asiatico / Islas del Pacifico",
                        "Negra (no Hispano)", "Hispano", "Blanca (no Hispano)", "Otra", "Declino comentar"]:
            submitted_form['race'] = "Other"
                    
    #submit to rocky
    rtv_response = rtv_proxy('POST',submitted_form,'/api/v2/gregistrations.json')
    if rtv_response.has_key('error'):
        return HttpResponseServerError(rtv_response)

    return HttpResponse('OK')

def error(request):
    return render_to_response('error.html', {}, context_instance=RequestContext(request))

def csrf_failure(request, reason=""):
    mail_admins('rocky error: csrf failure',"request: %s" % request)
    return render_to_response('403.html', {}, context_instance=RequestContext(request))

def share(request):
    return render_to_response('share.html', {}, context_instance=RequestContext(request))
