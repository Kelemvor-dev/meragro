from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('createProduct/', views.CreateProductView, name='createProduct'),
    path('saveProduct/', views.SaveProductView, name='saveProduct'),
]
