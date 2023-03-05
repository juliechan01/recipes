from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

# DASHBOARD/DISPLAYING ALL RECIPES FROM USER
@app.route('/users/recipes')
def profile():
    user_id = int(session['user_id'])
    try:
        user = User.get_user_by_id(user_id)
    except ValueError as e:
        return str(e)
    all_recipes = Recipe.get_all()
    return render_template("dashboard.html" , user=user, recipes=all_recipes)

# ADDING A RECIPE PAGE
@app.route('/recipes/new')
def add_recipe():
    user = User.get_user_by_id(session['user_id'])
    return render_template("new_recipe.html", user=user)

# ADDING A NEW RECIPE FORM
@app.route('/create-recipe', methods=['POST'])
def create_recipe():
    data = {
        "user_id":session['user_id'],
        "name":request.form['name'],
        "description":request.form['description'],
        "instructions":request.form['instructions'],
        "mins":request.form['mins']
    }
    if Recipe.validate_input(data):
        Recipe.save_recipe(data)
        return redirect('/users/recipes')
    return redirect('/recipes/new')

# DISPLAYING 1 RECIPE
@app.route('/recipes/<int:recipes_id>')
def one_recipe(recipes_id):
    user = User.get_user_by_id(session['user_id'])
    recipe = Recipe.get_one(recipes_id)
    return render_template("recipe.html", user=user, recipe=recipe)

# EDITING A RECIPE PAGE
@app.route('/recipes/edit/<int:recipes_id>')
def edit_recipe(recipes_id):
    user = User.get_user_by_id(session['user_id'])
    recipe = Recipe.get_one(recipes_id)
    return render_template("edit_recipe.html", user=user, recipe=recipe)

# EDITING A RECIPE FORM
@app.route('/update/<int:recipes_id>', methods=['POST'])
def update_recipe(recipes_id):
    data = {
        "id":recipes_id, 
        "name":request.form['name'],
        "description":request.form['description'],
        "instructions":request.form['instructions'],
        "mins":request.form['mins']
    }
    if Recipe.validate_input(data):
        print("Input has been validated.")
        Recipe.update(data)
        return redirect('/users/recipes')
    print("Validation has failed. Please try again.")
    return redirect(f"/recipes/edit/{recipes_id}")

# DELETING A RECIPE
@app.route('/recipe/delete/<int:recipes_id>')
def delete(recipes_id):
    Recipe.delete(recipes_id)
    return redirect('/users/recipes')