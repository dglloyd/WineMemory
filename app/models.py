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
    price = db.Column('price',db.Numeric(precision=2))
    def __repr__(self):
        return '<Wine %r>' % (self.name)
