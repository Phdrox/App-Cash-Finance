from Classes.Data import DataFinanceFunc, CreateFormData
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
import json
from flask import Blueprint

dataroute=Blueprint('data',__name__)

@dataroute.post('/')
@jwt_required()
def createDataFinance():
  try:
    requestData=request.get_json()
    body_data=CreateFormData()
    body_data.name=requestData.get('name')
    body_data.value=requestData.get('value')
    body_data.quantity=requestData.get('quantity')
    body_data.payment=requestData.get('payment')
    body_data.categorie=requestData.get('categorie')
    body_data.type_data=requestData.get('type_data')
    jwtUser=get_jwt_identity()
    return DataFinanceFunc(jwtUser).createDataFinance(body_data)
  
  except Exception as e:
    print(e)
    return json.dumps({
       "error":"Erro ao criar fluxo"
    })

@dataroute.put('/update/<id>')
@jwt_required()
def updateDataFinance(id):
  request_json=request.get_json()
  try:
    jwtUser=get_jwt_identity()

    data_finance=CreateFormData()
    data_finance.categorie=request_json.get('categorie')
    data_finance.name=request_json.get('name')
    data_finance.payment=request_json.get('payment')
    data_finance.type_data=request_json.get('type_data')
    data_finance.value=request_json.get('value')
    data_finance.quantity=request_json.get('quantity')

    return DataFinanceFunc(jwtUser).updateDataFinance(data_finance,id)  
  except Exception as e:
    return json.dumps({"error":"Erro ao atualizar dados"})

@dataroute.delete('/delete/<id>')
@jwt_required()
def deleteDataFinance(id):
  try:
    jwtUser=get_jwt_identity()
    
    DataFinanceFunc(jwtUser).deleteDataFinance(id)
  except Exception as e:
    return json.dumps({"error":"Erro ao deletar dados"})

@dataroute.get('/month')
@jwt_required()
def getMonthDataFinance():
  request_json=request.get_json()
  try:
    jwtUser=get_jwt_identity()
    data_finance=request_json.get('date')
    return DataFinanceFunc(jwtUser,data_finance).getDataFinanceforUserAndDate()
  except Exception as e:
    return json.dumps({"error":"Erro ao buscar dados"})

@dataroute.get('/all')
@jwt_required()
def getAllDataFinance():
  try:
    jwtUser=get_jwt_identity()
    return DataFinanceFunc(jwtUser).getDataFinanceforUser()
  except Exception as e: 
    return json.dumps({"error":"Erro ao buscar dados do usuário"})

@dataroute.get('/categories')
@jwt_required()
def getCategoriesFinance():
  try:
    jwtUser=get_jwt_identity()
    return DataFinanceFunc(jwtUser).categoriesGroup()
  except Exception as e:
    return json.dumps({"error": "Error ao buscar dados"})

@dataroute.get("/percentcategories")
@jwt_required()
def getPercentDataCategories():
  jwtUser= get_jwt_identity()
  try:
   return DataFinanceFunc(jwtUser).percentDataCategorie()
  except Exception as e:
    return json.dumps({"error":"Error ao buscar do usuário"})

@dataroute.get("/flowdata")
@jwt_required()
def getFlowData():
  try:
    jwtUser=get_jwt_identity()
    dataFlow=json.dumps({"data":{
      "amount":DataFinanceFunc(jwtUser).getAmount(),
      "expensive":DataFinanceFunc(jwtUser).getSumFlow(0),
      "gain":DataFinanceFunc(jwtUser).getSumFlow(1)
      }
    })

    return dataFlow
  except Exception as e:
    print(e)
    return json.dumps({"error":"Erro a buscar dados"}) 


