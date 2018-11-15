# used to manipulate diff parts of py run-time env.
import sys
import os
# import all modules needed for configuration
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# base instance inherit all features of SQLAlchemy
Base = declarative_base()

# add class definition code
class User(Base):
    __tablename__ = 'user'

# user table mapper
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

# add class definition code
class Restaurant(Base):
    __tablename__ = 'restaurant'

# restaurant table mapper
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_if
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'

# menu_table table mapper
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    course = Column(String(250))
    description = Column(String(250))
    price = Column (String(8))
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
