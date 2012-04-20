from django.template import RequestContext
from django.shortcuts import render_to_response,redirect

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
                
def get_started_save(request):
    #save name,email,zip to our local db
    return HttpResponse('get_started_save not yet implemented')
    
def submit(request):
    #actually hits the rtv api
    #returns a redirect to print
    return HttpResponse('submit not yet implemented')

def download(request):
    return HttpResponse('download not yet implemented')

def get_pdf(request):
    return HttpResponse('getpdf not yet implemented')
    
def finish(request):
    return render_to_response('finish.html',context_instance=RequestContext(request))