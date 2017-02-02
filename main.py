class Environment:
    def __init__(self):
        self.projects_list = {}
        self.users = {}

    def add_project(self, name, description):
        try:
            self.projects_list[name]
        except KeyError:
            self.projects_list[name] = Project(name, description)
        else:
            print('There is an existing project with such name. Use another one')

    def delete_project(self, name):
        try:
            del(self.projects_list[name])
        except KeyError:
            print('There is no project with such name')

    def create_user(self, name, password):
        try:
            self.users[name]
        except KeyError:
            self.users[name] = User(name, password)
        else:
            print('There is a user with such name. Use another one')

    def delete_user(self, name, password):
        try:
            user_data = self.users[name]
        except KeyError:
            print('There is no user with such name')
        else:
            if user_data.password == password:
                del(self.users[name])
            else:
                print('Password is wrong. Try again.')


class Project:
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description
        self.members = {}

    def update_project_data(self, new_name, new_description):
        """
        Incorrect name in dict keys after project data update
        """
        self.name = new_name
        self.description = new_description

    def add_member(self, member_login, users):
        try:
            users[member_login]
        except KeyError:
            print('You can not add the member. There is no user with such name')
        else:
            self.members[member_login] = users[member_login]

    def delete_member(self, member_login):
        try:
            del(self.members[member_login])
        except KeyError:
            print('There is no user with such name')


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def change_credentials(self, old_password, new_login, new_password):
        """
        Incorrect name in dict keys after credentials update
        """
        if old_password == self.password:
            self.login = new_login
            self.password = new_password
        else:
            print('Password is wrong. Try again.')
