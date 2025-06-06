from django.core.mail import send_mail
from django.conf import settings

def SendMail(email, fullname):
    subject = "Welcome to Naomi Howard Crystal Gems"
    message = f'''
    Hi {fullname},
    Thank you for registering with Naomi Howard Crystal Gems.
    We're thrilled to have you as part of our community! Explore our exclusive collection of stunning jewelry designed just for you.
    If you have any questions or need assistance, feel free to reach out.
    Happy shopping!
    Best regards,
    The Naomi Howard Crystal Gems Team
    '''
    from_email = f"Naomi Howard Crystal Gems <{settings.EMAIL_HOST_USER}>"

    send_mail(
        subject,
        message,
        from_email,
        [email],
        fail_silently=False,
    )
