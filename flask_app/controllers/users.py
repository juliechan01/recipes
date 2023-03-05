from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User

# LOGIN PAGE
@app.route('/')
def home():
    return render_template("login.html")

# CREATE USER/REGISTER
@app.route('/register', methods=['POST'])
def register():
    if User.create_user(request.form):
        print("end")
        return redirect('/users/recipes')
    return redirect('/')

# SIGN OUT 
@app.route('/users/logout')
def sign_out():
    session.clear()
    return redirect('/')

# SIGN IN
@app.route('/users/login', methods=['POST'])
def sign_in():
    if User.login(request.form):
        return redirect('/users/recipes')
        session['user_id'] = User.id
    return redirect('/')