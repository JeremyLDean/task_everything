from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.models_user import User
from flask_app.models.models_task import Task
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date


# tasks page / dashboard
@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    assigned_tasks = Task.get_assigned_tasks(user_data) 
    tasks = Task.get_all()
    return render_template('tasks.html', user = user, assigned_tasks = assigned_tasks, tasks = tasks)

# new task page
@app.route('/tasks/new')
def new_task_page():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    today = date.today()
    user = User.get_one(user_data)
    tasks = Task.get_all() 
    return render_template('new.html', user = user, tasks = tasks, today = today)

# new task
@app.route('/create_task', methods=['POST'])
def create_task():
    data = {
        'description' : request.form['description'],
        'status' : request.form['status'],
        'due_date' : request.form['due_date'],
        'created_by_id' : session['user_id'],
        'assigned_to_id' : request.form['assigned_to_id'],
    }
    valid = Task.task_validator(data)
    if valid:
        Task.create_task(data)
        return redirect('/tasks')
    return redirect('/tasks/new')

# edit task page
@app.route('/tasks/<int:task_id>/edit')
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : task_id
    }
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    task = Task.get_one(data)
    return render_template('edit.html', task = task, user = user)

# update task
@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    valid = Task.task_validator(request.form)
    if valid:
        Task.update_task(request.form, task_id)
        return redirect('/tasks')
    return redirect(f"/tasks/{task_id}/edit")

# show task page
@app.route('/tasks/<int:task_id>')
def show_task(task_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : task_id
    }
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    task = Task.get_one(data) 
    return render_template('show.html', task = task, user = user)

# delete task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    data = {
        "id" : task_id
    }
    Task.delete(data)
    return redirect('/tasks')
