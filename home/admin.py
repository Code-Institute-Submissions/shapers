from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    """Contact model admin panel"""

    ordering = ('-date',)


admin.site.register(Contact, ContactAdmin)
