from . import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique = True)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
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

    def __init__(self, email=None, name=None, password=None, age=None, gender=None):
        self.email = email
        self.name = name
        self.password = password
        self.age = age
        self.gender = gender
        self.wishlist = []

    def __repr__(self):
        return '<User %r>' % (self.id)
        
    @property
    def serialize(self):
       return {
           'id'                 : self.id,
           'email'              : self.email,
           'name'               : self.name,
           'age'                : self.age,
           'gender'             : self.gender,
           'profile_created_on' : self.created
       }
       
    @property
    def serialize_many(self):
       return {
           'id'     : self.id,
           'name'  : self.name,
           'email' : self.email
       }

class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(255))
    url = db.Column(db.String(255))
    thumbnail = db.Column(db.String(255))
    
    def __init__(self, name=None, thumbnail=None, url=None, description=None):
        self.name = name
        self.thumbnail = thumbnail
        self.url = url
        self.description = description
        
    def __repr__(self):
        return '<Item %r>' % (self.id)
        
    @property
    def serialize(self):
       return {
           'id'             : self.id,
           'title'          : self.name,
           'description'    : self.description,
           'thumbnail_url'  : self.thumbnail,
           'url'            : self.url
       }