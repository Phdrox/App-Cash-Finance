from flask import Flask 
import os
from dotenv import load_dotenv
from extension import databaseFlask
from flask_jwt_extended import JWTManager
import datetime

load_dotenv()
app =Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_ACCESS_TOKEN_EXPIRES']=datetime.timedelta(minutes=30)
app.config["JWT_TOKEN_LOCATION"]=["headers", "cookies", "json", "query_string"]
app.config["JWT_SECRET_KEY"]=os.environ.get('SECRET_KEY')
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_HTTPONLY"]=True
app.config["JWT_COOKIE_SECURE"] = False

jwt=JWTManager(app)

from Routes.Auth import authroute
from Routes.Data import dataroute
from Routes.User import userroute
app.register_blueprint(authroute,url_prefix='/auth')
app.register_blueprint(dataroute,url_prefix='/data')
app.register_blueprint(userroute,url_prefix='/user')



databaseFlask.init_app(app)
from Database.Tables import *

with app.app_context():
  
  databaseFlask.create_all()

if __name__ =='__main__':
  app.run(debug=True)



