from typing import Optional
from sqlmodel import SQLModel


# -------------------------
# Student schemas
# -------------------------

class StudentCreate(SQLModel):
    name: str
    email: str


class StudentUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None


class StudentRead(SQLModel):
    id: int
    name: str
    email: str


# -------------------------
# Course schemas
# -------------------------

class CourseCreate(SQLModel):
    name: str
    description: Optional[str] = None
    capacity: int


class CourseUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None


class CourseRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    capacity: int


# -------------------------
# Enrollment schemas
# -------------------------

class EnrollmentCreateById(SQLModel):
    student_id: int
    course_id: int


class EnrollmentCreateByEmail(SQLModel):
    email: str
    course_id: int


class EnrollmentRead(SQLModel):
    id: int
    student_id: int
    course_id: int