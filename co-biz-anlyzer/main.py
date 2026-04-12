"""
main.py — CLI 진입점
비즈니스 전략 분석 Multi-Agent 시스템 실행

사용법:
  python main.py --concept "AI 영어 회화 앱" --target "20~30대 직장인"
  python main.py --provider openai --model gpt-4o-mini --concept "..." --target "..."
  python main.py  # 인터랙티브 입력 모드
"""

import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_PROVIDERS = ("anthropic", "openai")

DEFAULT_MODELS = {
  "anthropic": "claude-sonnet-4-6",
  "openai": "gpt-4o",
}


def validate_env(provider: str) -> None:
  """선택한 provider에 필요한 환경변수 확인"""
  missing = []

  if provider == "anthropic" and not os.getenv("ANTHROPIC_API_KEY"):
    missing.append("ANTHROPIC_API_KEY")
  elif provider == "openai" and not os.getenv("OPENAI_API_KEY"):
    missing.append("OPENAI_API_KEY")

  if missing:
    print(f"❌ 환경변수 누락: {', '.join(missing)}")
    print("   .env.example을 복사하여 .env 파일을 생성하고 API 키를 입력하세요.")
    print("   cp .env.example .env")
    sys.exit(1)

  if not os.getenv("SERPER_API_KEY"):
    print("⚠️  SERPER_API_KEY 없음 — 웹 검색 없이 LLM 내장 지식으로만 분석합니다.")


def get_inputs_interactive() -> tuple[str, str]:
  """인터랙티브 모드로 입력 받기"""
  print("\n" + "=" * 60)
  print("  비즈니스 전략가 Multi-Agent 분석 시스템")
  print("=" * 60)
  print("\n분석할 비즈니스 아이디어를 입력하세요.\n")

  concept = input("📌 초기 컨셉 (제품/서비스 아이디어): ").strip()
  if not concept:
    print("❌ 초기 컨셉을 입력해야 합니다.")
    sys.exit(1)

  target_user = input("👤 타겟 유저 (대상 고객군 가설): ").strip()
  if not target_user:
    print("❌ 타겟 유저를 입력해야 합니다.")
    sys.exit(1)

  return concept, target_user


def main() -> None:
  parser = argparse.ArgumentParser(
    description="비즈니스 전략가 CrewAI Multi-Agent 분석 시스템",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=(
      "예시:\n"
      "  python main.py --concept 'AI 영어 회화 앱' --target '20~30대 직장인'\n"
      "  python main.py --provider openai --concept 'AI 영어 회화 앱' --target '20~30대 직장인'\n"
      "  python main.py --provider openai --model gpt-4o-mini --concept '...' --target '...'\n"
      "  python main.py  # 인터랙티브 입력 모드\n\n"
      "지원 provider:\n"
      "  anthropic  claude-sonnet-4-6 (기본값), claude-opus-4-6 등\n"
      "  openai     gpt-4o (기본값), gpt-4o-mini 등"
    ),
  )
  parser.add_argument("--concept", type=str, help="초기 컨셉 (제품/서비스 아이디어 설명)")
  parser.add_argument("--target", type=str, help="타겟 유저 (대상 고객군 초기 가설)")
  parser.add_argument(
    "--provider",
    type=str,
    choices=SUPPORTED_PROVIDERS,
    default="anthropic",
    help="LLM provider (기본값: anthropic)",
  )
  parser.add_argument(
    "--model",
    type=str,
    default=None,
    help="모델명 (기본값: provider별 자동 선택 — anthropic: claude-sonnet-4-6, openai: gpt-4o)",
  )
  args = parser.parse_args()

  provider = args.provider
  model = args.model

  validate_env(provider)

  # 입력값 결정: CLI 인자 우선, 없으면 인터랙티브 모드
  if args.concept and args.target:
    concept = args.concept.strip()
    target_user = args.target.strip()
  else:
    concept, target_user = get_inputs_interactive()

  resolved_model = model or DEFAULT_MODELS[provider]

  print("\n" + "=" * 60)
  print("  분석 시작")
  print("=" * 60)
  print(f"  컨셉   : {concept}")
  print(f"  타겟   : {target_user}")
  print(f"  Provider: {provider}")
  print(f"  모델   : {resolved_model}")
  print("=" * 60)
  print("\n7개 에이전트가 순서대로 분석을 수행합니다...\n")
  print("  Step 1: 타겟 사용자 페르소나 & Pain Point 분석")
  print("  Step 2: 시장 분석 (TAM/SAM/SOM + SWOT + PESTLE)")
  print("  Step 3: 경쟁사 분석 (직접/간접/대체재 + Value Curve)")
  print("  Step 4: USP 설계")
  print("  Step 5: 비즈니스 모델 기획 (BMC + Unit Economics)")
  print("  Step 6: KPI & 목표 설정 (OKR + North Star)")
  print("  Step 7: Risk & 시나리오 플래닝 → docs/decisions.md 저장")
  print()

  # CrewAI 임포트는 환경변수 로드 후 진행
  from crew import run_analysis

  try:
    result = run_analysis(concept=concept, target_user=target_user, provider=provider, model=model)

    print("\n" + "=" * 60)
    print("  분석 완료")
    print("=" * 60)
    print(result)
    print("\n✅ 분석 결과가 docs/decisions.md에 저장되었습니다.")

  except KeyboardInterrupt:
    print("\n\n분석이 중단되었습니다.")
    sys.exit(0)
  except Exception as e:
    print(f"\n❌ 분석 중 오류 발생: {e}")
    raise


if __name__ == "__main__":
  main()
