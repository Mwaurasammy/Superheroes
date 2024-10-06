from app import db

# Hero Model
class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name
        }

    def to_dict_with_powers(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "hero_powers": [hp.to_dict() for hp in self.hero_powers]
        }

# Power Model
class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')

    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    @staticmethod
    def validate_description(description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

# Hero-Power (Join Table)
class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    strength = db.Column(db.String, nullable=False)  # Changed to String to match validation

    def __init__(self, hero_id, power_id, strength):
        self.hero_id = hero_id
        self.power_id = power_id
        self.strength = strength

    @staticmethod
    def validate_strength(strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Invalid strength value')
        
    def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "hero": self.hero.to_dict(),
            "power": self.power.to_dict()
        }
