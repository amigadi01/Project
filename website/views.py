from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Task
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
        flash('Note deleted!', category='success')
    return jsonify({"success": True})

@views.route('/calendar')
def calendar():
    return render_template('calendar.html', user=current_user)

@views.route('/termine')
def termine():
    return jsonify(termin_daten)

@views.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        if 'newTask' in request.form:
            new_task = Task(description=request.form.get('newTask'), user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', category='success')
        elif 'note' in request.form:
            new_note = Note(data=request.form.get('note'), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', category='success')
        return redirect(url_for('views.todo'))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', tasks=tasks, user=current_user, notes=notes)

@views.route('/delete-task', methods=['POST'])
@login_required
def delete_task():
    task = json.loads(request.data)
    task_id = task['taskId']
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!', category='success')
    return jsonify({"success": True})
