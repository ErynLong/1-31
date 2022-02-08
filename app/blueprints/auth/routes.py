from .forms import LoginForm, RegisterForm
from flask import render_template, request, flash, url_for, redirect
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from .import bp as auth

@auth.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email = request.form.get('email').lower()   
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Pokemon Paradise!','success')
            return redirect(url_for('main.index'))
        flash('Incorrect Email Address/Password','danger')
        return render_template('login.html.j2',form=form)
    return render_template('login.html.j2',form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You\'re logged out', 'warning')
        return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method =='POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash('There was an unexpected error; try again.','danger')
            return render_template('register.html.j2', form = form)
        flash('You\'re registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html.j2', form = form)