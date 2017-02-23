

from project_model import ModelDatabase
from database_json import Database
from user import User
from project import Project

class Controller:
    def __init__(self ):
        self.model = ModelDatabase(Database())
        self.command_set = {'1': self.create_user, '2': self.create_project, '3': self.update_user,
                            '4': self.update_project, '5': self.delete_user, '6': self.delete_project,
                            '7': self.show_users, '8': self.show_projects, 'exit': None, 'q': None
                            }
        self.connect()

    def input_command(self):
        while True:
            command = input(
                            """
Enter number(create user - 1, create project - 2)
                update user - 3, update project - 4
                delete user - 5, delete project - 6):
                get users - 7, get projects - 8):
>>>""")

            if command == 'exit' or command == 'q':
                break
            elif not command.isdigit():
                print('Input must be integer')
            elif int(command) not in range(1, 9):
                print ('Input must be one of the next number '
                       '- 1, 2, 3, 4, 5, 6, 7, 8')
            else:
                return command

    def connect(self):
        command = self.input_command()
        if not command:
            return
        self.command_set[command]()

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
            self.model.add_user(user.strip())
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("User created"))
        self.connect()

    def create_project(self):
        name = input('Enter Name:>')
        description = input('Enter Description:>')
        author = input('Enter Author:>')
        members = input('Enter Members(separate only by ","):>')

        project = Project(name, description, author, members.split(','))
        try:
            self.model.add_project(project.strip())
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("Project created"))

        self.connect()

    def delete_user(self):
        name = input('Enter User login:>')

        try:
            self.model.delete_user(name.strip())
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("User deleted"))

        self.connect()

    def delete_project(self):
        name = input('Enter Project name:>')

        try:
            self.model.delete_project(name.strip())
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("Project deleted"))

        self.connect()

    def update_user(self):
        name = input('Enter User login:>')
        property = input('Enter name of property and new value '
                         '(separated only by ":")>')

        property, value = property.split(":")


        try:
            self.model.update_user(name.strip(), (property.strip(), value.strip()))
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("User updated"))

        self.connect()

    def update_project(self):
        name = input('Enter Project name:>')
        property = input('Enter name of property and new value(separate only'
                         ' by ":")\n'
                         ' if property == members(separate members by ",")>')

        property, value = property.split(":")
        if property == 'members':
            value = value.split(",")


        try:
            self.model.update_project(name, (property.strip(), value.strip()))
        except Exception as e:
            print('\t{}'.format(e))
        else:
            print('\t{}'.format("project updated"))

        self.connect()


env = Controller()
