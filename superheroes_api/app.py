from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates

app = Flask(__name__)

# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after initializing SQLAlchemy
from models import Hero, Power, HeroPower

# Routes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    else:
        return jsonify({"error": "Power not found"}), 404

# PATCH /powers/:id - Updates the description of a Power
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get('description')
    
    # Validate description length
    if description and len(description) >= 20:
        power.description = description
        db.session.commit()
        return jsonify({
            "id": power.id,
            "name": power.name,
            "description": power.description
        }), 200
    else:
        return jsonify({"errors": ["Description must be at least 20 characters long."]}), 400

# Handle both GET and POST methods for /hero_powers
@app.route('/hero_powers', methods=['GET', 'POST'])
def hero_powers():
    if request.method == 'POST':
        data = request.get_json()
        strength = data.get('strength')
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')

        # Validate strength
        if strength not in ['Strong', 'Weak', 'Average']:
            return jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'."]}), 400

        # Validate hero and power existence
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)
        
        if not hero or not power:
            return jsonify({"errors": ["Hero or Power not found."]}), 404

        # Create HeroPower
        hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(hero_power)
        db.session.commit()

        # Include hero and power details in the response
        return jsonify({
            "id": hero_power.id,
            "strength": hero_power.strength,
            "hero_id": hero.id,
            "power_id": power.id,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            },
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
        }), 201

    elif request.method == 'GET':
        # Retrieve all HeroPower records
        hero_powers = HeroPower.query.all()
        return jsonify([{
            "id": hero_power.id,
            "strength": hero_power.strength,
            "hero_id": hero_power.hero_id,
            "power_id": hero_power.power_id,
            "hero": hero_power.hero.to_dict(),
            "power": hero_power.power.to_dict()
        } for hero_power in hero_powers])

if __name__ == '__main__':
    app.run(debug=True)
