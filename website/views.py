from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note  # oder ein eigenes Modell für Termine
from . import db
import json

views = Blueprint('views', __name__)

# Beispiel-Daten für den Kalender
termin_daten = [
    {"id": 1, "title": 'Event 1', "start": '2024-04-01'},
    {"id": 2, "title": 'Ami Study', "start": '2024-05-05T15:30:00', "end": '2024-05-07'},
    {"id": 3, "title": 'Event 3', "start": '2024-01-09T12:30:00', "allDay": False}
]

@views.route('/termine', methods=['GET'])
def termine():
    return jsonify(termin_daten)

@views.route('/add-event', methods=['POST'])
@login_required
def add_event():
    data = json.loads(request.data)
    title = data['title']
    start = data['start']
    end = data.get('end')
    
    new_event = {"id": len(termin_daten) + 1, "title": title, "start": start, "end": end}
    termin_daten.append(new_event)
    
    return jsonify(new_event)

@views.route('/delete-event', methods=['DELETE'])
@login_required
def delete_event():
    data = json.loads(request.data)
    event_id = data['id']
    
    global termin_daten
    termin_daten = [event for event in termin_daten if event["id"] != event_id]
    
    return jsonify({"success": True})
