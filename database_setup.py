# used to manipulate diff parts of py run-time env.
import sys
import os
# import all modules needed for configuration
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
# base instance inherit all features of SQLAlchemy
Base = declarative_base()


# add usertype class definition code for usertype table
class UserType(Base):
    __tablename__ = 'usertype'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


# add class definition code and mapper for user table
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_type = Column(Integer, ForeignKey('usertype.id'))
    usertype = relationship(UserType)

    @property
    def serialize(self):
        """return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
        }


# add class definition code and mapper for restaurant table
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_id
        }


# add class definition code and mapper for menu item table
class MenuItem(Base):
    __tablename__ = 'menu_item'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    course = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(String(8), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'course': self.course
        }


# === to connect to an existing db or create a new one ===
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.create_all(engine)
print("connected to restaurantmenu database")

# fill usertype table with Admin and Normal
DBSession = sessionmaker(bind=engine)
session = DBSession()
admin = UserType(name='Admin')
session.add(admin)
normal = UserType(name='Normal')
session.add(normal)
session.commit()
session.query(UserType).all()
