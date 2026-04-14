from sqlmodel import Session, select

from app import models  # garante registo dos modelos
from app.database import create_db_and_tables, engine
from app.models import Student, Course, Enrollment
from app.services import (
    create_student,
    create_course,
    enroll_student_by_email,
    ConflictError,
    BusinessRuleError,
    NotFoundError,
)


def get_or_create_student(session: Session, name: str, email: str) -> Student:
    existing = session.exec(select(Student).where(Student.email == email)).first()
    if existing:
        return existing
    return create_student(session, name, email)


def get_or_create_course(session: Session, name: str, description: str, capacity: int) -> Course:
    existing = session.exec(select(Course).where(Course.name == name)).first()
    if existing:
        return existing
    return create_course(session, name, description, capacity)


def enrollment_exists(session: Session, student_id: int, course_id: int) -> bool:
    existing = session.exec(
        select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        )
    ).first()
    return existing is not None


def seed() -> None:
    create_db_and_tables()

    students_data = [
        ("Ana Silva", "ana@example.com"),
        ("Rafael Simão", "rafael@example.com"),
        ("Hugo Almeida", "hugo@example.com"),
        ("Diogo Costa", "diogo@example.com"),
        ("João Martins", "joao@example.com"),
        ("Beatriz Santos", "beatriz@example.com"),
        ("Marta Ferreira", "marta@example.com"),
        ("Pedro Lopes", "pedro@example.com"),
    ]

    courses_data = [
        ("Databases", "Relational databases and SQL", 4),
        ("Operating Systems", "Processes, memory and file systems", 3),
        ("Software Architecture", "Architectural styles and design", 4),
        ("Computer Networks", "Networking fundamentals", 3),
        ("Cybersecurity", "Security principles and threats", 2),
    ]

    enrollments_data = [
        ("ana@example.com", "Databases"),
        ("rafael@example.com", "Databases"),
        ("hugo@example.com", "Databases"),
        ("diogo@example.com", "Operating Systems"),
        ("joao@example.com", "Operating Systems"),
        ("beatriz@example.com", "Software Architecture"),
        ("marta@example.com", "Software Architecture"),
        ("pedro@example.com", "Computer Networks"),
        ("ana@example.com", "Cybersecurity"),
        ("beatriz@example.com", "Cybersecurity"),
    ]

    with Session(engine) as session:
        created_students = []
        created_courses = []
        created_enrollments = 0

        for name, email in students_data:
            student = get_or_create_student(session, name, email)
            created_students.append(student)

        for name, description, capacity in courses_data:
            course = get_or_create_course(session, name, description, capacity)
            created_courses.append(course)

        course_by_name = {
            course.name: course for course in session.exec(select(Course)).all()
        }

        student_by_email = {
            student.email: student for student in session.exec(select(Student)).all()
        }

        for email, course_name in enrollments_data:
            student = student_by_email[email]
            course = course_by_name[course_name]

            if enrollment_exists(session, student.id, course.id):
                continue

            try:
                enroll_student_by_email(session, email, course.id)
                created_enrollments += 1
            except (ConflictError, BusinessRuleError, NotFoundError):
                pass

        print("Seed completed.")
        print(f"Students in DB: {len(session.exec(select(Student)).all())}")
        print(f"Courses in DB: {len(session.exec(select(Course)).all())}")
        print(f"Enrollments in DB: {len(session.exec(select(Enrollment)).all())}")


if __name__ == "__main__":
    seed()