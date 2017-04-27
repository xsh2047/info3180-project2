"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from models import User, WishlistItem
from forms import UserForm, WishlistForm
from bs4 import BeautifulSoup
from flask_mail import Mail, Message

import urllib2,json
from werkzeug.utils import secure_filename
from functools import wraps
import urllib2, requests, os, hashlib

def validate_user(username, password):
    user = User.query.filter_by(email=username).first()
    if user != None:
        enpass = hashlib.md5(password.encode()).hexdigest()
        return user.password == enpass
    return False
    
def authenticate(func):
    @wraps(func)
    def decorated(*args, **kargs):
        auth = request.authorization
        if not auth or not validate_user(auth.username, auth.password):
            response = make_response("", 401)
            response.headers["WWW-Authenticate"] = 'Basic realm="Login Required"'
            return response
        return func(*args, **kargs)
    return decorated

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/api/users/register', methods=['POST'])
def register():
    response = { "error": 'null', "data": {}, "message": "Success"}
    if request.method == 'POST':
        data = json.loads(request.data)
        # user = User(data['email'], data['fname'], data['lname'], data['password'])
        # file = request.files['picture']
        # if file:
        #     file_folder = app.config['UPLOAD_FOLDER']
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(file_folder, filename))
        #     name = filename
        # else:
        name = 'default.jpg'
        password = hashlib.md5(data['password'].encode()).hexdigest()
        user = User(data['email'], data['name'], password, data['age'], data['gender'])
        db.session.add(user)
        db.session.commit()
        response["data"] = {"user" : user.serialize}
        return jsonify(response)
    response["error"] = "true"
    response["message"] = "Error creating user"
    return jsonify(response)

@app.route('/api/users/login', methods=['POST'])
def login():
    response = { "error": 'null', "data": {}, "message": "Success"}
    if request.method == 'POST':
        data = json.loads(request.data)
        user = User.query.filter_by(email=data['email']).first()
        if user == None:
            response['error'] = 'true'
            response['message'] = 'User does not exist.'
            return jsonify(response)
        elif user.password == hashlib.md5(data['password'].encode()).hexdigest():
            response['data'] = {'user' : user.serialize_many}
            return jsonify(response)
    response['error'] = 'true'
    response['message'] = 'Invalid Password.'
    return jsonify(response)

@app.route('/api/users/<int:userid>/wishlist', methods=['GET', 'POST'])
@authenticate
def wishlist(userid):
    response = { "error": 'null', "data": {}, "message": "Success"}
    user = User.query.get(userid)
    if user == None:
        response['error'] = 'true'
        response['message'] = 'User does not exist.'
        return jsonify(response)
    if request.method == 'POST':
        data = json.loads(request.data)
        wishlistitem = WishlistItem(data['name'], data['thumbnail'], data['url'], data['desc'])
        user.wishlist.append(wishlistitem) 
        db.session.add(user)
        db.session.commit()
        response['data'] = {"item" : wishlistitem.serialize}
        return jsonify(response)
    itemlist = user.wishlist
    if len([i for i in itemlist]) < 1:
         response['error'] = 'true'
         response['message'] = 'No wishlist exists'
    else:
        response['data'] = {"items" : [item.serialize for item in itemlist]}
    return jsonify(response)

@app.route('/api/thumbnails', methods=['GET'])
@authenticate
def thumbnails():
    soup = BeautifulSoup(requests.get(request.args.get('url')).text, "lxml")
    response = { "error": 'null', "data": {"thumbnails": [img.get('src') for img in soup.find_all('img')]}, "message": "Success"}
    return jsonify(response)

@app.route('/api/users/<int:userid>/wishlist/<int:itemid>', methods=['DELETE'])
@authenticate
def deleteitem(userid, itemid):
    response = { "error": 'null', "data": {}, "message": "Success"}
    user = User.query.get(userid)
    if user == None:
        response['error'] = 'true'
        response['message'] = 'User not found'
        return jsonify(response)
    else:
        for item in user.wishlist:
            if item.id == itemid:
                user.wishlist.remove(item)
                db.session.commit()
                return jsonify(response)
    response['error'] = 'true'
    response['message'] = 'Item not found'
    return jsonify(response)
 
@app.route('/api/send/<int:userid>/<emails>')
@authenticate
def send_email(userid, emails):
    user = User.query.get(userid)
    recpts = emails.split(',')
    count = 1
    heading = user.name + "'s Wishlist"
    body = heading + ": \n"
    for item in user.wishlist:
        body += str(count) + ". " + item.name + " - " + item.url + "\n"
        count += 1
    mail = Mail(app)
    msg = Message(heading, sender = user.email, recipients = recpts)
    msg.body = body
    mail.send(msg)
    return "Sent"

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

def uploadfile(file):
    file_folder = app.config['UPLOAD_FOLDER']
    filename = secure_filename(file.filename)
    file_path = os.path.join(file_folder, filename)
    file.save(file_path)
    
    return filename

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
