from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Availability
from routes import availability_bp
from config import Config
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TimeField 
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = b"%\xf6v\xeb'\x98w\xa2\xdb\x8f9\x82\xff\x86\xb9\xe6\x08w\x05\x15|\x05\xeb\xe2" 

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AvailabilityForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])  
    start_time = TimeField('Start Time', validators=[DataRequired()])  
    end_time = TimeField('End Time', validators=[DataRequired()])  
    submit = SubmitField('Create Availability')


app.register_blueprint(availability_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#definig new admin dashboard
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('user_dashboard'))

    form = AvailabilityForm()
    if form.validate_on_submit():
        date = form.date.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        new_availability = Availability(date=date, start_time=start_time, end_time=end_time)
        db.session.add(new_availability)
        db.session.commit()
        flash('Availability created!', 'success')

    availabilities = Availability.query.all()
    return render_template('admin.html', form=form, availabilities=availabilities, username=current_user.username)

#defining new user dashboard
@app.route('/user_dashboard')
@login_required
def user_dashboard():
    availabilities = Availability.query.all()
    return render_template('user_dashboard.html', availabilities=availabilities, username=current_user.username)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
