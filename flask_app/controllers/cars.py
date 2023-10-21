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

# Check if the format is right 
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
        required_fields = {'car_make': 'Make', 'car_model': 'Model', 'car_engine': 'Engine', 'car_fuel': 'Fuel', 'car_transmissions': 'Transmissions', 'car_drive': 'Drive', 'car_mileage': 'Mileage', 'car_price': 'Price'}

        for field, display_name in required_fields.items():
            if not request.form.get(field):
                flash(f'{display_name} is required!', 'carImage')
                return redirect(request.referrer)

        if not request.files['car_images']:
            flash('Car image is required!', 'carImage')
            return redirect(request.referrer)

        image = request.files['car_images']
        if not allowed_file(image.filename):
            flash('Image should be in png, jpg, jpeg format!', 'carImage')
            return redirect(request.referrer)

        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        data = {
            'car_make': request.form['car_make'],
            'car_model': request.form['car_model'],
            'car_engine': request.form['car_engine'],
            'car_fuel': request.form['car_fuel'],
            'car_transmissions': request.form['car_transmissions'],
            'car_drive': request.form['car_drive'],
            'car_mileage': request.form['car_mileage'],
            'car_price': request.form['car_price'],
            'car_images': filename1,
            'car_description': request.form['car_description'],
        }
        Car.createCarPost(data)
        return redirect('/dashboard')
    return redirect('/')
