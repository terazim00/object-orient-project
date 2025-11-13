"""
메인 애플리케이션
전체 시스템을 통합하고 실행하는 메인 클래스
"""

import tkinter as tk
from database_manager import DatabaseManager
from managers import (UserManager, JobManager, ApplicationManager, 
                     NotificationManager, ResumeManager, TimetableManager,
                     BookmarkManager, ViewHistoryManager, RecommendationManager)
from gui_modules import LoginWindow, MainWindow

class Application:
    """메인 애플리케이션 클래스"""
    
    def __init__(self):
        """
        애플리케이션 초기화
        """
        self.root = tk.Tk()
        self.root.title("한기WORKS - 근로장학 관리 시스템")
        self.root.geometry("1200x800")
        
        # 데이터베이스 초기화
        self.db_manager = None
        
        # Manager 인스턴스들
        self.user_manager = None
        self.job_manager = None
        self.application_manager = None
        self.notification_manager = None
        self.resume_manager = None
        self.timetable_manager = None
        self.bookmark_manager = None
        self.view_history_manager = None
        self.recommendation_manager = None
        self.faq_manager = None
        self.inquiry_manager = None
        
        # 현재 로그인한 사용자
        self.current_user = None
        
        # 현재 화면
        self.current_window = None
        
    def initialize(self):
        """
        애플리케이션 초기화
        - 데이터베이스 연결
        - Manager 인스턴스 생성
        - 초기 화면 설정
        """
        # 데이터베이스 설정
        self.setup_database()

        # Manager 인스턴스 생성
        self.setup_managers()

        # 기본 관리자 계정 생성 (개발/테스트용)
        self.create_default_admin()

        # 로그인 화면 표시
        self.show_login_window()
    
    def setup_database(self):
        """
        데이터베이스 설정
        - SQLite 연결
        - 테이블 생성
        """
        # DatabaseManager 인스턴스 생성
        self.db_manager = DatabaseManager(Config.DATABASE_PATH)

        # 데이터베이스 연결
        self.db_manager.connect()

        # 테이블 생성
        self.db_manager.create_tables()
    
    def setup_managers(self):
        """
        모든 Manager 인스턴스 초기화
        """
        from managers import FAQManager, InquiryManager

        # 각 Manager 인스턴스 생성
        self.user_manager = UserManager(self.db_manager)
        self.job_manager = JobManager(self.db_manager)
        self.application_manager = ApplicationManager(self.db_manager)
        self.notification_manager = NotificationManager(self.db_manager)
        self.resume_manager = ResumeManager(self.db_manager)
        self.timetable_manager = TimetableManager(self.db_manager)
        self.bookmark_manager = BookmarkManager(self.db_manager)
        self.view_history_manager = ViewHistoryManager(self.db_manager)
        self.recommendation_manager = RecommendationManager(self.db_manager)
        self.faq_manager = FAQManager(self.db_manager)
        self.inquiry_manager = InquiryManager(self.db_manager)

    def create_default_admin(self):
        """
        기본 관리자 계정 생성 (개발/테스트용)
        학번: admin (0000000000)
        이름: 관리자
        """
        from dao import UserDAO

        user_dao = UserDAO(self.db_manager)

        # admin 계정이 이미 있는지 확인
        existing_admin = user_dao.get_user_by_student_id("0000000000")

        if not existing_admin:
            # 없으면 생성
            admin_data = {
                'student_id': '0000000000',
                'username': '관리자',
                'department': '시스템',
                'role': 'admin'
            }

            admin_id = self.user_manager.register(admin_data)

            if admin_id:
                print("기본 관리자 계정이 생성되었습니다. (학번: 0000000000)")
            else:
                print("관리자 계정 생성 실패")
        else:
            print("관리자 계정이 이미 존재합니다.")

    def show_login_window(self):
        """
        로그인 화면 표시
        """
        # 기존 창이 있으면 제거
        if self.current_window:
            self.current_window.destroy()

        # 로그인 창 생성
        self.current_window = LoginWindow(
            self.root,
            self.user_manager,
            on_login_success=self.on_login_success
        )
    
    def show_main_window(self):
        """
        메인 화면 표시
        """
        # 기존 창이 있으면 제거
        if self.current_window:
            self.current_window.destroy()

        # 메인 창 생성
        self.current_window = MainWindow(
            self.root,
            self.current_user,
            self.job_manager,
            self.application_manager,
            self.resume_manager,
            self.timetable_manager,
            self.notification_manager,
            self.bookmark_manager,
            self.view_history_manager,
            self.recommendation_manager,
            self.faq_manager,
            self.inquiry_manager,
            on_logout=self.on_logout
        )
    
    def on_login_success(self, user):
        """
        로그인 성공 시 처리
        :param user: 로그인한 User 객체
        """
        # 현재 사용자 설정
        self.current_user = user

        # 백그라운드 작업 시작
        self.start_background_tasks()

        # 메인 화면으로 전환
        self.show_main_window()
    
    def on_logout(self):
        """
        로그아웃 처리
        """
        # 사용자 로그아웃
        if self.current_user:
            self.user_manager.logout(self.current_user.user_id)

        # 현재 사용자 초기화
        self.current_user = None

        # 로그인 화면으로 전환
        self.show_login_window()
    
    def start_background_tasks(self):
        """
        백그라운드 작업 시작
        - 공고 수집 (FR-01: 10분 주기)
        - 알림 확인 (PERP-03: 5분 이내)
        - 자동 임시저장 (REL-01: 30초마다)
        """
        import threading

        # 공고 수집 작업 (10분 주기)
        job_collection_thread = threading.Thread(
            target=self.collect_job_announcements_task,
            daemon=True
        )
        job_collection_thread.start()

        # 알림 확인 작업 (5분 주기)
        notification_thread = threading.Thread(
            target=self.check_notifications_task,
            daemon=True
        )
        notification_thread.start()

        # 마감 리마인더 작업 (일일 1회)
        deadline_thread = threading.Thread(
            target=self.check_deadline_reminders_task,
            daemon=True
        )
        deadline_thread.start()
    
    def collect_job_announcements_task(self):
        """
        공고 수집 백그라운드 작업 (FR-01)
        10분 주기로 실행
        """
        import time

        while True:
            try:
                # TODO: 실제 공고 수집 API 연동
                # 현재는 더미 구현
                print("공고 수집 작업 실행...")

                # 10분 대기
                time.sleep(Config.JOB_COLLECTION_INTERVAL_MIN * 60)
            except Exception as e:
                print(f"공고 수집 작업 에러: {e}")
                time.sleep(60)  # 에러 발생 시 1분 후 재시도
    
    def check_notifications_task(self):
        """
        알림 확인 백그라운드 작업
        주기적으로 실행
        """
        import time

        while True:
            try:
                if self.current_user:
                    # 읽지 않은 알림 확인
                    unread_notifications = self.notification_manager.get_unread_notifications(
                        self.current_user.user_id
                    )

                    # TODO: GUI에 알림 표시
                    if unread_notifications:
                        print(f"새로운 알림 {len(unread_notifications)}개")

                # 5분 대기
                time.sleep(Config.NOTIFICATION_DELAY_MIN * 60)
            except Exception as e:
                print(f"알림 확인 작업 에러: {e}")
                time.sleep(60)  # 에러 발생 시 1분 후 재시도
    
    def check_deadline_reminders_task(self):
        """
        마감 임박 리마인더 확인 (FR-09)
        일일 1회 실행
        """
        import time
        from datetime import datetime, timedelta

        while True:
            try:
                # 마감 3일 이내의 공고 조회
                all_jobs = self.job_manager.get_all_jobs()
                deadline_jobs = []

                for job in all_jobs:
                    if job.deadline:
                        days_until = DateTimeHelper.calculate_days_until(job.deadline.isoformat())
                        if 0 <= days_until <= 3:
                            deadline_jobs.append(job)

                # 해당 공고에 북마크한 사용자들에게 알림
                for job in deadline_jobs:
                    # TODO: 북마크 사용자 조회 및 알림 전송
                    pass

                # 24시간 대기
                time.sleep(24 * 60 * 60)
            except Exception as e:
                print(f"마감 리마인더 작업 에러: {e}")
                time.sleep(60 * 60)  # 에러 발생 시 1시간 후 재시도
    
    def cleanup_old_data_task(self):
        """
        오래된 데이터 정리
        - 탈퇴 사용자 데이터 파기 (SEC-02: 7일)
        - 오래된 열람 이력 삭제
        """
        import time
        from datetime import datetime, timedelta

        while True:
            try:
                # 오래된 열람 이력 삭제 (30일 이상)
                cutoff_date = datetime.now() - timedelta(days=30)
                # TODO: 오래된 열람 이력 삭제 로직

                # 24시간 대기
                time.sleep(24 * 60 * 60)
            except Exception as e:
                print(f"데이터 정리 작업 에러: {e}")
                time.sleep(60 * 60)  # 에러 발생 시 1시간 후 재시도
    
    def run(self):
        """
        애플리케이션 실행
        """
        # Tkinter 이벤트 루프 시작
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.root.mainloop()
    
    def shutdown(self):
        """
        애플리케이션 종료 처리
        - 데이터베이스 연결 종료
        - 리소스 정리
        """
        # 데이터베이스 연결 종료
        if self.db_manager:
            self.db_manager.disconnect()

        # Tkinter 창 종료
        self.root.quit()
        self.root.destroy()


