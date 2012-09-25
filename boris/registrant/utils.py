from proxy.models import CustomForm,CoBrandForm
from proxy.views import rtv_proxy
from django.core.mail import mail_admins

def get_branding(context):
    """Util method to get branding given partner id.
    Used in submit view, because we need access before the context processor runs.
    Not totally DRY, but better than faking an HttpRequest."""

    #check for cobrand form first
    try:
        context['cobrandform'] = CoBrandForm.objects.get(partner_id=context['partner'])
        context['customform'] = context['cobrandform'].toplevel_org
        return context
    except (CoBrandForm.DoesNotExist,ValueError):
        pass

    #then custom form
    context['cobrandform'] = None
    try:
        context['customform'] = CustomForm.objects.get(partner_id=context['partner'])
        return context
    except (CustomForm.DoesNotExist,ValueError):
        pass

    #finally, try rtv whitelabel
    try:
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

        #unlike in context_processor, this needs to be object-like
        #so create a CustomForm, but don't save it
        fakin_bacon = CustomForm(**quack)
        context['customform'] = fakin_bacon
    except KeyError:
        #whitelabel error, never mind
        mail_admins("white label error, id %s" % context['partner'], "rtv_whitelabel:%s\n" % rtv_whitelabel)

    return context

def empty(the_list):
    #returns True if list has only one object, and it's empty or otherwise False-y
    #need this because the submitted_form is a dict of lists, not a dict of values
    #could be as simple as not bool(the_list[0]), but let's be more explicit...
    if len(the_list) == 0:
        return True
    try:
        elem = the_list[0]
        if bool(elem):
            return False
        else:
            return True
    except IndexError:
        return False

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)