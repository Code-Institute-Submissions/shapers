from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-use/', views.terms_use, name='terms_use'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
