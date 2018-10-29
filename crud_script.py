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

myFirstRestaurant = Restaurant(name = "Pizza Station")
session.add(myFirstRestaurant)
session.commit()
# end of adding Restaurant Pizza Station

# adding new MenuItem entry to Pizza Station
cheesepizza = MenuItem(name = "Cheese Pizza", description =
                        "made with all fresh mozzarella",
                        price = "$8.99", course = "Entree",
                        restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()

# Interact with my database and see what's inside of it

print(session.query(Restaurant).all())
print(session.query(MenuItem).all())
