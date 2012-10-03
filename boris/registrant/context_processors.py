from proxy.models import CustomForm,CoBrandForm
from proxy.views import rtv_proxy
from django.core.cache import cache
from django.core.mail import mail_admins

def facebook(request):
    """Context processor to add facebook partner & source from session"""
    context = {}
    
    if request.session.has_key('facebook_canvas'):
        if request.session.has_key('facebook_partner_id'):
            context['partner'] = request.session['facebook_partner_id']
        else:
            #use facebook default
            context['partner'] = 19093

        #if not already a source, add it
        if not request.GET.get('source') and request.session.has_key('facebook_source'):
            context['source'] = request.session['facebook_source']
    return context

def whitelabel(request):
    """
    Context processor to add customform and cobrandform to request.session
    Checks proxy CoBrandForm, then CustomForm, then rocky whitelabel API
    """
    context = {}

    #save partner & source
    if request.GET.get('partner'):
        partner = request.GET.get('partner')
        context['partner'] = partner
    elif not context.has_key('partner'):
        #no partner specified, return early
        context['partner'] = 1
        return context

    if request.GET.get('source'):
        source = request.GET.get('source')
        context['source'] = source

    #get whitelabel branding
    #try CoBrandForm first
    try:
        cobrand = CoBrandForm.objects.get(partner_id=partner)
        context['cobrandform'] = cobrand
        context['customform'] = cobrand.toplevel_org
        return context
    except (CoBrandForm.DoesNotExist,ValueError):
        pass

    #no CoBrandForm, try CustomForm
    context['cobrandform'] = None
    try:
        context['customform'] = CustomForm.objects.get(partner_id=partner)
        return context
    except (CustomForm.DoesNotExist,ValueError):
        context['customform'] = None

    try:
        #finally, try rtv whitelabel

        #check cache first
        cache_key = 'rtv_whitelabel_%s' % context['partner']
        if cache.get(cache_key):
            rtv_whitelabel = cache.get(cache_key)
        else:
            rtv_whitelabel = rtv_proxy('GET',{'partner_id':context['partner']},
            'api/v2/partnerpublicprofiles/partner.json')
            cache.set(cache_key,rtv_whitelabel,3600) #cache whitelabel hits for an hour
    
        #duck type a customform
        quack = {'partner_id':context['partner'],
                 'name':rtv_whitelabel['org_name'],
                 'logo':rtv_whitelabel['logo_image_URL'],
                 'logo_link':rtv_whitelabel['org_URL'],
                 'show_sms_box':rtv_whitelabel['partner_ask_sms_opt_in'],
                 'show_volunteer_box':rtv_whitelabel['rtv_ask_volunteer'],
                 }
        if request.LANGUAGE_CODE == "es":
            quack['question_1'] = rtv_whitelabel['survey_question_1_es']
            quack['question_2'] = rtv_whitelabel['survey_question_2_es']
        else:
            quack['question_1'] = rtv_whitelabel['survey_question_1_en']
            quack['question_2'] = rtv_whitelabel['survey_question_2_en']

        #check for missing logo image url
        if '/logos/original/missing.png' in quack['logo']:
            quack['logo'] = None
        context['rtv_whitelabel'] = True
        context['customform'] = quack

    except KeyError,e:
        pass
        #whitelabel error, never mind
        #mail_admins("white label error, id %s" % context['partner'],
        #    "key error:%s\n,rtv_whitelabel:%s\n" % (e,rtv_whitelabel))

    return context