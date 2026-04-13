from sqlmodel import Session

from app.database import engine
from app.mcp.server import mcp
from app.services import list_courses, list_students, list_enrollments


@mcp.resource("school://schema")
def get_system_schema() -> str:
    """Describe the database entities and relationships."""
    return """
Student-Course Management System Schema

Entities:
1. Student
   - id: integer, primary key
   - name: string
   - email: string

2. Course
   - id: integer, primary key
   - name: string
   - description: string or null
   - capacity: integer

3. Enrollment
   - id: integer, primary key
   - student_id: integer, foreign key -> Student.id
   - course_id: integer, foreign key -> Course.id

Relationships:
- A student can enroll in many courses.
- A course can have many students.
- Enrollment is the association entity between Student and Course.

Business rules:
- Student email must be unique.
- Course name must be unique.
- Course capacity must be greater than 0.
- A student cannot be enrolled twice in the same course.
- A student cannot enroll in a course that is already full.

Special cases:
- enroll_student_by_id and enroll_student_by_email are similar tools with different inputs.
- Attempting to enroll in a full course raises a business-rule failure.
- Using invalid student_id or course_id returns a not-found error.
""".strip()


@mcp.resource("school://report/courses")
def get_courses_report() -> str:
    """Provide a textual report of all courses and current occupancy."""
    with Session(engine) as session:
        courses = list_courses(session)
        enrollments = list_enrollments(session)

        enrollment_count_by_course = {}
        for enrollment in enrollments:
            enrollment_count_by_course[enrollment.course_id] = (
                enrollment_count_by_course.get(enrollment.course_id, 0) + 1
            )

        if not courses:
            return "No courses found."

        lines = ["Courses report:"]
        for course in courses:
            enrolled = enrollment_count_by_course.get(course.id, 0)
            available = course.capacity - enrolled
            lines.append(
                f"- Course #{course.id}: {course.name} | "
                f"capacity={course.capacity} | enrolled={enrolled} | available={available}"
            )

        return "\n".join(lines)


@mcp.resource("school://report/students")
def get_students_report() -> str:
    """Provide a textual report of all students."""
    with Session(engine) as session:
        students = list_students(session)

        if not students:
            return "No students found."

        lines = ["Students report:"]
        for student in students:
            lines.append(
                f"- Student #{student.id}: {student.name} | email={student.email}"
            )

        return "\n".join(lines)
