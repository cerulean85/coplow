"""UX 설계자 Agent 정의."""
from __future__ import annotations

import logging

from crewai import Agent

from src.config import load_rule, load_skill
from src.llm_factory import create_llm
from src.tools.file_tools import PRDFileReaderTool, PRDValidatorTool

logger = logging.getLogger(__name__)


def create_ux_designer_agent(model: str | None = None) -> Agent:
    """UX 설계자 Agent를 생성하고 반환한다.

    persona.md와 SKILL.md의 내용을 Agent의 role/goal/backstory에 주입하여
    일관된 UX 설계자 정체성과 스킬셋을 보장한다.

    Args:
        model: 사용할 LLM 모델명. None이면 환경변수 또는 기본값(claude-opus-4-6) 사용.

    Returns:
        설정이 완료된 CrewAI Agent 인스턴스.
    """
    llm = create_llm(model)

    persona = load_rule("persona.md")
    skills = load_skill("SKILL.md")

    backstory = f"""
{persona}

---

{skills}
""".strip()

    logger.info("UX 설계자 Agent 생성 완료")

    return Agent(
        role="UX 설계자 (UX Designer & UX Researcher)",
        goal=(
            "서비스 기획자가 제공한 PRD를 분석하여 정보 구조도(IA), 핵심 유저 플로우, "
            "화면 별 필수 UI 컴포넌트를 체계적으로 설계한다. "
            "사용자가 최소한의 인지 부하로 최대한 빠르고 만족스럽게 목표를 달성할 수 있도록 "
            "직관성·효율성·접근성·일관성을 최우선 원칙으로 삼는다."
        ),
        backstory=backstory,
        tools=[PRDFileReaderTool(), PRDValidatorTool()],
        llm=llm,
        verbose=True,
        memory=True,
        allow_delegation=False,
    )
