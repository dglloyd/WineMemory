from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    wines = db.relationship('Wine', backref = 'author', lazy = 'dynamic')
    def __repr__(self):
        return '<User %r>' % (self.name)

class Wine(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)
    variety = db.Column('variety', db.String(50))
    year = db.Column('year', db.Integer)
    country = db.Column('country', db.String(50))
    date_entered = db.Column('date_entered', db.DateTime)
    entered_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    purchases = db.relationship("Purchase", backref = db.backref('purchases', order_by=id))
    def __repr__(self):
        return '<Wine %r>' % (self.name)

class Purchase(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    price = db.Column('price',db.Numeric(precision=2))
    store = db.Column('store',db.String())
    wine_id = db.Column(db.Integer, db.ForeignKey('wine.id'))
    wine = db.relationship("Wine", backref=db.backref('wine', order_by=id))
    def __repr__(self):
        return '<Purchase %r>' % (self.name)
