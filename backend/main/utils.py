from datetime import datetime
from .models import User, Employee, ProjectManager, HR

def create_employee_user(first_name, last_name, email, phone_number, department, birthday, date_of_joining, reporting_manager=None):
    """
    Utility to create an Employee user and associate it with an Employee profile.
    """
    # Generate a username by combining first name and current date
    username = f"{first_name.lower()}_{datetime.now().strftime('%Y%m%d')}"
    
    # Create the user
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role='EMPLOYEE'
    )
    
    # Create the Employee profile
    Employee.objects.create(
        username=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=department,
        birthday=birthday,
        date_of_joining=date_of_joining,  # Manual date input
        reporting_manager=reporting_manager
    )
    return user

def create_project_manager_user(first_name, last_name, email, phone_number, department, birthday):
    """
    Utility to create a Project Manager user and associate it with a Project Manager profile.
    """
    # Generate a username by combining first name and last name
    username = f"{first_name.lower()}_{last_name.lower()}"
    
    # Create the user
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role='PROJECT_MANAGER'
    )
    
    # Create the Project Manager profile
    ProjectManager.objects.create(
        username=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=department,
        birthday=birthday
    )
    return user

def create_hr_user(first_name, last_name, email, branch, birthday):
    """
    Utility to create an HR user and associate it with an HR profile.
    """
    # Generate a username by combining first name and branch
    username = f"{first_name.lower()}_{branch.lower().replace(' ', '_')}"  # Replace spaces with underscores in branch name
    
    # Create the user
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role='HR'
    )
    
    # Create the HR profile
    HR.objects.create(
        username=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        branch=branch,
        birthday=birthday
    )
    return user
