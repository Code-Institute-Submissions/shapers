from django.http import HttpResponse
from .models import Order, OrderLineProduct
from profile.models import UserProfile
from store.models import Product
import time
import json


class StripeWhHandler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event_default(self, event):
        """Default Stripe webhook events handler method"""

        return HttpResponse(
            content=f'Stripe webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle Stripe successful payment intents"""

        payment_intent = event.data.object

        billing_details = payment_intent.charges.data[0].billing_details

        cart_content = json.loads(payment_intent.metadata.cart_content)
        username = payment_intent.metadata.username

        user_profile = UserProfile.objects.get(user__username=username)

        order_exists = False
        attempt = 1
        while attempt <= 5:
            # If a given user has placed an order within the following 5s
            # I assume it is the one.
            # Order form submission is triggered after Stripe Payment succeeded
            try:
                order = Order.objects.filter(
                    user_profile=user_profile,
                    date__gte=payment_intent.created)
                order_exists = True
                break
            except Exception as e:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=(f'Stripe Webhook processed: {event["type"]};'
                         f'Order already saved in Database'),
                status=200)

        else:
            order_process = None
            try:
                for field, value in billing_details.address.items():
                    if value == "":
                        billing_details.address[field] = None

                order_process = Order.objects.create(
                    full_name=billing_details.name,
                    user_profile=user_profile,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    town_or_city=billing_details.address.city,
                    postcode=billing_details.address.postal_code,
                    county=billing_details.address.state,
                    country=billing_details.address.country,
                )

                for product_id, quantity in cart_content.items():
                    product = Product.objects.get(id=product_id)
                    OrderLineProduct.objects.create(
                        order=order_process,
                        product=product,
                        quantity=quantity
                    )

                return HttpResponse(
                    content=f'Stripe Webhook received: {event["type"]}; '
                            f'Order saved by webhook handler',
                    status=200)

            except Exception as e:

                return HttpResponse(
                    content=f'Error saving the order with WH handler: '
                            f'{event["type"]}; '
                            f'ERROR: {e}',
                    status=200)

    def handle_payment_intent_failed(self, event):
        """Handle Stripe payment intent failures"""

        print('INTENT FAILED', f'{event["type"]}')
        return HttpResponse(
            content=f'Stripe Webhook received: {event["type"]}',
            status=200)
