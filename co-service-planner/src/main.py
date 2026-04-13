#!/usr/bin/env python3
"""Service Planner Agent CLI 진입점.

사용법:
  python -m src.main
  python -m src.main --model claude-3-opus-20240229

Market Analyst 보고서 없이는 기획을 시작하지 않는다.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

_REQUIRED_MARKET_KEYWORDS = ["페르소나", "Pain Point", "경쟁", "USP", "BM"]

_SECTION_PROJECT = "[프로젝트명]"
_SECTION_CONCEPT = "[초기 컨셉]"
_SECTION_USER = "[타겟 유저]"
_SECTION_MARKET = "[시장 분석 보고서]"
_SECTIONS = [_SECTION_PROJECT, _SECTION_CONCEPT, _SECTION_USER, _SECTION_MARKET]

_BANNER = """
================================================================
  Service Planner Agent — 서비스 기획자
  15년차 시니어 서비스 기획자가 시장 검증된 기획을 제공합니다
================================================================
"""


def _validate_api_key(provider: str) -> None:
    """provider에 맞는 API 키 설정 여부를 검증한다.

    Args:
        provider: LLM 제공자. "anthropic" 또는 "openai".

    Raises:
        SystemExit: API 키가 없을 경우 종료.
    """
    if provider == "anthropic" and not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print("[오류] .env 파일에 ANTHROPIC_API_KEY=your-key-here 를 추가하세요.")
        sys.exit(1)

    if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("[오류] .env 파일에 OPENAI_API_KEY=your-key-here 를 추가하세요.")
        sys.exit(1)



def _parse_input(raw: str) -> dict[str, str]:
    """섹션 마커를 기준으로 원본 입력을 파싱한다.

    Args:
        raw: 사용자가 붙여넣은 전체 텍스트.

    Returns:
        "project_name", "service_concept", "target_user", "market_analysis"
        키를 포함한 딕셔너리.

    Raises:
        ValueError: 필수 섹션 마커가 없을 경우.
    """
    missing = [s for s in _SECTIONS if s not in raw]
    if missing:
        raise ValueError(f"필수 섹션이 없습니다: {', '.join(missing)}")

    def _extract(start_marker: str, end_marker: str | None) -> str:
        start = raw.index(start_marker) + len(start_marker)
        end = raw.index(end_marker) if end_marker else len(raw)
        return raw[start:end].strip().lstrip("-* \t")

    return {
        "project_name": _extract(_SECTION_PROJECT, _SECTION_CONCEPT),
        "service_concept": _extract(_SECTION_CONCEPT, _SECTION_USER),
        "target_user": _extract(_SECTION_USER, _SECTION_MARKET),
        "market_analysis": _extract(_SECTION_MARKET, None),
    }


def _validate_market_analysis(market_analysis: str) -> bool:
    """Market Analyst 보고서의 최소 요건을 검증한다.

    Args:
        market_analysis: 검증할 보고서 문자열.

    Returns:
        필수 키워드가 모두 포함된 경우 True, 아니면 False.
    """
    missing = [kw for kw in _REQUIRED_MARKET_KEYWORDS if kw not in market_analysis]

    if missing:
        logger.warning("Market Analyst 보고서에 누락된 항목: %s", missing)
        print("\n[경고] Market Analyst 보고서에 다음 필수 항목이 누락되었습니다:")
        for kw in missing:
            print(f"  - {kw}")
        print(
            "\n기획을 시작하려면 위 항목이 모두 포함되어야 합니다. "
            "Market Analyst에게 보고서 보완을 요청하세요.\n"
        )
        return False

    return True


def _parse_args() -> argparse.Namespace:
    """CLI 인자를 파싱한다.

    Returns:
        파싱된 Namespace 객체.
    """
    parser = argparse.ArgumentParser(
        description="Service Planner Agent — 시장 검증된 서비스 기획을 자동으로 수행합니다."
    )
    parser.add_argument(
        "input_file",
        help="입력 파일 경로 (섹션 마커 형식의 .md 파일)",
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai"],
        default="anthropic",
        help="LLM 제공자 (기본값: anthropic)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="모델명 (기본값: anthropic=claude-3-opus-20240229, openai=gpt-4o)",
    )
    return parser.parse_args()


def main() -> None:
    """Service Planner Agent CLI 메인 함수."""
    args = _parse_args()
    _validate_api_key(args.provider)

    print(_BANNER)

    input_path = args.input_file
    try:
        raw = open(input_path, encoding="utf-8").read()
    except OSError as e:
        logger.error("파일 읽기 실패: %s", e)
        print(f"[오류] 파일을 읽을 수 없습니다: {input_path}")
        sys.exit(1)

    try:
        inputs = _parse_input(raw)
    except ValueError as e:
        logger.error("입력 파싱 실패: %s", e)
        print(f"\n[오류] {e}")
        print("파일에 [프로젝트명], [초기 컨셉], [타겟 유저], [시장 분석 보고서] 섹션이 모두 있어야 합니다.")
        sys.exit(1)

    for field, label in [
        ("project_name", "프로젝트명"),
        ("service_concept", "초기 컨셉"),
        ("target_user", "타겟 유저"),
        ("market_analysis", "시장 분석 보고서"),
    ]:
        if not inputs[field]:
            logger.error("%s 미입력", label)
            print(f"[오류] '{label}' 내용이 비어 있습니다.")
            sys.exit(1)

    if not _validate_market_analysis(inputs["market_analysis"]):
        confirm = input("그래도 계속 진행하시겠습니까? (y/N): ").strip().lower()
        if confirm != "y":
            logger.info("사용자가 기획 중단 선택")
            print("기획을 중단합니다. Market Analyst 보고서를 보완 후 다시 시도해주세요.")
            sys.exit(0)

    logger.info("모든 입력 확인 완료, 기획 실행")
    print("\n모든 입력이 확인되었습니다. 기획을 시작합니다...\n")

    from src.crew import run_crew

    run_crew(
        project_name=inputs["project_name"],
        service_concept=inputs["service_concept"],
        target_user=inputs["target_user"],
        market_analysis=inputs["market_analysis"],
        provider=args.provider,
        model=args.model,
    )


if __name__ == "__main__":
    main()
