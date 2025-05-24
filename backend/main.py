from fastapi import FastAPI
from sqlmodel import Session, select
from models import Item
from database import engine, create_db_and_tables

def add_items(item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

def select_items():
    with Session(engine) as session:
        data = session.exec(select(Item)).all()
        return data
        # statement = select(Item) # equivalent to SELECT * FROM Item // not exactly * it returns everything needed for the class Item in python,
        #                          # db can have excess classes

        # s2 = select(Item).where(Item.name == "Apple")

        # result = session.exec(statement)
        # r2 = session.exec(s2).all()

        # results = result.all()  # gives a list of items instead of an iterable
        # for item in results:
        #     print(item, "-----------------item--------------single-----------------")
        # print(results, "Item-------------in--------------list")

        # items = session.exec(statement).all() # compact version of everything done until this point
        # print(r2, "Where-------------Query---------------")

        


def update_items(item_no: int, updated_item: Item):
    with Session(engine) as session:
        val_to_be_updated = session.exec(select(Item).where(Item.id == item_no)).one()
        val_to_be_updated.quantity = updated_item.quantity
        val_to_be_updated.name = updated_item.name

        session.commit()
        session.refresh(val_to_be_updated)

        return val_to_be_updated



        # statement = select(Item).where(Item.name == "Yakult")
        # result = session.exec(statement)
        # item = result.one()
        # print(item, "sdfsdfsd")

        # item.quantity = 2
        # session.add(item)
        # session.commit()
        # session.refresh(item)
        # print(item)

def delete_items(item_id: int):
    with Session(engine) as session:
        val_to_be_deleted = session.exec(select(Item).where(Item.id == item_id)).one()
        
        session.delete(val_to_be_deleted)
        session.commit()


        # statement = select(Item).where(Item.name == "Banana")
        # results = session.exec(statement)
        # item = results.one()
        # print(item)

        # session.delete(item)
        # session.commit()

        # i = session.exec(select(Item).where(Item.name == "Banana")).first()
        # if i is None:
        #     print("not there")


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def get_req():
    data =  select_items()
    return data

@app.post("/")
def post_req(item: Item):
    item = add_items(item)
    return {"message": "Item received", "item": item}

@app.put("/{item_id}")
def put_req(item_id: int, updated_item: Item):
    return update_items(item_id, updated_item)

@app.delete("/{item_id}")
def delete_req(item_id: int):
    id = item_id
    delete_items(item_id)
    return {"detail": f"Item with ID {id} deleted"}