from proxy.models import CustomForm,CoBrandForm
from proxy.views import rtv_proxy
from django.core.mail import mail_admins

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
    else:
        #no partner specified, return early
        return {}

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
        rtv_whitelabel = rtv_proxy('GET',{'partner_id':context['partner']},
        'api/v2/partnerpublicprofiles/partner.json')
        #cache these?
    
        #duck type a customform
        quack = {'partner_id':context['partner'],
                 'name':rtv_whitelabel['org_name'],
                 'logo':rtv_whitelabel['logo_image_URL'],
                 'logo_link':rtv_whitelabel['org_URL'],
                 'show_sms_box':rtv_whitelabel['partner_ask_sms_opt_in'],
                 'show_volunteer_box':rtv_whitelabel['rtv_ask_volunteer'],
                 'question_1':rtv_whitelabel['survey_question_1_en'],
                 'question_2':rtv_whitelabel['survey_question_2_en'],
                 }

        #check for missing logo image url
        if '/logos/original/missing.png' in quack['logo']:
            quack['logo'] = None
        context['rtv_whitelabel'] = True
        context['customform'] = quack

    except KeyError:
        #whitelabel error, never mind
        mail_admins("white label error, id %s" % context['partner'], "rtv_whitelabel:%s\n" % rtv_whitelabel)

    return context