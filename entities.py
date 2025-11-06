"""
엔티티 클래스 모듈
데이터베이스 테이블에 대응되는 도메인 객체들
"""

from datetime import datetime
from typing import Optional

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
        pass
    
    def is_admin(self) -> bool:
        """
        관리자 권한 확인
        :return: 관리자 여부
        """
        pass
    
    def is_staff(self) -> bool:
        """
        부서담당자 권한 확인
        :return: 부서담당자 여부
        """
        pass


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
        pass
    
    def is_expired(self) -> bool:
        """
        공고 마감 여부 확인
        :return: 마감 여부
        """
        pass
    
    def get_remaining_days(self) -> int:
        """
        마감까지 남은 일수 계산
        :return: 남은 일수
        """
        pass


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
        pass
    
    def set_status(self, status: str):
        """
        지원 상태 변경
        :param status: 새로운 상태
        """
        pass
    
    def get_timeline(self) -> list:
        """
        지원서 처리 타임라인 반환
        :return: 타임라인 리스트
        """
        pass


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
        pass
    
    def update_info(self, **kwargs):
        """
        이력서 정보 수정
        :param kwargs: 수정할 필드와 값
        """
        pass


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
        pass
    
    def is_available(self, day: str, start_time: str, end_time: str) -> bool:
        """
        특정 시간대의 가능 여부 확인
        :param day: 요일
        :param start_time: 시작 시간
        :param end_time: 종료 시간
        :return: 가능 여부
        """
        pass
    
    def get_free_slots(self) -> list:
        """
        비어있는 시간대 목록 반환
        :return: 가능한 시간대 리스트
        """
        pass