# gui_modules.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from typing import List

from entities import Job, User
from managers import (
    UserManager,
    JobManager,
    ResumeManager,
    ApplicationManager,
    BookmarkManager,
    ViewHistoryManager,
    TimetableManager,
    FAQManager,
    InquiryManager,
)


# ==========================
# 로그인 창
# ==========================
class LoginWindow:
    """로그인 / 회원가입 화면"""

    def __init__(self, root: tk.Tk, user_manager: UserManager, on_login_success):
        self.root = root
        self.user_manager = user_manager
        self.on_login_success = on_login_success

        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill="both", expand=True)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        # 상단 로고
        logo_frame = tk.Frame(self.frame, bg="white")
        logo_frame.pack(fill="x", pady=40)

        tk.Label(
            logo_frame,
            text="한기 WORKS",
            bg="white",
            fg="black",
            font=("맑은 고딕", 24, "bold"),
        ).pack()

        # 입력 폼 카드
        form_card = tk.Frame(self.frame, bg="#F5F5F7", bd=1, relief="solid")
        form_card.pack(pady=10, padx=40)

        inner = tk.Frame(form_card, bg="#F5F5F7")
        inner.pack(padx=20, pady=20)

        tk.Label(inner, text="아이디", bg="#F5F5F7").grid(
            row=0, column=0, sticky="w", pady=5
        )
        tk.Entry(inner, textvariable=self.username_var, width=30).grid(
            row=1, column=0, pady=5
        )

        tk.Label(inner, text="비밀번호", bg="#F5F5F7").grid(
            row=2, column=0, sticky="w", pady=(15, 5)
        )
        tk.Entry(inner, textvariable=self.password_var, show="*", width=30).grid(
            row=3, column=0, pady=5
        )

        btn_frame = tk.Frame(inner, bg="#F5F5F7")
        btn_frame.grid(row=4, column=0, pady=(20, 0))

        tk.Button(
            btn_frame,
            text="로그인",
            width=12,
            command=self.on_login_click,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="회원가입",
            width=12,
            command=self.on_register_click,
        ).pack(side="left", padx=5)

    def on_login_click(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        user = self.user_manager.login(username, password)
        if user:
            messagebox.showinfo("로그인 성공", f"{username}님 환영합니다.")
            self.frame.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 올바르지 않습니다.")

    def on_register_click(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("입력 오류", "아이디와 비밀번호를 모두 입력하세요.")
            return

        user = self.user_manager.register(username, password)
        if user:
            messagebox.showinfo("회원가입 완료", "회원가입이 완료되었습니다. 다시 로그인해 주세요.")
        else:
            messagebox.showerror("회원가입 실패", "이미 존재하는 아이디입니다.")


# ==========================
# 메인 화면
# ==========================
class MainWindow:
    """메인 화면 - 한기 WORKS 스타일"""

    def __init__(
        self,
        root: tk.Tk,
        current_user: User,
        user_manager: UserManager,
        job_manager: JobManager,
        resume_manager: ResumeManager,
        application_manager: ApplicationManager,
        bookmark_manager: BookmarkManager,
        view_history_manager: ViewHistoryManager,
        timetable_manager: TimetableManager,
        faq_manager: FAQManager,
        inquiry_manager: InquiryManager,
    ):
        self.root = root
        self.current_user = current_user
        self.user_manager = user_manager
        self.job_manager = job_manager
        self.resume_manager = resume_manager
        self.application_manager = application_manager
        self.bookmark_manager = bookmark_manager
        self.view_history_manager = view_history_manager
        self.timetable_manager = timetable_manager
        self.faq_manager = faq_manager
        self.inquiry_manager = inquiry_manager

        self.jobs: List[Job] = []
        self.current_filter = "전체"

        self.search_var = tk.StringVar()

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        self._build_ui()
        self.load_jobs()

    # ---------- UI ----------
    def _build_ui(self):
        # 상단 헤더
        header = tk.Frame(self.main_frame, bg="white", height=60)
        header.pack(fill="x", side="top")

        tk.Label(
            header,
            text="한기 WORKS",
            bg="white",
            fg="black",
            font=("맑은 고딕", 20, "bold"),
        ).pack(side="left", padx=20, pady=10)

        tk.Button(
            header,
            text="❓FAQ",
            bg="white",
            bd=0,
            font=("맑은 고딕", 10),
            command=self.open_faq_window,
        ).pack(side="right", padx=5)

        tk.Button(
            header,
            text="🔍",
            bg="white",
            bd=0,
            font=("맑은 고딕", 14),
            command=self.on_search_click,
        ).pack(side="right", padx=5)

        tk.Label(
            header,
            text=f"{self.current_user.username}님",
            bg="white",
            fg="#555",
            font=("맑은 고딕", 10),
        ).pack(side="right", padx=10)

        # 검색줄
        search_frame = tk.Frame(self.main_frame, bg="white")
        search_frame.pack(fill="x", padx=20, pady=5)

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            relief="groove",
        ).pack(side="left", padx=(0, 5))
        tk.Button(
            search_frame,
            text="검색",
            width=8,
            command=self.on_search_click,
        ).pack(side="left", padx=5)
        tk.Button(
            search_frame,
            text="전체보기",
            width=8,
            command=self.load_jobs,
        ).pack(side="left", padx=5)

        # 상단 배너
        banner = tk.Frame(self.main_frame, bg="#F5F5F7", height=120)
        banner.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(
            banner,
            text="캠퍼스 근로장학 공고를 한 번에!",
            bg="#F5F5F7",
            font=("맑은 고딕", 12, "bold"),
        ).pack(anchor="w", padx=20, pady=(15, 0))
        tk.Label(
            banner,
            text="장기·단기·일일 알바를 한기 WORKS에서 확인해 보세요.",
            bg="#F5F5F7",
            font=("맑은 고딕", 10),
            fg="#444",
        ).pack(anchor="w", padx=20, pady=(5, 0))

        # 필터 탭
        tab_frame = tk.Frame(self.main_frame, bg="white")
        tab_frame.pack(fill="x", padx=20, pady=10)

        self.tab_buttons = {}
        for i, (name, key) in enumerate(
            [("장소별", "장소별"), ("장기", "장기"), ("단기", "단기"), ("일일", "일일")]
        ):
            btn = tk.Button(
                tab_frame,
                text=name,
                width=10,
                relief="solid",
                bd=1,
                command=lambda k=key: self.on_tab_click(k),
            )
            btn.grid(row=0, column=i, padx=5)
            self.tab_buttons[key] = btn

        self._update_tab_style()

        # 중앙 영역
        center = tk.Frame(self.main_frame, bg="white")
        center.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # 왼쪽 공고 리스트
        list_frame = tk.Frame(center, bg="white")
        list_frame.pack(side="left", fill="both", expand=True)

        self.job_listbox = tk.Listbox(list_frame, activestyle="none")
        self.job_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=self.job_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.job_listbox.config(yscrollcommand=scrollbar.set)

        self.job_listbox.bind("<<ListboxSelect>>", self.on_job_select)

        # 오른쪽 상세 카드
        detail_frame = tk.Frame(center, bg="white")
        detail_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.detail_card = tk.Frame(detail_frame, bg="#F5F5F7", bd=1, relief="solid")
        self.detail_card.pack(fill="both", expand=True)

        self.detail_title = tk.Label(
            self.detail_card,
            text="공고를 선택하면 상세 정보가 표시됩니다.",
            bg="#F5F5F7",
            font=("맑은 고딕", 12, "bold"),
            justify="left",
            wraplength=300,
        )
        self.detail_title.pack(anchor="w", padx=15, pady=(15, 5))

        self.detail_body = tk.Label(
            self.detail_card,
            text="",
            bg="#F5F5F7",
            font=("맑은 고딕", 10),
            justify="left",
            wraplength=320,
        )
        self.detail_body.pack(anchor="w", padx=15, pady=(0, 10))

        # 아래 버튼들
        btn_frame = tk.Frame(self.main_frame, bg="white")
        btn_frame.pack(fill="x", padx=20, pady=(0, 5))

        tk.Button(
            btn_frame, text="공고 등록", width=12, command=self.on_add_job_click
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame, text="공고 삭제", width=12, command=self.on_delete_job_click
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="통합 이력서 등록",
            width=15,
            command=self.on_resume_register_click,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame,
            text="선택 공고 지원",
            width=15,
            command=self.on_apply_click,
        ).pack(side="left", padx=5)

        # 하단 탭바
        bottom = tk.Frame(self.main_frame, bg="#F5F5F7", height=50)
        bottom.pack(fill="x", side="bottom")

        def open_mypage():
            MyPageWindow(
                self.root,
                self.current_user,
                self.resume_manager,
                self.application_manager,
                self.bookmark_manager,
                self.view_history_manager,
                self.timetable_manager,
                self.faq_manager,
                self.inquiry_manager,
            )

        for name in ["홈", "시작한", "학교지도", "채팅", "마이페이지"]:
            if name == "마이페이지":
                tk.Button(
                    bottom,
                    text=name,
                    bg="#F5F5F7",
                    bd=0,
                    font=("맑은 고딕", 9),
                    command=open_mypage,
                ).pack(side="left", expand=True)
            else:
                tk.Button(
                    bottom,
                    text=name,
                    bg="#F5F5F7",
                    bd=0,
                    font=("맑은 고딕", 9),
                    command=lambda n=name: messagebox.showinfo(
                        "안내", f"'{n}' 기능은 데모입니다."
                    ),
                ).pack(side="left", expand=True)

    # ---------- 탭 / 필터 ----------
    def on_tab_click(self, key: str):
        self.current_filter = key
        self._update_tab_style()
        self.apply_filter()

    def _update_tab_style(self):
        for key, btn in self.tab_buttons.items():
            if key == self.current_filter:
                btn.config(bg="black", fg="white")
            else:
                btn.config(bg="white", fg="black")

    def apply_filter(self):
        if self.current_filter in ("장소별", "전체"):
            self.load_jobs()
            return

        all_jobs = self.job_manager.get_all_jobs()
        self.jobs = [
            j for j in all_jobs if (j.category or "") == self.current_filter
        ]
        self.refresh_job_listbox()

    # ---------- 데이터 ----------
    def load_jobs(self):
        self.jobs = self.job_manager.get_all_jobs()
        self.refresh_job_listbox()

    def refresh_job_listbox(self):
        self.job_listbox.delete(0, tk.END)
        for job in self.jobs:
            title = job.title or "(제목 없음)"
            self.job_listbox.insert(tk.END, f"[{job.job_id}] {title}")
        self.detail_title.config(text="공고를 선택하면 상세 정보가 표시됩니다.")
        self.detail_body.config(text="")

    def get_selected_job(self) -> Job:
        sel = self.job_listbox.curselection()
        if not sel:
            return None
        idx = sel[0]
        if idx < 0 or idx >= len(self.jobs):
            return None
        return self.jobs[idx]

    # ---------- 이벤트 ----------
    def on_job_select(self, event=None):
        job = self.get_selected_job()
        if not job:
            return

        # 열람 이력 기록
        self.view_history_manager.record_view(self.current_user.user_id, job.job_id)

        title_line = f"[{job.job_id}] {job.title or '(제목 없음)'}"
        self.detail_title.config(text=title_line)

        lines = []
        if job.location:
            lines.append(f"📍 근무 위치: {job.location}")
        if job.category:
            lines.append(f"📂 카테고리: {job.category}")
        if job.job_type:
            lines.append(f"🧰 근로 형태: {job.job_type}")
        if job.work_hours:
            lines.append(f"⏰ 근무 시간: {job.work_hours}")
        if job.salary is not None:
            lines.append(f"💰 시급: {job.salary}원")
        if job.department:
            lines.append(f"🏢 부서: {job.department}")
        if job.max_applicants:
            lines.append(f"👥 모집 인원: {job.max_applicants}명")
        if job.deadline:
            try:
                d = job.deadline.strftime("%Y-%m-%d")
            except Exception:
                d = str(job.deadline)
            lines.append(f"📅 마감일: {d}")

        if job.description:
            lines.append("")
            lines.append("상세 내용")
            lines.append(job.description)

        if job.requirements:
            lines.append("")
            lines.append("요구 조건")
            lines.append(job.requirements)

        self.detail_body.config(text="\n".join(lines))

    def on_search_click(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            self.load_jobs()
            return
        self.jobs = self.job_manager.search_jobs(keyword)
        self.refresh_job_listbox()

    # ---------- 공고 등록 ----------
    def on_add_job_click(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("공고 등록")
        dialog.geometry("470x680")

        title_var = tk.StringVar()
        category_var = tk.StringVar()
        location_var = tk.StringVar()
        job_type_var = tk.StringVar()
        work_hours_var = tk.StringVar()
        salary_var = tk.StringVar()
        deadline_var = tk.StringVar()
        department_var = tk.StringVar()
        max_app_var = tk.StringVar()

        def add_row(label, var, row):
            tk.Label(dialog, text=label).grid(
                row=row, column=0, padx=5, pady=5, sticky="e"
            )
            tk.Entry(dialog, textvariable=var, width=30).grid(
                row=row, column=1, padx=5, pady=5
            )

        add_row("제목:", title_var, 0)
        add_row("카테고리(장기/단기/일일):", category_var, 1)
        add_row("근무 위치:", location_var, 2)
        add_row("근로 형태:", job_type_var, 3)
        add_row("근무 시간:", work_hours_var, 4)
        add_row("시급:", salary_var, 5)
        add_row("마감일(YYYY-MM-DD):", deadline_var, 6)
        add_row("부서:", department_var, 7)
        add_row("최대 모집 인원:", max_app_var, 8)

        tk.Label(dialog, text="설명:").grid(row=9, column=0, sticky="ne", padx=5, pady=5)
        desc_text = scrolledtext.ScrolledText(dialog, width=30, height=4)
        desc_text.grid(row=9, column=1, padx=5, pady=5)

        tk.Label(dialog, text="요구 조건:").grid(
            row=10, column=0, sticky="ne", padx=5, pady=5
        )
        req_text = scrolledtext.ScrolledText(dialog, width=30, height=4)
        req_text.grid(row=10, column=1, padx=5, pady=5)

        def on_save():
            title = title_var.get().strip()
            if not title:
                messagebox.showwarning("입력 오류", "제목은 필수입니다.")
                return

            from datetime import datetime as dt

            dl_str = deadline_var.get().strip()
            if dl_str:
                try:
                    deadline = dt.fromisoformat(dl_str)
                except Exception:
                    messagebox.showerror("오류", "마감일 형식이 잘못되었습니다. 예) 2025-03-01")
                    return
            else:
                deadline = None

            try:
                salary = int(salary_var.get()) if salary_var.get().strip() else 0
            except ValueError:
                messagebox.showerror("오류", "시급은 숫자로 입력해주세요.")
                return

            try:
                max_app = (
                    int(max_app_var.get()) if max_app_var.get().strip() else None
                )
            except ValueError:
                messagebox.showerror("오류", "최대 모집 인원은 숫자로 입력해주세요.")
                return

            now = dt.now()

            job = Job(
                title=title,
                description=desc_text.get("1.0", tk.END).strip(),
                category=category_var.get().strip(),
                location=location_var.get().strip(),
                job_type=job_type_var.get().strip(),
                work_hours=work_hours_var.get().strip(),
                salary=salary,
                requirements=req_text.get("1.0", tk.END).strip(),
                deadline=deadline,
                created_at=now,
                department=department_var.get().strip(),
                max_applicants=max_app,
            )

            job_id = self.job_manager.job_dao.insert_job(job)
            if job_id:
                messagebox.showinfo("등록 완료", "공고가 성공적으로 등록되었습니다.")
                dialog.destroy()
                self.load_jobs()
            else:
                messagebox.showerror("오류", "공고 등록 실패.")

        tk.Button(dialog, text="저장", width=15, command=on_save).grid(
            row=11, column=0, columnspan=2, pady=15
        )

    # ---------- 공고 삭제 ----------
    def on_delete_job_click(self):
        job = self.get_selected_job()
        if not job:
            messagebox.showwarning("선택 오류", "삭제할 공고를 선택하세요.")
            return

        if messagebox.askyesno("삭제 확인", f"[{job.job_id}] {job.title} 공고를 삭제할까요?"):
            ok = self.job_manager.delete_job(job.job_id)
            if ok:
                messagebox.showinfo("삭제 완료", "공고가 삭제되었습니다.")
                self.load_jobs()
            else:
                messagebox.showerror("삭제 실패", "공고 삭제에 실패했습니다.")

    # ---------- 통합 이력서 ----------
    def on_resume_register_click(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("통합 이력서 등록")
        dialog.geometry("470x500")

        tk.Label(dialog, text="이력서 제목:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        title_var = tk.StringVar(value="공통 이력서")
        tk.Entry(dialog, textvariable=title_var, width=35).grid(
            row=0, column=1, padx=5, pady=5
        )

        tk.Label(dialog, text="내용(학력/경력/자기소개 등):").grid(
            row=1, column=0, padx=5, pady=5, sticky="ne"
        )
        content_text = scrolledtext.ScrolledText(dialog, width=35, height=15)
        content_text.grid(row=1, column=1, padx=5, pady=5)

        def on_save():
            title = title_var.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("입력 오류", "내용을 입력하세요.")
                return
            resume = self.resume_manager.register_or_update_common_resume(
                self.current_user.user_id, title, content
            )
            if resume:
                messagebox.showinfo("저장 완료", "통합 이력서가 저장되었습니다.")
                dialog.destroy()
            else:
                messagebox.showerror("저장 실패", "이력서 저장에 실패했습니다.")

        tk.Button(dialog, text="저장", width=12, command=on_save).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    # ---------- 지원 ----------
    def on_apply_click(self):
        job = self.get_selected_job()
        if not job:
            messagebox.showwarning("선택 오류", "지원할 공고를 선택하세요.")
            return

        resume = self.resume_manager.get_default_resume(self.current_user.user_id)
        if not resume:
            messagebox.showwarning(
                "이력서 없음", "먼저 '통합 이력서 등록' 버튼으로 이력서를 등록해주세요."
            )
            return

        app = self.application_manager.apply_to_job(
            self.current_user.user_id, job.job_id, resume.resume_id
        )
        if app:
            messagebox.showinfo(
                "지원 완료",
                f"[{job.job_id}] {job.title} 공고에 통합 이력서로 지원했습니다.",
            )
        else:
            messagebox.showerror("지원 실패", "지원 중 오류가 발생했습니다.")

    # ---------- FAQ ----------
    def open_faq_window(self):
        FAQWindow(self.root, self.faq_manager)

    def validate_form(self):
        return True


# ==========================
# MyPage
# ==========================
class MyPageWindow:
    """마이페이지 화면"""

    def __init__(
        self,
        root: tk.Tk,
        user: User,
        resume_manager: ResumeManager,
        application_manager: ApplicationManager,
        bookmark_manager: BookmarkManager,
        view_history_manager: ViewHistoryManager,
        timetable_manager: TimetableManager,
        faq_manager: FAQManager,
        inquiry_manager: InquiryManager,
    ):
        self.root = root
        self.user = user
        self.resume_manager = resume_manager
        self.application_manager = application_manager
        self.bookmark_manager = bookmark_manager
        self.view_history_manager = view_history_manager
        self.timetable_manager = timetable_manager
        self.faq_manager = faq_manager
        self.inquiry_manager = inquiry_manager

        self.win = tk.Toplevel(self.root)
        self.win.title("MyPage")
        self.win.geometry("700x550")
        self.win.configure(bg="white")

        self._build_ui()

    def _build_ui(self):
        # 헤더
        header = tk.Frame(self.win, bg="white")
        header.pack(fill="x", pady=10)

        tk.Label(
            header,
            text="MyPage",
            bg="white",
            fg="black",
            font=("맑은 고딕", 20, "bold"),
        ).pack(side="left", padx=20)

        tk.Button(
            header,
            text="✕",
            bg="white",
            bd=0,
            font=("맑은 고딕", 16),
            command=self.win.destroy,
        ).pack(side="right", padx=20)

        # 상단 탭
        tab_frame = tk.Frame(self.win, bg="white")
        tab_frame.pack(fill="x", pady=10)

        tk.Button(
            tab_frame,
            text="이력서 관리",
            relief="solid",
            bd=1,
            bg="white",
            width=12,
            command=self.show_resume_tab,
        ).pack(side="left", padx=5)
        tk.Button(
            tab_frame,
            text="지원현황",
            relief="solid",
            bd=1,
            bg="white",
            width=12,
            command=self.show_application_tab,
        ).pack(side="left", padx=5)
        tk.Button(
            tab_frame,
            text="스크랩",
            relief="solid",
            bd=1,
            bg="white",
            width=12,
            command=self.show_bookmark_tab,
        ).pack(side="left", padx=5)
        tk.Button(
            tab_frame,
            text="최근 본 알바",
            relief="solid",
            bd=1,
            bg="white",
            width=12,
            command=self.show_history_tab,
        ).pack(side="left", padx=5)

        # 서브탭 (디자인용)
        sub_frame = tk.Frame(self.win, bg="white")
        sub_frame.pack(fill="x", pady=10)

        for s in ["이력서 열람", "관심 알바", "근로계약서"]:
            tk.Button(
                sub_frame,
                text=s,
                relief="solid",
                bd=1,
                bg="white",
                width=12,
            ).pack(side="left", expand=True, padx=5)

        # 내용 영역
        self.content_frame = tk.Frame(self.win, bg="white")
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # 기본 화면
        self.show_resume_tab()

        # 하단 아이콘
        bottom = tk.Frame(self.win, bg="white")
        bottom.pack(fill="x", pady=10)

        for ic in ["●", "⚫", "🟡", "📘"]:
            tk.Button(
                bottom,
                text=ic,
                bg="white",
                bd=0,
                font=("맑은 고딕", 12),
            ).pack(side="left", padx=10)

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    # --- 탭별 내용 ---
    def show_resume_tab(self):
        self._clear_content()
        card = tk.Frame(self.content_frame, bg="#F7F3EF")
        card.pack(fill="both", expand=True)

        resume = self.resume_manager.get_default_resume(self.user.user_id)

        if resume:
            tk.Label(
                card,
                text=f"통합 이력서 제목: {resume.title}",
                bg="#F7F3EF",
                font=("맑은 고딕", 12, "bold"),
            ).pack(pady=(20, 10))
            text = scrolledtext.ScrolledText(card, width=60, height=15)
            text.pack(padx=20, pady=10)
            text.insert(tk.END, resume.content)
            text.config(state="disabled")
        else:
            tk.Label(
                card,
                text="아직 통합 이력서가 없습니다.",
                bg="#F7F3EF",
                fg="#444",
                font=("맑은 고딕", 12),
            ).pack(pady=40)
        tk.Button(
            card,
            text="통합 이력서 등록/수정",
            command=self._open_resume_editor,
        ).pack(pady=10)

    def _open_resume_editor(self):
        from tkinter import Toplevel

        dialog = Toplevel(self.win)
        dialog.title("통합 이력서 수정")
        dialog.geometry("470x500")

        tk.Label(dialog, text="이력서 제목:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        title_var = tk.StringVar(value="공통 이력서")
        tk.Entry(dialog, textvariable=title_var, width=35).grid(
            row=0, column=1, padx=5, pady=5
        )

        tk.Label(dialog, text="내용:").grid(
            row=1, column=0, padx=5, pady=5, sticky="ne"
        )
        content_text = scrolledtext.ScrolledText(dialog, width=35, height=15)
        content_text.grid(row=1, column=1, padx=5, pady=5)

        existing = self.resume_manager.get_default_resume(self.user.user_id)
        if existing:
            title_var.set(existing.title or "공통 이력서")
            content_text.insert(tk.END, existing.content or "")

        def on_save():
            title = title_var.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("입력 오류", "내용을 입력하세요.")
                return
            self.resume_manager.register_or_update_common_resume(
                self.user.user_id, title, content
            )
            messagebox.showinfo("저장 완료", "통합 이력서가 저장되었습니다.")
            dialog.destroy()
            self.show_resume_tab()

        tk.Button(dialog, text="저장", width=12, command=on_save).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def show_application_tab(self):
        self._clear_content()
        card = tk.Frame(self.content_frame, bg="#F7F3EF")
        card.pack(fill="both", expand=True)

        apps = self.application_manager.get_applications_by_user(self.user.user_id)

        tk.Label(
            card,
            text="지원 현황",
            bg="#F7F3EF",
            font=("맑은 고딕", 12, "bold"),
        ).pack(pady=10)

        if not apps:
            tk.Label(
                card,
                text="아직 지원한 공고가 없습니다.",
                bg="#F7F3EF",
                fg="#444",
            ).pack(pady=40)
            return

        listbox = tk.Listbox(card, width=70)
        listbox.pack(padx=20, pady=10, fill="both", expand=True)

        for a in apps:
            ts = a.submitted_at.strftime("%Y-%m-%d %H:%M") if a.submitted_at else "-"
            listbox.insert(
                tk.END, f"ID {a.application_id} | 공고 {a.job_id} | 상태 {a.status} | {ts}"
            )

    def show_bookmark_tab(self):
        self._clear_content()
        card = tk.Frame(self.content_frame, bg="#F7F3EF")
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="스크랩한 공고",
            bg="#F7F3EF",
            font=("맑은 고딕", 12, "bold"),
        ).pack(pady=10)

        jobs = self.bookmark_manager.get_bookmarked_jobs(self.user.user_id)
        if not jobs:
            tk.Label(
                card,
                text="스크랩한 공고가 없습니다.",
                bg="#F7F3EF",
                fg="#444",
            ).pack(pady=40)
            return

        listbox = tk.Listbox(card, width=70)
        listbox.pack(padx=20, pady=10, fill="both", expand=True)
        for j in jobs:
            listbox.insert(tk.END, f"[{j.job_id}] {j.title}")

    def show_history_tab(self):
        self._clear_content()
        card = tk.Frame(self.content_frame, bg="#F7F3EF")
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="최근 본 알바",
            bg="#F7F3EF",
            font=("맑은 고딕", 12, "bold"),
        ).pack(pady=10)

        jobs = self.view_history_manager.get_recent_jobs(self.user.user_id, limit=10)
        if not jobs:
            tk.Label(
                card,
                text="최근 본 공고가 없습니다.",
                bg="#F7F3EF",
                fg="#444",
            ).pack(pady=40)
            return

        listbox = tk.Listbox(card, width=70)
        listbox.pack(padx=20, pady=10, fill="both", expand=True)
        for j in jobs:
            listbox.insert(tk.END, f"[{j.job_id}] {j.title}")


# ==========================
# FAQ & Inquiry
# ==========================
class FAQWindow:
    """FAQ / 1:1 문의 화면"""

    def __init__(self, root: tk.Tk, faq_manager: FAQManager):
        self.root = root
        self.faq_manager = faq_manager

        self.win = tk.Toplevel(self.root)
        self.win.title("FAQ")
        self.win.geometry("600x450")
        self.win.configure(bg="white")

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.win, bg="white")
        header.pack(fill="x", pady=10)

        tk.Label(
            header,
            text="FAQ",
            bg="white",
            fg="black",
            font=("맑은 고딕", 18, "bold"),
        ).pack(side="left", padx=20)

        tk.Button(
            header,
            text="✕",
            bg="white",
            bd=0,
            font=("맑은 고딕", 14),
            command=self.win.destroy,
        ).pack(side="right", padx=20)

        content = tk.Frame(self.win, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        faqs = self.faq_manager.get_all()
        if not faqs:
            tk.Label(
                content,
                text="등록된 FAQ가 없습니다.",
                bg="white",
                fg="#444",
            ).pack(pady=20)
            return

        text = scrolledtext.ScrolledText(content, width=70, height=20)
        text.pack(fill="both", expand=True)

        for f in faqs:
            text.insert(tk.END, f"[{f.category}] {f.question}\n")
            text.insert(tk.END, f"  - {f.answer}\n\n")

        text.config(state="disabled")
