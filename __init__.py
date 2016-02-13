"""Webserver for the Catalog application."""

import random
import string
import httplib2
import json
import requests
import datetime
import xmltodict
from datetime import timedelta
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask import Flask, render_template, request
from flask import redirect, url_for, flash
from flask import session as login_session
from flask import make_response
from os import curdir, sep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.catalogdb.database_setup import Categories, User, Items, Base
from src.catalogutils.db_interface import catalog_interface
from src.catalogutils.custompagination import cusotmPaginator
from src.catalogutils.catalogforms import UserForm, AdminLoginForm
from src.catalogutils.catalogforms import CategoriesForm, ItemForm
# IMPORTS FOR oAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials


GOOGLE_FILE = curdir + sep + 'src/json/client_secrets.json'

app = Flask(__name__)
engine = create_engine('postgresql://cataloga:catalog@localhost/catalogdb')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app.logger.debug("DB Session OK")
catalogDb = catalog_interface(session)

# number of results to display per page for Items
PER_PAGE_ITEMS = 9

#  Client Id for Google
CLIENT_ID = json.loads(
    open(GOOGLE_FILE, 'r').read())['web']['client_id']

# Application Name
APPLICATION_NAME = "Sams Item Catalog"

# secret key for the sessions
APP_SECRET_KEY = 'thisisaseceretkeythisisaseceretkeythisisaseceretkey'

# No of items to display in the crousel
NO_LATEST_ITEMS = 9

# How may days old is treated as new
CUT_OFF_DATE = 7

# session timeout set to 30 minutes
SESSION_TIME_OUT = 30


def update_category_list():
    """
    caches the list of categories
    """
    result = dict([(int(cat.id), cat.name)
                   for cat in catalogDb.get_all_categories()])
    return result


def get_error_template(error_message):
    """
    render the error message template
    Argument:
        error_message: message to be displayed on the page
    """
    output = render_template('header.html', SESSION=login_session)
    output += render_template('error.html',
                              message=error_message)
    output += render_template('footer.html')
    return output


def get_categories_list(page):
    """
    returns the category list template
    Arguments:
        page: the page number of the list.
    """
    resultsTemplate = ""
    categories = catalogDb.get_all_categories()
    # Check if there are categories
    if(len(categories) >= 1):
        pagination = cusotmPaginator(page, PER_PAGE_ITEMS, categories)
        slices = pagination.getPageSlice()
        resultsTemplate = render_template(
            "category_list.html", categories=slices,
            SESSION=login_session, pagination=pagination)
        resultsTemplate += render_template("pages_list.html",
                                           pagination=pagination)
    else:
        # if categories not found return the user to error page
        resultsTemplate = render_template(
            "error.html",
            message="Sorry we could not find what you were looking for")
    return resultsTemplate


def get_item_list(page):
    """
    gets the list of items for a user, paginates and
    creates a template for display
    Arguments:
        page: the page number of the list.
    """
    # check if admin is logged in if yes fetch all items
    if is_admin_loggedin():
        items = catalogDb.get_all_items()
    elif is_someone_Loggedin():
        # check if someone is logged in if yes fetch all items
        # for that user only
        app.logger.debug(
            "Fetching records for user " + str(login_session['userid']))
        items = catalogDb.get_all_items_user(login_session['userid'])
        app.logger.debug(str(len(items)) + " records found")
        if len(items) == 0:
            # if no records found list all records in read only mode
            app.logger.debug("Getting all records found")
            flash("You have not added any Items yet", category="warning")
            items = catalogDb.get_all_items()
    else:
        # list all records in read only mode
        items = catalogDb.get_all_items()

    if len(items) >= 1:
        # if more than one record then paginate
        pagination = cusotmPaginator(page, PER_PAGE_ITEMS, items)
        slices = pagination.getPageSlice()
        output = render_template(
            "items_list.html", items=slices, SESSION=login_session,
            pagination=pagination)
        output += render_template("pages_list.html",
                                  pagination=pagination)
    else:
        output = render_template('error.html',
                                 message="You Have not added any Items yet")
    return output


