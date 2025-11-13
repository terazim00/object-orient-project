"""
GUI 모듈
Python Tkinter 기반 사용자 인터페이스
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont


class LoginWindow:
    """로그인 화면"""

    def __init__(self, root, user_manager, on_login_success):
        """
        로그인 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user_manager: UserManager 인스턴스
        :param on_login_success: 로그인 성공 콜백 함수
        """
        self.root = root
        self.user_manager = user_manager
        self.on_login_success = on_login_success

        # 입력 필드
        self.username_entry = None
        self.password_entry = None

        # UI 구성
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        """
        로그인 화면 UI 구성
        - 학번/아이디 입력 필드
        - 비밀번호 입력 필드
        - 로그인 버튼
        - 회원가입 버튼
        """
        # 제목
        title_label = tk.Label(
            self.frame,
            text="한기WORKS",
            font=("맑은 고딕", 24, "bold")
        )
        title_label.pack(pady=50)

        # 입력 프레임
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=20)

        # 학번/아이디
        tk.Label(input_frame, text="학번/아이디:", font=("맑은 고딕", 12)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.username_entry = tk.Entry(input_frame, font=("맑은 고딕", 12), width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # 비밀번호
        tk.Label(input_frame, text="비밀번호:", font=("맑은 고딕", 12)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.password_entry = tk.Entry(input_frame, font=("맑은 고딕", 12), width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # 버튼 프레임
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=20)

        # 로그인 버튼
        login_btn = tk.Button(
            button_frame,
            text="로그인",
            font=("맑은 고딕", 12),
            width=15,
            command=self.on_login_click
        )
        login_btn.pack(side=tk.LEFT, padx=10)

        # 회원가입 버튼
        register_btn = tk.Button(
            button_frame,
            text="회원가입",
            font=("맑은 고딕", 12),
            width=15,
            command=self.on_register_click
        )
        register_btn.pack(side=tk.LEFT, padx=10)

        # Enter 키로 로그인
        self.password_entry.bind('<Return>', lambda e: self.on_login_click())

    def on_login_click(self):
        """
        로그인 버튼 클릭 이벤트 처리
        학교 SSO 연동 (SEC-01)
        """
        if not self.validate_input():
            return

        username = self.username_entry.get()
        password = self.password_entry.get()

        # 로그인 시도
        user = self.user_manager.login(username, password)

        if user:
            messagebox.showinfo("로그인 성공", f"환영합니다, {user.username}님!")
            self.on_login_success(user)
        else:
            messagebox.showerror("로그인 실패", "학번/아이디 또는 비밀번호가 올바르지 않습니다.")

    def on_register_click(self):
        """
        회원가입 버튼 클릭 이벤트 처리
        """
        messagebox.showinfo("회원가입", "회원가입 기능은 학교 SSO를 통해 자동으로 진행됩니다.")

    def validate_input(self) -> bool:
        """
        입력 값 유효성 검사
        :return: 유효성 여부
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username:
            messagebox.showwarning("입력 오류", "학번/아이디를 입력해주세요.")
            return False

        if not password:
            messagebox.showwarning("입력 오류", "비밀번호를 입력해주세요.")
            return False

        return True

    def destroy(self):
        """프레임 제거"""
        self.frame.destroy()


