from django.http import HttpResponseForbidden

def user_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_users:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied.")
    return _wrapped_view
