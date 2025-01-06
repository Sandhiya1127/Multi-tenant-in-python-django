# shared/middleware.py
from django.db import connection
from shared.models import Organization

class SchemaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            organization = request.user.organization
            if organization:
                schema_name = organization.schema_name
                with connection.cursor() as cursor:
                    cursor.execute(f'SET search_path TO {schema_name}')
        response = self.get_response(request)
        return response