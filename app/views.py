from flask import render_template, flash, redirect, g, url_for, session, request, jsonify, Response
from functools import wraps
from app import app, db, bcrypt
from forms import LoginForm, WineForm, PurchaseForm, WineEditForm, RegisterForm
from models import User, Wine, Purchase, WineRating
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from beaker.middleware import SessionMiddleware
import json

# decoration
def requires_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.has_key('user'):
            g.user = session['user']
        else:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@app.route('/index')
@requires_authentication
def index():
    wine = Wine.query.outerjoin(Purchase).order_by(Purchase.drank == True).all()
    return render_template("index.html",
                           title = "Main Listing",
                           wines = wine,
                           page = 'index',
                           user = g.user)

@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        g.user =  User.query.filter_by(name = form.name.data).first()
        if g.user:
            if bcrypt.check_password_hash(g.user.password,form.password.data):
                session['user'] = g.user
                flash("Logged In","success")
                return redirect(url_for('index'))
            else:
                flash("Incorrect username or password", "danger")
                return redirect(url_for('login'))
        else:
            flash("Incorrect username or password", "danger")
            return redirect(url_for('login'))
    return render_template('login.html',
                           title = 'Sign In',
                           page = 'login',
                           form = form)                          

@app.route('/logout', methods = ['GET','POST'])
def logout():
    session.delete()
    return redirect(url_for('login'))

@app.route('/wine/new', methods = ['GET','POST'])
@requires_authentication
def wine_new():
    form = WineForm()
    if form.validate_on_submit():
        date = datetime.now()
        g.wine = Wine()
        g.purchase = Purchase()
        g.rating= WineRating()
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
        g.purchase.drank = form.drank.data
        db.session.add(g.purchase)
        db.session.commit()
        g.rating.wine_id = g.wine.id
        g.rating.rating = form.rating.data
        db.session.add(g.rating)
        db.session.commit()

        flash('Wine Added', 'success')
        return redirect('/index')
    return render_template('wine_form.html',
                           title = 'Add New Wine',
                           page = 'wine_new',
                           form = form,
                           user = g.user)


@app.route('/wine/edit/<id>', methods = ['GET','POST'])
@requires_authentication
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
        flash('Wine Saved', 'success')
        return redirect(url_for('wine', id=id))

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
                           form = form,
                           user = g.user)


@app.route('/wine/show/<id>')
@requires_authentication
def wine(id):
    wine = Wine.query.filter_by(id = id).first()
    if wine == None:
        flash('Wine ' + id + ' not found.', 'danger')
        return redirect(url_for('index'))
    return render_template('wine.html',
                           title = wine.name,
                           page = 'wine',
                           wines = [wine],
                           user = g.user)

@app.route('/wine/purchase/new/<id>', methods = ['GET','POST'])
@requires_authentication
def wine_purchase(id):
    form = PurchaseForm()
    if form.validate_on_submit():
        g.purchase = Purchase()
        g.wine = Wine.query.filter_by(id = id).first()
        g.purchase.wine_id = g.wine.id
        g.purchase.price = form.price.data
        g.purchase.store = form.store.data
        g.purchase.drank = form.drank.data
        db.session.add(g.purchase)
        db.session.commit()
        flash('Purchase for '+g.wine.name+' added','success')
        return redirect(url_for('wine',id=id))
    if not id:
        flash('Need a wine id', 'warning')
        return redirect(url_for('index'))
    wine = Wine.query.get(id)
    return render_template('wine_purchase.html',
                           title = "New Purchase",
                           form = form,
                           page = 'wine_purchase',
                           wine = wine,
                           user = g.user)

@app.route('/wine/delete/<id>')
@requires_authentication
def wine_delete(id):
    wine = Wine.query.get(id)
    if not wine:
        flash('No such wine', 'danger')
        return redirect(url_for('index'))
    db.session.delete(wine)
    db.session.commit()
    flash('Wine '+wine.name+' deleted.','success')
    return redirect(url_for('index'))

