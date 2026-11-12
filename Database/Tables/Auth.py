from extension import databaseFlask as db
from sqlalchemy.orm import Mapped,mapped_column

class Auth(db.Model):
  __tablename__='auth'

  id:Mapped[int]=mapped_column(primary_key=True)
  username:Mapped[str]=mapped_column(unique=True,nullable=False)
  password:Mapped[str]=mapped_column(nullable=False)
  email:Mapped[str]= mapped_column(unique=True,nullable=False)

