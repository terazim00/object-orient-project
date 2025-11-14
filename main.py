# main.py
import tkinter as tk
from database_manager import DatabaseManager
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
from gui_modules import LoginWindow, MainWindow


DB_PATH = "hangi_works.db"


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("한기 WORKS - 근로장학 관리 시스템")
        self.root.geometry("1200x800")

        self.db_manager = DatabaseManager(DB_PATH)
        self.db_manager.create_tables()

        # Managers
        self.user_manager = UserManager(self.db_manager)
        self.job_manager = JobManager(self.db_manager)
        self.resume_manager = ResumeManager(self.db_manager)
        self.application_manager = ApplicationManager(self.db_manager)
        self.bookmark_manager = BookmarkManager(self.db_manager)
        self.view_history_manager = ViewHistoryManager(self.db_manager)
        self.timetable_manager = TimetableManager(self.db_manager)
        self.faq_manager = FAQManager(self.db_manager)
        self.inquiry_manager = InquiryManager(self.db_manager)

        # FAQ 기본 데이터
        self.faq_manager.seed_default_faqs()

        # 로그인 화면부터 시작
        self.current_user = None
        LoginWindow(self.root, self.user_manager, self.on_login_success)

    def on_login_success(self, user):
        self.current_user = user
        MainWindow(
            self.root,
            self.current_user,
            self.user_manager,
            self.job_manager,
            self.resume_manager,
            self.application_manager,
            self.bookmark_manager,
            self.view_history_manager,
            self.timetable_manager,
            self.faq_manager,
            self.inquiry_manager,
        )

    def run(self):
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
