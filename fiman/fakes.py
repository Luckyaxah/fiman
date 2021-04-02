
import random
import string
from faker import Faker

from fiman.extensions import db
from fiman.models import Admin, Account, Transaction, Project
from sqlalchemy.exc import IntegrityError



faker = Faker(locale = 'zh_CN')

def fake_admin():
    admin = Admin(
        username = 'admin',
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()

def fake_account(count=3):
    for i in range(count):
        account = Account(
            owner = faker.name(),
            number = faker.bban(),
            bank = faker.iban()
        )
        db.session.add(account)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_project(count=5):
    for i in range(count):
        ran_str = ''.join(random.sample(string.digits, 3))
        project = Project(
            id = 'S-'+ ran_str,
            project_name = faker.word(),
        )
        db.session.add(project)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_transaction(count =50):
    projects = Project.query.all()


    for i in range(count):
        flag = random.random()>0.5
        rindex = random.randint(1, Project.query.count())-1
        project_id = projects[rindex].id
        transaction = Transaction(
            timestamp = faker.date_this_year(),
            pay = random.randint(1,1000) if flag else 0,
            income = random.randint(1,1000) if not flag else 0,
            balance = 0,
            oppo_account = faker.bban(),
            oppo_name = faker.name(),
            summary = faker.sentence(),
            account = Account.query.get(random.randint(1, Account.query.count())),
            project = Project.query.get(project_id)
        )
        db.session.add(transaction)
    db.session.commit()

