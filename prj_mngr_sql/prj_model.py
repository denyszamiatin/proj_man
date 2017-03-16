# -*- coding: utf-8 -*

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    projects = relationship("Project", cascade="save-update, merge", backref="users")
    member = relationship("Members", cascade="all,delete", backref="users")


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    dsc = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    members = relationship("Members", cascade="all,delete", backref="projects")


class Members(Base):
    __tablename__ = "members"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


