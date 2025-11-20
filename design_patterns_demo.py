"""
디자인 패턴 적용 예제 - 한기 WORKS 시스템

적용된 패턴:
1. 싱글톤 (Singleton) - DatabaseManager
2. 팩토리 메서드 (Factory Method) - EntityFactory
3. 추상 팩토리 (Abstract Factory) - ComponentFactory
4. 옵저버 (Observer) - ApplicationObserver
5. 전략 (Strategy) - JobSearchStrategy
6. 데코레이터 (Decorator) - JobDecorator
7. 상태 (State) - ApplicationState
8. 파사드 (Facade) - HangiWorksFacade
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import threading


# ============================================================
# 1. 싱글톤 패턴 (Singleton Pattern)
# ============================================================
class SingletonMeta(type):
    """싱글톤 메타클래스 - 스레드 안전"""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseManagerSingleton(metaclass=SingletonMeta):
    """싱글톤 DatabaseManager - 애플리케이션 전체에서 하나의 DB 연결만 유지"""

    def __init__(self, db_path: str = "hangi_works.db"):
        if not hasattr(self, 'initialized'):
            self.db_path = db_path
            self.connection = None
            self.initialized = True
            print(f"[싱글톤] DatabaseManager 인스턴스 생성: {db_path}")

    def get_connection(self):
        """DB 연결 반환"""
        if self.connection is None:
            import sqlite3
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def execute(self, query: str, params: tuple = None):
        """쿼리 실행"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor


# ============================================================
# 2. 팩토리 메서드 패턴 (Factory Method Pattern)
# ============================================================
class Entity:
    """기본 엔티티 클래스"""
    def __init__(self, entity_id: int = None):
        self.entity_id = entity_id


class Job(Entity):
    """근로장학 공고"""
    def __init__(self, job_id: int = None, title: str = "", description: str = "",
                 category: str = "", salary: int = 0, deadline: datetime = None):
        super().__init__(job_id)
        self.title = title
        self.description = description
        self.category = category
        self.salary = salary
        self.deadline = deadline
        self.observers = []  # 옵저버 패턴용

    def get_info(self) -> str:
        return f"[{self.category}] {self.title} - {self.salary}원"

    def is_expired(self) -> bool:
        if not self.deadline:
            return False
        return datetime.now() > self.deadline


class Application(Entity):
    """지원서"""
    def __init__(self, application_id: int = None, user_id: int = None,
                 job_id: int = None, status: str = "제출"):
        super().__init__(application_id)
        self.user_id = user_id
        self.job_id = job_id
        self.status = status
        self.state = None  # 상태 패턴용
        self.observers = []  # 옵저버 패턴용

    def set_state(self, state):
        """상태 변경"""
        self.state = state

    def process(self):
        """현재 상태에 따른 처리"""
        if self.state:
            self.state.handle(self)

    def notify_observers(self, message: str):
        """옵저버들에게 알림"""
        for observer in self.observers:
            observer.update(self, message)

    def add_observer(self, observer):
        """옵저버 추가"""
        self.observers.append(observer)


class EntityFactory(ABC):
    """추상 팩토리 메서드 클래스"""

    @abstractmethod
    def create_entity(self, **kwargs) -> Entity:
        """엔티티 생성"""
        pass


class JobFactory(EntityFactory):
    """Job 생성 팩토리"""

    def create_entity(self, **kwargs) -> Job:
        print(f"[팩토리 메서드] Job 생성: {kwargs.get('title', 'Unknown')}")
        return Job(**kwargs)

    def create_urgent_job(self, **kwargs) -> Job:
        """긴급 공고 생성"""
        job = self.create_entity(**kwargs)
        job.category = f"긴급-{job.category}"
        return job

    def create_featured_job(self, **kwargs) -> Job:
        """추천 공고 생성"""
        job = self.create_entity(**kwargs)
        job.title = f"⭐ {job.title}"
        return job


class ApplicationFactory(EntityFactory):
    """Application 생성 팩토리"""

    def create_entity(self, **kwargs) -> Application:
        print(f"[팩토리 메서드] Application 생성: user_id={kwargs.get('user_id')}")
        return Application(**kwargs)


