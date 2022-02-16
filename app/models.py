from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class Userpokedata(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    pokedataid = db.Column(db.Integer, db.ForeignKey('pokedata.id'), primary_key=True)

    def remove_pokemon(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String())
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    team = db.relationship('Pokedata',
        secondary = 'userpokedata',
        backref='user',
        lazy='dynamic')

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
    
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
    
    def add_to_team(self, data):
        if len(list(self.team)) < 5:
            self.team.append(data)
            self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def hit_points(self):
        all_points = []
        for pokemon in self.team:
            all_points.append(pokemon.hp)
            match_total = sum(all_points)
            return str(match_total)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Pokedata(db.Model):
    # __tablename__='pokedata'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    hp = db.Column(db.Integer)
    defense = db.Column(db.String(50))
    attack = db.Column(db.String(50))
    ability_1 = db.Column(db.String(50))
    ability_2 = db.Column(db.String(50))
    sprite = db.Column(db.String(100))

    def exists(name):
        return Pokedata.query.filter_by(name=name).first()

    def __repr__(self):
        return f'<User: {self.id} | {self.name}>'

    def from_dict(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.defense = data['defense']
        self.attack = data['attack']
        self.ability_1 = data['ability_1']
        self.ability_2 = data['ability_2']
        self.sprite = data['sprite']

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()