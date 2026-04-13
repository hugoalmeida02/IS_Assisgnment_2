from sqlmodel import Session

from app.database import engine
from app.mcp.server import mcp
from app.services import (
    create_student,
    get_student,
    list_students,
    update_student,
    delete_student,
    create_course,
    get_course,
    list_courses,
    update_course,
    delete_course,
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


def _student_to_dict(student):
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
    }


def _course_to_dict(course):
    return {
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "capacity": course.capacity,
    }


def _enrollment_to_dict(enrollment):
    return {
        "id": enrollment.id,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id,
    }


def _handle_service_error(e: Exception) -> dict:
    return {
        "success": False,
        "error_type": e.__class__.__name__,
        "message": str(e),
    }


# -------------------------
# Student tools
# -------------------------

@mcp.tool
def create_student_tool(name: str, email: str) -> dict:
    """Create a new student."""
    with Session(engine) as session:
        try:
            student = create_student(session, name, email)
            return {
                "success": True,
                "student": _student_to_dict(student),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def get_student_tool(student_id: int) -> dict:
    """Get a student by id."""
    with Session(engine) as session:
        try:
            student = get_student(session, student_id)
            return {
                "success": True,
                "student": _student_to_dict(student),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def list_students_tool() -> dict:
    """List all students."""
    with Session(engine) as session:
        students = list_students(session)
        return {
            "success": True,
            "students": [_student_to_dict(student) for student in students],
        }


@mcp.tool
def update_student_tool(
    student_id: int,
    name: str | None = None,
    email: str | None = None
) -> dict:
    """Update a student."""
    with Session(engine) as session:
        try:
            student = update_student(session, student_id, name=name, email=email)
            return {
                "success": True,
                "student": _student_to_dict(student),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def delete_student_tool(student_id: int) -> dict:
    """Delete a student."""
    with Session(engine) as session:
        try:
            delete_student(session, student_id)
            return {
                "success": True,
                "message": f"Student {student_id} deleted successfully.",
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


# -------------------------
# Course tools
# -------------------------

@mcp.tool
def create_course_tool(name: str, description: str | None, capacity: int) -> dict:
    """Create a new course."""
    with Session(engine) as session:
        try:
            course = create_course(session, name, description, capacity)
            return {
                "success": True,
                "course": _course_to_dict(course),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def get_course_tool(course_id: int) -> dict:
    """Get a course by id."""
    with Session(engine) as session:
        try:
            course = get_course(session, course_id)
            return {
                "success": True,
                "course": _course_to_dict(course),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def list_courses_tool() -> dict:
    """List all courses."""
    with Session(engine) as session:
        courses = list_courses(session)
        return {
            "success": True,
            "courses": [_course_to_dict(course) for course in courses],
        }


@mcp.tool
def update_course_tool(
    course_id: int,
    name: str | None = None,
    description: str | None = None,
    capacity: int | None = None
) -> dict:
    """Update a course."""
    with Session(engine) as session:
        try:
            course = update_course(
                session,
                course_id,
                name=name,
                description=description,
                capacity=capacity,
            )
            return {
                "success": True,
                "course": _course_to_dict(course),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def delete_course_tool(course_id: int) -> dict:
    """Delete a course."""
    with Session(engine) as session:
        try:
            delete_course(session, course_id)
            return {
                "success": True,
                "message": f"Course {course_id} deleted successfully.",
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


# -------------------------
# Enrollment tools
# -------------------------

@mcp.tool
def enroll_student_by_id_tool(student_id: int, course_id: int) -> dict:
    """Enroll a student in a course using student id."""
    with Session(engine) as session:
        try:
            enrollment = enroll_student_by_id(session, student_id, course_id)
            return {
                "success": True,
                "enrollment": _enrollment_to_dict(enrollment),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def enroll_student_by_email_tool(email: str, course_id: int) -> dict:
    """Enroll a student in a course using student email."""
    with Session(engine) as session:
        try:
            enrollment = enroll_student_by_email(session, email, course_id)
            return {
                "success": True,
                "enrollment": _enrollment_to_dict(enrollment),
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def list_enrollments_tool() -> dict:
    """List all enrollments."""
    with Session(engine) as session:
        enrollments = list_enrollments(session)
        return {
            "success": True,
            "enrollments": [_enrollment_to_dict(enrollment) for enrollment in enrollments],
        }


@mcp.tool
def remove_enrollment_tool(student_id: int, course_id: int) -> dict:
    """Remove an enrollment using student id and course id."""
    with Session(engine) as session:
        try:
            remove_enrollment(session, student_id, course_id)
            return {
                "success": True,
                "message": "Enrollment removed successfully.",
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def list_courses_of_student_tool(student_id: int) -> dict:
    """List all courses of a student."""
    with Session(engine) as session:
        try:
            courses = list_courses_of_student(session, student_id)
            return {
                "success": True,
                "courses": [_course_to_dict(course) for course in courses],
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)


@mcp.tool
def list_students_in_course_tool(course_id: int) -> dict:
    """List all students in a course."""
    with Session(engine) as session:
        try:
            students = list_students_in_course(session, course_id)
            return {
                "success": True,
                "students": [_student_to_dict(student) for student in students],
            }
        except (NotFoundError, ConflictError, BusinessRuleError) as e:
            return _handle_service_error(e)
