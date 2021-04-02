import os
from flask import Flask
from fiman.settings import config


from fiman.extensions import db, bootstrap
from fiman.commands import register_commands
from fiman.models import Admin, Account, Project, Transaction
from fiman.blueprints.backend import backend_bp



def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask('fiman')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)

    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)

def register_blueprints(app):
    app.register_blueprint(backend_bp)

def register_errors(app):
    pass

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Account=Account, Project=Project, Transaction=Transaction)

def register_template_context(app):
    pass
def register_request_handlers(app):
    pass

