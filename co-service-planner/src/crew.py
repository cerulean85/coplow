#!/usr/bin/env python3
"""Service Planner Agent Crew 조립 및 기획 실행 모듈.

build_crew(): 에이전트 + 태스크를 CrewAI Crew로 조립한다.
run_crew(): 기획을 실행하고 docs/decisions.md에 자동 저장한다.
"""

from __future__ import annotations

import logging
from typing import Optional

from crewai import Crew, Process

from src.agents.planner_agents import build_all_agents, create_llm
from src.tasks.planner_tasks import create_tasks
from src.tools.planner_tools import SavePlanningTool, get_search_tool, update_progress

logger = logging.getLogger(__name__)


def build_crew(
    service_concept: str,
    target_user: str,
    market_analysis: str,
    provider: str = "anthropic",
    model: Optional[str] = None,
) -> Crew:
    """Service Planner Crew를 조립한다.

    Args:
        service_concept: 초기 서비스/제품 컨셉.
        target_user: 타겟 유저 정보.
        market_analysis: Market Analyst 시장 분석 보고서.
        provider: LLM 제공자. "anthropic" 또는 "openai".
        model: 모델명. None이면 제공자별 기본값 사용.

    Returns:
        실행 준비된 CrewAI Crew 인스턴스.
    """
    logger.info("Crew 조립 시작 (provider=%s)", provider)

    llm = create_llm(provider=provider, model=model)
    tools = [t for t in [get_search_tool(), SavePlanningTool()] if t is not None]
    agents = build_all_agents(llm=llm, tools=tools)

    inputs = {
        "service_concept": service_concept,
        "target_user": target_user,
        "market_analysis": market_analysis,
    }
    tasks = create_tasks(agents=agents, inputs=inputs)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=False,
    )

    logger.info("Crew 조립 완료 — 에이전트 %d개, 태스크 %d개", len(agents), len(tasks))
    return crew


def run_crew(
    project_name: str,
    service_concept: str,
    target_user: str,
    market_analysis: str,
    provider: str = "anthropic",
    model: Optional[str] = None,
) -> str:
    """서비스 기획 전체 사이클을 실행하고 결과를 저장한다.

    Args:
        project_name: 서비스/프로젝트 이름 (저장 시 제목으로 사용).
        service_concept: 초기 서비스/제품 컨셉.
        target_user: 타겟 유저 정보.
        market_analysis: Market Analyst 시장 분석 보고서.
        provider: LLM 제공자. "anthropic" 또는 "openai".
        model: 모델명. None이면 제공자별 기본값 사용.

    Returns:
        최종 기획 보고서 전문 (문자열).
    """
    logger.info("서비스 기획 시작: %s (provider=%s)", project_name, provider)

    crew = build_crew(
        service_concept=service_concept,
        target_user=target_user,
        market_analysis=market_analysis,
        provider=provider,
        model=model,
    )
    result = crew.kickoff()
    final_report = str(result)

    save_tool = SavePlanningTool()
    save_msg = save_tool._run(
        project_name=project_name,
        report_content=final_report,
    )
    logger.info(save_msg)

    update_msg = update_progress("examples/planning-example.md")
    logger.debug(update_msg)

    logger.info("기획 완료: %s", project_name)
    return final_report


if __name__ == "__main__":
    run_crew(
        project_name="테스트 프로젝트",
        service_concept="테스트 컨셉",
        target_user="테스트 유저",
        market_analysis="테스트 분석",
        provider="anthropic",
    )
