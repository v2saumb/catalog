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
from os import curdir, sep, pardir
from src.catalogdb.database_setup import Shelter, Puppy, User, Base
from src.catalogutils.db_interface import catalog_interface
from src.catalogutils.custompagination import cusotmPaginator
from src.catalogutils.catalogforms import UserForm, AdminLoginForm
# IMPORTS FOR oAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
DATABASE_FILEPATH = curdir + sep + 'src/catalogdb/animalshelter.db'
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

CLIENT_ID = json.loads(
    open(GOOGLE_FILE, 'r').read())['web']['client_id']
APPLICATION_NAME = "Animal Shelter Test App"


def getShelterList(page):
    """
    returns the shelter list template
    """
    resultsTemplate = ""
    shelters = catalogDb.getAllShelters()
    if(len(shelters) >= 1):
        pagination = cusotmPaginator(page, PER_PAGE, shelters)
        slices = pagination.getPageSlice()
        resultsTemplate = render_template(
            "shelter_list.html", shelters=slices, SESSION=login_session, pagination=pagination)
        resultsTemplate += render_template("pages_list.html",
                                           pagination=pagination)
    else:
        resultsTemplate = render_template("empty_list.html")
    return resultsTemplate


def getPuppyList(page):
    puppies = catalogDb.getAllPuppies()
    if(len(puppies) >= 1):
        pagination = cusotmPaginator(page, PER_PAGE, puppies)
        slices = pagination.getPageSlice()
        resultsTemplate = render_template(
            "puppies_list.html", puppies=slices, SESSION=login_session, pagination=pagination)
        resultsTemplate += render_template("pages_list.html",
                                           pagination=pagination)
    else:
        resultsTemplate = render_template("empty_list.html")
    return resultsTemplate


# def isAdminUserLoggedIn():
    # if login_session['username']

def getUserList(page):
    users = catalogDb.getAllUser()
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


def other_page_urls(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['other_page_urls'] = other_page_urls


@app.route('/', defaults={'page': 1})
@app.route('/shelters', defaults={'page': 1})
@app.route('/shelters/<int:page>')
def shelters(page):
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += getShelterList(page)
    output += render_template('footer.html')
    return output


@app.route('/puppies', defaults={'page': 1})
@app.route('/puppies/<int:page>')
def puppies(page):
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += getPuppyList(page)
    output += render_template('footer.html')
    return output


@app.route('/', defaults={'page': 1})
@app.route('/users', defaults={'page': 1})
@app.route('/users/<int:page>')
def users(page):
    output = ''
    output = render_template('header.html', SESSION=login_session)
    try:
        output += getUserList(page)
    except:
        output += render_template('error.html')
        raise
    output += render_template('footer.html')
    return output


@app.route('/edituser', defaults={'userid': -1}, methods=['GET', 'POST'])
@app.route('/edituser/<int:userid>', methods=['GET'])
def edit_user(userid):
    form = UserForm(request.form)
    app.logger.debug("Request Method " + request.method)
    app.logger.debug("Form Valid " + str(form.validate()))
    if request.method == 'POST' and form.validate():
        newUser = User()
        form.populate_obj(newUser)
        if newUser.id is not None:
            if catalogDb.updateUserDetails(newUser) == True:
                flash('User Updated Successful!')
            else:
                flash('There was an error updating user!')
        else:
            flash("User Not Found!")
        return redirect(url_for('users'))
    if userid is not None and userid >= 0:
        app.logger.debug("User Id" + str(userid))
        tempUser = catalogDb.getUserById(userid)
        form = UserForm(request.form, obj=tempUser)

    output = render_template('header.html', SESSION=login_session)
    output += render_template('editUser.html', form=form)
    output += render_template('footer.html')
    return output


@app.route('/addEditShelter', defaults={'shelterId': -1}, methods=['GET', 'POST'])
@app.route('/addEditShelter/<int:shelterId>', methods=['GET'])
def new_shelter(shelterId):
    form = ShelterForm(request.form)
    print request.method
    print form.validate()
    if request.method == 'POST' and form.validate():
        newShelter = Shelter()
        form.populate_obj(newShelter)
        if newShelter.id is not None:
            catalogDb.updateShelterDetails(newShelter)
        else:
            catalogDb.addShelter(newShelter)

        return redirect(url_for('shelters'))
    if shelterId is not None and shelterId >= 0:
        shelterX = catalogDb.getShelterById(shelterId)
        form = ShelterForm(request.form, obj=shelterX)

    output = render_template('header.html', SESSION=login_session)
    output += render_template('addeditShelter.html', form=form)
    output += render_template('footer.html')
    return output


@app.route('/deleteuser')
def delete_user():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "delete user Code"
    output += render_template('footer.html')
    return output


@app.route('/deleteShelter')
def delete_shelter():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "delete Shelter Code"
    output += render_template('footer.html')
    return output


@app.route('/editPuppy')
def edit_puppy():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "Edit Puppy Code"
    output += render_template('footer.html')
    return output


@app.route('/deletePuppy')
def delete_puppy():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "delete Puppy Code"
    output += render_template('footer.html')
    return output


@app.route('/addPuppy')
def new_puppy():
    output = ''
    output = render_template('header.html', SESSION=login_session)
    output += "New Puppy Code"
    output += render_template('footer.html')
    return output


@app.route('/login')
def login():
    """
    server the login request for Google
    """

    # check if already logged in
    if login_session['username'] is not None:
        endpointurl = "already_loggedin.html"
        flash('You are already logged in!')
    else:
        endpointurl = "login.html"

    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    login_session['state'] = state

    output = render_template('loginheader.html', STATE=state)
    output += render_template(endpointurl, STATE=state, SESSION=login_session)
    output += render_template('loginfooter.html', STATE=state)
    return output


@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    """
    serves the admin user login
    """
    form = AdminLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        admnuser = User()
        form.populate_obj(admnuser)
        chkUser = catalogDb.adminlogin(admnuser)
        if chkUser is not None:
            flash("Login Successful!")
            processAdminLogin(chkUser)
            return redirect(url_for('shelters'))
        else:
            flash("Incorrect email and password combination!")
            return redirect(url_for('admin_login'))

    output = render_template('header.html', SESSION=login_session)
    output += render_template('admin_login.html', form=form)
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
    catalogDb.addUser(newUser)
    output = ""
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
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
    return redirect(url_for("shelters"))


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
        flash('You have Been Successfully Logged Out.')
        return redirect(url_for("shelters"))
    else:

        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def processAdminLogin(adminuser):
    """
    sets the admin user information the session
    """
    login_session['username'] = adminuser.name
    login_session['email'] = adminuser.email
    login_session['accountType'] = "ADMIN"

if __name__ == '__main__':
    app.secret_key = 'thisisthesecretkey'
    app.debug = True
    app.logger.debug("Starting The Server at port 5000")
    app.run(host='0.0.0.0', port=5000)
