from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineProduct


@receiver(post_save, sender=OrderLineProduct)
def update_on_save(sender, instance, **kwargs):
    """
    Update order total on lineproduct update/create

    :param sender: model class sending the signal ie OrderLineProduct
    :param instance: actual instance of the model that sent it, ie being saved
    :param kwargs: any keyword arguments
    """

    instance.order.update_total()


@receiver(post_delete, sender=OrderLineProduct)
def update_on_delete(sender, instance, **kwargs):
    """Update order total on lineproduct delete"""

    instance.order.update_total()
