import os

from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE'),
        SECRET_KEY = os.environ.get('SECRET_KEY')
    )

    from . import db
    db.init_app(app)

    from . import usuario
    app.register_blueprint(usuario.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import alumno
    app.register_blueprint(alumno.bp)

    from . import profesor
    app.register_blueprint(profesor.bp)
    
    return app