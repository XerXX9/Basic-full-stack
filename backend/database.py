from sqlmodel import SQLModel, create_engine

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

postgres_url = "postgresql://advaithm:test123@localhost:5432/postgres"


engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)