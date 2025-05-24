from fastapi import FastAPI
from sqlmodel import Session, select
from models import Item
from database import engine, create_db_and_tables


item_1 = Item(name="Banana", quantity=1)
item_2 = Item(name="Apple", quantity=1)
item_3 = Item(name="Yakult", quantity=1)


def create_items():
    with Session(engine) as session:

        session.add(item_1)
        session.add(item_2)
        session.add(item_3)

        session.commit()

def select_items():
    with Session(engine) as session:
        statement = select(Item) # equivalent to SELECT * FROM Item // not exactly * it returns everything needed for the class Item in python,
                                 # db can have excess classes

        s2 = select(Item).where(Item.name == "Apple")

        result = session.exec(statement)
        r2 = session.exec(s2).all()

        results = result.all()  # gives a list of items instead of an iterable
        for item in results:
            print(item, "-----------------item--------------single-----------------")
        print(results, "Item-------------in--------------list")

        items = session.exec(statement).all() # compact version of everything done until this point
        print(r2, "Where-------------Query---------------")


def update_items():
    with Session(engine) as session:
        statement = select(Item).where(Item.name == "Yakult")
        result = session.exec(statement)
        item = result.one()
        print(item, "sdfsdfsd")

        item.quantity = 2
        session.add(item)
        session.commit()
        session.refresh(item)
        print(item)

def delete_items():
    with Session(engine) as session:
        statement = select(Item).where(Item.name == "Banana")
        results = session.exec(statement)
        item = results.one()
        print(item)

        session.delete(item)
        session.commit()

        i = session.exec(select(Item).where(Item.name == "Banana")).first()
        if i is None:
            print("not there")

    

def main():
    create_db_and_tables()
    create_items()
    select_items()
    update_items()
    delete_items()

if __name__ == "__main__":
    main()