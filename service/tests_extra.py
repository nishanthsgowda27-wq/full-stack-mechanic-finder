from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from service.models import UserProfile
from django.utils import timezone
from datetime import timedelta
from .models import MechanicService, Booking


class MapPresenceTests(TestCase):
    """Verify that map JS and OSM references are present on list and detail pages."""

    def setUp(self):
        call_command('create_demo_data')

    def test_search_page_contains_leaflet_and_osm(self):
        resp = self.client.get('/search/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        # Look for Leaflet map initialization and an OSM tile URL
        self.assertIn('L.map(', content)
        self.assertIn('openstreetmap.org', content)

    def test_mechanic_detail_contains_map(self):
        mech = UserProfile.objects.filter(is_mechanic=True).first()
        self.assertIsNotNone(mech, 'No demo mechanic found')
        resp = self.client.get(f'/mechanic/{mech.pk}/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        self.assertIn('detail-map', content)
        self.assertIn('L.map(', content)


class BookingAcceptRejectTests(TestCase):
    """Test accept/reject JSON endpoints for mechanics and unauthorized users."""

    def setUp(self):
        # Create demo data and pick a mechanic, a user and a service
        call_command('create_demo_data')
        self.mechanic_user = User.objects.get(username='mech1')
        self.user_user = User.objects.get(username='user1')
        self.mechanic_profile = UserProfile.objects.get(user=self.mechanic_user)
        # Ensure the mechanic has at least one service
        self.service = MechanicService.objects.filter(mechanic=self.mechanic_profile).first()
        if not self.service:
            # create a simple service for the mechanic
            self.service = MechanicService.objects.create(
                mechanic=self.mechanic_profile,
                service_name='Test Service',
                price='10.00',
                description='Auto-generated for tests'
            )

        # Create a booking in the future by user1 for that service
        self.user_profile = UserProfile.objects.get(user=self.user_user)
        self.booking = Booking.objects.create(
            user=self.user_profile,
            mechanic=self.mechanic_profile,
            service=self.service,
            booking_date=timezone.now() + timedelta(hours=2)
        )

    def test_mechanic_can_accept_booking_via_json(self):
        # login as mechanic
        logged = self.client.login(username='mech1', password='password123')
        self.assertTrue(logged, 'Could not log in as mechanic')
        url = f'/booking/{self.booking.pk}/accept/json/'
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get('status'), 'confirmed')
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.STATUS_CONFIRMED)

    def test_non_mechanic_cannot_accept_booking(self):
        # login as regular user and attempt to accept
        logged = self.client.login(username='user1', password='password123')
        self.assertTrue(logged, 'Could not log in as user1')
        url = f'/booking/{self.booking.pk}/accept/json/'
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)
        data = resp.json()
        self.assertEqual(data.get('error'), 'forbidden')

    def test_mechanic_can_reject_booking_via_json(self):
        # login as mechanic
        self.client.login(username='mech1', password='password123')
        url = f'/booking/{self.booking.pk}/reject/json/'
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get('status'), 'rejected')
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, Booking.STATUS_REJECTED)

    def test_non_mechanic_cannot_reject_booking(self):
        self.client.login(username='user1', password='password123')
        url = f'/booking/{self.booking.pk}/reject/json/'
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)
        data = resp.json()
        self.assertEqual(data.get('error'), 'forbidden')
