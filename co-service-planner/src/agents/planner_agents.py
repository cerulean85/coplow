#!/usr/bin/env python3
"""Service Planner Agent의 7개 CrewAI 에이전트 클래스 정의.

SKILL.md의 8가지 방법론을 7개 에이전트 클래스로 매핑:
  JTBDAnalystAgent       — JTBD Framework (스킬 #1)
  JourneyMapperAgent     — User Journey Mapping (스킬 #2)
  FlowArchitectAgent     — User Flow & IA (스킬 #3)
  PrioritizationAgent    — MoSCoW + RICE Scoring (스킬 #4)
  MVPDesignerAgent       — MVP 설계 (스킬 #5)
  PRDWriterAgent         — 실행 문서화 (스킬 #8)
  PrototypeStrategistAgent — 프로토타입 & 검증 계획 (스킬 #6)
"""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from typing import Optional

from crewai import Agent
from crewai.tools import BaseTool

logger = logging.getLogger(__name__)

# ── 공유 상수 ────────────────────────────────────────────────────────────────

_DEFAULT_ANTHROPIC_MODEL = "claude-3-opus-20240229"
_DEFAULT_OPENAI_MODEL = "gpt-4o"

_SERVICE_PLANNER_BACKSTORY = """
당신은 15년차 시니어 서비스 기획자이자 Product Manager(PM)입니다.
스타트업 0→1 런칭부터 대기업 디지털 트랜스포메이션까지 100여 건의 실전 경험을 보유했습니다.

핵심 원칙:
- 항상 Why → How → What 순서로 사고한다
- Desirability + Viability + Feasibility 3가지 렌즈를 동시에 적용한다
- 모든 주장은 Market Analyst 데이터 또는 사용자 증거를 근거로 한다
- 추상적·모호한 표현을 절대 사용하지 않는다
- MVP와 Iteration 중심으로 실행 가능한 기획만 제시한다
"""


# ── LLM 팩토리 ────────────────────────────────────────────────────────────────

def create_llm(
    provider: str = "anthropic",
    model: Optional[str] = None,
) -> str:
    """LLM 모델 식별자를 반환한다.

    CrewAI는 LiteLLM을 통해 모델명 문자열을 직접 처리한다.
    API 키는 환경변수에서 LiteLLM이 자동으로 읽는다.

    Args:
        provider: LLM 제공자. "anthropic" 또는 "openai".
        model: 모델명. None이면 제공자별 기본값 사용.

    Returns:
        LiteLLM 호환 모델 식별자 문자열.

    Raises:
        ValueError: API 키 미설정 또는 지원하지 않는 provider인 경우.
    """
    if provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        return model or _DEFAULT_ANTHROPIC_MODEL

    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        return model or _DEFAULT_OPENAI_MODEL

    raise ValueError(f"지원하지 않는 provider: '{provider}'. 'anthropic' 또는 'openai' 사용")


# ── 베이스 에이전트 ────────────────────────────────────────────────────────────

class BasePlannerAgent(ABC):
    """서비스 기획자 에이전트 추상 기반 클래스.

    모든 기획 에이전트는 이 클래스를 상속하고 `build()`를 구현해야 한다.
    """

    @abstractmethod
    def build(
        self,
        llm: str,
        tools: list[BaseTool],
    ) -> Agent:
        """CrewAI Agent 인스턴스를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """


# ── 에이전트 클래스 ────────────────────────────────────────────────────────────

class JTBDAnalystAgent(BasePlannerAgent):
    """JTBD Framework 기반 사용자 Job & Pain Point 분석 에이전트."""

    def build(self, llm: ChatAnthropic, tools: list[BaseTool]) -> Agent:
        """JTBD 분석 Agent를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """
        logger.debug("JTBDAnalystAgent 생성")
        return Agent(
            role="JTBD 분석가 (사용자 Job & Pain Point 전문가)",
            goal=(
                "Market Analyst 보고서를 기반으로 타겟 사용자의 핵심 Job(하고자 하는 일)과 "
                "Pain Point를 명확하게 정의하고, 서비스 컨셉과 가치 제안을 1문장으로 정리한다."
            ),
            backstory=(
                _SERVICE_PLANNER_BACKSTORY
                + "\n특히 JTBD(Jobs to be Done) Framework에 정통하며, "
                "사용자 인터뷰와 행동 데이터를 분석해 진짜 Pain Point를 발굴하는 전문가입니다."
            ),
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )


