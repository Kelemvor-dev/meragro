from django.shortcuts import render

import random

from products.models import Product


# Create your views here.

def homeView(request):
    products = Product.objects.order_by('?')[:6]
    return render(request, "home.html", {'products': products})
