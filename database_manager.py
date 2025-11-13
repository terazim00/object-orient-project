# database_manager.py
import sqlite3
from typing import Optional


class DatabaseManager:
    """SQLite 데이터베이스 연결 및 쿼리 실행"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: tuple = None):
        conn = self.connect()
        cur = conn.cursor()
        if params is None:
            cur.execute(query)
        else:
            cur.execute(query, params)
        conn.commit()
        return cur

    def create_tables(self):
        """필요한 테이블 전부 생성"""
        conn = self.connect()
        cur = conn.cursor()

        # 사용자
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT UNIQUE NOT NULL,
                password    TEXT NOT NULL,
                email       TEXT,
                phone       TEXT,
                student_id  TEXT,
                department  TEXT,
                role        TEXT DEFAULT 'student'
            )
            """
        )

        # 공고
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                job_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title           TEXT NOT NULL,
                description     TEXT,
                category        TEXT,
                location        TEXT,
                job_type        TEXT,
                work_hours      TEXT,
                salary          INTEGER,
                requirements    TEXT,
                deadline        TEXT,
                created_at      TEXT,
                department      TEXT,
                max_applicants  INTEGER
            )
            """
        )

        # 이력서
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
                resume_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT,
                content     TEXT,
                is_default  INTEGER DEFAULT 0,
                created_at  TEXT,
                updated_at  TEXT
            )
            """
        )

        # 지원서
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                application_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                job_id          INTEGER NOT NULL,
                resume_id       INTEGER,
                status          TEXT,
                submitted_at    TEXT
            )
            """
        )

        # 시간표
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS timetables (
                timetable_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL,
                semester        TEXT,
                schedule_data   TEXT,
                created_at      TEXT
            )
            """
        )

        # 스크랩(북마크)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bookmarks (
                bookmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                job_id      INTEGER NOT NULL,
                created_at  TEXT
            )
            """
        )

        # 열람 이력
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS view_history (
                history_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                job_id      INTEGER NOT NULL,
                viewed_at   TEXT
            )
            """
        )

        # FAQ
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS faqs (
                faq_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                category    TEXT,
                question    TEXT,
                answer      TEXT
            )
            """
        )

        # 1:1 문의
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS inquiries (
                inquiry_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT,
                content     TEXT,
                answer      TEXT,
                status      TEXT,
                created_at  TEXT,
                answered_at TEXT
            )
            """
        )

        conn.commit()