class JourneyMapperAgent(BasePlannerAgent):
    """7단계 User Journey Map 설계 에이전트."""

    def build(self, llm: ChatAnthropic, tools: list[BaseTool]) -> Agent:
        """User Journey 매퍼 Agent를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """
        logger.debug("JourneyMapperAgent 생성")
        return Agent(
            role="User Journey 매퍼 (여정 지도 설계 전문가)",
            goal=(
                "JTBD 분석 결과를 바탕으로 Awareness → Consideration → Purchase → Onboarding "
                "→ Core Usage → Retention → Advocacy 7단계 User Journey Map을 작성한다. "
                "각 단계별 행동, Emotional State, Pain Point, Opportunity를 구체적으로 명시한다."
            ),
            backstory=(
                _SERVICE_PLANNER_BACKSTORY
                + "\n사용자 심리와 행동 패턴을 Journey Map으로 시각화하는 데 탁월하며, "
                "각 터치포인트에서의 감정 변화와 기회를 정밀하게 포착합니다."
            ),
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )


class FlowArchitectAgent(BasePlannerAgent):
    """User Flow & Information Architecture 설계 에이전트."""

    def build(self, llm: ChatAnthropic, tools: list[BaseTool]) -> Agent:
        """User Flow & IA 설계 Agent를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """
        logger.debug("FlowArchitectAgent 생성")
        return Agent(
            role="User Flow & IA 설계자 (정보 구조 & 흐름 전문가)",
            goal=(
                "User Journey Map을 화면 단위 User Flow Diagram으로 구체화한다. "
                "메인 Flow, Conditional Flow(분기), Error Flow를 모두 설계하고, "
                "전체 Information Architecture(IA) 메뉴 트리 구조를 완성한다."
            ),
            backstory=(
                _SERVICE_PLANNER_BACKSTORY
                + "\n복잡한 서비스 흐름을 명확하고 직관적인 Flow Diagram과 IA로 정리하는 전문가입니다. "
                "개발팀과 디자인팀이 즉시 이해하고 실행할 수 있는 수준의 산출물을 만듭니다."
            ),
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )


class PrioritizationAgent(BasePlannerAgent):
    """MoSCoW + RICE Scoring 기능 우선순위화 에이전트."""

    def build(self, llm: ChatAnthropic, tools: list[BaseTool]) -> Agent:
        """기능 우선순위 분석 Agent를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """
        logger.debug("PrioritizationAgent 생성")
        return Agent(
            role="기능 우선순위 분석가 (MoSCoW + RICE 전문가)",
            goal=(
                "서비스의 모든 기능을 MoSCoW(Must/Should/Could/Won't)로 분류하고, "
                "각 기능에 RICE Score(Reach × Impact × Confidence / Effort)를 계산해 "
                "우선순위화된 기능 명세표를 작성한다. Must-have 기능은 5개 이상 포함."
            ),
            backstory=(
                _SERVICE_PLANNER_BACKSTORY
                + "\n기능의 사업적 가치와 개발 비용을 객관적으로 평가해 우선순위를 결정합니다. "
                "'있으면 좋을 것 같은' 기능은 반드시 Won't-have로 분류하고 그 이유를 명확히 설명합니다."
            ),
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )


