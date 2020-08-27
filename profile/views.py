from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.models import User
from checkout.models import Order
from django.contrib import messages


@login_required
def profile(request):
    """View returning Profile page"""

    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your details have been updated!')

    profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
    }

    return render(request, 'profile/profile.html', context=context)


@login_required()
def delete_account(request):
    """Deletes a user account"""

    user = request.user

    User.objects.get(username=user.username).delete()

    return redirect(reverse('home'))


@login_required()
def my_orders(request):
    """View returning the current users order history"""

    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_orders = user_profile.orders.all()

    context = {
        'user_orders': user_orders
    }

    return render(request, 'profile/my_orders.html', context=context)


@login_required()
def order_details(request, order_id):
    """View return details of a specific order"""

    context = {
        'order': get_object_or_404(Order, pk=order_id),
    }

    return render(request, 'profile/order_details.html', context=context)
