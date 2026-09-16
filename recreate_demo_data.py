#!/usr/bin/env python
"""Clean up and recreate demo data."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.contrib.auth.models import User
from service.models import UserProfile, MechanicService

# Delete all existing demo users and their profiles
for username in ['mech1', 'mech2', 'mech3', 'mech4', 'user1', 'user2']:
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"Deleted {username}")
    except User.DoesNotExist:
        pass

# Delete all services
MechanicService.objects.all().delete()
print("Deleted all services")

# Create fresh demo data
print("\n=== Creating fresh demo data ===")

# Mechanics
u1 = User.objects.create_user('mech1', password='password123', first_name='Mike', last_name='One')
p1 = UserProfile.objects.create(user=u1, is_mechanic=True, city='Springfield', phone='1234567890', latitude=40.0, longitude=-75.0)
MechanicService.objects.create(mechanic=p1, service_name='Oil Change', price=25.00, description='Quick oil change')
MechanicService.objects.create(mechanic=p1, service_name='Brake Repair', price=120.00, description='Brake pad replacement')
print(f"✓ Created mechanic mech1 with 2 services")

u2 = User.objects.create_user('mech2', password='password123', first_name='Sara', last_name='Two')
p2 = UserProfile.objects.create(user=u2, is_mechanic=True, city='Shelbyville', phone='0987654321', latitude=41.0, longitude=-74.0)
MechanicService.objects.create(mechanic=p2, service_name='Tire Change', price=40.00, description='Tire mount and balance')
MechanicService.objects.create(mechanic=p2, service_name='Battery Replacement', price=90.00, description='New battery installation')
print(f"✓ Created mechanic mech2 with 2 services")

# Additional mechanics
u3 = User.objects.create_user('mech3', password='password123', first_name='Alan', last_name='Three')
p3 = UserProfile.objects.create(user=u3, is_mechanic=True, city='Capital City', phone='2223334444', latitude=39.5, longitude=-76.0)
MechanicService.objects.create(mechanic=p3, service_name='Engine Tune-up', price=150.00, description='Full engine tune-up')
MechanicService.objects.create(mechanic=p3, service_name='AC Recharge', price=60.00, description='AC refrigerant top-up')
print(f"✓ Created mechanic mech3 with 2 services")

u4 = User.objects.create_user('mech4', password='password123', first_name='Linda', last_name='Four')
p4 = UserProfile.objects.create(user=u4, is_mechanic=True, city='Ogdenville', phone='7778889999', latitude=38.9, longitude=-77.1)
MechanicService.objects.create(mechanic=p4, service_name='Transmission Repair', price=500.00, description='Transmission diagnostics and repair')
MechanicService.objects.create(mechanic=p4, service_name='Wheel Alignment', price=70.00, description='4-wheel alignment')
print(f"✓ Created mechanic mech4 with 2 services")

# Users
uu1 = User.objects.create_user('user1', password='password123', first_name='User', last_name='One')
UserProfile.objects.create(user=uu1, is_mechanic=False, city='Springfield', phone='1112223333')
print(f"✓ Created user user1")

uu2 = User.objects.create_user('user2', password='password123', first_name='User', last_name='Two')
UserProfile.objects.create(user=uu2, is_mechanic=False, city='Shelbyville', phone='4445556666')
print(f"✓ Created user user2")

print("\n✅ Demo data recreated successfully!")
