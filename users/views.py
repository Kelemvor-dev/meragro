from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import UserProfile

from .forms import UserLoginForm, UserSignUpForm, UserEditProfileForm
from products.models import Product, Orders, ShoppingCart


def accontView(request):
    return render(request, "user/login-register.html")


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
            return redirect('users:profile')
        else:
            messages.warning(request, 'Usuario o contraseña incorrectos')
            return redirect('users:userlogin')
    else:
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


# Los estados son 0 = carrito de compras, 1 = Producto Solicitado para comprar, 2 = Finalizacion de la compra del producto, 3 = Producto cancelado
@login_required(login_url='home:home')
def profile_view(request):
    user_id = UserProfile.objects.get(pk=request.user.id)
    products = Product.objects.filter(id_user_id=user_id)
    orders = Orders.objects.filter(id_user_id=user_id)
    # Productos del perfil Comprador con estado diferente de 0
    productsOrder = Orders.objects.raw(
        "select po.id, pp.title, po.register_date, pois.orders_id as order_id, ps.amount, ps.unit_price, ps.state from products_orders po  \n" +
        "inner join products_orders_id_shoppingcart pois on pois.orders_id = po.id \n" +
        "inner join products_shoppingcart ps on pois.shoppingcart_id = ps.id \n" +
        "inner join products_product pp on pp.id = ps.id_product_id \n" +
        "where ps.state = 1 or ps.state = 2 or ps.state = 3")
    # productos del perfil vendedor para finalizar su venta con estado diferente de 0
    productsSellOrder = Orders.objects.raw(
        "select ps.id, pp.title, pp.image, ps.amount, ps.unit_price, ps.register_date, ps.state, uu.first_name, uu.last_name, uu.phone  \n" +
        "from products_product pp  \n" +
        "inner join products_shoppingcart ps on pp.id = ps.id_product_id  \n" +
        "inner join users_userprofile uu on uu.id = ps.id_user_id  \n" +
        "where pp.id_user_id = %s and ps.state != 0 order by uu.id ", [request.user.id])
    return render(request, 'user/profile.html', {
        'products': products,
        'orders': orders,
        'productsOrder': productsOrder,
        'productsSellOrder': productsSellOrder
    })


def editUsuProfile(request):
    return render(request, "user/edit-profile.html")