def get_user_list(page):
    """
    gets the list of user, paginates and
    creates a template for display
    Arguments:
        page: the page number of the list.
    """
    users = catalogDb.get_all_user()
    # if records found list all record
    if(len(users) >= 1):
        pagination = cusotmPaginator(page, PER_PAGE_ITEMS, users)
        slices = pagination.getPageSlice()
        resultsTemplate = render_template(
            "users_list.html", users=slices,
            SESSION=login_session, pagination=pagination)
        resultsTemplate += render_template("pages_list.html",
                                           pagination=pagination)
    else:
        resultsTemplate = render_template("empty_list.html")
    return resultsTemplate


def get_catalog(page):
    """
     creates a catalog template for display
    Arguments:
        page: the page number of the list.
    """
    parent_categories = catalogDb.get_all_parent_categories()
    sub_categories = catalogDb.get_all_sub_categories()
    latest_items = enumerate(catalogDb.get_latest_items(CUT_OFF_DATE,
                                                        NO_LATEST_ITEMS))
    all_items = catalogDb.get_all_items(True)
    pagination = cusotmPaginator(page, PER_PAGE_ITEMS, all_items)
    slices = enumerate(pagination.getPageSlice())
    template = render_template("items_catalog.html",
                               parent_categories=parent_categories,
                               sub_categories=sub_categories,
                               latest_items=latest_items,
                               item_count=NO_LATEST_ITEMS,
                               all_items=slices)
    template += render_template("pages_list.html",
                                pagination=pagination)
    return template


def get_cataegory_listings(db_category_name, page):
    """
     creates a catalog template for a specific category
    Arguments:
        page: the page number of the list.
        db_category_name: the name of the category
    """

    parent_categories = catalogDb.get_all_parent_categories()
    sub_categories = catalogDb.get_all_sub_categories()
    latest_items = enumerate(catalogDb.get_latest_items(CUT_OFF_DATE,
                                                        NO_LATEST_ITEMS))

    all_items = catalogDb.get_items_by_category(db_category_name)
    pagination = cusotmPaginator(page, PER_PAGE_ITEMS, all_items)
    slices = enumerate(pagination.getPageSlice())
    if not latest_items:
        flash("Could not find anything for this category ", category="info")
    template = render_template("items_catalog.html",
                               parent_categories=parent_categories,
                               sub_categories=sub_categories,
                               latest_items=latest_items,
                               item_count=NO_LATEST_ITEMS,
                               all_items=slices)
    template += render_template("pages_list.html",
                                pagination=pagination)
    return template


def get_cataegory_item(item_id):
    """
    renders the template for an Item in a category
    Arguments:
        item_id: The item id for the record
    """
    parent_categories = catalogDb.get_all_parent_categories()
    sub_categories = catalogDb.get_all_sub_categories()
    category_item = catalogDb.get_item_by_id(item_id)
    if not category_item:
        result = render_template('error.html',
                                 message="Could not find this item")
    else:
        result = render_template("category_item_view.html",
                                 parent_categories=parent_categories,
                                 sub_categories=sub_categories,
                                 category_item=category_item)
    return result


def get_cataloged_items():
    """
    returns the list of all active items.
    """
    items = catalogDb.get_all_items()
    parent_categories = catalogDb.get_all_parent_categories()
    sub_categories = catalogDb.get_all_sub_categories()
    return render_template('sitemap.xml', parent_categories=parent_categories,
                           sub_categories=sub_categories,
                           items=items)


def process_admin_login(adminuser):
    """
    sets the admin user information the session
    Arguments:
        adminuser: the admin user object
    """
    login_session['username'] = adminuser.name
    login_session['email'] = adminuser.email
    login_session['account_type'] = "ADMIN"
    login_session['userid'] = 1


def is_admin_loggedin():
    """
    returns true if a admin account is logged in
    """
    try:
        acType = login_session['account_type']
    except:
        acType = None

    if acType is not None and acType == "ADMIN":
        result = True
    else:
        result = False
    return result


def is_someone_Loggedin():
    """
    returns true if someone is logged in
    """
    try:
        username = login_session['username']
    except:
        username = None

    if username is not None:
        result = True
    else:
        result = False
    return result


