from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class User(AbstractUser):
    fullname = models.CharField(
        max_length=100, blank=True, verbose_name=_("fullname"))
    
    gender = models.CharField(max_length=20, null=True, blank=True)

    birth_date = models.DateTimeField(null=True, blank=True)

    phone = models.CharField(max_length=20, blank=True,
                             verbose_name=_("phone"))

    address = models.CharField(
        max_length=300, blank=True, verbose_name=_("address"))
    
    profile_picture = models.ImageField(
        upload_to='static/images/profiles', blank=True, null=True, verbose_name=_("profile.picture"))
   
    tmp_password = models.CharField(max_length=50, blank=True, null=True)
    tmp_password_expired = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    is_admin = models.BooleanField(blank=True, default=False, verbose_name=_("is_admin"))

    created_date = models.DateTimeField(auto_now_add=True)
    active_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def display(self):
        if self.fullname:
            return self.fullname
        else:
            return self.username