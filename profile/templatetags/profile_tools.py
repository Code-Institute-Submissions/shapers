from django import template
from checkout.models import OrderLineProduct


register = template.Library()


@register.filter(name='multiply')
def multiply(a, b):
    return a * b


@register.filter(name='printqty')
def printqty(lineproducts):
    """
    Iterate through order's lineproducts and returns the total number of prints

    :return: Total number of items print
    """

    prints = 0
    for lineproduct in lineproducts:
        line = OrderLineProduct.objects.get(pk=lineproduct.id)
        prints += line.quantity
    return prints
