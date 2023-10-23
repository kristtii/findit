from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car
import os
from flask import render_template, redirect, session, request, flash, jsonify
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask_cors import CORS
CORS(app)
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add/car')
def addCar():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        return render_template('addCar.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/car', methods=['POST'])
def createCar():
    if 'user_id' in session:        
        
        

        images = request.files.getlist('car_images')
        image_filenames = []

        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                time = datetime.now().strftime("%d%m%Y%S%f")
                time += filename
                filename = time
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filenames.append(filename)
                
        if not Car.validateImage(image_filenames):
            return redirect(request.referrer)
        
        if not Car.validate_car(request.form):
            return redirect(request.referrer)

        data = {
            'car_make': request.form['car_make'],
            'car_model': request.form['car_model'],
            'car_engine': request.form['car_engine'],
            'car_fuel': request.form['car_fuel'],
            'car_transmissions': request.form['car_transmissions'],
            'car_drive': request.form['car_drive'],
            'car_mileage': request.form['car_mileage'],
            'car_price': request.form['car_price'],
            'car_images': ','.join(image_filenames),  # Combine image filenames into a comma-separated string
            'car_description': request.form['car_description'],
            'user_id': session['user_id']
        }
        Car.createCarPost(data)
        return redirect('/dashboard')
    return redirect('/')


@app.route("/cars/edit/<int:id>")
def editCar(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'car_id': id
    }
    loggedUser = User.get_user_by_id(data)
    car = Car.get_car_by_id(data)
    if loggedUser['id'] == car['user_id']:
        return render_template('editCar.html', car=car, loggedUser=loggedUser)
    return redirect(request.referrer)

@app.route('/edit/car/<int:id>', methods=['POST'])
def updatecar(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Car.validate_car(request.form):
        return redirect(request.referrer)

    data = {
            'car_make': request.form['car_make'],
            'car_model': request.form['car_model'],
            'car_engine': request.form['car_engine'],
            'car_fuel': request.form['car_fuel'],
            'car_transmissions': request.form['car_transmissions'],
            'car_drive': request.form['car_drive'],
            'car_mileage': request.form['car_mileage'],
            'car_price': request.form['car_price'],
            'car_description': request.form['car_description'],
            'user_id': session['user_id'],
            'car_id': id
        }
    loggedUser = User.get_user_by_id(data)
    car = Car.get_car_by_id(data)
    if loggedUser['id'] == car['user_id']:
        Car.update_car(data)
        flash('Update succesfull!', 'updateDone')
        return redirect(f'/cars/edit/{id}')
    return redirect('/')

@app.route('/cars/delete/<int:id>')
def deletePost(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'car_id': id
    }
    loggedUser = User.get_user_by_id(data)
    car = Car.get_car_by_id(data)
    if loggedUser['id'] == car['user_id']:
        Car.delete_car_parkedcars(data)
        Car.delete_car(data)
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/save/<int:id>')
def save(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'car_id': id
    }
    usersWhoParkedThiscar = Car.getUserWhoParkedCars(data)
    if session['user_id'] not in usersWhoParkedThiscar:
        Car.save(data)
    return redirect(request.referrer)


@app.route('/unsave/<int:id>')
def removeSaved(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'car_id': id
    }
    usersWhoParkedThiscar = Car.getUserWhoParkedCars(data)
    if session['user_id'] in usersWhoParkedThiscar:
        Car.unsave(data)
    return redirect(request.referrer)

@app.route('/saved')
def savedCars():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    parkedCars = Car.getAllParkedCarsByUser(data)
    print(parkedCars, 'parked cars')
    return render_template('saved.html', parkedCars=parkedCars)

@app.route('/about')
def about():
    return render_template('about.html')