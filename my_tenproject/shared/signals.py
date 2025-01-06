# shared/signals.py
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from shared.models import Organization

@receiver(post_save, sender=Organization)
def create_schema(sender, instance, created, **kwargs):
    if created:
        schema_name = instance.schema_name
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name}')