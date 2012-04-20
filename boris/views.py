from django.template import RequestContext
from django.shortcuts import render_to_response,redirect

def frontpage(request):
    return redirect('/registrants/new/')

def rtv_iframe_test(request):
    layout = request.GET.get('layout')
    context = {'layout':layout}
    return render_to_response('rtv_iframe_test.html',context,
                context_instance=RequestContext(request))
                
def submit(request):
	return render_to_response('submit.html', context_instance=RequestContext(request))