# it is a ADT class
from abc import ABC, abstractmethod

import bcrypt


class Person(ABC):
    def __init__(self, username, name, email, password):
        # encapsulation
        self._username = username
        self._name = name
        self._email = email
        self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def set_password(self, password):
        self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.__password.encode('utf-8'))
    
    def get_username(self):
        return self._username
    
    def set_username(self, username):
        self._username = username

    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name

    def get_email(self):
        return self._email
    
    def set_email(self, email):
        self._email = email

    def get_password_hash(self):
        return self.__password

    def set_password_hash(self, password_hash):
        self.__password = password_hash

    @abstractmethod
    def __str__(self):
        pass
    
    @abstractmethod
    def display_role(self):
        pass
    