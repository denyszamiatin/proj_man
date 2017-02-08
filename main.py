"""

"""
import json


class Database:
    """
    Methods to work with files
    """
    def __init__(self, users_file='data_users', projects_file='data_projects'):
        self.users_file = users_file
        self.projects_file = projects_file

    def save_projects(self, projects):
        with open(self.projects_file, "wt") as f:
            for project in projects:
                f.write(json.dumps([project.name, project.description, project.owner, project.members]) + "\n")

    def save_users(self, users):
        with open(self.users_file, "wt") as f:
            for user in users:
                f.write(json.dumps([user.email, user.login, user.password]) + "\n")

    def _get_loader(self, item_type):
        if item_type == 'user':
            return self.users_file, self._load_user
        elif item_type == 'project':
            return self.projects_file, self._load_project
        else:
            raise ValueError("Invalid type")

    def load_items(self, item_type):
        filename, loader = self._get_loader(item_type)
        items = []
        try:
            with open(filename, "rt") as f:
                while True:
                    item = loader(f)
                    if not item:
                        return items
                    items.append(item)
        except FileNotFoundError:
            return items

    def _load_user(self, f):
        try:
            user = json.loads(f.readline())
        except json.decoder.JSONDecodeError:
            return False
        return User(*user)  # user is [email, login, password]

    def _load_project(self, f):
        try:
            project = json.loads(f.readline())
        except json.decoder.JSONDecodeError:
            return False
        return Project(*project)  # project is [name, description, owner, members]

class Environment:
    """
    Main configuration
    """
    def __init__(self, db):
        self.db = db
        self.projects = {}
        self.users = {}
        for user in self.db.load_items('user'):
            self.add_user(user)
        for project in self.db.load_items('project'):
            self.add_project(project)

    def add_project(self, project):
        if project.name in self.projects:
            raise KeyError(
                'There is an existing project with such name. Use another one'
            )
        project.register_observer(self)
        self.projects[project.name] = project

    def delete_project(self, name):
        try:
            del self.projects[name]
        except KeyError:
            raise KeyError('There is no project with such name')

    def add_user(self, user):
        if user.login in self.users:
            raise KeyError('There is a user with such name. Use another one')
        self.users[user.login] = user

    def delete_user(self, name):
        try:
            del self.users[name]
        except KeyError:
            raise KeyError('There is no user with such name')

    def notify(self, old_name, project):
        print(self.projects, old_name)
        self.delete_project(old_name)
        self.add_project(project)

    def get_users(self):
        users = []
        for user in self.users:
            users.append(self.users[user])
        return users

    def get_projects(self):
        projects = []
        for project in self.projects:
            projects.append(self.projects[project])
        return projects


class Project:
    def __init__(self, name, description, owner, members=[]):
        self.name = name
        self.description = description
        self.members = members
        self.owner = owner
        self.observers = []

    def update_description(self, description):
        self.description = description

    def update_name(self, name):
        old_name, self.name = self.name, name
        for observer in self.observers:
            print('Notify:', self.observers)
            observer.notify(old_name, self)

    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def add_member(self, user):
        self.members.append(user)

    def delete_member(self, name):
        try:
            del self.members[name]
        except KeyError:
            raise KeyError('There is no user with such name')


class User:
    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password

    def change_password(self, old_password, new_password):
        if old_password != self.password:
            raise ValueError('Password is wrong. Try again.')
        self.password = new_password

env = Environment(Database())

Database().save_users(env.get_users())
Database().save_projects(env.get_projects())
