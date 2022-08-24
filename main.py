from sqlalchemy.orm import Session

import models
import schemas
from database import Base, SessionLocal, engine
from fastapi import Body, Depends, FastAPI

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

# fakeDatabase = {
#     1:{'task':'Wash car'},
#     2:{'task':'Bathe dog'},
#     3:{'task':'Write blog'},
#     4:{'task':'Keep coding'},
# }

@app.get('/')
def getITems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get('/{id}')
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


#Option # 1
# @app.post("/")
# def addItem(task:str):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task":task}
#     return fakeDatabase


# Option #2
@app.post("/")
def addItem(item:schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# Option #3
# @app.post("/")
# def addItem(body = Body()):
#    newId = len(fakeDatabase.keys()) + 1
#    fakeDatabase[newId] = {"task":body['task']}
#    return fakeDatabase


@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


@app.delete("/{id}")
def deleteItem(id:int, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'
