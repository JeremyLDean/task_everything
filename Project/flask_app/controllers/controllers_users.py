from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_user import User
from flask_app.models.models_task import Task
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# login page
@app.route('/')
def index():
    return render_template('login.html')

# register user
@app.route('/register_user', methods=['POST'])
def register_user():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password'],
    }
    valid = User.user_validator(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data['pw_hash'] = pw_hash
        user = User.create_user(data)
        session['user_id'] = user
        print('New user created!')
        return redirect("/tasks")
    return redirect("/")

# login
@app.route('/login_user', methods=['POST'])
def login_user():  
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/tasks')

# logout
@app.route('/logout')
def logout():
    session.clear() 
    return redirect('/')

# friends page
@app.route('/friends')
def friends():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    users = User.get_all()
    user = User.get_one(data)
    for x in users:
        print(x.id)
    return render_template('friends.html', users = users, user = user)
    
# in progress
# add_friendship
@app.route('/add_friendship/<int:user_id>', methods=['POST'])
def add_friendship():
    friend_data = {
        'friend1_id' : request.form['email'],
    }
    friend = User.get_one()
    data = {
        'friend1_id' : request.form['email'],
        'friend2_id' : session['user_id'],
    }
    return redirect('/friends')

# in progress
# remove friendship
@app.route('/remove_friendship/<int:task_id>')
def remove_friendship(task_id):
    data = {
        "id" : task_id
    }
    User.remove_friendship(data)
    return redirect('/tasks')