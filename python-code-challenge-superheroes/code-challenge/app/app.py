#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow

from models import db, Hero, Power, HeroPower

# create your Flask Application and Set the DATABASE URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app) # connects our database to our application before it runs

ma = Marshmallow(app) # instantiating Marshmallow with the flask application instance

class PowerSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Power
    # Fields to expose
        fields = ("id","name","description")

power_schema = PowerSchema()
powers_schema = PowerSchema(many=True)

class HeroSchema(ma.SQLAlchemyAutoSchema):
    
    powers = ma.Nested(PowerSchema, many=True)

    class Meta:
        model = Hero
        # Fields to expose
        fields = ("id", "name", "super_name")

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)

api = Api(app)

class Index(Resource):

    def get(self):

        response_dict = {
            "index": "Welcome to Superheroes RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(Index, '/')

class Heroes(Resource):
    def get(self):
        hero = Hero.query.all()
        hero_dict = heroes_schema.dump(hero)
        response = make_response(
            jsonify(hero_dict), 
            200
            )
        return response
    
api.add_resource(Heroes, '/heroes')

class HeroByID(Resource):
    # get the record using the id
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()

        if not hero:
            response_body = {"error": "Hero not found"}
            response = make_response(
                jsonify(response_body),
                404
            )
            return response
        else:
            powers = Power.query.join(HeroPower).filter(HeroPower.hero_id == id).all()
            
            response_body = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": []
            }
            for power in powers:
                pd = {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                }
                response_body["powers"].append(pd)

            return response_body, 200

# add the resource to the API   
api.add_resource(HeroByID, '/heroes/<int:id>')

class Powers(Resource):

    def get(self):
        power_dict = Power.query.all()

        response = make_response(
            powers_schema.dump(power_dict), 
            200
        )
        return response
    
# add the resource to the API   
api.add_resource(Powers, '/powers')

class PowerByID(Resource):
    def get(self, id):

        power_list = Power.query.filter_by(id=id).first()

        if not power_list:
            return make_response ({"error": "Power not found"}, 404)
        else:
            response = power_schema.dump(power_list)
            return make_response(
                jsonify(response),
                200
            )
    
    def patch(self, id):

        power = Power.query.filter_by(id=id).first()
        
        if not power:
            return make_response({"error": "Power not found"}, 404)
        
        for attr in request.form:
            setattr(power, attr, request.form.get(attr))
            
        db.session.add(power)
        db.session.commit()

        response = make_response(
            power_schema.dump(power),
            200
        )
        return response
        
api.add_resource(PowerByID, '/powers/<int:id>')

class HeroPowers(Resource):

    def post(self):

        new_hero_power = HeroPower(
            hero_id = request.form.get("hero_id"), 
            power_id = request.form.get("power_id"), 
            strength = request.form.get("strength")
            )
        
        hero = Hero.query.filter_by(id=request.form.get("hero_id")).first()

        if not hero:
            return {"error": "Hero not found"}
        else:
            db.session.add(new_hero_power)
            db.session.commit()

            powers = Power.query.join(HeroPower).filter_by(id=request.form.get("hero_id")).all()
            
            response_body = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": []
            }

            for power in powers:
                pd = {
                    "id":power.id,
                    "name": power.name,
                    "description": power.description
                }
                response_body["powers"].append(pd)

            response = make_response(
                power_schema.dump(response_body),
                201,
            )
            return response
        
# add the resource to the API
api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

