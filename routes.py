from flask import Blueprint, request, jsonify
from models import db, Availability

availability_bp = Blueprint('availability_bp', __name__)

@availability_bp.route('/availability', methods=['GET'])
def get_availabilities():
    availabilities = Availability.query.all()
    return jsonify([{
        'id': a.id,
        'date': a.date.isoformat(),
        'start_time': a.start_time.isoformat(),
        'end_time': a.end_time.isoformat()
    } for a in availabilities])

@availability_bp.route('/availability', methods=['POST'])
def create_availability():
    data = request.get_json()
    new_availability = Availability(
        date=data['date'],
        start_time=data['start_time'],
        end_time=data['end_time']
    )
    db.session.add(new_availability)
    db.session.commit()
    return jsonify({
        'id': new_availability.id,
        'date': new_availability.date.isoformat(),
        'start_time': new_availability.start_time.isoformat(),
        'end_time': new_availability.end_time.isoformat()
    }), 201
