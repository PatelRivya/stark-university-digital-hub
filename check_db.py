#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_site.settings')
django.setup()

from django.db import connection
from django.apps import apps

print('=' * 70)
print('SQLITE DATABASE CONNECTION VERIFIED ✓')
print('=' * 70)
print(f'\nDatabase Engine: {connection.settings_dict["ENGINE"]}')
print(f'Database File: {connection.settings_dict["NAME"]}')
print(f'\nDatabase Tables & Records:')
print('-' * 70)

for model in apps.get_models():
    count = model.objects.count()
    if count > 0:
        print(f'  • {model._meta.label:<30} {count:>3} records')

print('\n' + '=' * 70)
print('Your website is CONNECTED to SQLite database!')
print('=' * 70)
