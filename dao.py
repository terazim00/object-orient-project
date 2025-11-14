# dao.py
from typing import List, Optional
from datetime import datetime
from database_manager import DatabaseManager
from entities import (
    User,
    Job,
    Application,
    Resume,
    Timetable,
    Bookmark,
    ViewHistory,
    FAQ,
    Inquiry,
)


# ========== UserDAO ==========
class UserDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_user(self, user: User) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO users (username, password, email, phone, student_id, department, role)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.username,
                user.password,
                user.email,
                user.phone,
                user.student_id,
                user.department,
                user.role,
            ),
        )
        return cur.lastrowid

    def _row_to_user(self, row) -> User:
        return User(
            user_id=row["user_id"],
            username=row["username"],
            password=row["password"],
            email=row["email"],
            phone=row["phone"],
            student_id=row["student_id"],
            department=row["department"],
            role=row["role"],
        )

    def get_user_by_username(self, username: str) -> Optional[User]:
        cur = self.db_manager.execute_query(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        row = cur.fetchone()
        return self._row_to_user(row) if row else None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        cur = self.db_manager.execute_query(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        row = cur.fetchone()
        return self._row_to_user(row) if row else None


# ========== JobDAO ==========
class JobDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_job(self, job: Job) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO jobs (
                title, description, category, location,
                job_type, work_hours, salary, requirements,
                deadline, created_at, department, max_applicants
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.title,
                job.description,
                job.category,
                job.location,
                job.job_type,
                job.work_hours,
                job.salary,
                job.requirements,
                job.deadline.isoformat() if isinstance(job.deadline, datetime) else None,
                job.created_at.isoformat()
                if isinstance(job.created_at, datetime)
                else None,
                job.department,
                job.max_applicants,
            ),
        )
        return cur.lastrowid

    def update_job(self, job_id: int, data: dict) -> bool:
        if not data:
            return False
        fields = []
        params = []
        for k, v in data.items():
            fields.append(f"{k} = ?")
            params.append(v)
        params.append(job_id)
        query = f"UPDATE jobs SET {', '.join(fields)} WHERE job_id = ?"
        cur = self.db_manager.execute_query(query, tuple(params))
        return cur.rowcount > 0

    def delete_job(self, job_id: int) -> bool:
        cur = self.db_manager.execute_query(
            "DELETE FROM jobs WHERE job_id = ?", (job_id,)
        )
        return cur.rowcount > 0

    def _parse_dt(self, s: Optional[str]) -> Optional[datetime]:
        if s is None:
            return None
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    def _row_to_job(self, row) -> Job:
        return Job(
            job_id=row["job_id"],
            title=row["title"],
            description=row["description"],
            category=row["category"],
            location=row["location"],
            job_type=row["job_type"],
            work_hours=row["work_hours"],
            salary=row["salary"],
            requirements=row["requirements"],
            deadline=self._parse_dt(row["deadline"]),
            created_at=self._parse_dt(row["created_at"]),
            department=row["department"],
            max_applicants=row["max_applicants"],
        )

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        cur = self.db_manager.execute_query(
            "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
        )
        row = cur.fetchone()
        return self._row_to_job(row) if row else None

    def get_all_jobs(self) -> List[Job]:
        cur = self.db_manager.execute_query(
            "SELECT * FROM jobs ORDER BY created_at DESC"
        )
        return [self._row_to_job(r) for r in cur.fetchall()]

    def search_jobs(self, keyword: str) -> List[Job]:
        like = f"%{keyword}%"
        cur = self.db_manager.execute_query(
            """
            SELECT * FROM jobs
            WHERE title LIKE ? OR description LIKE ? OR location LIKE ?
            ORDER BY created_at DESC
            """,
            (like, like, like),
        )
        return [self._row_to_job(r) for r in cur.fetchall()]


# ========== ApplicationDAO ==========
class ApplicationDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_application(self, app: Application) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO applications (user_id, job_id, resume_id, status, submitted_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                app.user_id,
                app.job_id,
                app.resume_id,
                app.status,
                app.submitted_at.isoformat()
                if isinstance(app.submitted_at, datetime)
                else None,
            ),
        )
        return cur.lastrowid

    def _parse_dt(self, s: Optional[str]) -> Optional[datetime]:
        if s is None:
            return None
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    def _row_to_app(self, row) -> Application:
        return Application(
            application_id=row["application_id"],
            user_id=row["user_id"],
            job_id=row["job_id"],
            resume_id=row["resume_id"],
            status=row["status"],
            submitted_at=self._parse_dt(row["submitted_at"]),
        )

    def get_applications_by_user(self, user_id: int) -> List[Application]:
        cur = self.db_manager.execute_query(
            "SELECT * FROM applications WHERE user_id = ? ORDER BY submitted_at DESC",
            (user_id,),
        )
        return [self._row_to_app(r) for r in cur.fetchall()]


