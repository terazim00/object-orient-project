# 디자인 패턴 적용 가이드 - 한기 WORKS 시스템

이 문서는 한기 WORKS 근로장학 관리 시스템에 적용된 8가지 디자인 패턴을 설명합니다.

## 📋 목차

1. [싱글톤 (Singleton)](#1-싱글톤-singleton)
2. [팩토리 메서드 (Factory Method)](#2-팩토리-메서드-factory-method)
3. [추상 팩토리 (Abstract Factory)](#3-추상-팩토리-abstract-factory)
4. [옵저버 (Observer)](#4-옵저버-observer)
5. [전략 (Strategy)](#5-전략-strategy)
6. [데코레이터 (Decorator)](#6-데코레이터-decorator)
7. [상태 (State)](#7-상태-state)
8. [파사드 (Facade)](#8-파사드-facade)

---

## 1. 싱글톤 (Singleton)

### 목적
애플리케이션 전체에서 **하나의 인스턴스만** 생성되도록 보장

### 적용 위치
`DatabaseManagerSingleton` - 데이터베이스 연결 관리

### 코드 예제
```python
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseManagerSingleton(metaclass=SingletonMeta):
    def __init__(self, db_path: str = "hangi_works.db"):
        if not hasattr(self, 'initialized'):
            self.db_path = db_path
            self.connection = None
            self.initialized = True
```

### 왜 사용했나?
- 데이터베이스 연결은 시스템 리소스를 많이 사용
- 여러 개의 연결을 생성하면 성능 저하 발생
- 하나의 연결을 공유하여 효율성 향상
- 스레드 안전성 보장

### 실행 결과
```
[싱글톤] DatabaseManager 인스턴스 생성: hangi_works.db
db1 is db2: True  # 동일한 인스턴스 반환
```

---

## 2. 팩토리 메서드 (Factory Method)

### 목적
객체 생성 로직을 **캡슐화**하여 유연한 객체 생성

### 적용 위치
- `JobFactory` - 다양한 Job 객체 생성
- `ApplicationFactory` - Application 객체 생성

### 코드 예제
```python
class JobFactory(EntityFactory):
    def create_entity(self, **kwargs) -> Job:
        return Job(**kwargs)

    def create_urgent_job(self, **kwargs) -> Job:
        job = self.create_entity(**kwargs)
        job.category = f"긴급-{job.category}"
        return job

    def create_featured_job(self, **kwargs) -> Job:
        job = self.create_entity(**kwargs)
        job.title = f"⭐ {job.title}"
        return job
```

### 왜 사용했나?
- Job 객체 생성 시 다양한 타입(일반, 긴급, 추천)이 필요
- 생성 로직을 한 곳에서 관리
- 새로운 타입 추가가 쉬움
- 코드 중복 제거

### 실행 결과
```
[팩토리 메서드] Job 생성: 도서관 사서 보조
[팩토리 메서드] Job 생성: 실험실 조교
[팩토리 메서드] Job 생성: 멘토링 튜터
```

---

## 3. 추상 팩토리 (Abstract Factory)

### 목적
**관련된 객체들의 군(family)**을 함께 생성

### 적용 위치
- `JobComponentFactory` - JobManager + JobDAO 생성
- `ApplicationComponentFactory` - ApplicationManager + ApplicationDAO 생성

### 코드 예제
```python
class JobComponentFactory(ComponentFactory):
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_manager(self):
        return JobManager(self.create_dao())

    def create_dao(self):
        return JobDAO(self.db_manager)
```

### 왜 사용했나?
- Manager와 DAO는 항상 쌍으로 생성됨
- 의존성 주입을 자동으로 처리
- 컴포넌트 간 일관성 유지
- 새로운 도메인 추가 시 팩토리만 추가하면 됨

### 실행 결과
```
[추상 팩토리] JobManager 생성
[추상 팩토리] JobDAO 생성
[추상 팩토리] ApplicationManager 생성
[추상 팩토리] ApplicationDAO 생성
```

---

## 4. 옵저버 (Observer)

### 목적
객체의 상태 변화를 **여러 객체에 자동으로 알림**

### 적용 위치
지원서(Application) 상태 변경 시 알림 시스템

### 구현된 옵저버들
1. `EmailNotificationObserver` - 이메일 발송
2. `SMSNotificationObserver` - SMS 발송
3. `LogObserver` - 로그 기록

### 코드 예제
```python
class EmailNotificationObserver(Observer):
    def update(self, subject: Application, message: str):
        print(f"[옵저버-이메일] 지원서 #{subject.entity_id} 상태 변경: {message}")
        print(f"  → 이메일 발송: user_{subject.user_id}@hangi.ac.kr")

# 사용 예
app.add_observer(EmailNotificationObserver())
app.add_observer(SMSNotificationObserver())
app.add_observer(LogObserver())
app.notify_observers("검토가 시작되었습니다")
```

### 왜 사용했나?
- 지원서 상태 변경 시 학생에게 즉시 알림 필요
- 알림 방법(이메일, SMS, 로그)을 독립적으로 관리
- 새로운 알림 방법 추가가 쉬움
- 느슨한 결합(loose coupling) 유지

### 실행 결과
```
[옵저버-이메일] 지원서 #1 상태 변경: 검토가 시작되었습니다
  → 이메일 발송: user_101@hangi.ac.kr
[옵저버-SMS] 지원서 #1 상태 변경: 검토가 시작되었습니다
  → SMS 발송: user_101
[옵저버-로그] [2025-11-20 05:32:23] Application #1: 검토가 시작되었습니다
```

---

## 5. 전략 (Strategy)

### 목적
알고리즘을 **런타임에 선택**할 수 있도록 캡슐화

### 적용 위치
Job 검색 기능

### 구현된 전략들
1. `TitleSearchStrategy` - 제목 검색
2. `CategorySearchStrategy` - 카테고리 검색
3. `SalaryRangeSearchStrategy` - 급여 범위 검색

### 코드 예제
```python
class JobSearcher:
    def __init__(self, strategy: SearchStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def execute_search(self, jobs: List[Job], criteria: str = "") -> List[Job]:
        return self.strategy.search(jobs, criteria)

# 사용 예
searcher = JobSearcher()
searcher.set_strategy(TitleSearchStrategy())
results = searcher.execute_search(jobs, "도서관")

searcher.set_strategy(CategorySearchStrategy())
results = searcher.execute_search(jobs, "행정")
```

### 왜 사용했나?
- 검색 방법이 다양함 (제목, 카테고리, 급여 등)
- 검색 방법을 동적으로 변경 필요
- 새로운 검색 전략 추가가 쉬움
- if-else 지옥 방지

### 실행 결과
```
[전략-제목검색] '도서관' 검색
✓ 1개 검색 결과

[전략-카테고리검색] '행정' 검색
✓ 1개 검색 결과

[전략-급여검색] 100000원 ~ 130000원
✓ 2개 검색 결과
```

---

## 6. 데코레이터 (Decorator)

### 목적
객체에 **동적으로 기능을 추가**

### 적용 위치
Job 객체에 다양한 속성 추가

### 구현된 데코레이터들
1. `UrgentJobDecorator` - 긴급 공고 (급여 10% 인상)
2. `FeaturedJobDecorator` - 추천 공고 (⭐ 표시)
3. `BonusJobDecorator` - 보너스 지급 공고 (보너스 금액 추가)

### 코드 예제
```python
# 기본 Job
job_component = BasicJob(job)
print(f"급여: {job_component.get_salary():,}원")  # 100,000원

# 긴급 데코레이터 추가
urgent_job = UrgentJobDecorator(job_component)
print(f"급여: {urgent_job.get_salary():,}원")  # 110,000원 (10% 인상)

# 추천 데코레이터 추가
featured_urgent = FeaturedJobDecorator(urgent_job)

# 보너스 데코레이터 추가
bonus_job = BonusJobDecorator(featured_urgent, 30000)
print(f"급여: {bonus_job.get_salary():,}원")  # 140,000원
```

### 왜 사용했나?
- Job에 다양한 속성(긴급, 추천, 보너스)을 조합 가능
- 상속 대신 구성(composition) 사용
- 런타임에 기능 추가/제거 가능
- 조합 폭발(combinatorial explosion) 방지

### 실행 결과
```
기본: [행정] 도서관 사서 보조 - 100000원
급여: 100,000원

긴급 추가: 🚨 [긴급] [행정] 도서관 사서 보조 - 100000원
급여: 110,000원

추천 추가: ⭐ [추천] 🚨 [긴급] [행정] 도서관 사서 보조 - 100000원
급여: 110,000원

보너스 추가: 💰 [보너스] ⭐ [추천] 🚨 [긴급] [행정] 도서관 사서 보조 - 100000원 (+30000원)
급여: 140,000원
```

---

## 7. 상태 (State)

### 목적
객체의 **내부 상태에 따라 행동을 변경**

### 적용 위치
Application(지원서)의 상태 관리

### 구현된 상태들
1. `SubmittedState` - 제출됨
2. `UnderReviewState` - 검토중
3. `ApprovedState` - 승인됨
4. `RejectedState` - 반려됨

### 코드 예제
```python
class UnderReviewState(ApplicationState):
    def handle(self, application: Application):
        print(f"[상태-검토중] 지원서 #{application.entity_id} 검토 진행 중")
        application.status = "검토중"
        application.notify_observers("검토가 시작되었습니다")

# 사용 예
app.set_state(SubmittedState())
app.process()  # 제출 상태 처리

app.set_state(UnderReviewState())
app.process()  # 검토중 상태 처리

app.set_state(ApprovedState())
app.process()  # 승인 상태 처리
```

### 왜 사용했나?
- 지원서는 명확한 상태 전환이 있음
- 상태별로 다른 동작 수행
- 상태 전환 로직을 캡슐화
- if-else 조건문 제거

### 실행 결과
```
[상태-제출됨] 지원서 #1 검토 대기 중
[상태-검토중] 지원서 #1 검토 진행 중
[상태-승인됨] 지원서 #1 합격!
```

---

## 8. 파사드 (Facade)

### 목적
**복잡한 서브시스템을 간단한 인터페이스**로 제공

### 적용 위치
`HangiWorksFacade` - 전체 시스템의 통합 인터페이스

### 제공 기능
```python
class HangiWorksFacade:
    def create_sample_jobs(self)                    # 공고 생성
    def apply_job_decorators(self, job)             # 데코레이터 적용
    def search_jobs_by_title(self, keyword)         # 제목 검색
    def search_jobs_by_category(self, category)     # 카테고리 검색
    def search_jobs_by_salary_range(self, min, max) # 급여 검색
    def submit_application(self, user_id, job_id)   # 지원서 제출
    def review_application(self, application)       # 검토 시작
    def approve_application(self, application)      # 승인
    def reject_application(self, application)       # 반려
```

### 왜 사용했나?
- 여러 디자인 패턴을 사용하는 복잡한 시스템
- 클라이언트가 쉽게 사용할 수 있는 간단한 인터페이스 필요
- 서브시스템 간 의존성 숨김
- 사용하기 쉬운 API 제공

### 실행 결과
```python
# 복잡한 초기화를 한 줄로
facade = HangiWorksFacade()

# 간단한 메서드 호출로 복잡한 작업 수행
jobs = facade.create_sample_jobs()
results = facade.search_jobs_by_title("도서관")
app = facade.submit_application(user_id=101, job_id=1)
facade.approve_application(app)
```

---

## 🎯 패턴 조합의 시너지

### 지원서 제출 시나리오
```python
# 1. 파사드로 간단하게 호출
app = facade.submit_application(user_id=101, job_id=1)

# 내부적으로는...
# 2. 팩토리 메서드로 Application 생성
# 3. 옵저버 패턴으로 이메일/SMS 발송
# 4. 상태 패턴으로 "제출됨" 상태 처리
```

### 공고 검색 시나리오
```python
# 1. 파사드로 간단하게 호출
results = facade.search_jobs_by_salary_range(100000, 150000)

# 내부적으로는...
# 2. 전략 패턴으로 검색 알고리즘 선택
# 3. 결과 Job들은 팩토리 메서드로 생성됨
# 4. 데코레이터로 추가 속성 부여 가능
```

---

## 📊 패턴 요약 비교표

| 패턴 | 분류 | 핵심 개념 | 사용 이유 |
|------|------|-----------|-----------|
| 싱글톤 | 생성 | 인스턴스 하나만 | DB 연결 관리 |
| 팩토리 메서드 | 생성 | 객체 생성 캡슐화 | 다양한 Job 타입 |
| 추상 팩토리 | 생성 | 관련 객체 군 생성 | Manager+DAO 쌍 |
| 옵저버 | 행동 | 상태 변화 알림 | 지원 상태 알림 |
| 전략 | 행동 | 알고리즘 캡슐화 | 검색 방법 선택 |
| 데코레이터 | 구조 | 동적 기능 추가 | Job 속성 조합 |
| 상태 | 행동 | 상태별 행동 변경 | 지원서 상태 관리 |
| 파사드 | 구조 | 간단한 인터페이스 | 복잡성 숨김 |

---

## 🚀 실행 방법

```bash
# 데모 실행
python design_patterns_demo.py
```

---

## 📚 참고 자료

- Gang of Four (GoF) Design Patterns
- Head First Design Patterns
- Refactoring Guru - Design Patterns

---

## 💡 실무 적용 팁

### 언제 싱글톤을 사용할까?
- 데이터베이스 연결
- 로깅 시스템
- 설정 관리자
- 캐시 관리자

### 언제 팩토리를 사용할까?
- 객체 생성이 복잡할 때
- 생성할 객체 타입이 다양할 때
- 생성 로직을 숨기고 싶을 때

### 언제 옵저버를 사용할까?
- 이벤트 처리 시스템
- 상태 변화 알림
- 여러 객체가 동기화되어야 할 때

### 언제 전략을 사용할까?
- 알고리즘을 런타임에 선택
- 조건문이 많을 때
- 유사한 동작의 변형이 많을 때

### 언제 데코레이터를 사용할까?
- 객체에 동적으로 기능 추가
- 상속보다 구성을 선호할 때
- 기능 조합이 필요할 때

### 언제 상태를 사용할까?
- 명확한 상태 전환이 있을 때
- 상태별로 다른 동작 필요
- 상태 관련 조건문이 많을 때

### 언제 파사드를 사용할까?
- 복잡한 시스템을 간단히 사용
- 레거시 시스템 래핑
- API 단순화

---

## 🔧 확장 가능성

### 추가할 수 있는 패턴들

1. **프로토타입 (Prototype)** - Resume 복사
2. **빌더 (Builder)** - 복잡한 Job 객체 생성
3. **컴포지트 (Composite)** - 부서 계층 구조
4. **프록시 (Proxy)** - 지연 로딩
5. **책임 연쇄 (Chain of Responsibility)** - 승인 체인
6. **커맨드 (Command)** - 작업 취소/재실행
7. **반복자 (Iterator)** - Job 목록 순회
8. **중재자 (Mediator)** - UI 컴포넌트 간 통신
9. **템플릿 메서드 (Template Method)** - DAO 공통 로직

---

이 문서는 한기 WORKS 시스템의 디자인 패턴 적용 사례를 설명합니다.
실제 프로젝트에 적용할 때는 과도한 패턴 사용을 피하고, 필요한 패턴만 선택적으로 사용하세요.

**"패턴은 도구일 뿐입니다. 문제를 해결하기 위해 사용하되, 패턴을 위한 패턴은 피하세요."**
