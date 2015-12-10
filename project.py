# webserver for the restaurant menu application
import sys
import random
import string
import httplib2
import json
import requests
import datetime
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from flask import session as login_session
from flask import make_response
from os import curdir, pardir, sep
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
import itertools

DATABASE_FILEPATH = curdir + sep + 'src/catalogdb/catalogdatabase.db'
GOOGLE_FILE = curdir + sep + 'src/json/client_secrets.json'

app = Flask(__name__)
engine = create_engine('sqlite:///' + DATABASE_FILEPATH)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app.logger.debug("DB Session OK")
catalogDb = catalog_interface(session)

# number of results to display per page
PER_PAGE = 10

#  Client Id for Google
CLIENT_ID = json.loads(
    open(GOOGLE_FILE, 'r').read())['web']['client_id']

# Application Name
APPLICATION_NAME = "Sams Item Catalog"

# secret key for the sessions
APP_SECRET_KEY = 'thisisaseceretkey'

# No of items to display in the crousel
NO_LATEST_ITEMS = 9

# How may days old is treated as new
CUT_OFF_DATE = 7


def update_category_list():
    """
    caches the list of categories
    """
    result = dict([(int(cat.id), cat.name)
                   for cat in catalogDb.get_all_categories()])
    return result


def get_categories_list(page):
    """
    returns the category list template
    """
    resultsTemplate = ""
    categories = catalogDb.get_all_categories()
    if(len(categories) >= 1):
        pagination = cusotmPaginator(page, PER_PAGE, categories)
        slices = pagination.getPageSlice()
        resultsTemplate = render_template(
            "category_list.html", categories=slices, SESSION=login_session, pagination=pagination)
        resultsTemplate += render_template("pages_list.html",
                                           pagination=pagination)
    else:
        resultsTemplate = render_template(
            "error.html",
            message="Sorry we could not find what you were looking for")
    return resultsTemplate


def get_item_list(page):
    """
    gets the list of items for a user, paginates and
    creates a template for display
    """
    if is_admin_loggedin():
        items = catalogDb.get_all_items()
    elif is_someone_Loggedin():
        print login_session['userid']
        items = catalogDb.get_all_items_user(login_session['userid'])
    else:
        items = catalogDb.get_all_items()

    if(len(items) >= 1):
        pagination = cusotmPaginator(page, PER_PAGE, items)
        slices = pagination.getPageSlice()
        resultsTemplate = render_template(
            "items_list.html", items=slices, SESSION=login_session,
            pagination=pagination)
        resultsTemplate += render_template("pages_list.html",
                                           pagination=pagination)
    else:
        resultsTemplate = render_template('error.html',
                                          message="You Have not added any Items yet")
    return resultsTemplate


# def isAdminUserLoggedIn():
    # if login_session['username']

def get_user_list(page):
    """
    gets the list of user, paginates and
    creates a template for display
    """
    users = catalogDb.get_all_user()
    if(len(users) >= 1):
        pagination = cusotmPaginator(page, PER_PAGE, users)
        slices = pagination.getPageSlice()
        resultsTemplate = render_template(
            "users_list.html", users=slices, SESSION=login_session, pagination=pagination)
        resultsTemplate += render_template("pages_list.html",
                                           pagination=pagination)
    else:
        resultsTemplate = render_template("empty_list.html")
    return resultsTemplate


def get_catalog():
    """
     creates a catalog template for display
    """
    parent_categories = catalogDb.get_all_parent_categories()
    sub_categories = catalogDb.get_all_sub_categories()
    latest_items = enumerate(catalogDb.get_latest_items(CUT_OFF_DATE,
                                                        NO_LATEST_ITEMS))
    all_items = enumerate(catalogDb.get_all_items(True))
    return render_template("items_catalog.html",
                           parent_categories=parent_categories,
                           sub_categories=sub_categories,
                           latest_items=latest_items,
                           item_count=NO_LATEST_ITEMS,
                           all_items=all_items)


