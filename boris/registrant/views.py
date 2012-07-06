from django.template import RequestContext
from django.shortcuts import render_to_response,redirect

from proxy.views import rtv_proxy
from proxy.models import CustomForm

from django.contrib.localflavor.us import us_states
STATE_NAME_LOOKUP = dict(us_states.US_STATES)

def map(request):
    context = {}
    if request.GET.get('partner'):
        context['partner'] = request.GET.get('partner')
    if request.GET.get('source'):
        context['source'] = request.GET.get('source')

    return render_to_response('map.html',context,
            context_instance=RequestContext(request))

def register(request):
    context = {}
    #setup partner id based on get parameter
    if 'partner' in request.GET:
        context['partner'] = request.GET.get('partner')
        try:
            context['customform'] = CustomForm.objects.get(partner_id=context['partner'])
        except (CustomForm.DoesNotExist,ValueError):
            context['customform'] = None
            context['partner'] = 9937
    else:
        #use CEL default
        context['partner'] = 9937

    if request.GET.get('source'):
        context['source'] = request.GET.get('source')

    #set state based on get parameter
    if 'state' in request.GET:
        #hit rtv_proxy for staterequirements
        state = request.GET.get('state')
        #TODO: get language code from localeurl
        staterequirements = rtv_proxy('POST',{'home_state_id':state,'lang':'en'},'/api/v1/state_requirements.json')
        context['staterequirements'] = staterequirements
        context['state'] = state
        context['state_name'] = STATE_NAME_LOOKUP[state]
        if staterequirements.has_key('error'):
            return render_to_response('ineligible.html',context,
                        context_instance=RequestContext(request))
    else:
        return redirect('/') #redirect to frontpage to do geolocation
    
    return render_to_response('form.html',context,
                context_instance=RequestContext(request))
    
def submit(request):
    if request.method != "POST":
        return redirect('/registrants/new/')
    submitted_form = request.POST.copy()
    #make a mutable copy

    #delete csrf token
    if 'csrfmiddlewaretoken' in submitted_form:
        submitted_form.pop('csrfmiddlewaretoken')

    #delete source, but save it for later
    #HACK: because the API isn't accepting it as a parameter
    saved_source = None
    if 'source' in submitted_form:
        saved_source = submitted_form.pop('source')
    
    #convert "on/off" to boolean values expected by api
    booleans = ['first_registration','has_mailing_address',
                'change_of_name','change_of_address',
                'opt_in_sms','opt_in_email','us_citizen']
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
    rtv_response = rtv_proxy('POST',submitted_form,'/api/v1/registrations.json')

    context = {}
    if rtv_response.has_key('pdfurl'):
        context['pdfurl'] = rtv_response['pdfurl']
    if rtv_response.has_key('error'):
        #something went wrong that wasn't caught in the frontend validation
        #clean up error message for human consumption
        try:
            field_name = rtv_response['error']['field_name'].replace('_',' ').title()
            message = rtv_response['error']['message'].lower()
            context['error'] = "%s %s" % (field_name, message)
        except KeyError:
            context['error'] = "Looks like we've gone sideways"
    context['email_address'] = submitted_form.get("email_address")

    #if a partner, post to their api
    if submitted_form.has_key('partner_id'):
        try:
            customform = CustomForm.objects.get(partner_id=submitted_form['partner_id'])
            response = customform.submit(submitted_form)
            if response.get('error'):
                #something went wrong...
                # email admin?
                print response
        except (CustomForm.DoesNotExist,ValueError):
            pass

    context['state_name'] = STATE_NAME_LOOKUP[submitted_form.get('home_state_id')]

    #send user values to context, for trackable social media links
    context['partner'] = submitted_form.get('partner_id')
    if saved_source:
        context['source'] = saved_source
    #TODO, what user id should we use?
    #some hash of email and partner_id?
    context['user_id'] = "TBD"

    return render_to_response('submit.html', context, context_instance=RequestContext(request))
