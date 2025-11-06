"""
DAO (Data Access Object) 모듈
데이터베이스 접근 로직을 담당하는 클래스들
"""

from typing import List, Optional
from entities import User, Job, Application, Notification, Resume, Timetable, Bookmark, ViewHistory, FAQ, Inquiry

class UserDAO:
    """사용자 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        UserDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_user(self, user: User) -> int:
        """
        새로운 사용자 추가
        :param user: User 객체
        :return: 생성된 사용자 ID
        """
        pass
    
    def update_user(self, user_id: int, data: dict) -> bool:
        """
        사용자 정보 수정
        :param user_id: 사용자 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_user(self, user_id: int) -> bool:
        """
        사용자 삭제
        :param user_id: 사용자 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        ID로 사용자 조회
        :param user_id: 사용자 ID
        :return: User 객체 또는 None
        """
        pass
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        사용자명으로 조회
        :param username: 사용자명
        :return: User 객체 또는 None
        """
        pass
    
    def get_user_by_student_id(self, student_id: str) -> Optional[User]:
        """
        학번으로 사용자 조회
        :param student_id: 학번
        :return: User 객체 또는 None
        """
        pass
    
    def get_all_users(self) -> List[User]:
        """
        모든 사용자 조회
        :return: User 객체 리스트
        """
        pass


class JobDAO:
    """공고 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        JobDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_job(self, job: Job) -> int:
        """
        새로운 공고 추가
        :param job: Job 객체
        :return: 생성된 공고 ID
        """
        pass
    
    def update_job(self, job_id: int, data: dict) -> bool:
        """
        공고 정보 수정
        :param job_id: 공고 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_job(self, job_id: int) -> bool:
        """
        공고 삭제
        :param job_id: 공고 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """
        ID로 공고 조회
        :param job_id: 공고 ID
        :return: Job 객체 또는 None
        """
        pass
    
    def get_all_jobs(self) -> List[Job]:
        """
        모든 공고 조회
        :return: Job 객체 리스트
        """
        pass
    
    def get_jobs_by_category(self, category: str) -> List[Job]:
        """
        카테고리별 공고 조회
        :param category: 카테고리 (장기/단기/일일)
        :return: Job 객체 리스트
        """
        pass
    
    def get_jobs_by_location(self, location: str) -> List[Job]:
        """
        장소별 공고 조회
        :param location: 근무 장소
        :return: Job 객체 리스트
        """
        pass
    
    def get_active_jobs(self) -> List[Job]:
        """
        마감되지 않은 공고 조회
        :return: Job 객체 리스트
        """
        pass
    
    def search_jobs(self, keyword: str) -> List[Job]:
        """
        키워드로 공고 검색
        :param keyword: 검색 키워드
        :return: Job 객체 리스트
        """
        pass


