# managers.py
from typing import Optional, List
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
from dao import (
    UserDAO,
    JobDAO,
    ApplicationDAO,
    ResumeDAO,
    TimetableDAO,
    BookmarkDAO,
    ViewHistoryDAO,
    FAQDAO,
    InquiryDAO,
)


# ========== UserManager ==========
class UserManager:
    def __init__(self, db_manager: DatabaseManager):
        self.user_dao = UserDAO(db_manager)

    def register(self, username: str, password: str) -> Optional[User]:
        existing = self.user_dao.get_user_by_username(username)
        if existing:
            return None
        user = User(username=username, password=password, role="student")
        user_id = self.user_dao.insert_user(user)
        user.user_id = user_id
        return user

    def login(self, username: str, password: str) -> Optional[User]:
        user = self.user_dao.get_user_by_username(username)
        if user and user.password == password:
            return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_dao.get_user_by_id(user_id)


# ========== JobManager ==========
class JobManager:
    def __init__(self, db_manager: DatabaseManager):
        self.job_dao = JobDAO(db_manager)

    def get_all_jobs(self) -> List[Job]:
        return self.job_dao.get_all_jobs()

    def search_jobs(self, keyword: str) -> List[Job]:
        return self.job_dao.search_jobs(keyword)

    def delete_job(self, job_id: int) -> bool:
        return self.job_dao.delete_job(job_id)


# ========== ResumeManager ==========
class ResumeManager:
    def __init__(self, db_manager: DatabaseManager):
        self.resume_dao = ResumeDAO(db_manager)

    def register_or_update_common_resume(
        self, user_id: int, title: str, content: str
    ) -> Optional[Resume]:
        now = datetime.now()
        existing = self.resume_dao.get_default_resume(user_id)
        if existing:
            self.resume_dao.update_resume(
                existing.resume_id,
                {
                    "title": title,
                    "content": content,
                    "updated_at": now.isoformat(),
                },
            )
            existing.title = title
            existing.content = content
            existing.updated_at = now
            return existing
        else:
            resume = Resume(
                user_id=user_id,
                title=title,
                content=content,
                is_default=True,
                created_at=now,
                updated_at=now,
            )
            resume_id = self.resume_dao.insert_resume(resume)
            resume.resume_id = resume_id
            return resume

    def get_default_resume(self, user_id: int) -> Optional[Resume]:
        return self.resume_dao.get_default_resume(user_id)


# ========== ApplicationManager ==========
class ApplicationManager:
    def __init__(self, db_manager: DatabaseManager):
        self.application_dao = ApplicationDAO(db_manager)

    def apply_to_job(
        self, user_id: int, job_id: int, resume_id: int
    ) -> Optional[Application]:
        now = datetime.now()
        app = Application(
            user_id=user_id,
            job_id=job_id,
            resume_id=resume_id,
            status="제출",
            submitted_at=now,
        )
        app_id = self.application_dao.insert_application(app)
        app.application_id = app_id
        return app

    def get_applications_by_user(self, user_id: int) -> List[Application]:
        return self.application_dao.get_applications_by_user(user_id)


# ========== TimetableManager ==========
class TimetableManager:
    def __init__(self, db_manager: DatabaseManager):
        self.table_dao = TimetableDAO(db_manager)

    def save_timetable(self, user_id: int, semester: str, schedule_data: str) -> Timetable:
        now = datetime.now()
        tb = Timetable(
            user_id=user_id,
            semester=semester,
            schedule_data=schedule_data,
            created_at=now,
        )
        tid = self.table_dao.insert_timetable(tb)
        tb.timetable_id = tid
        return tb

    def get_latest_timetable(self, user_id: int) -> Optional[Timetable]:
        return self.table_dao.get_latest_timetable(user_id)


# ========== BookmarkManager ==========
class BookmarkManager:
    def __init__(self, db_manager: DatabaseManager):
        self.bookmark_dao = BookmarkDAO(db_manager)
        self.job_dao = JobDAO(db_manager)

    def add_bookmark(self, user_id: int, job_id: int) -> bool:
        now = datetime.now()
        bm = Bookmark(user_id=user_id, job_id=job_id, created_at=now)
        self.bookmark_dao.insert_bookmark(bm)
        return True

    def remove_bookmark(self, user_id: int, job_id: int) -> bool:
        return self.bookmark_dao.delete_bookmark(user_id, job_id)

    def get_bookmarked_jobs(self, user_id: int) -> List[Job]:
        job_ids = self.bookmark_dao.get_bookmarked_job_ids(user_id)
        res = []
        for jid in job_ids:
            job = self.job_dao.get_job_by_id(jid)
            if job:
                res.append(job)
        return res


# ========== ViewHistoryManager ==========
class ViewHistoryManager:
    def __init__(self, db_manager: DatabaseManager):
        self.vh_dao = ViewHistoryDAO(db_manager)
        self.job_dao = JobDAO(db_manager)

    def record_view(self, user_id: int, job_id: int):
        now = datetime.now()
        vh = ViewHistory(user_id=user_id, job_id=job_id, viewed_at=now)
        self.vh_dao.insert_view(vh)

    def get_recent_jobs(self, user_id: int, limit: int = 10) -> List[Job]:
        ids = self.vh_dao.get_recent_job_ids(user_id, limit)
        res = []
        for jid in ids:
            job = self.job_dao.get_job_by_id(jid)
            if job:
                res.append(job)
        return res


# ========== FAQManager ==========
class FAQManager:
    def __init__(self, db_manager: DatabaseManager):
        self.faq_dao = FAQDAO(db_manager)

    def get_all_faqs(self) -> List[FAQ]:
        return self.faq_dao.get_all_faqs() if hasattr(self.faq_dao, "get_all_faqs") else self.faq_dao.get_all()

    # get_all_faqs 이름 통일
    def get_all(self) -> List[FAQ]:
        return self.faq_dao.get_all()

    def seed_default_faqs(self):
        """처음 실행 시 FAQ가 비어 있으면 기본 몇 개 넣기"""
        cur_list = self.faq_dao.get_all()
        if cur_list:
            return
        examples = [
            FAQ(category="지원", question="지원서는 어떻게 제출하나요?", answer="공고 선택 후 '선택 공고 지원' 버튼을 눌러주세요."),
            FAQ(category="이력서", question="통합 이력서는 무엇인가요?", answer="여러 공고에 공통으로 사용할 수 있는 기본 이력서입니다."),
        ]
        for f in examples:
            self.faq_dao.insert_faq(f)


# ========== InquiryManager ==========
class InquiryManager:
    def __init__(self, db_manager: DatabaseManager):
        self.inq_dao = InquiryDAO(db_manager)

    def create_inquiry(self, user_id: int, title: str, content: str) -> Inquiry:
        now = datetime.now()
        inq = Inquiry(
            user_id=user_id,
            title=title,
            content=content,
            answer=None,
            status="등록됨",
            created_at=now,
            answered_at=None,
        )
        iid = self.inq_dao.insert_inquiry(inq)
        inq.inquiry_id = iid
        return inq

    def get_user_inquiries(self, user_id: int) -> List[Inquiry]:
        return self.inq_dao.get_inquiries_by_user(user_id)
