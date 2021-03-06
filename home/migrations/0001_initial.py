# Generated by Django 3.1 on 2020-08-29 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile', '0004_auto_20200826_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=120)),
                ('full_name', models.CharField(blank=True, max_length=120, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inquiries', to='profile.userprofile')),
            ],
        ),
    ]
