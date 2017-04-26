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
import urllib2,json

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/api/users/register', methods=['POST'])
def register():
    if request.method == 'POST':
        
        data = json.loads(request.data)
        user = User(data['email'], data['fname'], data['lname'], data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'status' : 'success', 'message' : 'User created successfully', 'user' : user.serialize})
    return jsonify({'status' : 'error', 'message' : 'Error creating user'})

@app.route('/api/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        user = User.query.filter_by(email=data['email']).first()
        response = {'status' : 'error', 'message' : 'Unknown', 'user' : 'null'}
        if user == None:
            response['message'] = 'User does not exist.'
            return jsonify(response)
        elif user.password == data['password']:
            response['status'] = 'success'
            response['message'] = 'User logged in successfully.'
            response['user'] = user.serialize
            return jsonify(response)
    response['message'] = 'Invalid Password.'
    return jsonify(response)

@app.route('/api/users/<int:userid>/wishlist', methods=['GET', 'POST'])
def wishlist(userid):
    user = User.query.get(userid)
    if user == None:
        return jsonify({'status' : 'error', 'message' : 'User does not exist.'})
    if request.method == 'POST':
        data = json.loads(request.data)
        wishlistitem = WishlistItem(data['name'], data['thumbnail'])
        # fix shit below
        user.wishlist.append(wishlistitem) 
        db.session.add(user)
        db.session.commit()
        return jsonify(status = 'success')

    itemlist = user.wishlist
    print itemlist[0].user
    return jsonify(wishlist = [item.serialize for item in itemlist])

@app.route('/api/thumbnails', methods=['GET'])
def thumbnails():
    print urllib2.quote(requests.args.get('url'))
    soup = BeautifulSoup(requests.get(request.args.get('url')).text, "lxml")
    return jsonify(thumbnails = [img.get('src') for img in soup.find_all('img')])

@app.route('/api/users/<int:userid>/wishlist/<int:itemid>', methods=['DELETE'])
def deleteitem(userid, itemid):
    response = {'status' : 'error', 'message' : 'Unknown'}
    user = User.query.get(userid)
    if user == None:
        response['message'] = 'User not found'
        return jsonify(response)
    else:
        for item in user.wishlist:
            if item.id == itemid:
                user.wishlist.remove(item)
                db.session.commit()
                response = {'status' : 'success', 'message' : 'Item deleted successfully'}
                return jsonify(response)
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
