#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_site.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Student

print('=' * 90)
print('LOGIN & REGISTER DATA IN SQLITE DATABASE')
print('=' * 90)

# Get all users
users = User.objects.all()
print(f'\nTotal Registered Users: {users.count()}\n')
print('-' * 90)
print(f'{"ID":<5} {"Username":<20} {"Email":<30} {"Date Joined":<20} {"Last Login":<15}')
print('-' * 90)

for user in users:
    print(f'{user.id:<5} {user.username:<20} {user.email:<30} {str(user.date_joined):<20} {str(user.last_login):<15}')

print('\n' + '=' * 90)
print('STUDENT PROFILES')
print('=' * 90)

students = Student.objects.select_related('user').all()
print(f'\nTotal Student Profiles: {students.count()}\n')

if students.count() > 0:
    print('-' * 90)
    print(f'{"Username":<20} {"Roll No":<20} {"Status":<15} {"Admission Date":<20}')
    print('-' * 90)
    
    for student in students:
        print(f'{student.user.username:<20} {student.roll_number:<20} {student.status:<15} {str(student.admission_date):<20}')
else:
    print('No student profiles created yet.')

print('\n' + '=' * 90)
