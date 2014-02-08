from flask import render_template, flash, redirect, g, url_for, session, request
from app import app, db
from forms import LoginForm, WineForm
from models import User, Wine
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

@app.route('/')
@app.route('/index')
def index():
    wine = Wine.query.all()
    return render_template("index.html",
            title = "Main Listing",
            wines = wine,
            content = "Stuff will go here")

@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')

    return render_template('login.html',
            title = 'Sign In',
            form = form)

@app.route('/wine/new', methods = ['GET','POST'])
def wine_new():
    form = WineForm()
    if form.validate_on_submit():
        date = datetime.now()
        g.wine = Wine()
        g.wine.name = form.name.data
        g.wine.variety = form.variety.data
        g.wine.year = form.year.data
        g.wine.country = form.country.data
        g.wine.date_entered = date 
        db.session.add(g.wine)
        db.session.commit()
        flash('Wine Added')
        return redirect('/index')
    return render_template('wine_form.html',
            title = 'Add New Wine',
            form = form)


@app.route('/wine/edit/<id>', methods = ['GET','POST'])
def wine_edit(id=None):
    form = WineForm()
    if form.validate_on_submit():
        g.wine = Wine()
        g.wine.name = form.name.data
        g.wine.variety = form.variety.data
        g.wine.year = form.year.data
        g.wine.country = form.country.data
        g.wine.price = form.price.data
        db.session.add(g.wine)
        db.session.commit()
        flash('Wine Added')
        return redirect(url_for('wine_edit', id=id))

    wine = Wine.query.filter_by(id = id).first()
    form.name.data = wine.name
    form.variety.data = wine.variety
    form.year.data = wine.year
    form.country.data = wine.country
    form.price.data = wine.price
    return render_template('wine_form.html',
            title = "Edit wine",
            form = form)


@app.route('/wine/show/<id>')
def wine(id):
    wine = Wine.query.filter_by(id = id).first()
    if wine == None:
        flash('Wine ' + id + ' not found.')
        return redirect(url_for('index'))
    return render_template('wine.html',
            title = wine.name,
            wines = [wine])
