# co-service-planner — 서비스 기획자 에이전트

> **COPLOW 멀티-에이전트 스웜의 서비스 기획 담당**
> Market Analyst의 시장 검증 보고서를 받아 실행 가능한 서비스 기획으로 구체화합니다.

---

## 소개

**Service Planner Agent**는 15년차 시니어 서비스 기획자 페르소나를 가진 AI 에이전트입니다.
모호한 초기 아이디어를 사용자에게 진짜 가치를 주면서 사업적으로도 지속 가능한 실행 가능한 서비스로 구체화합니다.

### COPLOW 에이전트 연동 순서

```
Market Analyst (co-biz-anlyzer)
    ↓  시장 분석 보고서
Service Planner (이 프로젝트)
    ↓  User Flow, 기능 명세, PRD
UX/UI Designer / Tech Lead / Marketing Agent
```

---

## 빠른 시작

### 1. 설치

```bash
cd co-service-planner
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY 입력
```

### 3. 입력 파일 작성

`input.md`를 열어 내용을 채웁니다:

```
[프로젝트명]
HireMatch

[초기 컨셉]
AI 기반 채용 매칭 서비스 ...

[타겟 유저]
20~50인 규모 중소기업 HR 담당자 ...

[시장 분석 보고서]
(co-biz-anlyzer 결과 붙여넣기)
```

### 4. 실행

```bash
# 기본 실행 (Anthropic claude-3-opus-20240229)
python -m src.main input.md

# OpenAI 사용
python -m src.main input.md --provider openai --model gpt-4o-mini
```

---

## 입력 요구사항

기획 시작 전 다음 3가지가 **모두** 필요합니다:

| 입력 | 설명 | 필수 여부 |
|------|------|---------|
| 초기 컨셉 | 서비스/제품 설명, 핵심 기능, 가치 제안 | 필수 |
| 타겟 유저 정보 | 연령, 직업, 라이프스타일, 현재 사용 대안 | 필수 |
| Market Analyst 보고서 | co-biz-anlyzer가 생성한 시장 분석 보고서 | **필수** |

> Market Analyst 보고서 없이는 기획을 시작하지 않습니다.
> co-biz-anlyzer를 먼저 실행해 보고서를 받아주세요.

---

## 산출물

기획 완료 시 다음 산출물이 `docs/decisions.md`에 자동 저장됩니다:

1. **서비스 컨셉 정의** — JTBD + 가치 제안 + USP
2. **타겟 사용자 페르소나** — 2개 이상, JTBD 연결
3. **User Journey Map** — 7단계 (Awareness → Advocacy)
4. **User Flow & IA** — 화면 단위 흐름 + 메뉴 구조
5. **기능 요구사항 명세** — MoSCoW 분류 + RICE Score
6. **MVP 정의 & Phase 로드맵** — Phase 1~3 계획

---

## 기획 방법론 (7단계 순차 실행)

| 단계 | 에이전트 | 담당 |
|------|---------|------|
| 1 | JTBD 분석가 | 사용자 Job & Pain Point 정의 |
| 2 | Journey 매퍼 | 7단계 User Journey Map |
| 3 | Flow 설계자 | User Flow & IA |
| 4 | 우선순위 분석가 | MoSCoW + RICE Scoring |
| 5 | MVP 설계자 | MVP & Phase 로드맵 |
| 6 | PRD 작성자 | 통합 기획 보고서 |
| 7 | 프로토타입 전략가 | 검증 계획 수립 |

---

## 프로젝트 구조

```
co-service-planner/
├── .claude/
│   ├── rules/
│   │   └── persona.md          # 서비스 기획자 페르소나
│   └── skills/
│       └── SKILL.md            # 8가지 기획 방법론
├── docs/
│   ├── PRD.md                  # 에이전트 요구사항 명세
│   ├── workflow.md             # 기획 워크플로우
│   ├── output_format.md        # 산출물 형식 & 검증 체크리스트
│   ├── decisions.md            # 기획 보고서 누적 아카이브
│   ├── progress.md             # Harness 완성 진행 상황
│   └── changelog.md            # 버전 이력
├── examples/
│   └── planning-example.md     # 완성된 기획 예시
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── planner_agents.py   # 7개 에이전트 클래스
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── planner_tasks.py    # 7개 순차 태스크
│   ├── tools/
│   │   ├── __init__.py
│   │   └── planner_tools.py    # 커스텀 도구
│   ├── crew.py                 # Crew 조립 & run_crew()
│   └── main.py                 # CLI 진입점
├── requirements.txt
├── .env.example
├── feature_list.json
└── CLAUDE.md
```

---

## Claude Code Harness 사용

Claude Code CLI에서 직접 대화형으로 사용할 수도 있습니다:

```bash
# 이 디렉토리에서 Claude Code 실행
cd co-service-planner && claude

# 대화 시작 예시:
# "서비스 기획 시작: [컨셉 설명]"
# "기획해줘: [컨셉]"
```

CLAUDE.md의 트리거 키워드를 사용하면 서비스 기획자 모드로 자동 진입합니다.

---

## 라이선스

MIT License — COPLOW Project
