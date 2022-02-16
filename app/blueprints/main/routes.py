from .forms import AshKetchum
from app.models import Pokedata, Userpokedata, User
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from .import bp as main

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/poke_search', methods=['GET', 'POST'])
@login_required
def poke_search():
    form = AshKetchum()   
    if request.method == 'POST' and form.validate_on_submit():
        enter_field = request.form.get('enter_field')
        url = f"https://pokeapi.co/api/v2/pokemon/{enter_field}"
        response = requests.get(url)
        if response.ok:
            poke = response.json()
            poke_dict = {
            "name":poke['forms'][0]['name'],
            "hp":poke['stats'][0]['base_stat'],
            "defense":poke['stats'][2]['base_stat'],
            "attack":poke['stats'][1]['base_stat'],
            "ability_1":poke['abilities'][0]['ability']['name'],
            "ability_2":response.json()['abilities'][1]['ability']['name'] if len(response.json()['abilities']) > 1 else "",               
            "sprite": poke['sprites']['front_shiny']
            }
            if not Pokedata.exists(poke_dict["name"]):
                add_poke = Pokedata()
                add_poke.from_dict(poke_dict)
                add_poke.save()  
        
            user = current_user
            user.add_to_team(Pokedata.exists(poke_dict["name"]))

            return render_template('poke_search.html.j2', form=form, pokemon = poke_dict)
        else:
            error_message = "Pokemon not found."
            return render_template('poke_search.html.j2', error = error_message, form=form)
    return render_template('poke_search.html.j2', form=form)

@main.route('/edit_team', methods=['GET', 'POST'])
@login_required
def edit_team():
    display = current_user.team
    return render_template('edit_team.html.j2', team=display)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_pokemon(id):
    poke = Userpokedata.query.get((current_user.id, id))
    poke.remove_pokemon()
    
    flash('Your pokemon has been removed', 'warning')
    return redirect(url_for('main.edit_team'))

@main.route('/view_opponents', methods=['GET', 'POST'])
@login_required
def view_opponents():
    show = User.query.all()
    
    return render_template('view_opponents.html.j2', show=show)

@main.route('/battle/<int:id>', methods=['GET', 'POST'])
@login_required
def battle(id):
    user = User.query.get(id)
    if int(current_user.hit_points()) > int(user.hit_points()):
        flash('You win! Congrats!', 'success')
    elif int(current_user.hit_points()) < int(user.hit_points()):
        flash('You lose!', 'danger')
    else:
        flash('Issa tie! Play again!', 'warning')
    return redirect(url_for('main.view_opponents'))

# add buttons to battle from view opponents since i'll have current and opponents id
# click battle button to look through the user table to access each user's hps
# create function to say if current_user hp > opponent's hp, current user wins
# elif hp < opponent's hp
# else issa tie
   
