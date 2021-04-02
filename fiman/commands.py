import click
from fiman.extensions import db
from fiman.models import Admin, Account, Transaction

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help = 'Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', about = True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
    
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        click.echo('Initialzing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username = username,
            )
            admin.set_password(password)
            db.session.add(admin)

        account = Account.query.first()
        if account is None:
            click.echo("Creating the default bank..")
            account = Account(
                owner = 'Axah',
                number = '000000000000000000000000',
                bank = 'ICBC'
            )
            db.session.add(account)

        account = Account.query.first()
        if account is None:
            click.echo("Creating the default bank..")
            account = Account(
                owner = 'Axah',
                number = '000000000000000000000000',
                bank = 'ICBC'
            )
            db.session.add(account)


        transaction = Transaction.query.first()
        if transaction is None:
            click.echo("Creating the default transaction.")
            transaction = Transaction(
                pay = 10000,
                income = 0,
                oppo_account = '111111111',
                oppo_name = 'Jack',
                summary = 'salary',
            )
            db.session.add(transaction)
    
        db.session.commit()
        click.echo('Done.')


    @app.cli.command()
    @click.option('--account', default=3, help = '..')
    @click.option('--project', default = 5, help = '..')
    @click.option('--transaction', default = 50, help = '..')
    def forge(account, project, transaction):
        from fiman.fakes import fake_admin, fake_account, fake_project, fake_transaction

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d account' % account)
        fake_account(account)

        click.echo('Generating %d project...' % project)
        fake_project(project)

        click.echo('Generating %d transaction...' % transaction)
        fake_transaction(transaction)

        click.echo('Done.')
