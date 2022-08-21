from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import UserProfile

from .forms import UserLoginForm, UserSignUpForm, UserEditProfileForm


def accontView(request):
    return render(request, "user/login-register.html")


def editUsuProfile(request):
    return render(request, "user/edit-profile.html")


def editProfile_view(request):
    obj = UserProfile.objects.get(email=request.user.email)
    edit_form = UserEditProfileForm(request.POST, request.FILES, instance=obj or None)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, 'Se guardaron los datos correctamente')
        return redirect('users:edit-profile')
    else:
        messages.error(request, edit_form.errors)
        return redirect('users:edit-profile')


def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            messages.warning(
                request, login_form.errors)
            return redirect('users:userlogin')

    messages.error(request, login_form.errors)
    return redirect('users:userlogin')


def signup_view(request):
    signup_form = UserSignUpForm(request.POST, request.FILES or None)
    if signup_form.is_valid():
        profile_pic = signup_form.cleaned_data.get('profile_pic')
        username = signup_form.cleaned_data.get('username')
        email = signup_form.cleaned_data.get('email')
        first_name = signup_form.cleaned_data.get('first_name')
        last_name = signup_form.cleaned_data.get('last_name')
        phone = signup_form.cleaned_data.get('phone')
        id_rol = signup_form.cleaned_data.get('id_rol')
        password = signup_form.cleaned_data.get('password')
        try:
            user = get_user_model().objects.create(
                profile_pic=profile_pic,
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                id_rol=id_rol,
                password=make_password(password),
                is_active=True
            )
            login(request, user)
            return redirect('home:home')

        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})
    else:
        messages.error(request, signup_form.errors)
        return redirect('users:userlogin')


def logout_view(request):
    logout(request)
    return redirect('home:home')


@login_required(login_url='home:home')
def profile_view(request):
    return render(request, 'user/profile.html')
