"""UX 설계자 Agent — CLI 메인 실행 파일."""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

# 프로젝트 루트를 Python path에 추가 (src/ 내부에서 실행 시 필요)
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv

load_dotenv(_PROJECT_ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

BANNER = """
╔══════════════════════════════════════════════════════╗
║          UX 설계자 Agent  v1.0                       ║
║  PRD → IA + User Flow + UI 컴포넌트 자동 설계        ║
╚══════════════════════════════════════════════════════╝
"""


def parse_args() -> argparse.Namespace:
    """CLI 인자를 파싱하고 반환한다."""
    parser = argparse.ArgumentParser(
        prog="ux-designer",
        description="PRD를 입력으로 받아 정보 구조도(IA), 핵심 유저 플로우, UI 컴포넌트를 설계합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python src/main.py --prd docs/example_prd.md --service BookLog
  python src/main.py --prd my_prd.md
  python src/main.py  # 대화형 입력 모드
        """,
    )
    parser.add_argument(
        "--prd",
        type=str,
        default=None,
        metavar="FILE_PATH",
        help="PRD 파일 경로 (.md 또는 .txt). 미입력 시 표준 입력(stdin) 모드.",
    )
    parser.add_argument(
        "--service",
        type=str,
        default=None,
        metavar="SERVICE_NAME",
        help="서비스명 (미입력 시 PRD 파일명 또는 PRD 내용에서 자동 추출).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        metavar="DIR",
        help="산출물 저장 디렉토리 (기본값: outputs/).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        metavar="MODEL",
        help=(
            "사용할 LLM 모델 (기본값: 환경변수 LLM_MODEL 또는 anthropic/claude-opus-4-6). "
            "단축명 사용 가능: opus, sonnet, haiku, gpt-4o, gpt-4o-mini. "
            "--list-models 로 전체 목록 확인."
        ),
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="지원하는 LLM 모델 목록을 출력하고 종료.",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="docs/example_prd.md를 사용하여 데모 실행.",
    )
    return parser.parse_args()


def load_prd_from_file(file_path: str) -> tuple[str, str]:
    """파일에서 PRD 내용과 서비스명을 로드한다.

    Args:
        file_path: PRD 파일 경로.

    Returns:
        (prd_content, service_name) 튜플.

    Raises:
        SystemExit: 파일을 찾을 수 없거나 지원하지 않는 형식인 경우.
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"PRD 파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)
    if path.suffix not in {".md", ".txt", ".markdown"}:
        logger.error(f"지원하지 않는 파일 형식: {path.suffix} (지원: .md, .txt)")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    # 파일명에서 서비스명 추출 (snake_case → Title Case)
    service_name = path.stem.replace("_", " ").replace("-", " ").title()
    logger.info(f"PRD 파일 로드: {file_path} ({len(content):,} 글자)")
    return content, service_name


def load_prd_from_stdin() -> tuple[str, str]:
    """표준 입력(stdin)에서 PRD 내용을 읽는다.

    Returns:
        (prd_content, "Unknown Service") 튜플.

    Raises:
        SystemExit: 입력이 비어 있거나 취소된 경우.
    """
    print("\n📄 PRD 내용을 입력하세요.")
    print("   입력 완료 후 빈 줄에서 Ctrl+D (Mac/Linux) 또는 Ctrl+Z+Enter (Windows)를 누르세요.\n")

    try:
        lines = sys.stdin.readlines()
        content = "".join(lines).strip()
    except KeyboardInterrupt:
        print("\n\n입력이 취소되었습니다.")
        sys.exit(0)

    if not content:
        logger.error("PRD 내용이 비어 있습니다.")
        sys.exit(1)

    return content, "Unknown Service"


def _extract_service_name_from_prd(prd_content: str) -> str | None:
    """PRD 내용에서 서비스명을 간단히 추출 시도한다."""
    for line in prd_content.splitlines():
        line = line.strip()
        if line.startswith("**서비스명"):
            # "**서비스명**: BookLog" 형태 처리
            parts = line.split(":", 1)
            if len(parts) > 1:
                name = parts[1].strip().strip("*").strip()
                if name:
                    return name
        elif line.lower().startswith("# ") and "prd" not in line.lower():
            # 첫 번째 H1 제목을 서비스명으로 사용
            name = line.lstrip("# ").strip()
            if name:
                return name
    return None


def main() -> None:
    """메인 실행 함수."""
    print(BANNER)
    args = parse_args()

    # 모델 목록 출력 후 종료
    if args.list_models:
        from src.llm_factory import list_supported_models
        print(list_supported_models())
        sys.exit(0)

    # PRD 로드
    if args.example:
        example_path = _PROJECT_ROOT / "docs" / "example_prd.md"
        prd_content, service_name = load_prd_from_file(str(example_path))
        service_name = "BookLog"
    elif args.prd:
        prd_content, service_name = load_prd_from_file(args.prd)
        # PRD 내용에서 서비스명 추출 시도
        extracted = _extract_service_name_from_prd(prd_content)
        if extracted:
            service_name = extracted
    else:
        prd_content, service_name = load_prd_from_stdin()
        extracted = _extract_service_name_from_prd(prd_content)
        if extracted:
            service_name = extracted

    # CLI 인자로 서비스명을 명시한 경우 덮어쓰기
    if args.service:
        service_name = args.service

    # 사용 모델 확인 출력
    from src.llm_factory import _resolve_model
    effective_model = _resolve_model(args.model or os.getenv("LLM_MODEL") or "anthropic/claude-opus-4-6")

    print(f"🚀 서비스명: {service_name}")
    print(f"🤖 사용 모델: {effective_model}")
    print(f"📂 산출물 저장 경로: {args.output_dir}/ux_design_output.md")
    print(f"📝 PRD 분량: {len(prd_content):,} 글자")
    print("\n⏳ UX 설계를 시작합니다...\n")

    try:
        from src.crew import UXDesignerCrew

        crew_instance = UXDesignerCrew(
            prd_content=prd_content,
            service_name=service_name,
            model=args.model,
        )
        # output_dir 재설정
        crew_instance.OUTPUT_DIR = args.output_dir
        Path(args.output_dir).mkdir(exist_ok=True)

        result = crew_instance.run()

        print("\n" + "=" * 60)
        print("✅ UX 설계 완료!")
        print(f"📄 산출물 저장 완료: {args.output_dir}/ux_design_output.md")
        print("=" * 60)

        # 결과 미리보기 (첫 300자)
        preview = result.strip()[:300]
        if len(result) > 300:
            preview += "\n... (전체 내용은 산출물 파일을 확인하세요)"
        print(f"\n[결과 미리보기]\n{preview}")

    except KeyboardInterrupt:
        print("\n\n실행이 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"실행 중 오류 발생: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
