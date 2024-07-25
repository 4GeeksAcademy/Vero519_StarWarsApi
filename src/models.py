from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Characters(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=True)
    mass = db.Column(db.String(250), nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    skin_color = db.Column(db.String(250), nullable=True)
    birth_year = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    favorites = db.relationship('Favorites', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "heigt": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "gender": self.gender

            # do not serialize the password, its a security breach
        }
class Planets(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name_planet = db.Column(db.String(250), nullable=False)
    mass = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    populate = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.String(250), nullable=True)
    gravity = db.Column(db.String(250), nullable=True)
    orbital_period = db.Column(db.String(250), nullable=True)
    surface_water = db.Column(db.String(250), nullable=True)
    favorites = db.relationship('Favorites', backref='planets', lazy=True)
    
    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name_planet": self.name_planet,
            "mass": self.mass,
            "climate": self.climate,
            "populate": self.populate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "surface_water": self.surface_water
        }
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250))
    pasword = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'),
        nullable=True)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'),
        nullable=True)
    
    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def serialize(self):
        query_character = Characters.query.filter_by(id=self.characters_id).first()
        print(query_character.serialize())
        return {

            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
            "characters_info": query_character.serialize()["name"]
        }

## Draw from SQLAlchemy base
