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
        self.student_id_entry = None

        # UI 구성
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        """
        로그인 화면 UI 구성
        - 학번 입력 필드
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

        # 안내 문구
        info_label = tk.Label(
            self.frame,
            text="개발/테스트 버전 - 학번으로 로그인하세요",
            font=("맑은 고딕", 10),
            fg="gray"
        )
        info_label.pack(pady=5)

        # 입력 프레임
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=20)

        # 학번
        tk.Label(input_frame, text="학번:", font=("맑은 고딕", 12)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.student_id_entry = tk.Entry(input_frame, font=("맑은 고딕", 12), width=30)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(input_frame, text="(관리자: 0000000000)", font=("맑은 고딕", 9), fg="gray").grid(row=0, column=2, sticky=tk.W)

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
        self.student_id_entry.bind('<Return>', lambda e: self.on_login_click())

    def on_login_click(self):
        """
        로그인 버튼 클릭 이벤트 처리
        (개발/테스트 버전 - 학번으로만 로그인)
        """
        if not self.validate_input():
            return

        student_id = self.student_id_entry.get().strip()

        # 학번으로 로그인 시도 (비밀번호 없음)
        user = self.user_manager.login(student_id, "")

        if user:
            messagebox.showinfo("로그인 성공", f"환영합니다, {user.username}님!")
            self.on_login_success(user)
        else:
            messagebox.showerror("로그인 실패", "존재하지 않는 학번입니다.\n회원가입을 먼저 진행해주세요.")

    def on_register_click(self):
        """
        회원가입 버튼 클릭 이벤트 처리
        """
        # 회원가입 창 열기
        RegisterWindow(self.root, self.user_manager, on_register_success=None)

    def validate_input(self) -> bool:
        """
        입력 값 유효성 검사
        :return: 유효성 여부
        """
        student_id = self.student_id_entry.get().strip()

        if not student_id:
            messagebox.showwarning("입력 오류", "학번을 입력해주세요.")
            return False

        return True

    def destroy(self):
        """프레임 제거"""
        self.frame.destroy()


class RegisterWindow:
    """회원가입 화면"""

    def __init__(self, root, user_manager, on_register_success):
        """
        회원가입 화면 초기화
        :param root: Tkinter 루트 윈도우
        :param user_manager: UserManager 인스턴스
        :param on_register_success: 회원가입 성공 콜백 함수
        """
        self.root = root
        self.user_manager = user_manager
        self.on_register_success = on_register_success

        # 입력 필드
        self.student_id_entry = None
        self.username_entry = None
        self.department_var = None
        self.email_entry = None

        # 회원가입 창 생성
        self.window = tk.Toplevel(root)
        self.window.title("회원가입")
        self.window.geometry("500x500")
        self.setup_ui()

    def setup_ui(self):
        """
        회원가입 화면 UI 구성
        """
        # 제목
        title_label = tk.Label(
            self.window,
            text="회원가입",
            font=("맑은 고딕", 20, "bold")
        )
        title_label.pack(pady=30)

        # 입력 프레임
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=20)

        # 학번
        tk.Label(input_frame, text="학번:", font=("맑은 고딕", 12)).grid(row=0, column=0, sticky=tk.W, pady=15, padx=10)
        self.student_id_entry = tk.Entry(input_frame, font=("맑은 고딕", 12), width=30)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=15)
        tk.Label(input_frame, text="(10자리 숫자)", font=("맑은 고딕", 9), fg="gray").grid(row=0, column=2, sticky=tk.W)

        # 이름
        tk.Label(input_frame, text="이름:", font=("맑은 고딕", 12)).grid(row=1, column=0, sticky=tk.W, pady=15, padx=10)
        self.username_entry = tk.Entry(input_frame, font=("맑은 고딕", 12), width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=15)

        # 학과
        tk.Label(input_frame, text="학과:", font=("맑은 고딕", 12)).grid(row=2, column=0, sticky=tk.W, pady=15, padx=10)
        self.department_var = tk.StringVar(value="컴퓨터공학")
        department_menu = ttk.Combobox(
            input_frame,
            textvariable=self.department_var,
            values=["컴퓨터공학", "디자인공학", "건축공학"],
            font=("맑은 고딕", 12),
            width=28,
            state="readonly"
        )
        department_menu.grid(row=2, column=1, padx=10, pady=15)

        # 이메일 (비활성화)
        tk.Label(input_frame, text="이메일:", font=("맑은 고딕", 12)).grid(row=3, column=0, sticky=tk.W, pady=15, padx=10)
        self.email_entry = tk.Entry(input_frame, font=("맑은 고딕", 12), width=30, state="disabled")
        self.email_entry.grid(row=3, column=1, padx=10, pady=15)
        tk.Label(input_frame, text="(개발 버전에서는 미지원)", font=("맑은 고딕", 9), fg="gray").grid(row=3, column=2, sticky=tk.W)

        # 버튼 프레임
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=30)

        # 가입 버튼
        register_btn = tk.Button(
            button_frame,
            text="가입하기",
            font=("맑은 고딕", 12),
            width=15,
            command=self.on_register_click
        )
        register_btn.pack(side=tk.LEFT, padx=10)

        # 취소 버튼
        cancel_btn = tk.Button(
            button_frame,
            text="취소",
            font=("맑은 고딕", 12),
            width=15,
            command=self.window.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def on_register_click(self):
        """
        가입하기 버튼 클릭 이벤트 처리
        """
        if not self.validate_input():
            return

        student_id = self.student_id_entry.get().strip()
        username = self.username_entry.get().strip()
        department = self.department_var.get()

        # 회원가입 데이터 준비
        user_data = {
            'student_id': student_id,
            'username': username,
            'department': department,
            'role': 'student'
        }

        # 회원가입 시도
        user_id = self.user_manager.register(user_data)

        if user_id:
            messagebox.showinfo("가입 성공", f"회원가입이 완료되었습니다!\n학번: {student_id}로 로그인해주세요.")
            self.window.destroy()
            if self.on_register_success:
                self.on_register_success()
        else:
            messagebox.showerror("가입 실패", "이미 존재하는 학번이거나 가입에 실패했습니다.")

    def validate_input(self) -> bool:
        """
        입력 값 유효성 검사
        :return: 유효성 여부
        """
        student_id = self.student_id_entry.get().strip()
        username = self.username_entry.get().strip()

        if not student_id:
            messagebox.showwarning("입력 오류", "학번을 입력해주세요.")
            return False

        if len(student_id) != 10 or not student_id.isdigit():
            messagebox.showwarning("입력 오류", "학번은 10자리 숫자여야 합니다.")
            return False

        if not username:
            messagebox.showwarning("입력 오류", "이름을 입력해주세요.")
            return False

        return True


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

    def __init__(self, root, job_id, user):
        self.root = root
        self.job_id = job_id
        self.user = user
        self.job_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("공고 상세")
        self.frame.geometry("600x500")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="공고 상세 정보", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        info_frame = tk.Frame(self.frame)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(info_frame, text="공고 ID: " + str(self.job_id), font=("맑은 고딕", 12)).pack(pady=5)

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="지원하기", command=self.on_apply_click, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="북마크", command=self.on_bookmark_click, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="닫기", command=self.frame.destroy, width=15).pack(side=tk.LEFT, padx=10)

    def load_job_details(self):
        pass

    def on_apply_click(self):
        messagebox.showinfo("지원하기", "지원서 작성 화면으로 이동합니다.")

    def on_bookmark_click(self):
        messagebox.showinfo("북마크", "북마크에 추가되었습니다.")

    def check_time_conflict(self):
        return False


class ApplicationWindow:
    """지원서 작성 화면"""

    def __init__(self, root, job_id, user):
        self.root = root
        self.job_id = job_id
        self.user = user
        self.application_manager = None
        self.resume_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("지원서 작성")
        self.frame.geometry("600x500")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="지원서 작성", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="이력서 선택:", font=("맑은 고딕", 12)).grid(row=0, column=0, sticky=tk.W, pady=10)
        tk.Button(form_frame, text="이력서 불러오기", command=self.load_user_resumes).grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="자기소개서:", font=("맑은 고딕", 12)).grid(row=1, column=0, sticky=tk.NW, pady=10)
        self.cover_letter = tk.Text(form_frame, height=10, width=40)
        self.cover_letter.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.frame, text="제출", command=self.on_submit_click, width=15).pack(pady=20)

    def load_user_resumes(self):
        messagebox.showinfo("이력서", "이력서 목록을 불러옵니다.")

    def on_resume_select(self, resume_id):
        pass

    def on_submit_click(self):
        if self.validate_form():
            messagebox.showinfo("제출 완료", "지원서가 제출되었습니다.")
            self.frame.destroy()

    def auto_save(self):
        pass

    def validate_form(self):
        return True


class MyPageWindow:
    """마이페이지 화면"""

    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.frame = tk.Toplevel(root)
        self.frame.title("마이페이지")
        self.frame.geometry("800x600")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="마이페이지", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        resume_tab = tk.Frame(notebook)
        application_tab = tk.Frame(notebook)
        bookmark_tab = tk.Frame(notebook)
        history_tab = tk.Frame(notebook)

        notebook.add(resume_tab, text="이력서 관리")
        notebook.add(application_tab, text="지원현황")
        notebook.add(bookmark_tab, text="스크랩")
        notebook.add(history_tab, text="최근 본 알바")

    def setup_resume_tab(self):
        pass

    def setup_application_tab(self):
        pass

    def setup_bookmark_tab(self):
        pass

    def setup_history_tab(self):
        pass


class ApplicationStatusWindow:
    """지원현황 화면"""

    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.application_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("지원현황")
        self.frame.geometry("700x500")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="지원현황", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        self.listbox = tk.Listbox(self.frame, font=("맑은 고딕", 10), height=15)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.listbox.bind('<Double-Button-1>', lambda e: self.on_application_click())

    def display_application_list(self, applications):
        self.listbox.delete(0, tk.END)
        for app in applications:
            self.listbox.insert(tk.END, f"공고 {app.job_id} - 상태: {app.status}")

    def display_timeline(self, application_id):
        messagebox.showinfo("타임라인", f"지원서 {application_id}의 타임라인을 표시합니다.")

    def on_application_click(self):
        selection = self.listbox.curselection()
        if selection:
            self.display_timeline(selection[0])


class ResumeEditorWindow:
    """이력서 편집 화면"""

    def __init__(self, root, user, resume_id=None):
        self.root = root
        self.user = user
        self.resume_id = resume_id
        self.resume_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("이력서 편집")
        self.frame.geometry("600x600")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="이력서 편집", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        fields = [
            ("제목:", "title"),
            ("학력:", "education"),
            ("경력:", "experience"),
            ("자격증:", "certifications")
        ]

        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("맑은 고딕", 11)).grid(row=i, column=0, sticky=tk.W, pady=10)
            entry = tk.Entry(form_frame, font=("맑은 고딕", 11), width=30)
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[key] = entry

        tk.Label(form_frame, text="자기소개:", font=("맑은 고딕", 11)).grid(row=len(fields), column=0, sticky=tk.NW, pady=10)
        self.intro_text = tk.Text(form_frame, height=5, width=30)
        self.intro_text.grid(row=len(fields), column=1, padx=10, pady=10)

        tk.Button(self.frame, text="저장", command=self.on_save_click, width=15).pack(pady=20)

    def load_resume_data(self):
        pass

    def on_save_click(self):
        if self.validate_form():
            messagebox.showinfo("저장 완료", "이력서가 저장되었습니다.")
            self.frame.destroy()

    def validate_form(self):
        return True


class TimetableWindow:
    """시간표 관리 화면"""

    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.timetable_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("시간표 관리")
        self.frame.geometry("700x600")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="시간표 관리", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        canvas = tk.Canvas(self.frame, width=650, height=400, bg="white")
        canvas.pack(pady=10)

        # 간단한 시간표 그리드 그리기
        for i in range(6):  # 요일
            for j in range(10):  # 시간
                x1, y1 = 50 + i*100, 50 + j*35
                x2, y2 = x1 + 100, y1 + 35
                canvas.create_rectangle(x1, y1, x2, y2)

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="가져오기", command=self.on_import_click, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="저장", command=self.on_save_click, width=15).pack(side=tk.LEFT, padx=10)

    def display_timetable(self, timetable_data):
        pass

    def on_import_click(self):
        messagebox.showinfo("가져오기", "시간표를 가져옵니다.")

    def on_save_click(self):
        messagebox.showinfo("저장", "시간표가 저장되었습니다.")


class NotificationPanel:
    """알림 패널"""

    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.notification_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("알림")
        self.frame.geometry("400x500")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="알림", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        self.listbox = tk.Listbox(self.frame, font=("맑은 고딕", 10), height=20)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.listbox.bind('<Double-Button-1>', lambda e: self.on_notification_click())

    def load_notifications(self):
        pass

    def display_notifications(self, notifications):
        self.listbox.delete(0, tk.END)
        for notif in notifications:
            self.listbox.insert(tk.END, notif.message)

    def on_notification_click(self):
        messagebox.showinfo("알림 상세", "알림 내용을 표시합니다.")

    def mark_as_read(self, notification_id):
        pass


class RecommendationPanel:
    """추천 공고 패널"""

    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.recommendation_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("추천 공고")
        self.frame.geometry("600x500")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="AI 추천 공고", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        self.listbox = tk.Listbox(self.frame, font=("맑은 고딕", 10), height=15)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Button(self.frame, text="새로고침", command=self.load_recommendations, width=15).pack(pady=10)

    def load_recommendations(self):
        messagebox.showinfo("추천", "AI 추천 공고를 불러옵니다.")

    def display_recommendations(self, jobs):
        self.listbox.delete(0, tk.END)
        for job in jobs:
            self.listbox.insert(tk.END, f"{job.title} - 매칭도: 높음")


class FAQWindow:
    """FAQ 화면"""

    def __init__(self, root):
        self.root = root
        self.faq_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("FAQ")
        self.frame.geometry("600x500")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="자주 묻는 질문", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        # 카테고리 선택
        category_frame = tk.Frame(self.frame)
        category_frame.pack(pady=10)

        tk.Label(category_frame, text="카테고리:", font=("맑은 고딕", 11)).pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar(value="전체")
        category_menu = ttk.Combobox(category_frame, textvariable=self.category_var,
                                     values=["전체", "지원", "급여", "근무", "기타"])
        category_menu.pack(side=tk.LEFT, padx=5)
        category_menu.bind('<<ComboboxSelected>>', lambda e: self.on_category_change())

        # FAQ 목록
        self.faq_listbox = tk.Listbox(self.frame, font=("맑은 고딕", 10), height=15)
        self.faq_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.faq_listbox.bind('<Double-Button-1>', lambda e: self.on_faq_click())

    def load_faqs(self):
        pass

    def on_category_change(self):
        messagebox.showinfo("카테고리", f"{self.category_var.get()} FAQ를 불러옵니다.")

    def on_faq_click(self):
        selection = self.faq_listbox.curselection()
        if selection:
            messagebox.showinfo("FAQ 상세", "FAQ 내용을 표시합니다.")

    def search_faq(self, keyword):
        pass


class InquiryWindow:
    """1:1 문의 화면"""

    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.inquiry_manager = None

        self.frame = tk.Toplevel(root)
        self.frame.title("1:1 문의")
        self.frame.geometry("600x500")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="1:1 문의", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="제목:", font=("맑은 고딕", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.title_entry = tk.Entry(form_frame, font=("맑은 고딕", 11), width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="내용:", font=("맑은 고딕", 11)).grid(row=1, column=0, sticky=tk.NW, pady=10)
        self.content_text = tk.Text(form_frame, height=10, width=40)
        self.content_text.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="제출", command=self.on_submit_click, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="내 문의 목록", command=self.view_my_inquiries, width=15).pack(side=tk.LEFT, padx=10)

    def on_submit_click(self):
        if self.validate_form():
            messagebox.showinfo("제출 완료", "문의가 제출되었습니다.")
            self.frame.destroy()

    def validate_form(self):
        if not self.title_entry.get().strip():
            messagebox.showwarning("입력 오류", "제목을 입력해주세요.")
            return False
        if not self.content_text.get("1.0", tk.END).strip():
            messagebox.showwarning("입력 오류", "내용을 입력해주세요.")
            return False
        return True

    def view_my_inquiries(self):
        messagebox.showinfo("내 문의", "내 문의 목록을 표시합니다.")

    def display_inquiry_list(self, inquiries):
        pass


class AdminPanel:
    """관리자 패널"""

    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.frame = tk.Toplevel(root)
        self.frame.title("관리자 패널")
        self.frame.geometry("800x600")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="관리자 패널", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        job_tab = tk.Frame(notebook)
        application_tab = tk.Frame(notebook)
        user_tab = tk.Frame(notebook)
        inquiry_tab = tk.Frame(notebook)

        notebook.add(job_tab, text="공고 관리")
        notebook.add(application_tab, text="지원서 관리")
        notebook.add(user_tab, text="사용자 관리")
        notebook.add(inquiry_tab, text="문의 관리")

    def setup_job_management(self):
        pass

    def setup_application_management(self):
        pass

    def setup_user_management(self):
        pass

    def setup_inquiry_management(self):
        pass

    def view_statistics(self):
        pass


class SettingsWindow:
    """설정 화면"""

    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.frame = tk.Toplevel(root)
        self.frame.title("설정")
        self.frame.geometry("500x400")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="설정", font=("맑은 고딕", 16, "bold")).pack(pady=20)

        settings_frame = tk.Frame(self.frame)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 다크모드 설정
        self.dark_mode_var = tk.BooleanVar()
        tk.Checkbutton(
            settings_frame,
            text="다크모드",
            variable=self.dark_mode_var,
            command=self.on_dark_mode_toggle,
            font=("맑은 고딕", 11)
        ).pack(anchor=tk.W, pady=10)

        # 알림 설정
        self.notification_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            settings_frame,
            text="알림 받기",
            variable=self.notification_var,
            command=self.on_notification_toggle,
            font=("맑은 고딕", 11)
        ).pack(anchor=tk.W, pady=10)

        tk.Button(self.frame, text="저장", command=self.on_save_click, width=15).pack(pady=20)

    def on_dark_mode_toggle(self):
        if self.dark_mode_var.get():
            messagebox.showinfo("다크모드", "다크모드가 활성화되었습니다.")
        else:
            messagebox.showinfo("다크모드", "다크모드가 비활성화되었습니다.")

    def on_notification_toggle(self):
        pass

    def on_save_click(self):
        messagebox.showinfo("저장", "설정이 저장되었습니다.")
        self.frame.destroy()
