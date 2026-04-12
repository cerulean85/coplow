# Business Strategist Multi-Agent Analysis System

A **CrewAI-based Multi-Agent System** that transforms early-stage ideas into actionable, revenue-generating businesses in real markets.

7 specialized agents perform analysis sequentially, and the final results are automatically saved to `docs/decisions.md`.

---

## Agent Architecture

A total of 7 agents execute **sequentially** according to the analysis methodology defined in SKILL.md.

```
Step 1  UserResearcherAgent    Target User Persona & Pain Points (JTBD-based)
  ↓
Step 2  MarketAnalystAgent     Market Analysis (TAM/SAM/SOM + PESTLE + SWOT)
  ↓
Step 3  CompetitiveIntelAgent  Competitor Analysis (Direct/Indirect/Substitutes + Value Curve)
  ↓
Step 4  ValuePropAgent         USP Design (3 Sentences + Customer Choice Rationale)
  ↓
Step 5  BusinessModelAgent     BM Planning (BMC 9 Blocks + Unit Economics + 3 Scenarios)
  ↓
Step 6  KpiStrategyAgent       KPI & Goals (North Star + OKR + Leading/Lagging)
  ↓
Step 7  RiskManagerAgent       Risk Matrix + 3-Year Financial Projections → Save to decisions.md
```

---

## Project Structure

```
cooperator-biz-anlyzer/
├── main.py               # CLI entry point
├── crew.py               # Crew assembly and execution
├── agents.py             # 7 agent definitions (provider/model factory)
├── tasks.py              # 7 task definitions (context chaining)
├── tools.py              # SerperSearchTool + SaveDecisionsTool
├── requirements.txt      # Dependencies
├── .env.example          # Environment variable template
│
├── .claude/
│   ├── rules/
│   │   └── persona.md    # Business strategist persona rules
│   └── skills/
│       └── SKILL.md      # 7-step analysis methodology
│
└── docs/
    ├── decisions.md      # Cumulative analysis results storage
    ├── PRD.md            # Agent requirements specification
    ├── workflow.md       # Detailed analysis workflow
    ├── output_format.md  # Output format standards
    ├── progress.md       # Harness Engineering progress
    └── changelog.md      # Change history
```

---

## Getting Started

### 1. Install Packages

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Open the `.env` file and enter your API keys.

```env
# Anthropic (required when using --provider anthropic)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI (required when using --provider openai)
OPENAI_API_KEY=your_openai_api_key_here

# Web Search (optional — without it, analysis uses only LLM built-in knowledge)
SERPER_API_KEY=your_serper_api_key_here
```

