from typing import Optional

from sqlmodel import Session, select

from app.models import Student, Course, Enrollment


class NotFoundError(Exception):
    pass


class BusinessRuleError(Exception):
    pass


class ConflictError(Exception):
    pass


# -------------------------
# Student services
# -------------------------

def create_student(session: Session, name: str, email: str) -> Student:
    existing_student = session.exec(
        select(Student).where(Student.email == email)
    ).first()

    if existing_student:
        raise ConflictError(f"A student with email '{email}' already exists.")

    student = Student(name=name.strip(), email=email.strip().lower())
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def get_student(session: Session, student_id: int) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise NotFoundError(f"Student with id {student_id} was not found.")
    return student


def list_students(session: Session) -> list[Student]:
    return list(session.exec(select(Student)).all())


def update_student(
    session: Session,
    student_id: int,
    name: Optional[str] = None,
    email: Optional[str] = None
) -> Student:
    student = get_student(session, student_id)

    if name is not None:
        student.name = name.strip()

    if email is not None:
        normalized_email = email.strip().lower()

        existing_student = session.exec(
            select(Student).where(Student.email == normalized_email)
        ).first()

        if existing_student and existing_student.id != student_id:
            raise ConflictError(f"A student with email '{normalized_email}' already exists.")

        student.email = normalized_email

    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def delete_student(session: Session, student_id: int) -> None:
    student = get_student(session, student_id)

    enrollments = session.exec(
        select(Enrollment).where(Enrollment.student_id == student_id)
    ).all()

    for enrollment in enrollments:
        session.delete(enrollment)

    session.delete(student)
    session.commit()


# -------------------------
# Course services
# -------------------------

def create_course(
    session: Session,
    name: str,
    description: Optional[str],
    capacity: int
) -> Course:
    if capacity <= 0:
        raise BusinessRuleError("Course capacity must be greater than 0.")

    normalized_name = name.strip()

    existing_course = session.exec(
        select(Course).where(Course.name == normalized_name)
    ).first()

    if existing_course:
        raise ConflictError(f"Course with name '{normalized_name}' already exists.")

    course = Course(
        name=normalized_name,
        description=description.strip() if description else None,
        capacity=capacity
    )
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def get_course(session: Session, course_id: int) -> Course:
    course = session.get(Course, course_id)
    if not course:
        raise NotFoundError(f"Course with id {course_id} was not found.")
    return course


def list_courses(session: Session) -> list[Course]:
    return list(session.exec(select(Course)).all())


def update_course(
    session: Session,
    course_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    capacity: Optional[int] = None
) -> Course:
    course = get_course(session, course_id)

    if name is not None:
        normalized_name = name.strip()

        existing_course = session.exec(
            select(Course).where(Course.name == normalized_name)
        ).first()

        if existing_course and existing_course.id != course_id:
            raise ConflictError(f"Course with name '{normalized_name}' already exists.")

        course.name = normalized_name

    if description is not None:
        course.description = description.strip()

    if capacity is not None:
        if capacity <= 0:
            raise BusinessRuleError("Course capacity must be greater than 0.")

        current_enrollments_count = len(
            session.exec(
                select(Enrollment).where(Enrollment.course_id == course_id)
            ).all()
        )

        if capacity < current_enrollments_count:
            raise BusinessRuleError(
                "Cannot reduce capacity below the current number of enrolled students."
            )

        course.capacity = capacity

    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def delete_course(session: Session, course_id: int) -> None:
    course = get_course(session, course_id)

    enrollments = session.exec(
        select(Enrollment).where(Enrollment.course_id == course_id)
    ).all()

    for enrollment in enrollments:
        session.delete(enrollment)

    session.delete(course)
    session.commit()


# -------------------------
# Enrollment services
# -------------------------

def enroll_student_by_id(session: Session, student_id: int, course_id: int) -> Enrollment:
    student = get_student(session, student_id)
    course = get_course(session, course_id)

    existing_enrollment = session.exec(
        select(Enrollment).where(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course.id
        )
    ).first()

    if existing_enrollment:
        raise ConflictError(
            f"Student {student.id} is already enrolled in course {course.id}."
        )

    current_enrollments_count = len(
        session.exec(
            select(Enrollment).where(Enrollment.course_id == course.id)
        ).all()
    )

    if current_enrollments_count >= course.capacity:
        raise BusinessRuleError(f"Course '{course.name}' is full.")

    enrollment = Enrollment(student_id=student.id, course_id=course.id)
    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)
    return enrollment


def enroll_student_by_email(session: Session, email: str, course_id: int) -> Enrollment:
    student = session.exec(
        select(Student).where(Student.email == email.strip().lower())
    ).first()

    if not student:
        raise NotFoundError(f"Student with email '{email}' was not found.")

    return enroll_student_by_id(session, student.id, course_id)


def list_enrollments(session: Session) -> list[Enrollment]:
    return list(session.exec(select(Enrollment)).all())


def remove_enrollment(session: Session, student_id: int, course_id: int) -> None:
    enrollment = session.exec(
        select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        )
    ).first()

    if not enrollment:
        raise NotFoundError(
            f"No enrollment found for student {student_id} in course {course_id}."
        )

    session.delete(enrollment)
    session.commit()


def list_courses_of_student(session: Session, student_id: int) -> list[Course]:
    get_student(session, student_id)

    enrollments = session.exec(
        select(Enrollment).where(Enrollment.student_id == student_id)
    ).all()

    courses = []
    for enrollment in enrollments:
        course = session.get(Course, enrollment.course_id)
        if course:
            courses.append(course)

    return courses


def list_students_in_course(session: Session, course_id: int) -> list[Student]:
    get_course(session, course_id)

    enrollments = session.exec(
        select(Enrollment).where(Enrollment.course_id == course_id)
    ).all()

    students = []
    for enrollment in enrollments:
        student = session.get(Student, enrollment.student_id)
        if student:
            students.append(student)

    return students