# ============================================================
# 3. 추상 팩토리 패턴 (Abstract Factory Pattern)
# ============================================================
class ComponentFactory(ABC):
    """추상 컴포넌트 팩토리 - Manager와 DAO를 함께 생성"""

    @abstractmethod
    def create_manager(self) -> Any:
        pass

    @abstractmethod
    def create_dao(self) -> Any:
        pass


class JobComponentFactory(ComponentFactory):
    """Job 관련 컴포넌트 팩토리"""

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_manager(self):
        print("[추상 팩토리] JobManager 생성")
        return JobManager(self.create_dao())

    def create_dao(self):
        print("[추상 팩토리] JobDAO 생성")
        return JobDAO(self.db_manager)


class ApplicationComponentFactory(ComponentFactory):
    """Application 관련 컴포넌트 팩토리"""

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_manager(self):
        print("[추상 팩토리] ApplicationManager 생성")
        return ApplicationManager(self.create_dao())

    def create_dao(self):
        print("[추상 팩토리] ApplicationDAO 생성")
        return ApplicationDAO(self.db_manager)


# ============================================================
# 4. 옵저버 패턴 (Observer Pattern)
# ============================================================
class Observer(ABC):
    """추상 옵저버"""

    @abstractmethod
    def update(self, subject: Any, message: str):
        """상태 변경 알림 받기"""
        pass


class EmailNotificationObserver(Observer):
    """이메일 알림 옵저버"""

    def update(self, subject: Application, message: str):
        print(f"[옵저버-이메일] 지원서 #{subject.entity_id} 상태 변경: {message}")
        print(f"  → 이메일 발송: user_{subject.user_id}@hangi.ac.kr")


class SMSNotificationObserver(Observer):
    """SMS 알림 옵저버"""

    def update(self, subject: Application, message: str):
        print(f"[옵저버-SMS] 지원서 #{subject.entity_id} 상태 변경: {message}")
        print(f"  → SMS 발송: user_{subject.user_id}")


