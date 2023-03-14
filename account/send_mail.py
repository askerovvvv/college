from django.core.mail import send_mail


def send_confirmation_email(code, email):
    """
    function for send message
    """
    full_link = f"http://localhost:8000/account/activate/{code}"

    send_mail(
        'Activation code for College',
        full_link,
        'alinaolkim@gmail.com',
        [email]
    )



