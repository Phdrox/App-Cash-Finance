from Database.Tables.Auth import Auth 
from Classes.Auth import Auth as Subscribe
from Classes.Login import Login
from Classes.User import UserFunctions
from flask import request,make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,set_access_cookies
from extension import databaseFlask
from sqlalchemy import select
import json
from flask import Blueprint,jsonify

authroute=Blueprint('auth',__name__)

@authroute.post('/subscribe')
def subscribe():
  request_json=request.get_json()
  try:
    Subscribe(
      request_json.get('username'),
      request_json.get('email'),
      request_json.get('password')
    ).createAuth()
    
    UserFunctions(
      request_json.get('name'),
      0
    ).createUser()
    return json.dumps({"msg":"Conta criada com sucesso"})
  except Exception as e:
    print(e)
    return json.dumps({"erro":"Erro ao tentar criar conta"})

@authroute.post('/login')
def login():
  request_json=request.get_json()
  try:
    return Login(
      request_json.get('username'),
      request_json.get('password')
    ).authenticationUser()
  except Exception as e:
    print(e)
    return json.dumps({
      "erro":"Erro ao logar"
    })

@authroute.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
  identity = get_jwt_identity()
  access_token = create_access_token(identity=identity)
  usernameSelect=select(Auth).where(Auth.id== int(identity))
  getUsername=databaseFlask.session.scalars(usernameSelect).first()
  user_data={
      "id":getUsername.id,
      "username":getUsername.username,
      "email":getUsername.email
    }
  response = make_response(jsonify({'data': user_data}))
  set_access_cookies( response , access_token)
  return response







    

