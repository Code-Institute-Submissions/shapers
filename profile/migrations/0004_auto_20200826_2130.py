# Generated by Django 3.1 on 2020-08-26 21:30

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