def get_cataegory_listings(db_category_name):
    """
     creates a catalog template for display
    """

    parent_categories = catalogDb.get_all_parent_categories()
    sub_categories = catalogDb.get_all_sub_categories()
    latest_items = enumerate(catalogDb.get_items_by_category(db_category_name))
    if not latest_items:
        flash("Could not find anything for ", category="info")
    return render_template("items_catalog.html",
                           parent_categories=parent_categories,
                           sub_categories=sub_categories,
                           latest_items=latest_items)


def get_cataegory_item(db_category_name, db_item_name):
    """
    renders the template for an Item in a category
    """
    parent_categories = catalogDb.get_all_parent_categories()
    sub_categories = catalogDb.get_all_sub_categories()
    category_item = catalogDb.get_category_item_by_name(db_category_name,
                                                        db_item_name)
    print category_item
    if not category_item:
        result = render_template('error.html',
                                 message="Oops! We could not serve what you were looking for...")
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
    # category_item = catalogDb.get_category_item_by_name(db_category_name,
    #                                                     db_item_name)
    # print category_item
    # if not category_item:
    #     result = render_template('error.html',
    #                              message="Oops! We could not serve what you were looking for...")
    # else:
    #     result = render_template("category_item_view.html",
    #                              parent_categories=parent_categories,
    #                              sub_categories=sub_categories,
    #                              category_item=category_item)
    return True


def process_admin_login(adminuser):
    """
    sets the admin user information the session
    """
    login_session['username'] = adminuser.name
    login_session['email'] = adminuser.email
    login_session['accountType'] = "ADMIN"
    login_session['userid'] = 1


