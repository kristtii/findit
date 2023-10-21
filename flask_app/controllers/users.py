import math
import random
import smtplib
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt

from .env import ADMINEMAIL
from .env import PASSWORD


bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/loginRegister')

@app.route('/loginRegister', methods=['POST', 'GET'])
def login_register():
    if 'user_id' in session:
        return redirect('/')

    action = request.form.get('action')

    if action == 'register':
        if 'user_id' in session:
            return redirect('/')

        if User.get_user_by_email(request.form):
            flash('This email already exists. Try another one.', 'emailSignUp')
            return redirect(request.referrer)

        if not User.validate_user(request.form):
            return redirect(request.referrer)

        string = '0123456789'
        vCode = ""
        length = len(string)
        for i in range(8) :
            vCode += string[math.floor(random.random() * length)]
        verificationCode = vCode

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']),
            'verification_code': verificationCode
        }
        User.create_user(data)
        
        LOGIN = ADMINEMAIL
        TOADDRS  = request.form['email']
        SENDER = ADMINEMAIL
        SUBJECT = 'Verify Your Email'
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
            % ((SENDER), "".join(TOADDRS), SUBJECT) )
        msg += f'Use this verification code to activate your account: {verificationCode}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()

        user = User.get_user_by_email(data)
        
        session['user_id'] = user['id']
        return redirect('/verify/email')

    elif action == 'login':
        if 'user_id' in session:
            return redirect('/')
        user = User.get_user_by_email(request.form)
        if not user:
            flash('This email does not exist.', 'emailLogin')
            return redirect(request.referrer)
        if not bcrypt.check_password_hash(user['password'], request.form['password']):
            flash('Your password is wrong!', 'passwordLogin')
            return redirect(request.referrer)
        session['user_id'] = user['id']
        return redirect('/verify/email')

    return render_template('login_register.html')

@app.route('/verify/email')
def verifyEmail():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    if user['is_verified'] == 1:
        return redirect('/dashboard')
    return render_template('verify.html', loggedUser = user)

@app.route('/activate/account', methods=['POST'])
def activateAccount():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    if user['is_verified'] == 1:
        return redirect('/dashboard')
    
    if not request.form['verification_code']:
        flash('Verification Code is required', 'wrongCode')
        return redirect(request.referrer)
    
    if int(request.form['verification_code']) != int(user['verification_code']):
        string = '0123456789'
        vCode = ""
        length = len(string)
        for i in range(8) :
            vCode += string[math.floor(random.random() * length)]
        verificationCode = vCode
        dataUpdate = {
            'verification_code': verificationCode,
            'user_id': session['user_id']
        }
        User.updateVerificationCode(dataUpdate)
        LOGIN = ADMINEMAIL
        TOADDRS  = user['email']
        SENDER = ADMINEMAIL
        SUBJECT = 'Verify Your Email'
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
            % ((SENDER), "".join(TOADDRS), SUBJECT) )
        msg += f'Use this verification code to activate your account: {verificationCode}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(LOGIN, PASSWORD)
        server.sendmail(SENDER, TOADDRS, msg)
        server.quit()

        flash('Verification Code is wrong. We just sent you a new one', 'wrongCode')
        return redirect(request.referrer)
    
    User.activateAccount(data)
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/logout')
    cars = Car.get_all()
    return render_template('dashboard.html', loggedUser=loggedUser, cars=cars)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginRegister')
