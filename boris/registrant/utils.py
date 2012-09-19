from proxy.models import CustomForm,CoBrandForm

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

        #then custom form
        context['cobrandform'] = None
        try:
            context['customform'] = CustomForm.objects.get(partner_id=context['partner'])
            return context
        except (CustomForm.DoesNotExist,ValueError):
            context['customform'] = None
            return context
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