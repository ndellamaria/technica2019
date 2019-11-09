# main.py

from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from .models import User, Transaction
from . import db
import random
import math

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	total = current_user.total
	name = current_user.name
	nonprofit = current_user.nonprofit
	orgs = Transaction.query.filter_by(user_id=current_user.id).all()
	if 'category' in request.args and 'price' in request.args:
		payment = {
		'category': request.args['category'],
		'price' : request.args['price']
		}
	else:
		payment = None
	# orgs = Transaction.query.all()
	return render_template('profile.html', nonprofit=nonprofit,total=round(total,2), name=name, orgs=orgs, payment=payment)

@main.route('/breakdown')
@login_required
def breakdown():
	total = current_user.total
	name = current_user.name
	nonprofit = current_user.nonprofit
	orgs = Transaction.query.filter_by(user_id=current_user.id).all()
	# orgs = Transaction.query.all()
	return render_template('breakdown.html', total=round(total,2), name=name, orgs=orgs, nonprofit=nonprofit)

@main.route('/nonprofit')
@login_required
def nonprofit():
	return render_template('nonprofit.html')

@main.route('/nonprofit', methods=['POST'])
@login_required
def nonprofit_post():
	nonprofit = request.form.get('nonprofit')

	user = current_user
	user.nonprofit = nonprofit
	db.session.commit()

	transaction = Transaction.query.filter_by(name=nonprofit, user_id=user.id).first()
	if not transaction: 
		new_transaction = Transaction(name=nonprofit, user_id=user.id, amt=0)
		db.session.add(new_transaction)
		db.session.commit()
		# return render_template('breakdown.html',name=nonprofit)
	# orgs = Transaction.query.all()
	# return render_template('breakdown.html',name=transaction.name, orgs=orgs)
	return redirect(url_for('main.profile'))

@main.route('/payment')
@login_required
def payment():
	categories = ['Food', 'Entertainment', 'Clothes', 'Home Improvement', 'Books', 'School Supplies', 'Camping Gear']
	price = round(random.uniform(10,100), 2)
	diff = float(math.ceil(price)-price)
	user = current_user
	transaction = Transaction.query.filter_by(name=user.nonprofit, user_id=user.id).first()
	transaction.amt+=diff
	user.total+=diff
	db.session.commit()
	category = random.choice(categories)
	return redirect(url_for('main.profile', category=category, price=price))