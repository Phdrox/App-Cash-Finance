from extension import databaseFlask as db
from sqlalchemy.orm import Mapped,mapped_column

class User(db.Model):
  __tablename__='users'

  id:Mapped[int]= mapped_column(primary_key=True)
  name:Mapped[str]= mapped_column(nullable=False)
  admin:Mapped[bool]= mapped_column(nullable=False)




