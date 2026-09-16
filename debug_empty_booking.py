#!/usr/bin/env python
"""Test creating an empty booking and rendering it."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from service.models import Booking, UserProfile, MechanicService
from service.forms import BookingForm

print("Testing empty Booking rendering")
print("=" * 60)

# Get a user and service
user_profile = UserProfile.objects.filter(is_mechanic=False).first()
service = MechanicService.objects.filter().first()

if not user_profile or not service:
    print("❌ Missing user or service")
    exit(1)

print(f"✓ User: {user_profile}")
print(f"✓ Service: {service}")
print(f"✓ Service mechanic: {service.mechanic}")

# Create a new empty booking
print("\nCreating new empty booking...")
booking = Booking(user=user_profile, service=service)
print(f"✓ Created booking (not saved): {booking}")

# Try to access mechanic (should fail with RelatedObjectDoesNotExist)
print("\nTrying to access booking.mechanic...")
try:
    mechanic = booking.mechanic
    print(f"✓ Mechanic: {mechanic}")
except Exception as e:
    print(f"❌ Error accessing mechanic: {type(e).__name__}: {e}")

# Try to create a form with this instance
print("\nCreating form with empty booking instance...")
try:
    form = BookingForm(instance=booking, mechanic=service.mechanic)
    print("✓ Form created")
    
    print("\nRendering form.as_p()...")
    html = form.as_p()
    print("✓ Form rendered successfully")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
