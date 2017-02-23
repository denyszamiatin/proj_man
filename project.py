
from project_manager_error import ProjectError
import re



def name_validation(value):
    if len(value) < 2:
        raise ProjectError("Name is too short - minimum 2 characters")
    if len(value) > 12:
        raise ProjectError("Name is too long - maximum 12 characters")
    if not re.match('^[a-zA-Z0-9]+$', value):
        raise ProjectError("Name is invalid - can contain only letters and numbers")


def autor_validation(value):
    if len(value) < 2:
        raise ProjectError("Autor name is too short - minimum 2 characters")
    if len(value) > 12:
        raise ProjectError("Autor name too long - maximum 12 characters")
    if not re.match('^[a-zA-Z0-9]+$', value):
        raise ProjectError("Autor name is invalid - can contain only letters and numbers")


def description_validation(value):
    if len(value) > 1200:
        raise ProjectError("Description is too long - maximum 1200 characters")



def project_create_validation(fn):
    def wrap(self, name, description, author, members=[]):

        name_validation(name)
        autor_validation(author)
        description_validation(description)

        return fn(self, name, description, author, members)
    return wrap



def project_update_validation(fn):
    def wrap(self, name, value):

        if name == 'name': name_validation(value)
        if name == 'autor': autor_validation(value)
        if name == 'description': description_validation(value)

        return fn(self, name, value)
    return wrap



class Project:
    @project_create_validation
    def __init__(self, name, description, author, members=[]):
        self.name = name
        self.description = description
        self.members = members.copy()
        self.author = author


    def add_member(self, user_name):
        try:
            if isinstance(user_name, str):
                self.members.append(user_name)
            else:
                self.members.extend(user_name)
        except ValueError:
            pass

    def remove_member(self, user_name):
        try:
            self.members.remove(user_name)
        except ValueError:
            pass

    @project_update_validation
    def update_property(self, name, value):
        if not hasattr(self, name):
            raise ProjectError("Project doesn't have such attribute")
        self._set_property(name, value)

    @project_update_validation
    def _set_property(self, name, value):
        setattr(self, name, value)

    @staticmethod
    def get_fields():
        return 'name', 'description', 'members', 'author'


if __name__ == "__main__":
    project = Project('one', 'first', 'igor', ['tom'])
    print([(key, value) for key, value in project.__dict__.items()])
    project.update_property('name', 'two')
    print([(key, value) for key, value in project.__dict__.items()])
    project.update_property('description', 'second')
    print([(key, value) for key, value in project.__dict__.items()])
    project.update_property('author', 'alex')
    print([(key, value) for key, value in project.__dict__.items()])

