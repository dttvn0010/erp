from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .constants import Gender, BaseStatus, CodeSystemStatus, CodeSystemDataType, PartnerType

class AddressBlock(models.Model):
    city = models.ForeignKey('Coding', related_name='city_blocks', on_delete=models.PROTECT)
    district = models.ForeignKey('Coding', related_name='district_blocks', on_delete=models.PROTECT)
    ward = models.ForeignKey('Coding', related_name='ward_blocks', on_delete=models.PROTECT)

class User(AbstractUser):
    display = models.CharField(max_length=100, blank=True,
                verbose_name=_("verbose_name.user.display"))
    
    gender = models.CharField(choices=Gender.choices(), null=True, blank=True,
                verbose_name=_("verbose_name.user.gender"),
                max_length=50)

    birth_date = models.DateTimeField(null=True, blank=True,
                verbose_name=_("verbose_name.user.birth_date"))

    phone = models.CharField(max_length=20, blank=True, unique=True,
                verbose_name=_("verbose_name.user.phone"))

    address = models.CharField(
                max_length=300, blank=True, 
                verbose_name=_("verbose_name.user.address"))

    address_block = models.ForeignKey(AddressBlock, on_delete=models.PROTECT,
                blank=True, null=True,
                verbose_name=_("verbose_name.user.address.block"))
    
    profile_picture = models.ImageField(
                upload_to='static/images/profiles', blank=True, null=True, 
                verbose_name=_("verbose_name.user.profile.picture"))
   
    tmp_password = models.CharField(max_length=50, blank=True, null=True)
    tmp_password_expired = models.DateTimeField(blank=True, null=True)

    is_admin = models.BooleanField(blank=True, default=False, 
                verbose_name=_("verbose_name.user.is_admin"))

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.display:
            return self.display
        else:
            return self.username

class Company(models.Model):
    name = models.CharField(max_length=200, blank=True,
                verbose_name=_("verbose_name.company.name"))
    
    phone = models.CharField(max_length=20, blank=True,
                verbose_name=_("verbose_name.company.phone"))

    address = models.CharField(
                max_length=300, blank=True, 
                verbose_name=_("verbose_name.company.address"))

    director = models.ForeignKey(User, on_delete=models.PROTECT)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=BaseStatus.choices(),
                            default=BaseStatus.DRAFT.name,
                            max_length=50)

class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    code = models.CharField(max_length=30, unique=True)
    partner_type = models.CharField(choices=PartnerType.choices(),
                            max_length=50)

    def __str__(self):
        return self.user.display

class ModelProperty(models.Model):
    model = models.CharField(max_length=200, blank=True,
                verbose_name=_("verbose_name.model.property.model"))
    
    code = models.CharField(max_length=100, 
                verbose_name=_("verbose_name.model.property.code"))
    
    name = models.CharField(max_length=200, 
                verbose_name=_("verbose_name.model.property.name"))

    datatype = models.CharField(choices=CodeSystemDataType.choices(),
                verbose_name=_("verbose_name.model.property.datatype"),
                max_length=50)

    related_model = models.CharField(max_length=200, blank=True,
                verbose_name=_("verbose_name.model.property.related.model"))

class CodeSystem(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    code = models.CharField(max_length=100, 
                verbose_name=_("verbose_name.codesystem.code"))

    name = models.CharField(max_length=200, 
                verbose_name=_("verbose_name.codesystem.name"))

    version = models.CharField(max_length=30)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=CodeSystemStatus.choices(), max_length=50)

class Coding(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    code_system = models.ForeignKey(CodeSystem, on_delete=models.PROTECT)

    code = models.CharField(max_length=100, 
                verbose_name=_("verbose_name.code.code"))
    
    display = models.CharField(max_length=200, 
                verbose_name=_("verbose_name.code.display"))

    properties = models.JSONField()