class MainWindow:
    """메인 화면 (홈화면)"""

    def __init__(self, root, user, job_manager, application_manager, resume_manager,
                 timetable_manager, notification_manager, bookmark_manager,
                 view_history_manager, recommendation_manager, faq_manager,
                 inquiry_manager, on_logout):
        """
        메인 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        :param job_manager: JobManager 인스턴스
        :param application_manager: ApplicationManager 인스턴스
        :param resume_manager: ResumeManager 인스턴스
        :param timetable_manager: TimetableManager 인스턴스
        :param notification_manager: NotificationManager 인스턴스
        :param bookmark_manager: BookmarkManager 인스턴스
        :param view_history_manager: ViewHistoryManager 인스턴스
        :param recommendation_manager: RecommendationManager 인스턴스
        :param faq_manager: FAQManager 인스턴스
        :param inquiry_manager: InquiryManager 인스턴스
        :param on_logout: 로그아웃 콜백 함수
        """
        self.root = root
        self.user = user
        self.job_manager = job_manager
        self.application_manager = application_manager
        self.resume_manager = resume_manager
        self.timetable_manager = timetable_manager
        self.notification_manager = notification_manager
        self.bookmark_manager = bookmark_manager
        self.view_history_manager = view_history_manager
        self.recommendation_manager = recommendation_manager
        self.faq_manager = faq_manager
        self.inquiry_manager = inquiry_manager
        self.on_logout = on_logout

        # UI 요소
        self.search_entry = None
        self.job_listbox = None
        self.current_jobs = []

        # 메인 프레임
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        """
        메인 화면 UI 구성
        - 상단 네비게이션 바
        - 검색 바
        - 공고 카드 리스트
        - 사이드바 (필터)
        """
        self.setup_navigation_bar()
        self.setup_search_bar()

        # 메인 컨텐츠 영역
        content_frame = tk.Frame(self.frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 필터 사이드바 (왼쪽)
        self.setup_filter_sidebar(content_frame)

        # 공고 리스트 (오른쪽)
        job_list_frame = tk.Frame(content_frame)
        job_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # 공고 리스트박스
        tk.Label(job_list_frame, text="근로장학 공고 목록", font=("맑은 고딕", 14, "bold")).pack(pady=10)

        scrollbar = tk.Scrollbar(job_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.job_listbox = tk.Listbox(
            job_list_frame,
            font=("맑은 고딕", 10),
            yscrollcommand=scrollbar.set,
            height=20
        )
        self.job_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.job_listbox.yview)

        self.job_listbox.bind('<Double-Button-1>', lambda e: self.on_job_click())

        # 초기 공고 로드
        self.load_all_jobs()

    def setup_navigation_bar(self):
        """
        네비게이션 바 구성
        - 홈 버튼
        - 지원현황 버튼
        - 관심공고 버튼
        - 마이페이지 버튼
        - 알림 아이콘
        """
        nav_frame = tk.Frame(self.frame, bg="#007AFF", height=50)
        nav_frame.pack(fill=tk.X)

        # 왼쪽: 제목
        tk.Label(
            nav_frame,
            text=f"한기WORKS - {self.user.username}님 환영합니다",
            font=("맑은 고딕", 12, "bold"),
            bg="#007AFF",
            fg="white"
        ).pack(side=tk.LEFT, padx=20, pady=10)

        # 오른쪽: 버튼들
        btn_frame = tk.Frame(nav_frame, bg="#007AFF")
        btn_frame.pack(side=tk.RIGHT, padx=20)

        buttons = [
            ("홈", self.on_home_click),
            ("지원현황", self.on_applications_click),
            ("관심공고", self.on_bookmarks_click),
            ("마이페이지", self.on_mypage_click),
            ("로그아웃", self.on_logout)
        ]

        for text, command in buttons:
            tk.Button(
                btn_frame,
                text=text,
                font=("맑은 고딕", 10),
                command=command,
                bg="white",
                width=10
            ).pack(side=tk.LEFT, padx=5)

    def setup_search_bar(self):
        """
        검색 바 구성
        """
        search_frame = tk.Frame(self.frame)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(search_frame, text="검색:", font=("맑은 고딕", 11)).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_frame, font=("맑은 고딕", 11), width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.on_search())

        tk.Button(
            search_frame,
            text="검색",
            font=("맑은 고딕", 11),
            command=self.on_search,
            width=10
        ).pack(side=tk.LEFT, padx=5)

    def setup_filter_sidebar(self, parent):
        """
        필터 사이드바 구성 (FR-03)
        - 장소 필터
        - 장기/단기/일일 필터
        - 급여 범위 필터
        """
        filter_frame = tk.Frame(parent, width=200, relief=tk.RIDGE, borderwidth=2)
        filter_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(filter_frame, text="필터", font=("맑은 고딕", 12, "bold")).pack(pady=10)

        # TODO: 실제 필터 구현
        tk.Label(filter_frame, text="장소", font=("맑은 고딕", 10)).pack(pady=5)
        tk.Label(filter_frame, text="근무 유형", font=("맑은 고딕", 10)).pack(pady=5)
        tk.Label(filter_frame, text="급여 범위", font=("맑은 고딕", 10)).pack(pady=5)

    def load_all_jobs(self):
        """모든 공고 로드"""
        try:
            jobs = self.job_manager.get_all_jobs()
            self.display_job_list(jobs)
        except Exception as e:
            messagebox.showerror("오류", f"공고 로드 실패: {e}")

    def display_job_list(self, jobs: list):
        """
        공고 목록 표시
        :param jobs: Job 객체 리스트
        """
        self.job_listbox.delete(0, tk.END)
        self.current_jobs = jobs

        for job in jobs:
            display_text = f"{job.title} | {job.location} | {job.salary}원"
            self.job_listbox.insert(tk.END, display_text)

    def on_search(self):
        """
        검색 실행 (PERP-01: 1000ms 이내)
        """
        keyword = self.search_entry.get().strip()

        if not keyword:
            self.load_all_jobs()
            return

        try:
            jobs = self.job_manager.search_jobs(keyword)
            self.display_job_list(jobs)
        except Exception as e:
            messagebox.showerror("검색 오류", f"검색 실패: {e}")

    def on_filter_change(self):
        """
        필터 변경 이벤트 처리
        """
        # TODO: 필터 적용 로직
        pass

    def on_job_click(self):
        """
        공고 클릭 이벤트 처리
        """
        selection = self.job_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index < len(self.current_jobs):
            job = self.current_jobs[index]
            messagebox.showinfo("공고 상세", f"{job.title}\n\n{job.description}")

    def on_home_click(self):
        """홈 버튼 클릭"""
        self.load_all_jobs()

    def on_applications_click(self):
        """지원현황 버튼 클릭"""
        messagebox.showinfo("지원현황", "지원현황 화면 (구현 예정)")

    def on_bookmarks_click(self):
        """관심공고 버튼 클릭"""
        messagebox.showinfo("관심공고", "관심공고 화면 (구현 예정)")

    def on_mypage_click(self):
        """마이페이지 버튼 클릭"""
        messagebox.showinfo("마이페이지", "마이페이지 화면 (구현 예정)")

    def destroy(self):
        """프레임 제거"""
        self.frame.destroy()


