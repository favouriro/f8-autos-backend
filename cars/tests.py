from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Car

class CarTests(TestCase):

    def setUp(self):
        # Runs before every test
        # Create regular user and an admin user
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass2024!'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            password='AdminPass2024!'
        )
        # Create a test car
        self.car = Car.objects.create(
            make='Ford',
            model='Focus',
            year=2020,
            mileage=50000,
            price=8500.00,
            condition='good',
            description='A test car',
            is_available=True
        )

    def test_anyone_can_view_cars(self):
        # Test that unauthenticated users can view cars
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cars_list_returns_correct_data(self):
        # Test that the cars list contains our test car
        response = self.client.get('/api/cars/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['make'], 'Ford')
        self.assertEqual(response.data[0]['model'], 'Focus')

    def test_regular_user_cannot_add_car(self):
        # Test that regular users cannot add cars
        self.client.force_authenticate(user=self.user)
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2021,
            'mileage': 30000,
            'price': 9000.00,
            'condition': 'excellent',
            'description': 'Another test car',
            'is_available': True
        }
        response = self.client.post('/api/cars/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_add_car(self):
        # Test that admin users can add cars
        self.client.force_authenticate(user=self.admin)
        data = {
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2021,
            'mileage': 30000,
            'price': 9000.00,
            'condition': 'excellent',
            'description': 'Another test car',
            'is_available': True
        }
        response = self.client.post('/api/cars/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
