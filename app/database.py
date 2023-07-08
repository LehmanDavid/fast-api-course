from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_password: str
    database_user: str = 'postgres'
    database_name: str = 'fastapi-course'

    class Config:
        env_file = '.env' 
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi-course"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# connection for raw sql queries using psycopg
# while True:
#     try:
#         conn = psycopg.connect(
#             "dbname=fastapi-course user=postgres host=localhost port=5432 password=postgres")
#         cursor = conn.cursor()
#         print("connected to db")
#         break
#     except Exception as e:
#         print(e)
#         time.sleep(2)