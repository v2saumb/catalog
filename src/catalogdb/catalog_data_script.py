from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, User
from random import randint
import datetime
import random


engine = create_engine('sqlite:///src/catalogdb/animalshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# inserting record for admin user
newUser = User(name="Admin", email="admin@itemcatalog.com", accounttype="ADMIN",
               lastlogin=datetime.date.today(), password="123456")
try:
    existinguser = session.query(User).filter(
        User.email == newUser.email).one()
except:
    existinguser = None
if existinguser is None:
    print "Creating User "
    session.add(newUser)
    session.commit()
else:
    print "Skipping admin user create"
