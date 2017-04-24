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

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/api/users/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.form
        user = User(data['email'], data['fname'], data['lname'], data['password'])
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('home'))
    flash('Error creating user')
    return url_for('home')

@app.route('/api/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.form
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
    if request.method == 'POST':
        data = request.form
        wishlistitem = WishlistItem(data['name'], userid, data['thumbnail'])
        db.session.add(wishlistitem)
        db.session.commit()
        return jsonify(status = 'success')
    itemlist = User.query.get(userid).wishlist
    return jsonify(wishlist = [item.serialize for item in itemlist])

@app.route('/api/thumbnails', methods=['GET'])
def thumbnails():
    """Render the website's about page."""
    return render_template('thumbnails.html')

@app.route('/api/users/<int:userid>/wishlist/<int:itemid>', methods=['DELETE'])
def deleteitem(userid, itemid):
    """Render the website's about page."""
    return render_template('wishlist.html')

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
