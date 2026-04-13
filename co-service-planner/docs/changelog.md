# docs/changelog.md
# 변경 이력 (Changelog)

> 버전별 변경 사항을 역순으로 기록합니다 (최신 버전이 맨 위).

---

## v1.1 — 2026-04-13

**Harness Engineering 완성 (Phase 2~5)**

### 추가 (Added)
- `docs/progress.md` — Harness Engineering 진행 체크리스트
- `docs/output_format.md` — 기획 산출물 강제 형식 & 12개 항목 검증 체크리스트
- `docs/changelog.md` — 버전 이력 파일 (이 파일)
- `examples/planning-example.md` — 완성된 서비스 기획 예시 (AI 채용 매칭 서비스)
- `tools.py` — SerperSearchTool + SavePlanningTool
- `agents.py` — 7개 CrewAI 에이전트 정의
- `tasks.py` — 7개 순차 태스크 (context chaining)
- `crew.py` — Crew 조립 + decisions.md 자동 저장
- `main.py` — CLI 진입점 (Market Analyst 보고서 입력 검증)
- `requirements.txt` — Python 의존성
- `.env.example` — 환경변수 템플릿
- `README.md` — 프로젝트 문서 (한국어/영어)

### 변경 (Changed)
- `feature_list.json` — JSON Schema 업그레이드, `harnessEnabled: true`, `status: "complete"` 업데이트

---

## v1.0 — 2026-04-12

**초기 문서 구조 완성 (Phase 1~2)**

### 추가 (Added)
- `CLAUDE.md` — 에이전트 선언문 & 파일 읽기 우선순위 가이드
- `.claude/rules/persona.md` — 15년차 서비스 기획자 페르소나 정의
- `.claude/skills/SKILL.md` — 8가지 기획 방법론 상세 정의
- `docs/PRD.md` — 에이전트 요구사항 명세서
- `docs/workflow.md` — 7단계 기획 워크플로우
- `docs/decisions.md` — 기획 보고서 누적 아카이브 템플릿
- `feature_list.json` — 트리거, 기능 목록, 연동 정보

---

**이 파일은 co-service-planner의 모든 버전 이력을 추적합니다.**
