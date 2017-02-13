"""
    Project Manager v: 0.6.3
"""
import json


class Database:
    def __init__(self):
        self.data = {}
        self.connect_db()


    def connect_db(self):
        with open('data.json', 'r') as storage:
            self.data = json.load(storage)


    def update_db(self):
        with open('data.json', 'w') as storage:
            json.dump(self.data, storage)


    def update_data(self, data):
        self.data = {'projects': [], "users": []}
        for group in data:
            for item in data[group]:
                self.data[group].append(data[group][item].__dict__)

        self.update_db()


    def get_data(self):
        data = {'projects' : {}, "users" : {}}
        for group in self.data:
            for item in self.data[group]:
                if group == 'users':
                    data[group][item['login']] = User(item['email'], item['login'], item['password'])
                elif group == 'projects':
                    pass
                    data[group][item['name']] = Project(item['name'], item['description'], item['owner'], item['members'])
        return data



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
        self.members = members
        self.owner = owner



class User:
    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password


env = Environment(Database())


