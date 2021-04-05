import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from fiman.settings import config
from fiman.extensions import db, bootstrap, login_manager, csrf, ckeditor
from fiman.commands import register_commands
from fiman.models import Admin, Account, Project, Transaction

from fiman.blueprints.front import front_bp
from fiman.blueprints.auth import auth_bp
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
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)


def register_blueprints(app):
    app.register_blueprint(front_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(backend_bp, url_prefix='/record')

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Account=Account, Project=Project, Transaction=Transaction)

def register_template_context(app):
    pass
def register_request_handlers(app):
    pass

