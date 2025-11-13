"""
엔티티 클래스 모듈
데이터베이스 테이블에 대응되는 도메인 객체들
"""

from datetime import datetime
from typing import Optional
import json

class User:
    """사용자 정보를 담는 엔티티"""
    
    def __init__(self, user_id: int = None, username: str = None, 
                 email: str = None, phone: str = None, 
                 student_id: str = None, department: str = None,
                 role: str = "student"):
        """
        사용자 객체 초기화
        :param user_id: 사용자 고유 ID
        :param username: 사용자 이름
        :param email: 이메일 주소
        :param phone: 전화번호
        :param student_id: 학번
        :param department: 학과
        :param role: 역할 (student/staff/admin)
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.phone = phone
        self.student_id = student_id
        self.department = department
        self.role = role
        
    def get_info(self) -> dict:
        """
        사용자 정보를 딕셔너리로 반환
        :return: 사용자 정보 딕셔너리
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "student_id": self.student_id,
            "department": self.department,
            "role": self.role
        }

    def is_admin(self) -> bool:
        """
        관리자 권한 확인
        :return: 관리자 여부
        """
        return self.role == "admin"

    def is_staff(self) -> bool:
        """
        부서담당자 권한 확인
        :return: 부서담당자 여부
        """
        return self.role == "staff"


class Job:
    """근로장학 공고 정보를 담는 엔티티"""
    
    def __init__(self, job_id: int = None, title: str = None,
                 description: str = None, category: str = None,
                 location: str = None, job_type: str = None,
                 work_hours: str = None, salary: int = None,
                 requirements: str = None, deadline: datetime = None,
                 created_at: datetime = None, department: str = None,
                 max_applicants: int = None):
        """
        공고 객체 초기화
        :param job_id: 공고 고유 ID
        :param title: 공고 제목
        :param description: 공고 상세 설명
        :param category: 카테고리 (장기/단기/일일)
        :param location: 근무 장소
        :param job_type: 근무 유형
        :param work_hours: 근무 시간
        :param salary: 시급
        :param requirements: 지원 자격
        :param deadline: 마감일
        :param created_at: 공고 등록일
        :param department: 담당 부서
        :param max_applicants: 최대 모집 인원
        """
        self.job_id = job_id
        self.title = title
        self.description = description
        self.category = category
        self.location = location
        self.job_type = job_type
        self.work_hours = work_hours
        self.salary = salary
        self.requirements = requirements
        self.deadline = deadline
        self.created_at = created_at
        self.department = department
        self.max_applicants = max_applicants
        
    def get_details(self) -> dict:
        """
        공고 상세 정보를 딕셔너리로 반환
        :return: 공고 정보 딕셔너리
        """
        return {
            "job_id": self.job_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "location": self.location,
            "job_type": self.job_type,
            "work_hours": self.work_hours,
            "salary": self.salary,
            "requirements": self.requirements,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "department": self.department,
            "max_applicants": self.max_applicants
        }

    def is_expired(self) -> bool:
        """
        공고 마감 여부 확인
        :return: 마감 여부
        """
        if self.deadline is None:
            return False
        return datetime.now() > self.deadline

    def get_remaining_days(self) -> int:
        """
        마감까지 남은 일수 계산
        :return: 남은 일수
        """
        if self.deadline is None:
            return -1
        delta = self.deadline - datetime.now()
        return max(0, delta.days)


class Application:
    """지원서 정보를 담는 엔티티"""
    
    def __init__(self, application_id: int = None, user_id: int = None,
                 job_id: int = None, resume_id: int = None,
                 status: str = "제출", submitted_at: datetime = None,
                 cover_letter: str = None):
        """
        지원서 객체 초기화
        :param application_id: 지원서 고유 ID
        :param user_id: 지원자 ID
        :param job_id: 공고 ID
        :param resume_id: 이력서 ID
        :param status: 지원 상태 (제출/서류통과/면접/선발/불합격)
        :param submitted_at: 제출 일시
        :param cover_letter: 자기소개서
        """
        self.application_id = application_id
        self.user_id = user_id
        self.job_id = job_id
        self.resume_id = resume_id
        self.status = status
        self.submitted_at = submitted_at
        self.cover_letter = cover_letter
        
    def get_status(self) -> str:
        """
        현재 지원 상태 반환
        :return: 지원 상태
        """
        return self.status

    def set_status(self, status: str):
        """
        지원 상태 변경
        :param status: 새로운 상태
        """
        self.status = status

    def get_timeline(self) -> list:
        """
        지원서 처리 타임라인 반환
        :return: 타임라인 리스트
        """
        # 간단한 타임라인 반환 (실제로는 별도 테이블에서 조회하는 것이 좋음)
        timeline = []
        if self.submitted_at:
            timeline.append({
                "status": "제출",
                "timestamp": self.submitted_at.isoformat() if isinstance(self.submitted_at, datetime) else self.submitted_at
            })
        if self.status != "제출":
            timeline.append({
                "status": self.status,
                "timestamp": datetime.now().isoformat()
            })
        return timeline


