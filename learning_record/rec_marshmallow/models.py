# -*- coding: utf-8 -*-
import datetime as dt


class User(object):
    """用户"""
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()
        self.friends = []
        self.employer = None

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)
