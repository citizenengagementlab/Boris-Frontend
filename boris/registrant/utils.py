from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.db.models import Count

from registrant.models import Registrant,RegistrationProgress

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