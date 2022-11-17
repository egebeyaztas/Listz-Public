from django.http.response import JsonResponse
from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.views import LoginView, SignupView
from allauth.account import urls
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from authz.decorators import allowed_users
from authz.models import Profile
from django.contrib.auth.models import User
from authz.forms import ProfileUpdateForm
from django.http import HttpResponse
from django.conf import settings
from lists.models import List

# Create your views here.
@login_required(login_url="account_login")
#@allowed_users(allowed_roles=["admin"])
def admin_dashboard_view(request):
    user_profile = Profile.objects.filter(user=request.user)
    context = {
        'profile': user_profile,
    }

    return render(request, "listz/dashboards/admin_dashboard.html", context)

@login_required(login_url="account_login")
#@allowed_users(allowed_roles=["editor", "admin"])
def editor_dashboard_view(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, "listz/dashboards/editor_dashboard.html",context)

def welcome_page(request):

    return render(request, "listz/auth/welcome.html")

@login_required(login_url="account_login")
def user_profile(request, user_name):
    if request.user.profile:
        user_profile = Profile.objects.get(user__username=user_name)
        #print(user_profile)
    else:
        return HttpResponse("You don't have a profile")
    form = ProfileUpdateForm( 
                initial = {
                    'name': user_profile.name,
                    'country': user_profile.country,
                    'bio': user_profile.bio,
                    'profile_picture': user_profile.profile_picture,
                }
            )
    context = {'profile': user_profile, 'form': form}

    return render(request, 'listz/profile/profile.html', context)

'''This function gets an ajax request and 
    returns a html with content of watchlists as a response.'''
@login_required(login_url="account_login")
def get_watchlists_for_profile(request):
    if request.method == 'GET' and request.is_ajax():
        keyword = [key for key in request.GET.dict().keys()][0]
        if keyword == 'yours':
            lists = List.objects.filter(type='Editor')
        elif keyword == 'followed':
            lists = List.objects.filter(type='Editor')[:2]
        context = {'watchlists': lists}

        html = render_to_string('listz/profile/profile_watchlist_content.html', context)
        return JsonResponse(html, safe=False)


@login_required(login_url="account_login")
def update_profile(request, *args, **kwargs):
    form = ProfileUpdateForm()
    print(request.user)
    if request.user.profile:
        profile = Profile.objects.get(user__id=request.user.id)
    else:
        return HttpResponse("something went wrong.")
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_name=request.user.username)
        else:
            form = ProfileUpdateForm(instance=profile, 
                initial = {
                    'name': profile.name,
                    'country': profile.country,
                    'bio': profile.bio,
                    'profile_picture': profile.profile_picture,
                }
            )
    else:
        form = ProfileUpdateForm( 
                initial = {
                    'name': profile.name,
                    'country': profile.country,
                    'bio': profile.bio,
                    'profile_picture': profile.profile_picture,
                }
            )

    context = {'form': form }
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

    return render(request, 'listz/profile/profile_update.html', context)
