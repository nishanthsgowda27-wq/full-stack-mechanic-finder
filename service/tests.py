from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from service.models import UserProfile


class DemoDataCommandTest(TestCase):
    def test_create_demo_data_creates_mechanics_and_users(self):
        # Ensure command runs without error
        call_command('create_demo_data')

        # Expected demo mechanics
        mechanics = ['mech1', 'mech2', 'mech3', 'mech4']
        for m in mechanics:
            with self.subTest(mechanic=m):
                self.assertTrue(User.objects.filter(username=m).exists(), f"{m} should exist")
                profile = UserProfile.objects.filter(user__username=m, is_mechanic=True)
                self.assertTrue(profile.exists(), f"UserProfile for {m} should exist and be a mechanic")

        # Expected demo users
        users = ['user1', 'user2']
        for u in users:
            with self.subTest(user=u):
                self.assertTrue(User.objects.filter(username=u).exists(), f"{u} should exist")
                profile = UserProfile.objects.filter(user__username=u, is_mechanic=False)
                self.assertTrue(profile.exists(), f"UserProfile for {u} should exist and be a non-mechanic")