class LogObserver(Observer):
    """로그 기록 옵저버"""

    def update(self, subject: Application, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[옵저버-로그] [{timestamp}] Application #{subject.entity_id}: {message}")


# ============================================================
# 5. 전략 패턴 (Strategy Pattern)
# ============================================================
class SearchStrategy(ABC):
    """검색 전략 인터페이스"""

    @abstractmethod
    def search(self, jobs: List[Job], criteria: str) -> List[Job]:
        """검색 실행"""
        pass


class TitleSearchStrategy(SearchStrategy):
    """제목 검색 전략"""

    def search(self, jobs: List[Job], criteria: str) -> List[Job]:
        print(f"[전략-제목검색] '{criteria}' 검색")
        return [job for job in jobs if criteria.lower() in job.title.lower()]


class CategorySearchStrategy(SearchStrategy):
    """카테고리 검색 전략"""

    def search(self, jobs: List[Job], criteria: str) -> List[Job]:
        print(f"[전략-카테고리검색] '{criteria}' 검색")
        return [job for job in jobs if criteria.lower() in job.category.lower()]


class SalaryRangeSearchStrategy(SearchStrategy):
    """급여 범위 검색 전략"""

    def __init__(self, min_salary: int, max_salary: int):
        self.min_salary = min_salary
        self.max_salary = max_salary

    def search(self, jobs: List[Job], criteria: str = "") -> List[Job]:
        print(f"[전략-급여검색] {self.min_salary}원 ~ {self.max_salary}원")
        return [job for job in jobs
                if self.min_salary <= job.salary <= self.max_salary]


class JobSearcher:
    """검색 전략을 사용하는 클라이언트"""

    def __init__(self, strategy: SearchStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        """전략 변경"""
        self.strategy = strategy

    def execute_search(self, jobs: List[Job], criteria: str = "") -> List[Job]:
        """전략을 사용해 검색"""
        if not self.strategy:
            return jobs
        return self.strategy.search(jobs, criteria)


# ============================================================
# 6. 데코레이터 패턴 (Decorator Pattern)
# ============================================================
class JobComponent(ABC):
    """Job 컴포넌트 인터페이스"""

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_salary(self) -> int:
        pass


class BasicJob(JobComponent):
    """기본 Job"""

    def __init__(self, job: Job):
        self.job = job

    def get_description(self) -> str:
        return self.job.get_info()

    def get_salary(self) -> int:
        return self.job.salary


class JobDecorator(JobComponent):
    """Job 데코레이터 기본 클래스"""

    def __init__(self, job_component: JobComponent):
        self.job_component = job_component

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_salary(self) -> int:
        pass


class UrgentJobDecorator(JobDecorator):
    """긴급 공고 데코레이터"""

    def get_description(self) -> str:
        return f"🚨 [긴급] {self.job_component.get_description()}"

    def get_salary(self) -> int:
        # 긴급 공고는 급여 10% 인상
        return int(self.job_component.get_salary() * 1.1)


class FeaturedJobDecorator(JobDecorator):
    """추천 공고 데코레이터"""

    def get_description(self) -> str:
        return f"⭐ [추천] {self.job_component.get_description()}"

    def get_salary(self) -> int:
        return self.job_component.get_salary()


class BonusJobDecorator(JobDecorator):
    """보너스 지급 공고 데코레이터"""

    def __init__(self, job_component: JobComponent, bonus: int = 50000):
        super().__init__(job_component)
        self.bonus = bonus

    def get_description(self) -> str:
        return f"💰 [보너스] {self.job_component.get_description()} (+{self.bonus}원)"

    def get_salary(self) -> int:
        return self.job_component.get_salary() + self.bonus


# ============================================================
# 7. 상태 패턴 (State Pattern)
# ============================================================
class ApplicationState(ABC):
    """지원서 상태 인터페이스"""

    @abstractmethod
    def handle(self, application: Application):
        """상태별 처리"""
        pass

    @abstractmethod
    def get_status_name(self) -> str:
        pass


class SubmittedState(ApplicationState):
    """제출됨 상태"""

    def handle(self, application: Application):
        print(f"[상태-제출됨] 지원서 #{application.entity_id} 검토 대기 중")
        application.status = "제출"

    def get_status_name(self) -> str:
        return "제출"


class UnderReviewState(ApplicationState):
    """검토중 상태"""

    def handle(self, application: Application):
        print(f"[상태-검토중] 지원서 #{application.entity_id} 검토 진행 중")
        application.status = "검토중"
        application.notify_observers("검토가 시작되었습니다")

    def get_status_name(self) -> str:
        return "검토중"


class ApprovedState(ApplicationState):
    """승인됨 상태"""

    def handle(self, application: Application):
        print(f"[상태-승인됨] 지원서 #{application.entity_id} 합격!")
        application.status = "승인"
        application.notify_observers("축하합니다! 합격하셨습니다")

    def get_status_name(self) -> str:
        return "승인"


class RejectedState(ApplicationState):
    """반려됨 상태"""

    def handle(self, application: Application):
        print(f"[상태-반려됨] 지원서 #{application.entity_id} 불합격")
        application.status = "반려"
        application.notify_observers("아쉽지만 불합격하셨습니다")

    def get_status_name(self) -> str:
        return "반려"


# ============================================================
# 8. 파사드 패턴 (Facade Pattern)
# ============================================================
class HangiWorksFacade:
    """한기 WORKS 시스템의 복잡한 서브시스템을 간단하게 사용할 수 있는 파사드"""

    def __init__(self):
        print("\n" + "="*60)
        print("한기 WORKS 파사드 초기화")
        print("="*60)

        # 싱글톤 DB 매니저
        self.db_manager = DatabaseManagerSingleton()

        # 팩토리들
        self.job_factory = JobFactory()
        self.application_factory = ApplicationFactory()

        # 컴포넌트 팩토리
        self.job_component_factory = JobComponentFactory(self.db_manager)
        self.app_component_factory = ApplicationComponentFactory(self.db_manager)

        # 옵저버들
        self.email_observer = EmailNotificationObserver()
        self.sms_observer = SMSNotificationObserver()
        self.log_observer = LogObserver()

        # 검색 전략
        self.job_searcher = JobSearcher()

        # 샘플 데이터
        self.jobs = []
        self.applications = []

        print("[파사드] 초기화 완료\n")

    def create_sample_jobs(self):
        """샘플 공고 생성"""
        print("\n[파사드] 샘플 공고 생성")
        print("-" * 60)

        # 일반 공고
        job1 = self.job_factory.create_entity(
            job_id=1,
            title="도서관 사서 보조",
            description="도서관 업무 보조",
            category="행정",
            salary=100000,
            deadline=datetime(2025, 12, 31)
        )

        # 긴급 공고
        job2 = self.job_factory.create_urgent_job(
            job_id=2,
            title="실험실 조교",
            description="실험 준비 및 정리",
            category="실습",
            salary=120000,
            deadline=datetime(2025, 12, 15)
        )

        # 추천 공고
        job3 = self.job_factory.create_featured_job(
            job_id=3,
            title="멘토링 튜터",
            description="신입생 멘토링",
            category="교육",
            salary=150000,
            deadline=datetime(2025, 12, 20)
        )

        self.jobs = [job1, job2, job3]
        print(f"✓ {len(self.jobs)}개의 공고 생성 완료\n")
        return self.jobs

    def apply_job_decorators(self, job: Job) -> JobComponent:
        """공고에 데코레이터 적용 예제"""
        print(f"\n[파사드] 공고 데코레이터 적용: {job.title}")
        print("-" * 60)

        # 기본 Job을 Component로 래핑
        job_component = BasicJob(job)
        print(f"기본: {job_component.get_description()}")
        print(f"급여: {job_component.get_salary():,}원")

        # 긴급 데코레이터 추가
        urgent_job = UrgentJobDecorator(job_component)
        print(f"\n긴급 추가: {urgent_job.get_description()}")
        print(f"급여: {urgent_job.get_salary():,}원")

        # 추천 데코레이터 추가
        featured_urgent = FeaturedJobDecorator(urgent_job)
        print(f"\n추천 추가: {featured_urgent.get_description()}")
        print(f"급여: {featured_urgent.get_salary():,}원")

        # 보너스 데코레이터 추가
        bonus_featured_urgent = BonusJobDecorator(featured_urgent, 30000)
        print(f"\n보너스 추가: {bonus_featured_urgent.get_description()}")
        print(f"급여: {bonus_featured_urgent.get_salary():,}원")

        return bonus_featured_urgent

    def search_jobs_by_title(self, keyword: str) -> List[Job]:
        """제목으로 공고 검색"""
        print(f"\n[파사드] 공고 검색 (제목)")
        print("-" * 60)
        self.job_searcher.set_strategy(TitleSearchStrategy())
        results = self.job_searcher.execute_search(self.jobs, keyword)
        print(f"✓ {len(results)}개 검색 결과\n")
        return results

    def search_jobs_by_category(self, category: str) -> List[Job]:
        """카테고리로 공고 검색"""
        print(f"\n[파사드] 공고 검색 (카테고리)")
        print("-" * 60)
        self.job_searcher.set_strategy(CategorySearchStrategy())
        results = self.job_searcher.execute_search(self.jobs, category)
        print(f"✓ {len(results)}개 검색 결과\n")
        return results

    def search_jobs_by_salary_range(self, min_sal: int, max_sal: int) -> List[Job]:
        """급여 범위로 공고 검색"""
        print(f"\n[파사드] 공고 검색 (급여)")
        print("-" * 60)
        self.job_searcher.set_strategy(SalaryRangeSearchStrategy(min_sal, max_sal))
        results = self.job_searcher.execute_search(self.jobs)
        print(f"✓ {len(results)}개 검색 결과\n")
        return results

    def submit_application(self, user_id: int, job_id: int) -> Application:
        """지원서 제출 (옵저버 + 상태 패턴 포함)"""
        print(f"\n[파사드] 지원서 제출: user_id={user_id}, job_id={job_id}")
        print("-" * 60)

        # 지원서 생성
        app = self.application_factory.create_entity(
            application_id=len(self.applications) + 1,
            user_id=user_id,
            job_id=job_id,
            status="제출"
        )

        # 옵저버 등록
        app.add_observer(self.email_observer)
        app.add_observer(self.sms_observer)
        app.add_observer(self.log_observer)

        # 초기 상태 설정
        app.set_state(SubmittedState())
        app.process()

        self.applications.append(app)
        print(f"✓ 지원서 #{app.entity_id} 제출 완료\n")
        return app

    def review_application(self, application: Application):
        """지원서 검토 시작"""
        print(f"\n[파사드] 지원서 검토 시작")
        print("-" * 60)
        application.set_state(UnderReviewState())
        application.process()

    def approve_application(self, application: Application):
        """지원서 승인"""
        print(f"\n[파사드] 지원서 승인")
        print("-" * 60)
        application.set_state(ApprovedState())
        application.process()

    def reject_application(self, application: Application):
        """지원서 반려"""
        print(f"\n[파사드] 지원서 반려")
        print("-" * 60)
        application.set_state(RejectedState())
        application.process()


# ============================================================
# DAO 클래스 (간단한 예제)
# ============================================================
class JobDAO:
    """Job DAO"""
    def __init__(self, db_manager):
        self.db_manager = db_manager


class ApplicationDAO:
    """Application DAO"""
    def __init__(self, db_manager):
        self.db_manager = db_manager


class JobManager:
    """Job Manager"""
    def __init__(self, job_dao):
        self.job_dao = job_dao


class ApplicationManager:
    """Application Manager"""
    def __init__(self, app_dao):
        self.app_dao = app_dao


# ============================================================
# 데모 실행 함수
# ============================================================
def demonstrate_all_patterns():
    """모든 디자인 패턴 시연"""

    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "한기 WORKS 디자인 패턴 데모" + " "*20 + "║")
    print("╚" + "="*58 + "╝")

    # 파사드 패턴으로 전체 시스템 초기화
    facade = HangiWorksFacade()

    # 1. 공고 생성 (팩토리 메서드 패턴)
    jobs = facade.create_sample_jobs()

    # 2. 데코레이터 패턴 - 공고에 기능 추가
    decorated_job = facade.apply_job_decorators(jobs[0])

    # 3. 전략 패턴 - 다양한 검색 방법
    facade.search_jobs_by_title("도서관")
    facade.search_jobs_by_category("행정")
    facade.search_jobs_by_salary_range(100000, 130000)

    # 4. 지원서 제출 (팩토리 메서드 + 옵저버 + 상태 패턴)
    app1 = facade.submit_application(user_id=101, job_id=1)

    # 5. 상태 변경 (상태 패턴 + 옵저버 패턴)
    facade.review_application(app1)
    facade.approve_application(app1)

    # 6. 다른 지원서 (반려 케이스)
    app2 = facade.submit_application(user_id=102, job_id=2)
    facade.review_application(app2)
    facade.reject_application(app2)

    # 7. 싱글톤 패턴 검증
    print("\n[검증] 싱글톤 패턴")
    print("-" * 60)
    db1 = DatabaseManagerSingleton()
    db2 = DatabaseManagerSingleton()
    print(f"db1 is db2: {db1 is db2}")
    print(f"동일한 인스턴스: {id(db1) == id(db2)}")

    # 8. 추상 팩토리 패턴 검증
    print("\n[검증] 추상 팩토리 패턴")
    print("-" * 60)
    job_factory = JobComponentFactory(facade.db_manager)
    job_manager = job_factory.create_manager()

    app_factory = ApplicationComponentFactory(facade.db_manager)
    app_manager = app_factory.create_manager()

    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "패턴 적용 완료!" + " "*23 + "║")
    print("║" + " "*58 + "║")
    print("║  ✓ 싱글톤 (Singleton)" + " "*35 + "║")
    print("║  ✓ 팩토리 메서드 (Factory Method)" + " "*24 + "║")
    print("║  ✓ 추상 팩토리 (Abstract Factory)" + " "*23 + "║")
    print("║  ✓ 옵저버 (Observer)" + " "*36 + "║")
    print("║  ✓ 전략 (Strategy)" + " "*38 + "║")
    print("║  ✓ 데코레이터 (Decorator)" + " "*31 + "║")
    print("║  ✓ 상태 (State)" + " "*41 + "║")
    print("║  ✓ 파사드 (Facade)" + " "*38 + "║")
    print("╚" + "="*58 + "╝")
    print()


if __name__ == "__main__":
    demonstrate_all_patterns()
