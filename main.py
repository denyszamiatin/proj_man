"""

"""


class Environment:
    """
    Main configuration
    """
    def __init__(self):
        self.projects = {}
        self.users = {}

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


class Project:
    def __init__(self, user, name, description):
        self.name = name
        self.description = description
        self.members = {}
        self.owner = user
        self.observers = []

    def update_description(self, description):
        self.description = description

    def update_name(self, name):
        old_name, self.name = self.name, name
        for observer in self.observers:
            print('Notify:', self.observers)
            observer.notify(old_name, self)

    def register_observer(self, observer):
        if observer not in self.observers: #
            self.observers.append(observer)

    def add_member(self, user):
        self.members[user.name] = user

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

env = Environment()
with open("data_users", "r") as f:
    for i in f:
        env.add_user(User(i.strip(), f.readline().strip(), f.readline().strip()))

print(env.users)

with open("data_users", "w") as f:
    for user in env.users:
        f.write(env.users[user].email + "\n")
        f.write(user + "\n")
        f.write(env.users[user].password + "\n")