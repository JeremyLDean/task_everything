from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_user import User

db = 'task_everything_db2'

class Task:
    def __init__( self , data ):
        self.id = data['id']
        self.description = data['description']
        self.status = data['status']
        self.due_date = data['due_date']
        self.created_by_id = data['created_by_id']
        self.assigned_to_id = data['assigned_to_id']
        self.creator = None
        self.owner = None

    @classmethod
    def create_task(cls, data):
        query = """
                INSERT INTO tasks ( description, status, due_date , created_by_id, assigned_to_id) 
                VALUES ( %(description)s,  %(status)s, %(due_date)s, %(created_by_id)s, %(assigned_to_id)s);
                """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM tasks
                JOIN users ON users.id = tasks.created_by_id
                WHERE tasks.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        task = cls(results[0])
        owner_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
        }
        task.owner = User(owner_data)
        return task

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM tasks
                LEFT JOIN users AS created_by ON created_by.id  = tasks.created_by_id
                LEFT JOIN users AS assigned_to ON assigned_to.id = tasks.assigned_to_id
                """
        results = connectToMySQL(db).query_db(query)
        print("B")
        print(results)
        all_tasks = []
        for db_row in results:
            for key,value in db_row.items():
                print(key,"\t\t",value)
            one_task = cls(db_row)
            creator_info = {
                'id' : db_row['created_by.id'],
                'first_name' : db_row['first_name'],
                'last_name' : db_row['last_name'],
                'email' : db_row['email'],
                'password' : db_row['password'],
                'created_at' : db_row['created_by.created_at'],
                'updated_at' : db_row['created_by.updated_at']
            }
            one_task.creator = User(creator_info)
            all_tasks.append(one_task)
        return all_tasks

    @classmethod
    def update_task(cls, form_data, task_id):
        print("RECIPE ID =",task_id,"FORM_DATA =",form_data)
        query = f"UPDATE tasks SET description = %(description)s, status = %(status)s, due_date = %(due_date)s WHERE id = {task_id}" 
        return connectToMySQL(db).query_db(query, form_data)

    @staticmethod
    def task_validator(data):
        is_valid = True
        if len(data['description']) < 1:
            flash("Description must be at least 1 characters", 'task')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users WHERE email = %(email)s
                """
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return (cls(results[0]))        

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM tasks WHERE id = %(id)s;"
        return connectToMySQL(db).query_db( query, data)

    @classmethod
    def get_assigned_tasks(cls, data):
        query = """
                SELECT * FROM tasks
                JOIN users on users.id = assigned_to_id
                WHERE users.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        all_tasks = []
        for db_row in results:
            one_task = cls(db_row)
            creator_info = {
                'id' : db_row['users.id'],
                'first_name' : db_row['first_name'],
                'last_name' : db_row['last_name'],
                'email' : db_row['email'],
                'password' : db_row['password'],
                'created_at' : db_row['users.created_at'],
                'updated_at' : db_row['users.updated_at']
            }
            one_task.creator = User(creator_info)
            all_tasks.append(one_task)
        return all_tasks        
