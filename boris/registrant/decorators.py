from functools import wraps
from django.utils.decorators import available_attrs

def capture_get_parameters(params):
    """
    Decorator to capture get parameters to session

    @capture_get_parameters(["email_address", "state"])
    def my_view(request):
    # all named get parameters are now available in request.session

    """
    def decorator(view):
        @wraps(view, assigned=available_attrs(view))
        def inner(request, *args, **kwargs):
            for p in params:
                request.session[p] = request.GET.get(p)
            return view(request, *args, **kwargs)
        return inner
    return decorator

def capture_locale(view):
    """
    Decorator to determine locale from request. Checks session first, then get parameter.
    Sets session['django_language'] and session['locale'] to language code.
    Defaults to 'en'

    @get_locale
    def my_view(request):
    # all named get parameters are now available in request.session

    """
    @wraps(view)
    def inner(request, *args, **kwargs):
        if request.GET.get('locale'):
            locale = request.GET['locale']
        elif request.session.has_key('django_language'):
            locale = request.session['django_language']
        else:
            #default to english
            locale = "en"
        request.LANGUAGE_CODE = locale
        request.session['django_language'] = locale
        return view(request, *args, **kwargs)
    return inner

def capture_partner(view):
    """
    Decorator to determine branding from request get parameters
    Sets session partner and source

    @capture_partner
    def my_view(request):
    # partner id now in request.session

    """
    @wraps(view)
    def inner(request, *args, **kwargs):
        if request.GET.get('partner'):
            request.session['partner'] = request.GET.get('partner')
        if request.GET.get('source'):
            request.session['source'] = request.GET.get('source')

        return view(request, *args, **kwargs)
    return inner