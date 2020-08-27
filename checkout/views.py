from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from django.contrib import messages
from .forms import OrderForm
from .models import Order
from profile.models import UserProfile
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import OrderLineProduct
from django.conf import settings
import stripe
from cart.context import cart_content as cc
import json
from django.views.decorators.http import require_POST


@require_POST
def add_checkout_metadata(request):
    """
    Add Metadata into Stripe Payment Intent for Webhook process

    :return: Payment Intent with cart_content, user & checkout time
    """

    try:
        pid = request.POST.get('stripeClientSKey').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe.PaymentIntent.modify(pid, metadata={
            'cart_content': json.dumps(request.session.get('cart', {})),
            'username': request.user.username,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, "Sorry we couldn't process your payment. "
                                "Please try again later or contact us")
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
    """View returning checkout page and processing payment logic"""

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.user.is_anonymous:
        messages.error(request, 'You need to be logged in to proceed.')
        return redirect('account_login')

    cart_content = request.session.get('cart', {})

    if not cart_content:
        messages.error(request, "Your cart is empty ! Add something in ;)")
        return redirect(reverse('store'))

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_process = order_form.save(commit=False)
            user_profile = UserProfile.objects.get(user=request.user)
            order_process.user_profile = user_profile
            order_process.save()

            for product_id, quantity in cart_content.items():
                try:
                    product = Product.objects.get(id=product_id)
                    OrderLineProduct.objects.create(
                        order=order_process,
                        product=product,
                        quantity=quantity
                    )

                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "We couldn't process your order. You have not "
                        "been charged. Please try again or contact us.")
                    order_process.delete()
                    return redirect(reverse('get_cart'))

            messages.success(request,
                             "Your order has been placed successfully. "
                             "You will receive an email shortly.")

            return redirect('checkout_success',
                            order_number=order_process.order_number)

    else:
        user_profile = UserProfile.objects.get(user=request.user)
        order_form = OrderForm(initial={
            'full_name': f'{user_profile.user.first_name} '
                         f'{user_profile.user.last_name}'.strip(),
            'email': request.user.email,
            'phone_number': user_profile.profile_phone_number,
            'street_address1': user_profile.profile_street_address1,
            'street_address2': user_profile.profile_street_address2,
            'postcode': user_profile.profile_postcode,
            'town_or_city': user_profile.profile_town_or_city,
            'country': user_profile.profile_country,
        })

        current_cart = cc(request)
        total_charge = round(current_cart['cart_total'] * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=total_charge,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'cart_content': json.dumps(cart_content),
                'username': request.user.username,
            }
        )

        context = {
            'order_form': order_form,
            'cart_content': cart_content,
            'spk': stripe_public_key,
            'scsk': intent.client_secret,
        }

        return render(request, 'checkout/checkout.html', context=context)


def checkout_success(request, order_number):
    """View returning success payment page"""

    order = get_object_or_404(Order, order_number=order_number)

    if 'cart' in request.session:
        del request.session['cart']

    context = {
        'order': order
    }

    return render(request, 'checkout/checkout_success.html', context=context)
