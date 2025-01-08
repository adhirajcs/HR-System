from ninja import NinjaAPI
from ninja.security import django_auth
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .utils import (
    create_employee_user,
    create_hr_user,
    create_project_manager_user,
    delete_project_manager,
    update_employee,
    delete_employee,
    update_project_manager,
)

from .models import User, Employee, ProjectManager, HR, Holiday, Leave
from . import schemas

api = NinjaAPI()


@api.get("/set-csrf-token")
def get_csrf_token(request):
    return {"csrftoken": get_token(request)}


# ---------------------------------- HR APIs ---------------------------------- #

# Api for HR to register
@api.post("/register")
def register_hr(request, payload: schemas.RegisterHRSchema):
    try:
        # Call the utility function to create the HR user and profile
        user = create_hr_user(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password,
            branch=payload.branch,
            birthday=payload.birthday,
        )
        return {
            "success": True,
            "message": "HR registered successfully",
            "username": user.username,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# Api for HR to login
@api.post("/login")
def login_view(request, payload: schemas.SignInSchema):
    print(f"Payload received: {payload}")  # For debugging
    user = authenticate(request, username=payload.username, password=payload.password)
    print(f"Authenticated user: {user}")  # For debugging

    if user:
        if user.role == "HR":
            login(request, user)
            hr_profile = getattr(user, "hr_profile", None)
            if hr_profile:
                return {"success": True, "message": f"Welcome {hr_profile.first_name}!"}
            return {"success": False, "message": "HR profile not found"}
        return {"success": False, "message": "User is not an HR"}
    return {"success": False, "message": "Invalid credentials"}


# Api for HR to logout
@api.post("/logout", auth=django_auth)
def logout_view(request):
    username = request.user.username
    logout(request)
    return {"message": f"{username} Logged out"}


# ---------------------------------- Employee APIs for HR ---------------------------------- #

# Api for HR to create employee
@api.post("/employees/create", auth=django_auth)
def create_employee_handler(request, payload: schemas.EmployeeCreateSchema):
    if request.user.role != "HR":
        return {"success": False, "message": "Unauthorized"}
    user = create_employee_user(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone_number=payload.phone_number,
        department=payload.department,
        birthday=payload.birthday,
        date_of_joining=payload.date_of_joining,
        reporting_manager=None,
    )
    return {"success": True, "message": "Employee created", "username": user.username}


# Api for HR to update employee
@api.put("/employees/{username}", auth=django_auth)
def update_employee_handler(
    request, username: str, payload: schemas.EmployeeUpdateSchema
):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {"success": False, "message": "User not found"}

    try:
        employee = Employee.objects.get(username_id=user.id)
    except Employee.DoesNotExist:
        return {"success": False, "message": "Employee not found"}

    updated_employee = update_employee(
        username=user.username,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=getattr(payload, "email", None),  # or handle if needed
        phone_number=payload.phone_number,
        department=payload.department,
        birthday=payload.birthday,
        date_of_joining=payload.date_of_joining,
        reporting_manager=payload.reporting_manager,
    )

    if not updated_employee:
        return {"success": False, "message": "Unable to update Employee"}

    return {"success": True, "message": "Employee updated"}


# Api for HR to delete employee
@api.delete("/employees/{username}", auth=django_auth)
def delete_employee_handler(request, username: str):
    if request.user.role != "HR":
        return {"success": False, "message": "Unauthorized"}
    try:
        user = User.objects.get(username=username, role="EMPLOYEE")
    except User.DoesNotExist:
        return {"success": False, "message": "Employee not found"}
    if delete_employee(user.username):
        return {"success": True, "message": "Employee deleted"}
    return {"success": False, "message": "Failed to delete Employee"}


# ---------------------------------- Project Manager APIs for HR ---------------------------------- #

# Api for HR to create project manager
@api.post("/project_managers/create", auth=django_auth)
def create_project_manager_handler(
    request, payload: schemas.ProjectManagerCreateSchema
):
    if request.user.role != "HR":
        return {"success": False, "message": "Unauthorized"}
    user = create_project_manager_user(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone_number=payload.phone_number,
        department=payload.department,
        birthday=payload.birthday,
    )
    return {
        "success": True,
        "message": "Project Manager created",
        "username": user.username,
    }


# Api for HR to update project manager
@api.put("/project_managers/{username}", auth=django_auth)
def update_project_manager_handler(
    request, username: int, payload: schemas.ProjectManagerUpdateSchema
):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {"success": False, "message": "User not found"}
    
    try:
        project_manager = ProjectManager.objects.get(username_id=user.id)
    except ProjectManager.DoesNotExist:
        return {"success": False, "message": "Project Manager not found"}
    
    updated_project_manager = update_project_manager(
        username=user.username,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=getattr(payload, "email", None),  # or handle if needed
        phone_number=payload.phone_number,
        department=payload.department,
        birthday=payload.birthday,
    )

    if not updated_project_manager:
        return {"success": False, "message": "Unable to update Project Manager"}
    
    return {"success": True, "message": "Project Manager updated"}


# Api for HR to delete project manager
@api.delete("/project_managers/{username}", auth=django_auth)
def delete_project_manager_handler(request, username: int):
    if request.user.role != "HR":
        return {"success": False, "message": "Unauthorized"}
    try:
        user = User.objects.get(username=username, role="PROJECT_MANAGER")
    except User.DoesNotExist:
        return {"success": False, "message": "Project Manager not found"}
    if delete_project_manager(user.username):
        return {"success": True, "message": "Project Manager deleted"}
    return {"success": False, "message": "Failed to delete Project Manager"}