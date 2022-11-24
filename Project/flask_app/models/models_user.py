from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL

db = 'task_everything_db2'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tasks_assigned_to = []
        self.tasks_created = []
        self.friends = []
        # self.friends_ids = []

    @classmethod
    def add_friendship(cls, data):
        query = """
                INSERT INTO friendship ( friend1_id, friend2_id ) 
                VALUES ( %(user_id)s, %(xxx)s )
                """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def remove_friendship(cls, data):
        query = """
                DELETE FROM friendship WHERE id = %(id)s; 
                """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM users WHERE id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM users
                """
        results = connectToMySQL(db).query_db(query)
        all_users = []
        for row in results:
            this_user = cls(row)
            all_users.append(this_user)
        return all_users

    @classmethod
    def get_assigned_tasks(cls, data):
        query = """
                SELECT * FROM tasks WHERE assigned_to_id = %(id)s
                """    
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_created_tasks(cls, data):
        query = """
                SELECT * FROM tasks WHERE created_by_id = %(id)s
                """    
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def create_user(cls, data):
        query = """
                INSERT INTO users ( first_name, last_name, email, password) 
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s);
                """
        return connectToMySQL(db).query_db( query, data )

    @staticmethod
    def user_validator(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 character.", 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 character.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) != 0:
            flash('This email is alreay being used', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Password does not match!', 'register')
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

    # @classmethod
    # def get_one(cls, data):
    #     query = """
    #             SELECT * FROM users AS friend1 
    #             LEFT JOIN friendships
    #             ON friend1.id = friendships.friend1_id
    #             LEFT JOIN users AS friend2
    #             ON friend2.id = friendships.friend2_id
    #             LEFT JOIN tasks AS tasks_created
    #             ON tasks_created.created_by_id = %(id)s
    #             LEFT JOIN tasks AS tasks_assigned_to
    #             ON tasks_assigned_to.assigned_to_id = %(id)s
    #             WHERE friend1_id = %(id)s OR friend2_id = %(id)s;
    #             """
    #     results = connectToMySQL(db).query_db(query, data)
    #     for row in results:
    #         print("A")
    #         for key, value in results[0].items():
    #             print(key,"\t\t",value)
    #     user = cls(results[0])
    #     # populate empty lists
    #     return user
