"""
crew.py — CrewAI Crew 조립 및 실행
7개 에이전트를 Sequential Process로 조립하여 실행
SKILL.md의 "1→2→3→4→5→6→7 순서 절대 준수" 규칙을 코드 레벨에서 강제
"""

from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks
from tools import save_decisions_tool


def build_crew(concept: str, target_user: str, provider: str = "anthropic", model: str | None = None) -> Crew:
  """
  비즈니스 전략 분석 Crew를 구성하여 반환한다.

  Args:
    concept: 초기 컨셉 (예: "AI로 개인화된 영어 회화 학습 앱")
    target_user: 타겟 유저 가설 (예: "20~30대 직장인, 영어 실력 향상을 원하지만 시간이 부족한 사람")
    provider: LLM provider — "anthropic" 또는 "openai"
    model: 모델명 (없으면 provider별 기본값 사용)

  Returns:
    실행 준비된 Crew 인스턴스
  """
  agents = create_agents(provider=provider, model=model)
  tasks = create_tasks(concept=concept, target_user=target_user, agents=agents)

  crew = Crew(
    agents=list(agents.values()),
    tasks=tasks,
    process=Process.sequential,  # 1→7 순서 강제 (SKILL.md 규칙 준수)
    verbose=True,
  )

  return crew


def run_analysis(concept: str, target_user: str, provider: str = "anthropic", model: str | None = None) -> str:
  """
  비즈니스 전략 분석을 실행하고 최종 결과를 반환한다.
  모든 태스크 출력을 수집해 docs/decisions.md에 저장한다.

  Returns:
    전체 분석 결과 문자열
  """
  crew = build_crew(concept=concept, target_user=target_user, provider=provider, model=model)
  crew.kickoff()

  # 각 태스크의 출력을 순서대로 수집해 하나의 보고서로 합산
  full_report = "\n\n".join(
    task.output.raw
    for task in crew.tasks
    if task.output and task.output.raw
  )

  save_decisions_tool._run(project_name=concept, content=full_report)

  return full_report
