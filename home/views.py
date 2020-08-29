from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import ContactForm
from profile.models import UserProfile
from django.contrib import messages


def home(request):
    """View returning Home page"""

    return render(request, 'home/index.html')


def about_us(request):
    """View returning About Us page"""

    return render(request, 'home/about_us.html')


def privacy_policy(request):
    """View returning Shapers Privacy Policy"""

    return render(request, 'home/privacy_policy.html')


def terms_use(request):
    """View returning Shapers Terms and Conditions of Use"""

    return render(request, 'home/terms_use.html')


def contact_us(request):
    """View returning Shapers Contact form page"""

    if request.method == 'POST':
        redirect_to = request.POST.get('redirect_to')
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            try:
                if request.user.is_authenticated:
                    contact_form = contact_form.save(commit=False)
                    user_profile = UserProfile.objects.get(user=request.user)
                    contact_form.user_profile = user_profile
                contact_form.save()
                # insert send email code here !

                messages.success(request,
                                 "We have received your message. "
                                 "An email confirmation has been sent.")
                return redirect(redirect_to)

            except Exception as e:
                messages.error(request,
                               "We couldn't process your inquiry. "
                               "Please try again later.")
                return render(request, 'home/contact_us.html',
                              context={'contact_form': contact_form})

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        contact_form = ContactForm(initial={
            'full_name': f'{user_profile.user.first_name} '
                         f'{user_profile.user.last_name}'.strip(),
            'email': request.user.email,
        })
    else:
        contact_form = ContactForm()

    context = {
        'next': request.GET.get('next', ''),
        'contact_form': contact_form
    }

    return render(request, 'home/contact_us.html', context=context)
