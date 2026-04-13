"""PRD 파일 읽기 및 유효성 검사 커스텀 Tool."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PRDFileReaderInput(BaseModel):
    """PRD 파일 읽기 Tool 입력 스키마."""

    file_path: str = Field(description="읽을 PRD 파일의 절대 또는 상대 경로")


class PRDFileReaderTool(BaseTool):
    """파일 경로에서 PRD 내용을 읽어 반환하는 Tool."""

    name: str = "PRD 파일 리더"
    description: str = (
        "지정된 파일 경로에서 PRD(Product Requirements Document) 내용을 읽어 반환합니다. "
        "Markdown(.md) 또는 텍스트(.txt) 파일을 지원합니다."
    )
    args_schema: type[BaseModel] = PRDFileReaderInput

    def _run(self, file_path: str) -> str:
        """PRD 파일을 읽고 내용을 반환한다."""
        path = Path(file_path)
        if not path.exists():
            return f"[오류] 파일을 찾을 수 없습니다: {file_path}"
        if path.suffix not in {".md", ".txt", ".markdown"}:
            return f"[오류] 지원하지 않는 파일 형식입니다: {path.suffix} (지원: .md, .txt)"
        try:
            content = path.read_text(encoding="utf-8")
            logger.info(f"PRD 파일 로드 완료: {file_path} ({len(content)} 글자)")
            return content
        except Exception as e:
            return f"[오류] 파일 읽기 실패: {e}"


class PRDValidatorInput(BaseModel):
    """PRD 유효성 검사 Tool 입력 스키마."""

    prd_content: str = Field(description="유효성을 검사할 PRD 내용 문자열")


class PRDValidatorTool(BaseTool):
    """PRD 필수 항목 존재 여부를 검사하는 Tool."""

    name: str = "PRD 유효성 검사기"
    description: str = (
        "PRD 내용을 검사하여 UX 설계에 필요한 필수 항목(비즈니스 목표, 타겟 페르소나, "
        "기능 명세)이 존재하는지 확인하고 검증 결과를 반환합니다."
    )
    args_schema: type[BaseModel] = PRDValidatorInput

    # 필수 항목과 대응하는 탐지 키워드 목록
    _REQUIRED_SECTIONS: dict[str, list[str]] = {
        "비즈니스 목표": [
            "비즈니스 목표", "business goal", "목표", "goal", "kpi", "지표",
            "달성", "성공 지표",
        ],
        "타겟 사용자 페르소나": [
            "페르소나", "persona", "타겟 사용자", "target user", "사용자",
            "유저", "고객", "user",
        ],
        "기능 명세": [
            "기능", "feature", "기능 명세", "functional", "requirements",
            "f-0", "기능 목록", "주요 기능",
        ],
    }

    def _run(self, prd_content: str) -> str:
        """PRD 유효성을 검사하고 결과를 반환한다."""
        if not prd_content or not prd_content.strip():
            return "INVALID: PRD 내용이 비어 있습니다."

        content_lower = prd_content.lower()
        missing: list[str] = []
        found: list[str] = []

        for section, keywords in self._REQUIRED_SECTIONS.items():
            if any(kw.lower() in content_lower for kw in keywords):
                found.append(section)
            else:
                missing.append(section)

        if missing:
            missing_str = ", ".join(missing)
            found_str = ", ".join(found) if found else "없음"
            return (
                f"INCOMPLETE\n"
                f"- 누락 항목: {missing_str}\n"
                f"- 확인된 항목: {found_str}\n"
                f"- 총 글자 수: {len(prd_content)}"
            )

        return (
            f"VALID\n"
            f"- 확인된 항목: {', '.join(found)}\n"
            f"- 총 글자 수: {len(prd_content)}"
        )