> `SERPER_API_KEY` is optional. Without it, analysis relies solely on LLM built-in knowledge. With it, real-time market/competitor data is searched, improving analysis quality. You can get a free key at [serper.dev](https://serper.dev).

### 3. Run

```bash
# Default execution (Anthropic Claude)
python main.py --concept "AI English conversation app" --target "Working professionals in their 20s-30s"

# Using OpenAI GPT-4o
python main.py --provider openai --concept "AI English conversation app" --target "Working professionals in their 20s-30s"

# Specify model directly
python main.py --provider openai --model gpt-4o-mini --concept "..." --target "..."
python main.py --provider anthropic --model claude-opus-4-6 --concept "..." --target "..."
```

---

## License

MIT License

---

---

# 비즈니스 전략가 Multi-Agent 분석 시스템 (한국어)

초기 아이디어를 실제 시장에서 수익을 창출하는 실행 가능한 '사업'으로 전환하는 **CrewAI 기반 Multi-Agent 시스템**입니다.

7개의 전문 에이전트가 순서대로 분석을 수행하고, 최종 결과를 `docs/decisions.md`에 자동 저장합니다.

---

## 에이전트 구성

총 7개의 에이전트가 SKILL.md의 분석 방법론에 따라 **순서대로** 실행됩니다.

```
Step 1  UserResearcherAgent    타겟 사용자 페르소나 & Pain Point (JTBD 기반)
  ↓
Step 2  MarketAnalystAgent     시장 분석 (TAM/SAM/SOM + PESTLE + SWOT)
  ↓
Step 3  CompetitiveIntelAgent  경쟁사 분석 (직접/간접/대체재 + Value Curve)
  ↓
Step 4  ValuePropAgent         USP 설계 (3문장 + 고객 선택 이유)
  ↓
Step 5  BusinessModelAgent     BM 기획 (BMC 9블록 + Unit Economics + 3시나리오)
  ↓
Step 6  KpiStrategyAgent       KPI & 목표 (North Star + OKR + Leading/Lagging)
  ↓
Step 7  RiskManagerAgent       리스크 매트릭스 + 3년 재무 전망 → decisions.md 저장
```

---

## 프로젝트 구조

```
cooperator-biz-anlyzer/
├── main.py               # CLI 진입점
├── crew.py               # Crew 조립 및 실행
├── agents.py             # 7개 에이전트 정의 (provider/model 팩토리)
├── tasks.py              # 7개 태스크 정의 (context 체이닝)
├── tools.py              # SerperSearchTool + SaveDecisionsTool
├── requirements.txt      # 의존성
├── .env.example          # 환경변수 템플릿
│
├── .claude/
│   ├── rules/
│   │   └── persona.md    # 비즈니스 전략가 페르소나 규칙
│   └── skills/
│       └── SKILL.md      # 7단계 분석 방법론
│
└── docs/
    ├── decisions.md      # 분석 결과 누적 저장소
    ├── PRD.md            # 에이전트 요구사항 정의서
    ├── workflow.md       # 분석 워크플로우 상세
    ├── output_format.md  # 출력 포맷 표준
    ├── progress.md       # Harness Engineering 진행 현황
    └── changelog.md      # 변경 이력
```

---

## 시작하기

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열고 API 키를 입력합니다.

```env
# Anthropic (--provider anthropic 사용 시 필요)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OpenAI (--provider openai 사용 시 필요)
OPENAI_API_KEY=your_openai_api_key_here

# 웹 검색 (선택 사항 — 없으면 LLM 내장 지식만으로 분석)
SERPER_API_KEY=your_serper_api_key_here
```

> `SERPER_API_KEY`는 선택 사항입니다. 없으면 웹 검색 없이 LLM 내장 지식으로만 분석하고, 있으면 실시간 시장/경쟁사 데이터를 검색해 분석 품질이 높아집니다. [serper.dev](https://serper.dev)에서 무료로 발급받을 수 있습니다.

### 3. 실행

```bash
# 기본 실행 (Anthropic Claude)
python main.py --concept "AI 영어 회화 앱" --target "20~30대 직장인"

# OpenAI GPT-4o 사용
python main.py --provider openai --concept "AI 영어 회화 앱" --target "20~30대 직장인"

# 모델 직접 지정
python main.py --provider openai --model gpt-4o-mini --concept "..." --target "..."
python main.py --provider anthropic --model claude-opus-4-6 --concept "..." --target "..."
```

---

## 라이선스

MIT License
python main.py --provider openai --concept "휴가 매매 시스템" --target "법적으로 휴가가 보장되는 모든 직장인"
python main.py --provider openai --concept "AI 영어 학습 앱" --target "20-30대 직장인"

# 인터랙티브 모드 (인자 없이 실행)
python main.py
```

---

## 지원 LLM

| Provider | 기본 모델 | 직접 지정 예시 |
|----------|-----------|----------------|
| `anthropic` (기본값) | `claude-sonnet-4-6` | `claude-opus-4-6`, `claude-haiku-4-5` |
| `openai` | `gpt-4o` | `gpt-4o-mini`, `gpt-4-turbo` |

---

## 분석 산출물

분석이 완료되면 `docs/decisions.md`에 아래 6섹션 보고서가 자동 저장됩니다.

| # | 섹션 | 주요 내용 |
|---|------|-----------|
| 1 | 타겟 사용자 페르소나 | JTBD 기반 페르소나 2~3개, Pain Point 4~6개 |
| 2 | 시장 분석 | TAM/SAM/SOM, SWOT, PESTLE |
| 3 | 경쟁사 분석 & USP | 경쟁사 테이블, Value Curve, USP 3문장 |
| 4 | 비즈니스 모델 | BMC 9블록, Unit Economics, 3가지 시나리오 |
| 5 | KPI & 비즈니스 목표 | North Star Metric, OKR, Leading/Lagging KPI 6개 |
| 6 | Risk & 대응 전략 | 리스크 매트릭스, Mitigation Plan, 3년 재무 전망 |

---

## 사용 프레임워크

- **JTBD** (Jobs-to-be-Done)
- **TAM / SAM / SOM**
- **PESTLE + SWOT**
- **Value Curve / Blue Ocean Strategy**
- **Business Model Canvas**
- **Unit Economics** (CAC, LTV, Payback Period)
- **OKR + North Star Metric**
- **Risk Matrix** (발생 확률 × 영향도)

---

## 필수 입력값

| 항목 | 설명 | 예시 |
|------|------|------|
| `--concept` | 제품/서비스 아이디어 | `"AI로 개인화된 영어 회화 학습 앱"` |
| `--target` | 대상 고객군 초기 가설 | `"20~30대 직장인, 영어 실력 향상을 원하지만 시간이 부족한 사람"` |