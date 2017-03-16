from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prj_model import Base

#----------------------------
# Turn Foreign Key Constraints ON for
# each connection.
#----------------------------

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

#----------------------------
# Create the engine
#----------------------------


db = create_engine('sqlite:///project.db')


def session_create():
    return sessionmaker(bind=db)()

if __name__ == "__main__":
    Base.metadata.bind = db
    Base.metadata.create_all()

