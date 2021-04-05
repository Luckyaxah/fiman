

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from fiman.models import Account, Transaction, Project

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class PostForm(FlaskForm):
    pay = StringField('Pay')
    income = StringField('Income')
    balance = StringField('Balance')
    oppo_account = StringField('Account Number')
    oppo_name = StringField('Account Name')
    summary = CKEditorField('Summary')
    project_id = SelectField('Project')
    account_id = SelectField('Account')
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.project_id.choices = [(project.id, project.project_name)
                                    for project in Project.query.order_by(Project.project_name).all()]
        self.account_id.choices = [(account.id, account.number)
                                    for account in Account.query.order_by(Account.number).all()]
