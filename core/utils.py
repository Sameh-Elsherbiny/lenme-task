from django.core.mail import EmailMessage
import threading
from django.conf import settings
from .models import User
import pyotp
from rest_framework_simplejwt.tokens import RefreshToken

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_email(email):
        user = None
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        if User.objects.filter(new_email=email).exists():
            user = User.objects.get(new_email=email)
        totp = pyotp.TOTP('base32secret3232', digits=6)
        user.otp = totp.now()
        user.save()
        email_data = {
            'email_subject': 'Verify your email',
            'email_body': f'Use this OTP to verify your email: {user.otp}',
            'to_email': email if email else user.email
        }
        email = EmailMessage(
            subject=email_data['email_subject'], body=email_data['email_body'], to=[email_data['to_email']], from_email=settings.EMAIL_HOST_USER)
        EmailThread(email).start()

def create_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