class Config:
    """설정 클래스"""
    
    # 데이터베이스 설정
    DATABASE_PATH = "hangi_works.db"
    
    # 성능 설정 (PERP)
    SEARCH_TIMEOUT_MS = 1000  # PERP-01: 검색 1000ms 이내
    JOB_UPDATE_INTERVAL_MIN = 2  # PERP-02: 공고 최신화 2분 이내
    NOTIFICATION_DELAY_MIN = 5  # PERP-03: 알림 5분 이내
    
    # 품질 설정 (REL)
    AUTO_SAVE_INTERVAL_SEC = 30  # REL-01: 30초마다 자동저장
    TARGET_AVAILABILITY = 0.995  # REL-02: 99.5% 가용성
    
    # 보안 설정 (SEC)
    USE_SSO = True  # SEC-01: 학교 SSO 사용
    DATA_RETENTION_DAYS = 7  # SEC-02: 데이터 보관 기간
    AUDIT_LOG_RETENTION_MONTHS = 6  # SEC-03: 감사 로그 보관 기간
    
    # 사용성 설정 (UX)
    SUPPORT_DARK_MODE = True  # UX-01: 다크모드 지원
    MAX_APPLICATION_STEPS = 3  # UX-02: 지원서 제출 최대 단계
    
    # 기능 설정
    JOB_COLLECTION_INTERVAL_MIN = 10  # FR-01: 공고 수집 주기
    RECENT_VIEW_DAYS = 7  # FR-10: 최근 열람 기준 일수
    
    # UI 설정
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    FONT_FAMILY = "맑은 고딕"
    DEFAULT_FONT_SIZE = 10
    
    # 색상 테마
    LIGHT_THEME = {
        "bg": "#FFFFFF",
        "fg": "#000000",
        "primary": "#007AFF",
        "secondary": "#5856D6",
        "success": "#34C759",
        "warning": "#FF9500",
        "danger": "#FF3B30"
    }
    
    DARK_THEME = {
        "bg": "#1C1C1E",
        "fg": "#FFFFFF",
        "primary": "#0A84FF",
        "secondary": "#5E5CE6",
        "success": "#30D158",
        "warning": "#FF9F0A",
        "danger": "#FF453A"
    }


