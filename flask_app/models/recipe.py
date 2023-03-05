from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app import app
from flask import flash, session

class Recipe:
    DB = 'recipes'
    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.mins = data['mins']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.id = data['id']
        self.users_id = data['users_id']
        self.creator = None
    
    @classmethod
    def get_all(cls): # READ ALL RECIPES & DISPLAY ON DASH
        query = """SELECT * FROM recipes
                JOIN users ON users.id = recipes.users_id;"""
        result = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for row in result:
            recipe = cls(row)
            recipe.creator = user.User({
                "f_name": row["f_name"],
                "l_name": row["l_name"],
                "email": "",
                "pw": "",
                "created_at": "",
                "updated_at": "",
                "id": row["users.id"]
            })
            recipes.append(recipe)
        print(result)
        return recipes
    
    @classmethod
    def save_recipe(cls, data): # CREATE & SAVE A RECIPE
        print("Saving recipe...")
        if not cls.validate_input(data):
            return False
        query = """INSERT into recipes (users_id, name, description, instructions, mins)
                VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(mins)s);"""
        print("Recipe has been saved.")
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("Recipe has been created!")
        if True:
            return result
    
    @staticmethod
    def validate_input(data): # VALIDATE RECIPE INPUT
        is_valid = True
        if len(data['name']) < 1: # IS NAME THERE
            flash("Recipe name is a required field.", "recipe")
            is_valid = False
        elif len(data['name']) < 3: # VALIDATE LENGTH OF RECIPE NAME
            flash("Recipe name must contain letters only and be at least 2 characters long.", "recipe")
            is_valid = False
        if len(data['description']) < 1: # IS DESCRIPTION THERE
            flash("Description must not be blank.", "recipe")
            is_valid = False
        elif len(data['description']) < 3: # VALIDATE LENGTH OF DESCRIPTION
            flash("Description must contain letters only and be at least 2 characters long.", "recipe")
            is_valid = False
        if len(data['instructions']) < 1: # ARE INSTRUCTIONS THERE
            flash("Instructions must not be blank.", "recipe")
            is_valid = False
        elif len(data['instructions']) < 3: # VALIDATE LENGTH OF INSTRUCTIONS
            flash("Instructions must contain letters only and be at least 2 characters long.", "recipe")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_one(cls, id): # READ 1 RECIPE
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.users_id WHERE recipes.id = %(id)s;"
        data = {'id':id}
        result = connectToMySQL(cls.DB).query_db(query,data)
        recipe = cls(result[0])
        print(result)
        recipe.creator = user.User({
                "f_name": result[0]["f_name"],
                "l_name": "",
                "email": "",
                "pw": "",
                "created_at": "",
                "updated_at": "",
                "id": ["users.id"]
            })
        print(recipe.creator.first_name)
        print("Selecting recipe...")
        return recipe

    @classmethod
    def update(cls, data): # UPDATING RECIPE INFO
        print("Updating...")
        query = """UPDATE recipes
                SET name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s,
                mins = %(mins)s
                WHERE id = %(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("Update completed!")
        return result
    
    @classmethod
    def delete(cls, id): # DELETE A RECIPE
        query = """DELETE FROM recipes
                WHERE id = %(id)s;"""
        data = {'id':id}
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("Deleting recipe...")
        return result