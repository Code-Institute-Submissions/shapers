const stripePublicKey = $('#spk').text().slice(1, -1);
const stripeClientSKey = $('#scsk').text().slice(1, -1);

var stripe = Stripe(stripePublicKey);

var elements = stripe.elements({
    fonts: [{
        fontFamily: 'Lato',
        cssSrc: 'https://fonts.googleapis.com/css2?family=Lato&display=swap',
    }]
});

const style = {
    base: {
        color: '#495057',
        fontFamily: '"Lato", serif',
        fontSmoothing: 'antialiased',
        '::placeholder': {
            color: '#6c757d',
            fontStyle: 'italic',
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {'style': style, 'hidePostalCode': true});

card.mount('#card-element');

// Stripe Form Validation Feedback
card.addEventListener('change', function (event) {
    const cardErrors = document.getElementById('card-errors');
    if (event.error) {
        const html = `
            <p class="form-field-error">
            * <span>${event.error.message}</span>
            <p>
        `;
        $(cardErrors).html(html);
    } else {
        cardErrors.textContent = '';
    }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    // prevent multiple submissions
    card.update({'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#fullscreen-overlay').fadeToggle(200);

    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    const postUrl = '/checkout/add_checkout_metadata/';
    const postData = {
        'csrfmiddlewaretoken': csrfToken,
        'stripeClientSKey': stripeClientSKey,
    };

    $.post(postUrl, postData).done(function () {

        stripe.confirmCardPayment(stripeClientSKey, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        postal_code: $.trim(form.postcode.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                    },
                },
            }
        }).then(function (result) {

            if (result.error) {
                const cardErrors = document.getElementById('card-errors');
                const html = `
              <p class="form-field-error">
                * <span>${result.error.message}</span>
              <p>`
                $(cardErrors).html(html);
                // enable form modification on errors
                card.update({'disabled': false});
                $('#submit-button').attr('disabled', false);
                $('#fullscreen-overlay').fadeToggle(200);

            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        location.reload();
    });
});


