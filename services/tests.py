from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Service, Booking

class ServiceTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass2024!',
            email='test@test.com'
        )
        self.service = Service.objects.create(
            name='Full MOT',
            description='Full MOT test',
            price=55.00,
            duration_minutes=60,
            is_available=True
        )

    def test_anyone_can_view_services(self):
        # Test that unauthenticated users can view services
        response = self.client.get('/api/services/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_create_booking(self):
        # Test that unauthenticated users cannot create bookings
        data = {
            'service': self.service.id,
            'booking_date': '2026-06-01',
            'booking_time': '10:00:00',
            'notes': 'Test booking'
        }
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_booking(self):
        # Test that a logged in user can create a booking
        self.client.force_authenticate(user=self.user)
        data = {
            'service': self.service.id,
            'booking_date': '2026-06-01',
            'booking_time': '10:00:00',
            'notes': 'Test booking'
        }
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_only_see_own_bookings(self):
        # Test that users can only see their own bookings
        other_user = User.objects.create_user(
            username='otheruser',
            password='TestPass2024!'
        )
        # Create a booking for other user
        Booking.objects.create(
            user=other_user,
            service=self.service,
            booking_date='2026-06-01',
            booking_time='10:00:00',
            status='pending'
        )
        # Log in as testuser and check they see no bookings
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)