from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    DB = 'recipes'
    def __init__(self, data):
        self.first_name = data['f_name']
        self.last_name = data['l_name']
        self.email = data['email']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.id = data['id']
        self.recipes = []

    @classmethod
    def create_user(cls, data):
        if not cls.validate_input(data):
            return False
        pdata = User.parse_data(data)
        print("Data has been parsed.")
        query = """INSERT INTO users (f_name, l_name, email, pw)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s);
        """
        print("Data has been saved.")
        user_id = connectToMySQL(cls.DB).query_db(query, pdata)
        session['user_id'] = user_id
        print("User has been created.")
        return True

    # READ login.user SQL
    
    @classmethod
    def user_email(cls, email):
        data = {'email':email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if result:
            result = cls(result[0])
        return result

    @staticmethod
    def validate_input(data):
        EMAIL_REGEX =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['f_name']) < 1: # IS FIRST NAME THERE
            flash("First name is a required field.", "reg")
            is_valid = False
        elif len(data['f_name']) < 3: # VALIDATE LENGTH OF FIRST NAME
            flash("First name must contain letters only and be at least 2 characters long.", "reg")
            is_valid = False
        if len(data['l_name']) < 1: # IS LAST NAME THERE
            flash("Last name is a required field.", "reg")
            is_valid = False
        elif len(data['l_name']) < 3: # VALIDATE LENGTH OF LAST NAME
            flash("Last name must contain letters only and be at least 2 characters long.", "reg")
            is_valid = False
        if len(data['email']) < 1: # IS EMAIL THERE
            flash("Email is a required field.", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): # NEED TO ALSO CHECK IF EMAIL ALREADY EXISTS
            flash("Invalid email address. Please try again.", "reg")
            is_valid = False
        if User.user_email(data['email'].lower()):
            flash("That email has already been taken. Please use another email.", "reg")
            is_valid = False
        if len(data['pw']) < 1: # IS PW THERE
            flash("Password is a required field.", "reg")
        elif len(data['pw']) < 8: # VALIDATE LENGTH OF PW
            flash("Password must be at least 8 characters long.", "reg")
            is_valid = False
        if data['pw'] != data['cpw']: # VALIDATE IF BOTH FIELDS OF PW AND CONFIRM PW MATCH
            flash("Passwords do not match. Please try again.", "reg")
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_data(data):
        print("Parsing data...")
        parsed_data = {}
        parsed_data['first_name'] = data['f_name']
        parsed_data['last_name'] = data['l_name']
        print("hi")
        parsed_data['email'] = data['email'].lower()
        print("ew")
        parsed_data['pw'] = bcrypt.generate_password_hash(data['pw'])
        print(parsed_data)
        return parsed_data
    
    @staticmethod
    def login(data):
        user = User.user_email(data['email'].lower())
        print("Logging in...")
        if user:
            if bcrypt.check_password_hash(user.pw, data['pw']):
                session['user_id'] = user.id
                print("Verifying...")
                return True
        flash("Your login is incorrect. Please try again.", "login")
        return False
    
    @classmethod # GETTING USER BY ID
    def get_user_by_id(cls, users_id):
        query = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL(cls.DB).query_db(query,{'id':users_id})
        print(result)
        get_user = cls(result[0])
        if result:
            return get_user
        else:
            raise ValueError("User with id {} does not exist".format(users_id))

    @classmethod # ALL RECIPES FROM 1 USER
    def recipes_from_user(cls, users_id):
        query = """SELECT * FROM recipes 
                WHERE users_id = %(id)s;"""
        print("Retrieving recipes...")
        data = {'id':users_id}
        result = connectToMySQL(cls.DB).query_db(query,data)
        recipes = []
        if result:
            for row in result:
                recipe_data = {'id':row['id'], 'name':row['name'], 'description':row['description'], 'instructions':row['instructions'], 'created_at':row['created_at'], 'updated_at':row['updated_at'], 'users_id':row['users_id']}
                one_recipe = recipe_data
                recipes.append(one_recipe)
        print("Retrieval completed.")
        return recipes