class ApplicationDAO:
    """지원서 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        ApplicationDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_application(self, application: Application) -> int:
        """
        새로운 지원서 추가
        :param application: Application 객체
        :return: 생성된 지원서 ID
        """
        pass
    
    def update_application(self, application_id: int, data: dict) -> bool:
        """
        지원서 정보 수정
        :param application_id: 지원서 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_application(self, application_id: int) -> bool:
        """
        지원서 삭제
        :param application_id: 지원서 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_application_by_id(self, application_id: int) -> Optional[Application]:
        """
        ID로 지원서 조회
        :param application_id: 지원서 ID
        :return: Application 객체 또는 None
        """
        pass
    
    def get_applications_by_user(self, user_id: int) -> List[Application]:
        """
        사용자의 모든 지원서 조회
        :param user_id: 사용자 ID
        :return: Application 객체 리스트
        """
        pass
    
    def get_applications_by_job(self, job_id: int) -> List[Application]:
        """
        특정 공고의 모든 지원서 조회
        :param job_id: 공고 ID
        :return: Application 객체 리스트
        """
        pass
    
    def get_applications_by_status(self, user_id: int, status: str) -> List[Application]:
        """
        상태별 지원서 조회
        :param user_id: 사용자 ID
        :param status: 지원 상태
        :return: Application 객체 리스트
        """
        pass


class NotificationDAO:
    """알림 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        NotificationDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_notification(self, notification: Notification) -> int:
        """
        새로운 알림 추가
        :param notification: Notification 객체
        :return: 생성된 알림 ID
        """
        pass
    
    def update_notification(self, notification_id: int, data: dict) -> bool:
        """
        알림 정보 수정
        :param notification_id: 알림 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_notification(self, notification_id: int) -> bool:
        """
        알림 삭제
        :param notification_id: 알림 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        ID로 알림 조회
        :param notification_id: 알림 ID
        :return: Notification 객체 또는 None
        """
        pass
    
    def get_notifications_by_user(self, user_id: int) -> List[Notification]:
        """
        사용자의 모든 알림 조회
        :param user_id: 사용자 ID
        :return: Notification 객체 리스트
        """
        pass
    
    def get_unread_notifications(self, user_id: int) -> List[Notification]:
        """
        읽지 않은 알림 조회
        :param user_id: 사용자 ID
        :return: Notification 객체 리스트
        """
        pass
    
    def mark_all_as_read(self, user_id: int) -> bool:
        """
        사용자의 모든 알림을 읽음 처리
        :param user_id: 사용자 ID
        :return: 처리 성공 여부
        """
        pass


class ResumeDAO:
    """이력서 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        ResumeDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_resume(self, resume: Resume) -> int:
        """
        새로운 이력서 추가
        :param resume: Resume 객체
        :return: 생성된 이력서 ID
        """
        pass
    
    def update_resume(self, resume_id: int, data: dict) -> bool:
        """
        이력서 정보 수정
        :param resume_id: 이력서 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_resume(self, resume_id: int) -> bool:
        """
        이력서 삭제
        :param resume_id: 이력서 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_resume_by_id(self, resume_id: int) -> Optional[Resume]:
        """
        ID로 이력서 조회
        :param resume_id: 이력서 ID
        :return: Resume 객체 또는 None
        """
        pass
    
    def get_resumes_by_user(self, user_id: int) -> List[Resume]:
        """
        사용자의 모든 이력서 조회
        :param user_id: 사용자 ID
        :return: Resume 객체 리스트
        """
        pass
    
    def get_default_resume(self, user_id: int) -> Optional[Resume]:
        """
        사용자의 기본 이력서 조회
        :param user_id: 사용자 ID
        :return: Resume 객체 또는 None
        """
        pass


class TimetableDAO:
    """시간표 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        TimetableDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_timetable(self, timetable: Timetable) -> int:
        """
        새로운 시간표 추가
        :param timetable: Timetable 객체
        :return: 생성된 시간표 ID
        """
        pass
    
    def update_timetable(self, timetable_id: int, data: dict) -> bool:
        """
        시간표 정보 수정
        :param timetable_id: 시간표 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_timetable(self, timetable_id: int) -> bool:
        """
        시간표 삭제
        :param timetable_id: 시간표 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_timetable_by_id(self, timetable_id: int) -> Optional[Timetable]:
        """
        ID로 시간표 조회
        :param timetable_id: 시간표 ID
        :return: Timetable 객체 또는 None
        """
        pass
    
    def get_timetable_by_user(self, user_id: int, semester: str) -> Optional[Timetable]:
        """
        사용자의 특정 학기 시간표 조회
        :param user_id: 사용자 ID
        :param semester: 학기
        :return: Timetable 객체 또는 None
        """
        pass
    
    def get_current_timetable(self, user_id: int) -> Optional[Timetable]:
        """
        사용자의 현재 학기 시간표 조회
        :param user_id: 사용자 ID
        :return: Timetable 객체 또는 None
        """
        pass


class BookmarkDAO:
    """북마크 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        BookmarkDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_bookmark(self, bookmark: Bookmark) -> int:
        """
        새로운 북마크 추가
        :param bookmark: Bookmark 객체
        :return: 생성된 북마크 ID
        """
        pass
    
    def delete_bookmark(self, bookmark_id: int) -> bool:
        """
        북마크 삭제
        :param bookmark_id: 북마크 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_bookmarks_by_user(self, user_id: int) -> List[Bookmark]:
        """
        사용자의 모든 북마크 조회
        :param user_id: 사용자 ID
        :return: Bookmark 객체 리스트
        """
        pass
    
    def is_bookmarked(self, user_id: int, job_id: int) -> bool:
        """
        특정 공고의 북마크 여부 확인
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 북마크 여부
        """
        pass
    
    def delete_bookmark_by_job(self, user_id: int, job_id: int) -> bool:
        """
        특정 공고의 북마크 삭제
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 삭제 성공 여부
        """
        pass


class ViewHistoryDAO:
    """열람 이력 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        ViewHistoryDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_view_history(self, history: ViewHistory) -> int:
        """
        새로운 열람 이력 추가
        :param history: ViewHistory 객체
        :return: 생성된 이력 ID
        """
        pass
    
    def get_recent_views(self, user_id: int, days: int = 7) -> List[ViewHistory]:
        """
        최근 열람 이력 조회
        :param user_id: 사용자 ID
        :param days: 조회할 일수
        :return: ViewHistory 객체 리스트
        """
        pass
    
    def get_view_count(self, job_id: int) -> int:
        """
        특정 공고의 조회수 계산
        :param job_id: 공고 ID
        :return: 조회수
        """
        pass
    
    def delete_old_history(self, days: int = 30) -> bool:
        """
        오래된 열람 이력 삭제
        :param days: 기준 일수
        :return: 삭제 성공 여부
        """
        pass


