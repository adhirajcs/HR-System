import pytest
from django.test import Client
from main.models import ProjectManager
from main.tests.test_hr_auth_apis import csrf_token, hr_user  # Reuse fixtures


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_create_project_manager(client, csrf_token, hr_user):
    # Log in HR user
    client.post(
        "/api/login",
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json",
    )
    client.cookies["csrftoken"] = csrf_token

    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "department": "Engineering",
        "birthday": "1992-02-20",
    }
    response = client.post(
        "/api/project_managers/create",
        payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert ProjectManager.objects.filter(email="john.doe@example.com").exists()


@pytest.mark.django_db
def test_update_project_manager(client, csrf_token, hr_user):
    # Create a project manager first
    client.post(
        "/api/login",
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json",
    )
    client.cookies["csrftoken"] = csrf_token
    payload = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone_number": "9876543210",
        "department": "Engineering",
        "birthday": "1993-03-15",
    }
    create_response = client.post(
        "/api/project_managers/create",
        payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    created_data = create_response.json()
    assert create_response.status_code == 200
    assert create_response.json()["success"] is True

    # Update the project manager
    username = created_data["username"]
    update_payload = {
        "department": "Sales",
        "phone_number": "0987654321",
        "email": "jane.new@example.com",
    }
    update_response = client.put(
        f"/api/project_managers/{username}",
        update_payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    assert update_response.status_code == 200
    updated_pm = ProjectManager.objects.filter(email="jane.smith@example.com").first()
    assert updated_pm is not None
    assert updated_pm.department == "Sales"


@pytest.mark.django_db
def test_delete_project_manager(client, csrf_token, hr_user):
    # Create a project manager first
    client.post(
        "/api/login",
        {"username": hr_user.username, "password": "test_password"},
        content_type="application/json",
    )
    client.cookies["csrftoken"] = csrf_token
    payload = {
        "first_name": "Bob",
        "last_name": "Davis",
        "email": "bob.davis@example.com",
        "phone_number": "5555555555",
        "department": "Marketing",
        "birthday": "1994-04-10",
    }
    create_response = client.post(
        "/api/project_managers/create",
        payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )

    created_data = create_response.json()
    assert create_response.status_code == 200
    assert create_response.json()["success"] is True

    # Delete the project manager
    username = created_data["username"]
    delete_response = client.delete(
        f"/api/project_managers/{username}",
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["success"] is True
    assert not ProjectManager.objects.filter(email="bob.davis@example.com").exists()