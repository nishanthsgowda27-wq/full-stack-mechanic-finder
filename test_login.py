#!/usr/bin/env python
"""Test login with demo credentials."""
import urllib.request
import urllib.parse

# First, fetch the login page to get CSRF token
try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/login/')
    html = response.read().decode('utf-8')
    
    # Extract CSRF token from HTML
    import re
    csrf_match = re.search(r'csrfmiddlewaretoken["\']?\s*value=["\']([^"\']+)["\']', html)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"✓ Login page loaded (HTTP {response.status})")
        print(f"✓ CSRF token found: {csrf_token[:20]}...")
        
        # Try login
        login_data = urllib.parse.urlencode({
            'username': 'user1',
            'password': 'password123',
            'csrfmiddlewaretoken': csrf_token
        }).encode('utf-8')
        
        req = urllib.request.Request('http://127.0.0.1:8000/login/', data=login_data, method='POST')
        req.add_header('Referer', 'http://127.0.0.1:8000/login/')
        
        try:
            response = urllib.request.urlopen(req)
            print(f"✓ Login POST request successful (HTTP {response.status})")
        except urllib.error.HTTPError as e:
            # 302 is redirect (success), 200 is form redisplay (failure)
            if e.code == 302:
                print(f"✓ Login successful - redirect response (HTTP {e.code})")
                if 'Location' in e.headers:
                    print(f"  Redirected to: {e.headers['Location']}")
            else:
                print(f"⚠ Login response: HTTP {e.code}")
    else:
        print("⚠ CSRF token not found in login page")
except Exception as e:
    print(f"✗ Error: {e}")
