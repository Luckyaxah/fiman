from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

from fiman.utils import redirect_back
from fiman.forms import LoginForm
from fiman.models import Admin, Transaction

front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def index():
    return render_template('front.html')

