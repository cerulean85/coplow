#!/usr/bin/env python3
"""Service Planner Agent의 7개 순차 태스크 정의.

실행 순서 (Process.sequential 강제):
  Task 1: JTBD 분석 & 서비스 컨셉 정의
  Task 2: User Journey Map 작성
  Task 3: User Flow & IA 설계
  Task 4: 기능 우선순위화 (MoSCoW + RICE)
  Task 5: MVP 정의 & Phase 로드맵
  Task 6: PRD 통합 보고서 작성
  Task 7: 프로토타입 & 검증 계획

각 태스크는 이전 태스크의 결과를 context로 자동 수신한다.
"""

from __future__ import annotations

import logging
from typing import Any

from crewai import Agent, Task

logger = logging.getLogger(__name__)


def _make_jtbd_task(agent: Agent, inputs: dict[str, str]) -> Task:
    """JTBD 분석 & 서비스 컨셉 정의 태스크를 생성한다.

    Args:
        agent: 담당 JTBD 분석 에이전트.
        inputs: service_concept, target_user, market_analysis 키를 포함한 딕셔너리.

    Returns:
        설정된 CrewAI Task 인스턴스.
    """
    return Task(
        description=f"""
아래 입력 정보를 분석해 서비스 컨셉과 사용자 JTBD를 정의하세요.

## 초기 컨셉
{inputs['service_concept']}

## 타겟 유저 정보
{inputs['target_user']}

## Market Analyst 시장 분석 보고서
{inputs['market_analysis']}

### 수행 항목
1. **핵심 한 줄 정의**: "누가/어떤 상황에서/무엇을 위해 사용하는 서비스" 형식으로 1문장 작성
2. **JTBD 문장**: 주요 사용자 유형별로 각 1문장 작성
3. **핵심 Pain Point**: 3개 이상, 각 Pain Point에 수치 또는 행동 증거 포함 (Market Analyst 보고서 인용 필수)
4. **가치 제안**: 경쟁사 대비 차별점 명시
5. **USP**: 3문장 이내

### 주의사항
- "좋은 아이디어예요", "잘 될 것 같아요" 금지
- 모든 주장은 Market Analyst 보고서 데이터를 근거로 한다
- Pain Point는 구체적 수치 또는 사례 포함 필수
""",
        expected_output="""
섹션 1 완성본:

## 섹션 1. 서비스 컨셉 정의
### 핵심 한 줄 정의
[1문장]

### JTBD
- [사용자 유형 A]: "[상황]에서 [목표]를 달성하기 위해 이 서비스를 사용한다"

### 핵심 Pain Point
1. [Pain Point 1] — 근거: [수치/출처]
2. [Pain Point 2] — 근거: [수치/출처]
3. [Pain Point 3] — 근거: [수치/출처]

### 가치 제안
[경쟁 대비 차별점]

### USP
1. [USP 문장 1]
2. [USP 문장 2]
3. [USP 문장 3]
""",
        agent=agent,
    )


def _make_journey_task(agent: Agent, context: list[Task]) -> Task:
    """User Journey Map 작성 태스크를 생성한다.

    Args:
        agent: 담당 Journey 매퍼 에이전트.
        context: 이전 태스크 목록 (context chaining).

    Returns:
        설정된 CrewAI Task 인스턴스.
    """
    return Task(
        description="""
Task 1의 JTBD 분석 결과와 Market Analyst 보고서를 바탕으로
7단계 User Journey Map을 작성하세요.

### 필수 7단계
Awareness → Consideration → Purchase → Onboarding → Core Usage → Retention → Advocacy

### 각 단계별 필수 포함 항목
- **행동(Action)**: 사용자가 실제로 취하는 행동
- **Emotional State**: 구체적 감정 단어 (단순 "긍정/부정" 금지)
- **Pain Point**: 해당 단계에서 겪는 불편함
- **Opportunity**: 서비스가 해결할 수 있는 기회

### 주의사항
- 주요 사용자 유형별로 각각 작성
- 추상적 표현 금지 — 구체적 행동과 감정 단어 사용
""",
        expected_output="""
섹션 3 완성본 (각 사용자 유형별):

## 섹션 3. User Journey Map

| 단계 | Awareness | Consideration | Purchase | Onboarding | Core Usage | Retention | Advocacy |
|------|-----------|--------------|---------|------------|-----------|----------|---------|
| 행동 | | | | | | | |
| Emotional State | | | | | | | |
| Pain Point | | | | | | | |
| Opportunity | | | | | | | |
""",
        agent=agent,
        context=context,
    )


