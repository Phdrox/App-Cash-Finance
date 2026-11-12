from extension import databaseFlask
from Database.Tables.User import User
from sqlalchemy import select
from Utils.pagination import paginationSelectModel
import json

class UserFunctions:
  def __init__(self,name='',admin=0):
    self.name=name
    self.admin=admin

  def createUser(self):
    userModel=User(name=self.name,admin=self.admin)
    databaseFlask.session.add(userModel)
    databaseFlask.session.commit()

  def deleteUser(user_id):
    userModel = User.query.get_or_404(user_id)
    databaseFlask.session.delete(userModel)
    databaseFlask.session.commit()

  def updateUser(self,user_id):
    userModelData= User.query.get_or_404(user_id)
    userModelData.name=self.name
    userModelData.admin=self.admin
    databaseFlask.session.commit()

  def getUser(user_id):
    userModelData=User.query.get_or_404(user_id)
    return json.dump({
      "data":userModelData
    })

  def getUsers():
    usersModelData=databaseFlask.session.scalars(
      select(User)
    )

    paginationSelectModel(usersModelData)



