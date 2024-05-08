from urllib.parse import urlparse, urljoin
from sqlalchemy.exc import IntegrityError
from flask import render_template, url_for, request, flash, redirect, Blueprint
from flask_login import login_required, current_user, logout_user, login_user
from recipe_app.database import db
from recipe_app.models import User, Recipe

from recipe_app.users.forms import LoginForm, UpdateForm, RegistrationForm
from recipe_app.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)


def is_safe_url(target):

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please Choose a different username')
            return redirect(url_for('users.register'))
        else:

            try:

                user = User(email=form.email.data,
                            username=form.username.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Thanks for the Registration')
                return redirect(url_for('users.login'))
            except IntegrityError:
                db.session.rollback()
                flash("An error occurred during registration. Please try again.")
                return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid email or password', 'error')
    #         return redirect(url_for('users.login'))
        
    #     login_user(user, remember=form.remember_me.data)

    #     next_page = request.args.get('next')
    #     if not next_page or not is_safe_url(next_page):
    #         next_page = url_for('core.index')

    #     return redirect(next_page)

    # return render_template('login.html', form=form)
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Log in Success!')
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('core.index'))
    return render_template('login.html', form=form)



@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for(
        'static', filename='/profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route('/<username>')
def user_recipes(username):

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    recipes = Recipe.query.filter_by(author=user).order_by(
        Recipe.rating.desc()).paginate(page=page, per_page=7)
    return render_template('user_recipes.html', recipes=recipes, user=user)










