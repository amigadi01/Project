from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

termin_daten = [
     {
            "title": 'event1',
            "start": '2024-04-01'
    },
    {
            "title": 'Ami Study',
            "start": '2024-05-05T15:30:00',
            "end": '2024-05-07'
    },
    {
            "title": 'event3',
            "start": '2024-01-09T12:30:00',
            "allDay": False
    }
]

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})

@views.route('/calendar')
def calendar():
    return render_template('calendar.html', user=current_user)

@views.route('/termine')
def termine():
    return jsonify(termin_daten)

@views.route('/todo')
def todo():
    return render_template('todo.html', user=current_user)