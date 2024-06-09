from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, Task, Goal, User, Event  # Stelle sicher, dass das Event-Modell importiert ist
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
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
@login_required
def calendar():
    return render_template('calendar.html', user=current_user)

@views.route('/termine')
@login_required
def termine():
    # Diese Route sollte Events aus der Datenbank abrufen
    events = Event.query.filter_by(user_id=current_user.id).all()
    event_list = []
    for event in events:
        event_data = {
            "id": event.id,
            "title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat() if event.end else None
        }
        event_list.append(event_data)
    return jsonify(event_list)

@views.route('/add-event', methods=['POST'])
@login_required
def add_event():
    data = request.get_json()
    new_event = Event(
        title=data['title'],
        start=data['start'],
        end=data.get('end', None),
        user_id=current_user.id
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(id=new_event.id, title=new_event.title, start=new_event.start, end=new_event.end)

@views.route('/delete-event', methods=['DELETE'])
@login_required
def delete_event():
    data = request.get_json()
    event_id = data['id']
    event = Event.query.get(event_id)
    if event and event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)

@views.route('/get-events', methods=['GET'])
@login_required
def get_events():
    events = Event.query.filter_by(user_id=current_user.id).all()
    events_data = []
    for event in events:
        events_data.append({
            "id": event.id,
            "title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat() if event.end else None
        })
    return jsonify(events_data)

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

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title or not description:
            flash('Title and description are required!', category='error')
        else:
            new_goal = Goal(title=title, description=description, user_id=current_user.id)
            db.session.add(new_goal)
            db.session.commit()
            flash('Goal added successfully!', category='success')
        return redirect(url_for('views.profile'))

    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=current_user, goals=goals)

@views.route('/delete-goal', methods=['POST'])
@login_required
def delete_goal():
    goal = json.loads(request.data)
    goal_id = goal['goalId']
    goal = Goal.query.get(goal_id)
    if goal and goal.user_id == current_user.id:
        db.session.delete(goal)
        db.session.commit()
        flash('Goal deleted!', category='success')
    return jsonify({"success": True})

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        description = request.form.get('description')

        if not name or not email or not description:
            flash('All fields are required!', category='error')
        else:
            current_user.name = name
            current_user.email = email
            current_user.description = description
            db.session.commit()
            flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.edit_profile'))

    return render_template('edit_profile.html', user=current_user)

@views.route('/wettspiel')
@login_required
def wettspiel():
    return render_template('wettspiel.html', user=current_user)

@views.route('/add', methods=['POST'])
@login_required
def add_task():
    new_task = request.form.get('newTask')
    if new_task:
        task = Task(description=new_task, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', category='success')
    return redirect(url_for('views.todo'))