def _make_flow_task(agent: Agent, context: list[Task]) -> Task:
    """User Flow & IA 설계 태스크를 생성한다.

    Args:
        agent: 담당 Flow 설계자 에이전트.
        context: 이전 태스크 목록 (context chaining).

    Returns:
        설정된 CrewAI Task 인스턴스.
    """
    return Task(
        description="""
Task 2의 User Journey Map을 화면 단위 User Flow로 구체화하고
전체 Information Architecture(IA)를 설계하세요.

### 필수 작성 항목
1. **핵심 User Flow** (최소 3개): 회원가입/온보딩, 핵심 기능 사용, 결제/구독
2. **Conditional Flow**: 분기 조건(if/else) 명시
3. **Error Flow**: 실패 케이스 처리 경로
4. **Information Architecture**: 전체 메뉴 트리 구조

### 형식
- Flow: [화면] → [화면] → (조건: Y/N) → [화면A/화면B] 형식
- IA: 들여쓰기 트리 형식 (├── / └── 사용)
""",
        expected_output="""
섹션 4 완성본:

## 섹션 4. User Flow & Information Architecture

### 4.1 핵심 User Flow — [Flow명]
[화면 흐름도]

### 4.3 Conditional Flow — [조건명]
[분기 흐름도]

### 4.4 Error Flow — [에러명]
[에러 처리 흐름도]

### 4.5 Information Architecture
[메뉴 트리]
""",
        agent=agent,
        context=context,
    )


def _make_prioritization_task(agent: Agent, context: list[Task]) -> Task:
    """MoSCoW + RICE 기능 우선순위화 태스크를 생성한다.

    Args:
        agent: 담당 우선순위 분석 에이전트.
        context: 이전 태스크 목록 (context chaining).

    Returns:
        설정된 CrewAI Task 인스턴스.
    """
    return Task(
        description="""
앞선 분석 결과를 바탕으로 서비스 기능 전체를 MoSCoW로 분류하고
RICE Score를 계산해 우선순위화된 기능 명세표를 작성하세요.

### MoSCoW 기준
- **Must-have**: 이것 없으면 서비스 의미 없음 (5개 이상 필수)
- **Should-have**: 있으면 명확히 좋지만 MVP 없어도 됨
- **Could-have**: 여유가 있으면 추가
- **Won't-have**: 이번 버전에서는 하지 않음 (이유 명시 필수)

### RICE Score 계산 공식
RICE = (Reach × Impact × Confidence) / Effort
- Reach: 월간 영향받는 사용자 수 (숫자)
- Impact: 0.25 / 0.5 / 1 / 2 / 3
- Confidence: 확신도 (%)
- Effort: 개발 인월 (person-month)

### 주의사항
- "있으면 좋을 것 같아서" 이유로는 Must-have 불가
- Won't-have 이유는 구체적으로 명시
""",
        expected_output="""
섹션 5 완성본:

## 섹션 5. 기능 요구사항 명세 (MoSCoW + RICE)

### Must-have (필수)
| 기능 | 설명 | Reach | Impact | Confidence | Effort | RICE Score | 근거 |
|------|------|-------|--------|-----------|--------|-----------|------|

### Should-have (중요)
| 기능 | 설명 | Reach | Impact | Confidence | Effort | RICE Score | 근거 |
|------|------|-------|--------|-----------|--------|-----------|------|

### Could-have (선택)
| 기능 | 설명 | Reach | Impact | Confidence | Effort | RICE Score | 근거 |
|------|------|-------|--------|-----------|--------|-----------|------|

### Won't-have (제외)
| 기능 | 제외 이유 |
|------|---------|
""",
        agent=agent,
        context=context,
    )


def _make_mvp_task(agent: Agent, context: list[Task]) -> Task:
    """MVP 정의 & Phase 로드맵 태스크를 생성한다.

    Args:
        agent: 담당 MVP 설계 에이전트.
        context: 이전 태스크 목록 (context chaining).

    Returns:
        설정된 CrewAI Task 인스턴스.
    """
    return Task(
        description="""
Task 4의 우선순위화 결과를 바탕으로 MVP를 정의하고 Phase별 로드맵을 수립하세요.

### MVP 정의 기준
- Must-have 기능 중 핵심 가치 검증에 필요한 최소 세트 (3~5개)
- 각 기능의 MVP 포함 이유를 명시

### 검증 지표
- 정량 목표 수치 필수 (예: "DAU X명", "전환율 Y%")
- Go/No-Go 기준 명시 (숫자 기반)

### Phase 로드맵
- Phase 1 (MVP): 기간 + 주요 기능 + 목표
- Phase 2 (Iteration): 기간 + 주요 기능 + 목표
- Phase 3 (Scale): 기간 + 주요 기능 + 목표
""",
        expected_output="""
섹션 6 완성본:

## 섹션 6. MVP 정의 & Phase별 로드맵

### MVP 핵심 기능 세트
1. [기능명] — 포함 이유: [이유]

### MVP 검증 지표 & 성공 기준
| 지표 | 측정 방법 | 목표 | Go 기준 |
|-----|---------|------|--------|

### Phase별 로드맵
| Phase | 기간 | 주요 기능 | 목표 |
|-------|------|---------|------|
| Phase 1 (MVP) | X개월 | | |
| Phase 2 (Iteration) | X개월 | | |
| Phase 3 (Scale) | X개월 | | |
""",
        agent=agent,
        context=context,
    )


