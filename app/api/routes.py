from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Schedule, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/schedule', methods = ['POST'])
@token_required
def create_schedule(current_user_token):
    Monday = request.json['Monday']
    Tuesday = request.json['Tuesday']
    Wednesday = request.json['Wednesday']
    Thursday = request.json['Thursday']
    Friday = request.json['Friday']
    Saturday = request.json['Saturday']
    Sunday = request.json['Sunday']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    schedule = Schedule(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, user_token = user_token )

    db.session.add(schedule)
    db.session.commit()

    response = contact_schema.dump(schedule)
    return jsonify(response)

@api.route('/schedule', methods = ['GET'])
@token_required
def get_schedule(current_user_token):
    a_user = current_user_token.token
    schedule = Schedule.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(schedule)
    return jsonify(response)

@api.route('/schedule/<id>', methods = ['GET'])
@token_required
def get_single_schedule(current_user_token, id):
    schedule = Schedule.query.get(id)
    response = contact_schema.dump(schedule)
    return jsonify(response)

@api.route('/schedule/<id>', methods = ['POST','PUT'])
@token_required
def update_schedule(current_user_token,id):
    schedule = Schedule.query.get(id) 
    schedule.Monday = request.json['Monday']
    schedule.Tuesday = request.json['Tuesday']
    schedule.Wednesday = request.json['Wednesday']
    schedule.Thursday = request.json['Thursday']
    schedule.Friday = request.json['Friday']
    schedule.Saturday = request.json['Saturday']
    schedule.Sunday = request.json['Sunday']
    schedule.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(schedule)
    return jsonify(response)

@api.route('/schedule/<id>', methods = ['DELETE'])
@token_required
def delete_schedule(current_user_token, id):
    schedule = Schedule.query.get(id)
    db.session.delete(schedule)
    db.session.commit()
    response = contact_schema.dump(schedule)
    return jsonify(response)