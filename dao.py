"""
DAO (Data Access Object) 모듈
데이터베이스 접근 로직을 담당하는 클래스들
"""

from typing import List, Optional
from datetime import datetime
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
        query = """
            INSERT INTO users (username, email, phone, student_id, department, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (user.username, user.email, user.phone, user.student_id,
                  user.department, user.role)
        return self.db_manager.execute_query(query, params)

    def update_user(self, user_id: int, data: dict) -> bool:
        """
        사용자 정보 수정
        :param user_id: 사용자 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        if not data:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE users SET {set_clause} WHERE user_id = ?"
        params = tuple(data.values()) + (user_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_user(self, user_id: int) -> bool:
        """
        사용자 삭제
        :param user_id: 사용자 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM users WHERE user_id = ?"
        result = self.db_manager.execute_query(query, (user_id,))
        return result is not None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        ID로 사용자 조회
        :param user_id: 사용자 ID
        :return: User 객체 또는 None
        """
        query = "SELECT * FROM users WHERE user_id = ?"
        rows = self.db_manager.execute_query(query, (user_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return User(
                user_id=row['user_id'],
                username=row['username'],
                email=row['email'],
                phone=row['phone'],
                student_id=row['student_id'],
                department=row['department'],
                role=row['role']
            )
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        사용자명으로 조회
        :param username: 사용자명
        :return: User 객체 또는 None
        """
        query = "SELECT * FROM users WHERE username = ?"
        rows = self.db_manager.execute_query(query, (username,))

        if rows and len(rows) > 0:
            row = rows[0]
            return User(
                user_id=row['user_id'],
                username=row['username'],
                email=row['email'],
                phone=row['phone'],
                student_id=row['student_id'],
                department=row['department'],
                role=row['role']
            )
        return None

    def get_user_by_student_id(self, student_id: str) -> Optional[User]:
        """
        학번으로 사용자 조회
        :param student_id: 학번
        :return: User 객체 또는 None
        """
        query = "SELECT * FROM users WHERE student_id = ?"
        rows = self.db_manager.execute_query(query, (student_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return User(
                user_id=row['user_id'],
                username=row['username'],
                email=row['email'],
                phone=row['phone'],
                student_id=row['student_id'],
                department=row['department'],
                role=row['role']
            )
        return None

    def get_all_users(self) -> List[User]:
        """
        모든 사용자 조회
        :return: User 객체 리스트
        """
        query = "SELECT * FROM users"
        rows = self.db_manager.execute_query(query)

        users = []
        if rows:
            for row in rows:
                users.append(User(
                    user_id=row['user_id'],
                    username=row['username'],
                    email=row['email'],
                    phone=row['phone'],
                    student_id=row['student_id'],
                    department=row['department'],
                    role=row['role']
                ))
        return users


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
        query = """
            INSERT INTO jobs (title, description, category, location, job_type,
                            work_hours, salary, requirements, deadline, department, max_applicants)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (job.title, job.description, job.category, job.location,
                  job.job_type, job.work_hours, job.salary, job.requirements,
                  job.deadline, job.department, job.max_applicants)
        return self.db_manager.execute_query(query, params)

    def update_job(self, job_id: int, data: dict) -> bool:
        """
        공고 정보 수정
        :param job_id: 공고 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        if not data:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE jobs SET {set_clause} WHERE job_id = ?"
        params = tuple(data.values()) + (job_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_job(self, job_id: int) -> bool:
        """
        공고 삭제
        :param job_id: 공고 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM jobs WHERE job_id = ?"
        result = self.db_manager.execute_query(query, (job_id,))
        return result is not None

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """
        ID로 공고 조회
        :param job_id: 공고 ID
        :return: Job 객체 또는 None
        """
        query = "SELECT * FROM jobs WHERE job_id = ?"
        rows = self.db_manager.execute_query(query, (job_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_job(row)
        return None

    def get_all_jobs(self) -> List[Job]:
        """
        모든 공고 조회
        :return: Job 객체 리스트
        """
        query = "SELECT * FROM jobs ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query)

        jobs = []
        if rows:
            for row in rows:
                jobs.append(self._row_to_job(row))
        return jobs

    def get_jobs_by_category(self, category: str) -> List[Job]:
        """
        카테고리별 공고 조회
        :param category: 카테고리 (장기/단기/일일)
        :return: Job 객체 리스트
        """
        query = "SELECT * FROM jobs WHERE category = ? ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (category,))

        jobs = []
        if rows:
            for row in rows:
                jobs.append(self._row_to_job(row))
        return jobs

    def get_jobs_by_location(self, location: str) -> List[Job]:
        """
        장소별 공고 조회
        :param location: 근무 장소
        :return: Job 객체 리스트
        """
        query = "SELECT * FROM jobs WHERE location = ? ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (location,))

        jobs = []
        if rows:
            for row in rows:
                jobs.append(self._row_to_job(row))
        return jobs

    def get_active_jobs(self) -> List[Job]:
        """
        마감되지 않은 공고 조회
        :return: Job 객체 리스트
        """
        query = "SELECT * FROM jobs WHERE deadline > datetime('now') OR deadline IS NULL ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query)

        jobs = []
        if rows:
            for row in rows:
                jobs.append(self._row_to_job(row))
        return jobs

    def search_jobs(self, keyword: str) -> List[Job]:
        """
        키워드로 공고 검색
        :param keyword: 검색 키워드
        :return: Job 객체 리스트
        """
        query = """
            SELECT * FROM jobs
            WHERE title LIKE ? OR description LIKE ? OR requirements LIKE ?
            ORDER BY created_at DESC
        """
        search_term = f"%{keyword}%"
        rows = self.db_manager.execute_query(query, (search_term, search_term, search_term))

        jobs = []
        if rows:
            for row in rows:
                jobs.append(self._row_to_job(row))
        return jobs

    def _row_to_job(self, row) -> Job:
        """Helper method to convert database row to Job object"""
        return Job(
            job_id=row['job_id'],
            title=row['title'],
            description=row['description'],
            category=row['category'],
            location=row['location'],
            job_type=row['job_type'],
            work_hours=row['work_hours'],
            salary=row['salary'],
            requirements=row['requirements'],
            deadline=datetime.fromisoformat(row['deadline']) if row['deadline'] else None,
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            department=row['department'],
            max_applicants=row['max_applicants']
        )


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
        query = """
            INSERT INTO applications (user_id, job_id, resume_id, status, cover_letter)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (application.user_id, application.job_id, application.resume_id,
                  application.status, application.cover_letter)
        return self.db_manager.execute_query(query, params)

    def update_application(self, application_id: int, data: dict) -> bool:
        """
        지원서 정보 수정
        :param application_id: 지원서 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        if not data:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE applications SET {set_clause} WHERE application_id = ?"
        params = tuple(data.values()) + (application_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_application(self, application_id: int) -> bool:
        """
        지원서 삭제
        :param application_id: 지원서 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM applications WHERE application_id = ?"
        result = self.db_manager.execute_query(query, (application_id,))
        return result is not None

    def get_application_by_id(self, application_id: int) -> Optional[Application]:
        """
        ID로 지원서 조회
        :param application_id: 지원서 ID
        :return: Application 객체 또는 None
        """
        query = "SELECT * FROM applications WHERE application_id = ?"
        rows = self.db_manager.execute_query(query, (application_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_application(row)
        return None

    def get_applications_by_user(self, user_id: int) -> List[Application]:
        """
        사용자의 모든 지원서 조회
        :param user_id: 사용자 ID
        :return: Application 객체 리스트
        """
        query = "SELECT * FROM applications WHERE user_id = ? ORDER BY submitted_at DESC"
        rows = self.db_manager.execute_query(query, (user_id,))

        applications = []
        if rows:
            for row in rows:
                applications.append(self._row_to_application(row))
        return applications

    def get_applications_by_job(self, job_id: int) -> List[Application]:
        """
        특정 공고의 모든 지원서 조회
        :param job_id: 공고 ID
        :return: Application 객체 리스트
        """
        query = "SELECT * FROM applications WHERE job_id = ? ORDER BY submitted_at DESC"
        rows = self.db_manager.execute_query(query, (job_id,))

        applications = []
        if rows:
            for row in rows:
                applications.append(self._row_to_application(row))
        return applications

    def get_applications_by_status(self, user_id: int, status: str) -> List[Application]:
        """
        상태별 지원서 조회
        :param user_id: 사용자 ID
        :param status: 지원 상태
        :return: Application 객체 리스트
        """
        query = "SELECT * FROM applications WHERE user_id = ? AND status = ? ORDER BY submitted_at DESC"
        rows = self.db_manager.execute_query(query, (user_id, status))

        applications = []
        if rows:
            for row in rows:
                applications.append(self._row_to_application(row))
        return applications

    def _row_to_application(self, row) -> Application:
        """Helper method to convert database row to Application object"""
        return Application(
            application_id=row['application_id'],
            user_id=row['user_id'],
            job_id=row['job_id'],
            resume_id=row['resume_id'],
            status=row['status'],
            submitted_at=datetime.fromisoformat(row['submitted_at']) if row['submitted_at'] else None,
            cover_letter=row['cover_letter']
        )


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
        query = """
            INSERT INTO notifications (user_id, message, notification_type, is_read, related_id)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (notification.user_id, notification.message, notification.notification_type,
                  1 if notification.is_read else 0, notification.related_id)
        return self.db_manager.execute_query(query, params)

    def update_notification(self, notification_id: int, data: dict) -> bool:
        """
        알림 정보 수정
        :param notification_id: 알림 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        if not data:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE notifications SET {set_clause} WHERE notification_id = ?"
        params = tuple(data.values()) + (notification_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_notification(self, notification_id: int) -> bool:
        """
        알림 삭제
        :param notification_id: 알림 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM notifications WHERE notification_id = ?"
        result = self.db_manager.execute_query(query, (notification_id,))
        return result is not None

    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        ID로 알림 조회
        :param notification_id: 알림 ID
        :return: Notification 객체 또는 None
        """
        query = "SELECT * FROM notifications WHERE notification_id = ?"
        rows = self.db_manager.execute_query(query, (notification_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_notification(row)
        return None

    def get_notifications_by_user(self, user_id: int) -> List[Notification]:
        """
        사용자의 모든 알림 조회
        :param user_id: 사용자 ID
        :return: Notification 객체 리스트
        """
        query = "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (user_id,))

        notifications = []
        if rows:
            for row in rows:
                notifications.append(self._row_to_notification(row))
        return notifications

    def get_unread_notifications(self, user_id: int) -> List[Notification]:
        """
        읽지 않은 알림 조회
        :param user_id: 사용자 ID
        :return: Notification 객체 리스트
        """
        query = "SELECT * FROM notifications WHERE user_id = ? AND is_read = 0 ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (user_id,))

        notifications = []
        if rows:
            for row in rows:
                notifications.append(self._row_to_notification(row))
        return notifications

    def mark_all_as_read(self, user_id: int) -> bool:
        """
        사용자의 모든 알림을 읽음 처리
        :param user_id: 사용자 ID
        :return: 처리 성공 여부
        """
        query = "UPDATE notifications SET is_read = 1 WHERE user_id = ?"
        result = self.db_manager.execute_query(query, (user_id,))
        return result is not None

    def _row_to_notification(self, row) -> Notification:
        """Helper method to convert database row to Notification object"""
        return Notification(
            notification_id=row['notification_id'],
            user_id=row['user_id'],
            message=row['message'],
            notification_type=row['notification_type'],
            is_read=bool(row['is_read']),
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            related_id=row['related_id']
        )


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
        query = """
            INSERT INTO resumes (user_id, title, education, experience, certifications, self_introduction)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (resume.user_id, resume.title, resume.education, resume.experience,
                  resume.certifications, resume.self_introduction)
        return self.db_manager.execute_query(query, params)

    def update_resume(self, resume_id: int, data: dict) -> bool:
        """
        이력서 정보 수정
        :param resume_id: 이력서 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        if not data:
            return False

        data['updated_at'] = datetime.now().isoformat()
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE resumes SET {set_clause} WHERE resume_id = ?"
        params = tuple(data.values()) + (resume_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_resume(self, resume_id: int) -> bool:
        """
        이력서 삭제
        :param resume_id: 이력서 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM resumes WHERE resume_id = ?"
        result = self.db_manager.execute_query(query, (resume_id,))
        return result is not None

    def get_resume_by_id(self, resume_id: int) -> Optional[Resume]:
        """
        ID로 이력서 조회
        :param resume_id: 이력서 ID
        :return: Resume 객체 또는 None
        """
        query = "SELECT * FROM resumes WHERE resume_id = ?"
        rows = self.db_manager.execute_query(query, (resume_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_resume(row)
        return None

    def get_resumes_by_user(self, user_id: int) -> List[Resume]:
        """
        사용자의 모든 이력서 조회
        :param user_id: 사용자 ID
        :return: Resume 객체 리스트
        """
        query = "SELECT * FROM resumes WHERE user_id = ? ORDER BY updated_at DESC"
        rows = self.db_manager.execute_query(query, (user_id,))

        resumes = []
        if rows:
            for row in rows:
                resumes.append(self._row_to_resume(row))
        return resumes

    def get_default_resume(self, user_id: int) -> Optional[Resume]:
        """
        사용자의 기본 이력서 조회
        :param user_id: 사용자 ID
        :return: Resume 객체 또는 None
        """
        # 가장 최근에 업데이트된 이력서를 기본 이력서로 간주
        query = "SELECT * FROM resumes WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1"
        rows = self.db_manager.execute_query(query, (user_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_resume(row)
        return None

    def _row_to_resume(self, row) -> Resume:
        """Helper method to convert database row to Resume object"""
        return Resume(
            resume_id=row['resume_id'],
            user_id=row['user_id'],
            title=row['title'],
            education=row['education'],
            experience=row['experience'],
            certifications=row['certifications'],
            self_introduction=row['self_introduction'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )


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
        import json
        query = """
            INSERT INTO timetables (user_id, semester, schedule_data)
            VALUES (?, ?, ?)
        """
        schedule_json = json.dumps(timetable.schedule_data) if isinstance(timetable.schedule_data, dict) else timetable.schedule_data
        params = (timetable.user_id, timetable.semester, schedule_json)
        return self.db_manager.execute_query(query, params)

    def update_timetable(self, timetable_id: int, data: dict) -> bool:
        """
        시간표 정보 수정
        :param timetable_id: 시간표 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        import json
        if not data:
            return False

        # schedule_data가 딕셔너리면 JSON으로 변환
        if 'schedule_data' in data and isinstance(data['schedule_data'], dict):
            data['schedule_data'] = json.dumps(data['schedule_data'])

        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE timetables SET {set_clause} WHERE timetable_id = ?"
        params = tuple(data.values()) + (timetable_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_timetable(self, timetable_id: int) -> bool:
        """
        시간표 삭제
        :param timetable_id: 시간표 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM timetables WHERE timetable_id = ?"
        result = self.db_manager.execute_query(query, (timetable_id,))
        return result is not None

    def get_timetable_by_id(self, timetable_id: int) -> Optional[Timetable]:
        """
        ID로 시간표 조회
        :param timetable_id: 시간표 ID
        :return: Timetable 객체 또는 None
        """
        query = "SELECT * FROM timetables WHERE timetable_id = ?"
        rows = self.db_manager.execute_query(query, (timetable_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_timetable(row)
        return None

    def get_timetable_by_user(self, user_id: int, semester: str) -> Optional[Timetable]:
        """
        사용자의 특정 학기 시간표 조회
        :param user_id: 사용자 ID
        :param semester: 학기
        :return: Timetable 객체 또는 None
        """
        query = "SELECT * FROM timetables WHERE user_id = ? AND semester = ?"
        rows = self.db_manager.execute_query(query, (user_id, semester))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_timetable(row)
        return None

    def get_current_timetable(self, user_id: int) -> Optional[Timetable]:
        """
        사용자의 현재 학기 시간표 조회
        :param user_id: 사용자 ID
        :return: Timetable 객체 또는 None
        """
        # 가장 최근 시간표를 현재 학기로 간주
        query = "SELECT * FROM timetables WHERE user_id = ? ORDER BY created_at DESC LIMIT 1"
        rows = self.db_manager.execute_query(query, (user_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_timetable(row)
        return None

    def _row_to_timetable(self, row) -> Timetable:
        """Helper method to convert database row to Timetable object"""
        return Timetable(
            timetable_id=row['timetable_id'],
            user_id=row['user_id'],
            semester=row['semester'],
            schedule_data=row['schedule_data'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )


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
        query = """
            INSERT INTO bookmarks (user_id, job_id)
            VALUES (?, ?)
        """
        params = (bookmark.user_id, bookmark.job_id)
        return self.db_manager.execute_query(query, params)

    def delete_bookmark(self, bookmark_id: int) -> bool:
        """
        북마크 삭제
        :param bookmark_id: 북마크 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM bookmarks WHERE bookmark_id = ?"
        result = self.db_manager.execute_query(query, (bookmark_id,))
        return result is not None

    def get_bookmarks_by_user(self, user_id: int) -> List[Bookmark]:
        """
        사용자의 모든 북마크 조회
        :param user_id: 사용자 ID
        :return: Bookmark 객체 리스트
        """
        query = "SELECT * FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (user_id,))

        bookmarks = []
        if rows:
            for row in rows:
                bookmarks.append(Bookmark(
                    bookmark_id=row['bookmark_id'],
                    user_id=row['user_id'],
                    job_id=row['job_id'],
                    created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                ))
        return bookmarks

    def is_bookmarked(self, user_id: int, job_id: int) -> bool:
        """
        특정 공고의 북마크 여부 확인
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 북마크 여부
        """
        query = "SELECT COUNT(*) as count FROM bookmarks WHERE user_id = ? AND job_id = ?"
        rows = self.db_manager.execute_query(query, (user_id, job_id))

        if rows and len(rows) > 0:
            return rows[0]['count'] > 0
        return False

    def delete_bookmark_by_job(self, user_id: int, job_id: int) -> bool:
        """
        특정 공고의 북마크 삭제
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM bookmarks WHERE user_id = ? AND job_id = ?"
        result = self.db_manager.execute_query(query, (user_id, job_id))
        return result is not None


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
        query = """
            INSERT INTO view_history (user_id, job_id)
            VALUES (?, ?)
        """
        params = (history.user_id, history.job_id)
        return self.db_manager.execute_query(query, params)

    def get_recent_views(self, user_id: int, days: int = 7) -> List[ViewHistory]:
        """
        최근 열람 이력 조회
        :param user_id: 사용자 ID
        :param days: 조회할 일수
        :return: ViewHistory 객체 리스트
        """
        query = """
            SELECT * FROM view_history
            WHERE user_id = ? AND viewed_at >= datetime('now', '-' || ? || ' days')
            ORDER BY viewed_at DESC
        """
        rows = self.db_manager.execute_query(query, (user_id, days))

        histories = []
        if rows:
            for row in rows:
                histories.append(ViewHistory(
                    history_id=row['history_id'],
                    user_id=row['user_id'],
                    job_id=row['job_id'],
                    viewed_at=datetime.fromisoformat(row['viewed_at']) if row['viewed_at'] else None
                ))
        return histories

    def get_view_count(self, job_id: int) -> int:
        """
        특정 공고의 조회수 계산
        :param job_id: 공고 ID
        :return: 조회수
        """
        query = "SELECT COUNT(*) as count FROM view_history WHERE job_id = ?"
        rows = self.db_manager.execute_query(query, (job_id,))

        if rows and len(rows) > 0:
            return rows[0]['count']
        return 0

    def delete_old_history(self, days: int = 30) -> bool:
        """
        오래된 열람 이력 삭제
        :param days: 기준 일수
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM view_history WHERE viewed_at < datetime('now', '-' || ? || ' days')"
        result = self.db_manager.execute_query(query, (days,))
        return result is not None


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
        query = """
            INSERT INTO faqs (category, question, answer, view_count)
            VALUES (?, ?, ?, ?)
        """
        params = (faq.category, faq.question, faq.answer, faq.view_count)
        return self.db_manager.execute_query(query, params)

    def update_faq(self, faq_id: int, data: dict) -> bool:
        """
        FAQ 정보 수정
        :param faq_id: FAQ ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        if not data:
            return False

        data['updated_at'] = datetime.now().isoformat()
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE faqs SET {set_clause} WHERE faq_id = ?"
        params = tuple(data.values()) + (faq_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_faq(self, faq_id: int) -> bool:
        """
        FAQ 삭제
        :param faq_id: FAQ ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM faqs WHERE faq_id = ?"
        result = self.db_manager.execute_query(query, (faq_id,))
        return result is not None

    def get_all_faqs(self) -> List[FAQ]:
        """
        모든 FAQ 조회
        :return: FAQ 객체 리스트
        """
        query = "SELECT * FROM faqs ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query)

        faqs = []
        if rows:
            for row in rows:
                faqs.append(self._row_to_faq(row))
        return faqs

    def get_faqs_by_category(self, category: str) -> List[FAQ]:
        """
        카테고리별 FAQ 조회
        :param category: 카테고리
        :return: FAQ 객체 리스트
        """
        query = "SELECT * FROM faqs WHERE category = ? ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (category,))

        faqs = []
        if rows:
            for row in rows:
                faqs.append(self._row_to_faq(row))
        return faqs

    def search_faqs(self, keyword: str) -> List[FAQ]:
        """
        키워드로 FAQ 검색
        :param keyword: 검색 키워드
        :return: FAQ 객체 리스트
        """
        query = """
            SELECT * FROM faqs
            WHERE question LIKE ? OR answer LIKE ?
            ORDER BY created_at DESC
        """
        search_term = f"%{keyword}%"
        rows = self.db_manager.execute_query(query, (search_term, search_term))

        faqs = []
        if rows:
            for row in rows:
                faqs.append(self._row_to_faq(row))
        return faqs

    def _row_to_faq(self, row) -> FAQ:
        """Helper method to convert database row to FAQ object"""
        return FAQ(
            faq_id=row['faq_id'],
            category=row['category'],
            question=row['question'],
            answer=row['answer'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
            view_count=row['view_count']
        )


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
        query = """
            INSERT INTO inquiries (user_id, title, content, status)
            VALUES (?, ?, ?, ?)
        """
        params = (inquiry.user_id, inquiry.title, inquiry.content, inquiry.status)
        return self.db_manager.execute_query(query, params)

    def update_inquiry(self, inquiry_id: int, data: dict) -> bool:
        """
        문의 정보 수정
        :param inquiry_id: 문의 ID
        :param data: 수정할 데이터
        :return: 수정 성공 여부
        """
        if not data:
            return False

        # 답변이 추가되면 answered_at 업데이트
        if 'answer' in data and data['answer']:
            data['answered_at'] = datetime.now().isoformat()
            data['status'] = '답변완료'

        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE inquiries SET {set_clause} WHERE inquiry_id = ?"
        params = tuple(data.values()) + (inquiry_id,)

        result = self.db_manager.execute_query(query, params)
        return result is not None

    def delete_inquiry(self, inquiry_id: int) -> bool:
        """
        문의 삭제
        :param inquiry_id: 문의 ID
        :return: 삭제 성공 여부
        """
        query = "DELETE FROM inquiries WHERE inquiry_id = ?"
        result = self.db_manager.execute_query(query, (inquiry_id,))
        return result is not None

    def get_inquiry_by_id(self, inquiry_id: int) -> Optional[Inquiry]:
        """
        ID로 문의 조회
        :param inquiry_id: 문의 ID
        :return: Inquiry 객체 또는 None
        """
        query = "SELECT * FROM inquiries WHERE inquiry_id = ?"
        rows = self.db_manager.execute_query(query, (inquiry_id,))

        if rows and len(rows) > 0:
            row = rows[0]
            return self._row_to_inquiry(row)
        return None

    def get_inquiries_by_user(self, user_id: int) -> List[Inquiry]:
        """
        사용자의 모든 문의 조회
        :param user_id: 사용자 ID
        :return: Inquiry 객체 리스트
        """
        query = "SELECT * FROM inquiries WHERE user_id = ? ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (user_id,))

        inquiries = []
        if rows:
            for row in rows:
                inquiries.append(self._row_to_inquiry(row))
        return inquiries

    def get_unanswered_inquiries(self) -> List[Inquiry]:
        """
        답변되지 않은 문의 조회
        :return: Inquiry 객체 리스트
        """
        query = "SELECT * FROM inquiries WHERE status = '대기중' ORDER BY created_at ASC"
        rows = self.db_manager.execute_query(query)

        inquiries = []
        if rows:
            for row in rows:
                inquiries.append(self._row_to_inquiry(row))
        return inquiries

    def get_inquiries_by_status(self, status: str) -> List[Inquiry]:
        """
        상태별 문의 조회
        :param status: 처리 상태
        :return: Inquiry 객체 리스트
        """
        query = "SELECT * FROM inquiries WHERE status = ? ORDER BY created_at DESC"
        rows = self.db_manager.execute_query(query, (status,))

        inquiries = []
        if rows:
            for row in rows:
                inquiries.append(self._row_to_inquiry(row))
        return inquiries

    def _row_to_inquiry(self, row) -> Inquiry:
        """Helper method to convert database row to Inquiry object"""
        return Inquiry(
            inquiry_id=row['inquiry_id'],
            user_id=row['user_id'],
            title=row['title'],
            content=row['content'],
            answer=row['answer'],
            status=row['status'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            answered_at=datetime.fromisoformat(row['answered_at']) if row['answered_at'] else None
        )
