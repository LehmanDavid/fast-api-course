from typing import Optional
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    rating: Optional[int] = None  # optional value


myPosts = [
    {"title": "title of post 1 ", "content": "content of post 1", "id": 1},
    {"title": "fav foods ", "content": "i like pizza", "id": 2}
]


@app.get("/")
async def root():
    return {"data": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    return myPosts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(2, 10000000)
    myPosts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"data": post}


def find_post(id: int):
    for post in myPosts:
        if post["id"] == id:
            return post