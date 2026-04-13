"""UX 설계 6단계 Task 정의 (instructions.md 기반)."""
from __future__ import annotations

import logging

from crewai import Agent, Task

from src.config import load_rule

logger = logging.getLogger(__name__)


def create_tasks(
    agent: Agent,
    prd_content: str,
    service_name: str,
    output_dir: str = "outputs",
) -> list[Task]:
    """6단계 UX 설계 Task 목록을 생성한다.

    instructions.md의 Step 0~6을 각각의 Task로 구현하며,
    output_format.md와 examples.md를 Task 지침에 주입한다.

    Args:
        agent: 모든 Task를 수행할 UX 설계자 Agent.
        prd_content: 분석할 PRD 원문.
        service_name: 서비스명 (산출물 헤더에 사용).
        output_dir: 최종 산출물 저장 디렉토리.

    Returns:
        순서대로 실행될 Task 리스트.
    """
    output_format = load_rule("output_format.md")
    examples = load_rule("examples.md")

    # ── Task 0: PRD 유효성 검증 ──────────────────────────────────────────────
    task_validate = Task(
        description=f"""
당신은 UX 설계자입니다. 아래 PRD의 유효성을 검증하십시오.

## 검증 대상 PRD
---
{prd_content}
---

## 검증 기준 (instructions.md Step 0)
다음 필수 항목이 모두 존재하는지 확인하십시오:
1. 비즈니스 목표 (비즈니스 지표, KPI, 달성 목표 등)
2. 타겟 사용자 페르소나 (나이/직업/목표/Pain Point 등)
3. 기능 명세 (최소 1개 이상의 기능 정의)

## 출력 규칙
- **누락 항목이 있는 경우**: 아래 형식으로 PRD 보완 요청 메시지를 출력하고,
  마지막 줄에 반드시 `[STATUS: INCOMPLETE]` 를 기재하십시오.

{output_format}
(위 형식 중 "1. PRD 보완 요청 형식" 섹션을 참고하십시오.)

- **모든 항목이 충족된 경우**: 아래 형식으로 통과 메시지를 출력하십시오.
  ```
  ✅ PRD 유효성 검증 통과
  - 서비스명: [PRD에서 추출한 서비스명]
  - 확인된 항목: 비즈니스 목표, 타겟 페르소나, 기능 명세
  [STATUS: VALID]
  ```
""",
        expected_output=(
            "PRD 유효성 검증 결과. "
            "누락 항목이 있으면 '⚠️ PRD 보완 요청' 형식 + [STATUS: INCOMPLETE], "
            "통과 시 ✅ 메시지 + [STATUS: VALID]."
        ),
        agent=agent,
    )

    # ── Task 1: PRD 분석 및 사용자 목표 추출 ─────────────────────────────────
    task_analyze = Task(
        description=f"""
이전 태스크의 결과를 확인하십시오.

- `[STATUS: INCOMPLETE]` 가 포함된 경우:
  "⏭️ PRD 분석 건너뜀 — PRD 보완 요청이 선행되어야 합니다." 를 출력하고 종료하십시오.

- `[STATUS: VALID]` 가 포함된 경우:
  아래 PRD를 instructions.md Step 1 기준으로 분석하십시오.

## 분석 대상 PRD
---
{prd_content}
---

## 분석 결과 출력 형식

### 📋 PRD 분석 결과

#### 1. 비즈니스 목표
[목표 1~3개를 명확한 불릿으로 정리]

#### 2. 타겟 페르소나
| 페르소나 | 나이/직업 | 주요 목표 | 주요 Pain Point | 사용 환경 |
|---|---|---|---|---|
[표 형태로 정리, 주 타겟 페르소나를 맨 위에]

#### 3. 기능 명세 구조화
| 기능 ID | 기능명 | 설명 요약 | 우선순위 |
|---|---|---|---|
[MVP 기능 먼저, Post-MVP 기능은 하단에]

#### 4. 사용자 핵심 목표 (User Goals)
[각 MVP 기능에 대해 "나는 [행동]을 통해 [목표]를 달성하고 싶다" 형식으로 1문장씩]

#### 5. Pain Point & Opportunity
| Pain Point | UX Opportunity | 우선순위 |
|---|---|---|
[Pain Point → 개선 기회 매핑]

#### 6. UX 설계 방향 요약
[분석을 바탕으로 IA 및 User Flow 설계에서 가장 중요하게 고려할 사항 3~5개]
""",
        expected_output=(
            "구조화된 PRD 분석 결과: 비즈니스 목표, 페르소나 표, 기능 명세 표, "
            "사용자 목표 1문장 목록, Pain Point & Opportunity 표, UX 설계 방향 요약."
        ),
        agent=agent,
    )

    # ── Task 2: 정보 구조도(IA) 설계 ────────────────────────────────────────
    task_ia = Task(
        description=f"""
이전 PRD 분석 결과를 기반으로 정보 구조도(IA)를 설계하십시오.

`[STATUS: INCOMPLETE]` 가 이전 결과에 포함된 경우:
"⏭️ IA 설계 건너뜀 — PRD 보완 요청이 선행되어야 합니다." 를 출력하고 종료하십시오.

## IA 설계 원칙 (instructions.md Step 2)
- Top-down + Bottom-up 하이브리드 접근 (Card Sorting 시뮬레이션)
- 메인 네비게이션 3~5개 (Fitts' Law, 인지 부하 최소화)
- 계층 깊이: 최대 3~4 Depth
- 메인 / 서브 / 숨김 메뉴(설정, 더보기) 모두 포함
- 기능 수에 따른 Depth 결정:
  - 5개 이하 → 2 Depth
  - 6~15개 → 3 Depth
  - 16개 이상 → 4 Depth + 검색 기능 포함

## 출력 형식 (output_format.md의 "2. 정보 구조도(IA) 출력 형식" 100% 준수)
{output_format}

## 예시 참조
{examples}
(위 예시 중 "예시 1: 정보 구조도(IA)" 형식을 기준으로 삼되, 이 PRD 서비스에 맞게 재설계하십시오.)

## 출력 항목
1. Mermaid Mindmap 코드 블록 (```mermaid mindmap ... ```)
2. 계층형 텍스트 (├── 형식)
3. 네비게이션 유형 결정 및 근거 (Fitts' Law 등 UX 원칙 명시)
4. 총 Depth 및 주요 화면 수 요약
""",
        expected_output=(
            "완성된 정보 구조도(IA): Mermaid Mindmap 코드 블록 + 계층형 텍스트 + "
            "네비게이션 유형 및 근거 + Depth/화면 수 요약."
        ),
        agent=agent,
    )

    # ── Task 3: 핵심 유저 플로우 설계 ───────────────────────────────────────
    task_flow = Task(
        description=f"""
IA 설계 결과와 PRD 분석을 기반으로 핵심 유저 플로우를 설계하십시오.

`[STATUS: INCOMPLETE]` 가 이전 결과에 포함된 경우:
"⏭️ User Flow 설계 건너뜀 — PRD 보완 요청이 선행되어야 합니다." 를 출력하고 종료하십시오.

## 유저 플로우 설계 원칙 (instructions.md Step 3)
- Happy Path 중심으로 먼저 설계 (가장 일반적인 성공 경로)
- 최소 2개, 최대 5개 핵심 플로우 (MVP 기능 수 × 0.5 기준)
- 각 플로우 구성: Entry Point → [Decision Points] → Goal Achievement
- 각 Step: "사용자 액션 → 시스템 응답 → 상태/데이터 변화"
- Decision Point, Error Flow, Alternative Path 반드시 포함
- 화면 전환 시 필요한 데이터(파라미터) 간략 표기
- 최대 7 Steps 이내 (Miller's Law 7±2)

## 출력 형식 (output_format.md의 "3. 핵심 유저 플로우(User Flow) 출력 형식" 100% 준수)
{output_format}

## 예시 참조
{examples}
(위 예시 중 "예시 2: 핵심 유저 플로우" 형식 기준으로 이 PRD 서비스에 맞게 재설계하십시오.)

## 각 플로우별 출력 항목
1. 플로우 메타 정보 (대상 페르소나, 사용자 목표, Entry/Goal)
2. Mermaid Flowchart 코드 블록 (색상 구분: 시작=녹색, 종료=파란색, 오류=빨간색)
3. 단계별 설명 테이블 (Step | 화면 | 사용자 액션 | 시스템 응답 | 데이터 | 비고)
4. 오류 흐름 테이블
5. Alternative Path 테이블
""",
        expected_output=(
            "핵심 유저 플로우 (최소 2개): 각 플로우별 Mermaid Flowchart + "
            "단계별 설명 테이블 + 오류 흐름 + Alternative Path."
        ),
        agent=agent,
    )

    # ── Task 4: 화면 별 UI 컴포넌트 정의 ────────────────────────────────────
    task_components = Task(
        description=f"""
IA와 User Flow에서 도출된 주요 화면별 필수 UI 컴포넌트를 정의하십시오.

`[STATUS: INCOMPLETE]` 가 이전 결과에 포함된 경우:
"⏭️ UI 컴포넌트 정의 건너뜀 — PRD 보완 요청이 선행되어야 합니다." 를 출력하고 종료하십시오.

## UI 컴포넌트 정의 원칙 (instructions.md Step 4)
- Happy Path 기준 핵심 화면 최소 3개 정의
- 각 화면을 Atomic 단위로 분해:
  Header | Navigation | Content Area | CTA | Feedback | Footer
- 각 컴포넌트 필수 정의 항목:
  - 목적: 이 컴포넌트가 사용자에게 제공하는 가치
  - 상태: Enabled / Disabled / Loading / Empty / Error (해당 것만)
  - 필수 인터랙션: 탭, 스크롤, 스와이프, 입력 등
  - 접근성: ARIA label, 키보드 네비게이션, 색 대비
- 화면 당 CTA 1개 원칙 (취소/확인 쌍 예외)
- 컴포넌트 수 화면 당 최대 8~10개

## 출력 형식 (output_format.md의 "4. 화면 별 UI 컴포넌트 정의 출력 형식" 100% 준수)
{output_format}

## 예시 참조
{examples}
(위 예시 중 "예시 3: 화면 별 UI 컴포넌트 정의" 형식을 기준으로 이 PRD 서비스에 맞게 재정의하십시오.)

## 각 화면별 출력 항목
1. 화면 헤더 (화면 목적, 진입/이탈 경로, 플랫폼)
2. UI 컴포넌트 정의 Markdown Table
   (컴포넌트명 | 영역 | 목적 | 상태 | 필수 인터랙션 | 접근성 고려사항)
3. 레이아웃 가이드 (화면 구조, 여백, CTA 위치)
4. Empty State 가이드 (해당 화면에 빈 상태가 존재하는 경우)
5. 반응형 고려사항 (모바일/태블릿/데스크탑 분기 필요 시)
""",
        expected_output=(
            "주요 화면 최소 3개의 UI 컴포넌트 정의: 각 화면별 헤더 + "
            "컴포넌트 Markdown Table + 레이아웃 가이드 + Empty State 가이드."
        ),
        agent=agent,
    )

    # ── Task 5: Self-Review + 최종 산출물 통합 ───────────────────────────────
    task_review = Task(
        description=f"""
지금까지 생성된 모든 UX 설계 산출물(IA, User Flow, UI 컴포넌트)을 검토하고,
UX 원칙 Self-Review를 수행한 후, 최종 통합 산출물을 완성하십시오.

`[STATUS: INCOMPLETE]` 가 이전 결과에 포함된 경우:
"⏭️ Self-Review 건너뜀 — PRD 보완 요청으로 대화를 마무리합니다." 를 출력하고 종료하십시오.

## Self-Review 원칙 (instructions.md Step 5)
### 4대 설계 원칙 검증
- 직관성: 초보 사용자도 별도 학습 없이 사용 가능한가?
- 효율성: 목표 달성까지 최소 Steps인가? 불필요한 화면 전환은 없는가?
- 접근성: 색 대비, 텍스트 크기, 키보드 네비게이션, ARIA가 고려되었는가?
- 일관성: 동일 컴포넌트·레이블·인터랙션이 서비스 전체에서 일관되는가?

### Nielsen 10 Heuristics 체크
- #1~#10 각 항목에 대해 ✅/⚠️/❌ 평가 및 근거 제시

### 추가 원칙 검증
- Fitts' Law: CTA 버튼 크기(44px+) 및 위치 적절성
- Hick's Law: 화면 당 선택지 최대 5개 이하
- Gestalt: 시각적 그룹핑 및 계층 명확성

## 최종 산출물 구성 및 출력 형식

아래 순서로 완전한 최종 산출물을 출력하십시오:

---
서비스명: {service_name}
산출물 유형: 통합 UX 설계 산출물
Version: v1.0 (PRD v1.0 기준)
작성일: [오늘 날짜]
작성자: UX 설계자 Agent (ux_designer v1.0)
상태: Draft
---

# UX 설계 산출물 — {service_name}

## 1. PRD 분석 요약
[Task 1의 분석 결과 중 핵심 내용 요약]

## 2. 정보 구조도 (IA)
[Task 2의 IA 산출물 전체]

## 3. 핵심 유저 플로우
[Task 3의 모든 User Flow 전체]

## 4. 화면 별 UI 컴포넌트 정의
[Task 4의 모든 화면 컴포넌트 정의 전체]

## 5. UX 원칙 Self-Review
[output_format.md의 "5. Self-Review 체크리스트 출력 형식" 100% 준수]
{output_format}

## 6. 개선 제안 (선택)
[Self-Review에서 발견한 현재 버전 미반영 개선 사항]

---

## 예시 참조
{examples}
(위 예시 중 "예시 4: Self-Review 결과" 형식을 기준으로 삼으십시오.)
""",
        expected_output=(
            "완전한 최종 UX 설계 산출물: 공통 헤더 + PRD 분석 요약 + IA + "
            "User Flow 전체 + UI 컴포넌트 정의 전체 + Self-Review 체크리스트 + 개선 제안. "
            "output_format.md 기준 100% 준수."
        ),
        agent=agent,
        output_file=f"{output_dir}/ux_design_output.md",
    )

    logger.info("UX 설계 Task 6개 생성 완료")
    return [task_validate, task_analyze, task_ia, task_flow, task_components, task_review]
