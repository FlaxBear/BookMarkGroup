# from flask import Flask, render_template, redirect, url_for
# from flask_login import LoginManager, login_user, login_required
# from User import User

# app = Flask(__name__)

# app.secret_key = 'secret key'

# login_maneger = LoginManager()
# login_maneger.init_app(app)

# @app.route('/login', methods=['GET'])
# def form():
# 	return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
# 	user = User()
# 	login_user(user)
# 	return redirect(url_for('dashboard'))

# @app.route('/dashboard', methods=['GET'])
# @login_required
# def dashboard():
# 	return render_template('dashboard.html')

# @login_maneger.user_loader
# def load_user(user_id):
# 	return User()

import flask
from flask_login import LoginManager, UserMixin

class User(UserMixin, db.Model):
	pass
	
app = flask.Flask(__name__)
app.secret_key = 'super secret string'


login_maneger = LoginManager()
login_maneger.init_app(app)
login_maneger.login_view = "user.login"

