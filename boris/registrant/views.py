from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django.db.models import Count

from proxy.views import rtv_proxy
from registrant.models import Registrant,RegistrationProgress
import json

def register(request):
    #determine form layout from get parameter
    layout = request.GET.get('layout')
    #catch typo
    if layout == "tab":
        layout = "tabs"
    if layout not in ['tabs','accordion','singlepage']:
        #invalid layout param, default to singlepage
        layout = 'singlepage'
    context = {'layout':layout}
    
    #setup partner_id based on layout
    partner_ids = {'singlepage':11911,'tabs':11917,'accordion':11929}
    try:
        context['partner_id'] = partner_ids[layout]
    except KeyError:
        #default to RTV partner
        context['partner_id'] = 1
    
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
    
def stats(request):
    """Gets overall performance statistics by source for a given time period. Defaults to last month."""
    if not request.user.is_staff:
            return HttpResponseRedirect('/admin/?next=%s' % request.path)
    layouts = ['singlepage','accordion','tabs']
            
    context = {}
    context['num_started'] = Registrant.objects.filter(ignore=False).distinct('email').count()
    context['num_finished'] = RegistrationProgress.objects.filter(field_name="finished",field_value="True").count()
    try: 
    	context['avg_fields_completed'] = RegistrationProgress.objects.filter(registrant__ignore=False).\
                    count() / float(Registrant.objects.filter(ignore=False).distinct('email').count())
    except ZeroDivisionError:
    	context['avg_fields_completed'] = 0
    
    started_by_layout_list = Registrant.objects.filter(ignore=False).values('layout').\
                                annotate(lcount=Count('id')).order_by()
    #convert from a list to a dict
    started_by_layout = {}
    for l in started_by_layout_list:
        started_by_layout[l['layout']] = l['lcount']
    context['started_by_layout'] = started_by_layout
        
    finished_by_layout_list = RegistrationProgress.objects.filter(registrant__ignore=False,field_name="finished",field_value="True").\
                                    values('registrant__layout').annotate(lcount=Count('id')).order_by()
    finished_by_layout = {}
    for l in finished_by_layout_list:
        finished_by_layout[l['registrant__layout']] = l['lcount']
    context['finished_by_layout'] = finished_by_layout
    
    percent_by_layout = {}
    for l in layouts:
        try:
            finished = finished_by_layout[l]
        except KeyError:
            finished = 0
        try:
            started = started_by_layout[l]
        except KeyError:
            started = 0
        percent_by_layout[l] = 100*finished/float(started)
    context['percent_by_layout'] = percent_by_layout
    
    progress = {}
    for l in layouts:
        p_d = {}
        p_l = RegistrationProgress.objects.filter(registrant__ignore=False,registrant__layout=l).\
                        values('field_name').annotate(n=Count('id')).order_by()
        for p in p_l:
            try:
                p_d[p['field_name']] = p['n'] / float(started_by_layout[l])
            except ZeroDivisionError:
                p_d[p['field_name']] = 0
        progress[l] = p_d
    context['progress_by_layout'] = progress.items()
    context['layouts'] = layouts
    
    return render_to_response("stats.html",
                   context,RequestContext(request))