# co-ux-designer

서비스 기획자의 PRD를 입력으로 받아 **정보 구조도(IA)**, **핵심 유저 플로우**, **화면 별 필수 UI 컴포넌트**를 자동으로 설계하는 UX 리서처/설계자 Agent입니다.

CrewAI 프레임워크 기반으로 동작하며, Anthropic Claude 또는 OpenAI 모델을 LLM으로 사용합니다.

---

## 주요 기능

| 기능 | 설명 |
|---|---|
| PRD 분석 | 비즈니스 목표, 타겟 페르소나, 사용자 목표, Pain Point를 체계적으로 추출 |
| 정보 구조도(IA) 설계 | 전체 메뉴 계층을 Mermaid Mindmap + 계층형 텍스트로 산출 |
| 핵심 유저 플로우 설계 | Happy Path + Decision Point + Error Flow를 Mermaid Flowchart로 산출 |
| UI 컴포넌트 정의 | 화면 별 필수 컴포넌트, 상태, 인터랙션, 접근성 가이드 제공 |
| UX 원칙 Self-Review | Nielsen 10 Heuristics, Fitts' Law, Gestalt 원칙 기반 자동 검증 |

---

## 요구사항

- Python 3.11+
- Anthropic API Key (Claude 모델 사용 시)
- OpenAI API Key (GPT 모델 사용 시)

---

## 설치

```bash
# 가상 환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고 API 키를 입력합니다.

```bash
cp .env.example .env
```

```dotenv
# .env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

LLM_MODEL=anthropic/claude-opus-4-6   # 기본 모델
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=8192
```

---

## 사용법

### 기본 실행

```bash
# PRD 파일 지정
python src/main.py --prd docs/example_prd.md

# 서비스명 명시
python src/main.py --prd my_prd.md --service MyApp

# 산출물 저장 경로 지정 (기본값: outputs/)
python src/main.py --prd my_prd.md --output-dir results/
```

### 데모 실행

`docs/example_prd.md` (BookLog 독서 기록 앱)를 사용한 데모를 실행합니다.

```bash
python src/main.py --example
```

### 표준 입력(stdin) 모드

PRD 파일 없이 직접 텍스트를 붙여넣어 실행할 수 있습니다.

```bash
python src/main.py
# 안내에 따라 PRD 텍스트 입력 후 Ctrl+D
```

### 모델 선택

```bash
# Claude Sonnet 사용
python src/main.py --prd my_prd.md --model sonnet

# GPT-4o 사용
python src/main.py --prd my_prd.md --model gpt-4o

# 지원 모델 전체 목록 확인
python src/main.py --list-models
```

**지원 단축명**: `opus`, `sonnet`, `haiku`, `gpt-4o`, `gpt-4o-mini`, `gpt-4`

---

## 산출물

실행 완료 후 `outputs/ux_design_output.md`에 아래 내용이 저장됩니다.

1. **PRD 분석 요약** — 비즈니스 목표, 페르소나, 사용자 목표, Pain Point
2. **정보 구조도(IA)** — Mermaid Mindmap + 계층형 텍스트
3. **핵심 유저 플로우** — Mermaid Flowchart + 단계별 설명 테이블
4. **화면 별 UI 컴포넌트 정의** — 컴포넌트 목적·상태·인터랙션·접근성
5. **UX 원칙 Self-Review** — 4대 원칙 + Nielsen 체크리스트 + 개선 제안

---

## 프로젝트 구조

```
co-ux-designer/
├── src/
│   ├── agents/
│   │   └── ux_designer.py      # UX 설계자 Agent 정의
│   ├── tasks/
│   │   └── ux_design_tasks.py  # 6단계 설계 Task 정의
│   ├── crew.py                 # Crew 조립 및 실행 진입점
│   ├── main.py                 # CLI 메인 실행 파일
│   ├── config.py               # 설정 관리
│   └── llm_factory.py          # LLM 모델 팩토리
├── docs/
│   ├── PRD.md                  # Agent PRD (에이전트 요구사항 문서)
│   ├── decisions.md            # 분석 보고서 템플릿
│   ├── example_prd.md          # 샘플 PRD (BookLog 앱)
│   └── target_prd.md           # 실제 분석 대상 PRD
├── .claude/
│   ├── rules/                  # 페르소나, 실행 지침, 출력 형식, 예시
│   └── skills/                 # 핵심 스킬 정의
├── outputs/                    # 생성된 UX 설계 산출물
├── tests/
│   └── test_case_01.md         # 테스트 케이스
├── .env.example
├── requirements.txt
└── pyproject.toml
```

---

## 설계 원칙

이 Agent는 모든 산출물에 아래 원칙을 적용합니다.

- **직관성**: 초보 사용자도 별도 학습 없이 사용 가능한 구조 설계
- **효율성**: 목표 달성까지 최소 스텝, Miller's Law(7±2) 준수
- **접근성**: WCAG 2.1 기준, ARIA, 색 대비, 키보드 네비게이션 고려
- **일관성**: 서비스 전체에서 동일한 컴포넌트·레이블·인터랙션 유지

PRD에 없는 기능의 임의 추가, Dark Pattern 제안, 기술 제약을 이유로 한 UX 타협안 우선 제시는 하지 않습니다.
