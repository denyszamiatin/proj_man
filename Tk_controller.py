from project_model import ModelDatabase
from database_json import Database
from user import User
from project import Project
from tkinter import *
import hashlib

class LoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        self.model = ModelDatabase(Database())
        self.log_pwd_msg = Label(text="", font='Arial 12', fg='red')

        # Creating the username & password entry boxes
        self.login_text = Label(text="Username*", font='Arial 12')
        self.login_input = Entry(font='Arial 12')
        self.login_input.bind("<Key>", self.hide_login_password_message)

        self.password_text = Label(text="Password*", font='Arial 12')
        self.password_input = Entry(show="*", font='Arial 12')
        self.password_input.bind("<Key>", self.hide_login_password_message)

        # attempt to login button
        self.attempt_login = Button(text="Enter", font='Arial 12', command=lambda: self.login_password_message())
        self.register = Button(text=" New register", font='Arial 12',  command=lambda: controller.create_reg_page())

        self.login_text.grid(row=1, columnspan=2, pady=10)
        self.login_input.grid(row=2, columnspan=2)
        self.password_text.grid(row=3, columnspan=2)
        self.password_input.grid(row=4, columnspan=2, pady=10)
        self.attempt_login.grid(row=5, column=0, sticky="e", pady=10, padx=15)
        self.register.grid(row=5, column=1, sticky="w", pady=10, padx=15)

    def login_password_message(self):
        login = self.login_input.get().strip(' ')
        password = self.password_input.get().strip(' ')

        users = self.model.get_users()

        if not login or not password:
            self.show_login_password_message('Login and password is required', 'red')

        for user in users:
            if login == user.login:
                if hashlib.md5(password.encode('utf8')).hexdigest() == user.password:
                    self.show_login_password_message('Hi {}'.format(login), 'green')
                    self.controller.create_projects_page()
                else:
                    self.show_login_password_message('Login or password is invalid', 'red')

        if not login in [user.login for user in users]:
            self.show_login_password_message('No User with such login', 'red')

    def hide_login_password_message(self, event):
        self.log_pwd_msg.grid_forget()

    def show_login_password_message(self, message, color):
        self.log_pwd_msg.config(text=message, fg=color)
        self.log_pwd_msg.grid(row=0, column=0, columnspan=2, pady=10)


class RegisterPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.model = ModelDatabase(Database())

        self.model = ModelDatabase(Database())
        self.log_pwd_msg = Label(text="", font='Arial 12', fg='red')

        self.log_text = Label(text="Username*", font='Arial 12')
        self.log_input = Entry(font='Arial 12')

        self.email_text = Label(text="Email*", font='Arial 12')
        self.email_input = Entry(font='Arial 12')

        self.pwd_text = Label(text="Password*", font='Arial 12')
        self.pwd_input = Entry(show="*", font='Arial 12')

        self.cfm_pwd_text = Label(text="Repeat Password*", font='Arial 12')
        self.cfm_pwd_input = Entry(show="*", font='Arial 12')

        self.attempt_login = Button(text="Login", font='Arial 12', command=lambda: self.controller.create_log_page())
        self.register = Button(text="Register", font='Arial 12', command=lambda: self.register_validation())

        # dispose element on widget
        self.log_text.grid(row=1, columnspan=2, pady=10)
        self.log_input.grid(row=2, columnspan=2)

        self.email_text.grid(row=3, columnspan=2, pady=10)
        self.email_input.grid(row=4, columnspan=2)

        self.pwd_text.grid(row=5, columnspan=2)
        self.pwd_input.grid(row=6, columnspan=2, pady=10)

        self.cfm_pwd_text.grid(row=7, columnspan=2)
        self.cfm_pwd_input.grid(row=8, columnspan=2, pady=10)

        self.attempt_login.grid(row=9, column=0, sticky="e", pady=10, padx=15)
        self.register.grid(row=9, column=1, sticky="w", pady=10, padx=15)

    def register_validation(self):

        login = self.log_input.get().strip(' ')
        email = self.email_input.get().strip(' ')
        password = self.pwd_input.get().strip(' ')
        cfm_password = self.cfm_pwd_input.get().strip(' ')

        if not login or not email or not password:
            self.show_reg_message("Login, email, password is required", 'red')

        elif password != cfm_password:
            self.show_reg_message("Passwords didn't match", 'red')
        else:
            try:
                user = User(email, login, password, newuser=True)
            except Exception as e:
                self.show_reg_message(e, 'red')
            else:
                try:
                    self.model.add_user(user)
                except Exception as e:
                    self.show_reg_message(e, 'red')
                else:
                    self.show_reg_message("New user created", 'green')
                    self.controller.create_projects_page()

    def show_reg_message(self, message, color):
        self.log_pwd_msg.config(text=message, fg=color)
        self.log_pwd_msg.grid(row=0, column=0, columnspan=2, pady=10)


class ProjectsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.model = ModelDatabase(Database())

        self.projects_list = Label(text="Projects", font='Arial 12', borderwidth=0, highlightthickness=0)
        self.lb_projects = Listbox(font='Arial 12')

        for numb, project in enumerate(self.model.get_projects()):
            self.lb_projects.insert(numb, project.name)

        self.update_project = Button(text="Update project", font='Arial 12')
        self.create_project = Button(text="New project", font='Arial 12',
                                     command=lambda: controller.create_add_project_page())

        self.update_project.grid(row=9, column=0, sticky="e", pady=10, padx=15)
        self.create_project.grid(row=9, column=1, sticky="w", pady=10, padx=15)
        self.projects_list.grid(row=1, columnspan=2, pady=5)
        self.lb_projects.grid(row=2, columnspan=2, pady=10)

    def delegate_project(self):
        lb_projects = self.lb_projects.curselection()
        project = [self.model.get_projects()[numb] for numb in range(len(self.model.get_projects())) if numb in lb_projects]
        return project[0]


class AddProjectsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        self.model = ModelDatabase(Database())

        self.model = ModelDatabase(Database())
        self.log_pwd_msg = Label(text="", font='Arial 12', fg='red')

        self.name_text = Label(text="Project name*", font='Arial 12')
        self.name_input = Entry(font='Arial 12')

        self.author_text = Label(text="Author*", font='Arial 12')
        self.author_input = Entry(font='Arial 12')

        self.desc_text = Label(text="Description", font='Arial 12')
        self.desc_input = Text(font='Arial 12', width=20, height=6)

        self.users_list = Label(text="Members", font='Arial 12', borderwidth=0, highlightthickness=0)
        self.lb_user = Listbox(font='Arial 12', selectmode = "multiple")

        for numb, user in enumerate(self.model.get_users()):
            self.lb_user.insert(numb, user.login)

        self.add_btn = Button(text="Add", font='Arial 12',  command=lambda: self.add_project())
        self.cancel_btn = Button(text="Cancel", font='Arial 12', command=lambda: controller.create_projects_page())

        # dispose element on widget\

        self.name_text.grid(row=1, columnspan=2, pady=10)
        self.name_input.grid(row=2, columnspan=2)

        self.author_text.grid(row=3,  columnspan=2)
        self.author_input.grid(row=4,  columnspan=2, pady=10, padx=10)

        self.desc_text.grid(row=7, columnspan=2, pady=6)
        self.desc_input.grid(row=8, columnspan=2, padx=10)

        self.users_list.grid(row=1, column=2, columnspan=2)
        self.lb_user.grid(row=1, rowspan=8, column=2, columnspan=2, padx=10)

        self.add_btn.grid(row=9, column=1, sticky="w",  pady=10)
        self.cancel_btn.grid(row=9,  column=1, sticky="e", padx=10)

    def add_project(self):
        projects = self.model.get_projects()

        name = self.name_input.get().strip(' ')
        author = self.author_input.get().strip(' ')
        desc = self.desc_input.get("1.0", END)
        lb_user = self.lb_user.curselection()

        members = [self.model.get_users()[numb].login for numb in range(len(self.model.get_users())) if numb in lb_user]

        if not name:
            self.show_project_message('Projects name is required', 'red')
        elif not author:
            self.show_project_message('Projects author is required', 'red')
        else:
            try:
                project = Project(name, desc, author, members)
            except Exception as e:
                self.show_project_message(e, 'red')
            else:
                try:
                    self.model.add_project(project)
                except Exception as e:
                    self.show_project_message(e, 'red')
                else:
                    self.controller.create_projects_page()

    def show_project_message(self, message, color):
        self.log_pwd_msg.config(text=message, fg=color)
        self.log_pwd_msg.grid(row=0, column=1, columnspan=2, pady=10)


