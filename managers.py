"""
Manager 모듈
비즈니스 로직을 담당하는 클래스들
"""

from typing import List, Optional, Dict
from entities import User, Job, Application, Notification, Resume, Timetable, Bookmark
from dao import (UserDAO, JobDAO, ApplicationDAO, NotificationDAO, 
                 ResumeDAO, TimetableDAO, BookmarkDAO, ViewHistoryDAO, 
                 FAQdao, InquiryDAO)

class UserManager:
    """사용자 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        UserManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.user_dao = UserDAO(db_manager)
        
    def register(self, user_data: dict) -> Optional[int]:
        """
        신규 사용자 등록
        :param user_data: 사용자 정보 딕셔너리
        :return: 생성된 사용자 ID 또는 None
        """
        # 필수 필드 검증
        required_fields = ['username', 'student_id']
        for field in required_fields:
            if field not in user_data:
                return None

        # 중복 확인
        existing_user = self.user_dao.get_user_by_student_id(user_data['student_id'])
        if existing_user:
            return None

        # User 객체 생성 및 저장
        user = User(
            username=user_data.get('username'),
            email=user_data.get('email'),
            phone=user_data.get('phone'),
            student_id=user_data.get('student_id'),
            department=user_data.get('department'),
            role=user_data.get('role', 'student')
        )

        return self.user_dao.insert_user(user)

    def login(self, username: str, password: str) -> Optional[User]:
        """
        사용자 로그인 (학교 SSO 연동)
        :param username: 사용자명 또는 학번
        :param password: 비밀번호
        :return: User 객체 또는 None
        """
        # 먼저 username으로 조회
        user = self.user_dao.get_user_by_username(username)

        # username으로 못 찾으면 학번으로 조회
        if not user:
            user = self.user_dao.get_user_by_student_id(username)

        # TODO: 실제 SSO 연동 시 비밀번호 검증 추가
        # 현재는 user가 존재하면 로그인 성공으로 간주
        return user

    def logout(self, user_id: int):
        """
        사용자 로그아웃
        :param user_id: 사용자 ID
        """
        # 로그아웃 시 필요한 정리 작업 (세션 정리 등)
        # 현재는 별도 작업 없음
        pass

    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """
        사용자 정보 조회
        :param user_id: 사용자 ID
        :return: 사용자 정보 딕셔너리 또는 None
        """
        user = self.user_dao.get_user_by_id(user_id)
        if user:
            return user.get_info()
        return None

    def update_user_info(self, user_id: int, data: dict) -> bool:
        """
        사용자 정보 수정
        :param user_id: 사용자 ID
        :param data: 수정할 정보
        :return: 수정 성공 여부
        """
        return self.user_dao.update_user(user_id, data)

    def delete_user(self, user_id: int) -> bool:
        """
        사용자 탈퇴 (데이터 7일 이내 파기)
        :param user_id: 사용자 ID
        :return: 삭제 성공 여부
        """
        # TODO: 실제로는 soft delete 후 7일 뒤 완전 삭제하는 스케줄러 필요
        return self.user_dao.delete_user(user_id)

    def check_permission(self, user_id: int, required_role: str) -> bool:
        """
        권한 확인
        :param user_id: 사용자 ID
        :param required_role: 필요한 권한 (student/staff/admin)
        :return: 권한 보유 여부
        """
        user = self.user_dao.get_user_by_id(user_id)
        if not user:
            return False

        # admin은 모든 권한 보유
        if user.role == 'admin':
            return True

        # staff는 student 권한도 보유
        if user.role == 'staff' and required_role in ['student', 'staff']:
            return True

        # 정확히 일치하는 경우
        return user.role == required_role


class JobManager:
    """공고 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        JobManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.job_dao = JobDAO(db_manager)
        
    def create_job(self, job_data: dict) -> Optional[int]:
        """
        새로운 공고 등록
        :param job_data: 공고 정보 딕셔너리
        :return: 생성된 공고 ID 또는 None
        """
        from datetime import datetime

        job = Job(
            title=job_data.get('title'),
            description=job_data.get('description'),
            category=job_data.get('category'),
            location=job_data.get('location'),
            job_type=job_data.get('job_type'),
            work_hours=job_data.get('work_hours'),
            salary=job_data.get('salary'),
            requirements=job_data.get('requirements'),
            deadline=job_data.get('deadline'),
            created_at=datetime.now(),
            department=job_data.get('department'),
            max_applicants=job_data.get('max_applicants')
        )

        return self.job_dao.insert_job(job)

    def update_job(self, job_id: int, job_data: dict) -> bool:
        """
        공고 정보 수정
        :param job_id: 공고 ID
        :param job_data: 수정할 정보
        :return: 수정 성공 여부
        """
        return self.job_dao.update_job(job_id, job_data)

    def delete_job(self, job_id: int) -> bool:
        """
        공고 삭제
        :param job_id: 공고 ID
        :return: 삭제 성공 여부
        """
        return self.job_dao.delete_job(job_id)

    def get_job_details(self, job_id: int) -> Optional[Dict]:
        """
        공고 상세 정보 조회
        :param job_id: 공고 ID
        :return: 공고 정보 딕셔너리 또는 None
        """
        job = self.job_dao.get_job_by_id(job_id)
        if job:
            return job.get_details()
        return None

    def get_job_list(self, filters: dict = None) -> List[Job]:
        """
        공고 목록 조회 (필터링 지원)
        :param filters: 필터 조건 (category, location, job_type 등)
        :return: Job 객체 리스트
        """
        if not filters:
            return self.job_dao.get_all_jobs()

        # 카테고리 필터
        if 'category' in filters:
            return self.job_dao.get_jobs_by_category(filters['category'])

        # 장소 필터
        if 'location' in filters:
            return self.job_dao.get_jobs_by_location(filters['location'])

        # TODO: 더 복잡한 필터 조합 구현
        return self.job_dao.get_all_jobs()

    def search_jobs(self, keyword: str, filters: dict = None) -> List[Job]:
        """
        공고 검색 (FR-03: 카테고리/필터 검색)
        :param keyword: 검색 키워드
        :param filters: 추가 필터 조건
        :return: Job 객체 리스트
        """
        # 키워드로 검색
        jobs = self.job_dao.search_jobs(keyword)

        # 필터가 있으면 추가 필터링
        if filters:
            if 'category' in filters:
                jobs = [j for j in jobs if j.category == filters['category']]
            if 'location' in filters:
                jobs = [j for j in jobs if j.location == filters['location']]

        return jobs

    def get_active_jobs(self) -> List[Job]:
        """
        진행 중인 공고 목록 조회
        :return: Job 객체 리스트
        """
        return self.job_dao.get_active_jobs()

    def collect_job_announcements(self):
        """
        교내 포털/게시판에서 공고 수집 (FR-01: 10분 주기)
        """
        # TODO: 실제 포털 크롤링 로직 구현
        # 현재는 placeholder
        pass

    def remove_duplicates(self):
        """
        중복 공고 제거 및 변경 이력 관리 (FR-02)
        """
        # TODO: 중복 확인 로직 구현 (제목, 내용 유사도 등)
        pass

    def check_expiring_jobs(self) -> List[Job]:
        """
        마감 임박 공고 확인
        :return: 마감 임박 공고 리스트
        """
        from datetime import datetime, timedelta

        all_jobs = self.job_dao.get_active_jobs()
        expiring_jobs = []

        for job in all_jobs:
            if job.deadline:
                days_left = job.get_remaining_days()
                if 0 <= days_left <= 3:  # 3일 이내 마감
                    expiring_jobs.append(job)

        return expiring_jobs


