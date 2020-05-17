import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

epoch = datetime.datetime.utcfromtimestamp(0)


def camel_case(s):
    caps = False
    ret = []
    for ch in s:
        if ch == '_':
            caps = True
        else:
            ret.append(ch.capitalize() if caps else ch)
            caps = False
    return ''.join(ret)


class DatingEvent(db.Model):
    __tablename__ = 'dating_events'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    name = db.Column(db.String, nullable=False)

    def as_dict(self):
        d = {camel_case(a): getattr(self, a) for a in ['id', 'user_id', 'approve_user_id']}
        d['created'] = (self.created - epoch).total_seconds() * 1000
        return d


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    email = db.Column(db.String(256), nullable=False, unique=True, index=True)
    name = db.Column(db.String(512))

    def as_dict(self):
        return {camel_case(a): getattr(self, a) for a in ['id', 'created', 'email', 'customer_id', 'enabled', 'super']}


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    role = db.Column(db.Enum('USER', 'DEVELOPER', 'ADMINISTRATOR'), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = relationship("User", backref=backref('roles', lazy='dynamic'))


def find_dating_events():
    query = db.session.query(DatingEvent)
    return query.all()


