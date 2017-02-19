"""
Project Manager v: 0.6.4
"""
import json


class Project:
    def __init__(self, name, description, autor, members=[]):
        self.name = name
        self.description = description
        self.members = members.copy()
        self.autor = autor

    @staticmethod
    def get_fields():
        return 'name', 'description', 'members', 'autor'


class User:
    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password

    @staticmethod
    def get_fields():
        return 'login', 'email', 'password'

class ProjectError(Exception):pass
class UserError(Exception):pass

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


class ModelDatabaseValidation:

    @classmethod
    def add_project_validation(cls, fn):
        def wrapped(self, project):
            if type(project).__name__ != 'Project':
                raise TypeError('It is not a valid project instance')

            if project.name in self.data['projects']:
                raise ProjectError('The Projects name is already used')
            elif project.members:
                for member in project.members:
                    if member not in self.data['users'].keys():
                        raise ProjectError('Members must be users')
            elif project.owner not in self.data['users'].keys():
                raise ProjectError('Autor must be user')

            return fn(self, project)

        return wrapped

    @classmethod
    def delete_project_validation(cls, fn):
        def wrapped(self, project_name):

            if project_name in self.data['projects']:
                return fn(self, project_name)
            else:
                raise ProjectError("Project with this name doesn't exist")

        return wrapped

    @classmethod
    def add_user_validation(cls, fn):
        def wrapped(self, user):

            if type(user).__name__ != 'User':
                raise TypeError('It is not a valid user instance')
            if user.login in self.data['users'].keys():
                raise UserError('The User name or Email is already used')
            if user.email in [value.email for key, value in self.data['users'].items()]:
                raise UserError('The User name or Email is already used')

            return fn(self, user)

        return wrapped

    @classmethod
    def delete_user_validation(cls, fn):
        def wrapped(self, user_name):

            if user_name not in self.data['users']:
                raise UserError("User doesn't exist")

            return fn(self, user_name)
        return wrapped

    @classmethod
    def update_project_validation(cls, fn):
        def wrapped(self, project_name, property):
            if project_name in self.data["projects"]:

                if property[0] == 'name' and property[1] not in self.data['users']:
                    raise ProjectError('Autor must be user')

                if property[0] == 'members':
                    for member in property[1]:
                        if member not in self.data['users'].keys():
                            raise KeyError('Members must be users')

                return fn(self, project_name, property)
            else:
                raise ProjectError("Project with this name doesn't exist")

        return wrapped

    @classmethod
    def update_user_validation(cls, fn):
        def wrapped(self, user_name, property):
            if user_name in self.data["users"]:
                if property[0] not in self.data["users"][user_name].__dict__:
                    print(property[0])
                    print(self.data["users"][user_name].__dict__)
                    raise UserError('There are not such property')
                return fn(self, user_name, property)
            else:
                raise UserError('There are no user with such name')



        return wrapped


class ModelDatabase:
    """
    Main configuration
    """
    def __init__(self, db):
        self.db = db
        self.data = db.get_data()

    def get_users(self):
        return self.data['users']

    def get_projects(self):
        return self.data['projects']

    @ModelDatabaseValidation.add_project_validation
    def add_project(self, project):
        self.data['projects'][project.name] = project
        self.db.update_data(self.data)

    @ModelDatabaseValidation.add_user_validation
    def add_user(self, user):
        self.data['users'][user.login] = user
        self.db.update_data(self.data)

    @ModelDatabaseValidation.delete_project_validation
    def delete_project(self, project_name):
        del self.data['projects'][project_name]
        self.db.update_data(self.data)

    @ModelDatabaseValidation.delete_user_validation
    def delete_user(self, user_name):

        for projects in self.data['projects']:
            if user_name in self.data['projects'][projects].members:
                self.data['projects'][projects].members.remove(user_name)

        del self.data['users'][user_name]
        self.db.update_data(self.data)

    @ModelDatabaseValidation.update_project_validation
    def update_project(self, project_name, property):

        setattr(self.data["projects"][project_name], property[0], property[1])
        self.db.update_data(self.data)

    @ModelDatabaseValidation.update_user_validation
    def update_user(self, user_name, property):
        if property[0] == "login":
            for project in self.data['projects']:
                if user_name in self.data['projects'][project].members:
                    self.data['projects'][project].members.remove(user_name)
                    self.data['projects'][project].members.append(property[1])

                if  user_name == self.data['projects'][project].autor:
                    self.data['projects'][project].autor = property[1]

        setattr(self.data["users"][user_name], property[0], property[1])
        self.db.update_data(self.data)




class Controller:
    def __init__(self ):
        self.model =ModelDatabase(Database())
        self.connect()



    def connect(self):
        while True:

            command = input('\nEnter number(create user - 1, create project - 2)'
                            '\n\t\t\t update user - 3, update project - 4'
                            '\n\t\t\t delete user - 5, delete project - 6):'
                            '\n\t\t\t get users - 7, get projects - 8):\n>>>')

            if not command.isdigit():
                print ('Input must be integer')
            elif  int(command) not in range(1, 9):
                print ('Input must be one of the next number - 1, 2, 3, 4, 5, 6, 7, 8')
            else:
                break

        if int(command) == 1:
            self.create_user()
        elif int(command) == 2:
            self.create_project()
        elif int(command) == 3:
            self.update_user()
        elif int(command) == 4:
            self.update_project()
        elif int(command) == 5:
            self.delete_user()
        elif int(command) == 6:
            self.delete_project()
        elif int(command) == 7:
            self.show_users()
        elif int(command) == 8:
            self.show_projects()

    def show_users(self):
        print(self.model.get_users())
        self.connect()

    def show_projects(self):
        print(self.model.get_projects())
        self.connect()

    def create_user(self):
        email = input('Enter Email:>')
        login = input('Enter Login:>')
        password = input('Enter Password:>')

        user = User(email, login, password)
        try:
            self.model.add_user(user)
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("User created"))
        self.connect()

    def create_project(self):
        name = input('Enter Name:>')
        description = input('Enter Description:>')
        autor = input('Enter Autor:>')
        members = input('Enter Members(separate only by ","):>')

        project = Project(name, description, autor, members.split(','))
        try:
            self.model.add_project(project)
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("Project created"))

        self.connect()

    def delete_user(self):
        name = input('Enter User login:>')

        try:
            self.model.delete_user(name)
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("User deleted"))

        self.connect()

    def delete_project(self):
        name = input('Enter Project name:>')

        try:
            self.model.delete_project(name)
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("Project deleted"))

        self.connect()

    def update_user(self):
        name = input('Enter User login:>')
        property = input('Enter name of property and new value(separated only by ":")>')

        property, value = property.split(":")


        try:
            self.model.update_user(name, (property, value))
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("User updated"))

        self.connect()

    def update_project(self):
        name = input('Enter Project name:>')
        property = input('Enter name of property and new value(separate only by ":")\n'
                         ' if property == members(separate members by ",")>')

        property, value = property.split(":")
        if property == 'members':
            value = value.split(",")


        try:
            self.model.update_project(name, (property, value))
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("project updated"))

        self.connect()


env = Controller()




