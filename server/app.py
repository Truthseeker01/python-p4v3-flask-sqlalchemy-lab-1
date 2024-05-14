# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.get('/earthquakes/<int:id>')
def get_earthquake(id:int):
    eq = Earthquake.query.where(Earthquake.id == id).first()
    if eq:
        return eq.to_dict(), 200
    return { "message": f"Earthquake {id} not found."}, 404

@app.get('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes(magnitude:float):
    earthquakes = Earthquake.query.where(Earthquake.magnitude >= magnitude).all()
    if earthquakes:
        return {
            "count": len(earthquakes),
            "quakes":[eq.to_dict() for eq in earthquakes]
            }, 200
    return  {
            "count": len(earthquakes),
            "quakes":[]
            }, 200



if __name__ == '__main__':
    app.run(port=5555, debug=True)
