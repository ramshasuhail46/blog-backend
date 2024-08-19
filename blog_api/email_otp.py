from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
# from users import User

import random

User = get_user_model()


def send_otp_via_email(email):
    subject = 'Your acccount verification email'
    otp = random.randint(1000, 9999)
    message = 'your otp is: ' + str(otp)
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])

    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
