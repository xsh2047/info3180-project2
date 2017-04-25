"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from models import User, WishlistItem
from forms import UserForm, WishlistForm
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
import urllib2, requests, os

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
        file = request.files['picture']
        if file:
            file_folder = app.config['UPLOAD_FOLDER']
            filename = secure_filename(file.filename)
            file.save(os.path.join(file_folder, filename))
            name = filename
        else:
            name = 'default.jpg'
        data = request.form
        user = User(data['email'], data['name'], data['password'], name, data['age'], data['gender'])
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
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user == None:
            response['error'] = 'true'
            response['message'] = 'User does not exist.'
            return jsonify(response)
        elif user.password == data['password']:
            response['data'] = {'user' : user.serialize_many}
            return jsonify(response)
    response['error'] = 'true'
    response['message'] = 'Invalid Password.'
    return jsonify(response)

@app.route('/api/users/<int:userid>/wishlist', methods=['GET', 'POST'])
def wishlist(userid):
    response = { "error": 'null', "data": {}, "message": "Success"}
    user = User.query.get(userid)
    if user == None:
        response['error'] = 'true'
        response['message'] = 'User does not exist.'
        return jsonify(response)
    if request.method == 'POST':
        data = request.form
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
def thumbnails():
    print urllib2.quote(request.args.get('url'))
    soup = BeautifulSoup(requests.get(request.args.get('url')).text, "lxml")
    response = { "error": 'null', "data": {"thumbnails": [img.get('src') for img in soup.find_all('img')]}, "message": "Success"}
    return jsonify(response)

@app.route('/api/users/<int:userid>/wishlist/<int:itemid>', methods=['DELETE'])
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