def verify_owner_login(item_user):
    """
    returns true if the current user is the owner of the item or a Admin user
    Arguments:
        item_user:The user id of the owner of the item.
    """
    try:
        result = login_session['userid'] == item_user
        result = result or is_admin_loggedin()
    except:
        result = False
    app.logger.debug(" verify login " + str(result))
    return result


def other_page_urls(page):
    """
    creates the page url for pagination
    Arguments:
        page: the page number of the list.
    """
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def get_category_name(category_id):
    """
    returns the category name from the cached
    category_list
    Arguments:
        category_id: the id of the category for which the name is required.
    """
    result = "Uncategorized"
    try:
        result = login_session['categorylist'][category_id]
    except:
        app.logger.debug("cat list empty category_id " + str(category_id))
        login_session['categorylist'] = update_category_list()
        result = login_session['categorylist'][category_id]

    return result


def format_name_for_url(conversion_string):
    """
    strips the spaces and replaces them with
    '~' for passing these in the URL
    Arguments:
        conversion_string: the string to be converted.
    """
    return conversion_string.replace(" ", '~')


def unformat_name_for_url(conversion_string):
    """
    strips the '~' and replaces them with
    spaces
    Arguments:
        conversion_string: the string to be converted.
    """
    return conversion_string.replace("~", ' ')


@app.before_request
def add_state():
    """
        Validates and removes the CSRF token from post requests.
    """
    login_session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=SESSION_TIME_OUT)
    app.logger.debug(request.path)
    if request.method == "POST":
        try:
            token = login_session['state']
            # Skip the token deletion as it is used in the gconnect code.
            exceptions = ['/gconnect', '/fbconnect']
            isException = False
            for ex in exceptions:
                if ex in request.path:
                    isException = True
                    break

            if not isException:
                login_session.pop('state', None)
        except:
            token = None

        app.logger.debug(token)
        request_token = request.form.get('state') or request.args.get('state')
        app.logger.debug(request_token)
        # if session token and the request token dont match show error
        if not token or token != request_token:
            flash("""Invalid request or session
                timed out please login again""", "danger")
            return redirect(url_for('login'))
        else:
            # if the tokens are valid process the request normally
            app.logger.debug("Valid Token Proceed")


def generate_state():
    """
    generates a CSRF token adds this to the session
    this is called from the templates
    """
    if 'state' not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in xrange(32))
        login_session['state'] = state
    return login_session['state']


def create_external_url(url):
    """
    creates a fully qualified URL from the contextual
    URL
    Arguments:
        url: the url that needs to be converted.
    """
    return urljoin(request.url_root, url)


def is_active_nav(nav_item):
    """
    checks if a nav item is active
    Arguments:
        nav_item : nav item  to be checked
    returns:
        active or ""
    """
    result = ""
    print nav_item
    print request.path.find(nav_item)
    if request.path.find(nav_item) >= 0:
        result = "active"
    return result

# adding required functions to the template system
app.jinja_env.globals['other_page_urls'] = other_page_urls
app.jinja_env.globals['isSomeoneLoggedIn'] = is_someone_Loggedin
app.jinja_env.globals['isAdminLoggedIn'] = is_admin_loggedin
app.jinja_env.globals['verifyOwnerLogin'] = verify_owner_login
app.jinja_env.globals['get_category_name'] = get_category_name
app.jinja_env.globals['format_name_for_url'] = format_name_for_url
app.jinja_env.globals['generate_state'] = generate_state
app.jinja_env.globals['is_active_nav'] = is_active_nav


def set_page_title(page_name):
    """
    Sets the page title in the session
    """
    login_session['app_name'] = APPLICATION_NAME
    login_session['page_title'] = page_name


