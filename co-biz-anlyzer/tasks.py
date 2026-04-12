"""
tasks.py — 7개 분석 태스크 정의
SKILL.md의 7단계 분석 방법론을 태스크로 구현
Sequential Process로 실행 — 각 태스크의 결과가 다음 태스크의 context로 전달됨
"""

from crewai import Task


def create_tasks(concept: str, target_user: str, agents: dict) -> list[Task]:
  """
  초기 컨셉과 타겟 유저를 입력받아 7개 분석 태스크를 생성한다.
  태스크는 반드시 1→2→3→4→5→6→7 순서로 실행된다.
  """

  # ── Step 1: 타겟 사용자 페르소나 & Pain Point 도출 ──────────────────────────
  task_persona = Task(
    description=(
      f"다음 비즈니스 아이디어에 대한 타겟 사용자 페르소나와 Pain Point를 분석하라.\n\n"
      f"**초기 컨셉**: {concept}\n"
      f"**타겟 유저 가설**: {target_user}\n\n"
      "반드시 아래 규칙을 준수하라:\n"
      "1. JTBD(Jobs-to-be-Done) 프레임워크를 사용해 페르소나 2~3개를 생성한다.\n"
      "   - 각 페르소나에 이름, 연령, 직업, 생활 패턴, 디지털 행동을 포함한다.\n"
      "   - JTBD 문장 형식: '나는 ___ 할 때, ___ 하고 싶다. 왜냐하면 ___'\n"
      "2. Pain Point를 감정적·기능적·사회적으로 분류해 4~6개 도출한다.\n"
      "3. 각 Pain Point는 실제 사례나 수치로 구체화한다.\n"
      "4. '좋은 아이디어', '혁신적' 같은 모호한 표현은 절대 사용하지 않는다.\n"
      "5. 한국 시장 현실(규제, 소비자 행동, 트렌드)을 기반으로 분석한다."
    ),
    expected_output=(
      "## 1. 타겟 사용자 페르소나\n\n"
      "**페르소나 1~3**: 이름/연령/직업/생활 패턴/디지털 행동/JTBD 문장\n\n"
      "**Pain Points 테이블** (감정적/기능적/사회적 분류, 4~6개, 각 항목에 구체적 수치 또는 사례 포함)"
    ),
    agent=agents["user_researcher"],
  )

  # ── Step 2: 시장 분석 ──────────────────────────────────────────────────────
  task_market = Task(
    description=(
      f"다음 비즈니스 아이디어의 시장을 분석하라.\n\n"
      f"**초기 컨셉**: {concept}\n"
      f"**타겟 유저**: {target_user}\n\n"
      "반드시 아래 규칙을 준수하라:\n"
      "1. TAM/SAM/SOM을 구체적인 숫자로 산정하고 근거를 명시한다.\n"
      "2. 한국 시장 트렌드 + 글로벌 트렌드를 동시에 분석한다.\n"
      "3. PESTLE(Political/Economic/Social/Technological/Legal/Environmental) 분석을 수행한다.\n"
      "4. SWOT(Strengths/Weaknesses/Opportunities/Threats) 분석을 수행한다.\n"
      "5. 최신 시장 데이터 또는 유사 사례를 반드시 인용한다.\n"
      "6. 근거 없는 낙관적 수치는 절대 제시하지 않는다."
    ),
    expected_output=(
      "## 2. 시장 분석 & Pain Points\n\n"
      "**시장 규모**: TAM/SAM/SOM (각 숫자 + 근거)\n\n"
      "**주요 트렌드**: 한국 시장 + 글로벌 트렌드 각 3가지 이상\n\n"
      "**SWOT 매트릭스**: 4개 항목 모두 작성\n\n"
      "**PESTLE 분석**: 6개 요인 각각 한국 시장 기준으로 분석"
    ),
    agent=agents["market_analyst"],
    context=[task_persona],
  )

  # ── Step 3: 경쟁사 분석 ────────────────────────────────────────────────────
  task_competitive = Task(
    description=(
      f"다음 비즈니스 아이디어의 경쟁 환경을 분석하라.\n\n"
      f"**초기 컨셉**: {concept}\n\n"
      "반드시 아래 규칙을 준수하라:\n"
      "1. 직접 경쟁사 3개 + 간접 경쟁사 2개 + 대체재(Substitutes) 1~2개를 포함한다.\n"
      "2. 각 경쟁사의 강점·약점·BM·가격 전략을 테이블로 정리한다.\n"
      "3. Value Curve를 사용해 경쟁사 대비 차별화 포인트를 시각적으로 분석한다.\n"
      "   - 우리가 높이는 요소 vs 낮추는 요소를 명확히 서술한다.\n"
      "4. '우리만 할 수 있는 것'을 최소 1개 이상 명확히 도출한다.\n"
      "5. 실제 경쟁사명과 데이터를 기반으로 분석한다. 가상의 경쟁사는 사용하지 않는다."
    ),
    expected_output=(
      "## 3. 경쟁사 분석 & USP (경쟁사 파트)\n\n"
      "**경쟁사 분석 테이블**: 구분(직접/간접/대체재)/경쟁사명/강점/약점/BM/가격 전략\n\n"
      "**Value Curve**: 우리가 높이는 요소 / 낮추는 요소 서술\n\n"
      "**우리만 할 수 있는 것**: 핵심 차별화 포인트 명시"
    ),
    agent=agents["competitive_intel"],
    context=[task_persona, task_market],
  )

  # ── Step 4: USP 설계 ───────────────────────────────────────────────────────
  task_usp = Task(
    description=(
      f"다음 비즈니스 아이디어의 USP(Unique Selling Proposition)를 설계하라.\n\n"
      f"**초기 컨셉**: {concept}\n\n"
      "반드시 아래 규칙을 준수하라:\n"
      "1. USP를 3문장 이내로 명확히 정의한다. 모호한 표현은 절대 사용하지 않는다.\n"
      "2. 경쟁사 분석의 Value Curve를 활용해 차별화를 설명한다.\n"
      "3. '왜 고객이 우리를 선택해야 하는가?'를 고객 관점에서 3가지 이상 구체적으로 제시한다.\n"
      "   - 각 이유에 반드시 수치 또는 구체적 사례를 포함한다.\n"
      "4. '혁신적', '최고의' 같은 추상적 표현은 절대 사용하지 않는다."
    ),
    expected_output=(
      "## 3. 경쟁사 분석 & USP (USP 파트)\n\n"
      "**우리 USP**: 3문장 이내의 명확한 USP 문장\n\n"
      "**고객 선택 이유**: 3가지 이상, 각 항목에 수치 또는 사례 포함"
    ),
    agent=agents["value_prop"],
    context=[task_competitive],
  )

  # ── Step 5: 비즈니스 모델 기획 ─────────────────────────────────────────────
  task_bm = Task(
    description=(
      f"다음 비즈니스 아이디어의 비즈니스 모델을 기획하라.\n\n"
      f"**초기 컨셉**: {concept}\n\n"
      "반드시 아래 규칙을 준수하라:\n"
      "1. 수익 모델 옵션 3가지를 제시하고 가장 현실적인 것을 1순위로 추천한다.\n"
      "   (구독, 수수료, 광고, 프리미엄, 하이브리드 등)\n"
      "2. Business Model Canvas 9블록을 모두 작성한다.\n"
      "   (핵심 파트너/핵심 활동/핵심 자원/가치 제안/고객 관계/채널/고객 세그먼트/비용 구조/수익 흐름)\n"
      "3. 가격 전략을 Tiered Pricing 또는 Usage-based 방식으로 구체적 금액과 함께 제시한다.\n"
      "4. Unit Economics를 반드시 계산한다: CAC, LTV, Payback Period, LTV/CAC 비율.\n"
      "5. 3가지 시나리오별 1년/3년 매출을 표로 정리한다: Best/Realistic/Conservative."
    ),
    expected_output=(
      "## 4. 비즈니스 모델 (BM)\n\n"
      "**추천 수익 모델**: 1순위 추천 + 이유\n\n"
      "**Business Model Canvas**: 9블록 테이블\n\n"
      "**가격 전략**: 티어별 가격 + 포함 기능\n\n"
      "**Unit Economics**: CAC/LTV/Payback Period/LTV:CAC 비율\n\n"
      "**3가지 시나리오**: Best/Realistic/Conservative × 1년/3년 매출 테이블"
    ),
    agent=agents["business_model"],
    context=[task_usp, task_market],
  )

  # ── Step 6: KPI & 비즈니스 목표 설정 ──────────────────────────────────────
  task_kpi = Task(
    description=(
      f"다음 비즈니스 아이디어의 KPI와 비즈니스 목표를 설정하라.\n\n"
      f"**초기 컨셉**: {concept}\n\n"
      "반드시 아래 규칙을 준수하라:\n"
      "1. North Star Metric을 1개 선정하고 선정 이유를 설명한다.\n"
      "2. Leading Indicator 3개 + Lagging Indicator 3개를 설정한다.\n"
      "3. 1년 목표와 3년 목표를 구체적인 숫자로 제시한다.\n"
      "4. OKR 형식으로 정리한다: Objective 1개 + Key Results 3개.\n"
      "5. 각 KPI에 현재 기준값, 1년 목표치, 3년 목표치를 명시한다.\n"
      "6. 앞서 분석된 BM 시나리오와 일관성 있는 수치를 사용한다."
    ),
    expected_output=(
      "## 5. KPI & 비즈니스 목표\n\n"
      "**North Star Metric**: 1개 + 선정 이유\n\n"
      "**1년/3년 목표**: 구체적 수치\n\n"
      "**KPI 테이블**: 지표명/유형(Leading/Lagging)/현재/1년 목표/3년 목표 (6개)\n\n"
      "**OKR**: Objective 1개 + Key Results 3개"
    ),
    agent=agents["kpi_strategy"],
    context=[task_bm],
  )

  # ── Step 7: Risk & 시나리오 플래닝 ───────────────────────────────────────
  task_risk = Task(
    description=(
      f"다음 비즈니스 아이디어의 리스크를 분석하라.\n\n"
      f"**초기 컨셉**: {concept}\n"
      f"**타겟 유저**: {target_user}\n\n"
      "반드시 아래 규칙을 준수하라:\n"
      "1. 주요 리스크 5~7개를 식별한다.\n"
      "2. 발생 확률(높음/중간/낮음) × 영향도(높음/중간/낮음) 매트릭스를 작성한다.\n"
      "3. 각 리스크별 Mitigation Plan + Contingency Plan을 구체적으로 제시한다.\n"
      "4. Best/Base/Worst Case 3년 재무 전망을 표로 정리한다."
    ),
    expected_output=(
      "## 6. Risk & 대응 전략\n\n"
      "**리스크 매트릭스**: 리스크/발생 확률/영향도/우선순위/Mitigation Plan/Contingency Plan (5~7개)\n\n"
      "**3년 재무 전망**: Best/Base/Worst × 1년차/2년차/3년차 매출 테이블"
    ),
    agent=agents["risk_manager"],
    context=[task_persona, task_market, task_competitive, task_usp, task_bm, task_kpi],
  )

  return [
    task_persona,
    task_market,
    task_competitive,
    task_usp,
    task_bm,
    task_kpi,
    task_risk,
  ]
