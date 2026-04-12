"""
agents.py — 7개 비즈니스 전략가 에이전트 정의
SKILL.md의 7단계 분석 방법론을 각 에이전트 역할로 매핑
모든 에이전트는 persona.md의 "냉철한 비즈니스 전략가" 성격을 공유
"""

from crewai import Agent, LLM
from tools import search_tool

# search_tool이 None이면 빈 리스트, 있으면 리스트로 래핑
_search_tools = [search_tool] if search_tool else []

# 지원 provider별 기본 모델
DEFAULT_MODELS = {
  "anthropic": "anthropic/claude-sonnet-4-6",
  "openai": "openai/gpt-4o",
}

COLD_ANALYST_BACKSTORY = (
  "너는 냉철한 분석가이며, USP와 BM 설계에 특화된 비즈니스 전략가다. "
  "너의 유일한 사명은 초기 아이디어를 실제 시장에서 돈을 벌 수 있는 실행 가능한 '사업'으로 전환하는 것이다. "
  "감상, 칭찬, 추상적인 조언은 절대 하지 않는다. "
  "모든 판단은 데이터, 시장 현실, 논리적 타당성을 기반으로 하며, 현실성 없는 부분은 가차 없이 지적한다. "
  "'좋은 아이디어예요', '잘 될 것 같아요' 같은 표현은 절대 사용하지 않는다."
)


def create_llm(provider: str, model: str | None = None) -> LLM:
  """
  provider와 model을 받아 CrewAI LLM 인스턴스를 반환한다.

  Args:
    provider: "anthropic" 또는 "openai"
    model: 모델명 (없으면 provider별 기본값 사용)
             - anthropic 예시: "claude-sonnet-4-6", "claude-opus-4-6"
             - openai 예시: "gpt-4o", "gpt-4o-mini"
  """
  if provider not in DEFAULT_MODELS:
    raise ValueError(f"지원하지 않는 provider: '{provider}'. 선택 가능: {list(DEFAULT_MODELS.keys())}")

  if model:
    # provider prefix가 없으면 자동으로 붙여줌
    prefix = f"{provider}/"
    resolved = model if model.startswith(prefix) else f"{prefix}{model}"
  else:
    resolved = DEFAULT_MODELS[provider]

  return LLM(model=resolved, temperature=0.1)


def create_agents(provider: str = "anthropic", model: str | None = None) -> dict:
  """
  7개 비즈니스 전략가 에이전트를 생성해 딕셔너리로 반환한다.

  Args:
    provider: "anthropic" 또는 "openai"
    model: 모델명 (없으면 provider별 기본값 사용)

  Returns:
    에이전트 딕셔너리 (키: 에이전트 식별자)
  """
  llm = create_llm(provider=provider, model=model)

  user_researcher = Agent(
    role="타겟 사용자 페르소나 분석가",
    goal=(
      "JTBD(Jobs-to-be-Done) 프레임워크를 사용해 2~3개의 구체적인 타겟 사용자 페르소나를 도출하고, "
      "감정적·기능적·사회적으로 분류된 4~6개의 Pain Point를 실제 사례와 수치로 구체화한다."
    ),
    backstory=COLD_ANALYST_BACKSTORY,
    llm=llm,
    tools=_search_tools,
    verbose=True,
    allow_delegation=False,
  )

  market_analyst = Agent(
    role="시장 분석가",
    goal=(
      "TAM/SAM/SOM을 구체적인 숫자와 근거로 산정하고, "
      "한국 시장과 글로벌 트렌드를 동시에 분석하며, "
      "PESTLE + SWOT을 조합해 기회와 위협을 명확히 도출한다."
    ),
    backstory=COLD_ANALYST_BACKSTORY,
    llm=llm,
    tools=_search_tools,
    verbose=True,
    allow_delegation=False,
  )

  competitive_intel = Agent(
    role="경쟁사 분석가",
    goal=(
      "직접 경쟁사 3개 + 간접 경쟁사 2개 + 대체재 1~2개를 분석하고, "
      "Value Curve 기반으로 차별화 포인트를 시각화하며, "
      "'우리만 할 수 있는 것'을 명확히 도출한다."
    ),
    backstory=COLD_ANALYST_BACKSTORY,
    llm=llm,
    tools=_search_tools,
    verbose=True,
    allow_delegation=False,
  )

  value_prop = Agent(
    role="USP 설계 전문가",
    goal=(
      "경쟁사 분석과 시장 데이터를 기반으로 USP를 3문장 이내로 명확히 정의하고, "
      "고객 관점에서 '왜 우리를 선택해야 하는가'를 3가지 이상 구체적으로 제시한다."
    ),
    backstory=COLD_ANALYST_BACKSTORY,
    llm=llm,
    tools=[],
    verbose=True,
    allow_delegation=False,
  )

  business_model = Agent(
    role="비즈니스 모델 기획자",
    goal=(
      "Business Model Canvas 9블록을 완전히 작성하고, "
      "Best/Realistic/Conservative 3가지 시나리오를 제시하며, "
      "CAC·LTV·Payback Period를 계산하고 가장 현실적인 수익 모델을 추천한다."
    ),
    backstory=COLD_ANALYST_BACKSTORY,
    llm=llm,
    tools=[],
    verbose=True,
    allow_delegation=False,
  )

  kpi_strategy = Agent(
    role="KPI 및 목표 설정 전문가",
    goal=(
      "North Star Metric 1개를 선정하고, "
      "Leading Indicator 3개 + Lagging Indicator 3개를 설정하며, "
      "1년/3년 목표를 구체적인 숫자로 제시하고 OKR 형식으로 정리한다."
    ),
    backstory=COLD_ANALYST_BACKSTORY,
    llm=llm,
    tools=[],
    verbose=True,
    allow_delegation=False,
  )

  risk_manager = Agent(
    role="리스크 및 시나리오 플래너",
    goal=(
      "주요 리스크 5~7개를 식별하고 발생 확률 × 영향도 매트릭스를 작성하며, "
      "각 리스크별 Mitigation Plan + Contingency Plan을 제시하고, "
      "Best/Base/Worst Case 3년 재무 전망을 표로 정리한 후 전체 분석 결과를 docs/decisions.md에 저장한다."
    ),
    backstory=COLD_ANALYST_BACKSTORY,
    llm=llm,
    tools=[],
    verbose=True,
    allow_delegation=False,
  )

  return {
    "user_researcher": user_researcher,
    "market_analyst": market_analyst,
    "competitive_intel": competitive_intel,
    "value_prop": value_prop,
    "business_model": business_model,
    "kpi_strategy": kpi_strategy,
    "risk_manager": risk_manager,
  }
