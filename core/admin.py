from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import forms, models

# Register your models here.

class MyUserAdmin(UserAdmin):
    add_form = forms.MyUserCreationForm
    form = forms.MyUserChangeForm
    model = models.User
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Other information',
            {
                'fields': (
                    'display', 'phone', 'address', 'tmp_password',
                    'gender', 'birth_date', 'is_admin',
                    'profile_picture', 
                ),
            },
        ),
    )
    list_display = ['username', 'display',
                    'email', 'phone', 'address']

admin.site.register(models.Company)
admin.site.register(models.User, MyUserAdmin)
admin.site.register(models.Partner)
admin.site.register(models.ModelProperty)
admin.site.register(models.CodeSystem)
admin.site.register(models.Coding)
