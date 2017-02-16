"""
Project Manager v: 0.6.4
"""
import json


class Database:
    """
    JSON database for project manager
    """
    def __init__(self, file_name='data.json'):
        self.file_name = file_name

    def update_data(self, new_data):
        result = {'projects': [], "users": []}
        for group in new_data:
            for item in new_data[group]:
                result[group].append(new_data[group][item].__dict__)
        with open(self.file_name, 'w') as storage:
            json.dump(result, storage)

    def get_data(self):
        result = {'projects': {}, "users": {}}
        try:
            with open(self.file_name, 'r') as storage:
                data = json.load(storage)
                for group in data:
                    for item in data[group]:
                        if group == 'users':
                            result[group][item['login']] = User(item['email'], item['login'], item['password'])
                        elif group == 'projects':
                            result[group][item['name']] = Project(item['name'], item['description'],
                                                                  item['owner'], item['members'])
                return result
        except FileNotFoundError:
            return result


class Environment:
    """
    Main configuration
    """
    def __init__(self, db):
        self.db = db
        self.data = db.get_data()

    def get_users(self):
        return self.db.get_data()['users']

    def get_projects(self):
        return self.db.get_data()['projects']

    def add_project(self, new_project):

        for project in self.data['projects']:
            if new_project.name == project:
                raise KeyError('The Projects name is already used')

        for member in new_project.members:
            if member not in self.data['users'].keys():
                raise KeyError('Members must be users')

        if new_project.owner not in self.data['users'].keys():
            raise KeyError('Owner must be user')

        self.data['projects'][new_project.name] = new_project
        self.db.update_data(self.data)

    def add_user(self, new_user):
        for user in self.data['users']:
            if new_user.login == user:
                raise KeyError('The User name or Email  is already used')
            if new_user.email == self.data['users'][user].email:
                raise KeyError('The User name or Email  is already used')
        else:
            self.data['users'][new_user.login] = new_user
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


class Project:
    def __init__(self, name, description, owner, members=[]):
        self.name = name
        self.description = description
        self.members = members.copy()
        self.owner = owner


class User:
    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password


env = Environment(Database())
