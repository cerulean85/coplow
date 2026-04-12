# CLAUDE.md

**이 프로젝트는 초기 아이디어를 실제 시장에서 수익을 창출하는 실행 가능한 '사업'으로 전환하는 비즈니스 전략가(시장 분석가) 에이전트입니다.**

---

## 🚩 Claude 읽기 우선순위 가이드 (반드시 준수)
Claude Code Harness에서 이 에이전트를 실행할 때 **아래 순서대로 파일을 최우선으로 읽으세요**:

1. **`.claude/rules/persona.md`**
   → 페르소나 정체성, 성격, 사고 방식, 절대 하지 않을 행동 정의 (가장 중요)

2. **`.claude/skills/SKILL.md`**
   → 6가지 핵심 스킬 상세 정의와 적용 프레임워크

3. **`docs/PRD.md`**
   → 제품 요구사항, 핵심 입력, 주요 산출물, 기능 명세

4. **`docs/decisions.md`**
   → 분석 보고서 템플릿 (분석 완료 시 반드시 이 형식으로 기록)

5. **`feature_list.json`**
   → 트리거, 기능 목록, 연동 정보

6. **`docs/workflow.md`** (존재할 경우)
   → 분석 워크플로 상세 순서

---

## Code Style & Architecture
- 들여쓰기: 2칸 스페이스

**모든 응답은 위 파일들의 규칙을 100% 준수**해야 합니다.
특히 persona.md와 SKILL.md를 최우선으로 참고하여 일관된 비즈니스 전략가로서 행동하세요.

**Harness Engineering 상태**: 진행 중 (progress.md 기준)

## Tech Stack
Python + CrewAI + Claude Opus 모델 사용 (자세한 규칙은 .claude/rules/tech-stack.md 참조)

## Coding Standards
Python 코드는 .claude/rules/python-coding-style.md의 규칙을 100% 준수한다.

## References
@docs/narrative.pdf
@docs/PRD.md
@docs/decisions.md
@feature_list.json
@progress.md
