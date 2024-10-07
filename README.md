# Superhero Power Tracker API

## Overview

The **Superhero Power Tracker API** is a RESTful API built with Flask that allows users to manage superheroes, their powers, and the relationships between them. The API supports various operations for heroes, powers, and hero-power associations.

## Features

- **CRUD Operations**:
  - Get all heroes
  - Get a specific hero by ID
  - Get all powers
  - Get a specific power by ID
  - Create, update, and delete hero-power associations

- **Validation**:
  - Ensures that powers and heroes exist before creating associations.
  - Validates input data for strength and description length.

## API Endpoints

### Heroes

- **GET /heroes**: Retrieve a list of all heroes.
- **GET /heroes/<id>**: Retrieve a hero by ID.

### Powers

- **GET /powers**: Retrieve a list of all powers.
- **GET /powers/<id>**: Retrieve a power by ID.
- **PATCH /powers/<id>**: Update a power's description.

### Hero Powers

- **GET /hero_powers**: Retrieve all hero-power associations.
- **POST /hero_powers**: Create a new hero-power association.

## Setup

### Prerequisites

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Create a Virtual Environment:
    ```bash
    python3 -m venv .venv

3. Activate the Virtual Environment:
    ```bash
    source .venv/bin/activate

    
4. cd superheroes_api


5. Install the required packages:
    ```bash
    Copy code
    pip install -r requirements.txt

6. Set up the database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade

## Run the application:

    python app.py

## Usage
    Use tools like Postman or cURL to interact with the API endpoints. For example, to create a new hero-power association:

    curl -X POST http://127.0.0.1:5000/hero_powers \
    -H "Content-Type: application/json" \
    -d '{"strength": "Average", "power_id": 1, "hero_id": 3}'

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.