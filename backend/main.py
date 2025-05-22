from fastapi import FastAPI
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, )
    name: str
    quantity: int | None = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

item_1 = Item(name="Banana", quantity=1)
item_2 = Item(name="Apple", quantity=1)
item_3 = Item(name="Yakult", quantity=1)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

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

        result = session.exec(statement)
        results = result.all()  # gives a list of items instead of an iterable
        for item in result:
            print(item)
        print(results)

        items = session.exec(statement).all() # compact version of everything done until this point

def main():
    create_db_and_tables()
    create_items()
    select_items()

if __name__ == "__main__":
    main()