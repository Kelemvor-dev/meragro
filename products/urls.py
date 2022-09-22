from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [

    # Modulo Productos
    path('productsList', views.ProductsView, name='productsList'),
    path('createProduct/', views.CreateProductView, name='createProduct'),
    path('saveProduct/', views.SaveProductView, name='saveProduct'),
    path('editProduct/<id>', views.EditProductView, name='editProduct'),
    path('saveEditProduct/<id>', views.SaveEditProductView, name='saveEditProduct'),
    path('showProduct/<id>', views.ShowProductView, name='showProduct'),
    path('deleteProduct/<id>', views.DeleteProductView, name='deleteProduct'),

    # Modulo Carrito de Compras
    path('showCart', views.ShowCartView, name='showCart'),
    path('saveShoppingCart/<idProduct>', views.SaveShoppingCart, name='saveShoppingCart'),
    path('cartSuccess', views.cartSuccessView, name='cartSuccess'),
    path('deleteCartProduct/<id>', views.DeleteCartProductView, name='deleteCartProduct'),
    path('shopCartProduct/<id>', views.ShopCartProductView, name='shopCartProduct'),
    path('cancelCartProduct/<id>', views.CancelCartProductView, name='cancelCartProduct'),

    # Modulo PQR
    path('saveQuestion/<idP>', views.SaveQuestion, name='saveQuestion'),
    path('saveAsnwer/<idQ>/<idP>', views.SaveAsnwer, name='saveAsnwer'),


]
