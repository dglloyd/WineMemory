from flask import render_template, flash, redirect, g, url_for, session, request
from app import app, db
from forms import LoginForm, WineForm, PurchaseForm, WineEditForm
from models import User, Wine, Purchase
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

@app.route('/')
@app.route('/index')
def index():
    wine = Wine.query.all()
    return render_template("index.html",
            title = "Main Listing",
            wines = wine,
            page = 'index',
            content = "Stuff will go here")

@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')

    return render_template('login.html',
            title = 'Sign In',
            page = 'login',
            form = form)

@app.route('/wine/new', methods = ['GET','POST'])
def wine_new():
    form = WineForm()
    if form.validate_on_submit():
        date = datetime.now()
        g.wine = Wine()
        g.purchase = Purchase()
        g.wine.name = form.name.data
        g.wine.variety = form.variety.data
        g.wine.year = form.year.data
        g.wine.country = form.country.data
        g.wine.date_entered = date 
        g.wine.description = form.description.data 
        g.wine.notes = form.notes.data 
        db.session.add(g.wine)
        db.session.commit()
        g.purchase.wine_id = g.wine.id
        g.purchase.price = form.price.data
        g.purchase.store = form.store.data
        db.session.add(g.purchase)
        db.session.commit()
        flash('Wine Added')
        return redirect('/index')
    return render_template('wine_form.html',
            title = 'Add New Wine',
            page = 'wine_new',
            form = form)


@app.route('/wine/edit/<id>', methods = ['GET','POST'])
def wine_edit(id=None):
    form = WineEditForm()
    if form.validate_on_submit():
        g.wine = Wine.query.filter_by(id = id).first()
        g.wine.name = form.name.data
        g.wine.variety = form.variety.data
        g.wine.year = form.year.data
        g.wine.country = form.country.data
        g.wine.description= form.description.data
        g.wine.notes = form.notes.data 
        db.session.add(g.wine)
        db.session.commit()
        flash('Wine Added')
        return redirect(url_for('wine_edit', id=id))

    wine = Wine.query.filter_by(id = id).first()
    form.name.data = wine.name
    form.variety.data = wine.variety
    form.year.data = wine.year
    form.country.data = wine.country
    form.description.data = wine.description
    form.notes.data = wine.notes
    return render_template('wine_form.html',
            title = "Edit wine",
            page = 'wine_edit',
            action = 'edit',
            form = form)


@app.route('/wine/show/<id>')
def wine(id):
    wine = Wine.query.filter_by(id = id).first()
    if wine == None:
        flash('Wine ' + id + ' not found.')
        return redirect(url_for('index'))
    return render_template('wine.html',
            title = wine.name,
            page = 'wine',
            wines = [wine])

@app.route('/wine/purchase/new/<id>', methods = ['GET','POST'])
def wine_purchase(id):
    form = PurchaseForm()
    if form.validate_on_submit():
        g.purchase = Purchase()
        g.wine = Wine.query.filter_by(id = id).first()
        g.purchase.wine_id = g.wine.id
        g.purchase.price = form.price.data
        g.purchase.store = form.store.data
        db.session.add(g.purchase)
        db.session.commit()
        return redirect(url_for('wine',id=id))
    if not id:
        flash('Need a wine id')
        return redirect(url_for('index'))
    wine = Wine.query.get(id)
    return render_template('wine_purchase.html',
            title = "New Purchase",
            form = form,
            page = 'wine_purchase',
            wine = wine)

@app.route('/wine/delete/<id>')
def wine_delete(id):
    wine = Wine.query.get(id)
    if not wine:
        flash('No such wine', 'error')
        return redirect(url_for('index'))
    db.session.delete(wine)
    db.session.commit()
    flash('Wine '+wine.name+' deleted.','success')
    return redirect(url_for('index'))

@app.route('/wine/purchase/edit/<id>', methods = ['GET','POST'])
def wine_purchase_edit(id=None):
    form = PurchaseForm()
    if form.validate_on_submit():
        g.purchase = Purchase.query.filter_by(id = id).first()
        g.purchase.store = form.store.data
        g.purchase.price = form.price.data
        db.session.add(g.purchase)
        db.session.commit()
        flash('Wine Added')
        return redirect(url_for('wine', id=g.purchase.wine_id))

    purchase = Purchase.query.filter_by(id = id).first()
    form.store.data = purchase.store
    form.price.data = purchase.price
    return render_template('wine_form.html',
            title = "Edit wine",
            page = 'wine_edit',
            action = 'edit',
            form = form)

@app.route('/wine/purchase/delete/<id>')
def wine_purchase_delete(id):
    purchase = Purchase.query.get(id)
    if not purchase:
        flash('No such purchase', 'error')
        return redirect(url_for('index'))
    db.session.delete(purchase)
    db.session.commit()
    flash('Purchase from '+purchase.store+' for '+purchase.price+' deleted.','success')
    return redirect(url_for('index'))


