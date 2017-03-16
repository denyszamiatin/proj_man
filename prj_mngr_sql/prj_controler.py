from db_config import session_create
from prj_model import User, Project, Members
from prj_errors import DatabaseUserError, DatabaseProjectError, MemberError
from sqlalchemy import or_, and_




def add_user_rc(user):
    ses = session_create()
    data = ses.query(User).filter(or_(User.login == user.login, User.email == user.email)).first()

    if data:
        raise DatabaseUserError('The User with such login or email is already exist')
    try:
        ses.add(user)
    except Exception as e:
        print(e)
    else:
        ses.commit()


def add_project_rc(prj):
    ses = session_create()
    data = ses.query(Project).filter(Project.name == prj.name).first()

    if data:
        raise DatabaseProjectError('The Project with such name is already exist')
    try:
        ses.add(prj)
    except Exception as e:
        raise e
    else:
        ses.commit()


def delete_user_rc(user_login):
    ses = session_create()
    user = ses.query(User).filter(User.login == user_login).first()

    if not user:
        raise DatabaseUserError('User does not exist')
    else:
        try:
            ses.delete(user)
        except Exception as e:
            raise e
        else:
            ses.commit()


def delete_project_rc(project_name):
    ses = session_create()
    project = ses.query(Project).filter(Project.name == project_name).first()

    if not project:
        raise DatabaseProjectError('Project does not exist')
    else:
        try:
            ses.delete(project)
        except Exception as e:
            raise e
        else:
            ses.commit()


def update_user_rc(user_login, attr, val):
    ses = session_create()
    user = ses.query(User).filter(User.login == user_login).first()

    if not user:
        raise DatabaseUserError('User does not exist')
    else:
        try:
            setattr(user, attr, val)
        except Exception as e:
            raise e
        else:
            ses.commit()


def update_project_rc(project_name, attr, val):
    ses = session_create()
    project = ses.query(Project).filter(Project.name == project_name).first()

    if not project:
        raise DatabaseProjectError('Project does not exist')
    else:
        try:
            setattr(project, attr, val)
        except Exception as e:
            raise e
        else:
            ses.commit()


def add_member(project_name, user_login):
    ses = session_create()
    project = ses.query(Project).filter(Project.name == project_name).first()
    user = ses.query(User).filter(User.login == user_login).first()

    member = ses.query(Members).filter(and_(Members.project_id == project.id, Members.user_id == user.id)).first()


    if not project:
        raise DatabaseProjectError('Project does not exist')
    if not user:
        raise DatabaseUserError('User does not exist')
    if member:
        raise MemberError('Member is already exist')
    else:
        member = Members(project_id=project.id, user_id=user.id)
        try:
            ses.add(member)
        except Exception as e:
            raise e
        else:
            ses.commit()


def delete_member(project_name, user_login):
    ses = session_create()
    project = ses.query(Project).filter(Project.name == project_name).first()
    user = ses.query(User).filter(User.login == user_login).first()
    member = ses.query(Members).filter(and_(Members.project_id == project.id, Members.user_id == user.id)).first()

    if not project:
        raise DatabaseProjectError('Project does not exist')
    if not user:
        raise DatabaseUserError('User does not exist')
    if not member:
        raise MemberError('Member does not exist')
    else:
        try:
            ses.delete(member)
        except Exception as e:
            raise e
        else:
            ses.commit()
