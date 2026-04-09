from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.schemas import (
    EnrollmentCreateById,
    EnrollmentCreateByEmail,
    EnrollmentRead,
    CourseRead,
    StudentRead,
)
from app.services import (
    enroll_student_by_id,
    enroll_student_by_email,
    list_enrollments,
    remove_enrollment,
    list_courses_of_student,
    list_students_in_course,
    NotFoundError,
    ConflictError,
    BusinessRuleError,
)

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/by-id", response_model=EnrollmentRead)
def enroll_by_id_endpoint(
    enrollment_data: EnrollmentCreateById,
    session: Session = Depends(get_session)
):
    try:
        return enroll_student_by_id(
            session,
            enrollment_data.student_id,
            enrollment_data.course_id
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/by-email", response_model=EnrollmentRead)
def enroll_by_email_endpoint(
    enrollment_data: EnrollmentCreateByEmail,
    session: Session = Depends(get_session)
):
    try:
        return enroll_student_by_email(
            session,
            enrollment_data.email,
            enrollment_data.course_id
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except BusinessRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[EnrollmentRead])
def list_enrollments_endpoint(session: Session = Depends(get_session)):
    return list_enrollments(session)


@router.delete("/{student_id}/{course_id}")
def remove_enrollment_endpoint(
    student_id: int,
    course_id: int,
    session: Session = Depends(get_session)
):
    try:
        remove_enrollment(session, student_id, course_id)
        return {"message": "Enrollment removed successfully."}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/student/{student_id}/courses", response_model=list[CourseRead])
def list_courses_of_student_endpoint(
    student_id: int,
    session: Session = Depends(get_session)
):
    try:
        return list_courses_of_student(session, student_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/course/{course_id}/students", response_model=list[StudentRead])
def list_students_in_course_endpoint(
    course_id: int,
    session: Session = Depends(get_session)
):
    try:
        return list_students_in_course(session, course_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))