@app.route('/', defaults={'page': 1})
@app.route('/catalog', defaults={'page': 1})
@app.route('/catalog/<int:page>')
def catalog(page):
    """
    serves the paginated catalog
    Arguments:
        page: the page number that is to be displayed
        the default value for page is 1
    """
    set_page_title("Catalog")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_catalog(page)
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/catalog/<category_name>/items', defaults={'page': 1})
@app.route('/catalog/<category_name>/items/<int:page>')
def category_listings(category_name, page):
    """
     serves the paginated list of items for a category
     Arguments:
         category_name: name of the category for which item are to be searched
         page: the page number that is to be displayed the
         default value is page
     """
    set_page_title("Category Items")
    db_category_name = unformat_name_for_url(category_name)
    app.logger.debug("Listing items for " + db_category_name)
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_cataegory_listings(db_category_name, page)
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/catalog/<category_name>/<item_name>/<int:item_id>')
def category_item(category_name, item_name, item_id):
    """
    serves the selected item
    Arguments:
        category_name: name of the category for which item are to be searched
        item_name: the item name to be displayed in URL
        item_id: the item that is to be displayed
    """
    set_page_title("Items Details")
    app.logger.debug("Listing items for " + category_name)
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_cataegory_item(item_id)
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/catagory-list', defaults={'page': 1})
@app.route('/category-list/<int:page>')
def categories(page):
    """
    serves the paginated list of categories
    Arguments:
        page: the page number that is to be displayed
        the default value for page is 1
    """
    set_page_title("Categories")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_categories_list(page)
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/item-list', defaults={'page': 1})
@app.route('/item-list/<int:page>')
def items(page):
    """
    serves the paginated list of items
    Arguments:
        page: the page number that is to be displayed
        the default value for page is 1
    """
    set_page_title("Items")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_item_list(page)
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/', defaults={'page': 1})
@app.route('/users', defaults={'page': 1})
@app.route('/users/<int:page>')
def users(page):
    """
    serves the paginated list of users
    Arguments:
        page: the page number that is to be displayed
        the default value for page is 1
    """
    set_page_title("Users")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    try:
        if not is_admin_loggedin():
            # if the user logged in is not an admin show error
            output += render_template('error.html',
                                      message="""You need to login
                                      as administrator""")
        else:
            # show the list of user
            output += get_user_list(page)
    except:
        output += render_template('error.html',
                                  message="Oops Something went wrong")
        raise
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/edit-user', defaults={'userid': -1}, methods=['GET', 'POST'])
@app.route('/edit-user/<int:userid>', methods=['GET'])
def edit_user(userid):
    """
    serves the edit user functionality. Shows the populated form,
    when a post request is made the form is submitted and the user is
    updated
    Arguments:
        userid: if user id is passed then user is edited else.
         Default is -1
    """
    form = UserForm(request.form)
    app.logger.debug("Request Method " + request.method)
    app.logger.debug("Form Valid " + str(form.validate()))
    set_page_title("Add User")
    if request.method == 'POST' and form.validate():
        # if the form is valid and is a post request
        # create a new user
        newUser = User()
        form.populate_obj(newUser)
        # if the user record has an id process edit
        if newUser.id is not None:
            if catalogDb.update_user_details(newUser):
                flash('User Updated Successful!', category="success")
            else:
                flash('There was an error updating user!', category="danger")
        else:
            flash("User Not Found!", category="info")
        # take the user back to the list of users
        return redirect(url_for('users'))
    if userid is not None and userid >= 0:
        # if user id is passed and it is not the default -1
        # take the user to the pre populated form
        app.logger.debug("User Id" + str(userid))
        tempUser = catalogDb.get_user_by_id(userid)
        form = UserForm(request.form, obj=tempUser)
        set_page_title("Edit User")

    output = render_template('header.html', SESSION=login_session)
    output += render_template('editUser.html', form=form)
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/add-edit/category', defaults={'category_id': -1},
           methods=['GET', 'POST'])