class MVPDesignerAgent(BasePlannerAgent):
    """MVP 정의 및 Phase별 로드맵 설계 에이전트."""

    def build(self, llm: ChatAnthropic, tools: list[BaseTool]) -> Agent:
        """MVP 설계 Agent를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """
        logger.debug("MVPDesignerAgent 생성")
        return Agent(
            role="MVP 설계자 (최소 실행 가능 제품 전문가)",
            goal=(
                "우선순위 분석 결과를 바탕으로 Phase 1 MVP 핵심 기능 세트(3~5개)를 정의한다. "
                "MVP 검증 지표와 성공 기준(수치 기반 Go/No-Go)을 명시하고, "
                "Phase 1(MVP) → Phase 2(Iteration) → Phase 3(Scale) 로드맵을 작성한다."
            ),
            backstory=(
                _SERVICE_PLANNER_BACKSTORY
                + "\n완벽한 제품보다 빠른 검증을 우선시합니다. "
                "핵심 가치만으로 동작하는 최소 기능 세트를 정의하고, "
                "데이터 기반으로 다음 단계를 결정하는 Lean Startup 철학을 실천합니다."
            ),
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )


class PRDWriterAgent(BasePlannerAgent):
    """통합 PRD 문서 작성 에이전트."""

    def build(self, llm: ChatAnthropic, tools: list[BaseTool]) -> Agent:
        """PRD 작성 Agent를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """
        logger.debug("PRDWriterAgent 생성")
        return Agent(
            role="PRD 작성자 (실행 가능한 제품 명세 전문가)",
            goal=(
                "모든 기획 결과물을 통합해 개발·디자인·마케팅 팀이 즉시 실행할 수 있는 "
                "완전한 PRD(Product Requirements Document) 형식의 기획 보고서를 작성한다. "
                "output_format.md의 12개 검증 체크리스트를 모두 통과해야 한다."
            ),
            backstory=(
                _SERVICE_PLANNER_BACKSTORY
                + "\n실행 가능한 스펙 작성의 달인입니다. "
                "모호한 표현을 구체적 기준으로 변환하고, "
                "팀간 커뮤니케이션 비용을 최소화하는 정밀한 문서를 만듭니다."
            ),
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )


class PrototypeStrategistAgent(BasePlannerAgent):
    """프로토타입 계획 및 사용자 검증 전략 에이전트."""

    def build(self, llm: ChatAnthropic, tools: list[BaseTool]) -> Agent:
        """프로토타입 전략 Agent를 생성한다.

        Args:
            llm: 사용할 LLM 인스턴스.
            tools: 에이전트에 제공할 도구 목록.

        Returns:
            설정된 CrewAI Agent 인스턴스.
        """
        logger.debug("PrototypeStrategistAgent 생성")
        return Agent(
            role="프로토타입 전략가 (검증 계획 전문가)",
            goal=(
                "Low-fidelity → High-fidelity 프로토타입 설계 계획을 수립한다. "
                "사용자 테스트 시나리오, 성공 지표, 검증 방법론을 구체적으로 제시하고, "
                "UX/UI Designer와 개발팀에 전달할 핵심 화면 설계 요청 사항을 정의한다."
            ),
            backstory=(
                _SERVICE_PLANNER_BACKSTORY
                + "\n빠른 프로토타이핑과 사용자 검증 사이클을 통해 기획 리스크를 최소화합니다. "
                "Figma, Miro 등 도구 활용 경험을 바탕으로 실행 가능한 검증 계획을 수립합니다."
            ),
            llm=llm,
            tools=tools,
            verbose=True,
            allow_delegation=False,
        )


# ── 에이전트 팩토리 ────────────────────────────────────────────────────────────

def build_all_agents(
    llm: str,
    tools: list[BaseTool],
) -> dict[str, Agent]:
    """7개 서비스 기획 에이전트를 모두 생성한다.

    Args:
        llm: 공유할 LLM 인스턴스.
        tools: 공유할 도구 목록.

    Returns:
        에이전트 이름을 키로 하는 Agent 인스턴스 딕셔너리.
    """
    agent_classes: dict[str, BasePlannerAgent] = {
        "jtbd_analyst": JTBDAnalystAgent(),
        "journey_mapper": JourneyMapperAgent(),
        "flow_architect": FlowArchitectAgent(),
        "prioritization_agent": PrioritizationAgent(),
        "mvp_designer": MVPDesignerAgent(),
        "prd_writer": PRDWriterAgent(),
        "prototype_strategist": PrototypeStrategistAgent(),
    }
    return {name: cls.build(llm, tools) for name, cls in agent_classes.items()}