class ApplicationManager:
    """지원서 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        ApplicationManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.application_dao = ApplicationDAO(db_manager)
        self.notification_manager = None  # 나중에 초기화
        
    def register_application(self, app_info: dict) -> Optional[int]:
        """
        지원서 제출 (FR-04: 공통 이력서 작성)
        :param app_info: 지원서 정보
        :return: 생성된 지원서 ID 또는 None
        """
        from datetime import datetime

        application = Application(
            user_id=app_info.get('user_id'),
            job_id=app_info.get('job_id'),
            resume_id=app_info.get('resume_id'),
            status='제출',
            submitted_at=datetime.now(),
            cover_letter=app_info.get('cover_letter')
        )

        app_id = self.application_dao.insert_application(application)

        # 알림 전송
        if app_id and self.notification_manager:
            self.notification_manager.send_notification(
                app_info['user_id'],
                f"지원서가 성공적으로 제출되었습니다.",
                "application_submit",
                app_id
            )

        return app_id

    def update_application(self, app_id: int, data: dict) -> bool:
        """
        지원서 정보 수정
        :param app_id: 지원서 ID
        :param data: 수정할 정보
        :return: 수정 성공 여부
        """
        return self.application_dao.update_application(app_id, data)

    def delete_application(self, app_id: int) -> bool:
        """
        지원서 취소/삭제
        :param app_id: 지원서 ID
        :return: 삭제 성공 여부
        """
        return self.application_dao.delete_application(app_id)

    def get_application_list(self, user_id: int) -> List[Application]:
        """
        사용자의 지원서 목록 조회
        :param user_id: 사용자 ID
        :return: Application 객체 리스트
        """
        return self.application_dao.get_applications_by_user(user_id)

    def get_application_status(self, app_id: int) -> Optional[str]:
        """
        지원서 상태 조회 (FR-05: 지원 현황 추적)
        :param app_id: 지원서 ID
        :return: 상태 문자열 또는 None
        """
        application = self.application_dao.get_application_by_id(app_id)
        if application:
            return application.get_status()
        return None

    def update_application_status(self, app_id: int, status: str) -> bool:
        """
        지원서 상태 변경 (제출/서류통과/면접/선발/불합격)
        :param app_id: 지원서 ID
        :param status: 새로운 상태
        :return: 변경 성공 여부
        """
        result = self.application_dao.update_application(app_id, {'status': status})

        # 상태 변경 시 알림 전송
        if result:
            application = self.application_dao.get_application_by_id(app_id)
            if application and self.notification_manager:
                self.notification_manager.send_application_status_update(
                    application.user_id,
                    app_id,
                    status
                )

        return result

    def get_application_timeline(self, app_id: int) -> List[Dict]:
        """
        지원서 처리 타임라인 조회 (FR-05)
        :param app_id: 지원서 ID
        :return: 타임라인 리스트
        """
        application = self.application_dao.get_application_by_id(app_id)
        if application:
            return application.get_timeline()
        return []

    def auto_save_application(self, app_id: int, data: dict):
        """
        지원서 자동 임시저장 (REL-01: 30초마다)
        :param app_id: 지원서 ID
        :param data: 저장할 데이터
        """
        # 임시저장 로직
        self.application_dao.update_application(app_id, data)


class NotificationManager:
    """알림 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        NotificationManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.notification_dao = NotificationDAO(db_manager)
        
    def send_notification(self, user_id: int, message: str,
                         notification_type: str = None,
                         related_id: int = None) -> Optional[int]:
        """
        알림 전송
        :param user_id: 수신자 ID
        :param message: 알림 메시지
        :param notification_type: 알림 유형
        :param related_id: 관련 객체 ID
        :return: 생성된 알림 ID 또는 None
        """
        from datetime import datetime

        notification = Notification(
            user_id=user_id,
            message=message,
            notification_type=notification_type,
            is_read=False,
            created_at=datetime.now(),
            related_id=related_id
        )

        return self.notification_dao.insert_notification(notification)

    def get_notification_list(self, user_id: int) -> List[Notification]:
        """
        사용자의 알림 목록 조회
        :param user_id: 사용자 ID
        :return: Notification 객체 리스트
        """
        return self.notification_dao.get_notifications_by_user(user_id)

    def mark_as_read(self, notification_id: int) -> bool:
        """
        알림 읽음 처리
        :param notification_id: 알림 ID
        :return: 처리 성공 여부
        """
        return self.notification_dao.update_notification(notification_id, {'is_read': 1})

    def check_unread_notification(self, user_id: int) -> int:
        """
        읽지 않은 알림 개수 확인
        :param user_id: 사용자 ID
        :return: 읽지 않은 알림 개수
        """
        unread_notifications = self.notification_dao.get_unread_notifications(user_id)
        return len(unread_notifications)

    def send_deadline_reminder(self, user_id: int, job_id: int):
        """
        마감 임박 리마인더 전송 (FR-09: 관심공고 스크랩)
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        """
        self.send_notification(
            user_id,
            "관심공고의 마감이 임박했습니다!",
            "deadline_reminder",
            job_id
        )

    def send_new_job_alert(self, user_id: int, job_id: int):
        """
        신규 공고 알림 전송
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        """
        self.send_notification(
            user_id,
            "새로운 공고가 등록되었습니다.",
            "new_job",
            job_id
        )

    def send_application_status_update(self, user_id: int, app_id: int, status: str):
        """
        지원서 상태 변경 알림 전송
        :param user_id: 사용자 ID
        :param app_id: 지원서 ID
        :param status: 변경된 상태
        """
        self.send_notification(
            user_id,
            f"지원서 상태가 '{status}'(으)로 변경되었습니다.",
            "status_update",
            app_id
        )


