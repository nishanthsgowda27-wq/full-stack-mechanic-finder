#!/usr/bin/env python
"""Test script to verify enhanced Accept/Reject buttons on Bookings page"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create test client
client = Client()

print("=" * 60)
print("Testing Enhanced Accept/Reject Buttons")
print("=" * 60)

# Test 1: Login as mechanic
print("\n[Test 1] Logging in as mech1...")
login_success = client.login(username='mech1', password='password123')
print(f"  Login status: {'✓ Success' if login_success else '✗ Failed'}")

# Test 2: Access Bookings page
print("\n[Test 2] Accessing /bookings/ page...")
response = client.get('/bookings/')
print(f"  Status code: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check for enhanced button features
    checks = [
        ("Bookings Management heading", "<h2>Bookings Management</h2>" in content),
        ("Accept button (btn-lg)", 'btn btn-success btn-lg' in content),
        ("Reject button (btn-lg)", 'btn btn-outline-danger btn-lg' in content),
        ("Accept icon (fa-check-circle)", 'fa-check-circle' in content),
        ("Reject icon (fa-times-circle)", 'fa-times-circle' in content),
        ("Action buttons styling", 'action-buttons' in content),
        ("Accept button has title", 'title="✅ Accept this booking"' in content),
        ("Reject button has title", 'title="❌ Reject this booking"' in content),
        ("AJAX script present", 'fetch(jsonUrl' in content),
    ]
    
    print("\n  ✓ Enhanced Features Found:")
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"    {status} {check_name}")

# Test 3: Check navbar dropdown
print("\n[Test 3] Checking Bookings dropdown menu in navbar...")
response = client.get('/')
if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    dropdown_checks = [
        ("Bookings dropdown", 'bookingsDropdown' in content),
        ("Accept Pending Bookings link", 'Accept Pending Bookings' in content),
        ("Confirmed Bookings link", 'Confirmed Bookings' in content),
        ("Rejected Bookings link", 'Rejected Bookings' in content),
    ]
    
    print("\n  ✓ Navbar Enhancements Found:")
    for check_name, result in dropdown_checks:
        status = "✓" if result else "✗"
        print(f"    {status} {check_name}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
