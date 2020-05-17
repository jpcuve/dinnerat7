import logging
from pathlib import Path
from types import ModuleType

from flask import Flask, redirect

from dinnerat7.database import db, find_dating_events

logger = logging.getLogger(__name__)


def read_configuration(extension: str = None):
    filename = 'config.py'
    if extension is not None:
        filename = f'{filename[:-3]}-{extension}.py'
    logger.info(f"Using config file: {filename}")
    d = ModuleType("config")
    config_path = Path(__file__).parent.parent / filename
    d.__file__ = str(config_path)
    with config_path.open(mode='rb') as config_file:
        exec(compile(config_file.read(), filename, "exec"), d.__dict__)
    config = {key: getattr(d, key) for key in dir(d) if key.isupper()}
    return config


def create_app(profile: str = None):
    app = Flask(__name__)
    app.config.update(read_configuration(profile))
    db.init_app(app)
    from dinnerat7.ext.ext_mail import mailer
    mailer.init_app(app)
    from dinnerat7.ext.ext_stripe import stripe
    stripe.init_app(app)

    if app.config.get('TESTING', True):
        with app.app_context():
            db.create_all()
            connection = db.engine.connect()
            with open(Path(__file__).parent / 'data.sql', 'rb') as resource:
                sql = str(resource.read(), 'utf8')
                for statement in sql.split(';'):
                    with connection.begin() as transaction:
                        try:
                            connection.execute(statement)
                            transaction.commit()
                        except Exception as e:
                            app.logger.error(e)
                            transaction.rollback()

    from dinnerat7.api import api_web
    app.register_blueprint(api_web.bp)

    @app.route('/')
    def api_home():
        return redirect('/api/web')

    return app
