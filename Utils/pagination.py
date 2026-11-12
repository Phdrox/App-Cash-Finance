from extension import databaseFlask
import json

class PaginationModelSelectStructure:
  modelItems:classmethod
  page:int
  max_items:int

def paginationSelectModel(data:PaginationModelSelectStructure):
  itemsPagination=databaseFlask.paginate(
    data.modelItems,
    page=data.page,
    max_per_page=data.max_items
  )

  return json.dump({
    "data":itemsPagination, 
    "total":itemsPagination.total,
    "page":itemsPagination.page 
  })


   