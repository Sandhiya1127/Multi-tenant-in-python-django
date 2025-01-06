# shared/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from django_tenants.models import TenantMixin, DomainMixin

class Organization(TenantMixin):
    name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='shared_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='shared_user_set', blank=True)