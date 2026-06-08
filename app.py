from flask import Flask
from config import Config
from routes.auth import auth_bp
from routes.dashboard import dash_bp
from extensions import db, admin

def create_app():
    
    app = Flask(__name__)

    app.config.from_object(Config)

    #initialize extensions
    db.init_app(app)
    admin.init_app(app)

    #register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    
    return app