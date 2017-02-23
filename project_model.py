"""
Project Manager v: 0.7.4
"""

from project import Project
from user import User
from database_json import Database
from project_manager_error import DatabaseUserError, DatabaseProjectError


def add_project_validation(fn):
    def wrapped(self, project):

        if not isinstance(project, Project):
            raise DatabaseProjectError('It is not a valid project instance')

        if self.is_project_exist(project.name):
            raise DatabaseProjectError('The Projects name is already used')

        for member in project.members:
            if not self.is_user_exist(member):
                raise DatabaseProjectError('Members must be users')

        if not self.is_user_exist(project.author):
            raise DatabaseProjectError('Author must be user')

        return fn(self, project)

    return wrapped


def delete_project_validation(fn):
    def wrapped(self, project_name):

        if not self.is_project_exist(project_name):
            raise DatabaseProjectError("Project with this name doesn't exist")

        return fn(self, project_name)
    return wrapped


def add_user_validation(fn):
    def wrapped(self, user):

        if not isinstance(user, User):
            raise DatabaseUserError('It is not a valid user instance')
        if user.login in [duser.login for duser in self.data['users']]:
            raise DatabaseUserError('The User name or Email is already used')
        if user.email in [duser.email for duser in self.data['users']]:
            raise DatabaseUserError('The User name or Email is already used')

        return fn(self, user)

    return wrapped


def delete_user_validation(fn):
    def wrapped(self, user_name):

        if user_name not in self.get_users():
            raise DatabaseUserError("User doesn't exist")

        return fn(self, user_name)
    return wrapped


def update_project_validation(fn):
    def wrapped(self, project_name, property):

        if project_name in self.get_projects():
            if property[0] == 'author' and property[1] not in self.get_users():
                raise DatabaseProjectError('Author must be user')

            if property[0] == 'members':
                for member in property[1]:
                    if member not in self.get_users():
                        raise KeyError('Members must be users')

            return fn(self, project_name, property)
        else:
            raise DatabaseProjectError("Project with this name doesn't exist")

    return wrapped


def update_user_validation(fn):
    def wrapped(self, user_name, property):
        if user_name in self.get_users():
            return fn(self, user_name, property)
        else:
            raise DatabaseUserError('There are no user with such name')

    return wrapped


class ModelDatabase:
    """
    Main configuration
    """
    def __init__(self, db):
        self.db = db
        self.data = db.get_data()

    def get_users(self):
        return [user.login for user in self.data['users']]

    def get_projects(self):
        return [project.name for project in self.data['projects']]

    def is_project_exist(self, project_name):
        return project_name in [project.name for project in self.data['projects']]

    def is_user_exist(self, user):
        return user in [user.login for user in self.data['users']]

    @add_project_validation
    def add_project(self, project):
        self.data['projects'].append(project)
        self.db.update_data(self.data)


    @delete_project_validation
    def delete_project(self, project_name):
        for project in self.data['projects']:
            if project_name == project.name: self.data['projects'].remove(project)

        self.db.update_data(self.data)

    @update_project_validation
    def update_project(self, project_name, property_):
        for project in self.data['projects']:
            if project_name == project.name:
                project.update_property(*property_)
        self.db.update_data(self.data)

    @add_user_validation
    def add_user(self, user):
        self.data['users'].append(user)
        self.db.update_data(self.data)

    @delete_user_validation
    def delete_user(self, user_name):
        for project in self.data['projects']:
            project.remove_member(user_name)
            if user_name == project.author:
                project.author = 'No author'

        for user in self.data['users']:
            if user_name == user.login:
                self.data['users'].remove(user)

        self.db.update_data(self.data)

    @update_user_validation
    def update_user(self, user_name, property):

        if property[0] == "login":
            for project in self.data['projects']:
                if user_name in project.members:
                    project.remove_member(user_name)
                    project.add_member(property[1])

                if user_name == project.author:
                    project.author = property[1]

        for user in self.data['users']:
            if user_name == user.login:
                user.update_property(*property)

        self.db.update_data(self.data)


if __name__ == "__main__":
    a = ModelDatabase(Database())
    user = User('wifi@gmail.com', 'masha', '789')
    print(a.get_users())
    a.update_user('tom', ('email', 'vlad@ukr.net'))
    print(a.get_users())


