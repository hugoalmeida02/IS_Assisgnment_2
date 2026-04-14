from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app import models
from app.database import create_db_and_tables
from app.rest.students import router as students_router
from app.rest.courses import router as courses_router
from app.rest.enrollments import router as enrollments_router
from app.agent.chat_agent import ask_agent, reset_agent_memory, agent_lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    async with agent_lifespan():
        yield


app = FastAPI(title="Student Course Management API", lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str


templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root():
    return {
        "message": "Student-Course REST API is running.",
        "docs": "/docs",
        "ui": "/ui",
    }


@app.get("/ui")
def ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = await ask_agent(request.message)
    return {"response": response}


@app.post("/reset")
async def reset_endpoint():
    reset_agent_memory()
    return {"status": "Conversation history reset successfully."}


app.include_router(students_router)
app.include_router(courses_router)
app.include_router(enrollments_router)