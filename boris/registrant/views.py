from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseBadRequest

from proxy.views import rtv_proxy
from registrant.models import Registrant,RegistrationProgress

def map(request):
    return render_to_response('map.html',{},
            context_instance=RequestContext(request))

def register(request):
    
    return render_to_response('form.html',context,
                context_instance=RequestContext(request))
                
def save_registrant(request):
    #save name,email,zip to our local db
    if request.method != "POST":
        return HttpResponseBadRequest('must post to save_registrant')
    else:
        try:
            post_data = {'email':request.POST['registrant[email_address]'],
                         'zip_code':request.POST['registrant[zip_code]'],
                         'layout':request.POST['registrant[layout]']}
        except KeyError,e:
            return HttpResponseBadRequest(e)
        try:
            post_data.update({'first_name':request.POST['registrant[first_name]'],
                              'last_name':request.POST['registrant[last_name]']})
        except KeyError,e:
            pass
        registrant = Registrant(**post_data)
        registrant.save()
        return HttpResponse('registrant saved')
    return HttpResponse('error')
    
def save_progress(request):
    if request.method != "POST":
        return HttpResponseBadRequest('must post to save_progress')
    else:
        try:
            registrant = Registrant.objects.filter(email=request.POST['email_address']).latest()
            progress = RegistrationProgress(field_name=request.POST['field_name'],
                         field_value=request.POST['field_value'],
                         registrant=registrant)
            progress.save()
        except KeyError,e:
            return HttpResponseBadRequest(e)
        return HttpResponse('progress saved')
    return HttpResponse('save_progress error')
    
def submit(request):
    if request.method != "POST":
        return redirect('/registrants/new')
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
