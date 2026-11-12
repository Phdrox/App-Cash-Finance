from Database.Tables.Auth import Auth
from extension import databaseFlask
from sqlalchemy import select
from bcrypt import checkpw
import json 
from flask_jwt_extended import create_access_token,set_access_cookies,create_refresh_token,set_refresh_cookies
from flask import make_response

def getUsernameDatabase(username):
  usernameSelect=select(Auth).where(Auth.username==username)
  getUsername=databaseFlask.session.scalars(usernameSelect).first()

  return getUsername

def verifyPassword(password,hash_pass):
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    if isinstance(hash_pass, str):
        hash_pass = hash_pass.encode('utf-8')
        
    return checkpw(password, hash_pass)


def verifyLogin(username,password):
  getUsername=getUsernameDatabase(username)
  
  if getUsername:
    if verifyPassword(password,getUsername.password):
      return True
  else:
    return json.dumps({"error":"Usuário Incorreto"})

class Login:
  def __init__(self,username,password):
    self.username=username
    self.password=password

  def authenticationUser(self):
    verifyLogin(self.username,self.password)
    responseDatabase=getUsernameDatabase(self.username)

    user_data={
      "id":responseDatabase.id,
      "username":responseDatabase.username,
      "email":responseDatabase.email
    }
    responseAuth = make_response(json.dumps({"data": user_data}))
    access_token = create_access_token(identity= str(user_data["id"]))
    refresh_token=create_refresh_token(identity= str(user_data["id"]))
    set_access_cookies(responseAuth, access_token)
    set_refresh_cookies(responseAuth, refresh_token)

    return responseAuth
   

  

    
    

    




     
