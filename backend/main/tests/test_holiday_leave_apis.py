import pytest
from django.test import Client
from datetime import date, timedelta
from main.models import Holiday, Leave, Employee
from main.utils import create_employee_user, create_leave
from main.tests.test_hr_auth_apis import csrf_token, hr_user  # Reuse fixtures

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def test_employee(client, csrf_token, hr_user):
    """Create a test employee and add some leaves."""
    employee = create_employee_user(
        first_name="Test",
        last_name="Employee",
        email="test.employee@example.com",
        phone_number="1234567890",
        department="IT",
        birthday="1990-01-01",
        date_of_joining="2023-01-01"
    )
    return employee

@pytest.mark.django_db
def test_get_all_holidays(client, csrf_token, hr_user):
    # Login first
    client.post("/api/login",
                {"username": hr_user.username, "password": "test_password"},
                content_type="application/json")
    client.cookies["csrftoken"] = csrf_token

    # Create test holidays
    holiday_data = [
        {"name": "New Year", "date": date(2024, 1, 1)},
        {"name": "Christmas", "date": date(2024, 12, 25)}
    ]
    for holiday in holiday_data:
        Holiday.objects.create(**holiday)

    # Get all holidays
    response = client.get("/api/holidays",
                         HTTP_X_CSRFTOKEN=csrf_token)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["holidays"]) == 2

@pytest.mark.django_db
def test_get_all_leaves(client, csrf_token, hr_user, test_employee):
    # Login first
    client.post("/api/login",
                {"username": hr_user.username, "password": "test_password"},
                content_type="application/json")
    client.cookies["csrftoken"] = csrf_token

    # Create test leaves using utility function
    create_leave(
        employee_username=test_employee.username,
        number_of_days=2,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        approvable=True
    )
    create_leave(
        employee_username=test_employee.username,
        number_of_days=3,
        start_date=date.today() + timedelta(days=10),
        end_date=date.today() + timedelta(days=13),
        approvable=False
    )

    # Get all leaves
    response = client.get("/api/leaves",
                         HTTP_X_CSRFTOKEN=csrf_token)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["leaves"]) == 2

@pytest.mark.django_db
def test_get_employee_leaves(client, csrf_token, hr_user, test_employee):
    # Login first
    client.post("/api/login",
                {"username": hr_user.username, "password": "test_password"},
                content_type="application/json")
    client.cookies["csrftoken"] = csrf_token

    # Create a leave for the employee
    employee = Employee.objects.get(username=test_employee)
    Leave.objects.create(
        employee=employee,
        number_of_days=5,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=5),
        approvable=True
    )

    # Get employee's leaves
    response = client.get(f"/api/employees/{test_employee.username}/leaves",
                         HTTP_X_CSRFTOKEN=csrf_token)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["leaves"]) == 1
    assert data["leaves"][0]["number_of_days"] == 5

@pytest.mark.django_db
def test_create_leave(client, csrf_token, hr_user, test_employee):
    # Login first
    client.post("/api/login",
                {"username": hr_user.username, "password": "test_password"},
                content_type="application/json")
    client.cookies["csrftoken"] = csrf_token

    payload = {
        "employee_username": test_employee.username,
        "number_of_days": 5,
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=5)),
        "approvable": True
    }

    response = client.post("/api/leaves/create",
                          payload,
                          content_type="application/json",
                          HTTP_X_CSRFTOKEN=csrf_token)
    
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    # Verify leave was created
    employee = Employee.objects.get(username=test_employee)
    assert Leave.objects.filter(employee=employee, number_of_days=5).exists()

@pytest.mark.django_db
def test_create_leave_validation(client, csrf_token, hr_user, test_employee):
    """Test leave creation with various scenarios."""
    # Login first
    client.post("/api/login",
                {"username": hr_user.username, "password": "test_password"},
                content_type="application/json")
    client.cookies["csrftoken"] = csrf_token

    # Test case 1: Valid leave creation
    payload = {
        "employee_username": test_employee.username,
        "number_of_days": 5,
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=5)),
        "approvable": True
    }
    response = client.post("/api/leaves/create",
                          payload,
                          content_type="application/json",
                          HTTP_X_CSRFTOKEN=csrf_token)
    
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    # Verify leave in database
    employee = Employee.objects.get(username=test_employee)
    leave = Leave.objects.get(employee=employee)
    assert leave.number_of_days == 5
    assert leave.start_date == date.today()
    assert leave.end_date == date.today() + timedelta(days=5)
    assert leave.approvable is True

    # Test case 2: Invalid employee username
    payload["employee_username"] = "nonexistent_user"
    response = client.post("/api/leaves/create",
                          payload,
                          content_type="application/json",
                          HTTP_X_CSRFTOKEN=csrf_token)
    
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Employee not found" in response.json()["message"]

    # Test case 3: End date before start date
    payload["employee_username"] = test_employee.username
    payload["start_date"] = str(date.today())
    payload["end_date"] = str(date.today() - timedelta(days=1))
    response = client.post("/api/leaves/create",
                          payload,
                          content_type="application/json",
                          HTTP_X_CSRFTOKEN=csrf_token)
    
    assert response.status_code == 200
    assert response.json()["success"] is False  # Should fail validation
