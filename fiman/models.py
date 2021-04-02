from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from fiman.extensions import db

class BaseModel:
    def __str__(self):
        d = vars(self)
        ret = ''
        for key in d:
            ret += key+':'+str(d[key])+'\n'
        return ret

class Admin(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Account(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    owner = db.Column(db.String(30))
    number = db.Column(db.String(30), unique = True)
    bank = db.Column(db.String(20))

    transactions = db.relationship('Transaction', back_populates = 'account')

class Project(db.Model,BaseModel):
    id = db.Column(db.String(30), primary_key = True)
    project_name = db.Column(db.String(50))

    transactions = db.relationship('Transaction', back_populates='project')

class Transaction(db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow, index = True)
    pay = db.Column(db.Integer, default = 0)
    income = db.Column(db.Integer, default = 0)
    balance = db.Column(db.Integer, default = 0)
    oppo_account = db.Column(db.String(30))
    oppo_name = db.Column(db.String(30))
    summary = db.Column(db.String(200))
    
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    project_id = db.Column(db.String(10), db.ForeignKey('project.id'))
    
    account = db.relationship('Account', back_populates='transactions')
    project = db.relationship('Project', back_populates='transactions')







