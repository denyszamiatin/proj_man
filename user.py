
from project_manager_error import UserError
import re
import hashlib


def login_validation(value):
    if not re.match('^[a-zA-Z0-9]{2,12}$', value):
        raise UserError("Login is invalid - can contain only letters and numbers")


def email_validation(value):
    if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', value):
        raise UserError("Email is invalid")


def password_validation(value):
    if not 2 < len(value) < 12:
        raise UserError("Password is too short - minimum 2 characters")


def user_create_validation(fn):
    def wrap(self, email, login, password, newuser=False):
        email_validation(email)
        login_validation(login)
        if newuser:
            password_validation(password)
            newuser = False
        return fn(self, email, login, password, newuser)
    return wrap


def user_update_validation(fn):
    def wrap(self, name, value):
        try:
            {
                'login': login_validation,
                'email': email_validation,
                'password': password_validation,
            }[name](value)
        except KeyError:
            raise UserError("User doesn't have such attribute")
        return fn(self, name, value)
    return wrap


class User:
    @user_create_validation
    def __init__(self, email, login, password, newuser=False):
        self.email = email
        self.login = login
        self.newUser = newuser
        self.password = self.hash_password(password)

    def hash_password(self, password):
        if self.newUser:
            return hashlib.md5(password.encode('utf-8')).hexdigest()
        return password

    @staticmethod
    def get_fields():
        return 'login', 'email', 'password'

    @user_update_validation
    def update_property(self, name, value):
        if name == "password":
            value = self.hash_password(value)
        setattr(self, name, value)


if __name__ == "__main__":
    user = User('malfar@ukr.net', 'idsa', '1546546')
    print([(key, value) for key, value in user.__dict__.items()])
    user.update_property('login', 'igor')
    print([(key, value) for key, value in user.__dict__.items()])
    user.update_property('email', 'test@gmail.com')
    print([(key, value) for key, value in user.__dict__.items()])
    user.update_property('password', '5555')
    print([(key, value) for key, value in user.__dict__.items()])
