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
        return self.dsession.query(Items).order_by(Items.id).all()

    def get_all_items_user(self, user_id):
        """
        returns all the Items for a user
        """
        return self.dsession.query(Items).filter(
            Items.user_id == user_id).order_by(Items.id).all()

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

    def get_latest_items(self, time_delta, item_limit):
        """
        returns latest items if not found it will return the
        latest from all the records
        """
        today = datetime.date.today()
        cut_off_date = today - datetime.timedelta(days=time_delta)
        try:
            results = self.dsession.query(Items).filter(
                Items.created > cut_off_date).limit(item_limit).all()
        except:
            results = self.dsession.query(Items).order_by(
                Items.created.desc()).limit(item_limit).all()
        return results

    def get_categories_by_id(self, category_id):
        """
        returns a Categories record by id
        """
        return self.dsession.query(Categories).filter(
            Categories.id == category_id).one()

    def update_item_details(self, item):
        """
        updates a item record by id
        """
        result = False
        try:
            tempitem = self.dsession.query(Items).filter(
                Items.id == item.id).one()
            tempitem.name = item.name
            tempitem.description = item.description
            tempitem.pricerange = item.pricerange
            tempitem.pictureurl = item.pictureurl
            tempitem.isActive = item.isActive
            tempitem.category_id = item.category_id
            tempitem.user_id = item.user_id
            self.dsession.add(tempitem)
            self.dsession.commit()
            result = True
        except:
            result = False
        return result

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

    def add_user(self, new_user):
        """
        Adds a new user record in the database"""
        try:
            existinguser = self.dsession.query(User).filter(
                User.email == new_user.email).one()

        except:
            existinguser = None
        if existinguser is None:
            self.dsession.add(new_user)
            self.dsession.commit()
            self.dsession.refresh(new_user)
            print new_user.id
            userid = new_user.id
        else:
            self.update_user_login(existinguser)
            userid = existinguser.id
        return userid

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
