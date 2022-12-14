"""All Routes Are Placed In This File."""
from flask import (
    Blueprint,
    render_template,
    url_for,
    flash,
    redirect,
    request
    )

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
    )

from werkzeug.urls import url_parse

from .extensions import db

from .forms import (
    LoginForm,
    RegistrationForm
    )

from .models import (
    User
    )


bp = Blueprint('', __name__)


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    """Index Route"""
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login Route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register Route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    """Logout Route"""
    logout_user()
    return redirect(url_for('login'))