class FAQdao:
    """FAQ 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        FAQDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_faq(self, faq: FAQ) -> int:
        """
        새로운 FAQ 추가
        :param faq: FAQ 객체
        :return: 생성된 FAQ ID
        """
        pass
    
    def update_faq(self, faq_id: int, data: dict) -> bool:
        """
        FAQ 정보 수정
        :param faq_id: FAQ ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_faq(self, faq_id: int) -> bool:
        """
        FAQ 삭제
        :param faq_id: FAQ ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_all_faqs(self) -> List[FAQ]:
        """
        모든 FAQ 조회
        :return: FAQ 객체 리스트
        """
        pass
    
    def get_faqs_by_category(self, category: str) -> List[FAQ]:
        """
        카테고리별 FAQ 조회
        :param category: 카테고리
        :return: FAQ 객체 리스트
        """
        pass
    
    def search_faqs(self, keyword: str) -> List[FAQ]:
        """
        키워드로 FAQ 검색
        :param keyword: 검색 키워드
        :return: FAQ 객체 리스트
        """
        pass


class InquiryDAO:
    """문의 데이터 접근 객체"""
    
    def __init__(self, db_manager):
        """
        InquiryDAO 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        
    def insert_inquiry(self, inquiry: Inquiry) -> int:
        """
        새로운 문의 추가
        :param inquiry: Inquiry 객체
        :return: 생성된 문의 ID
        """
        pass
    
    def update_inquiry(self, inquiry_id: int, data: dict) -> bool:
        """
        문의 정보 수정
        :param inquiry_id: 문의 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        pass
    
    def delete_inquiry(self, inquiry_id: int) -> bool:
        """
        문의 삭제
        :param inquiry_id: 문의 ID
        :return: 삭제 성공 여부
        """
        pass
    
    def get_inquiry_by_id(self, inquiry_id: int) -> Optional[Inquiry]:
        """
        ID로 문의 조회
        :param inquiry_id: 문의 ID
        :return: Inquiry 객체 또는 None
        """
        pass
    
    def get_inquiries_by_user(self, user_id: int) -> List[Inquiry]:
        """
        사용자의 모든 문의 조회
        :param user_id: 사용자 ID
        :return: Inquiry 객체 리스트
        """
        pass
    
    def get_unanswered_inquiries(self) -> List[Inquiry]:
        """
        답변되지 않은 문의 조회
        :return: Inquiry 객체 리스트
        """
        pass
    
    def get_inquiries_by_status(self, status: str) -> List[Inquiry]:
        """
        상태별 문의 조회
        :param status: 처리 상태
        :return: Inquiry 객체 리스트
        """
        pass
