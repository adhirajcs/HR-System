from datetime import datetime
from .models import User, Employee, ProjectManager, HR, Holiday, Leave


# --------------------- Utility functions for HR --------------------- #

# Utility function to create HR user
def create_hr_user(first_name, last_name, email, branch, birthday, password):
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
        password=password,
        role="HR",
    )

    # Create the HR profile
    HR.objects.create(
        username=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        branch=branch,
        birthday=birthday,
    )
    return user


# Utility function to update HR data
def update_hr(
    username,
    first_name=None,
    last_name=None,
    email=None,
    branch=None,
    birthday=None,
):
    """
    Utility to update HR data by username and update the associated User as well.
    """
    try:
        user = User.objects.get(username=username, role="HR")
        hr_profile = HR.objects.get(username=user)
        
        if first_name:
            user.first_name = first_name
            hr_profile.first_name = first_name
        if last_name:
            user.last_name = last_name
            hr_profile.last_name = last_name
        if email:
            user.email = email
            hr_profile.email = email
        if branch:
            hr_profile.branch = branch
        if birthday:
            hr_profile.birthday = birthday
        
        user.save()
        hr_profile.save()
        return hr_profile
    except (User.DoesNotExist, HR.DoesNotExist):
        return None


def get_all_hrs():
    """
    Utility to get all HR profiles with their user data.
    Returns a list of HR profiles or empty list if none found.
    """
    try:
        hrs = HR.objects.all().select_related('username')
        hr_list = []
        for hr in hrs:
            hr_list.append({
                "username": hr.username.username,
                "first_name": hr.first_name,
                "last_name": hr.last_name,
                "email": hr.email,
                "branch": hr.branch,
                "birthday": str(hr.birthday) if hr.birthday else None
            })
        return hr_list
    except Exception:
        return []

def get_hr_by_username(username):
    """
    Utility to get HR profile by username.
    Returns HR profile data or None if not found.
    """
    try:
        user = User.objects.get(username=username, role="HR")
        hr = HR.objects.get(username=user)
        return {
            "username": hr.username.username,
            "first_name": hr.first_name,
            "last_name": hr.last_name,
            "email": hr.email,
            "branch": hr.branch,
            "birthday": str(hr.birthday) if hr.birthday else None
        }
    except (User.DoesNotExist, HR.DoesNotExist):
        return None


# --------------------- Utility functions for Employee --------------------- #

# Utility function to create employee user data
def create_employee_user(
    first_name,
    last_name,
    email,
    phone_number,
    department,
    birthday,
    date_of_joining,
    reporting_manager=None,
):
    """
    Utility to create an Employee user and associate it with an Employee profile.
    """
    # Generate a username by combining first name and current date and time
    username = f"{first_name.lower()}_{datetime.now().strftime('%y%m%d%H%M%S')}"

    # Create the user
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role="EMPLOYEE",
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
        reporting_manager=reporting_manager,
    )
    return user


# Utility function to update employee user data
def update_employee(
    username,
    first_name=None,
    last_name=None,
    email=None,
    phone_number=None,
    department=None,
    birthday=None,
    date_of_joining=None,
    reporting_manager=None,
):
    """
    Utility to update Employee data by username and update the associated User as well.
    """
    try:
        user = User.objects.get(username=username, role="EMPLOYEE")
        employee_profile = Employee.objects.get(username=user)
        if first_name:
            user.first_name = first_name
            employee_profile.first_name = first_name
        if last_name:
            user.last_name = last_name
            employee_profile.last_name = last_name
        if email:
            user.email = email
            employee_profile.email = email
        if phone_number:
            employee_profile.phone_number = phone_number
        if department:
            employee_profile.department = department
        if birthday:
            employee_profile.birthday = birthday
        if date_of_joining:
            employee_profile.date_of_joining = date_of_joining
        if reporting_manager:
            employee_profile.reporting_manager = reporting_manager

        user.save()
        employee_profile.save()
        return employee_profile
    except (User.DoesNotExist, Employee.DoesNotExist):
        return None


# Utility function to delete employee data
def delete_employee(username):
    """
    Utility to delete Employee data by username.

    Returns:
        bool: True if the employee is successfully deleted, False if the employee does not exist.
    """
    try:
        user = User.objects.get(username=username, role="EMPLOYEE")
        employee = Employee.objects.get(username=user)
        employee.delete()
        user.delete()
        return True
    except (User.DoesNotExist, Employee.DoesNotExist):
        return False


