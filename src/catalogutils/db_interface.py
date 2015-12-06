from sqlalchemy.sql.expression import false, true
import datetime
# import random

from ..catalogdb.database_setup import Categories, User


class catalog_interface:

    def __init__(self, newSession):
        """
        Constructor for the  interface and set the session
            Attributes:
                dbSession:      A database session
        """
        self.dsession = newSession

    def getAllCategories(self):
        """
        ---- Returns a list of all the Categoriess from the DB.
        """
        result = self.dsession.query(Categories).order_by(Categories.id).all()
        return result

    def getAllSubCategories(self):
        """
        ---- Returns a list of all the sub Categories from the DB.
        """
        result = self.dsession.query(Categories).filter(
            Categories.hasChildren == true(),
            Categories.isActive == true()).order_by(Categories.name).all()
        return result

    def getAllPuppies(self):
        """
        ---- Returns a list of all the Categoriess from the DB.
        """
        result = self.dsession.query(Puppy).order_by(Puppy.id).all()
        return result

    def addCategories(self, newCategories):
        """
        Adds a new Categories record in the database"""
        self.dsession.add(newCategories)
        self.dsession.commit()

    def getCategoriesById(self, categoryId):
        """
        returns a Categories record by id
        """
        return self.dsession.query(Categories).filter(
            Categories.id == categoryId).one()

    def updateCategoriesDetails(self, category):
        """
        updates a category record by id
        """
        result = False
        try:
            tempcategory = self.dsession.query(Categories).filter(
                Categories.id == category.id).one()
            tempcategory.name = category.name
            tempcategory.parent = category.parent
            tempcategory.isActive = category.isActive
            tempcategory.hasChildren = category.hasChildren
            self.dsession.add(tempcategory)
            self.dsession.commit()
            result = True
        except:
            result = False
        return result

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