class ResumeManager:
    """이력서 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        ResumeManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.resume_dao = ResumeDAO(db_manager)
        
    def create_resume(self, resume_data: dict) -> Optional[int]:
        """
        새로운 이력서 작성 (FR-04: 공통 이력서 작성)
        :param resume_data: 이력서 정보
        :return: 생성된 이력서 ID 또는 None
        """
        from datetime import datetime

        resume = Resume(
            user_id=resume_data.get('user_id'),
            title=resume_data.get('title'),
            education=resume_data.get('education'),
            experience=resume_data.get('experience'),
            certifications=resume_data.get('certifications'),
            self_introduction=resume_data.get('self_introduction'),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.resume_dao.insert_resume(resume)

    def update_resume(self, resume_id: int, data: dict) -> bool:
        """
        이력서 수정
        :param resume_id: 이력서 ID
        :param data: 수정할 정보
        :return: 수정 성공 여부
        """
        return self.resume_dao.update_resume(resume_id, data)

    def delete_resume(self, resume_id: int) -> bool:
        """
        이력서 삭제
        :param resume_id: 이력서 ID
        :return: 삭제 성공 여부
        """
        return self.resume_dao.delete_resume(resume_id)

    def get_resume(self, resume_id: int) -> Optional[Dict]:
        """
        이력서 조회
        :param resume_id: 이력서 ID
        :return: 이력서 정보 딕셔너리 또는 None
        """
        resume = self.resume_dao.get_resume_by_id(resume_id)
        if resume:
            return resume.get_info()
        return None

    def get_user_resumes(self, user_id: int) -> List[Resume]:
        """
        사용자의 모든 이력서 조회
        :param user_id: 사용자 ID
        :return: Resume 객체 리스트
        """
        return self.resume_dao.get_resumes_by_user(user_id)

    def set_default_resume(self, user_id: int, resume_id: int) -> bool:
        """
        기본 이력서 설정
        :param user_id: 사용자 ID
        :param resume_id: 이력서 ID
        :return: 설정 성공 여부
        """
        # TODO: 기본 이력서 플래그를 DB에 추가하면 좋음
        return True


class TimetableManager:
    """시간표 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        TimetableManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.timetable_dao = TimetableDAO(db_manager)
        
    def import_timetable(self, user_id: int, semester: str, schedule_data: dict) -> Optional[int]:
        """
        시간표 가져오기/등록 (FR-06: 시간표 연동)
        :param user_id: 사용자 ID
        :param semester: 학기
        :param schedule_data: 시간표 데이터
        :return: 생성된 시간표 ID 또는 None
        """
        from datetime import datetime

        timetable = Timetable(
            user_id=user_id,
            semester=semester,
            schedule_data=schedule_data,
            created_at=datetime.now()
        )

        return self.timetable_dao.insert_timetable(timetable)

    def update_timetable(self, timetable_id: int, schedule_data: dict) -> bool:
        """
        시간표 수정
        :param timetable_id: 시간표 ID
        :param schedule_data: 수정할 시간표 데이터
        :return: 수정 성공 여부
        """
        return self.timetable_dao.update_timetable(timetable_id, {'schedule_data': schedule_data})

    def get_timetable(self, user_id: int, semester: str = None) -> Optional[Dict]:
        """
        시간표 조회
        :param user_id: 사용자 ID
        :param semester: 학기 (None이면 현재 학기)
        :return: 시간표 딕셔너리 또는 None
        """
        if semester:
            timetable = self.timetable_dao.get_timetable_by_user(user_id, semester)
        else:
            timetable = self.timetable_dao.get_current_timetable(user_id)

        if timetable:
            return timetable.get_schedule()
        return None

    def check_time_conflict(self, user_id: int, day: str, start_time: str, end_time: str) -> bool:
        """
        시간표와 근무시간 충돌 확인
        :param user_id: 사용자 ID
        :param day: 요일
        :param start_time: 시작 시간
        :param end_time: 종료 시간
        :return: 충돌 여부 (True: 충돌, False: 가능)
        """
        timetable = self.timetable_dao.get_current_timetable(user_id)
        if not timetable:
            return False  # 시간표 없으면 충돌 없음

        return not timetable.is_available(day, start_time, end_time)

    def get_available_time_slots(self, user_id: int) -> List[Dict]:
        """
        가능한 시간대 조회
        :param user_id: 사용자 ID
        :return: 가능한 시간대 리스트
        """
        timetable = self.timetable_dao.get_current_timetable(user_id)
        if timetable:
            return timetable.get_free_slots()
        return []


