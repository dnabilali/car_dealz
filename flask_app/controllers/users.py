
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_app import app
from flask import redirect, render_template, session, request, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def login_registration():
    return render_template("login.html")

@app.route("/logout")
def log_out():
    session.clear()
    return render_template("login.html")

@app.route("/registration", methods=['POST'])
def registration():
    if not User.validate_inputs(request.form):
        return redirect('/')
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'email' : request.form['email'],
        'password' : hashed_password,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name']
        }
    user_id = User.registration(data)
    session['user_id'] = user_id
    return redirect(f"/profile/{user_id}")

@app.route("/profile/<int:id>")
def profile(id):
    if 'user_id' in session and session['user_id'] == id:
        return render_template("profile.html", user_name = User.get_one_user({"id": id}), all_cars = Car.get_all_cars(), user_id = session['user_id'])
    else:
        flash('Please sign in to access your profile!','login')
        return redirect('/')

@app.route("/login", methods=['POST'])
def login():
    user = User.get_user_by_email({'email':request.form['email']})
    # print('user is', user)
    if len(user) == 0:
        flash('This email address is not registered. Please register first.', 'login')
        return redirect('/')
    if bcrypt.check_password_hash(user[0]['password'],request.form['password']):
        session['user_id'] = user[0]['id']
        return redirect(f'profile/{user[0]["id"]}')
    else:
        flash('Incorrect password!','login')
        return redirect('/')

@app.route("/purchases/<int:user_id>")
def display_purchases(user_id):
    user_with_purchased_cars = User.get_bought_cars({'id':user_id})
    # print("here's the profile holder's info plus purchased cars",user_with_purchased_cars)
    return render_template("purchases.html", user = user_with_purchased_cars)