def get_all_employees():
    """Utility to get all employees with their user data."""
    employees = Employee.objects.all().select_related('username')
    return [{
        "username": emp.username.username,
        "first_name": emp.first_name,
        "last_name": emp.last_name,
        "email": emp.email,
        "department": emp.department,
        "date_of_joining": str(emp.date_of_joining),
        "phone_number": emp.phone_number,
        "birthday": str(emp.birthday) if emp.birthday else None
    } for emp in employees]


# --------------------- Utility functions for Project Manager --------------------- #

# Utility function to create project manager user
def create_project_manager_user(
    first_name, last_name, email, phone_number, department, birthday
):
    """
    Utility to create a Project Manager user and associate it with a Project Manager profile.
    """
    # Generate a username by combining first name and last name
    username = f"{first_name.lower()}_{datetime.now().strftime('%y%m%d%H%M%S')}"

    # Create the user
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role="PROJECT_MANAGER",
    )

    # Create the Project Manager profile
    ProjectManager.objects.create(
        username=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        department=department,
        birthday=birthday,
    )
    return user


# Utility function to update project manager user data
def update_project_manager(
    username,
    first_name=None,
    last_name=None,
    email=None,
    phone_number=None,
    department=None,
    birthday=None,
):
    """
    Utility to update Project manager data by username and update the associated User as well.
    """
    try:
        user = User.objects.get(username=username, role="PROJECT_MANAGER")
        project_manager_profile = ProjectManager.objects.get(username=user)
        if first_name:
            user.first_name = first_name
            project_manager_profile.first_name = first_name
        if last_name:
            user.last_name = last_name
            project_manager_profile.last_name = last_name
        if email:
            user.email = email
            project_manager_profile.email = email
        if phone_number:
            project_manager_profile.phone_number = phone_number
        if department:
            project_manager_profile.department = department
        if birthday:
            project_manager_profile.birthday = birthday
        
        user.save()
        project_manager_profile.save()
        return project_manager_profile
    except (User.DoesNotExist, project_manager_profile.DoesNotExist):
        return None
    

# Utility function to delete project manager data
def delete_project_manager(username):
    """
    Utility to delete Project Manager data by username.
    
    Returns:
        bool: True if the project manager is successfully deleted, False if the project manager does not exist.
    """
    try:
        user = User.objects.get(username=username, role="PROJECT_MANAGER")
        projectmanager = ProjectManager.objects.get(username=user)
        projectmanager.delete()
        user.delete()
        return True
    except (User.DoesNotExist, Employee.DoesNotExist):
        return False


def get_all_project_managers():
    """Utility to get all project managers with their user data."""
    managers = ProjectManager.objects.all().select_related('username')
    return [{
        "username": pm.username.username,
        "first_name": pm.first_name,
        "last_name": pm.last_name,
        "email": pm.email,
        "department": pm.department,
        "phone_number": pm.phone_number,
        "birthday": str(pm.birthday) if pm.birthday else None
    } for pm in managers]

def get_all_holidays():
    """Utility to get all holidays."""
    holidays = Holiday.objects.all()
    return [{
        "name": holiday.name,
        "date": str(holiday.date)
    } for holiday in holidays]

def get_all_leaves():
    """Utility to get all leaves."""
    leaves = Leave.objects.all().select_related('employee')
    return [{
        "employee_name": f"{leave.employee.first_name} {leave.employee.last_name}",
        "number_of_days": leave.number_of_days,
        "start_date": str(leave.start_date),
        "end_date": str(leave.end_date),
        "approvable": leave.approvable
    } for leave in leaves]

def get_user_leaves(username, role):
    """Utility to get leaves for any employee (including project managers)."""
    try:
        user = User.objects.get(username=username)
        leaves = Leave.objects.filter(employee__username=user)
        return [{
            "employee_name": f"{leave.employee.first_name} {leave.employee.last_name}",
            "number_of_days": leave.number_of_days,
            "start_date": str(leave.start_date),
            "end_date": str(leave.end_date),
            "approvable": leave.approvable
        } for leave in leaves]
    except User.DoesNotExist:
        return None