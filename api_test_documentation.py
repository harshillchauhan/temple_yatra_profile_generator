#!/usr/bin/env python3
"""
MyTempleYatra Profile Image Generator API - Testing Script & Documentation
=========================================================================

This script demonstrates how to use the Profile Image Generator API
and provides comprehensive testing examples.

Requirements:
- requests library: pip install requests
- Pillow library: pip install Pillow
- Flask: pip install Flask

Usage:
1. Start the API server: python profile_image_api.py
2. Run this test script: python api_test_documentation.py
"""

import requests
import json
import time
import base64
from typing import Dict, List, Optional

# API Configuration
API_BASE_URL = "http://localhost:5000"
API_ENDPOINTS = {
    'health': f"{API_BASE_URL}/health",
    'generate': f"{API_BASE_URL}/generate",
    'generate_variants': f"{API_BASE_URL}/generate-variants",
    'bulk_generate': f"{API_BASE_URL}/bulk-generate",
    'colors': f"{API_BASE_URL}/colors",
    'stats': f"{API_BASE_URL}/stats",
    'image': f"{API_BASE_URL}/image",  # /<initials>/<filename>
    'image_base64': f"{API_BASE_URL}/image-base64"  # /<initials>/<filename>
}

class APITester:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def print_separator(self, title: str):
        """Print formatted separator"""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_response(self, response: requests.Response, title: str = "Response"):
        """Print formatted response"""
        print(f"\n📋 {title}:")
        print(f"Status Code: {response.status_code}")
        
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response: {response.text}")
    
    def test_health_check(self):
        """Test health check endpoint"""
        self.print_separator("Health Check Test")
        
        try:
            response = self.session.get(API_ENDPOINTS['health'])
            self.print_response(response, "Health Check")
            
            if response.status_code == 200:
                print("✅ Health check passed!")
            else:
                print("❌ Health check failed!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
    
    def test_single_generation(self):
        """Test single profile image generation"""
        self.print_separator("Single Image Generation Test")
        
        test_users = [
            {"first_name": "Arjun", "last_name": "Sharma"},
            {"first_name": "Priya", "last_name": "Patel"},
            {"first_name": "Vikram", "last_name": "Singh"},
            {"first_name": "Kavitha", "last_name": "Nair"}
        ]
        
        for user in test_users:
            print(f"\n🔄 Generating image for {user['first_name']} {user['last_name']}...")
            
            try:
                response = self.session.post(
                    API_ENDPOINTS['generate'],
                    json=user
                )
                
                self.print_response(response, f"Generation for {user['first_name']} {user['last_name']}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Successfully generated image for initials: {data['user_info']['initials']}")
                    print(f"🖼️ Image URL: {data['image']['url']}")
                else:
                    print(f"❌ Generation failed!")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error: {e}")
    
    def test_variants_generation(self):
        """Test multiple variants generation"""
        self.print_separator("Multiple Variants Generation Test")
        
        test_data = {
            "first_name": "Radha",
            "last_name": "Krishna",
            "num_variants": 5
        }
        
        print(f"🔄 Generating {test_data['num_variants']} variants for {test_data['first_name']} {test_data['last_name']}...")
        
        try:
            response = self.session.post(
                API_ENDPOINTS['generate_variants'],
                json=test_data
            )
            
            self.print_response(response, "Variants Generation")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Successfully generated {data['total_variants']} variants!")
                print(f"🆔 Initials: {data['user_info']['initials']}")
                
                for i, variant in enumerate(data['variants'], 1):
                    print(f"   Variant {i}: {variant['url']} (Color: {variant['bg_color']})")
            else:
                print("❌ Variants generation failed!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
    
    def test_bulk_generation(self):
        """Test bulk generation for multiple users"""
        self.print_separator("Bulk Generation Test")
        
        test_users = [
            {"first_name": "Ganesh", "last_name": "Iyer"},
            {"first_name": "Lakshmi", "last_name": "Devi"},
            {"first_name": "Karthik", "last_name": "Reddy"},
            {"first_name": "Sita", "last_name": "Ram"},
            {"first_name": "Hanuman", "last_name": "Das"}
        ]
        
        bulk_data = {"users": test_users}
        
        print(f"🔄 Generating images for {len(test_users)} users...")
        
        try:
            response = self.session.post(
                API_ENDPOINTS['bulk_generate'],
                json=bulk_data
            )
            
            self.print_response(response, "Bulk Generation")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Bulk generation completed!")
                print(f"📊 Total: {data['total_users']}, Successful: {data['successful_generations']}, Failed: {data['failed_generations']}")
                
                for result in data['results']:
                    if result['success']:
                        user = result['user']
                        print(f"   ✅ {user['first_name']} {user['last_name']} -> {result['initials']} -> {result['image']['url']}")
                    else:
                        print(f"   ❌ {result['user']} -> Error: {result['error']}")
            else:
                print("❌ Bulk generation failed!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
    
    def test_colors_endpoint(self):
        """Test colors endpoint"""
        self.print_separator("Colors Information Test")
        
        try:
            response = self.session.get(API_ENDPOINTS['colors'])
            self.print_response(response, "Available Colors")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Retrieved {data['total_colors']} colors!")
                print("🎨 Color palette:")
                for i, color in enumerate(data['colors'], 1):
                    print(f"   {i:2d}. {color}")
            else:
                print("❌ Failed to retrieve colors!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
    
    def test_stats_endpoint(self):
        """Test statistics endpoint"""
        self.print_separator("Statistics Test")
        
        try:
            response = self.session.get(API_ENDPOINTS['stats'])
            self.print_response(response, "Generation Statistics")
            
            if response.status_code == 200:
                data = response.json()
                stats = data['stats']
                print(f"✅ Retrieved statistics!")
                print(f"📊 Total initials generated: {stats['total_initials']}")
                print(f"📊 Total variants created: {stats['total_variants']}")
                
                if stats['initials_generated']:
                    print("📋 Breakdown by initials:")
                    for item in stats['initials_generated']:
                        print(f"   {item['initials']}: {item['variants']} variants")
            else:
                print("❌ Failed to retrieve statistics!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
    
    def test_image_serving(self):
        """Test image serving endpoints"""
        self.print_separator("Image Serving Test")
        
        # First generate an image
        user_data = {"first_name": "Test", "last_name": "User"}
        
        try:
            response = self.session.post(
                API_ENDPOINTS['generate'],
                json=user_data
            )
            
            if response.status_code == 200:
                data = response.json()
                initials = data['user_info']['initials']
                filename = data['image']['filename']
                
                print(f"🔄 Testing image serving for {initials}/{filename}...")
                
                # Test direct image serving
                image_url = f"{API_ENDPOINTS['image']}/{initials}/{filename}"
                img_response = self.session.get(image_url)
                
                if img_response.status_code == 200:
                    print(f"✅ Direct image serving works! Content-Type: {img_response.headers.get('Content-Type')}")
                    print(f"📏 Image size: {len(img_response.content)} bytes")
                else:
                    print(f"❌ Direct image serving failed! Status: {img_response.status_code}")
                
                # Test base64 image serving
                base64_url = f"{API_ENDPOINTS['image_base64']}/{initials}/{filename}"
                b64_response = self.session.get(base64_url)
                
                if b64_response.status_code == 200:
                    b64_data = b64_response.json()
                    print(f"✅ Base64 image serving works!")
                    print(f"🔗 Base64 prefix: {b64_data['image_base64'][:50]}...")
                else:
                    print(f"❌ Base64 image serving failed! Status: {b64_response.status_code}")
            else:
                print("❌ Could not generate test image for serving test!")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
    
    def test_error_handling(self):
        """Test error handling"""
        self.print_separator("Error Handling Test")
        
        error_tests = [
            {
                "name": "Empty request",
                "data": {},
                "expected_status": 400
            },
            {
                "name": "Missing last name",
                "data": {"first_name": "John"},
                "expected_status": 400
            },
            {
                "name": "Missing first name",
                "data": {"last_name": "Doe"},
                "expected_status": 400
            },
            {
                "name": "Empty names",
                "data": {"first_name": "", "last_name": ""},
                "expected_status": 400
            },
            {
                "name": "Invalid variants count",
                "data": {"first_name": "John", "last_name": "Doe", "num_variants": 20},
                "expected_status": 400
            }
        ]
        
        for test in error_tests:
            print(f"\n🔄 Testing: {test['name']}")
            
            try:
                response = self.session.post(
                    API_ENDPOINTS['generate'],
                    json=test['data']
                )
                
                if response.status_code == test['expected_status']:
                    print(f"✅ Correct error handling! Status: {response.status_code}")
                else:
                    print(f"❌ Unexpected status! Expected: {test['expected_status']}, Got: {response.status_code}")
                
                if response.status_code >= 400:
                    try:
                        error_data = response.json()
                        print(f"📝 Error message: {error_data.get('error', 'No error message')}")
                    except:
                        print(f"📝 Error response: {response.text}")
                        
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 MyTempleYatra Profile Image Generator API - Comprehensive Testing")
        print("=" * 80)
        
        tests = [
            self.test_health_check,
            self.test_single_generation,
            self.test_variants_generation,
            self.test_bulk_generation,
            self.test_colors_endpoint,
            self.test_stats_endpoint,
            self.test_image_serving,
            self.test_error_handling
        ]
        
        start_time = time.time()
        
        for test in tests:
            try:
                test()
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        end_time = time.time()
        
        print(f"\n{'='*80}")
        print(f"🏁 All tests completed in {end_time - start_time:.2f} seconds")
        print(f"{'='*80}")


def main():
    """Main function to run tests"""
    tester = APITester()
    tester.run_all_tests()

