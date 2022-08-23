from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import Product

from .forms import CreateProductForm
from users.models import UserProfile


@login_required(login_url='home:home')
def CreateProductView(request):
    return render(request, "product/create_product.html")


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
