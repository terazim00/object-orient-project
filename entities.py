# entities.py
from datetime import datetime, date
from typing import Optional, List, Dict
import json


class User:
    """사용자 엔티티"""

    def __init__(
        self,
        user_id: int = None,
        username: str = None,
        password: str = None,
        email: str = None,
        phone: str = None,
        student_id: str = None,
        department: str = None,
        role: str = "student",
    ):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.student_id = student_id
        self.department = department
        self.role = role

    def get_info(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "student_id": self.student_id,
            "department": self.department,
            "role": self.role,
        }

    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_staff(self) -> bool:
        return self.role == "staff"


class Job:
    """근로장학 공고 엔티티"""

    def __init__(
        self,
        job_id: int = None,
        title: str = None,
        description: str = None,
        category: str = None,
        location: str = None,
        job_type: str = None,
        work_hours: str = None,
        salary: int = None,
        requirements: str = None,
        deadline: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        department: str = None,
        max_applicants: int = None,
    ):
        self.job_id = job_id
        self.title = title
        self.description = description
        self.category = category
        self.location = location
        self.job_type = job_type
        self.work_hours = work_hours
        self.salary = salary
        self.requirements = requirements
        self.deadline = deadline
        self.created_at = created_at
        self.department = department
        self.max_applicants = max_applicants

    def get_details(self) -> dict:
        return {
            "job_id": self.job_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "location": self.location,
            "job_type": self.job_type,
            "work_hours": self.work_hours,
            "salary": self.salary,
            "requirements": self.requirements,
            "deadline": self.deadline.isoformat()
            if isinstance(self.deadline, datetime)
            else None,
            "created_at": self.created_at.isoformat()
            if isinstance(self.created_at, datetime)
            else None,
            "department": self.department,
            "max_applicants": self.max_applicants,
        }

    def is_expired(self) -> bool:
        if not self.deadline:
            return False
        return datetime.now() > self.deadline

    def get_remaining_days(self) -> int:
        if not self.deadline:
            return 9999
        today = date.today()
        dl = self.deadline.date()
        return (dl - today).days


class Application:
    """지원서 엔티티"""

    def __init__(
        self,
        application_id: int = None,
        user_id: int = None,
        job_id: int = None,
        resume_id: int = None,
        status: str = "제출",
        submitted_at: Optional[datetime] = None,
    ):
        self.application_id = application_id
        self.user_id = user_id
        self.job_id = job_id
        self.resume_id = resume_id
        self.status = status
        self.submitted_at = submitted_at

    def get_status(self) -> str:
        return self.status

    def set_status(self, status: str):
        self.status = status

    def get_timeline(self) -> List[Dict]:
        timeline = []
        if self.submitted_at:
            timeline.append(
                {"status": "제출", "timestamp": self.submitted_at.isoformat()}
            )
        if self.status != "제출":
            timeline.append(
                {"status": self.status, "timestamp": datetime.now().isoformat()}
            )
        return timeline


class Resume:
    """이력서 엔티티"""

    def __init__(
        self,
        resume_id: int = None,
        user_id: int = None,
        title: str = None,
        content: str = None,
        is_default: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.resume_id = resume_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.is_default = is_default
        self.created_at = created_at
        self.updated_at = updated_at

    def get_info(self) -> dict:
        return {
            "resume_id": self.resume_id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat()
            if isinstance(self.created_at, datetime)
            else None,
            "updated_at": self.updated_at.isoformat()
            if isinstance(self.updated_at, datetime)
            else None,
        }

    def update_info(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)


class Timetable:
    """시간표 엔티티"""

    def __init__(
        self,
        timetable_id: int = None,
        user_id: int = None,
        semester: str = None,
        schedule_data: str = None,
        created_at: Optional[datetime] = None,
    ):
        self.timetable_id = timetable_id
        self.user_id = user_id
        self.semester = semester
        self.schedule_data = schedule_data
        self.created_at = created_at

    def get_schedule(self) -> dict:
        if not self.schedule_data:
            return {}
        try:
            return json.loads(self.schedule_data)
        except json.JSONDecodeError:
            return {}

    def is_available(self, day: str, start_time: str, end_time: str) -> bool:
        schedule = self.get_schedule()
        busy_list = schedule.get(day, [])

        def to_minutes(t: str) -> int:
            h, m = t.split(":")
            return int(h) * 60 + int(m)

        s = to_minutes(start_time)
        e = to_minutes(end_time)

        for item in busy_list:
            bs = to_minutes(item["start"])
            be = to_minutes(item["end"])
            if not (e <= bs or be <= s):
                return False
        return True

    def get_free_slots(self) -> list:
        schedule = self.get_schedule()
        days = ["월", "화", "수", "목", "금"]
        free_slots = []
        for d in days:
            if d not in schedule or not schedule[d]:
                free_slots.append({"day": d, "start": "00:00", "end": "23:59"})
        return free_slots


class Bookmark:
    def __init__(
        self,
        bookmark_id: int = None,
        user_id: int = None,
        job_id: int = None,
        created_at: Optional[datetime] = None,
    ):
        self.bookmark_id = bookmark_id
        self.user_id = user_id
        self.job_id = job_id
        self.created_at = created_at


class ViewHistory:
    def __init__(
        self,
        history_id: int = None,
        user_id: int = None,
        job_id: int = None,
        viewed_at: Optional[datetime] = None,
    ):
        self.history_id = history_id
        self.user_id = user_id
        self.job_id = job_id
        self.viewed_at = viewed_at


class FAQ:
    def __init__(
        self,
        faq_id: int = None,
        category: str = None,
        question: str = None,
        answer: str = None,
    ):
        self.faq_id = faq_id
        self.category = category
        self.question = question
        self.answer = answer


class Inquiry:
    def __init__(
        self,
        inquiry_id: int = None,
        user_id: int = None,
        title: str = None,
        content: str = None,
        answer: str = None,
        status: str = None,
        created_at: Optional[datetime] = None,
        answered_at: Optional[datetime] = None,
    ):
        self.inquiry_id = inquiry_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.answer = answer
        self.status = status
        self.created_at = created_at
        self.answered_at = answered_at
