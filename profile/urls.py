from django.urls import path
from . import views
from allauth.account.views import PasswordChangeView

urlpatterns = [
    path('', views.profile, name='profile'),
    path('password-change/',
         PasswordChangeView.as_view(
             success_url='/profile/',
             template_name='allauth/account/password_change.html'),
         name='profile_password_change'),
    path('delete/', views.delete_account, name='delete_account'),
    path('my-orders', views.my_orders, name='my_orders'),
    path('order-details/<int:order_id>/', views.order_details, name='order_details'),
]
