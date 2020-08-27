from django.http import HttpResponse
from .models import Order, OrderLineProduct
from profile.models import UserProfile
from store.models import Product
import time
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class StripeWhHandler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event_default(self, event):
        """Default Stripe webhook events handler method"""

        return HttpResponse(
            content=f'Stripe webhook received: {event["type"]}',
            status=200)

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""

        order_email = order.email
        email_subject = render_to_string(
            'checkout/emails/payment_confirmation_email_subject.txt',
            {'order': order})
        email_body = render_to_string(
            'checkout/emails/payment_confirmation_email_body.txt',
            {'order': order, 'contact_us_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order_email]
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle Stripe successful payment intents"""

        payment_intent = event.data.object

        billing_details = payment_intent.charges.data[0].billing_details

        cart_content = json.loads(payment_intent.metadata.cart_content)
        username = payment_intent.metadata.username

        user_profile = UserProfile.objects.get(user__username=username)

        # If a given user has placed an order within the following 5s
        # I assume it is the one.
        # Order form submission is triggered after Stripe Payment succeeded
        time_threshold = datetime.now() - timedelta(seconds=5)
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    user_profile=user_profile,
                    date__gte=time_threshold)
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

            except Order.MultipleObjectsReturned as e:
                # Should probably do something about that kind of situation !!
                return HttpResponse(
                    content=f'Error looking for order in the database: '
                            f'{event["type"]}; '
                            f'ERROR: {e}',
                    status=500)

            except Exception as e:
                return HttpResponse(
                    content=f'Error looking for order in the database: '
                            f'{event["type"]}; '
                            f'ERROR: {e}',
                    status=500)

        if order_exists:
            self._send_confirmation_email(order)
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

                self._send_confirmation_email(order_process)
                return HttpResponse(
                    content=f'Stripe Webhook received: {event["type"]}; '
                            f'Order saved by webhook handler',
                    status=200)

            except Exception as e:
                if order_process:
                    order_process.delete()

                return HttpResponse(
                    content=f'Error saving the order with WH handler: '
                            f'{event["type"]}; '
                            f'ERROR: {e}',
                    status=500)

    def handle_payment_intent_failed(self, event):
        """Handle Stripe payment intent failures"""

        print('INTENT FAILED', f'{event["type"]}')
        return HttpResponse(
            content=f'Stripe Webhook received: {event["type"]}',
            status=200)
