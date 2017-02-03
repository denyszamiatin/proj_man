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
        if observer not in self.observers: #
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

env = Environment()
with open("data_users", "r") as f:
    for i in f:
        env.add_user(User(i.strip(), f.readline().strip(), f.readline().strip()))

with open("data_projects", "r") as f:
    for i in f:
        env.add_project(Project(i.strip(), f.readline().strip(), f.readline().strip(), f.readline().strip().split(',')))

for user in env.users:
    print(env.users[user].email, env.users[user].login, env.users[user].password)
for project in env.projects:
    print(env.projects[project].name, env.projects[project].description, env.projects[project].owner, env.projects[project].members)

with open("data_projects", "w") as f:
    for project in env.projects:
        f.write(project + "\n")
        f.write(env.projects[project].description + "\n")
        f.write(env.projects[project].owner + "\n")
        for member in env.projects[project].members:
            if member == env.projects[project].members[-1]:
                f.write(member)
            else:
                f.write(member + ",")
        f.write("\n")

with open("data_users", "w") as f:
    for user in env.users:
        f.write(env.users[user].email + "\n")
        f.write(user + "\n")
        f.write(env.users[user].password + "\n")
