from django import template
from shirts.models import *
from math import floor

register = template.Library()

@register.simple_tag
def prices(tshirt):
    prices = tshirt.sizevariant_set.all().order_by('price').first()
    return prices.price


@register.simple_tag
def discount(tshirt):
    price = prices(tshirt)
    discount = tshirt.discount
    return floor(price - (price * (discount/100)))

@register.simple_tag
def get_active_size_btn_class(active_size, size):
    if active_size == size:
        return "primary"
    
    return "light"    

@register.simple_tag
def multiply(a, b):
    return a*b

@register.simple_tag
def sale_price(price, discount): #for cart sale price
    return floor(price - (price * (discount/100)))

@register.filter
def cart_total_price(cart): #for cart total price
    total = 0
    for c in cart:
        discount = c.get('tshirt').discount
        price = c.get('size').price
        final_price = sale_price(price, discount)
        total_of_single_product = final_price * c.get('quantity')
        total = total + total_of_single_product
    return total

