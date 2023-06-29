import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    # rating: Optional[int] = None  # optional value


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

myPosts = [
    {"title": "title of post 1 ", "content": "content of post 1", "id": 1},
    {"title": "fav foods ", "content": "i like pizza", "id": 2}
]


def find_post(id: int):
    for post in myPosts:
        if post["id"] == id:
            return post


@app.get("/")
async def root():
    return {"data": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    posts = [dict(zip(col_names, post)) for post in posts]
    return {"data": posts}


# default status code for the method set like this
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    col_names = [desc[0] for desc in cursor.description]
    new_post = [dict(zip(col_names, new_post))]
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    col_names = [desc[0] for desc in cursor.description]
    post = [dict(zip(col_names, post))]
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    myPosts.remove(post)
    # return status code only for delete
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_index = myPosts.index(post)
    myPosts[post_index] = updated_post
    return {"data": updated_post}
