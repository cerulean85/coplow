"""LLM 인스턴스 생성 팩토리 — Anthropic / OpenAI 공급자 통합 지원."""
from __future__ import annotations

import logging
import os

from crewai import LLM

logger = logging.getLogger(__name__)

# 지원 공급자별 기본 모델 및 필요 환경변수
_PROVIDER_DEFAULTS: dict[str, dict[str, str]] = {
    "anthropic": {
        "default_model": "anthropic/claude-opus-4-6",
        "api_key_env": "ANTHROPIC_API_KEY",
    },
    "openai": {
        "default_model": "openai/gpt-4o",
        "api_key_env": "OPENAI_API_KEY",
    },
}

# 모델 단축명 → 정규 모델 ID 매핑
_MODEL_ALIASES: dict[str, str] = {
    # Anthropic
    "opus": "anthropic/claude-opus-4-6",
    "sonnet": "anthropic/claude-sonnet-4-6",
    "haiku": "anthropic/claude-haiku-4-5-20251001",
    "claude-opus": "anthropic/claude-opus-4-6",
    "claude-sonnet": "anthropic/claude-sonnet-4-6",
    # OpenAI
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "gpt-4": "openai/gpt-4",
    "gpt-3.5": "openai/gpt-3.5-turbo",
}


def _resolve_model(model: str) -> str:
    """단축명 또는 완전한 모델 ID를 정규 모델 ID로 변환한다.

    Args:
        model: 사용자가 입력한 모델명 (단축명 또는 'provider/model' 형식).

    Returns:
        정규화된 'provider/model' 형식 모델 ID.
    """
    # 단축명 확인
    normalized = _MODEL_ALIASES.get(model.lower())
    if normalized:
        return normalized

    # 이미 'provider/model' 형식인 경우 그대로 사용
    if "/" in model:
        return model

    # 알 수 없는 모델명 — 그대로 전달하고 CrewAI가 처리하도록 위임
    logger.warning(f"알 수 없는 모델명 '{model}'. 그대로 사용합니다.")
    return model


def _detect_provider(model_id: str) -> str:
    """모델 ID에서 공급자명을 추출한다."""
    if "/" in model_id:
        return model_id.split("/")[0].lower()
    return "unknown"


def _validate_api_key(provider: str) -> None:
    """공급자에 맞는 API 키가 환경변수에 설정되어 있는지 검증한다.

    Args:
        provider: 공급자명 (예: "anthropic", "openai").

    Raises:
        EnvironmentError: 필요한 API 키가 없는 경우.
    """
    info = _PROVIDER_DEFAULTS.get(provider)
    if info is None:
        return  # 알 수 없는 공급자는 건너뜀

    key_env = info["api_key_env"]
    if not os.getenv(key_env):
        raise EnvironmentError(
            f"[{provider}] 모델 사용을 위해 '{key_env}' 환경변수를 설정해야 합니다.\n"
            f"  .env 파일에 {key_env}=your_api_key_here 를 추가하세요."
        )


def create_llm(model: str | None = None) -> LLM:
    """LLM 인스턴스를 생성한다.

    모델 우선순위:
      1. 함수 인자 `model` (CLI --model 옵션)
      2. 환경변수 `LLM_MODEL`
      3. 기본값 "anthropic/claude-opus-4-6"

    Args:
        model: 사용할 모델명. None이면 환경변수 또는 기본값을 사용.

    Returns:
        설정이 완료된 CrewAI LLM 인스턴스.

    Raises:
        EnvironmentError: 필요한 API 키가 설정되어 있지 않은 경우.
    """
    raw_model = model or os.getenv("LLM_MODEL") or "anthropic/claude-opus-4-6"
    resolved = _resolve_model(raw_model)
    provider = _detect_provider(resolved)

    _validate_api_key(provider)

    temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    max_tokens = int(os.getenv("LLM_MAX_TOKENS", "8192"))

    logger.info(f"LLM 생성: model={resolved}, provider={provider}, temperature={temperature}")

    return LLM(
        model=resolved,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def list_supported_models() -> str:
    """지원하는 모델 목록을 사람이 읽기 쉬운 형식으로 반환한다."""
    lines = ["지원 모델 목록:"]
    lines.append("\n  [Anthropic] — ANTHROPIC_API_KEY 필요")
    lines.append("    anthropic/claude-opus-4-6  (단축명: opus, claude-opus)")
    lines.append("    anthropic/claude-sonnet-4-6 (단축명: sonnet, claude-sonnet)")
    lines.append("    anthropic/claude-haiku-4-5-20251001 (단축명: haiku)")
    lines.append("\n  [OpenAI] — OPENAI_API_KEY 필요")
    lines.append("    openai/gpt-4o              (단축명: gpt-4o)")
    lines.append("    openai/gpt-4o-mini         (단축명: gpt-4o-mini)")
    lines.append("    openai/gpt-4               (단축명: gpt-4)")
    return "\n".join(lines)
