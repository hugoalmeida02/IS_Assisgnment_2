from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas import CourseCreate, CourseRead, CourseUpdate
from app.services import (
    create_course,
    get_course,
    list_courses,
    update_course,
    delete_course,
    NotFoundError,
    BusinessRuleError,
    ConflictError,
)

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseRead)
def create_course_endpoint(
    course_data: CourseCreate,
    session: Session = Depends(get_session)
):
    try:
        return create_course(
            session,
            course_data.name,
            course_data.description,
            course_data.capacity
        )
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/", response_model=list[CourseRead])
def list_courses_endpoint(session: Session = Depends(get_session)):
    return list_courses(session)


@router.get("/{course_id}", response_model=CourseRead)
def get_course_endpoint(course_id: int, session: Session = Depends(get_session)):
    try:
        return get_course(session, course_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{course_id}", response_model=CourseRead)
def update_course_endpoint(
    course_id: int,
    course_data: CourseUpdate,
    session: Session = Depends(get_session)
):
    try:
        return update_course(
            session,
            course_id,
            name=course_data.name,
            description=course_data.description,
            capacity=course_data.capacity
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{course_id}")
def delete_course_endpoint(course_id: int, session: Session = Depends(get_session)):
    try:
        delete_course(session, course_id)
        return {"message": f"Course {course_id} deleted successfully."}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))