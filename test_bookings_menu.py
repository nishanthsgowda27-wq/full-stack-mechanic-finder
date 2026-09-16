#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.conf import settings

settings.ALLOWED_HOSTS = ['testserver']
client = Client()

# Test 1: Login as mechanic
print("Test 1: Logging in as mech1...")
response = client.post('/login/', {
    'username': 'mech1',
    'password': 'password123'
}, HTTP_HOST='testserver', follow=True)
print(f"  Login status: {response.status_code}")

# Test 2: Check if Bookings link appears after login
print("\nTest 2: Checking navbar after login...")
response = client.get('/search/', HTTP_HOST='testserver')
content = response.content.decode('utf-8')

checks = {
    'Has Bookings link': 'href="/bookings/"' in content or 'manage_bookings' in content,
    'Has Dashboard link': 'dashboard' in content.lower(),
    'Has Logout link': 'logout' in content.lower(),
}

for check, result in checks.items():
    print(f"  {'✓' if result else '✗'} {check}")

# Test 3: Access bookings page
print("\nTest 3: Accessing /bookings/ page...")
response = client.get('/bookings/', HTTP_HOST='testserver')
print(f"  Status: {response.status_code}")

content = response.content.decode('utf-8')
if 'Accept' in content or 'Reject' in content or 'Bookings' in content:
    print(f"  ✓ Booking management page loaded")
    if 'Accept' in content:
        print(f"    - Accept button visible")
    if 'Reject' in content:
        print(f"    - Reject button visible")
else:
    print(f"  ✗ Bookings page content not as expected")

print("\nDone!")