class BookmarkManager:
    """관심공고(스크랩) 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        BookmarkManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.bookmark_dao = BookmarkDAO(db_manager)
        
    def add_bookmark(self, user_id: int, job_id: int) -> Optional[int]:
        """
        공고 북마크 추가 (FR-09: 관심공고 스크랩)
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 생성된 북마크 ID 또는 None
        """
        from datetime import datetime

        bookmark = Bookmark(
            user_id=user_id,
            job_id=job_id,
            created_at=datetime.now()
        )

        return self.bookmark_dao.insert_bookmark(bookmark)

    def remove_bookmark(self, user_id: int, job_id: int) -> bool:
        """
        공고 북마크 제거
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 제거 성공 여부
        """
        return self.bookmark_dao.delete_bookmark_by_job(user_id, job_id)

    def get_bookmarks(self, user_id: int) -> List[Job]:
        """
        사용자의 북마크 목록 조회
        :param user_id: 사용자 ID
        :return: Job 객체 리스트
        """
        bookmarks = self.bookmark_dao.get_bookmarks_by_user(user_id)
        job_dao = JobDAO(self.db_manager)

        jobs = []
        for bookmark in bookmarks:
            job = job_dao.get_job_by_id(bookmark.job_id)
            if job:
                jobs.append(job)
        return jobs

    def check_bookmark(self, user_id: int, job_id: int) -> bool:
        """
        북마크 여부 확인
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 북마크 여부
        """
        return self.bookmark_dao.is_bookmarked(user_id, job_id)

    def check_expiring_bookmarks(self, user_id: int) -> List[Job]:
        """
        마감 임박 북마크 확인 (FR-09: 리마인더)
        :param user_id: 사용자 ID
        :return: 마감 임박 공고 리스트
        """
        bookmarked_jobs = self.get_bookmarks(user_id)
        expiring_jobs = []

        for job in bookmarked_jobs:
            if job.deadline:
                days_left = job.get_remaining_days()
                if 0 <= days_left <= 3:
                    expiring_jobs.append(job)

        return expiring_jobs


class ViewHistoryManager:
    """열람 이력 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        ViewHistoryManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.view_history_dao = ViewHistoryDAO(db_manager)
        
    def record_view(self, user_id: int, job_id: int):
        """
        공고 열람 이력 기록 (FR-10: 알바 열람 이력)
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        """
        from datetime import datetime

        history = ViewHistory(
            user_id=user_id,
            job_id=job_id,
            viewed_at=datetime.now()
        )

        self.view_history_dao.insert_view_history(history)

    def get_recent_views(self, user_id: int, days: int = 7) -> List[Job]:
        """
        최근 열람한 공고 목록 조회
        :param user_id: 사용자 ID
        :param days: 조회할 일수
        :return: Job 객체 리스트
        """
        histories = self.view_history_dao.get_recent_views(user_id, days)
        job_dao = JobDAO(self.db_manager)

        jobs = []
        seen_job_ids = set()
        for history in histories:
            if history.job_id not in seen_job_ids:
                job = job_dao.get_job_by_id(history.job_id)
                if job:
                    jobs.append(job)
                    seen_job_ids.add(history.job_id)

        return jobs

    def get_view_statistics(self, job_id: int) -> Dict:
        """
        공고 조회 통계 조회
        :param job_id: 공고 ID
        :return: 통계 정보 딕셔너리
        """
        view_count = self.view_history_dao.get_view_count(job_id)
        return {
            "job_id": job_id,
            "total_views": view_count
        }


