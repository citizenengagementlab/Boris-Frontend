from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseBadRequest

from registrant.models import Registrant,RegistrationProgress

def register(request):
    #determine form layout from get parameter
    layout = request.GET.get('layout')
    #catch typo
    if layout == "tab":
        layout = "tabs"
    if layout not in ['tabs','accordion','singlepage']:
        #invalid layout param, default to singlepage
        layout = None
    context = {'layout':layout}
    
    #TODO: setup partner_id based on layout
    context['partner_id'] = 1
    
    return render_to_response('form.html',context,
                context_instance=RequestContext(request))
                
def save_registrant(request):
    #save name,email,zip to our local db
    if request.method != "POST":
        return HttpResponseBadRequest('must post to save_registrant')
    else:
        try:
            post_data = {'first_name':request.POST['first_name'],
                         'last_name':request.POST['last_name'],
                         'email':request.POST['email_address'],
                         'zip_code':request.POST['zip_code']}
        except KeyError,e:
            return HttpResponseBadRequest(e)
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
    #returns a redirect to print
    return HttpResponse('submit not yet implemented')

def download(request):
    return HttpResponse('download not yet implemented')

def get_pdf(request):
    return HttpResponse('getpdf not yet implemented')
    
def finish(request):
    return render_to_response('finish.html',context_instance=RequestContext(request))