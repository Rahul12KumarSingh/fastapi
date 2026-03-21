from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/health-check")
def health_check():
    return { "statusCode" : 200 , "success" : "true"}

@app.get("/blog")
def getBlogs(limit : int = 10 , published : bool = True):
    return { "limit": limit , "published" : published , "blogs" : f"Blogs with limit {limit} and published {published}" }

@app.get("/blog/{blog_id}")
def getBlog(blog_id: int):
    return { "blog_id" : blog_id }

@app.get("/blog/{blog_id}/comments")
def getComments(blog_id : int):
    return { "blog_id" : blog_id , "comments" : ["comment1" , "comment2" , "comment3"] }


class  Blog(BaseModel):
    title: str
    content: str
    published: bool

@app.post("/blog")
def createBlog(blog  : Blog):
    return { "blog_details": blog , "message" : "Blog created successfully" }

