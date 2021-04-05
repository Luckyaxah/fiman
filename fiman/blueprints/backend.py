
from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required

from fiman.extensions import db
from fiman.models import Transaction, Account, Project
from fiman.forms import PostForm
from fiman.utils import redirect_back

backend_bp = Blueprint('backend', __name__)

@backend_bp.before_request
@login_required
def login_protect():
    # 给整个蓝本增加登录保护
    pass

@backend_bp.route('/')
def record():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['FIMAN_RECORD_PER_PAGE']
    pagination = Transaction.query.order_by(Transaction.timestamp.desc()).paginate(page, per_page=per_page)
    transactions = pagination.items
    return render_template('record.html', pagination = pagination, transactions=transactions)

 
@backend_bp.route('/manage')
def manage_record():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['FIMAN_RECORD_PER_PAGE']
    pagination = Transaction.query.order_by(Transaction.timestamp.desc()).paginate(page, per_page=per_page)
    transactions = pagination.items
    return render_template('backend/manage_record.html', pagination = pagination, transactions=transactions)

@backend_bp.route('/new',methods=['GET','POST'])
def new_transaction():
    import datetime
    form = PostForm()
    if form.validate_on_submit():
        pay = form.pay.data
        income = form.income.data
        balance = form.balance.data
        oppo_account = form.oppo_account.data
        oppo_name = form.oppo_name.data
        summary = form.summary.data

        account = Account.query.get(form.account_id.data)
        project = Project.query.get(form.project_id.data)
        transaction = Transaction(pay=pay, income=income, balance=balance, oppo_account=oppo_account, 
        oppo_name=oppo_name, summary=summary, account=account, project=project)
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction created.', 'success')
    return render_template('backend/new_transaction.html', form=form)



@backend_bp.route('/<int:transaction_id>/edit', methods=['GET','POST'])
def edit_transaction(transaction_id):
    form = PostForm()
    print(transaction_id)
    transaction = Transaction.query.get_or_404(transaction_id)
    if form.validate_on_submit():
        # 修改Transaction字段
        transaction.pay = form.pay.data
        transaction.income = form.income.data
        transaction.balance = form.balance.data

        transaction.oppo_account = form.oppo_account.data
        transaction.oppo_name = form.oppo_name.data
        transaction.summary = form.summary.data

        transaction.account = Account.query.get(form.account_id.data)
        transaction.project = Project.query.get(form.project_id.data)

        db.session.commit()
        flash('Transaction updated.', 'success')
        return redirect(url_for('backend.manage_record', transaction_id=transaction.id))
    form.pay.data = transaction.pay
    form.income.data = transaction.income
    form.balance.data = transaction.balance

    form.oppo_account.data = transaction.oppo_account
    form.oppo_name.data = transaction.oppo_name
    form.summary.data = transaction.summary

    form.account_id.data = transaction.account.id
    form.project_id.data = transaction.project.id

    return render_template('backend/edit_transaction.html', form=form)


@backend_bp.route('/<int:transaction_id>/delete', methods=['POST'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted.', 'success')
    return redirect_back()
