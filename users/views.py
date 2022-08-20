from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserLoginForm, UserSignUpForm


def accontView(request):
    return render(request, "user/login-register.html")

def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesion correctamente')
            return redirect('home:home')
        else:
            messages.warning(
                request, 'Correo Electronico o Contrasena invalida')
            return redirect('home:home')

    messages.error(request, 'Formulario Invalido')
    return redirect('home:home')


def signup_view(request):
    signup_form = UserSignUpForm(request.POST or None)
    if signup_form.is_valid():
        username = signup_form.cleaned_data.get('username')
        email = signup_form.cleaned_data.get('email')
        first_name = signup_form.cleaned_data.get('first_name')
        last_name = signup_form.cleaned_data.get('last_name')
        phone = signup_form.cleaned_data.get('phone')
        id_rol = signup_form.cleaned_data.get('id_rol')
        password = signup_form.cleaned_data.get('password')
        try:
            user = get_user_model().objects.create(
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


def logout_view(request):
    logout(request)
    return redirect('home:home')


@login_required(login_url='home:home')
def profile_view(request):
    return render(request, 'user/profile.html')

