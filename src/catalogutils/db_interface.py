import datetime
# import random

from ..catalogdb.database_setup import Shelter, Puppy, User


class catalog_interface:

    def __init__(self, newSession):
        """
        Constructor for the  interface and set the session
            Attributes:
                dbSession:      A database session
        """
        self.dsession = newSession

    def getAllShelters(self):
        """
        ---- Returns a list of all the Shelters from the DB.
        """
        result = self.dsession.query(Shelter).order_by(Shelter.id).all()
        return result

    def getAllPuppies(self):
        """
        ---- Returns a list of all the Shelters from the DB.
        """
        result = self.dsession.query(Puppy).order_by(Puppy.id).all()
        return result

    def addShelter(self, newShelter):
        """
        Adds a new Shelter record in the database"""
        self.dsession.add(newShelter)
        self.dsession.commit()

    def getShelterById(self, shelterId):
        """
        returns a Shelter record by id
        """
        return self.dsession.query(Shelter).filter(
            Shelter.id == shelterId).one()

    def updateShelterDetails(self, shelter):
        """
        updates a shelter record by id
        """
        print "Trying to get restaurant by id"
        tempshelter = self.dsession.query(Shelter).filter(
            Shelter.id == shelter.id).one()
        if tempshelter is not None:
            tempshelter.name = shelter.name
            tempshelter.address = shelter.address
            tempshelter.city = shelter.city
            tempshelter.state = shelter.state
            tempshelter.email = shelter.email
            tempshelter.zipCode = shelter.zipCode
            tempshelter.website = shelter.website
            tempshelter.current_occupancy = shelter.current_occupancy
            tempshelter.maximum_capacity = shelter.maximum_capacity
            self.dsession.add(tempshelter)
            self.dsession.commit()
        else:
            print "Shelter not found "

    def getAllUser(self):
        """
        ---- Returns a list of all the users from the DB.
        """
        result = self.dsession.query(User).order_by(User.id).all()
        print result
        return result

    def updateUserLogin(self, existinguser):
        """
        ---- updates the user login time.
        """
        existinguser.lastlogin = datetime.date.today()
        self.dsession.add(existinguser)
        self.dsession.commit()

    def addUser(self, newUser):
        """
        Adds a new user record in the database"""
        try:
            existinguser = self.dsession.query(User).filter(
                User.email == newUser.email).one()
        except:
            existinguser = None
        if existinguser is None:
            self.dsession.add(newUser)
            self.dsession.commit()
        else:
            self.updateUserLogin(existinguser)

    def getUserById(self, userId):
        """
        returns a user record by id
        """
        return self.dsession.query(User).filter(
            User.id == userId).one()

    def updateUserDetails(self, user):
        """
        updates a user record
        """
        result = False
        try:

            tempuser = self.dsession.query(
                User).filter(User.id == user.id).one()
            tempuser.name = user.name
            tempuser.email = user.email
            tempuser.isActive = user.isActive
            tempuser.pictureurl = user.pictureurl
            tempuser.password = user.password
            self.dsession.add(tempuser)
            self.dsession.commit()
            result = True
        except:
            tempuser = None

        return result

    def adminlogin(self, adminuser):
        """
        return a user bases on the username and password
        """
        try:
            tempuser = self.dsession.query(User).filter(
                User.email == adminuser.email and
                User.password == adminuser.password).one()
        except:
            tempuser = None
        return tempuser