class Logger:
    """로깅 클래스"""
    
    def __init__(self, log_file: str = "hangi_works.log"):
        """
        로거 초기화
        :param log_file: 로그 파일 경로
        """
        self.log_file = log_file
        
    def log_info(self, message: str):
        """
        정보 로그 기록
        :param message: 로그 메시지
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [INFO] {message}\n"

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(log_entry.strip())
    
    def log_warning(self, message: str):
        """
        경고 로그 기록
        :param message: 로그 메시지
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [WARNING] {message}\n"

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(log_entry.strip())
    
    def log_error(self, message: str, exception=None):
        """
        에러 로그 기록
        :param message: 로그 메시지
        :param exception: 예외 객체
        """
        from datetime import datetime
        import traceback

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [ERROR] {message}\n"

        if exception:
            log_entry += f"Exception: {str(exception)}\n"
            log_entry += traceback.format_exc()

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(log_entry.strip())
    
    def log_audit(self, user_id: int, action: str, details: str = None):
        """
        감사 로그 기록 (SEC-03: 6개월 이상 보관)
        :param user_id: 사용자 ID
        :param action: 수행한 작업
        :param details: 상세 정보
        """
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [AUDIT] UserID={user_id}, Action={action}"

        if details:
            log_entry += f", Details={details}"

        log_entry += "\n"

        # 감사 로그는 별도 파일에 기록
        audit_log_file = self.log_file.replace('.log', '_audit.log')

        with open(audit_log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)


