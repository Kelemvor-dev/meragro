import uuid

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import Product, Category, ShoppingCart

from .forms import CreateProductForm, EditProductForm
from users.models import UserProfile


def ProductsView(request):
    products = Product.objects.all()
    categories = Category.objects.all().order_by('name')
    return render(request, "product/products.html", {'products': products, 'categories': categories})


@login_required(login_url='home:home')
def CreateProductView(request):
    return render(request, "product/create_product.html")


def ShowProductView(request, id):
    product = Product.objects.get(id=id)
    sku = str(uuid.uuid4().fields[-1])[:5] + 'ID' + id
    return render(request, "product/show_product.html", {'product': product, 'sku': sku})


def EditProductView(request, id):
    product = Product.objects.get(id=id)
    editProduct_form = EditProductForm(initial={
        'title': product.title,
        'image': product.image,
        'content': product.content,
        'price': product.price,
        'id_category': product.id_category
    })
    return render(request, "product/edit_product.html", {'editProduct_form': editProduct_form, 'product': product})


def SaveProductView(request):
    crateProduct_form = CreateProductForm(request.POST, request.FILES or None)
    user = UserProfile.objects.get(pk=request.user.id)
    if crateProduct_form.is_valid():
        image = crateProduct_form.cleaned_data.get('image')
        title = crateProduct_form.cleaned_data.get('title')
        content = crateProduct_form.cleaned_data.get('content')
        price = crateProduct_form.cleaned_data.get('price')
        id_category = crateProduct_form.cleaned_data.get('id_category')
        id_user_id = user
        try:
            Product.objects.create(
                image=image,
                title=title,
                content=content,
                price=price,
                id_category=id_category,
                id_user=id_user_id,
            )
            messages.success(request, 'Se guardaron los datos correctamente')
            return redirect('users:profile')
        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})
    else:
        messages.error(request, crateProduct_form.errors)
        return redirect('users:profile')


def SaveEditProductView(request, id):
    product = Product.objects.get(id=id)
    editProduct_form = EditProductForm(request.POST, request.FILES or None, instance=product)
    if editProduct_form.is_valid():
        editProduct_form.save()
        messages.success(request, 'Se guardaron los datos correctamente')
        return redirect('users:profile')
    else:
        messages.error(request, editProduct_form.errors)
        return redirect('users:profile')


def DeleteProductView(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Se eliminaron los datos correctamente')
    return redirect('users:profile')


def SaveShoppingCart(request, idProduct):
    idUser = UserProfile.objects.get(pk=request.user.id)
    product = Product.objects.get(id=idProduct)
    if request.method == "POST":
        amount = request.POST['amount']
        unit_price = request.POST['unit_price']
        sku = request.POST['sku']
        id_product = product
        id_user = idUser
        try:
            ShoppingCart.objects.create(
                amount=amount,
                unit_price=unit_price,
                sku=sku,
                id_product=id_product,
                id_user=id_user,
            )
            messages.success(request, 'Has añadido el producto a tu carrito de compras')
            return redirect('/showProduct/' + idProduct)
        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})
    else:
        messages.error(request, "Hay un error en la petición")
        return redirect('products:showProduct/' + idProduct)
