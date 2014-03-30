from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(60), index = True)
    wines = db.relationship('Wine', backref = 'author', lazy = 'dynamic')
    purchases = db.relationship('Purchase', backref = 'user_purchases', lazy = 'dynamic')
    ratings = db.relationship('WineRating', backref = 'user_ratings', lazy = 'dynamic')
    def __repr__(self):
        return '<User %r>' % (self.name)

class Wine(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)
    variety = db.Column('variety', db.String(50))
    year = db.Column('year', db.Integer)
    country = db.Column('country', db.String(50))
    region = db.Column('region', db.String(50))
    date_entered = db.Column('date_entered', db.DateTime)
    entered_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    purchases = db.relationship("Purchase", backref = db.backref('purchases', order_by="Purchase.drank"), cascade="all, delete, delete-orphan")
    ratings = db.relationship("WineRating", backref = db.backref('ratings', order_by="WineRating.rating"), cascade="all, delete, delete-orphan")
    def __repr__(self):
        return '<Wine %r>' % (self.name)

class WineRating(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    rating = db.Column('rating', db.Integer, default=-1)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref('owner'))
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'))
    wine = db.relationship("Wine", backref=db.backref('wine_rating', order_by=rating))
    date_entered = db.Column('date_entered', db.DateTime)
    def __repr__(self):
        return '<WineRating %r>' % (self.id)

class Purchase(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    price = db.Column('price',db.Numeric(precision=2))
    store = db.Column('store',db.String())
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'))
    drank = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref('user'))
    wine = db.relationship("Wine", backref=db.backref('wine', order_by=drank))
    date_entered = db.Column('date_entered', db.DateTime)
    def __repr__(self):
        return '<Purchase %r>' % (self.id)
