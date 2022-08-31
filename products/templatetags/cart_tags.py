from django import template
from django.db.models import Count
from products.models import ShoppingCart

register = template.Library()


@register.inclusion_tag('cart/head_cart.html')
def headerCart(userId):
    products = ShoppingCart.objects.select_related('id_product').filter(id_user_id=userId)
    count = ShoppingCart.objects.select_related('id_product').filter(id_user_id=userId).aggregate(Count('id_product'))
    price = 0
    for product in products:
        price = price + product.amount * product.unit_price

    return {
        'carts': ShoppingCart.objects.select_related().filter(id_user_id=userId),
        'totalPrice': price,
        'countProduct': count
    }
