# -*- coding: utf-8 -*-
# 28.11.2021, created by Egor Eremenko


from server_gk import app
from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


# mapping tables
UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)


UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


# models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.
    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Group(db.Model, RestrictionsMixin):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model, AllowancesMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Lesson(db.Model, PermissionsMixin):
    __tablename__ = 'lesson'
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
        group=['read', 'update'],
        other=['read']
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    content = db.Column(db.Text)
    deadline = db.Column(db.String(255))
