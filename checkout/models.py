from django.db import models
from uuid import uuid4
from profile.models import UserProfile
from store.models import Product
from django.db.models import Sum
from django_countries.fields import CountryField


class Order(models.Model):
    """Basic Order model used for payment & shipping"""

    order_number = models.UUIDField(default=uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=50, null=False, blank=False)
    street_address2 = models.CharField(max_length=50, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)
    county = models.CharField(max_length=40, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, blank=False, default=0)

    def __str__(self):
        return str(self.order_number)

    def update_total(self):
        """
        Update the order_total with the sum of lineproducts when a lineproduct
        is saved
        """

        self.order_total = self.lineproducts.aggregate(
            Sum('lineproduct_total'))['lineproduct_total__sum'] or 0
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrderLineProduct(models.Model):
    """Line Product for Order"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False,
                              blank=False, related_name='lineproducts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False,
                                blank=False)
    quantity = models.IntegerField(default=0, null=False, blank=False)
    lineproduct_total = models.DecimalField(max_digits=6, decimal_places=2,
                                            null=False, blank=False,
                                            editable=False)

    def save(self, *args, **kwargs):
        """Override save method to update the line product total"""

        self.lineproduct_total = self.product.base_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} ordered in ' \
               f'{self.order.order_number}'