class RecommendationManager:
    """AI 추천 매니저"""
    
    def __init__(self, db_manager):
        """
        RecommendationManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.timetable_manager = TimetableManager(db_manager)
        self.view_history_manager = ViewHistoryManager(db_manager)
        
    def recommend_jobs(self, user_id: int, limit: int = 10) -> List[Job]:
        """
        사용자 맞춤 공고 추천 (FR-08: AI 추천)
        시간표, 열람 이력, 지원 이력 등을 종합 분석
        :param user_id: 사용자 ID
        :param limit: 추천 개수
        :return: 추천 공고 리스트
        """
        # 활성 공고 가져오기
        job_dao = JobDAO(self.db_manager)
        all_jobs = job_dao.get_active_jobs()

        # 시간표로 필터링
        available_jobs = self.filter_by_timetable(user_id, all_jobs)

        # 매칭 점수 계산 및 정렬
        scored_jobs = []
        for job in available_jobs:
            score = self.calculate_match_score(user_id, job.job_id)
            scored_jobs.append((job, score))

        scored_jobs.sort(key=lambda x: x[1], reverse=True)

        return [job for job, score in scored_jobs[:limit]]

    def analyze_user_preference(self, user_id: int) -> Dict:
        """
        사용자 선호도 분석
        :param user_id: 사용자 ID
        :return: 선호도 정보 딕셔너리
        """
        # 열람 이력 기반 선호도 분석
        recent_views = self.view_history_manager.get_recent_views(user_id, 30)

        categories = {}
        locations = {}

        for job in recent_views:
            if job.category:
                categories[job.category] = categories.get(job.category, 0) + 1
            if job.location:
                locations[job.location] = locations.get(job.location, 0) + 1

        return {
            "preferred_categories": categories,
            "preferred_locations": locations
        }

    def filter_by_timetable(self, user_id: int, jobs: List[Job]) -> List[Job]:
        """
        시간표 기반 공고 필터링
        :param user_id: 사용자 ID
        :param jobs: 필터링할 공고 리스트
        :return: 필터링된 공고 리스트
        """
        # TODO: 근무 시간 정보가 공고에 있다면 시간표와 비교
        # 현재는 모든 공고 반환
        return jobs

    def calculate_match_score(self, user_id: int, job_id: int) -> float:
        """
        사용자-공고 매칭 점수 계산
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 매칭 점수 (0.0 ~ 1.0)
        """
        # 간단한 매칭 로직 (실제로는 더 복잡한 알고리즘 필요)
        score = 0.5  # 기본 점수

        # 선호도 기반 점수 증가
        preferences = self.analyze_user_preference(user_id)
        job_dao = JobDAO(self.db_manager)
        job = job_dao.get_job_by_id(job_id)

        if job:
            if job.category in preferences.get('preferred_categories', {}):
                score += 0.3
            if job.location in preferences.get('preferred_locations', {}):
                score += 0.2

        return min(1.0, score)


class FAQManager:
    """FAQ 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        FAQManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.faq_dao = FAQdao(db_manager)
        
    def get_all_faqs(self) -> List[Dict]:
        """
        모든 FAQ 조회 (FR-07: 문의/FAQ)
        :return: FAQ 리스트
        """
        faqs = self.faq_dao.get_all_faqs()
        return [faq.get_info() for faq in faqs]

    def get_faqs_by_category(self, category: str) -> List[Dict]:
        """
        카테고리별 FAQ 조회
        :param category: 카테고리
        :return: FAQ 리스트
        """
        faqs = self.faq_dao.get_faqs_by_category(category)
        return [faq.get_info() for faq in faqs]

    def search_faqs(self, keyword: str) -> List[Dict]:
        """
        FAQ 검색
        :param keyword: 검색 키워드
        :return: 검색 결과 리스트
        """
        faqs = self.faq_dao.search_faqs(keyword)
        return [faq.get_info() for faq in faqs]

    def add_faq(self, faq_data: dict) -> Optional[int]:
        """
        새로운 FAQ 추가 (관리자용)
        :param faq_data: FAQ 정보
        :return: 생성된 FAQ ID 또는 None
        """
        from datetime import datetime

        faq = FAQ(
            category=faq_data.get('category'),
            question=faq_data.get('question'),
            answer=faq_data.get('answer'),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            view_count=0
        )

        return self.faq_dao.insert_faq(faq)


