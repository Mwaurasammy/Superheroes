from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower  # Import db and models from models.py

app = Flask(__name__)

# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db.init_app(app)
migrate = Migrate(app, db)

# Root route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Superheroes API!"})

# Routes for heroes, powers, and hero powers
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

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get('description')
    if description and len(description) >= 20:
        power.description = description
        try:
            db.session.commit()
            return jsonify(power.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"errors": ["Description must be at least 20 characters"]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    strength = data.get('strength')
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    # Validate strength input
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Strength must be Strong, Weak, or Average."]}), 400
    
    # Fetch hero and power objects
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    # Check if hero and power exist
    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found."]}), 404

    # Create the new HeroPower object
    hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
    
    db.session.add(hero_power)
    
    try:
        db.session.commit()

        return jsonify({
            "id": hero_power.id,
            "hero_id": hero.id,
            "power_id": power.id,
            "strength": hero_power.strength,
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

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
