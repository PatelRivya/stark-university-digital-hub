from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Student


class StudentRegistrationTests(TestCase):
    def registration_data(self, **overrides):
        data = {
            'first_name': 'Peter',
            'last_name': 'Parker',
            'email': 'peter@example.com',
            'username': 'peterparker',
            'password1': 'StrongPass12345',
            'password2': 'StrongPass12345',
            'date_of_birth': '2001-08-10',
            'gender': 'M',
            'phone': '5551234567',
            'address': '20 Ingram Street',
            'city': 'Queens',
            'country': 'USA',
        }
        data.update(overrides)
        return data

    def test_registration_creates_user_and_student_profile_in_sqlite(self):
        response = self.client.post(reverse('register'), self.registration_data())

        self.assertRedirects(response, reverse('dashboard'))
        user = User.objects.get(username='peterparker')
        student = Student.objects.get(user=user)
        self.assertEqual(user.email, 'peter@example.com')
        self.assertEqual(user.first_name, 'Peter')
        self.assertEqual(student.phone, '5551234567')
        self.assertEqual(student.city, 'Queens')
        self.assertTrue(student.roll_number.startswith('STU'))

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(
            username='existing',
            email='peter@example.com',
            password='StrongPass12345',
        )

        response = self.client.post(
            reverse('register'),
            self.registration_data(username='newpeter')
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newpeter').exists())
        self.assertContains(response, 'An account with this email already exists.')

    def test_authenticated_user_register_link_goes_to_dashboard(self):
        user = User.objects.create_user(
            username='loggedin',
            password='StrongPass12345',
        )
        Student.objects.create(user=user, roll_number='STU-LOGGED-IN')
        self.client.login(username='loggedin', password='StrongPass12345')

        response = self.client.get(reverse('register'))

        self.assertRedirects(response, reverse('dashboard'))

