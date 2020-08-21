from django.shortcuts import render


def checkout(request):
    """View returning checkout page and processing payment logic"""

    return render(request, 'checkout/checkout.html')
