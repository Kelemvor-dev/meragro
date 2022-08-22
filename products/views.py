from django.shortcuts import render


def ProductUserView(request):
    return render(request, "product/product_user.html")
