from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from proxy.views import rtv_proxy
from proxy.models import CustomForm,CoBrandForm

from django.contrib.localflavor.us import us_states
STATE_NAME_LOOKUP = dict(us_states.US_STATES)
STATE_NAME_LOOKUP['DC'] = "DC" #monkey patch, because "District of Columbia doesn't fit"

def get_branding(context):
    """Util method to get branding given partner id
    Returns dict with updated context"""

    #check for cobrand form first
    try:
        context['cobrandform'] = CoBrandForm.objects.get(partner_id=context['partner'])
        context['customform'] = context['cobrandform'].toplevel_org
        return context
    except (CoBrandForm.DoesNotExist,ValueError):

        #then custom form
        context['cobrandform'] = None
        try:
            context['customform'] = CustomForm.objects.get(partner_id=context['partner'])
            return context
        except (CustomForm.DoesNotExist,ValueError):
            context['customform'] = None
            return context
    return context

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
    if request.GET.get('partner'):
        context['partner'] = request.GET.get('partner')
        context = get_branding(context)
    if request.GET.get('source'):
        context['source'] = request.GET.get('source')

    return render_to_response('map.html',context,
            context_instance=RequestContext(request))

def start(request):
    "Simple form for initial user engagement"
    get_locale(request)

    context = {}
    if request.GET.get('partner'):
        context['partner'] = request.GET.get('partner')
        context = get_branding(context)
    if request.GET.get('source'):
        context['source'] = request.GET.get('source')

    return render_to_response('start.html',context,
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
        #hit rtv_proxy for staterequirements
        state = request.GET.get('state').upper()
        context['state'] = state
        try:
            context['state_name'] = STATE_NAME_LOOKUP[state]
        except KeyError:
            redirect_url = '/registrants/map/'
            if context['has_partner']:
                redirect_url = redirect_url + '?partner=' + context['partner']
            return redirect(redirect_url)

        #TODO: get language code from localeurl

        staterequirements = rtv_proxy('POST',{'home_state_id':state,'lang':locale},
            '/api/v2/state_requirements.json')
        context['staterequirements'] = staterequirements

        if staterequirements.has_key('error'):
            print staterequirements
            return render_to_response('ineligible.html',context,
                        context_instance=RequestContext(request))
    else:
        redirect_url = '/'
        if context['has_partner']:
                redirect_url = redirect_url + '?partner=' + context['partner']
        return redirect(redirect_url) #redirect to frontpage to do geolocation
    
    return render_to_response('form.html',context,
                context_instance=RequestContext(request))
    
def submit(request):
    "Submit the posted form to the Rocky API"
    get_locale(request)

    if request.method != "POST":
        return redirect('/registrants/new/')
    submitted_form = request.POST.copy()
    #make a mutable copy

    #delete csrf token
    if 'csrfmiddlewaretoken' in submitted_form:
        submitted_form.pop('csrfmiddlewaretoken')

    #rename source to partner_tracking_id as per api
    if 'source' in submitted_form:
        submitted_form['partner_tracking_id'] = submitted_form.pop('source')[0]
    
    #convert "on/off" to boolean values expected by api
    booleans = ['first_registration','has_mailing_address',
                'change_of_name','change_of_address',
                'opt_in_sms','opt_in_email','opt_in_volunteer',
                'partner_opt_in_sms','partner_opt_in_email','partner_opt_in_volunteer',
                'us_citizen','volunteer'] #volunteer is old syntax, remove when api is updated
    for b in booleans:
        if submitted_form.get(b) == "off":
            submitted_form[b] = '0'
        if submitted_form.get(b) == "on":
            submitted_form[b] = '1'
    
    #check for required values that aren't defined in the post
    required_fields = ['opt_in_sms','opt_in_email','us_citizen','id_number']
    for r in required_fields:
        if not submitted_form.has_key(r):
            #and fill it in with zero
            submitted_form[r] = '0'
    
    #check for suffix and clear it if it's an invalid value
    suffix = submitted_form.get('name_suffix')
    if suffix not in ["Jr.", "Sr.", "II", "III", "IV"]:
        submitted_form['name_suffix'] = ""
            
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
    context['email_address'] = submitted_form.get("email_address")

    try:
        context['state_name'] = STATE_NAME_LOOKUP[submitted_form.get('home_state_id')]
    except KeyError:
        #unrecognized state
        context['error'] = True
        messages.error(request, _("Unrecognized state, please go back and try again."))

    #if a partner, post to their api
    if submitted_form.has_key('partner_id') and bool(submitted_form['opt_in_email']) == True:
        branding = get_branding({'partner':submitted_form['partner_id']})
        if branding.get('cobrandform'):
            customform = branding['cobrandform'].toplevel_org
        elif branding.get('customform'):
            customform = branding['customform']
        else:
            customform = None

        if customform:
            response = customform.submit(submitted_form)
            if response.get('error'):
                context['error'] = True
                messages.error(request, _("Unknown error, please contact an admin"),
                    extra_tags=response)

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

def error(request):
    get_locale(request)
    return render_to_response('error.html', {}, context_instance=RequestContext(request))
