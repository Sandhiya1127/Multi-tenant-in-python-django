# tenant/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django_tenants.utils import schema_context, get_tenant_model
from shared.models import User, Organization
from tenant.models import TenantUserDetails
from django.core.management import call_command
from django.db import connection, DatabaseError


def create_schema_and_migrate(schema_name):
    with connection.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')
        
    call_command('migrate_schemas', schema_name=schema_name, interactive=False)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        org_name = request.POST['org_name']

        if not username or not password or not org_name:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        try:
            with schema_context('public'):
                organization, created = Organization.objects.get_or_create(
                    name=org_name,
                    defaults={'schema_name': org_name.lower()}
                )

                if created:
                    create_schema_and_migrate(organization.schema_name)

            with schema_context(organization.schema_name):
                user = User.objects.create_user(username=username, password=password, organization=organization)
                TenantUserDetails.objects.create(user=user, details='User details here')

            login(request, user)
            # return redirect('home')
            return redirect('login')
        except DatabaseError:
            messages.error(request, "An error occurred while processing your registration. Please try again.")
            return render(request, 'register.html')
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            messages.error(request, "An unexpected error occurred. Please try again later.")
            return render(request, 'register.html')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

        with schema_context(user.organization.schema_name):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html', {'user': request.user})


def profile(request):
    return render(request, 'profile.html') 