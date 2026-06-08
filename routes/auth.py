from flask import Blueprint, render_template, request, jsonify, redirect, make_response, url_for, flash
import jwt
from functools import wraps
from models import User
from datetime import datetime, timezone, timedelta
from config import Config
import uuid
from extensions import db

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            flash("Please login","error")
            return render_template('login.html')

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.get_user_by_public_id(data['public_id'])
        except:
            flash("Please login", "error")
            return render_template("login.html")

        return f(current_user, *args, **kwargs)

    return decorated


auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/')
def home():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password = password):
            flash('Invalid username or password','error')
            return redirect(url_for('auth.login'))

        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, 
                           Config.SECRET_KEY, algorithm="HS256")

        response = make_response(redirect(url_for('dash.dashboard')))
        response.set_cookie('jwt_token', token)

        return response

    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.get_user_by_email(email)
        if existing_user:
            flash('User already exists', 'warning')
            return redirect(url_for('auth.login'))

        new_user = User(public_id=str(uuid.uuid4()), name=name, email=email)
        new_user.set_password(password)

        new_user.save()
        flash('Registered successfully','success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
@token_required
def logout(current_user):
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('jwt_token')
    return response
