from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production

        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .users import users_bp as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from .api_v1 import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    @app.route('/')
    def index():
        redirect(url_for('users.index'))

    return app
