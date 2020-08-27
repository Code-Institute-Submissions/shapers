from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """Model for Customers and Partners profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_phone_number = models.CharField(max_length=40,
                                            blank=True, null=True)
    profile_street_address1 = models.CharField(max_length=80,
                                               blank=True, null=True)
    profile_street_address2 = models.CharField(max_length=80,
                                               blank=True, null=True)
    profile_postcode = models.CharField(max_length=20, null=True, blank=True)
    profile_town_or_city = models.CharField(max_length=40, null=True,
                                            blank=True)
    profile_country = CountryField(blank_label='Country',
                                   null=True, blank=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name} as ' \
                   f'{self.user.username}'
        else:
            return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user's profile when a new user signs up"""

    if created:
        UserProfile.objects.create(user=instance)
