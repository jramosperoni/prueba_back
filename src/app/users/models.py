# -*- coding: utf-8 -*-
import logging
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    rut_is_username = True
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(64), nullable=False)
    rutdv = db.Column(db.String(1), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    is_enabled = db.Column(db.Boolean)
    name = db.Column(db.String(64), nullable=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @classmethod
    def create(cls, rut, rutdv, name, is_admin, password, is_enabled, username=None):
        try:
            if cls.rut_is_username:
                username="{0}-{1}".format(rut, rutdv).upper()
            else:
                pass
            user = User(
                username=username,
                password=password,
                is_admin=is_admin,
                name=name,
                rut=rut,
                rutdv=rutdv,
                # wristband_id=wristband_id,
                is_enabled=is_enabled
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            logging.exception(e)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))