@app.route('/wine/purchase/edit/<id>', methods = ['GET','POST'])
@requires_authentication
def wine_purchase_edit(id=None):
    form = PurchaseForm()
    if form.validate_on_submit():
        g.purchase = Purchase.query.filter_by(id = id).first()
        g.purchase.store = form.store.data
        g.purchase.price = form.price.data
        g.purchase.drank = form.drank.data
        db.session.add(g.purchase)
        db.session.commit()
        flash('Purchase edited', 'success')
        return redirect(url_for('wine', id=g.purchase.wine_id))

    purchase = Purchase.query.filter_by(id = id).first()
    form.store.data = purchase.store
    form.price.data = purchase.price
    form.drank.data = purchase.drank
    return render_template('wine_form.html',
                           title = "Edit wine",
                           page = 'wine_edit',
                           action = 'edit',
                           form = form,
                           user = g.user)

@app.route('/wine/purchase/delete/<id>')
@requires_authentication
def wine_purchase_delete(id):
    purchase = Purchase.query.get(id)
    if not purchase:
        flash('No such purchase', 'danger')
        return redirect(url_for('index'))
    db.session.delete(purchase)
    db.session.commit()
    flash('Purchase from '+purchase.store+' for $'+'{0:.2f}'.format(purchase.price)+' deleted.','success')
    return redirect(url_for('wine',id=purchase.wine_id))


@app.route('/autocomplete/store/')
@requires_authentication
def autocomplete_store():
    purchase = Purchase()
    results = []
    search = request.args.get('search[term]')
    print search
    for store in Purchase.query.filter(Purchase.store.ilike(search + '%')).all():
        results.append(store.store)

    return Response(json.dumps(list(set(results))),  mimetype='application/json')


@app.route('/autocomplete/variety/')
@requires_authentication
def autocomplete_variety():
    wine = Wine()
    results = []
    search = request.args.get('search[term]')
    print search
    for wine in Wine.query.filter(Wine.variety.ilike(search + '%')).all():
        results.append(wine.variety)

    results = list(set(results))
    if results:
        return Response(json.dumps(list(set(results))),  mimetype='application/json')
    return json.dumps([])



@app.route('/wine/purchase/dupe/<id>')
@requires_authentication
def wine_purchase_dupe(id):
    if not id:
        flash('Need a wine id', 'warning')
        return redirect(url_for('wine',id=wine_id))
    g.purchase = Purchase()
    wine = Wine()
    g.old_purchase = Purchase()
    g.old_purchase = Purchase.query.filter_by(id = id).first()
    g.purchase.wine_id = g.old_purchase.wine_id
    g.purchase.price = g.old_purchase.price
    g.purchase.store = g.old_purchase.store
    wine = Wine.query.filter_by(id = g.old_purchase.wine_id).first()
    db.session.add(g.purchase)
    db.session.commit()
    flash('Purchase for '+wine.name+' duplicated','success')
    return redirect(url_for('wine',id=wine.id))

@app.route('/wine/puchase/drink/<id>')
@requires_authentication
def wine_purchase_drink(id):
    if not id:
        flash('Need a wine id', 'warning')
        return redirect(url_for('wine',id=wine_id))
    g.purchase = Purchase()
    wine = Wine()
    g.purchase = Purchase.query.filter_by(id = id).first()
    wine = Wine.query.filter_by(id = g.purchase.wine_id).first()
    if g.purchase.drank == True:
        g.purchase.drank = False
    else:
        g.purchase.drank = True

    db.session.add(g.purchase)
    db.session.commit()
    flash('Purchase for '+wine.name+' marked as '+ ('drank' if g.purchase.drank else 'not drank'),'success')
    return redirect(url_for('wine',id=wine.id))

@app.route('/cellar/list')
@requires_authentication
def cellar_list():
    wines = Wine()
    counted_list = []
    wines = db.session.query(Wine, db.func.count(Wine.id)).outerjoin(Purchase).filter(Purchase.drank == False).group_by(Wine.id) 
    # Fix this, i hate it, why doesn't the ORM let me get count cleanly.
    for wine, count in wines:
        wine.count = count
        counted_list.append(wine)
        return render_template("cellar.html",
                               title = "Cellar Listing",
                               wines = counted_list,
                               page = 'cellar')

@app.route('/user/new', methods = ['GET','POST'])
def register():
    form = RegisterForm()
    g.user = User()
    if form.validate_on_submit():
        g.user.name = form.name.data
        g.user.password = bcrypt.generate_password_hash(form.password.data)
        g.user.email = form.email.data
        db.session.add(g.user)
        db.session.commit()
        flash("Successfully registered","success")
        return redirect(url_for("index"))
    return render_template("register.html",
                           form = form,
                           title = "Register",
                           page = 'register')
