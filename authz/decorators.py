from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator_func(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(request.user.groups.all()[0].name)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to see this page.")
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator_func