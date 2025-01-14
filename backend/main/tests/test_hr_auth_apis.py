import datetime
import pytest
from django.test import Client
from main.utils import create_hr_user
from main.models import HR, User


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def csrf_token(client):
    """Fetch CSRF token."""
    response = client.get("/api/set-csrf-token")
    return response.json()["csrftoken"]


@pytest.fixture
def hr_user():
    """
    Utility function to create an HR user and their profile.
    """
    user = create_hr_user(
        first_name="Test",
        last_name="HR",
        email="test_hr@example.com",
        branch="Test Branch",
        birthday=datetime.date(1990, 1, 1),
        password="test_password"
    )
    return user


@pytest.mark.django_db
def test_register_hr(client):
    """Test HR registration."""
    payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "password": "securepassword",
        "branch": "HR",
        "birthday": "1990-01-01",
    }
    response = client.post("/api/register", payload, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.django_db
def test_hr_login(client, hr_user):
    """Test HR login."""

    response = client.post(
        "/api/login",
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.django_db
def test_logout(client, hr_user):
    """
    Test the logout functionality for the HR user.
    """
    # Step 1: Log in the HR user
    login_response = client.post(
        "/api/login", 
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json"
    )
    assert login_response.status_code == 200
    assert login_response.json()["success"] is True

    # Step 2: Get the CSRF token for logout
    csrf_response = client.get("/api/set-csrf-token")
    assert csrf_response.status_code == 200
    csrf_token = csrf_response.json().get("csrftoken")
    assert csrf_token is not None

    # Step 3: Include the CSRF token in the headers for the logout request
    client.cookies["csrftoken"] = csrf_token
    logout_response = client.post("/api/logout", HTTP_X_CSRFTOKEN=csrf_token)
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == f"{hr_user.username} Logged out"


@pytest.mark.django_db
def test_get_csrf_token(client):
    """Test CSRF token retrieval."""
    response = client.get("/api/set-csrf-token")
    assert response.status_code == 200
    csrf_token = response.json().get("csrftoken")
    assert csrf_token
    assert isinstance(csrf_token, str)
    assert len(csrf_token) > 0


@pytest.mark.django_db
def test_get_all_hrs(client, csrf_token, hr_user):
    """Test getting all HRs list."""
    # Login first
    client.post(
        "/api/login",
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json",
    )
    client.cookies["csrftoken"] = csrf_token

    # Create another HR for testing
    create_hr_user(
        first_name="Second",
        last_name="HR",
        email="second_hr@example.com",
        branch="Another Branch",
        birthday=datetime.date(1992, 2, 2),
        password="test_password2"
    )

    # Get all HRs
    response = client.get(
        "/api/hrs",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["hrs"]) == 2  # Should have two HRs
    assert any(hr["email"] == "test_hr@example.com" for hr in data["hrs"])
    assert any(hr["email"] == "second_hr@example.com" for hr in data["hrs"])


@pytest.mark.django_db
def test_get_hr_profile(client, csrf_token, hr_user):
    """Test viewing HR profile."""
    # Login first
    client.post(
        "/api/login",
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json",
    )
    client.cookies["csrftoken"] = csrf_token

    # View own profile
    response = client.get(
        f"/api/hr/{hr_user.username}",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["hr"]["email"] == "test_hr@example.com"
    assert data["hr"]["first_name"] == "Test"
    assert data["hr"]["last_name"] == "HR"


@pytest.mark.django_db
def test_update_hr_profile(client, csrf_token, hr_user):
    """Test updating HR profile."""
    # Login first
    client.post(
        "/api/login",
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json",
    )
    client.cookies["csrftoken"] = csrf_token

    # Update profile
    update_payload = {
        "first_name": "Updated",
        "last_name": "Name",
        "branch": "New Branch"
    }
    
    update_response = client.put(
        "/api/hr/update",
        update_payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    
    assert update_response.status_code == 200
    assert update_response.json()["success"] is True

    # Verify changes
    profile_response = client.get(
        f"/api/hr/{hr_user.username}",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    
    profile_data = profile_response.json()["hr"]
    assert profile_data["first_name"] == "Updated"
    assert profile_data["last_name"] == "Name"
    assert profile_data["branch"] == "New Branch"
