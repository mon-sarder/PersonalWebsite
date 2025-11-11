"""
Simple script to test the API endpoints
Make sure the Flask server is running before executing this script
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_health_check():
    """Test health endpoint"""
    print("\n1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_get_projects():
    """Test getting all projects"""
    print("\n2. Testing GET /api/projects...")
    response = requests.get(f"{BASE_URL}/api/projects")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data.get('projects', []))} projects")
    return response.status_code == 200


def test_create_project():
    """Test creating a new project"""
    print("\n3. Testing POST /api/projects...")
    project_data = {
        "title": "Test Project",
        "description": "This is a test project created via API",
        "tech_stack": ["Python", "Flask", "MongoDB"],
        "github_link": "https://github.com/test/project",
        "live_link": "https://testproject.com"
    }
    response = requests.post(
        f"{BASE_URL}/api/projects",
        json=project_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201, response.json().get('id')


def test_get_skills():
    """Test getting all skills"""
    print("\n4. Testing GET /api/skills...")
    response = requests.get(f"{BASE_URL}/api/skills")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data.get('skills', []))} skills")

    # Test grouped skills
    print("\n5. Testing GET /api/skills?grouped=true...")
    response = requests.get(f"{BASE_URL}/api/skills?grouped=true")
    data = response.json()
    print(f"Categories: {list(data.get('skills', {}).keys())}")
    return response.status_code == 200


def test_contact_form():
    """Test contact form submission"""
    print("\n6. Testing POST /api/contact...")
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test message from the API test script."
    }
    response = requests.post(
        f"{BASE_URL}/api/contact",
        json=contact_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201


def test_analytics_track():
    """Test analytics tracking"""
    print("\n7. Testing POST /api/analytics/track...")

    # Track page view
    page_view_data = {
        "type": "page_view",
        "page": "/about"
    }
    response = requests.post(
        f"{BASE_URL}/api/analytics/track",
        json=page_view_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Page view tracking - Status: {response.status_code}")

    # Track project click
    project_click_data = {
        "type": "project_click",
        "project_id": "test123",
        "project_title": "Test Project"
    }
    response = requests.post(
        f"{BASE_URL}/api/analytics/track",
        json=project_click_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Project click tracking - Status: {response.status_code}")
    return response.status_code == 201


def test_analytics_dashboard():
    """Test analytics dashboard"""
    print("\n8. Testing GET /api/analytics/dashboard...")
    response = requests.get(f"{BASE_URL}/api/analytics/dashboard?days=7")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total Page Views: {data.get('total_page_views', 0)}")
        print(f"Total Project Clicks: {data.get('total_project_clicks', 0)}")
        print(f"Unique Visitors: {data.get('unique_visitors', 0)}")
    return response.status_code == 200


def run_all_tests():
    """Run all API tests"""
    print("=" * 60)
    print("API Testing Suite")
    print("=" * 60)

    results = []

    try:
        results.append(("Health Check", test_health_check()))
        results.append(("Get Projects", test_get_projects()))
        success, project_id = test_create_project()
        results.append(("Create Project", success))
        results.append(("Get Skills", test_get_skills()))
        results.append(("Contact Form", test_contact_form()))
        results.append(("Analytics Tracking", test_analytics_track()))
        results.append(("Analytics Dashboard", test_analytics_dashboard()))

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API.")
        print("Make sure the Flask server is running on http://localhost:5000")
        return

    # Print summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:<30} {status}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()