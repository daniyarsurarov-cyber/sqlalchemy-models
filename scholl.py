from datetime import date

from sqlalchemy import Column, ForeignKey, String, Table, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/praktika1"


class Base(DeclarativeBase):
    pass


course_teacher = Table(
    "course_teacher",
    Base.metadata,
    Column("teacher_id", ForeignKey("teacher.id"), primary_key=True),
    Column("course_id", ForeignKey("course.id"), primary_key=True),
)


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int]

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="course")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="course")
    teachers: Mapped[list["Teacher"]] = relationship(
        secondary=course_teacher, back_populates="courses"
    )


class Teacher(Base):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50), unique=True)

    courses: Mapped[list["Course"]] = relationship(
        secondary=course_teacher, back_populates="teachers"
    )
    homeworks: Mapped[list["Homework"]] = relationship(back_populates="teacher")


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50), unique=True)

    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")
    homeworks: Mapped[list["Homework"]] = relationship(back_populates="student")


class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    number_lesson: Mapped[int]
    theme_lesson: Mapped[str] = mapped_column(String(50))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))

    course: Mapped["Course"] = relationship(back_populates="lessons")
    homeworks: Mapped[list["Homework"]] = relationship(back_populates="lesson")


class Enrollment(Base):
    __tablename__ = "enrollment"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    price: Mapped[int]
    enrolled_at: Mapped[date]

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    course: Mapped["Course"] = relationship(back_populates="enrollments")


class Homework(Base):
    __tablename__ = "homework"

    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int | None]  # на схеме нет NN, значит оценка может быть пустой
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))

    lesson: Mapped["Lesson"] = relationship(back_populates="homeworks")
    student: Mapped["Student"] = relationship(back_populates="homeworks")
    teacher: Mapped["Teacher"] = relationship(back_populates="homeworks")


if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