class JobDetailWindow:
    """공고 상세 화면"""
    
    def __init__(self, root, job_id: int, user):
        """
        공고 상세 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param job_id: 공고 ID
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.job_id = job_id
        self.user = user
        self.job_manager = None
        
    def setup_ui(self):
        """
        공고 상세 화면 UI 구성
        - 공고 제목 및 기본 정보
        - 상세 설명
        - 근무 조건
        - 지원 자격
        - 지원하기 버튼
        - 북마크 버튼
        """
        pass
    
    def load_job_details(self):
        """
        공고 상세 정보 로드
        """
        pass
    
    def on_apply_click(self):
        """
        지원하기 버튼 클릭 이벤트 처리
        """
        pass
    
    def on_bookmark_click(self):
        """
        북마크 버튼 클릭 이벤트 처리 (FR-09)
        """
        pass
    
    def check_time_conflict(self) -> bool:
        """
        시간표 충돌 확인 (FR-06)
        :return: 충돌 여부
        """
        pass


class ApplicationWindow:
    """지원서 작성 화면"""
    
    def __init__(self, root, job_id: int, user):
        """
        지원서 작성 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param job_id: 지원할 공고 ID
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.job_id = job_id
        self.user = user
        self.application_manager = None
        self.resume_manager = None
        
    def setup_ui(self):
        """
        지원서 작성 화면 UI 구성 (UX-02: 3단계 이내)
        - 이력서 선택
        - 자기소개서 작성
        - 제출 버튼
        """
        pass
    
    def load_user_resumes(self):
        """
        사용자의 이력서 목록 로드 (FR-04)
        """
        pass
    
    def on_resume_select(self, resume_id: int):
        """
        이력서 선택 이벤트 처리
        :param resume_id: 선택한 이력서 ID
        """
        pass
    
    def on_submit_click(self):
        """
        제출 버튼 클릭 이벤트 처리
        """
        pass
    
    def auto_save(self):
        """
        자동 임시저장 (REL-01: 30초마다)
        """
        pass
    
    def validate_form(self) -> bool:
        """
        폼 유효성 검사
        :return: 유효성 여부
        """
        pass