@app.route('/add-edit/category/<int:category_id>', methods=['GET'])
def new_category(category_id):
    """
    serves the request for add and edit Categories.
    Shows the populated form when an category_id is passed
    when a post request is made the form is submitted and the user is
    updated
    Arguments:
        userid: if user id is passed then user is edited else.
         Default is -1
    """
    try:
        if not is_someone_Loggedin() and not is_admin_loggedin():
            # if user is not logged in throw error
            return get_error_template("""Please log in to add
             / edit Categories.""")

        form = CategoriesForm(request.form)
        # assign the list of choices to the form for the parent category
        form.parent.choices = [(int(cat.id), cat.name)
                               for cat in
                               catalogDb.get_all_parent_categories()]
        app.logger.debug("category_id: " + str(category_id) +
                         " request.method " + request.method)
        set_page_title("Add Category")

        if request.method == 'POST' and form.validate():
            newCategories = Categories()
            form.populate_obj(newCategories)
            if form.data['id']:
                # if its a  valid post and comes with an id
                # process the update category
                catalogDb.update_categories_details(newCategories)
            else:
                # if its a valid post and comes without an id
                # process and save the new category
                newCategories.id = None
                tempCategory = catalogDb.get_category_by_name(
                    newCategories.name)
                if tempCategory is None:
                    # verify if the category already exists if not
                    # create a new category
                    app.logger.debug("Creating Category")
                    catalogDb.add_categories(newCategories)
                    flash("New Category Created!",
                          category="success")
                else:
                    # if category exists show user an error
                    # and route him back to the categories list
                    flash("Category you are trying to create already exists!",
                          category="danger")
            return redirect(url_for('categories'))

        if category_id is not None and category_id >= 0:
            # if category id is not passed in or is default
            # show user an empty form for creating a new category
            app.logger.debug("Showing Category Details")
            categoryX = catalogDb.get_categories_by_id(category_id)
            form = CategoriesForm(request.form, obj=categoryX)
            form.parent.choices = [(int(cat.id), cat.name)
                                   for cat in
                                   catalogDb.get_all_parent_categories()]
            set_page_title("Edit Category")

        output = render_template('header.html', SESSION=login_session)
        output += render_template('addeditCategories.html', form=form)
        output += render_template('footer.html', SESSION=login_session)
    except:
        # show error if something goes wrong
        return get_error_template("Oops Something went wrong")

    return output


@app.route('/add-edit/item', defaults={'item_id': -1},
           methods=['GET', 'POST'])
@app.route('/add-edit/item/<int:item_id>', methods=['GET'])
def new_item(item_id):
    """
    serves the request for add and edit items.
    Shows the populated form when an category_id is passed
    when a post request is made the form is submitted and the user is
    updated
    Arguments:
        userid: if user id is passed then user is edited else.
         Default is -1
    """
    try:
        if not is_someone_Loggedin() and not is_admin_loggedin():
            # show error if user is not logged in
            return get_error_template("Please log in to add / edit Items.")

        form = ItemForm(request.form)
        # add choices for the category options
        form.category_id.choices = [(int(cat.id), cat.name)
                                    for cat in
                                    catalogDb.get_all_sub_categories()]
        set_page_title("Add Item")

        if request.method == 'POST' and form.validate():
            newItem = Items()
            form.populate_obj(newItem)
            if form.data['id']:
                # if valid post request and id is present
                # process edit
                catalogDb.update_item_details(newItem)
                flash("Item updated.", category="success")
            else:
                # if id is not present process the add
                # functionality and save the item
                newItem.id = None
                newItem.user_id = login_session['userid']
                catalogDb.add_item(newItem)
                flash("Item added.", category="success")

            return redirect(url_for('items'))

        if item_id is not None and item_id >= 0:
            # if default id show user empty form
            app.logger.debug("Showing Item Details")
            itemX = catalogDb.get_item_by_id(item_id)
            form = ItemForm(request.form, obj=itemX)
            form.category_id.choices = [(int(cat.id), cat.name)
                                        for cat in
                                        catalogDb.get_all_sub_categories()]
            set_page_title("Edit Item")

        output = render_template('header.html', SESSION=login_session)
        output += render_template('addeditItems.html', form=form)
        output += render_template('footer.html')
    except:
        return get_error_template("Oops Something went wrong")

    return output


@app.route('/confirmdelete/<delete_type>/<int:delete_key>')
def confirm_delete(delete_type, delete_key):
    """
    Shows user a confirmation message when the user tries to
    delete item user or category,
    if the a user or a category is deleted the items associated are
    also deleted.
    Arguments:
        delete_type: if it is a items, categories or user delete.
        delete_key: the id of item , category or the user to be
        deleted

    """
    try:
        if delete_type == 'items':
            # get the item if it is item delete operation
            itemX = catalogDb.get_item_by_id(delete_key)
        elif delete_type == 'users':
            # get the user if it is item delete operation
            itemX = catalogDb.get_user_by_id(delete_key)
        elif delete_type == 'categories':
            # get the categories if it is item delete operation
            itemX = catalogDb.get_categories_by_id(delete_key)

    except:
        return get_error_template("Oops Something went wrong")

    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += render_template('confirm_delete.html', type=delete_type,
                              item=itemX, SESSION=login_session)
    output += render_template('footer.html', SESSION=login_session)
    return output


