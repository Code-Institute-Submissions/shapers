from django.urls import path
from . import views
from .webhooks import stripe_webhook


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<order_number>', views.checkout_success,
         name='checkout_success'),
    path('webhooks/', stripe_webhook, name='stripe_webhook'),
    path('add_checkout_metadata/', views.add_checkout_metadata,
         name='add_checkout_metadata')
]
