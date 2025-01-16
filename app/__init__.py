from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager


from app.extensions import db
from app.auth.routes import auth
from app.buy.routes import main

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt = JWTManager(app)
    
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    
    return app
