"""
데이터베이스 관리 모듈
SQLite 데이터베이스 연결 및 쿼리 실행을 담당
"""

import sqlite3
from typing import Any, List, Tuple, Optional

class DatabaseManager:
    """데이터베이스 연결 및 트랜잭션 관리"""
    
    def __init__(self, db_path: str):
        """
        데이터베이스 매니저 초기화
        :param db_path: SQLite 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        """
        데이터베이스 연결 생성
        :return: Connection 객체
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
            return self.connection
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def disconnect(self):
        """
        데이터베이스 연결 종료
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: tuple = None):
        """
        SQL 쿼리 실행
        :param query: 실행할 SQL 쿼리
        :param params: 쿼리 파라미터
        :return: 쿼리 실행 결과
        """
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # SELECT 쿼리인 경우 결과 반환
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.lastrowid  # INSERT의 경우 생성된 ID 반환
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            self.connection.rollback()
            return None

    def begin_transaction(self):
        """
        트랜잭션 시작
        """
        if not self.connection:
            self.connect()
        self.connection.execute("BEGIN TRANSACTION")

    def commit(self):
        """
        트랜잭션 커밋
        """
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """
        트랜잭션 롤백
        """
        if self.connection:
            self.connection.rollback()

    def create_tables(self):
        """
        필요한 모든 테이블 생성
        """
        if not self.connection:
            self.connect()

        # Users 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT,
                phone TEXT,
                student_id TEXT UNIQUE,
                department TEXT,
                role TEXT DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Jobs 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                location TEXT,
                job_type TEXT,
                work_hours TEXT,
                salary INTEGER,
                requirements TEXT,
                deadline TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                department TEXT,
                max_applicants INTEGER
            )
        """)

        # Applications 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                resume_id INTEGER,
                status TEXT DEFAULT '제출',
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cover_letter TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (job_id) REFERENCES jobs(job_id),
                FOREIGN KEY (resume_id) REFERENCES resumes(resume_id)
            )
        """)

        # Resumes 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS resumes (
                resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT,
                education TEXT,
                experience TEXT,
                certifications TEXT,
                self_introduction TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Timetables 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS timetables (
                timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                semester TEXT,
                schedule_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Notifications 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                related_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Bookmarks 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                bookmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (job_id) REFERENCES jobs(job_id),
                UNIQUE(user_id, job_id)
            )
        """)

        # ViewHistory 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS view_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (job_id) REFERENCES jobs(job_id)
            )
        """)

        # FAQs 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS faqs (
                faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                view_count INTEGER DEFAULT 0
            )
        """)

        # Inquiries 테이블
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS inquiries (
                inquiry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                answer TEXT,
                status TEXT DEFAULT '대기중',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                answered_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        print("All tables created successfully")
