# from rest_framework import serializers
# from .models import User, Employee, ProjectManager, HR, Holiday, Leave

# # Serializer for User
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

# # Serializer for Employee
# class EmployeeSerializer(serializers.ModelSerializer):
#     username = UserSerializer()  # Nested User serializer for Employee's User data

#     class Meta:
#         model = Employee
#         fields = [
#             'id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 
#             'department', 'designation', 'salary', 'date_of_joining', 'birthday', 
#             'reporting_manager'
#         ]

# # Serializer for Project Manager
# class ProjectManagerSerializer(serializers.ModelSerializer):
#     username = UserSerializer()  # Nested User serializer

#     class Meta:
#         model = ProjectManager
#         fields = [
#             'id', 'username', 'first_name', 'last_name', 'email', 
#             'phone_number', 'department', 'birthday'
#         ]

# # Serializer for HR
# class HRSerializer(serializers.ModelSerializer):
#     username = UserSerializer()  # Nested User serializer

#     class Meta:
#         model = HR
#         fields = [
#             'id', 'username', 'first_name', 'last_name', 'email', 
#             'branch', 'birthday'
#         ]

# # Serializer for Holiday
# class HolidaySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Holiday
#         fields = ['id', 'name', 'date']

# # Serializer for Leave
# class LeaveSerializer(serializers.ModelSerializer):
#     employee = EmployeeSerializer()  # Nested Employee serializer

#     class Meta:
#         model = Leave
#         fields = [
#             'id', 'employee', 'approvable', 'number_of_days', 
#             'start_date', 'end_date'
#         ]