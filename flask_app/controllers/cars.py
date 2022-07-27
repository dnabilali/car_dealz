from flask_app.models.car import Car
from flask_app import app
from flask import redirect, render_template, session, request, flash

@app.route("/create" , methods = ['POST'])
def create_car():
    data = {
        "price": request.form["price"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "seller_id": session["user_id"]
    }
    if Car.validate_car(data):
        Car.save(data)
        return redirect(f"/profile/{session['user_id']}")
    else:
        return redirect("/new")

@app.route("/new")
def new_car():
    return render_template("new.html")

@app.route("/cars/<int:car_id>")
def display_one_car(car_id):
    return render_template("display_car.html", one_car = Car.get_car_by_id({'id': car_id}))

@app.route("/delete/<int:car_id>")
def delete_car(car_id):
    Car.delete({'id':car_id})
    return redirect(f"/profile/{session['user_id']}")

@app.route("/edit/<int:car_id>")
def edit_car(car_id):
    one_car = Car.get_car_by_id({'id':car_id})
    if 'user_id' in session and session['user_id'] == one_car[0]['seller_id']:
        # print("the show's info from db is:" , Show.get_show_by_id({"id": show_id}))
        return render_template("edit.html", one_car = Car.get_car_by_id({'id': car_id}))
    else:
        flash('Unauthorized use! Please sign in first!','login')
        return redirect('/')

@app.route("/update/<int:car_id>", methods = ['POST'])
def update_show(car_id):
    if Car.validate_car(request.form):
        Car.update(request.form, car_id)
        return redirect(f"/profile/{session['user_id']}")
    else:
        return redirect(f"/edit/{car_id}")

@app.route("/purchase/<int:car_id>", methods = ['POST'])
def purchase(car_id):
    Car.purchase_car({'buyer_id': session['user_id']}, car_id)
    return redirect(f"/profile/{session['user_id']}")


    
