"""
tools.py — CrewAI 도구 정의
- SerperSearchTool: 웹 검색 (시장/경쟁사 데이터 수집)
- SaveDecisionsTool: 분석 결과를 docs/decisions.md에 자동 저장
"""

import os
from datetime import date
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# SerperAPI 웹 검색 도구 — SERPER_API_KEY가 있을 때만 활성화
# 없으면 None으로 설정하고, 에이전트는 LLM 내장 지식만으로 분석 수행
search_tool = None
if os.getenv("SERPER_API_KEY"):
  try:
    from crewai_tools import SerperDevTool
    search_tool = SerperDevTool()
  except Exception:
    search_tool = None


class SaveDecisionsInput(BaseModel):
  project_name: str = Field(..., description="분석 대상 프로젝트명 또는 아이디어 제목")
  content: str = Field(..., description="decisions.md에 저장할 전체 분석 보고서 내용 (Markdown 형식)")


class SaveDecisionsTool(BaseTool):
  name: str = "save_decisions"
  description: str = (
    "비즈니스 전략 분석이 완료된 후 전체 보고서를 docs/decisions.md 파일에 저장한다. "
    "반드시 분석의 마지막 단계에서 호출하며, 6섹션 전체 내용을 포함해야 한다."
  )
  args_schema: Type[BaseModel] = SaveDecisionsInput

  def _run(self, project_name: str, content: str) -> str:
    decisions_path = Path(__file__).parent / "docs" / "decisions.md"
    today = date.today().strftime("%Y-%m-%d")

    section = f"\n---\n\n### [{today}] - {project_name} 전략 분석 보고서\n\n{content}\n"

    try:
      with open(decisions_path, "a", encoding="utf-8") as f:
        f.write(section)
      return f"✅ 분석 보고서가 docs/decisions.md에 저장되었습니다. (날짜: {today}, 프로젝트: {project_name})"
    except Exception as e:
      return f"❌ 저장 실패: {e}"


save_decisions_tool = SaveDecisionsTool()
