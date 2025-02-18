from app import app
from flask import render_template
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from flask import Flask, url_for, redirect, flash


# HOME PAGE
@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title='Eye Tracker Home')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def logIn():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
        	next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


# RECORD PASSWORD (GRID)
@app.route('/recording')
def recording():
    return render_template('recording.html', title='Record Password')


# LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))