import app

from Website import create_app
from config import Config
from routes import auth_bp
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

# app.config.from_object(Config)
# mongo = PyMongo(app)
# jwt = JWTManager(app)
#changes made by vamshi
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


