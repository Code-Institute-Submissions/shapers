from django.db import models
from profile.models import UserProfile


class Contact(models.Model):
    """Model for the contact_us form"""

    message = models.TextField(null=False, blank=False)
    email = models.EmailField(max_length=120, null=False, blank=False)
    full_name = models.CharField(max_length=120, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='inquiries')

    def __str__(self):
        if self.user_profile:
            return f'{self.date.strftime("%Y-%d-%w - %H:%M")} ' \
                   f'from {self.user_profile}'
        else:
            return f'{self.date.strftime("%Y-%d-%w - %H:%M")} ' \
                   f'from {self.email}'
