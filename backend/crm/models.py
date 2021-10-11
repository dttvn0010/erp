from django.db import models
from django.contrib.auth.models import Group

from core.models import Partner, Company, AddressBlock
from employee.models import Team
from core.constants import BaseStatus, Gender

# Create your models here.

class Stage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    sequence = models.IntegerField()
    is_won = models.BooleanField(default=False)

    status = models.CharField(choices=BaseStatus.choices(), 
                default=BaseStatus.DRAFT.name,
                max_length=50)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

class Lead(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    partner = models.OneToOneField(Partner, 
                        blank=True, null=True, 
                        on_delete=models.CASCADE)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, blank=True)

    fullname = models.CharField(max_length=100, 
                        blank=True)

    gender = models.CharField(choices=Gender.choices(), 
                        null=True, blank=True,
                        max_length=50)

    birth_date = models.DateTimeField(null=True, 
                        blank=True)

    address = models.CharField(max_length=300, 
                        blank=True)

    address_block = models.ForeignKey(AddressBlock, 
                        blank=True, null=True, 
                        on_delete=models.PROTECT)
    
    is_opportunity = models.BooleanField(default=False)

    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)

    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)