import pytest
from django.test import Client
from main.models import Employee
from main.tests.test_hr_auth_apis import csrf_token, hr_user  # Reuse fixtures


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_create_employee(client, csrf_token, hr_user):
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
        "date_of_joining": "2023-01-01",
    }
    response = client.post(
        "/api/employees/create",
        payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert Employee.objects.filter(email="john.doe@example.com").exists()


@pytest.mark.django_db
def test_update_employee(client, csrf_token, hr_user):
    # Create an employee first
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
        "date_of_joining": "2023-03-01",
    }
    create_response = client.post(
        "/api/employees/create",
        payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    created_data = create_response.json()
    assert create_response.status_code == 200
    assert created_data["success"] is True

    # Update the employee
    username = created_data["username"]
    update_payload = {"department": "Sales"}
    update_response = client.put(
        f"/api/employees/{username}",
        update_payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    assert update_response.status_code == 200
    updated_employee = Employee.objects.filter(email="jane.smith@example.com").first()
    assert updated_employee is not None
    assert updated_employee.department == "Sales"


@pytest.mark.django_db
def test_delete_employee(client, csrf_token, hr_user):
    # Create an employee first
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
        "date_of_joining": "2023-04-01",
    }
    create_response = client.post(
        "/api/employees/create",
        payload,
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    created_data = create_response.json()
    assert create_response.status_code == 200
    assert created_data["success"] is True

    # Delete the employee
    username = created_data["username"]
    delete_response = client.delete(
        f"/api/employees/{username}",
        content_type="application/json",
        HTTP_X_CSRFTOKEN=csrf_token,
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["success"] is True
    assert not Employee.objects.filter(email="bob.davis@example.com").exists()