def _make_prd_task(agent: Agent, context: list[Task]) -> Task:
    """PRD 통합 보고서 작성 태스크를 생성한다.

    Args:
        agent: 담당 PRD 작성 에이전트.
        context: 이전 태스크 목록 (context chaining).

    Returns:
        설정된 CrewAI Task 인스턴스.
    """
    return Task(
        description="""
Task 1~5의 모든 결과물을 통합해 완전한 서비스 기획 보고서를 작성하세요.

### 필수 포함 섹션 (순서 변경 불가)
섹션 1. 서비스 컨셉 정의 (JTBD + 가치 제안)
섹션 2. 타겟 사용자 페르소나 (표 형식, JTBD 연결)
섹션 3. User Journey Map
섹션 4. User Flow & IA
섹션 5. 기능 요구사항 명세 (MoSCoW + RICE)
섹션 6. MVP 정의 & Phase 로드맵
섹션 7. Market Analyst 연동 기록
섹션 8. Change Log

### 출력 전 자가 검증 체크리스트 (12개 항목)
- [ ] 섹션 1~6 모두 포함 / [ ] 섹션 순서 1→6 준수
- [ ] 모든 수치에 근거 명시 / [ ] Pain Point 3개 이상
- [ ] 페르소나 2개 이상 / [ ] User Journey 7단계
- [ ] User Flow 3개 이상 / [ ] MoSCoW 4분류 + RICE Score
- [ ] Must-have 5개 이상 / [ ] MVP 검증 지표 수치 명시
- [ ] Phase 1~3 로드맵 / [ ] 금지 표현 미포함

12개 항목 모두 통과한 경우에만 최종 출력한다.
""",
        expected_output=(
            "output_format.md의 형식을 완전히 준수한 서비스 기획 보고서 전문. "
            "섹션 1~8이 순서대로 포함되고, 12개 검증 항목이 모두 통과된 상태."
        ),
        agent=agent,
        context=context,
    )


def _make_prototype_task(agent: Agent, context: list[Task]) -> Task:
    """프로토타입 & 검증 계획 태스크를 생성한다.

    Args:
        agent: 담당 프로토타입 전략 에이전트.
        context: 이전 태스크 목록 (context chaining).

    Returns:
        설정된 CrewAI Task 인스턴스.
    """
    return Task(
        description="""
기획 보고서를 기반으로 프로토타입 계획과 사용자 검증 계획을 수립하세요.

### 프로토타입 계획
1. **Low-fidelity**: Miro/Figma 와이어프레임 대상 화면 목록
2. **High-fidelity**: 실제 디자인 시안 필요 화면 목록
3. **UX/UI Designer 전달 사항**: 각 화면의 핵심 UX 요구사항

### 사용자 검증 계획
- 테스트 대상: 인원, 프로필
- 테스트 방법론: 사용성 테스트, A/B 테스트, 인터뷰 등
- 검증 시나리오: 핵심 Task 3개 이상
- 성공 지표: 태스크 완료율, 에러율, NPS

### Tech Lead 전달 사항
- Feasibility 검토 요청 항목
- 기술 구현 우선순위 논의 포인트
""",
        expected_output="""
섹션 9~11 완성본:

## 섹션 9. 프로토타입 계획
### Low-fidelity 대상 화면 / ### High-fidelity 대상 화면
### UX/UI Designer 전달 사항

## 섹션 10. 사용자 검증 계획
### 테스트 대상 / ### 검증 시나리오 / ### 성공 지표

## 섹션 11. Tech Lead 전달 사항
""",
        agent=agent,
        context=context,
    )


def create_tasks(agents: dict[str, Any], inputs: dict[str, str]) -> list[Task]:
    """7개 순차 태스크를 생성한다.

    Args:
        agents: planner_agents.build_all_agents()가 반환한 에이전트 딕셔너리.
        inputs: service_concept, target_user, market_analysis 키를 포함한 딕셔너리.

    Returns:
        실행 순서대로 정렬된 Task 리스트.
    """
    logger.info("7개 순차 태스크 생성 시작")

    task_jtbd = _make_jtbd_task(agents["jtbd_analyst"], inputs)
    task_journey = _make_journey_task(agents["journey_mapper"], [task_jtbd])
    task_flow = _make_flow_task(agents["flow_architect"], [task_jtbd, task_journey])
    task_priority = _make_prioritization_task(
        agents["prioritization_agent"],
        [task_jtbd, task_journey, task_flow],
    )
    task_mvp = _make_mvp_task(
        agents["mvp_designer"],
        [task_jtbd, task_journey, task_flow, task_priority],
    )
    task_prd = _make_prd_task(
        agents["prd_writer"],
        [task_jtbd, task_journey, task_flow, task_priority, task_mvp],
    )
    task_prototype = _make_prototype_task(
        agents["prototype_strategist"],
        [task_jtbd, task_journey, task_flow, task_priority, task_mvp, task_prd],
    )

    logger.info("7개 태스크 생성 완료")
    return [
        task_jtbd,
        task_journey,
        task_flow,
        task_priority,
        task_mvp,
        task_prd,
        task_prototype,
    ]
