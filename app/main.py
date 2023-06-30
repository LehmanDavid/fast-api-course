import time
from fastapi import FastAPI
import psycopg
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg.connect(
            "dbname=fastapi-course user=postgres host=localhost port=5432 password=postgres")
        cursor = conn.cursor()
        print("connected to db")
        break
    except Exception as e:
        print(e)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"data": "This is an example of crud app with fastapi"}
