#!/usr/bin/env python
"""Test script to verify dynamic Leaflet map on tracking page"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechanic_finder.settings')
django.setup()

from django.test import Client

# Create test client
client = Client()

print("=" * 70)
print("Testing Dynamic Leaflet Map on /tracking/ Page")
print("=" * 70)

# Test 1: Access tracking map page
print("\n[Test 1] Accessing /tracking/ page...")
response = client.get('/tracking/')
print(f"  Status code: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check for dynamic map features
    checks = [
        ("Map container exists", '<div id="map"' in content),
        ("Leaflet CSS in base", 'leaflet.css' in content),
        ("Leaflet JS in base", 'leaflet.js' in content),
        ("OpenStreetMap attribution", 'openstreetmap.org' in content),
        ("Mechanics JSON data", 'mechanics_json' in content),
        ("Map initialization script", "L.map('map')" in content),
        ("Marker creation logic", 'L.marker' in content),
        ("Popup functionality", 'bindPopup' in content),
        ("TileLayer added", 'L.tileLayer' in content),
        ("Icon configuration", 'L.icon' in content),
        ("Mechanic cards displayed", 'card h-100' in content),
        ("Directory table present", 'Mechanics Directory' in content),
    ]
    
    print("\n  ✓ Dynamic Map Features Found:")
    all_passed = True
    for check_name, result in checks:
        status = "✓" if result else "✗"
        print(f"    {status} {check_name}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n  🎉 All dynamic map features are properly configured!")
    else:
        print("\n  ⚠️  Some features may need attention")
        
    # Check JSON data structure
    print("\n[Test 2] Verifying mechanics JSON data...")
    if 'mechanics_json' in content:
        print("  ✓ JSON data is being passed to template")
        # Try to extract and parse the JSON
        import re
        json_match = re.search(r'const mechanics = ({.*?});', content, re.DOTALL)
        if json_match:
            print("  ✓ JSON data is properly embedded in script")
    else:
        print("  ✗ JSON data not found in template context")
        
else:
    print(f"  ✗ Failed to load page (Status: {response.status_code})")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
print("\nThe dynamic map should now:")
print("  • Display all mechanics as interactive markers on the map")
print("  • Allow zooming and panning")
print("  • Show popup with mechanic details on marker click")
print("  • Include Profile and Book buttons in popup")
print("  • Use OpenStreetMap tiles for map display")
print("=" * 70)
