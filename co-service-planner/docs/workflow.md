# docs/workflow.md
# 서비스 기획 워크플로우 (Service Planning Workflow)

서비스 기획자가 기획을 수행할 때 따르는 **상세 순서**입니다.

---

## 전체 워크플로우

```
[입력 수신] → [입력 검증] → [Why 분석] → [How 설계] → [What 정의] → [산출물 작성] → [검토 및 Iteration]
```

---

## Step 1. 입력 수신 및 검증

**목적**: 기획에 필요한 모든 입력이 갖춰졌는지 확인

체크리스트:
- [ ] 초기 컨셉 수신 여부
- [ ] 타겟 유저 정보 수신 여부
- [ ] Market Analyst 시장 분석 보고서 수신 여부

**입력 부족 시**: 즉시 부족한 항목을 명시하고 추가 정보를 요청한다. 보고서 없이는 절대 기획을 시작하지 않는다.

---

## Step 2. Why 분석 (사용자와 시장 이해)

**목적**: "왜 이 서비스가 필요한가"를 명확히 정의

### 2-1. JTBD 정의
- 사용자가 언제, 왜, 어떻게 이 서비스를 사용하는지 1문장으로 정의
- Market Analyst의 페르소나와 Pain Point 데이터를 100% 반영

### 2-2. Pain Point 분류
- 감정적 Pain Point
- 기능적 Pain Point
- 사회적 Pain Point

### 2-3. 시장 기회 확인
- TAM/SAM/SOM 검토
- 경쟁사 공백 지점 확인
- USP 도출 근거 검토

**산출물**: JTBD 정의서, Pain Point 분류표

---

## Step 3. How 설계 (해결 전략 수립)

**목적**: "어떻게 사용자 문제를 해결할 것인가"를 설계

### 3-1. User Journey Mapping
- Awareness → Consideration → Purchase → Onboarding → Core Usage → Retention → Advocacy
- 각 단계별 Emotional State, Pain Point, Opportunity 도출

### 3-2. 서비스 컨셉 정의
- 핵심 가치 제안 확정
- 차별화 포인트 (USP) 구체화
- 비즈니스 모델 (BM) 연계

### 3-3. 해결 전략 수립
- 3가지 렌즈 동시 검토:
  - Desirability: 사용자가 진짜 원하는가?
  - Viability: 사업적으로 지속 가능한가?
  - Feasibility: 기술적으로 실행 가능한가?

**산출물**: User Journey Map, 서비스 컨셉 정의서

---

## Step 4. What 정의 (구체적 기능 스펙)

**목적**: "무엇을 만들 것인가"를 구체적으로 정의

### 4-1. User Flow & IA 설계
- 전체 화면 흐름 (Main Flow)
- 조건부 흐름 (Conditional Flow)
- 오류 처리 흐름 (Error Flow)
- Information Architecture (메뉴 구조)

### 4-2. 기능 목록 작성
- 전체 기능 브레인스토밍
- MoSCoW 분류 (Must / Should / Could / Won't)

### 4-3. RICE Scoring
- 각 기능별 Reach, Impact, Confidence, Effort 점수 산정
- RICE Score = (Reach × Impact × Confidence) / Effort
- 우선순위 표 완성

### 4-4. MVP 정의
- Must-have 중 핵심 가치 구현에 필수적인 최소 기능 세트 선정
- Phase 1 (MVP) → Phase 2 (Iteration) → Phase 3 (Scale) 로드맵 작성

**산출물**: User Flow Diagram, IA, 기능 우선순위 표, MVP 정의서, 로드맵

---

## Step 5. PRD 문서 작성

**목적**: 개발·디자인·마케팅 팀이 즉시 실행할 수 있는 스펙 문서 작성

포함 항목:
- 에이전트/서비스 정체성
- 핵심 입력값 및 출력값
- 기능 요구사항 (Functional Requirements)
- 비기능 요구사항 (Non-functional Requirements)
- Market Analyst 연동 기록
- Phase별 로드맵

**산출물**: `docs/decisions.md` (기획 보고서 형식으로 기록)

---

## Step 6. 프로토타입 계획 (선택)

**목적**: 기획 검증을 위한 프로토타입 설계

- Low-fidelity 와이어프레임 계획 (Figma / Miro)
- High-fidelity 프로토타입 계획
- 사용자 테스트 시나리오 작성
- 성공 지표 및 검증 방법론 정의

---

## Step 7. 검토 및 Iteration

**목적**: 피드백을 반영하여 기획을 개선

### Iteration 규칙
- 피드백 수신 즉시 Iteration 수행
- 변경 사항은 Change Log에 명시
- 이전 버전 대비 변경점 명확히 표기
- 추가 정보 필요 시 구체적으로 요청

### 팀 협업 순서
1. **Market Analyst** → 서비스 기획자 (시장 분석 결과 제공)
2. **서비스 기획자** → UX/UI Designer (User Flow, 화면 구조 전달)
3. **서비스 기획자** → Tech Lead (Feasibility Review)
4. **서비스 기획자** → Growth/Marketing (Go-to-Market 전략 연계)

---

## 출력 품질 기준

모든 산출물은 다음 기준을 충족해야 합니다:

| 기준 | 설명 |
|------|------|
| 구체성 | 추상적 표현 없이 화면·기능·수치로 구체화 |
| 실행 가능성 | 개발·디자인·마케팅 팀이 즉시 실행 가능한 수준 |
| 측정 가능성 | KPI와 성공 지표가 명확히 정의됨 |
| 데이터 기반 | 모든 주장에 Market Analyst 데이터 또는 사용자 증거 기반 |
| 우선순위 명확 | MoSCoW + RICE Score로 우선순위가 명확히 정의됨 |
