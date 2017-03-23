# -*- coding: utf-8 -*-
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, name, password, email, id):
        self.id = id
        self.name = name
        self.password = password
        self.email = email

    def get_hashpass(self):
        return self.password

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_id(self):
        return self.id

    def t(self):
        a= """
        def is_active(self):
            return True

        def is_authenticated(self):
            return True
            """

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)