"""
Project Manager v: 0.6.4
"""
import json


class Project:
    def __init__(self, name, description, owner, members=[]):
        self.name = name
        self.description = description
        self.members = members.copy()
        self.owner = owner

    @staticmethod
    def get_fields():
        return 'name', 'description', 'members', 'owner'


class User:
    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password

    @staticmethod
    def get_fields():
        return 'login', 'email', 'password'


class Database:
    """
    JSON database for project manager
    """
    CLSS = {'users': User, 'projects': Project}

    def __init__(self, file_name='data.json'):
        self.file_name = file_name

    def _get_result_format(self):
        return {'projects': {}, "users": {}}

    def update_data(self, new_data):
        result = {'projects': [], "users": []}
        for group in new_data:
            for item in new_data[group]:
                result[group].append(new_data[group][item].__dict__)
        with open(self.file_name, 'w') as storage:
            json.dump(result, storage)

    def _parse_object(self, cls, item):
        fields = {name: item[name] for name in cls.get_fields()}
        return item[cls.get_fields()[0]], cls(**fields)

    def _parse_data(self, data):
        result = self._get_result_format()
        for group in data:
            for item in data[group]:
                key, obj = self._parse_object(self.CLSS[group], item)
                result[group][key] = obj
        return result

    def get_data(self):
        try:
            with open(self.file_name, 'r') as storage:
                return self._parse_data(json.load(storage))
        except FileNotFoundError:
            return self._get_result_format()


class Environment:
    """
    Main configuration
    """
    def __init__(self, db):
        self.db = db
        self.data = db.get_data()
        self.log_in_user = None

    def get_users(self):
        return self.data['users']

    def get_projects(self):
        return self.data['projects']

    def create_project(self, name, description, owner, members=[]):
        members = members.copy()
        if name in self.data['projects']:
            raise KeyError('The Projects name is already used')
        for member in members:
            if member not in self.data['users'].keys():
                raise KeyError('Members must be users')
        if owner not in self.data['users'].keys():
            raise KeyError('Owner must be user')

        try:
            self.data['projects'][name] = Project(name, description, owner, members)
        except ValueError:
            raise ValueError("Project cannot be created")
        self.db.update_data(self.data)

    def create_user(self, email, login, password):
        for user in self.data['users']:
            if login == user:
                raise KeyError('The User name or Email is already used')
            if email == self.data['users'][user].email:
                raise KeyError('The User name or Email is already used')

        try:
            self.data['users'][login] = User(email, login, password)
        except ValueError:
            raise ValueError("User cannot be created")
        self.db.update_data(self.data)

    def delete_project(self, project_name):
        if project_name in self.data['projects']:
            del self.data['projects'][project_name]
            self.db.update_data(self.data)

    def delete_user(self, user_name):
        if user_name in self.data['users']:
            del self.data['users'][user_name]

            for projects in self.data['projects']:
                if user_name in self.data['projects'][projects].members:
                    self.data['projects'][projects].members.remove(user_name)

            self.db.update_data(self.data)

    def update_project(self, project_name, property):
        if project_name in self.data["projects"].keys():

            if property[0] == 'name' and property[1] not in self.data['users'].keys():
                raise KeyError('Owner must be user')

            if property[0] == 'members':
                for member in property[1]:
                    if member not in self.data['users'].keys():
                        raise KeyError('Members must be users')

            setattr(self.data["projects"][project_name], property[0], property[1])

        self.db.update_data(self.data)

    def update_user(self, user_name, property):
        print(self.data["users"].keys())
        if user_name in self.data["users"].keys():
            setattr(self.data["users"][user_name], property[0], property[1])
        else:
            raise KeyError('There are no user with such name' )

        if property[0] in self.data["users"][user_name].__dict__:
            raise KeyError('There are not such property')

        if property[0] == "login":
            for projects in self.data['projects']:
                if user_name in self.data['projects'][projects].members:
                    self.data['projects'][projects].members.remove(user_name)
                    self.data['projects'][projects].members.append(property[1])

        self.db.update_data(self.data)

    def log_in(self, login, password):
        if login in self.data["users"] and \
                        self.data["users"][login].password == password:
            self.log_in_user = login
        else:
            raise KeyError("Wrong password or user name")


env = Environment(Database())
