from . import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))
    wishlist = db.relationship('WishlistItem', backref="user", cascade="all, delete-orphan" , lazy='dynamic')
    created = db.Column(db.DateTime, default=datetime.datetime.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __init__(self, email=None, fname=None, lname=None, password=None):
        self.email = email
        self.firstname = fname
        self.lastname = lname
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.id)
        
    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'username' : self.email,
           'firstname': self.firstname,
           'lastname' : self.lastname,
           'profile_created_on' : self.created
       }
       
    @property
    def serialize_many(self):
       return {
           'id'         : self.id,
           'username' : self.email
       }

class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    thumbnail = db.Column(db.String(80))
    
    def __init__(self, name=None, user=None, thumbnail=None):
        self.name = name
        self.user = user
        self.thumbnail = thumbnail
        
    def __repr__(self):
        return '<Item %r>' % (self.id)
        
    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'name'       : self.name,
           'user'       : self.user,
           'thumbnail'  : self.thumbnail
       }