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
