from proxy.models import CustomForm,CoBrandForm

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
    except (CustomForm.DoesNotExist,ValueError):
        context['customform'] = None

    #finally, try rtv whitelabel
    #TODO

    return context