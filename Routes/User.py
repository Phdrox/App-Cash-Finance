from Classes.User import UserFunctions
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
import json 
from flask import Blueprint

userroute=Blueprint('user',__name__)

@userroute.get('/')
@jwt_required()
def getUser():
  idUser=get_jwt_identity()
  request_json=request.get_json()
  try:
    UserFunctions(
      request_json.get('username'),
      request_json.get('email'),
      request_json.get('password')
    ).getUser(idUser)
    
  except Exception as e:
    return json.dumps({
      "erro":"Erro ao tentar criar conta"
    })

@userroute.get('/users')
@jwt_required()
def getAllUsers():
  try:
    UserFunctions().getUsers()

  except Exception as e:
    return json.dumps({
      "error":"Error ao tentar requisitar todos os usuários"
    })

@userroute.put('/updateuser')
@jwt_required()
def upadateUser():
  request_json=request.get_json()
  try:
    idUser=get_jwt_identity()
    UserFunctions(
      request_json.get('name'),
      0
    ).updateUser(idUser)

  except Exception as e:
    return json.dumps({
      "error":"erro ao atualizar usuário"
    })

@userroute.delete('/deleteuser')
@jwt_required()
def deleteUser():
  try:
    idUser=get_jwt_identity()
    UserFunctions().deleteUser(idUser)
    return json.dumps({"message": "Usuário deletado com sucesso"}), 200

  except Exception as e:

    return json.dumps({
      "error":"Error ao tentar deletar usuários"
    }), 500

@userroute.post('/client/<id>')
@jwt_required()
def getClient(id) -> str:
  try:
    return UserFunctions().getUser(id)
  except Exception as e:
    return json.dumps({
      "erro":"Erro ao tentar criar conta"
    })
