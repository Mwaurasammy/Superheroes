from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    hero_powers = db.relationship('HeroPower', backref='hero', cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "hero_powers": [hp.to_dict(hero=False) for hp in self.hero_powers]  
        }

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    hero_powers = db.relationship('HeroPower', backref='power', cascade="all, delete")

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "hero_powers": [hp.to_dict(power=False) for hp in self.hero_powers]  
        }

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be Strong, Weak, or Average.")
        return strength

    def to_dict(self, hero=True, power=True):
        data = {
            "id": self.id,
            "strength": self.strength,
        }
        if hero:
            data["hero"] = {"id": self.hero.id, "name": self.hero.name}  
            data["power"] = {"id": self.power.id, "name": self.power.name}  
        return data
