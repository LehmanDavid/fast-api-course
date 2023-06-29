from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

def find_post(id: int):
    for post in myPosts:
        if post["id"] == id:
            return post


@app.get("/")
async def root():
    return {"data": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    return myPosts


@app.post("/posts", status_code=status.HTTP_201_CREATED) # default status code for the method set like this
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


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    myPosts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # return status code only for delete


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_index = myPosts.index(post)
    myPosts[post_index] = updated_post
    return {"data": updated_post}