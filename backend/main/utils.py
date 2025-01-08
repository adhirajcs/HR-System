from datetime import datetime
from .models import User, Employee, ProjectManager, HR


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