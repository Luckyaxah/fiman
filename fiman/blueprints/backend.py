
from flask import Blueprint, render_template, request, current_app
from fiman.models import Transaction
from flask_login import login_required

backend_bp = Blueprint('backend', __name__)

@backend_bp.before_request
@login_required
def login_protect():
    # 给整个蓝本增加登录保护
    pass

@backend_bp.route('/record')
def record():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['FIMAN_RECORD_PER_PAGE']
    pagination = Transaction.query.order_by(Transaction.timestamp.desc()).paginate(page, per_page=per_page)
    transactions = pagination.items
    return render_template('record.html', pagination = pagination, transactions=transactions)