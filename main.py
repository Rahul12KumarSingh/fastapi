from fastapi import Depends, FastAPI , Response , status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/blog")
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return {
        "statusCode": 200,
        "success": True,
        "blog": {
            "id": new_blog.id,
            "title": new_blog.title,
            "body": new_blog.body,
        },
    }


@app.get("/blog")
def get(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return {
        "statusCode": 200,
        "success": True,
        "blogs": [
            {"id": blog.id, "title": blog.title, "body": blog.body}
            for blog in blogs
        ],
    }


@app.get("/blog/{id}" , status_code=200)
def get_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND

        return { 
            "message": "Blog not found",
        }

    return {
        "success": True,
        "blog": {"id": blog.id, "title": blog.title, "body": blog.body},
    }