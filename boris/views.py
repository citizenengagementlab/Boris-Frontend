from django.template import RequestContext
from django.shortcuts import render_to_response,redirect

def frontpage(request):
    return redirect('/registrants/new/')

def register(request):
    return render_to_response('form.html',context_instance=RequestContext(request))