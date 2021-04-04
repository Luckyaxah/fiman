
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

from fiman.utils import redirect_back
from fiman.forms import LoginForm
from fiman.models import Admin, Transaction

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('backend.record'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return redirect_back() # 返回上一页面
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('front.index'))

