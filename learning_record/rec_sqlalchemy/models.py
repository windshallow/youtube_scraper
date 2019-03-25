# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from learning_record.rec_sqlalchemy.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __init__(self, name, fullname, password):
            self.name = name
            self.fullname = fullname
            self.password = password

    def __str__(self):
        return self.name


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer)

    def __init__(self, email_address, user_id):
            self.email_address = email_address
            self.user_id = user_id

    def __str__(self):
        return self.email_address

