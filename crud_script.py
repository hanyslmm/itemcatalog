# import all modules needed for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


# === let program know which database engine we want to communicate===
engine = create_engine('sqlite:///restaurantmenu.db')

# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine

# create session maker object
DBSession = sessionmaker(bind = engine)
session = DBSession()

# adding new entry to my database
# newEntry = ClassName(property = "value", )
# session.add(newEntry)
# session.commit()
"""
myFirstRestaurant = Restaurant(name = "Pizza Father")
session.add(myFirstRestaurant)
session.commit()
# end of adding Restaurant Pizza Station

# adding new MenuItem entry to Pizza Station
cheesepizza = MenuItem(name = "Cheese Pizza", description =
                        "made with all fresh mozzarella",
                        price = "$8.99", course = "Entree",
                        restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()""" # all items created in menu_items.py
# Interact with my database and see what's inside of it

vaggis = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for vaggi in vaggis:
    print(vaggi.id)
    print(vaggi.price)
    print(vaggi.restaurant.name)
    print("\n")
BurgerFuther = session.query(MenuItem).filter_by(id = 8).one()
print(BurgerFuther.price)
print("\n")

BurgerFuther.price = '$2.99'
session.add(BurgerFuther)
session.commit()

vaggis = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for vaggi in vaggis:
    print(vaggi.id)
    print(vaggi.price)
    print(vaggi.restaurant.name)
    print("\n")
