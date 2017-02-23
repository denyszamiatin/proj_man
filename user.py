from project_manager_error import UserError
import re



def login_validation(value):
    if len(value) < 2:
        raise UserError("Login is too short - minimum 2 characters")
    if len(value) > 12:
        raise UserError("Login is too long - maximum 12 characters")
    if not re.match('^[a-zA-Z0-9]+$', value):
        raise UserError("Login is invalid - can contain only letters and numbers")


def email_validation(value):
    if  not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', value):
        raise UserError("Email is invalid")


def password_validation(value):
    if len(value) < 2:
        raise UserError("Password is too short - minimum 2 characters")
    if len(value) > 12:
        raise UserError("Password is too long - maximum 12 characters")


def user_create_validation(fn):
    def wrap(self, email, login, password):

        email_validation(email)
        login_validation(login)
        password_validation(password)

        return fn(self, email, login, password)
    return wrap


def user_update_validation(fn):
    def wrap(self, name, value):

        if name == 'login': login_validation(value)
        if name == 'email': email_validation(value)
        if name == 'password': password_validation(value)

        return fn(self, name, value)
    return wrap



class User:
    @user_create_validation
    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password

    @staticmethod
    def get_fields():
        return 'login', 'email', 'password'

    @user_update_validation
    def update_property(self, name, value):
        if not hasattr(self, name):
            raise UserError("User doesn't have such attribute")
        self._set_property(name, value)

    @user_update_validation
    def _set_property(self, name, value):
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