class MyPageWindow:
    """마이페이지 화면"""
    
    def __init__(self, root, user):
        """
        마이페이지 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.user = user
        
    def setup_ui(self):
        """
        마이페이지 UI 구성
        - 이력서 관리 탭
        - 지원현황 탭
        - 스크랩 탭
        - 최근 본 알바 탭
        """
        pass
    
    def setup_resume_tab(self):
        """
        이력서 관리 탭 구성
        """
        pass
    
    def setup_application_tab(self):
        """
        지원현황 탭 구성 (FR-05: 타임라인)
        """
        pass
    
    def setup_bookmark_tab(self):
        """
        스크랩 탭 구성
        """
        pass
    
    def setup_history_tab(self):
        """
        최근 본 알바 탭 구성 (FR-10)
        """
        pass


class ApplicationStatusWindow:
    """지원현황 화면"""
    
    def __init__(self, root, user):
        """
        지원현황 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.user = user
        self.application_manager = None
        
    def setup_ui(self):
        """
        지원현황 화면 UI 구성
        - 지원서 목록
        - 각 지원서의 현재 상태
        - 타임라인 표시
        """
        pass
    
    def display_application_list(self, applications: list):
        """
        지원서 목록 표시
        :param applications: Application 객체 리스트
        """
        pass
    
    def display_timeline(self, application_id: int):
        """
        지원서 타임라인 표시 (FR-05)
        :param application_id: 지원서 ID
        """
        pass
    
    def on_application_click(self, application_id: int):
        """
        지원서 클릭 이벤트 처리
        :param application_id: 클릭한 지원서 ID
        """
        pass


class ResumeEditorWindow:
    """이력서 편집 화면"""
    
    def __init__(self, root, user, resume_id: int = None):
        """
        이력서 편집 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        :param resume_id: 수정할 이력서 ID (None이면 신규 작성)
        """
        self.root = root
        self.user = user
        self.resume_id = resume_id
        self.resume_manager = None
        
    def setup_ui(self):
        """
        이력서 편집 화면 UI 구성 (FR-04)
        - 학번/학과/경력 입력
        - 자격증 입력
        - 자기소개 입력
        - 저장 버튼
        """
        pass
    
    def load_resume_data(self):
        """
        기존 이력서 데이터 로드 (수정 모드)
        """
        pass
    
    def on_save_click(self):
        """
        저장 버튼 클릭 이벤트 처리
        """
        pass
    
    def validate_form(self) -> bool:
        """
        폼 유효성 검사
        :return: 유효성 여부
        """
        pass


class TimetableWindow:
    """시간표 관리 화면"""
    
    def __init__(self, root, user):
        """
        시간표 관리 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.user = user
        self.timetable_manager = None
        
    def setup_ui(self):
        """
        시간표 화면 UI 구성 (FR-06)
        - 시간표 그리드
        - 가져오기 버튼
        - 수정 버튼
        - 저장 버튼
        """
        pass
    
    def display_timetable(self, timetable_data: dict):
        """
        시간표 표시
        :param timetable_data: 시간표 데이터
        """
        pass
    
    def on_import_click(self):
        """
        시간표 가져오기 버튼 클릭 이벤트 처리
        """
        pass
    
    def on_save_click(self):
        """
        저장 버튼 클릭 이벤트 처리
        """
        pass


class NotificationPanel:
    """알림 패널"""
    
    def __init__(self, root, user):
        """
        알림 패널 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.user = user
        self.notification_manager = None
        
    def setup_ui(self):
        """
        알림 패널 UI 구성
        - 알림 목록
        - 읽음/안읽음 표시
        - 전체 읽음 버튼
        """
        pass
    
    def display_notifications(self, notifications: list):
        """
        알림 목록 표시
        :param notifications: Notification 객체 리스트
        """
        pass
    
    def on_notification_click(self, notification_id: int):
        """
        알림 클릭 이벤트 처리
        :param notification_id: 클릭한 알림 ID
        """
        pass
    
    def mark_all_as_read(self):
        """
        전체 읽음 처리
        """
        pass
    
    def check_new_notifications(self):
        """
        새 알림 확인 (PERP-03: 5분 이내 도착)
        """
        pass


