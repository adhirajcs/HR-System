from ninja import NinjaAPI
from ninja.security import django_auth
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .utils import create_hr_user

from .models import User, Employee, ProjectManager, HR, Holiday, Leave
from . import schemas

api = NinjaAPI(csrf=True)


@api.get("/set-csrf-token")
def get_csrf_token(request):
    return {"csrftoken": get_token(request)}


@api.post("/login")
def login_view(request, payload: schemas.SignInSchema):
    print(f"Payload received: {payload}")  # For debugging
    user = authenticate(request, username=payload.username, password=payload.password)
    print(f"Authenticated user: {user}")   # For debugging

    if user:
        if user.role == "HR":
            login(request, user)
            hr_profile = getattr(user, "hr_profile", None)
            if hr_profile:
                return {"success": True, "message": f"Welcome {hr_profile.first_name}!"}
            return {"success": False, "message": "HR profile not found"}
        return {"success": False, "message": "User is not an HR"}
    return {"success": False, "message": "Invalid credentials"}
  

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
            birthday=payload.birthday
        )
        return {"success": True, "message": "HR registered successfully", "username": user.username}
    except Exception as e:
        return {"success": False, "error": str(e)}