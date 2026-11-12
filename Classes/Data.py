from extension import databaseFlask
from Database.Tables.Data import DataFinance
from sqlalchemy import select, func


def percentData(number, amount):
    if amount == 0:
        return 0.0
    if abs(number) >= abs(amount):
        return 100.0
        
    return (abs(number) / abs(amount)) * 100

def sumExpensesFlowCategories(id, categorie):
    sum_value = databaseFlask.session.scalar(
        select(func.coalesce(func.sum(DataFinance.value), 0.0)).where(
            DataFinance.type_data == False, 
            DataFinance.categorie == categorie,
            DataFinance.id_user == int(id)
        )
    )
    return float(sum_value) if sum_value is not None else 0.0

def listCategories(categories, amount, id):
    dataArrayCategorie = []
    
    for categorie in categories:
        sumValues = sumExpensesFlowCategories(id, categorie)
        percentCategorie = percentData(sumValues, amount)
        dataArrayCategorie.append({
            "categorie": categorie,
            "value": round(percentCategorie,2) 
        })

    return dataArrayCategorie

class CreateFormData:
    name: str
    value: float
    quantity: int
    payment: str
    categorie: str
    type_data: bool

class DataFinanceFunc:
    def __init__(self, id):
        self.id = id

    def createDataFinance(self, form: CreateFormData):
        dataCreate = DataFinance(
            id_user=int(self.id),
            name=form.name,
            value=form.value,
            quantity=form.quantity,
            payment=form.payment,
            categorie=form.categorie,
            type_data=form.type_data
        )

        databaseFlask.session.add(dataCreate)
        databaseFlask.session.commit()

        return {"message": "Data criado com sucesso"}

    def updateDataFinance(self, data_finance: CreateFormData, id_finance):
        dataFinance = DataFinance.query.get_or_404(id_finance)
        dataFinance.name = data_finance.name
        dataFinance.value = data_finance.value
        dataFinance.quantity = data_finance.quantity
        dataFinance.payment = data_finance.payment
        dataFinance.categorie = data_finance.categorie
        dataFinance.type_data = bool(data_finance.type_data)
        databaseFlask.session.commit() 

        return {"message": "Dados atualizados com successo"}

    def deleteDataFinance(self, id_finance):
        getFinanceforId = DataFinance.query.get_or_404(id_finance)
        databaseFlask.session.delete(getFinanceforId)
        databaseFlask.session.commit()
        
        return {"message": "Dados deletados com successo"}
    
    def getDataFinanceforUser(self):
        databaseQuery = select(DataFinance).where(DataFinance.id_user == int(self.id))
        records = databaseFlask.session.scalars(databaseQuery).all()
  
        return [
            {
                "id": r.id,
                "name": r.name,
                "value": r.value,
                "quantity": r.quantity,
                "payment": r.payment,
                "categorie": r.categorie,
                "type_data": r.type_data,
                "create_at": str(r.create_at) if r.create_at else None
            } for r in records
        ]

    def getSumFlow(self, type_val):
        # Use .scalar() to return a single float/int number instead of a ScalarResult
        sum_value = databaseFlask.session.scalar(
            select(func.coalesce(func.sum(DataFinance.value), 0.0)).where(
                DataFinance.type_data == bool(type_val),
                DataFinance.id_user == int(self.id)
            )
        )
        print(sum_value)
        quantity=databaseFlask.session.scalar(select(
          DataFinance.quantity).where(
          DataFinance.type_data == bool(type_val),
          DataFinance.id_user == int(self.id)                                             
        ))

        return float(sum_value) * quantity  if sum_value is not None else 0.0

    def getAmount(self):
        total_income = self.getSumFlow(1)
        total_expense = self.getSumFlow(0)
        return total_income - total_expense

    def categoriesGroup(self):
        databaseQuery = select(DataFinance.categorie).where(
            DataFinance.id_user == int(self.id)
        ).distinct()
        return databaseFlask.session.scalars(databaseQuery).all()

    def percentDataCategorie(self):
        categories = self.categoriesGroup()
        amountValues = self.getAmount()
        return listCategories(categories, amountValues, self.id)

    def getDataFinanceforUserAndDate(self, date):
        databaseQuery = select(DataFinance).where(
            DataFinance.id_user == int(self.id),
            DataFinance.create_at == date
        )
        records = databaseFlask.session.scalars(databaseQuery).all()
        return [
            {
                "id": r.id,
                "name": r.name,
                "value": r.value,
                "quantity": r.quantity,
                "payment": r.payment,
                "categorie": r.categorie,
                "type_data": r.type_data,
                "create_at": str(r.create_at) if r.create_at else None
            } for r in records
        ]
  
  

  
    

  
  

  

    

     
  