#!/usr/bin/env python3
"""Service Planner Agent 커스텀 도구 모듈.

SerperSearchTool: 웹 검색 (SERPER_API_KEY 설정 시 활성화)
SavePlanningTool: 완성된 기획 보고서를 docs/decisions.md에 저장
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

_DECISIONS_PATH = Path(__file__).parent.parent.parent / "docs" / "decisions.md"
_PROGRESS_PATH = Path(__file__).parent.parent.parent / "docs" / "progress.md"


def get_search_tool() -> Optional[SerperDevTool]:
    """SerperDevTool 반환.

    Returns:
        SERPER_API_KEY 환경변수가 설정된 경우 SerperDevTool 인스턴스,
        설정되지 않은 경우 None.
    """
    if os.getenv("SERPER_API_KEY"):
        logger.info("Serper 검색 도구 활성화")
        return SerperDevTool()
    logger.warning("SERPER_API_KEY 미설정 — 웹 검색 도구 비활성화")
    return None


class _SavePlanningInput(BaseModel):
    """SavePlanningTool 입력 스키마."""

    project_name: str = Field(description="서비스/프로젝트 이름")
    report_content: str = Field(description="기획 보고서 전체 내용 (Markdown)")


class SavePlanningTool(BaseTool):
    """완성된 서비스 기획 보고서를 docs/decisions.md에 저장하는 도구."""

    name: str = "save_planning_report"
    description: str = (
        "완성된 서비스 기획 보고서를 docs/decisions.md에 날짜·프로젝트명과 함께 저장합니다. "
        "PRD 작성자가 최종 보고서 완성 후 반드시 호출해야 합니다."
    )
    args_schema: type[BaseModel] = _SavePlanningInput

    def _run(self, project_name: str, report_content: str) -> str:
        """기획 보고서를 decisions.md에 append 저장.

        Args:
            project_name: 서비스/프로젝트 이름.
            report_content: 기획 보고서 전체 내용 (Markdown).

        Returns:
            저장 성공 또는 실패 메시지.
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            separator = "\n\n" + "=" * 60 + "\n"
            header = (
                f"## 기획 보고서: {project_name}\n"
                f"**작성일**: {today}\n"
                f"**버전**: v1.0\n\n"
            )
            entry = separator + header + report_content.strip() + "\n"

            with open(_DECISIONS_PATH, "a", encoding="utf-8") as f:
                f.write(entry)

            logger.info(f"기획 보고서 저장 완료: {project_name} ({today})")
            return f"[저장 완료] '{project_name}' 기획 보고서가 docs/decisions.md에 저장되었습니다. ({today})"

        except OSError as e:
            logger.error(f"decisions.md 저장 실패: {e}")
            return f"[저장 실패] decisions.md 쓰기 오류: {e}"


def update_progress(completed_item: str) -> str:
    """docs/progress.md에서 완료 항목을 [ ] → [x]로 업데이트.

    Args:
        completed_item: 완료된 항목 파일명 또는 태스크명 (예: "tools.py").

    Returns:
        업데이트 성공 또는 경고 메시지.
    """
    if not _PROGRESS_PATH.exists():
        logger.warning("progress.md 파일 없음")
        return "[경고] progress.md 파일을 찾을 수 없습니다."

    content = _PROGRESS_PATH.read_text(encoding="utf-8")
    updated = content.replace(f"[ ] **{completed_item}**", f"[x] **{completed_item}**")

    if updated == content:
        logger.warning(f"progress.md에서 '{completed_item}' 항목을 찾지 못함")
        return f"[경고] '{completed_item}' 항목을 progress.md에서 찾지 못했습니다."

    _PROGRESS_PATH.write_text(updated, encoding="utf-8")
    logger.info(f"progress.md 업데이트 완료: {completed_item}")
    return f"[업데이트 완료] progress.md에서 '{completed_item}' 항목이 완료 처리되었습니다."
