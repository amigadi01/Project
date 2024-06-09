from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Task, Goal, Event
from . import db
import os

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        task_description = request.form.get('newTask')
        new_task = Task(description=task_description, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("todo.html", user=current_user, tasks=tasks)

@views.route('/delete-task', methods=['POST'])
@login_required
def delete_task():
    task_id = request.json['taskId']
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return '', 204

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note_id = request.json['noteId']
    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return '', 204

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_pdf():
    if request.method == 'POST':
        if 'pdfFile' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['pdfFile']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename) # type: ignore
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded', 'success')
        else:
            flash('Invalid file format', 'error')
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', files=files, user=current_user)

@views.route('/uploaded_file/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename) # type: ignore

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_goal = Goal(
            title=request.form.get('title'),
            description=request.form.get('description'),
            user_id=current_user.id
        )
        db.session.add(new_goal)
        db.session.commit()
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=current_user, goals=goals)
