from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('createProduct/', views.CreateProductView, name='createProduct'),
    path('saveProduct/', views.SaveProductView, name='saveProduct'),
    path('editProduct/<id>', views.EditProductView, name='editProduct'),
    path('saveEditProduct/<id>', views.SaveEditProductView, name='saveEditProduct'),
    path('showProduct/<id>', views.ShowProductView, name='showProduct'),
    path('deleteProduct/<id>', views.DeleteProductView, name='deleteProduct'),
]
