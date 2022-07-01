from django.contrib.auth.decorators import login_required
from config.settings import base
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

EXEMPT_URLS = [base.LOGIN_URL.lstrip('/')]
if hasattr(base, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [url for url in base.LOGIN_EXEMPT_URLS]


def login_exempt(view):
    view.login_exempt = True
    return view


def permission_required(perm):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm

        if not user.is_authenticated:
            return False

        if len(perms) == 1 and len(perms[0]) == 0:
            return True

        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        raise PermissionDenied

    return user_passes_test(check_perms, login_url=base.LOGIN_URL)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        if request.user.is_authenticated:
            pass

        if not request.user.is_authenticated:
            if path not in EXEMPT_URLS:
                return login_required(view_func)(request, *view_args, **view_kwargs)
            return
