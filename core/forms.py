from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext as _

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'display', 'email', 'phone', 'address')

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('display', 'email', 'phone', 'address')