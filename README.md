## Introduction
A web application for catalog management. The Item Catalog web application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

---

## Table of Contents

1. [Introduction ](#introduction)
    - [Program Features](#program-features)
1. [Setup ](#setup)
    - [Prerequisites ](#prerequisites)
    - [Creating The Database ](#creating-the-database)   
    - [Populate Basic Data](#populate-basic-data)   
    - [Running The Application ](#running-the-application)
1. [Assumptions](#assumptions)
1. [Extra Credit Features](#extra-credit-features)
1. [Code Documentation ](#code-documentation)
    - [Folder Structure ](#folder-structure)
    - [src/catalogdb/database_setup.py](#database-setup-file)
    - [src/catalogdb/catalog_data_script.py](#catalog-data-script)
    - [src/catalogutils/catalogforms.py](#catalog-forms)
    - [src/catalogutils/custompagination.py](#custom-pagination)
    - [src/catalogutils/db_interface.py](#db-interface)
    - [application.py](#application-file)
1. [Database Structure ](#database-structure)

---

###Program Features.
	
* ** Responsive Web Interface: ** The web interface for the application is responsive and supports multiple screen sizes.

![alt text][hpage]

* ** Administration Module: ** Application supports an administration module. If your are logged in as an Administrator you can add new categories and modify items posted by any user. Admin user can enable and disable users, categories and items. 

![alt text][admmnu]

---

![alt text][loginli]

---

![alt text][adminLogin]

---

   ** Default Login Information for Administrator **

| User Name | admin@itemcatalog.com |
|:---------:|:---------------------:|
|  Password |         123456        | 

* **Sub-Categories: ** Application supports one level of sub categories Like the category Electronics and Computers  can have sub categories Headphones, Video Games , Laptops and Tablets.

![alt text][catli]

---

* **Pagination: ** Pagination of results for easy readability on most of the pages.

![alt text][itmli]

---

* **Moderation: ** Administrator can enable and disable users, categories and items. The disabled items and categories will not show up in the catalog but will still be available in the users 

![alt text][editu]

---

![alt text][edititm]

---

![alt text][catli]

---

* **Third Party Login :** The application allows you to use you google account to login.

![alt text][loginli]

---

* **CRUD :** The application allows a logged in user to perform CRUD operations on their items. An administrator can update all items.

![alt text][editu]

---

![alt text][delfonf]

---

* **Item Images :** The application allows a logged in user to specify a picture / image url for there items these images are used in the listings.

![alt text][itmviewnoli]

---

![alt text][itmvli]

* **Latest Items :** The application displays latest items in a carousel on the home page. The number of Items and the cut of date can be changed in code. The default values are 7 days and 9 Items.

![alt text][hpage]

---

* **XML Catalog :** The application has an option to get the entire catalog as an XML. You can use the following URL ** http://localhost:8000/catalog.xml ** or using the Administration menu This is assuming the server is running on port 8000 


* **JSON Catalog :** The application has an option to get the entire catalog as an XML. You can use the following URL ** http://localhost:8000/catalog.json ** or using the Administration menu This is assuming the server is running on port 8000 

* **ATOM Feed :** The application has an option to get an ATOM RSS feed for the latest items from the catalog as an XML. You can use the following URL ** http://localhost:8000/newitems.atom ** or using the Administration menu This is assuming the server is running on port 8000 

![alt text][admmnu]

* **Readable URLs : ** most of the relevant urls are readable.


---


## Setup
### Prerequisites
1.  Python v2.7 or greater should be installed.
2.  PYTHON environment variable should be correctly set with the path to python executable.
3.  PYTHONPATH environment variable should be set with the python root folder
4.  PostgreSQL installation
5.  Vagrant installation if required 
6.  install WTForms (pip install WTForms or sudo pip install WTForms)
7.  install werkzeug version 0.8.3 (pip install werkzeug==0.8.3 or sudo pip install werkzeug==0.8.3)
8.  install flask 0.9 (pip install flask==0.9 or sudo pip install flask==0.9)
9.  install Flask-Login (pip install Flask-Login==0.1.3 or sudo pip install Flask-Login==0.1.3)
10. Clone this repository to some location on your system. 
11. A version of the database is included in the repo. In case you want to the catalog database should be created as mentioned in the [Creating The Database ](#creating-the-database) section. 
12. If you create a new datab.se please run database scripts as mentioned in the [Populate Basic Data](#populate-basic-data) section.


###Creating The Database
Asuming you are already logged in to vagrant ssh
1. Navigate to the folder where the repository has been cloned.
2. Use the `python -m src.catalogdb.database_setup` command to create a catalogdatabase.db.



###Populate Basic Data 
Asuming you are already logged in to vagrant ssh and have already created the database as mentioned in section [Creating The Database ](#creating-the-database).
1. Navigate to the folder where the repository has been cloned.
2. Use the `python -m src.catalogdb.catalog_data_script' This will insert some data and most importantly the admin user information.



###Running The Application

Navigate to the folder where the repository is cloned.  Run the command to start the application

`python application.py`

The application can now be accessed [http://localhost:8000]( http://localhost:8000)



**[Back to top](#table-of-contents)**

---

## Assumptions

1. If the user is deleted the items associated are also deleted.
1. If the category is deleted the items associated are also deleted.
1. The category names are unique.
1. Only administrators are allowed to create and edit categories.
1. If latest items are not available as the specified time limit, the latest items are decided based on the created date.
1. The parent category "Parent Category" can not  be deleted.
1. Logged in users can delete only the items they own.
1. **The Facebook oAuth implementation is not complete.**. The login works and the user is allowed in the app. The oAuth step 2 is not implemented yet (ran out of time). 


**[Back to top](#table-of-contents)**

---

## Extra Credit Features

1. ** Sub-Categories: ** Application supports one level of sub categories Like the category Electronics and Computers  can have sub categories Headphones, Video Games , Laptops and Tablets.
1. ** Pagination: ** Pagination of results for easy readability on most of the pages.
1. ** Moderation: ** Administrator can enable and disable users, categories and items. The disabled items and categories will not show up in the catalog but will still be available in the users 
1. ** Item Images :** The application allows a logged in user to specify a picture / image url for there items these images are used in the listings.
1. ** Latest Items :** The application displays latest items in a carousel on the home page. The number of Items and the cut of date can be changed in code. The default values are 7 days and 9 Items.
1. ** XML Catalog :** The application has an option to get the entire catalog as an XML. You can use the following URL ** http://localhost:8000/catalog.xml ** this is assuming the server is running on port 8000
1. ** JSON Catalog :** The application has an option to get the entire catalog as an JSON. You can use the following URL ** http://localhost:8000/catalog.json ** this is assuming the server is running on port 8000
1. ** ATOM Feed :** The application has an option to get an ATOM RSS feed for the latest items from the catalog as an XML. You can use the following URL ** http://localhost:8000/newitems.atom ** this is assuming the server is running on port 8000
**[Back to top](#table-of-contents)**

---
##Code Documentation

###Folder Structure

Application Folder Structure

![alt text][fstr]


**[Back to top](#table-of-contents)**
---
###Database Setup File

`src/catalogdb/database_setup.py` file has the database configuration for the database.

To execute navigate to the `catalog` folder run the command 

`python -m src.catalogdb.satabase_setup`


---

###Catalog Data Sctipt

`src/catalogdb/catalog_data_script.py` file contains the basic / test data scripts. When run inserts the data into relevant tables.

To execute navigate to the `catalog` folder run the command 

`python -m src.catalogdb.catalog_data_script`

---

###Catalog Forms

`src/ctalogutils/catalogforms.py`  this file contains the following `wtform` classes


**UserForm:** This is used for add and edit users
**AdminLoginForm** This form is used for the admin login functionality
**CategoriesForm** This form is used for add and edit categories
**ItemForm** This form is used for add and edit items.

---

###Custom Pagination

`src/ctalogutils/ccustompagination.py`  this file contains cusotmPaginator class the is required for breaking up the big list of items / catefories / users



### __init__(self, page, items_per_page, items):

The constructor for the custom pagination class

* Arguments:
    * page : the current page number
    * items_per_page :  how many records to show in each page
    * items : the collection of items to be paginated
    * self.current_page = page
    * self.items_per_page = items_per_page
    * self.total_count = len(items)
    * self.items = items


### totalPages(self):

Returns the total number of pages required


### hasPagesBefore(self):

Return if there are pages before the current page number


### hasPagesAfter(self):

Returns true if there are pages after the current page.

### getPageSlice(self):

Returns the slice of the object according to the page


---

### DB Interface

`src/ctalogutils/db_interface.py`  This file contains catalog_interface that has methods to connect to the database and fetch the results.

### __init__(self, new_session):

Constructor for the  interface and set the session

* Attributes:
    * new_session:      A database session

---

### get_all_categories(self):

Returns a list of all the Categories from the DB.

---

### get_all_parent_categories(self):

Returns a list of all the sub Categories from the DB.

---

### get_all_sub_categories(self):

Returns a list of all the sub Categories from the DB.

---

### get_all_items(self, only_active=False):

Returns a list of all the Categories from the DB.

* Arguments:
    * only_active: default is False searches for all items.If True searches only active items

---

### get_all_items_user(self, user_id):

Returns all the Items for a user

* Argument:
    * user_id: user for whih the items have to be searched for

---

### add_categories(self, new_cat):

Adds a new Categories record in the database

* Arguments:
    * new_cat: the new category object.

---

### add_item(self, new_item):

Adds a new item record in the database

* Arguments:
    * new_item: new item object.

---

### get_item_by_id(self, item_id):

Returns a item record by id

* Argument:
    * item_id: the id of the item to be searched

---

### get_items_by_category(self, db_category_name):

Returns a items record by category

* Arguments:
    * db_category_name: name of the category to search the record

---

### get_category_by_name(self, db_category_name):

Returns a category record by category name

* Arguments:
    * db_category_name: name of the category to search the record

---

### get_category_item_by_name(self, db_category_name, db_item_name):

Returns a items record by category and item name

* Arguments:
    * db_category_name: name of the category to search the record
    * db_item_name: The name of the item being searched

---

### get_latest_items(self, time_delta, item_limit):

Returns latest items if not found it will return the latest from all the records. This returns only active Items

* Arguments:
    * time_delta: number of day, how old items are considered as latest
    * item_limit: the number of records to be returned

---

### get_categories_by_id(self, category_id):

Returns a Categories record by id

* Argument:
    * category_id : id of the category that is being searched

---

### update_item_details(self, item):

Updates a item record by id

* Argument:
    * item: The item object that is being updated.

---

### update_categories_details(self, category):

Updates a category record by id

* Argument:
    * category: the category object that is being updated

---

### get_all_user(self):

Returns a list of all the users from the DB.

---

### update_user_login(self, existinguser):

Updates the user login time.

* Argument:
    * existinguser: the user that is being updated

---

### add_user(self, new_user):

Adds a new user record in the database

* Argument:
    * new_user: the new_user object that is being inserted

---

### get_user_by_id(self, user_id):

Returns a user record by id

* Arguments:
    * user_id: the id of the user


---

### update_user_details(self, user):

Updates a user record

* Argument:
    * user: the updated user object

---


### admin_login(self, adminuser):

Return a user bases on the username and password

* Argument:
    * adminuser: the object containing the username and
    * password of the admin user
---

### get_catalog_all(self):

Return a user bases on the username and password

---

### delete_item(self, item_id):

Deletes an item by id

* Argument:
    * item_id: id of the item being deleted

---

### delete_user(self, user_id):

Deletes an user by id

* Argument:
    * user_id: id of the user being deleted

---

### delete_category(self, category_id):

Deletes an category by id

* Argument:
    * category_id: id of the category being deleted

---

###Application File

`catalog/application.py` the application file contains the flask configuration, routes and other supporting methods

### update_category_list()

Caches the list of categories in the session

[Back to top](#table-of-contents)
---

### get_error_template(error_message):

Render the error message template

* Argument:
    * error_message: message to be displayed on the page



**[Back to top](#table-of-contents)**
---

### get_categories_list(page):

Returns the category list template

* Arguments:
    * page: the page number of the list.

* Returns:
    The parsed template for the category list page

**[Back to top](#table-of-contents)**
---

### get_item_list(page):

Gets the list of items for a user, paginates and creates a template for display

* Arguments:
    * page: the page number of the list.

* Returns:
    The parsed template for the item list page

**[Back to top](#table-of-contents)**
---    

### get_user_list(page):

Gets the list of user, paginates and creates a template for display

* Arguments:
    * page: the page number of the list.

* Returns:
    The parsed template for the user list page
    

**[Back to top](#table-of-contents)**
---

### get_catalog(page):

Creates a catalog template for display

* Arguments:
    * page: the page number of the list.
* Returns:
    The parsed template for the catalog page

**[Back to top](#table-of-contents)**
---

### get_cataegory_listings(db_category_name, page):

Creates a catalog template for a specific category

* Arguments:
      * page: the page number of the list.
      * db_category_name: the name of the category
* Returns:
    The parsed template for the category list page


**[Back to top](#table-of-contents)**
---

### get_cataegory_item(item_id):

Renders the template for an Item in a category

* Arguments:
    * item_id: The item id for the record
* Returns:
    The parsed template for the catalog page

**[Back to top](#table-of-contents)**
---

### get_cataloged_items()

Returns the list of all active items in xml format.


**[Back to top](#table-of-contents)**
---

### process_admin_login(adminuser):

Sets the admin user information the session

* Arguments:
    * adminuser: the admin user object

**[Back to top](#table-of-contents)**
---

### is_admin_loggedin()

Returns `True` if an admin account is logged in

**[Back to top](#table-of-contents)**
---

### is_someone_Loggedin()

Returns `True` if someone is logged in

**[Back to top](#table-of-contents)**
---

### verify_owner_login(item_user):

Returns `True` if the current user is the owner of the item or a Admin user

* Arguments:
    * item_user:The user id of the owner of the item.

**[Back to top](#table-of-contents)**
---

### other_page_urls(page):

Creates the page URL for pagination

* Arguments:
    * page: the page number of the list.
* Return the URL for the page.

**[Back to top](#table-of-contents)**
---

### get_category_name(category_id):

Returns the category name from the cached category_list

* Arguments:
    * category_id: the id of the category for which the name is required.

* Returns: the category name from the cached category_list


**[Back to top](#table-of-contents)**
---

### format_name_for_url(conversion_string):

Strips the spaces and replaces them with `~` for passing these in the URL

* Arguments:
    * conversion_string: the string to be converted.
* Returns: The converted string

    
**[Back to top](#table-of-contents)**
---

### unformat_name_for_url(conversion_string):

Strips the `~` and replaces them with spaces

* Arguments:
    * conversion_string: the string to be converted.

**[Back to top](#table-of-contents)**
---

### add_state()

Validates and removes the CSRF token from post requests.

**[Back to top](#table-of-contents)**
---

### generate_state()

Generates a CSRF token adds this to the session. This is called from the templates


**[Back to top](#table-of-contents)**
---

### create_external_url(url):

Creates a fully qualified URL from the contextual URL

* Arguments:
        url: the url that needs to be converted.

* Returns: A fully qualified URL


**[Back to top](#table-of-contents)**
---

### is_active_nav(nav_item):

Checks if a nav item is active
* Arguments:
    * nav_item : nav item  to be checked
* Returns: 'active' or ""

**[Back to top](#table-of-contents)**
---

### set_page_title(page_name):

Sets the page title in the session

**[Back to top](#table-of-contents)**
---

### catalog(page):

Serves the paginated catalog
* Arguments:
    * page: the page number that is to be displayed the default value for page is 1

**[Back to top](#table-of-contents)**
---

### category_listings(category_name, page):

Serves the paginated list of items for a category
* Arguments:
    * category_name: name of the category for which item are to be searched
    * page: the page number that is to be displayed the default value is page


**[Back to top](#table-of-contents)**
---

### category_item(category_name, item_name, item_id):

Serves the selected item
* Arguments:
    * category_name: name of the category for which item are to be searched
    * item_name: the item name to be displayed in URL
    * item_id: the item that is to be displayed

**[Back to top](#table-of-contents)**
---

### categories(page):
Serves the paginated list of categories

* Arguments:
    * page: the page number that is to be displayed the default value for page is 1

**[Back to top](#table-of-contents)**
---

### items(page):
Serves the paginated list of items
* Arguments:
    * page: the page number that is to be displayed the default value for page is 1

**[Back to top](#table-of-contents)**
---

### users(page):

Serves the paginated list of users
* Arguments:
    * page: the page number that is to be displayed the default value for page is 1


**[Back to top](#table-of-contents)**
---

### edit_user(userid):

serves the edit user functionality. Shows the populated form, when a post request is made the form is submitted and the user is updated
* Arguments:
    * userid: if user id is passed then user is edited else. Default is -1

**[Back to top](#table-of-contents)**
---

### new_category(category_id):

Serves the request for add and edit Categories. Shows the populated form when an category_id is passed when a post request is made the form is submitted and the user is  updated
* Arguments:
    * userid: if user id is passed then user is edited else. Default is -1

**[Back to top](#table-of-contents)**
---

### new_item(item_id):

Serves the request for add and edit items. Shows the populated form when an category_id is passed when a post request is made the form is submitted and the user is updated
* Arguments:
    * userid: if user id is passed then user is edited else. Default is -1

**[Back to top](#table-of-contents)**
---

### confirm_delete(delete_type, delete_key):

Shows user a confirmation message when the user tries to delete item user or category, if the a user or a category is deleted the items associated are also deleted.
* Arguments:
    * delete_type: if it is a items, categories or user delete.
    * delete_key: the id of item , category or the user to be deleted

**[Back to top](#table-of-contents)**
---

### delete_item(delete_type, delete_key):

Once the user confirms the delete on above method the item, category or the user is delete. if the a user or a category is deleted the items associated are also deleted.
* Arguments:
    * delete_type: if it is a items, categories or user delete.
    * delete_key: the id of item , category or the user to be deleted

**[Back to top](#table-of-contents)**
---

### login()
Server the login page and shows the login options for account login

**[Back to top](#table-of-contents)**
---

### admin_login()

Serves the admin user login

**[Back to top](#table-of-contents)**
---

### gconnect()

Process the google post login functionality

**[Back to top](#table-of-contents)**
---

### admin_logout()

Serves the admin logout functionality

**[Back to top](#table-of-contents)**
---

### gdisconnect()

Process the google dogout functionality


**[Back to top](#table-of-contents)**
---

### catalog_xml()

Returns the complete catalog in custom XML

**[Back to top](#table-of-contents)**
---

### catalog_json()

Returns the complete catalog in cusotm json format

**[Back to top](#table-of-contents)**
---

### recent_items_feed()

Returns a formatted ATOM RSS feed.

**[Back to top](#table-of-contents)**
---

### page_not_found(e):

Handles the invalid URLs

**[Back to top](#table-of-contents)**
---




##Database Structure

## Tables
The diagram below shows the different tables and their relationship

![alt text][dbdesign]

### User
This table contains the information about the users of the application.

    * id - id of the user
    * name - name of the user
    * email -email of the user
    * accounttype - account type to identify if it is admin 
    * isActive - is item active and can be displayed in the catalod
    * lastlogin - timestampof last login
    * pictureurl - user picture url
    * password - users password  required for admin users
    * created - when the user was created
    * lastupdated the last updated date of the record

**[Back to top](#table-of-contents)**
---

## Categories
The table contains the information about the categories and sub-categories

    * id - Categoey Id
    * name - name of the category
    * parent - id of the parent category
    * isActive - is the category Active
    * hasChildren - id category has children
    * created - when the user was created
    * lastupdated the last updated date of the record

**[Back to top](#table-of-contents)**
---

## Items

Table contains the items information 

    * id - id of the item
    * category_id - category id
    * user_id - item owner
    * name - name of the item
    * description - item description
    * pricerange - string price range
    * pictureurl - picture url of th item
    * isActive - is the item active
    * created - when the user was created
    * lastupdated the last updated date of the record

**[Back to top](#table-of-contents)**
---    
[editus]: https://github.com/v2saumb/catalog/blob/master/docs/images/userlist.gif "Edit users"
[loginli]: https://github.com/v2saumb/catalog/blob/master/docs/images/login-options.gif "Login Options"
[itmvli]: https://github.com/v2saumb/catalog/blob/master/docs/images/viewitems-loggedin.gif "Logged in Items View"
[itmviewnoli]: https://github.com/v2saumb/catalog/blob/master/docs/images/itemview.gif "Items view"
[itmnoli]: https://github.com/v2saumb/catalog/blob/master/docs/images/items-nologin.gif "Items No Login"
[itmli]: https://github.com/v2saumb/catalog/blob/master/docs/images/items-loggedin.gif "Items Logged in"
[edititm]: https://github.com/v2saumb/catalog/blob/master/docs/images/item-edit.gif "Edit Items"
[editu]: https://github.com/v2saumb/catalog/blob/master/docs/images/edit-user.gif "Edit User"
[delfonf]: https://github.com/v2saumb/catalog/blob/master/docs/images/delete-conf.gif "Delete Confirmation"
[catnoli]: https://github.com/v2saumb/catalog/blob/master/docs/images/cats-nologin.gif "Catagory Screen Without Login"
[catli]: https://github.com/v2saumb/catalog/blob/master/docs/images/cat-loggedin.gif "Category Screen Logged In"
[catitm]: https://github.com/v2saumb/catalog/blob/master/docs/images/cat-items.gif "Category Items Screen"
[admmnu]: https://github.com/v2saumb/catalog/blob/master/docs/images/admin-menu.gif "Admin Menu"
[hpage]: https://github.com/v2saumb/catalog/blob/master/docs/images/homepage.gif "Home Page"
[fstr]: https://github.com/v2saumb/catalog/blob/master/docs/images/folderstructure.gif "Folder Structure"
[adminLogin]: https://github.com/v2saumb/catalog/blob/master/docs/images/admin-login.gif "Admin Login Screen"
[dbdesign]: https://github.com/v2saumb/catalog/blob/master/docs/images/dbdiagram.gif "Database Design"