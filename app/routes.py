# from app import app
# from .forms import AshKetchum, LoginForm, RegisterForm
# from flask import render_template, request, flash, url_for, redirect
# from .models import User
# from flask_login import login_user, current_user, logout_user, login_required
# import requests

# @app.route('/', methods=['GET'])
# @login_required
# def index():
#     return render_template('index.html.j2')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if request.method=='POST' and form.validate_on_submit():
#         email = request.form.get('email').lower()   
#         password = request.form.get('password')
#         u = User.query.filter_by(email=email).first()
#         if u and u.check_hashed_password(password):
#             login_user(u)
#             flash('Welcome to Pokemon Paradise!','success')
#             return redirect(url_for('index'))
#         flash('Incorrect Email Address/Password','danger')
#         return render_template('login.html.j2',form=form)
#     return render_template('login.html.j2',form=form)

# @app.route('/logout')
# @login_required
# def logout():
#     if current_user:
#         logout_user()
#         flash('You\'re logged out', 'warning')
#         return redirect(url_for('login'))

# @app.route('/register', methods = ['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if request.method =='POST' and form.validate_on_submit():
#         try:
#             new_user_data = {
#                 "first_name":form.first_name.data.title(),
#                 "last_name":form.last_name.data.title(),
#                 "email":form.email.data.lower(),
#                 "password":form.password.data
#             }
#             new_user_object = User()
#             new_user_object.from_dict(new_user_data)
#             new_user_object.save()
#         except:
#             flash('There was an unexpected error; try again.','danger')
#             return render_template('register.html.j2', form = form)
#         flash('You\'re registered!', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html.j2', form = form)

# @app.route('/poke_search', methods=['GET', 'POST'])
# @login_required
# def poke_search():
#     form = AshKetchum()   
#     if request.method == 'POST' and form.validate_on_submit():
#         enter_field = request.form.get('enter_field')
#         url = f"https://pokeapi.co/api/v2/pokemon/{enter_field}"
#         response = requests.get(url)
#         if response.ok:
#             poke = response.json()
#             poke_dict = {
#             "name":poke['forms'][0]['name'],
#             "hp":poke['stats'][0]['base_stat'],
#             "defense":poke['stats'][2]['base_stat'],
#             "attack":poke['stats'][1]['base_stat'],
#             "ability_1":poke['abilities'][0]['ability']['name'],
#             "ability_2":response.json()['abilities'][1]['ability']['name'] if len(response.json()['abilities']) > 1 else "",               
#             "sprite": poke['sprites']['front_shiny']
#             }
#             return render_template('poke_search.html.j2', form=form, pokemon = poke_dict)
#         else:
#             error_message = "Pokemon not found."
#             return render_template('poke_search.html.j2', error = error_message, form=form)
#     return render_template('poke_search.html.j2', form=form)