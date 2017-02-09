"""
Project Manager v: 0.4.1
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
        json_project_obj = {atr : getattr(project, atr) for atr in project.__dict__.keys()}

        if not json_project_obj in self.get_projects():
            self.data["projects"].append(json_project_obj)
        else:
            raise KeyError('The project already exist')

        self.update_db()

    def add_user_to_db(self, user):
        json_user_obj = {atr : getattr(user, atr) for atr in user.__dict__.keys()}

        if not json_user_obj in self.get_users():
            self.data["users"].append(json_user_obj)
        else:
            raise KeyError('This name is used')

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



    def update_project(self, name, property):
        for project in self.get_projects():
            if name == project['name'] and property[0] in project.keys():
                project[property[0]] = property[1]

        self.update_db()


    def update_user(self, name, property):
        for user in self.get_users():
            if name == user['login'] and property[0] in user.keys():
                user[property[0]] = property[1]

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

    def get_users(self):
        self.users = {}
        for user in self.db.get_users():
            self.users[user['login']] = User(user['email'], user['login'], user['password'])

        print (self.users)
        return self.users


    def get_projects(self):
        self.projects = {}
        for project in self.db.get_projects():
            self.projects[project['name']] = Project(project['name'], project['description'], project['owner'],
                                                     ['project.members'])

        print(self.projects)
        return self.projects


    def add_project(self, project):
        self.db.add_project_to_db(project)


    def delete_project(self, name):
        self.db.del_project_from_db(name)


    def add_user(self, user):
        self.db.add_user_to_db(user)


    def delete_user(self, name):
        self.db.del_user_from_db(name)


    def update_project(self, name, property):
        self.db.update_project( name, property)


    def update_user(self, name, property):
        self.db.update_user(name, property)



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



if __name__ == "__main__":
    env = Environment(Database())
    env.get_projects()
    env.get_users()