class Validator:
    """유효성 검사 유틸리티 클래스"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        이메일 유효성 검사
        :param email: 이메일 주소
        :return: 유효성 여부
        """
        import re

        if not email:
            return False

        # 이메일 정규식 패턴
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        전화번호 유효성 검사
        :param phone: 전화번호
        :return: 유효성 여부
        """
        import re

        if not phone:
            return False

        # 한국 전화번호 패턴 (010-1234-5678, 01012345678 등)
        pattern = r'^(01[0-9])-?([0-9]{3,4})-?([0-9]{4})$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """
        학번 유효성 검사
        :param student_id: 학번
        :return: 유효성 여부
        """
        import re

        if not student_id:
            return False

        # 학번 패턴 (예: 2024123456, 10자리 숫자)
        pattern = r'^[0-9]{10}$'
        return bool(re.match(pattern, student_id))
    
    @staticmethod
    def validate_required_fields(data: dict, required_fields: list) -> tuple:
        """
        필수 필드 검사
        :param data: 검사할 데이터
        :param required_fields: 필수 필드 리스트
        :return: (유효성 여부, 에러 메시지)
        """
        missing_fields = []

        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                missing_fields.append(field)

        if missing_fields:
            error_message = f"필수 필드가 누락되었습니다: {', '.join(missing_fields)}"
            return (False, error_message)

        return (True, None)


class DateTimeHelper:
    """날짜/시간 관련 유틸리티 클래스"""
    
    @staticmethod
    def get_current_datetime() -> str:
        """
        현재 날짜/시간 반환
        :return: ISO 형식 날짜/시간 문자열
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    @staticmethod
    def get_current_semester() -> str:
        """
        현재 학기 반환
        :return: 학기 문자열 (예: 2025-1)
        """
        from datetime import datetime

        now = datetime.now()
        year = now.year
        month = now.month

        # 3월-8월: 1학기, 9월-2월: 2학기
        if 3 <= month <= 8:
            semester = 1
        else:
            semester = 2

        return f"{year}-{semester}"
    
    @staticmethod
    def calculate_days_until(target_date: str) -> int:
        """
        특정 날짜까지 남은 일수 계산
        :param target_date: 목표 날짜
        :return: 남은 일수
        """
        from datetime import datetime

        try:
            target = datetime.fromisoformat(target_date)
            now = datetime.now()
            delta = target - now
            return delta.days
        except Exception:
            return -1
    
    @staticmethod
    def format_datetime(datetime_str: str, format: str = "%Y-%m-%d %H:%M") -> str:
        """
        날짜/시간 포맷 변환
        :param datetime_str: 날짜/시간 문자열
        :param format: 출력 형식
        :return: 포맷팅된 문자열
        """
        from datetime import datetime

        try:
            dt = datetime.fromisoformat(datetime_str)
            return dt.strftime(format)
        except Exception:
            return datetime_str
    
    @staticmethod
    def is_expired(deadline: str) -> bool:
        """
        마감일 경과 여부 확인
        :param deadline: 마감일
        :return: 경과 여부
        """
        from datetime import datetime

        try:
            deadline_dt = datetime.fromisoformat(deadline)
            now = datetime.now()
            return now > deadline_dt
        except Exception:
            return False


def main():
    """
    프로그램 진입점
    """
    # 애플리케이션 생성
    app = Application()
    
    # 초기화
    app.initialize()
    
    # 실행
    app.run()


if __name__ == "__main__":
    main()