# ========== ResumeDAO ==========
class ResumeDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_resume(self, resume: Resume) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO resumes (user_id, title, content, is_default, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                resume.user_id,
                resume.title,
                resume.content,
                1 if resume.is_default else 0,
                resume.created_at.isoformat()
                if isinstance(resume.created_at, datetime)
                else None,
                resume.updated_at.isoformat()
                if isinstance(resume.updated_at, datetime)
                else None,
            ),
        )
        return cur.lastrowid

    def update_resume(self, resume_id: int, data: dict) -> bool:
        if not data:
            return False
        fields = []
        params = []
        for k, v in data.items():
            fields.append(f"{k} = ?")
            params.append(v)
        params.append(resume_id)
        query = f"UPDATE resumes SET {', '.join(fields)} WHERE resume_id = ?"
        cur = self.db_manager.execute_query(query, tuple(params))
        return cur.rowcount > 0

    def _parse_dt(self, s: Optional[str]) -> Optional[datetime]:
        if s is None:
            return None
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    def _row_to_resume(self, row) -> Resume:
        return Resume(
            resume_id=row["resume_id"],
            user_id=row["user_id"],
            title=row["title"],
            content=row["content"],
            is_default=bool(row["is_default"]),
            created_at=self._parse_dt(row["created_at"]),
            updated_at=self._parse_dt(row["updated_at"]),
        )

    def get_default_resume(self, user_id: int) -> Optional[Resume]:
        cur = self.db_manager.execute_query(
            "SELECT * FROM resumes WHERE user_id = ? AND is_default = 1",
            (user_id,),
        )
        row = cur.fetchone()
        return self._row_to_resume(row) if row else None


# ========== TimetableDAO ==========
class TimetableDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_timetable(self, timetable: Timetable) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO timetables (user_id, semester, schedule_data, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                timetable.user_id,
                timetable.semester,
                timetable.schedule_data,
                timetable.created_at.isoformat()
                if isinstance(timetable.created_at, datetime)
                else None,
            ),
        )
        return cur.lastrowid

    def _parse_dt(self, s: Optional[str]) -> Optional[datetime]:
        if s is None:
            return None
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    def _row_to_timetable(self, row) -> Timetable:
        return Timetable(
            timetable_id=row["timetable_id"],
            user_id=row["user_id"],
            semester=row["semester"],
            schedule_data=row["schedule_data"],
            created_at=self._parse_dt(row["created_at"]),
        )

    def get_latest_timetable(self, user_id: int) -> Optional[Timetable]:
        cur = self.db_manager.execute_query(
            """
            SELECT * FROM timetables
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (user_id,),
        )
        row = cur.fetchone()
        return self._row_to_timetable(row) if row else None


# ========== BookmarkDAO ==========
class BookmarkDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_bookmark(self, bm: Bookmark) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO bookmarks (user_id, job_id, created_at)
            VALUES (?, ?, ?)
            """,
            (
                bm.user_id,
                bm.job_id,
                bm.created_at.isoformat()
                if isinstance(bm.created_at, datetime)
                else None,
            ),
        )
        return cur.lastrowid

    def delete_bookmark(self, user_id: int, job_id: int) -> bool:
        cur = self.db_manager.execute_query(
            "DELETE FROM bookmarks WHERE user_id = ? AND job_id = ?",
            (user_id, job_id),
        )
        return cur.rowcount > 0

    def get_bookmarked_job_ids(self, user_id: int) -> List[int]:
        cur = self.db_manager.execute_query(
            "SELECT job_id FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return [r["job_id"] for r in cur.fetchall()]


# ========== ViewHistoryDAO ==========
class ViewHistoryDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_view(self, vh: ViewHistory) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO view_history (user_id, job_id, viewed_at)
            VALUES (?, ?, ?)
            """,
            (
                vh.user_id,
                vh.job_id,
                vh.viewed_at.isoformat()
                if isinstance(vh.viewed_at, datetime)
                else None,
            ),
        )
        return cur.lastrowid

    def get_recent_job_ids(self, user_id: int, limit: int = 10) -> List[int]:
        cur = self.db_manager.execute_query(
            """
            SELECT job_id
            FROM view_history
            WHERE user_id = ?
            ORDER BY viewed_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        return [r["job_id"] for r in cur.fetchall()]


# ========== FAQDAO ==========
class FAQDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_all(self) -> List[FAQ]:
        cur = self.db_manager.execute_query("SELECT * FROM faqs")
        rows = cur.fetchall()
        return [
            FAQ(
                faq_id=r["faq_id"],
                category=r["category"],
                question=r["question"],
                answer=r["answer"],
            )
            for r in rows
        ]

    def insert_faq(self, faq: FAQ) -> int:
        cur = self.db_manager.execute_query(
            "INSERT INTO faqs (category, question, answer) VALUES (?, ?, ?)",
            (faq.category, faq.question, faq.answer),
        )
        return cur.lastrowid


# ========== InquiryDAO ==========
class InquiryDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def insert_inquiry(self, inq: Inquiry) -> int:
        cur = self.db_manager.execute_query(
            """
            INSERT INTO inquiries (user_id, title, content, answer, status, created_at, answered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                inq.user_id,
                inq.title,
                inq.content,
                inq.answer,
                inq.status,
                inq.created_at.isoformat()
                if isinstance(inq.created_at, datetime)
                else None,
                inq.answered_at.isoformat()
                if isinstance(inq.answered_at, datetime)
                else None,
            ),
        )
        return cur.lastrowid

    def get_inquiries_by_user(self, user_id: int) -> List[Inquiry]:
        cur = self.db_manager.execute_query(
            "SELECT * FROM inquiries WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        res = []
        for r in rows:
            res.append(
                Inquiry(
                    inquiry_id=r["inquiry_id"],
                    user_id=r["user_id"],
                    title=r["title"],
                    content=r["content"],
                    answer=r["answer"],
                    status=r["status"],
                    created_at=datetime.fromisoformat(r["created_at"])
                    if r["created_at"]
                    else None,
                    answered_at=datetime.fromisoformat(r["answered_at"])
                    if r["answered_at"]
                    else None,
                )
            )
        return res
