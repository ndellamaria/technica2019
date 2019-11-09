# main.py

from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from .models import User, Transaction
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	total = current_user.total
	name = current_user.name
	orgs = Transaction.query.filter_by(user_id=current_user.id).all()
	return render_template('profile.html', total=total, name=name, orgs=orgs)

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

	transaction = Transaction.query.filter_by(name=nonprofit, user_id=user.id)
	if not transaction: 
		new_transaction = Transaction(name=nonprofit, user_id=user.id, amt=0)
		db.session.add(new_transaction)
		db.session.commit()

	return redirect(url_for('main.profile'))

