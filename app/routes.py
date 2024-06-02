from app import app  # Flask app object that will be initialized by __init__
from flask import render_template, flash, redirect, url_for
# forms
from app.forms import LoginForm, RegistrationForm
from app.forms import EditProfileForm
# logging in imports
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
# db imports
from app import db
from app.models import User, Role
import sqlalchemy as sa
# RBAC imports
from flask_principal import Identity, AnonymousIdentity, identity_changed
from flask_principal import identity_loaded, RoleNeed, UserNeed
from flask import session
from .permissions import admin_permission
# redirecting imports
from flask import request
from urllib.parse import urlsplit
# last time visit recording
from datetime import datetime, timezone


# connecting user info provider with flask-principal
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
    else:
        identity.provides.add(RoleNeed('user'))



# protect a view with a principal for that need
@app.route('/admin')
@admin_permission.require()
def do_admin_index():
    return 'Only if you are an admin'


@app.route('/something')
def something():
    name = 'Anon' if current_user.is_anonymous else current_user.username
    return render_template("layout.html", logged_in=True)


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()  # a form object to receive the filled form later
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)  # Keep the user info in the session using Flask-Login

        # Tell Flask-Principal the identity changed
        identity_changed.send(app, identity=Identity(user.id))

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        role = db.session.query(Role).filter_by(name=form.role.data).first()
        new_user = User()
        new_user.username = form.username.data
        new_user.email = form.email.data
        new_user.roles.append(role)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))  # is .scalar() but sends 404 otherwise
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
