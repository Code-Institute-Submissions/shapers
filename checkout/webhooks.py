import json
from django.http import HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .webhooks_handler import StripeWhHandler


@require_POST
@csrf_exempt
def stripe_webhook(request):
    """Listens for Stripe Webhooks"""

    stripe_wh_secret_key = settings.STRIPE_WEBHOOK_SECRET_KEY
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), signature_header, stripe_wh_secret_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        # Other Errors
        return HttpResponse(content=e, status=400)

    event_type = event['type']

    handler = StripeWhHandler(request)

    # Map webhook additional events to its StripeWhHandler method
    event_map = {
        'payment_intent.succeeded':
            handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed':
            handler.handle_payment_intent_failed,
    }

    event_handler = event_map.get(event_type, handler.handle_event_default)

    response = event_handler(event)
    return response
