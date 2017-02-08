"""
Project Manager v: 0.3.1
"""
import json



class Database:
    def __init__(self, users_file='data_users', projects_file='data_projects'):
        try:
            storage = open('data.json')
            self.data = json.load(storage)
            storage.close()
        except FileNotFoundError:
            self.data = {}

    def get_users(self):
        return self.data["users"]

    def get_projects(self):
        return self.data["projects"]

    def add_project_to_db(self, project):
        json_project_obj = {}
        for property in project.__dict__.keys():
            if property != 'observers':
                json_project_obj[property] = getattr(project, property)

        if not json_project_obj in self.get_users():
            self.data["projects"].append(json_project_obj)
        else:
            raise KeyError('The project already exist')
        self.update_db()


    def del_project_from_db(self, prj_name):
        for prj in self.get_projects():
            if prj_name == prj['name']:
                self.data["projects"].remove(prj)

        self.update_db()

    def del_user_from_db(self, user_name):
        for user in self.get_users():
            if user_name == user['login']:
                self.data["users"].remove(user)

        self.update_db()

    def add_user_to_db(self, user):
        json_user_obj = {}
        for property in user.__dict__.keys():
            json_user_obj[property] = getattr(user, property)

        if not json_user_obj in self.get_users():
            self.data["users"].append(json_user_obj)
        else:
            raise KeyError('This name is used')
        self.update_db()


    def update_db(self):
        try:
            storage = open('data.json', 'w')
            json.dump(self.data, storage)
            storage.close()
        except FileNotFoundError:
            return self.data


class Environment:
    """
    Main configuration
    """
    def __init__(self, db):
        self.db = db
        self.projects = {}
        self.users = {}


        for user in self.db.get_users():
            self.users[user['login']] = User(user['email'], user['login'], user['password'])
        for project in self.db.get_projects():
            self.projects[project['name']] = Project(project['name'], project['description'], project['owner'], ['project.members'])

    def add_project(self, project):
        if project.name in self.projects:
            raise KeyError(
                'There is an existing project with such name. Use another one'
            )
        project.register_observer(self)
        self.projects[project.name] = project

        self.db.add_project_to_db(project) #save projct to json file

    def delete_project(self, name):
        try:
            del self.projects[name]
        except KeyError:
            raise KeyError('There is no project with such name')
        else:
            self.db.del_project_from_db(name) #delete project from json file

    def add_user(self, user):
        if user.login in self.users:
            raise KeyError('There is a user with such name. Use another one')
        self.users[user.login] = user
        self.db.add_user_to_db(user) #add user to json file

    def delete_user(self, name):
        try:
            del self.users[name]
        except KeyError:
            raise KeyError('There is no user with such name')
        else:
            self.db.del_user_from_db(name) #delete user from json file

    def notify(self, old_name, project):
        print(self.projects, old_name)
        self.delete_project(old_name)
        self.add_project(project)


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
