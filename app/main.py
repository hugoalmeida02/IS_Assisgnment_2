from app import models
from app.database import create_db_and_tables, engine
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
from sqlmodel import Session


def seed_data(session: Session) -> None:
    print("Creating students...")
    s1 = create_student(session, "Ana Silva", "ana@example.com")
    s2 = create_student(session, "Bruno Costa", "bruno@example.com")
    print(f"Created students: {s1}, {s2}")

    print("\nCreating courses...")
    c1 = create_course(session, "Databases", "Introduction to relational databases", 2)
    c2 = create_course(session, "AI Fundamentals", "Basic AI concepts", 1)
    print(f"Created courses: {c1}, {c2}")


def run_tests(session: Session) -> None:
    print("\nListing students...")
    for student in list_students(session):
        print(student)

    print("\nListing courses...")
    for course in list_courses(session):
        print(course)

    print("\nEnrolling students by id...")
    e1 = enroll_student_by_id(session, 1, 1)
    e2 = enroll_student_by_id(session, 2, 1)
    print(e1)
    print(e2)

    print("\nEnrolling student by email...")
    e3 = enroll_student_by_email(session, "ana@example.com", 2)
    print(e3)

    print("\nCurrent enrollments...")
    for enrollment in list_enrollments(session):
        print(enrollment)

    print("\nCourses of student 1...")
    for course in list_courses_of_student(session, 1):
        print(course)

    print("\nStudents in course 1...")
    for student in list_students_in_course(session, 1):
        print(student)

    print("\nTesting duplicate enrollment...")
    try:
        enroll_student_by_id(session, 1, 1)
    except ConflictError as e:
        print(f"Expected conflict: {e}")

    print("\nTesting full course...")
    try:
        enroll_student_by_id(session, 2, 2)
    except BusinessRuleError as e:
        print(f"Expected business rule error: {e}")

    print("\nTesting nonexistent student...")
    try:
        get_student(session, 999)
    except NotFoundError as e:
        print(f"Expected not found: {e}")

    print("\nUpdating student 1...")
    updated_student = update_student(session, 1, name="Ana Maria Silva")
    print(updated_student)

    print("\nUpdating course 1...")
    updated_course = update_course(session, 1, capacity=3)
    print(updated_course)

    print("\nRemoving enrollment (student 2, course 1)...")
    remove_enrollment(session, 2, 1)
    print("Enrollment removed.")

    print("\nEnrollments after removal...")
    for enrollment in list_enrollments(session):
        print(enrollment)


if __name__ == "__main__":
    create_db_and_tables()

    with Session(engine) as session:
        try:
            seed_data(session)
            run_tests(session)
        except ConflictError as e:
            print(f"Conflict error: {e}")
        except BusinessRuleError as e:
            print(f"Business rule error: {e}")
        except NotFoundError as e:
            print(f"Not found error: {e}")