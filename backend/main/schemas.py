from ninja import Schema

class SignInSchema(Schema):
    username: str
    password: str


class RegisterHRSchema(Schema):
    first_name: str
    last_name: str
    email: str
    password: str
    branch: str
    birthday: str

class EmployeeCreateSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    department: str
    birthday: str
    date_of_joining: str
    reporting_manager: str = None

class EmployeeUpdateSchema(Schema):
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    department: str = None
    birthday: str = None
    date_of_joining: str = None
    reporting_manager: str = None

class ProjectManagerCreateSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    department: str
    birthday: str

class ProjectManagerUpdateSchema(Schema):
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    department: str = None
    birthday: str = None
