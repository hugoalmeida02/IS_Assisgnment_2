from fastapi import FastAPI

from app import models
from app.database import create_db_and_tables
from app.rest.students import router as students_router
from app.rest.courses import router as courses_router
from app.rest.enrollments import router as enrollments_router

app = FastAPI(title="Student Course Management API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {
        "message": "Student-Course REST API is running.",
        "docs": "/docs"
    }


app.include_router(students_router)
app.include_router(courses_router)
app.include_router(enrollments_router)