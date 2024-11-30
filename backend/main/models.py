from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('EMPLOYEE', 'Employee'),
        ('PROJECT_MANAGER', 'Project Manager'),
        ('HR', 'HR'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Employee Model
class Employee(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_of_joining = models.DateField()
    birthday = models.DateField(null=True, blank=True)  # Optional birthday field
    reporting_manager = models.ForeignKey('ProjectManager', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Employee"

# Project Manager Model
class ProjectManager(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)  # Optional birthday field

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Project Manager"

# HR Model
class HR(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hr_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    branch = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)  # Optional birthday field

    def __str__(self):
        return f"{self.first_name} {self.last_name} - HR"

# Holiday List Table
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.date})"

# Leave Table
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    approvable = models.BooleanField(default=False)
    number_of_days = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Leave({self.employee.first_name} {self.employee.last_name}, {self.number_of_days} days)"