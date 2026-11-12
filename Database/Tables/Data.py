
from sqlalchemy import ForeignKey,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column
from extension import databaseFlask as db
import datetime

class DataFinance(db.Model):
  __tablename__='data'

  id:Mapped[int]=mapped_column(primary_key=True)
  id_user:Mapped[int]=mapped_column(ForeignKey('users.id'))
  name:Mapped[str]=mapped_column(nullable=False)
  value:Mapped[float]=mapped_column(nullable=False)
  quantity:Mapped[int]=mapped_column(nullable=False)
  payment:Mapped[str]=mapped_column(nullable=False)
  categorie:Mapped[str]=mapped_column(nullable=False)
  type_data:Mapped[bool]=mapped_column(nullable=False)
  create_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