@app.route('/deleteitem/<delete_type>/<int:delete_key>', methods=['POST'])
def delete_item(delete_type, delete_key):
    """
    Once the user confirms the delete on above method
    the item, category or the user is delete.
    if the a user or a category is deleted the items associated are
    also deleted.
    Arguments:
        delete_type: if it is a items, categories or user delete.
        delete_key: the id of item , category or the user to be
        deleted

    """
    if not is_someone_Loggedin() and not is_admin_loggedin():
        # if the user is not logged in throw an error
        return get_error_template("Please log in to add / edit Items.")

    try:
        if delete_type == 'items':
            # get the the item to be deleted
            itemX = catalogDb.get_item_by_id(delete_key)
            #  verify if the user is authorized to delete the item
            # throw an error if the user is not allowed
            if not verify_owner_login(itemX.user_id):
                return get_error_template(
                    "You are not authorized to delete this Item")
            else:
                # delete the item
                catalogDb.delete_item(itemX.id)
                flash("Item Deleted Successfully", category="success")
        elif delete_type == 'users':
            # get the user that has to be deleted based on the id
            itemX = catalogDb.get_user_by_id(delete_key)
            catalogDb.delete_user(itemX.id)
            flash("User Deleted Successfully", category="success")
        elif delete_type == 'categories':
            # get the category to be deleted
            itemX = catalogDb.get_categories_by_id(delete_key)
            catalogDb.delete_category(itemX.id)
            flash("Category and items associated with it deleted successfully",
                  category="success")
    except:
        # if there is an exception show and error
        return get_error_template("Oops Something went wrong")
    # route the user to the appropriate list
    return redirect(url_for(delete_type))


