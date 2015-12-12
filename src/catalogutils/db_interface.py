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

    def get_all_items(self, only_active=False):
        """
        Returns a list of all the Categories from the DB.
        Arguments:
            only_active: default is False searches for
            all items.If True searches only active items
        """
        if only_active:
            return self.dsession.query(Items).filter(
                Items.isActive == true()).order_by(Items.name).all()
        else:
            return self.dsession.query(Items).order_by(Items.id).all()

    def get_all_items_user(self, user_id):
        """
        returns all the Items for a user
        Argument:
            user_id: user for whih the items have to be searched for
        """
        return self.dsession.query(Items).filter(
            Items.user_id == user_id).order_by(Items.id).all()

    def add_categories(self, new_cat):
        """
        Adds a new Categories record in the database
        Arguments:
            new_cat: the new category object.
        """
        self.dsession.add(new_cat)
        self.dsession.commit()

    def add_item(self, new_item):
        """
        Adds a new item record in the database
        Arguments:
            new_item: new item object.
        """
        self.dsession.add(new_item)
        self.dsession.commit()

    def get_item_by_id(self, item_id):
        """
        returns a item record by id
        Argument:
            item_id: the id of the item to be searched
        """
        return self.dsession.query(Items).filter(
            Items.id == item_id).one()

    def get_items_by_category(self, db_category_name):
        """
        returns a items record by category
        Arguments:
            db_category_name: name of the category to search the record
        """
        try:
            temp_category = self.dsession.query(Categories).filter(
                Categories.name == db_category_name,
                Categories.isActive == true()).one()

            results = self.dsession.query(Items).filter(
                Items.category_id == temp_category.id,
                Items.isActive == true()).all()
        except:
            results = None
        return results

    def get_category_by_name(self, db_category_name):
        """
        returns a category record by category name
        Arguments:
            db_category_name: name of the category to search the record
        """

        try:
            temp_category = self.dsession.query(Categories).filter(
                Categories.name == db_category_name).one()
        except:
            temp_category = None
        return temp_category

    def get_category_item_by_name(self, db_category_name, db_item_name):
        """
        returns a items record by category and item name
        Arguments:
            db_category_name: name of the category to search the record
            db_item_name: The name of the item being searched
        """

        try:
            temp_category = self.dsession.query(Categories).filter(
                Categories.name == db_category_name,
                Categories.isActive == true()).one()

            results = self.dsession.query(Items).filter(
                Items.category_id == temp_category.id,
                Items.isActive == true(),
                Items.name == db_item_name).all()
        except:
            results = None
        return results

    def get_latest_items(self, time_delta, item_limit):
        """
        returns latest items if not found it will return the
        latest from all the records. This returns only active Items
        Arguments:
            time_delta: number of day, how old items are considered as latest
            item_limit: the number of records to be returned
        """
        today = datetime.date.today()
        cut_off_date = today - datetime.timedelta(days=time_delta)
        try:
            results = self.dsession.query(Items).filter(
                Items.created > cut_off_date,
                Items.isActive == true()).order_by(
                Items.created.desc(), Items.name).limit(item_limit).all()
        except:
            # if no records are found matching the above criteria
            # return the latest records
            results = self.dsession.query(Items).filter(
                Items.isActive == true()).order_by(
                Items.created.desc(), Items.name).limit(item_limit).all()
        return results

    def get_categories_by_id(self, category_id):
        """
        returns a Categories record by id
        Argument:
            category_id : id of the category that is being searched
        """
        return self.dsession.query(Categories).filter(
            Categories.id == category_id).one()

    def update_item_details(self, item):
        """
        updates a item record by id
        Argument:
            item: The item object that is being updated.
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

            if item.user_id is not None:
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
        Argument:
            category: the category object that is being updated
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
        return result

    def update_user_login(self, existinguser):
        """
        ---- updates the user login time.
        Argument:
            existinguser: the user that is being updated
        """
        existinguser.lastlogin = datetime.date.today()
        self.dsession.add(existinguser)
        self.dsession.commit()

    def add_user(self, new_user):
        """
        Adds a new user record in the database
        Argument:
            new_user: the new_user object that is being inserted
        """
        try:
            existinguser = self.dsession.query(User).filter(
                User.email == new_user.email).one()

        except:
            existinguser = None
        # check if the user exists
        if existinguser is None:
            self.dsession.add(new_user)
            self.dsession.commit()
            self.dsession.refresh(new_user)

            userid = new_user.id
        else:
            self.update_user_login(existinguser)
            userid = existinguser.id
        # return the user id of the new ? existing user
        return userid

    def get_user_by_id(self, user_id):
        """
        returns a user record by id
        Arguments:
            user_id: the id of the user
        """
        return self.dsession.query(User).filter(
            User.id == user_id).one()

    def update_user_details(self, user):
        """
        updates a user record
        Argument:
            user: the updated user object
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
        Argument:
            adminuser: the object containing the username and
            password of the admin user
        """
        try:

            tempuser = self.dsession.query(User).filter(
                User.email == adminuser.email,
                User.password == adminuser.password).one()
        except:
            tempuser = None
        return tempuser

    def get_catalog_all(self):
        """
        return a user bases on the username and password
        """
        sql = "select i.id as id, i.name as name , i.pricerange as pricerange,"
        sql += " i.isActive, c.name as category, d.name as parent from"
        sql += " categories c, items i, categories d"
        sql += " where c.id=i.category_id and d.id=c.parent "
        sql += " order by parent , category, name"
        try:
            tempitems = self.dsession.execute(sql)
        except:
            tempitems = None
        return tempitems

    def delete_item(self, item_id):
        """  Deletes an item by id
        Argument:
            item_id: id of the item being deleted
        """
        tempItem = self.dsession.query(Items).filter(
            Items.id == item_id).one()
        if tempItem is not None:
            self.dsession.delete(tempItem)
            self.dsession.commit()

    def delete_user(self, user_id):
        """  Deletes an user by id
        Argument:
            user_id: id of the user being deleted
        """
        tempItem = self.dsession.query(User).filter(
            User.id == user_id).one()
        if tempItem is not None:
            self.dsession.delete(tempItem)
            self.dsession.commit()

    def delete_category(self, category_id):
        """  Deletes an category by id
        Argument:
            category_id: id of the category being deleted
        """
        tempItem = self.dsession.query(Categories).filter(
            Categories.id == category_id).one()
        if tempItem is not None:
            self.dsession.delete(tempItem)
            self.dsession.commit()
