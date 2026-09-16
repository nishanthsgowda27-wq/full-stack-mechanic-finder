#!/usr/bin/env python
"""Test script to fetch /register/ and show response."""
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/register/')
    print(f"Status Code: {response.status}")
    content = response.read().decode('utf-8')
    print("=== HTML Content (first 1000 chars) ===")
    print(content[:1000])
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Response body:\n{e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