@app.route('/login')
def login():
    """
    server the login request for Google
    """

    # check if already logged in if yes throw an error
    if is_someone_Loggedin():
        flash('You are already logged in!', category="warning")
        return redirect(url_for('catalog'))
    else:
        endpointurl = "login.html"

    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    login_session['state'] = state
    set_page_title("Login")
    output = render_template('header.html', STATE=state)
    output += render_template(endpointurl, STATE=state, SESSION=login_session)
    output += render_template('footer.html', STATE=state)
    return output


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """
    serves the admin user login
    """
    if is_someone_Loggedin():
        # if already logged in throw an error
        endpointurl = "already_loggedin.html"
        flash('You are already logged in!', category="warning")
    else:
        endpointurl = "admin_login.html"

    form = AdminLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # if a valid post request check for the username
        # email and verify the credentials
        admnuser = User()
        form.populate_obj(admnuser)
        chkUser = catalogDb.admin_login(admnuser)
        if chkUser is not None:
            # if login successful route user to home page
            flash("Login Successful!", category="success")
            process_admin_login(chkUser)
            return redirect(url_for('catalog'))
        else:
            # show error on error
            flash("Incorrect email and password combination!",
                  category="danger")
            return redirect(url_for('admin_login'))

    output = render_template('header.html', SESSION=login_session)
    output += render_template(endpointurl, form=form, SESSION=login_session)
    output += render_template('footer.html')
    return output


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
     Process the google post login functionality
    """

    # Validate state token
    app.logger.debug("in gconnect")
    app.logger.debug("from request" + request.args.get('state'))
    app.logger.debug("from session" + login_session['state'])
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(GOOGLE_FILE, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        app.logger.debug("Code is " + code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    login_session['access_token'] = access_token
    app.logger.debug("access token" + access_token)
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    app.logger.debug(stored_credentials)
    app.logger.debug(gplus_id)
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    credentials = AccessTokenCredentials(
        login_session['credentials'], 'user-agent-value')
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['account_type'] = "GOOGLE"
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   accounttype="GOOGLE", lastlogin=datetime.date.today(),
                   pictureurl=login_session['picture'])
    user_id = catalogDb.add_user(newUser)
    login_session['userid'] = user_id
    output = ""
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;'
    output += ' border-radius: 150px;-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" %
          login_session['username'], category="success")
    print "done!"
    return output


@app.route('/adminlogout')
def admin_logout():
    """
    serves the admin logout functionality
    """
    login_session['username'] = None
    login_session['email'] = None
    login_session['account_type'] = None
    login_session['userid'] = None
    flash("Logged out successfully !", category="info")
    return redirect(url_for("catalog"))


@app.route('/adminlogout')
def facebook_logout():
    """
    serves the admin logout functionality
    """
    login_session['username'] = None
    login_session['email'] = None
    login_session['account_type'] = None
    login_session['userid'] = None
    flash("Logged out successfully !", category="info")
    return redirect(url_for("catalog"))


@app.route('/gdisconnect')
def gdisconnect():
    """
    process the google dogout functionality
    """
    app.logger.debug("Verifying  the type of account")
    # check if this is an admin account and logout through that
    try:
        account_type = login_session['account_type'] or None
    except:
        account_type = None

    if account_type == "ADMIN":
        return redirect(url_for("admin_logout"))
    elif account_type == "FACEBOOK":
        return redirect(url_for("facebook_logout"))

    access_token = login_session['access_token']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o'
    url += '/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('You have Been Successfully Logged Out.', category="info")
        return redirect(url_for("catalog"))
    else:

        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog.xml')
def catalog_xml():
    """ returns the complete catalog in
    cusotm XML
    """

    template = get_cataloged_items()
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response


@app.route('/catalog.json')
def catalog_json():
    """ returns the complete catalog in
    cusotm json
    """

    template = get_cataloged_items()
    parsed = xmltodict.parse(template)
    print parsed
    response = make_response(json.dumps(parsed))
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/newitems.atom')
def recent_items_feed():
    feed = AtomFeed('New Items',
                    feed_url=request.url, url=request.url_root)
    items = catalogDb.get_latest_items(CUT_OFF_DATE,
                                       NO_LATEST_ITEMS)
    for item in items:
        text = " New item in category " + get_category_name(item.category_id)
        text += " Price Range" + str(item.pricerange)
        text += " Item Description " + item.description[100:]
        text += "... Read more here "
        text += create_external_url(
            url_for('category_item',
                    category_name=format_name_for_url(
                        get_category_name(item.category_id)),
                    item_name=format_name_for_url(item.name),
                    item_id=item.id))

        feed.add(item.name, unicode(text),
                 content_type='html',
                 author="Sams Item Catalog",
                 url=create_external_url(
            url_for('category_item',
                    category_name=format_name_for_url(
                        get_category_name(item.category_id)),
                    item_name=format_name_for_url(item.name),
                    item_id=item.id)),
                 updated=item.lastupdated or item.created,
                 published=item.created)
    return feed.get_response()


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
     Process the google post login functionality
    """

    # Validate state token
    app.logger.debug("in fbconnect")
    app.logger.debug("from request" + request.args.get('state'))
    app.logger.debug("from session" + login_session['state'])
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # obtain user info
    rawdata = request.data
    data = json.loads(rawdata)
    app.logger.debug(data['name'])
    login_session['username'] = data['name']
    # my current permissions do not allow picture
    login_session['picture'] = None
    login_session['email'] = str(data['id']) + '@itemcatalog.com'
    login_session['account_type'] = "FACEBOOK"
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   accounttype="FACEBOOK", lastlogin=datetime.date.today(),
                   pictureurl=login_session['picture'])
    user_id = catalogDb.add_user(newUser)
    login_session['userid'] = user_id
    output = ""
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("You are now logged in as %s" %
          login_session['username'], category="success")
    print "done!"
    return output


@app.errorhandler(404)
def page_not_found(e):
    """ routes the invalid Urls back to the home page"""
    flash("We could not find the what you were looking for..", "danger")
    return redirect(url_for("catalog"))

if __name__ == '__main__':
    app.secret_key = APP_SECRET_KEY
    app.debug = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.logger.debug("Starting The Server -- catalog app")
    app.run()
