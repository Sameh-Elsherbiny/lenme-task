from django.db import models
from django.contrib.auth.models import  BaseUserManager , AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.utils import timezone


class User(AbstractUser):
    
    username = None
    full_name = models.CharField(_('full name'), max_length=100)
    image = models.ImageField(_('image'), upload_to='users/images/', blank=True, null=True)
    otp = models.CharField(_('one time password'), max_length=6, blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=False)
    email = models.EmailField(_('email address'), unique=True,max_length=70) 
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _("Users")
        verbose_name_plural = _("Users")

    def __str__(self):
        return str(self.email)
    

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    def __str__(self):
        return self.user.email


# Create your models here.
