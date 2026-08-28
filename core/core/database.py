from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import SQLALCHEMY_POSTGRES_DATABASE_URL


engine = create_engine(SQLALCHEMY_POSTGRES_DATABASE_URL)

class Base(DeclarativeBase):
    pass

def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()