from django.shortcuts import redirect
from functools import wraps

def app2_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or 'app2_user' not in request.session:
            return redirect('app2:login')
        return view_func(request, *args, **kwargs)
    return wrapper