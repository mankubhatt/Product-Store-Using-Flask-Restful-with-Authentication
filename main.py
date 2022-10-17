from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from resource.auth import Login, Register, RefreshToken
from resource.product import Product, AllProducts, Search
from dotenv import load_dotenv, find_dotenv
from models.db import db
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#setting .env
load_dotenv(find_dotenv())

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

api.add_resource(Register, "/signup")
api.add_resource(Login, "/login")
api.add_resource(RefreshToken, "/refresh")
api.add_resource(Product, "/product/<int:p_id>")
api.add_resource(AllProducts, "/products")
api.add_resource(Search, "/search")

if __name__ == "__main__":
    app.run(debug=True)