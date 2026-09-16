#!/usr/bin/env python
"""Test form with initial service."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from service.models import MechanicService
from service.forms import BookingForm

print("Test: Form with initial service")
print("=" * 60)

service = MechanicService.objects.filter().first()
mechanic = service.mechanic

print(f"✓ Service: {service}")
print(f"✓ Mechanic: {mechanic}")

try:
    form = BookingForm(mechanic=mechanic, initial={'service': service})
    print("✓ Form created with initial")
    
    html = form.as_p()
    print("✓ Form rendered")
    
    # Check what's in the form
    print(f"\nForm fields:")
    for name, field in form.fields.items():
        print(f"  - {name}: {field}")
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
