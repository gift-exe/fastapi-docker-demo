from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
import json

#from . import crud, models, schemas
#from .database import SessionLocal, engine

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {'message': 'hello world :)'}


@app.post("/items/")
async def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    try:
        db_item = crud.get_item_by_name(db, name=item.name)
        if db_item:
            raise HTTPException(status_code=400, detail=json.dumps({'error':'Item Already Exist'}))
        
        db_item = crud.create_item(db=db, item=item)
        item_dict = schemas.Item.to_dict(db_item).model_dump()
        return Response(status_code=201, 
                        content=json.dumps({'message':'Item Created Successfully', 
                                            'details':item_dict}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        items = crud.get_items(db, skip=skip, limit=limit)
        return Response(status_code=200, 
                        content=json.dumps({'items':items}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': str(e)}))

@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db_item = crud.get_item_by_id(db=db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=400, detail=json.dumps({'error':'Item Does Not Exist'}))
        
        return Response(status_code=200, 
                        content=json.dumps({'item':db_item}))
    except Exception as e:
        raise HTTPException(status_code=400, detail={'message':'An Error Occured', 'error': str(e)})

@app.put("/items/{item_id}")
async def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    try:
        db_item = crud.get_item_by_id(db=db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=400, detail=json.dumps({'error':'Item Does Not Exist'}))
        
        db_item = crud.update_item(db=db, item_id=item_id, item_update=item_update)
        item_dict = schemas.Item.to_dict(db_item).model_dump()
        return Response(status_code=200, 
                        content=json.dumps({'message':'Item Updated Successfully', 
                                            'item':item_dict}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': {str(e)}}))

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db_item = crud.get_item_by_id(db=db, id=item_id)
        if db_item is None:
            raise HTTPException(status_code=400, detail=json.dumps({'error':'Item Does Not Exist'}))
        
        db_item = crud.delete_item(db=db, item_id=item_id)
        item_dict = schemas.Item.to_dict(db_item).model_dump()
        return Response(status_code=200, 
                        content=json.dumps({'message':'Item Deleted Successfully', 
                                            'item':item_dict}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=json.dumps({'message':'An Error Occured', 'error': {str(e)}}))
