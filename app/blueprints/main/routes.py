from .forms import AshKetchum
from flask import render_template, request
from flask_login import login_required
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
            return render_template('poke_search.html.j2', form=form, pokemon = poke_dict)
        else:
            error_message = "Pokemon not found."
            return render_template('poke_search.html.j2', error = error_message, form=form)
    return render_template('poke_search.html.j2', form=form)