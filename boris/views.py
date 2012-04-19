from django.template import RequestContext
from django.shortcuts import render_to_response,redirect

def frontpage(request):
    return redirect('/registrants/new/')

def register(request):
    return render_to_response('form.html',context_instance=RequestContext(request))
    
def finish(request):
    return render_to_response('finish.html',context_instance=RequestContext(request))
    
def rtv_iframe_test(request):
    layout = request.GET.get('layout')
    context = {'layout':layout}
    return render_to_response('rtv_iframe_test.html',context,
                context_instance=RequestContext(request))