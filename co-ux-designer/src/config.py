"""프로젝트 설정 및 .claude/ 룰 파일 로더."""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# 프로젝트 루트: src/config.py 기준 상위 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent


def load_rule(filename: str) -> str:
    """`.claude/rules/` 디렉토리에서 파일을 읽어 반환한다.

    Args:
        filename: 읽을 파일명 (예: "persona.md")

    Returns:
        파일 내용 문자열. 파일이 없으면 경고 후 빈 문자열 반환.
    """
    path = PROJECT_ROOT / ".claude" / "rules" / filename
    if not path.exists():
        logger.warning(f"룰 파일을 찾을 수 없습니다: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def load_skill(filename: str) -> str:
    """`.claude/skills/` 디렉토리에서 파일을 읽어 반환한다.

    Args:
        filename: 읽을 파일명 (예: "SKILL.md")

    Returns:
        파일 내용 문자열. 파일이 없으면 경고 후 빈 문자열 반환.
    """
    path = PROJECT_ROOT / ".claude" / "skills" / filename
    if not path.exists():
        logger.warning(f"스킬 파일을 찾을 수 없습니다: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def load_doc(filename: str) -> str:
    """`docs/` 디렉토리에서 파일을 읽어 반환한다.

    Args:
        filename: 읽을 파일명 (예: "example_prd.md")

    Returns:
        파일 내용 문자열. 파일이 없으면 경고 후 빈 문자열 반환.
    """
    path = PROJECT_ROOT / "docs" / filename
    if not path.exists():
        logger.warning(f"문서 파일을 찾을 수 없습니다: {path}")
        return ""
    return path.read_text(encoding="utf-8")
