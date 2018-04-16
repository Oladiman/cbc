from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from .forms import UserLoginForm, UserRegisterForm, UserForm


from django.db.models import Q

# Create your views here.

@login_required()
def edit_user(request, username):
    user = User.objects.get(username=username)
    user_form = UserForm(instance=user)
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('bio',
                                                                                'phone', 'campus', 'state', 'picture',
                                                                                'country'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect('/')

        return render(request, "account_update.html", {
            # "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied

# @login_required()
# def profile_view(request):
#     the_user = request.user
#     following_ = the_user.amfollowing.all()
#     followers_ = the_user.myfollowers.all()
#     followers = [i.follower for i in followers_]
#     the_list = [i.following for i in following_]
#     the_posts = Post.objects.filter(user__in=the_list).order_by('-timestamp')[:3]

#     return render(request, 'profile2.html', {'friendP':the_posts, 'following': the_list, 'followers': followers})

def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    return render(request, "login.html", {"form": form, "title": title})


def register_view(request):
    next = request.GET.get('next')
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        "form": form,
        "title": title
    }
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')