class UpdateProjectsPage(Frame):
    def __init__(self, parent, controller, prj):
        Frame.__init__(self, parent)

        self.prj = prj
        self.controller = controller
        self.model = ModelDatabase(Database())

        self.model = ModelDatabase(Database())
        self.log_pwd_msg = Label(text="", font='Arial 12', fg='red')

        self.name_text = Label(text="Project name*", font='Arial 12')
        self.name_input = Entry(font='Arial 12')
        self.name_input.insert(END, self.prj.name)

        self.author_text = Label(text="Author*", font='Arial 12')
        self.author_input = Entry(font='Arial 12')
        self.author_input.insert(END, self.prj.author)

        self.desc_text = Label(text="Description", font='Arial 12')
        self.desc_input = Text(font='Arial 12', width=20, height=6)
        self.desc_input.insert(END, self.prj.description)

        self.users_list = Label(text="Members", font='Arial 12', borderwidth=0, highlightthickness=0)
        self.lb_user = Listbox(font='Arial 12', selectmode="multiple")

        for numb, user in enumerate(self.model.get_users()):
            self.lb_user.insert(numb, user.login)

        self.add_btn = Button(text="Save", font='Arial 12',  command=lambda: self.save_project())
        self.cancel_btn = Button(text="Cancel", font='Arial 12', command=lambda: controller.create_projects_page())

        # dispose element on widget\

        self.name_text.grid(row=1, columnspan=2, pady=10)
        self.name_input.grid(row=2, columnspan=2)

        self.author_text.grid(row=3,  columnspan=2)
        self.author_input.grid(row=4,  columnspan=2, pady=10, padx=10)

        self.desc_text.grid(row=7, columnspan=2, pady=6)
        self.desc_input.grid(row=8, columnspan=2, padx=10)

        self.users_list.grid(row=1, column=2, columnspan=2)
        self.lb_user.grid(row=1, rowspan=8, column=2, columnspan=2, padx=10)

        self.add_btn.grid(row=9, column=1, sticky="w",  pady=10)
        self.cancel_btn.grid(row=9,  column=1, sticky="e", padx=10)

    def save_project(self):

        name = self.name_input.get().strip(' ')
        author = self.author_input.get().strip(' ')
        description = self.desc_input.get("1.0", END)
        lb_user = self.lb_user.curselection()

        members = [self.model.get_users()[numb].login for numb in range(len(self.model.get_users())) if numb in lb_user]

        properties = {'name': name, 'author': author, 'description': description, 'members': members}

        if not name:
            self.show_project_message('Projects name is required', 'red')
        elif not author:
            self.show_project_message('Projects author is required', 'red')
        else:
            for prp in properties.keys():
                try:
                    self.model.update_project(name, (prp, properties[prp]))
                except Exception as e:
                    self.show_project_message(e, 'red')
                else:
                    self.controller.create_projects_page()

    def show_project_message(self, message, color):
        self.log_pwd_msg.config(text=message, fg=color)
        self.log_pwd_msg.grid(row=0, column=1, columnspan=2, pady=10)


class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.grid_columnconfigure(1, weight=1)
        self.container = Frame(self)
        self.create_log_page()

    def create_log_page(self):
        self.remove_frame()
        self.log_page = LoginPage(parent=self.container, controller=self)
        self.log_page.grid(row=0, column=0, sticky="nsew")

    def create_reg_page(self):
        self.remove_frame()
        self.reg_page = RegisterPage(parent=self.container, controller=self)
        self.reg_page.grid(row=0, column=0, sticky="nsew")

    def create_projects_page(self):
        self.remove_frame()
        self.prj_page = ProjectsPage(parent=self.container, controller=self)
        self.prj_page.grid(row=0, column=0, sticky="nsew")

    def create_add_project_page(self):
        self.remove_frame()
        self.add_prj_page = AddProjectsPage(parent=self.container, controller=self)
        self.add_prj_page.grid(row=0, column=0, sticky="nsew")

    def create_update_project_page(self, project):
        self.remove_frame()
        self.up_prj_page = UpdateProjectsPage(parent=self.container, controller=self, prj=project)
        self.up_prj_page.grid(row=0, column=0, sticky="nsew")

    def remove_frame(self,):
        a = self.winfo_children()
        for widget in range(1, len(self.winfo_children())):
            a[widget].destroy()


if __name__ == "__main__":
    root = App()
    root.title("Project Manager")
    root.minsize('300', '100')
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()