class InquiryManager:
    """1:1 문의 관리 매니저"""
    
    def __init__(self, db_manager):
        """
        InquiryManager 초기화
        :param db_manager: DatabaseManager 인스턴스
        """
        self.db_manager = db_manager
        self.inquiry_dao = InquiryDAO(db_manager)
        
    def create_inquiry(self, inquiry_data: dict) -> Optional[int]:
        """
        새로운 문의 작성 (FR-07: 1:1 문의)
        :param inquiry_data: 문의 정보
        :return: 생성된 문의 ID 또는 None
        """
        from datetime import datetime

        inquiry = Inquiry(
            user_id=inquiry_data.get('user_id'),
            title=inquiry_data.get('title'),
            content=inquiry_data.get('content'),
            status='대기중',
            created_at=datetime.now()
        )

        return self.inquiry_dao.insert_inquiry(inquiry)
    
    def get_user_inquiries(self, user_id: int) -> List[Dict]:
        """
        사용자의 문의 목록 조회
        :param user_id: 사용자 ID
        :return: 문의 리스트
        """
        inquiries = self.inquiry_dao.get_inquiries_by_user(user_id)
        return [inquiry.get_info() for inquiry in inquiries]
    
    def get_inquiry_detail(self, inquiry_id: int) -> Optional[Dict]:
        """
        문의 상세 조회
        :param inquiry_id: 문의 ID
        :return: 문의 정보 딕셔너리 또는 None
        """
        inquiry = self.inquiry_dao.get_inquiry_by_id(inquiry_id)
        return inquiry.get_info() if inquiry else None
    
    def answer_inquiry(self, inquiry_id: int, answer: str) -> bool:
        """
        문의 답변 작성 (관리자/담당자용)
        :param inquiry_id: 문의 ID
        :param answer: 답변 내용
        :return: 답변 성공 여부
        """
        from datetime import datetime

        inquiry = self.inquiry_dao.get_inquiry_by_id(inquiry_id)
        if not inquiry:
            return False

        inquiry.answer = answer
        inquiry.status = '답변완료'
        inquiry.answered_at = datetime.now()

        result = self.inquiry_dao.update_inquiry(inquiry)
        return result is not None and result > 0
    
    def get_unanswered_inquiries(self) -> List[Dict]:
        """
        미답변 문의 목록 조회 (관리자/담당자용)
        :return: 미답변 문의 리스트
        """
        inquiries = self.inquiry_dao.get_unanswered_inquiries()
        return [inquiry.get_info() for inquiry in inquiries]
