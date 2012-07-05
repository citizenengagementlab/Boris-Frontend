from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseBadRequest

from proxy.views import rtv_proxy
from registrant.models import Registrant,RegistrationProgress

def map(request):
    return render_to_response('map.html',{},
            context_instance=RequestContext(request))

def register(request):
    context = {}
    #setup partner_id based on get parameter
    if 'partner_id' in request.GET:
        context['partner_id'] = request.GET.get('partner_id')
    else:
        #use CEL default
        context['partner_id'] = 9937

    #set state based on get parameter
    if 'state' in request.GET:
        #hit rtv_proxy for staterequirements
        state = request.GET.get('state')
        #TODO: get language code from localeurl
        staterequirements = rtv_proxy('POST',{'home_state_id':state,'lang':'en'},'/api/v1/state_requirements.json')
        context['staterequirements'] = staterequirements
        context['state'] = state
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
            
    #hit the api
    #todo, do this async?
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
    return render_to_response('submit.html', context, context_instance=RequestContext(request))
    
def finish(request):
    return render_to_response('finish.html',context_instance=RequestContext(request))