class Resume:
    """이력서 정보를 담는 엔티티"""
    
    def __init__(self, resume_id: int = None, user_id: int = None,
                 title: str = None, education: str = None,
                 experience: str = None, certifications: str = None,
                 self_introduction: str = None, created_at: datetime = None,
                 updated_at: datetime = None):
        """
        이력서 객체 초기화
        :param resume_id: 이력서 고유 ID
        :param user_id: 작성자 ID
        :param title: 이력서 제목
        :param education: 학력 사항
        :param experience: 경력 사항
        :param certifications: 자격증
        :param self_introduction: 자기소개
        :param created_at: 생성 일시
        :param updated_at: 수정 일시
        """
        self.resume_id = resume_id
        self.user_id = user_id
        self.title = title
        self.education = education
        self.experience = experience
        self.certifications = certifications
        self.self_introduction = self_introduction
        self.created_at = created_at
        self.updated_at = updated_at
        
    def get_info(self) -> dict:
        """
        이력서 정보를 딕셔너리로 반환
        :return: 이력서 정보
        """
        return {
            "resume_id": self.resume_id,
            "user_id": self.user_id,
            "title": self.title,
            "education": self.education,
            "experience": self.experience,
            "certifications": self.certifications,
            "self_introduction": self.self_introduction,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def update_info(self, **kwargs):
        """
        이력서 정보 수정
        :param kwargs: 수정할 필드와 값
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()


class Timetable:
    """시간표 정보를 담는 엔티티"""
    
    def __init__(self, timetable_id: int = None, user_id: int = None,
                 semester: str = None, schedule_data: str = None,
                 created_at: datetime = None):
        """
        시간표 객체 초기화
        :param timetable_id: 시간표 고유 ID
        :param user_id: 소유자 ID
        :param semester: 학기 (예: 2025-1)
        :param schedule_data: 시간표 데이터 (JSON 형식)
        :param created_at: 생성 일시
        """
        self.timetable_id = timetable_id
        self.user_id = user_id
        self.semester = semester
        self.schedule_data = schedule_data
        self.created_at = created_at
        
    def get_schedule(self) -> dict:
        """
        시간표 데이터를 파싱하여 반환
        :return: 시간표 딕셔너리
        """
        if not self.schedule_data:
            return {}
        if isinstance(self.schedule_data, str):
            try:
                return json.loads(self.schedule_data)
            except json.JSONDecodeError:
                return {}
        return self.schedule_data

    def is_available(self, day: str, start_time: str, end_time: str) -> bool:
        """
        특정 시간대의 가능 여부 확인
        :param day: 요일
        :param start_time: 시작 시간
        :param end_time: 종료 시간
        :return: 가능 여부
        """
        schedule = self.get_schedule()
        if day not in schedule:
            return True

        # 간단한 시간 충돌 체크 (시:분 형식 가정, 예: "09:00")
        for class_info in schedule.get(day, []):
            class_start = class_info.get("start_time", "")
            class_end = class_info.get("end_time", "")

            # 시간 겹침 확인
            if not (end_time <= class_start or start_time >= class_end):
                return False

        return True

    def get_free_slots(self) -> list:
        """
        비어있는 시간대 목록 반환
        :return: 가능한 시간대 리스트
        """
        schedule = self.get_schedule()
        days = ["월", "화", "수", "목", "금"]
        free_slots = []

        for day in days:
            if day not in schedule or not schedule[day]:
                free_slots.append({
                    "day": day,
                    "note": "전체 시간 가능"
                })
            else:
                free_slots.append({
                    "day": day,
                    "busy_times": schedule[day]
                })

        return free_slots


class Notification:
    """알림 정보를 담는 엔티티"""

    def __init__(self, notification_id: int = None, user_id: int = None,
                 message: str = None, notification_type: str = None,
                 is_read: bool = False, created_at: datetime = None,
                 related_id: int = None):
        """
        알림 객체 초기화
        :param notification_id: 알림 고유 ID
        :param user_id: 수신자 ID
        :param message: 알림 메시지
        :param notification_type: 알림 유형 (지원상태/마감임박/신규공고 등)
        :param is_read: 읽음 여부
        :param created_at: 생성 일시
        :param related_id: 관련 객체 ID (공고 ID, 지원서 ID 등)
        """
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.notification_type = notification_type
        self.is_read = is_read
        self.created_at = created_at
        self.related_id = related_id

    def mark_as_read(self):
        """
        알림을 읽음으로 표시
        """
        self.is_read = True

    def get_info(self) -> dict:
        """
        알림 정보를 딕셔너리로 반환
        :return: 알림 정보
        """
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "notification_type": self.notification_type,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "related_id": self.related_id
        }


class Bookmark:
    """북마크(관심공고) 정보를 담는 엔티티"""

    def __init__(self, bookmark_id: int = None, user_id: int = None,
                 job_id: int = None, created_at: datetime = None):
        """
        북마크 객체 초기화
        :param bookmark_id: 북마크 고유 ID
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :param created_at: 북마크 생성 일시
        """
        self.bookmark_id = bookmark_id
        self.user_id = user_id
        self.job_id = job_id
        self.created_at = created_at

    def get_info(self) -> dict:
        """
        북마크 정보를 딕셔너리로 반환
        :return: 북마크 정보
        """
        return {
            "bookmark_id": self.bookmark_id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ViewHistory:
    """공고 열람 이력 정보를 담는 엔티티"""

    def __init__(self, history_id: int = None, user_id: int = None,
                 job_id: int = None, viewed_at: datetime = None):
        """
        열람 이력 객체 초기화
        :param history_id: 이력 고유 ID
        :param user_id: 사용자 ID
        :param job_id: 공고 ID
        :param viewed_at: 열람 일시
        """
        self.history_id = history_id
        self.user_id = user_id
        self.job_id = job_id
        self.viewed_at = viewed_at

    def get_info(self) -> dict:
        """
        열람 이력 정보를 딕셔너리로 반환
        :return: 이력 정보
        """
        return {
            "history_id": self.history_id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "viewed_at": self.viewed_at.isoformat() if self.viewed_at else None
        }


class FAQ:
    """FAQ 정보를 담는 엔티티"""

    def __init__(self, faq_id: int = None, category: str = None,
                 question: str = None, answer: str = None,
                 created_at: datetime = None, updated_at: datetime = None,
                 view_count: int = 0):
        """
        FAQ 객체 초기화
        :param faq_id: FAQ 고유 ID
        :param category: 카테고리
        :param question: 질문
        :param answer: 답변
        :param created_at: 생성 일시
        :param updated_at: 수정 일시
        :param view_count: 조회수
        """
        self.faq_id = faq_id
        self.category = category
        self.question = question
        self.answer = answer
        self.created_at = created_at
        self.updated_at = updated_at
        self.view_count = view_count

    def get_info(self) -> dict:
        """
        FAQ 정보를 딕셔너리로 반환
        :return: FAQ 정보
        """
        return {
            "faq_id": self.faq_id,
            "category": self.category,
            "question": self.question,
            "answer": self.answer,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "view_count": self.view_count
        }

    def increment_view_count(self):
        """
        조회수 증가
        """
        self.view_count += 1


class Inquiry:
    """1:1 문의 정보를 담는 엔티티"""

    def __init__(self, inquiry_id: int = None, user_id: int = None,
                 title: str = None, content: str = None,
                 answer: str = None, status: str = "대기중",
                 created_at: datetime = None, answered_at: datetime = None):
        """
        문의 객체 초기화
        :param inquiry_id: 문의 고유 ID
        :param user_id: 문의자 ID
        :param title: 문의 제목
        :param content: 문의 내용
        :param answer: 답변 내용
        :param status: 처리 상태 (대기중/답변완료)
        :param created_at: 문의 생성 일시
        :param answered_at: 답변 일시
        """
        self.inquiry_id = inquiry_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.answer = answer
        self.status = status
        self.created_at = created_at
        self.answered_at = answered_at

    def get_info(self) -> dict:
        """
        문의 정보를 딕셔너리로 반환
        :return: 문의 정보
        """
        return {
            "inquiry_id": self.inquiry_id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "answer": self.answer,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "answered_at": self.answered_at.isoformat() if self.answered_at else None
        }

    def is_answered(self) -> bool:
        """
        답변 완료 여부 확인
        :return: 답변 여부
        """
        return self.status == "답변완료" or (self.answer is not None and self.answer.strip() != "")