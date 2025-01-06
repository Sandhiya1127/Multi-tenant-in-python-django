# shared/admin.py
from django.contrib import admin
from .models import Organization, Domain, User

admin.site.register(Organization)
admin.site.register(Domain)
admin.site.register(User)