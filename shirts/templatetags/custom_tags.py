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
