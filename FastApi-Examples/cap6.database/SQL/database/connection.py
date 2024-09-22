from sqlmodel import SQLModel,Session,create_engine
from models.events import Event

# Connection

database_file = "apiDatabas.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread":False}
engine_url = create_engine(database_connection_string,echo=True,connect_args=connect_args)

def conn() -> None:
    SQLModel.metadata.create_all(engine_url)

def get_session() -> None:
    with Session(engine_url) as session:
        yield session