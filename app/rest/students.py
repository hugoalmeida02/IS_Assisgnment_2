from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas import StudentCreate, StudentRead, StudentUpdate
from app.services import (
    create_student,
    get_student,
    list_students,
    update_student,
    delete_student,
    NotFoundError,
    ConflictError,
)

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentRead)
def create_student_endpoint(
    student_data: StudentCreate,
    session: Session = Depends(get_session)
):
    try:
        return create_student(session, student_data.name, student_data.email)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/", response_model=list[StudentRead])
def list_students_endpoint(session: Session = Depends(get_session)):
    return list_students(session)


@router.get("/{student_id}", response_model=StudentRead)
def get_student_endpoint(student_id: int, session: Session = Depends(get_session)):
    try:
        return get_student(session, student_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{student_id}", response_model=StudentRead)
def update_student_endpoint(
    student_id: int,
    student_data: StudentUpdate,
    session: Session = Depends(get_session)
):
    try:
        return update_student(
            session,
            student_id,
            name=student_data.name,
            email=student_data.email
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{student_id}")
def delete_student_endpoint(student_id: int, session: Session = Depends(get_session)):
    try:
        delete_student(session, student_id)
        return {"message": f"Student {student_id} deleted successfully."}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
