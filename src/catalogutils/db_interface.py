from sqlalchemy.sql.expression import true, false
import datetime
# import random

from ..catalogdb.database_setup import Categories, User, Items


class catalog_interface:

    def __init__(self, new_session):
        """
        Constructor for the  interface and set the session
            Attributes:
                new_session:      A database session
        """
        self.dsession = new_session

    def get_all_categories(self):
        """
        ---- Returns a list of all the Categories from the DB.
        """
        result = self.dsession.query(Categories).order_by(Categories.id).all()
        return result

    def get_all_parent_categories(self):
        """
        ---- Returns a list of all the sub Categories from the DB.
        """
        result = self.dsession.query(Categories).filter(
            Categories.hasChildren == true(),
            Categories.isActive == true()).order_by(Categories.name).all()
        return result

    def get_all_sub_categories(self):
        """
        ---- Returns a list of all the sub Categories from the DB.
        """
        result = self.dsession.query(Categories).filter(
            Categories.hasChildren == false(),
            Categories.isActive == true()).order_by(Categories.name).all()
        return result

    def get_all_items(self):
        """
        ---- Returns a list of all the Categories from the DB.
        """
        result = self.dsession.query(Items).order_by(Items.id).all()
        return result

    def add_categories(self, new_cat):
        """
        Adds a new Categories record in the database"""
        self.dsession.add(new_cat)
        self.dsession.commit()

    def add_item(self, new_item):
        """
        Adds a new item record in the database"""
        self.dsession.add(new_item)
        self.dsession.commit()

    def get_item_by_id(self, item_id):
        """
        returns a item record by id
        """
        return self.dsession.query(Items).filter(
            Items.id == item_id).one()

    def get_categories_by_id(self, category_id):
        """
        returns a Categories record by id
        """
        return self.dsession.query(Categories).filter(
            Categories.id == category_id).one()

    def update_categories_details(self, category):
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

    def get_all_user(self):
        """
        ---- Returns a list of all the users from the DB.
        """
        result = self.dsession.query(User).order_by(User.id).all()
        print result
        return result

    def update_user_login(self, existinguser):
        """
        ---- updates the user login time.
        """
        existinguser.lastlogin = datetime.date.today()
        self.dsession.add(existinguser)
        self.dsession.commit()

    def add_user(self, newUser):
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
            self.update_user_login(existinguser)

    def get_user_by_id(self, userId):
        """
        returns a user record by id
        """
        return self.dsession.query(User).filter(
            User.id == userId).one()

    def update_user_details(self, user):
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

    def admin_login(self, adminuser):
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
