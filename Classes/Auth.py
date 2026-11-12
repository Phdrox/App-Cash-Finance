from extension import databaseFlask
from Utils.pagination import paginationSelectModel
from Database.Tables.Auth import Auth as AuthModel
from sqlalchemy import select
import json 
from bcrypt import gensalt,hashpw

class Auth:
  def __init__(self,username='',email='',password=''):
    self.username=username
    self.email=email
    self.password=password
  
  def createAuth(self):
    salt=gensalt()
    authModel=AuthModel(
       username=self.username,
       password=hashpw(self.password.encode('utf-8'), salt).decode('utf-8'),
       email=self.email
    )  
    databaseFlask.session.add(authModel)
    databaseFlask.session.commit()  

    return json.dumps({'message':"Usuário criado"})
  
  def deleteAuth(auth_id):
    authModel = Auth.query.get_or_404(auth_id)
    databaseFlask.session.delete(authModel)
    databaseFlask.session.commit()
  
  def updateAuth(self,auth_id):
    userModelData= Auth.query.get_or_404(auth_id)
    userModelData.password=self.password
    userModelData.email=self.email
    databaseFlask.session.commit()  
  
  def getAuth(auth_id):
    userModelData=Auth.query.get_or_404(auth_id)
    return json.dump({
      "data":userModelData
    })  

  def getAuths():
    usersModelData=databaseFlask.session.scalars(
      select(Auth)
    )  
    paginationSelectModel(usersModelData)