class RecommendationPanel:
    """AI 추천 패널"""
    
    def __init__(self, root, user):
        """
        AI 추천 패널 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.user = user
        self.recommendation_manager = None
        
    def setup_ui(self):
        """
        추천 패널 UI 구성 (FR-08)
        - 추천 공고 카드
        - 매칭 점수 표시
        """
        pass
    
    def display_recommendations(self, jobs: list):
        """
        추천 공고 표시
        :param jobs: 추천된 Job 객체 리스트
        """
        pass
    
    def on_refresh_click(self):
        """
        추천 새로고침 버튼 클릭 이벤트 처리
        """
        pass


class FAQWindow:
    """FAQ 화면"""
    
    def __init__(self, root):
        """
        FAQ 화면 초기화
        :param root: Tkinter 루트 윈도우
        """
        self.root = root
        self.faq_manager = None
        
    def setup_ui(self):
        """
        FAQ 화면 UI 구성 (FR-07)
        - 카테고리 필터
        - 검색 바
        - FAQ 목록
        """
        pass
    
    def display_faq_list(self, faqs: list):
        """
        FAQ 목록 표시
        :param faqs: FAQ 리스트
        """
        pass
    
    def on_faq_click(self, faq_id: int):
        """
        FAQ 클릭 이벤트 처리
        :param faq_id: 클릭한 FAQ ID
        """
        pass
    
    def on_search(self):
        """
        FAQ 검색 실행
        """
        pass


class InquiryWindow:
    """1:1 문의 화면"""
    
    def __init__(self, root, user):
        """
        1:1 문의 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.user = user
        self.inquiry_manager = None
        
    def setup_ui(self):
        """
        1:1 문의 화면 UI 구성 (FR-07)
        - 문의 제목 입력
        - 문의 내용 입력
        - 제출 버튼
        - 내 문의 목록
        """
        pass
    
    def display_my_inquiries(self, inquiries: list):
        """
        내 문의 목록 표시
        :param inquiries: 문의 리스트
        """
        pass
    
    def on_submit_click(self):
        """
        문의 제출 버튼 클릭 이벤트 처리
        """
        pass
    
    def on_inquiry_click(self, inquiry_id: int):
        """
        문의 클릭 이벤트 처리 (답변 확인)
        :param inquiry_id: 클릭한 문의 ID
        """
        pass


class AdminPanel:
    """관리자 패널"""
    
    def __init__(self, root, admin_user):
        """
        관리자 패널 초기화
        :param root: Tkinter 루트 윈도우
        :param admin_user: 관리자 User 객체
        """
        self.root = root
        self.admin_user = admin_user
        
    def setup_ui(self):
        """
        관리자 패널 UI 구성 (FR-11: 역할/권한 관리)
        - 공고 관리 탭
        - 지원서 관리 탭
        - 사용자 관리 탭
        - 통계 탭
        """
        pass
    
    def setup_job_management_tab(self):
        """
        공고 관리 탭 구성
        - 공고 등록/수정/삭제
        """
        pass
    
    def setup_application_management_tab(self):
        """
        지원서 관리 탭 구성
        - 지원서 목록 조회
        - 상태 변경
        """
        pass
    
    def setup_user_management_tab(self):
        """
        사용자 관리 탭 구성
        - 사용자 목록
        - 권한 변경
        """
        pass
    
    def setup_statistics_tab(self):
        """
        통계 탭 구성
        - 공고별 지원자 수
        - 인기 공고
        - 사용자 활동 통계
        """
        pass


class SettingsWindow:
    """설정 화면"""
    
    def __init__(self, root, user):
        """
        설정 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user: 로그인한 User 객체
        """
        self.root = root
        self.user = user
        
    def setup_ui(self):
        """
        설정 화면 UI 구성 (UX-01: 다크모드, 글자 크기)
        - 다크모드 토글
        - 글자 크기 조절
        - 알림 설정
        - 개인정보 관리
        """
        pass
    
    def on_dark_mode_toggle(self):
        """
        다크모드 토글 이벤트 처리
        """
        pass
    
    def on_font_size_change(self, size: int):
        """
        글자 크기 변경 이벤트 처리
        :param size: 새로운 글자 크기
        """
        pass
    
    def on_delete_account_click(self):
        """
        회원 탈퇴 버튼 클릭 이벤트 처리 (SEC-02: 3단계 이내, 7일 이내 파기)
        """
        pass