def is_admin_loggedin():
    """
    returns true if a admin account is logged in
    """
    try:
        acType = login_session['accountType']
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
    """
    try:
        result = login_session['userid'] == item_user
        print "This " + str(login_session['userid']) + str(item_user)
        result = result or is_admin_loggedin()
    except:
        print "exception " + str(item_user) + str(login_session['userid'])
        raise
        result = False
    # app.logger.debug(" verify login " + str(result))
    return result


def other_page_urls(page):
    """
    creates the page url for pagination
    """
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def get_category_name(category_id):
    """
    returns the category name from the cached
    category_list
    """
    result = "Uncategorized"
    try:
        result = login_session['categorylist'][category_id]
    except:
        app.logger.debug("cat list empty category_id" + str(category_id))
        login_session['categorylist'] = update_category_list()
        result = login_session['categorylist'][category_id]

    return result


def format_name_for_url(conversion_string):
    """
    strips the spaces and replaces them with
    - for passing these in the URL
    """
    return conversion_string.replace(" ", '~')


def unformat_name_for_url(conversion_string):
    """
    strips the - and replaces them with
    spaces
    """
    return conversion_string.replace("~", ' ')


# adding required functions to the template system
app.jinja_env.globals['other_page_urls'] = other_page_urls
app.jinja_env.globals['isSomeoneLoggedIn'] = is_someone_Loggedin
app.jinja_env.globals['isAdminLoggedIn'] = is_admin_loggedin
app.jinja_env.globals['verifyOwnerLogin'] = verify_owner_login
app.jinja_env.globals['get_category_name'] = get_category_name
app.jinja_env.globals['format_name_for_url'] = format_name_for_url


def set_page_title(page_name):
    """
    Sets the page title in the session
    """
    login_session['app_name'] = APPLICATION_NAME
    login_session['page_title'] = page_name


@app.route('/', )
@app.route('/catalog')
def catalog():
    set_page_title("Catalog")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_catalog()
    output += render_template('footer.html')
    return output


@app.route('/catalog/<category_name>/items')
def category_listings(category_name):
    """ renders list of items for the category
    """
    set_page_title("Category Items")
    db_category_name = unformat_name_for_url(category_name)
    app.logger.debug("Listing items for " + db_category_name)
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_cataegory_listings(db_category_name)
    output += render_template('footer.html')
    return output


@app.route('/catalog/<category_name>/<item_name>')
def category_item(category_name, item_name):
    """ renders a specific item in the category """
    set_page_title("Items Details")
    db_category_name = unformat_name_for_url(category_name)
    db_item_name = unformat_name_for_url(item_name)
    app.logger.debug("Listing items for " + db_category_name)
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_cataegory_item(db_category_name, db_item_name)
    output += render_template('footer.html')
    return output


@app.route('/categories', defaults={'page': 1})
@app.route('/categories/<int:page>')
def categories(page):
    """
    serves the paginated categories list
    """
    set_page_title("Categories")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_categories_list(page)
    output += render_template('footer.html')
    return output


@app.route('/items', defaults={'page': 1})
@app.route('/items/<int:page>')
def items(page):
    set_page_title("Items")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += get_item_list(page)
    output += render_template('footer.html')
    return output


@app.route('/', defaults={'page': 1})
@app.route('/users', defaults={'page': 1})
@app.route('/users/<int:page>')
def users(page):
    set_page_title("Users")
    output = ''
    output = render_template('header.html', SESSION=login_session)
    try:
        if not is_admin_loggedin():
            output += render_template('error.html',
                                      message="You need to login as administrator")
        else:
            output += get_user_list(page)
    except:
        output += render_template('error.html',
                                  message="Oops Something went wrong")
        raise
    output += render_template('footer.html')
    return output


@app.route('/edituser', defaults={'userid': -1}, methods=['GET', 'POST'])
@app.route('/edituser/<int:userid>', methods=['GET'])
def edit_user(userid):
    form = UserForm(request.form)
    app.logger.debug("Request Method " + request.method)
    app.logger.debug("Form Valid " + str(form.validate()))
    set_page_title("Add User")
    if request.method == 'POST' and form.validate():
        newUser = User()
        form.populate_obj(newUser)
        if newUser.id is not None:
            if catalogDb.update_user_details(newUser):
                flash('User Updated Successful!', category="success")
            else:
                flash('There was an error updating user!', category="danger")
        else:
            flash("User Not Found!", category="info")
        return redirect(url_for('users'))
    if userid is not None and userid >= 0:
        app.logger.debug("User Id" + str(userid))
        tempUser = catalogDb.get_user_by_id(userid)
        form = UserForm(request.form, obj=tempUser)
        set_page_title("Edit User")

    output = render_template('header.html', SESSION=login_session)
    output += render_template('editUser.html', form=form)
    output += render_template('footer.html')
    return output


@app.route('/addEditCategories', defaults={'categoryId': -1},
           methods=['GET', 'POST'])
@app.route('/addEditCategories/<int:categoryId>', methods=['GET'])
def new_category(categoryId):
    """
    serves the request for new category and edit categories
    """
    try:

        form = CategoriesForm(request.form)
        form.parent.choices = [(int(cat.id), cat.name)
                               for cat in catalogDb.get_all_parent_categories()]
        app.logger.debug("categoryId: " + str(categoryId) +
                         " request.method " + request.method)
        set_page_title("Add Category")
        if request.method == 'POST' and form.validate():
            print "in the add update block"
            newCategories = Categories()
            form.populate_obj(newCategories)
            if form.data['id']:
                print "category is [" + newCategories.id + "]"
                catalogDb.update_categories_details(newCategories)
            else:
                print "add category is " + newCategories.id
                newCategories.id = None
                catalogDb.add_categories(newCategories)
            return redirect(url_for('categories'))

        if categoryId is not None and categoryId >= 0:
            app.logger.debug("Showing Category Details")
            categoryX = catalogDb.get_categories_by_id(categoryId)
            form = CategoriesForm(request.form, obj=categoryX)
            form.parent.choices = [(int(cat.id), cat.name)
                                   for cat in catalogDb.get_all_parent_categories()]
            set_page_title("Edit Category")

        output = render_template('header.html', SESSION=login_session)
        output += render_template('addeditCategories.html', form=form)
        output += render_template('footer.html')
    except:
        output = render_template('header.html', SESSION=login_session)
        output += render_template('error.html',
                                  message="Oops Something went wrong")
        output += render_template('footer.html')
        raise

    return output


@app.route('/addEditItem', defaults={'item_id': -1},
           methods=['GET', 'POST'])
@app.route('/addEditItem/<int:item_id>', methods=['GET'])
def new_item(item_id):
    """
    serves the request for new item and edit item
    """
    try:

        form = ItemForm(request.form)
        form.category_id.choices = [(int(cat.id), cat.name)
                                    for cat in catalogDb.get_all_sub_categories()]
        set_page_title("Add Item")

        if request.method == 'POST' and form.validate():
            print "in the add update block"
            newItem = Items()
            form.populate_obj(newItem)
            if form.data['id']:
                print "item is [" + newItem.id + "]"
                catalogDb.update_item_details(newItem)
            else:
                print "add item is " + newItem.id
                newItem.id = None
                newItem.user_id = login_session['userid']
                catalogDb.add_item(newItem)
            return redirect(url_for('items'))

        if item_id is not None and item_id >= 0:
            app.logger.debug("Showing Item Details")
            itemX = catalogDb.get_item_by_id(item_id)
            form = ItemForm(request.form, obj=itemX)
            form.category_id.choices = [(int(cat.id), cat.name)
                                        for cat in catalogDb.get_all_sub_categories()]
            set_page_title("Edit Item")

        output = render_template('header.html', SESSION=login_session)
        output += render_template('addeditItems.html', form=form)
        output += render_template('footer.html')
    except:
        output = render_template('header.html', SESSION=login_session)
        output += render_template('error.html',
                                  message="Oops Something went wrong")
        output += render_template('footer.html')
        raise

    return output


@app.route('/deleteuser')
def delete_user():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "delete user Code"
    output += render_template('footer.html')
    return output


@app.route('/deleteCategories')
def delete_category():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "delete Categories Code"
    output += render_template('footer.html')
    return output


@app.route('/edititem')
def edit_item():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "Edit Puppy Code"
    output += render_template('footer.html')
    return output


@app.route('/deleteitem')
def delete_item():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "delete Puppy Code"
    output += render_template('footer.html')
    return output


@app.route('/login')
def login():
    """
    server the login request for Google
    """

    # check if already logged in
    print str(request)
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
        endpointurl = "already_loggedin.html"
        flash('You are already logged in!', category="warning")
    else:
        endpointurl = "admin_login.html"

    form = AdminLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        admnuser = User()
        form.populate_obj(admnuser)
        chkUser = catalogDb.admin_login(admnuser)
        if chkUser is not None:
            flash("Login Successful!", category="success")
            process_admin_login(chkUser)
            return redirect(url_for('catalog'))
        else:
            flash("Incorrect email and password combination!", category="error")
            return redirect(url_for('admin_login'))

    output = render_template('header.html', SESSION=login_session)
    output += render_template(endpointurl, form=form, SESSION=login_session)
    output += render_template('footer.html')
    return output


@app.route('/gconnect', methods=['POST'])
def gconnect():
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
        response = make_response(json.dumps('Current user is already connected.'),
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
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
    login_session['accountType'] = None
    login_session['userid'] = None
    flash("Logged out successfully !", category="info")
    return redirect(url_for("catalog"))


@app.route('/gdisconnect')
def gdisconnect():
    app.logger.debug("Verifying  the type of account")
    if login_session['accountType'] == "ADMIN":
        return redirect(url_for("admin_logout"))

    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
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


@app.route('/catalog/xml')
def sitemap_xml():
    """ returns the complete catalog in 
    cusotm XML format_name_for_url
    """

    template = get_cataloged_items()
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response

if __name__ == '__main__':
    app.secret_key = APP_SECRET_KEY
    app.debug = True
    app.logger.debug("Starting The Server at port 5000")
    app.run(host='0.0.0.0', port=5000)
