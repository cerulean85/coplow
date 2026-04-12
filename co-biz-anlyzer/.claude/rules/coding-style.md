# Python Coding Style & Best Practices

## Core Standards
- Python 버전: 3.11 이상
- 코딩 스타일: PEP 8 + Ruff (strict mode)
- Formatter: Black (line-length=88)
- Linter: Ruff + isort + pyright (타입 체크)
- Type Hint: 모든 함수·클래스·변수에 반드시 사용 (from __future__ import annotations)

## File & Module Rules
- 파일 인코딩: UTF-8
- 파일 상단: shebang + docstring + __future__ imports
- 모듈 이름: snake_case
- 클래스·함수 이름: PascalCase / snake_case (PEP 8 준수)
- 한 파일당 최대 400줄 권장 (너무 길면 Agent/Task별로 분리)

## CrewAI Specific Rules
- Agent: class MarketResearchAgent(BaseAgent) 형태로 정의
- Task: @task 데코레이터 또는 Task() 클래스로 생성
- Crew: crew.py에 Single Entry Point (run_crew() 함수)
- 모든 Agent의 role, goal, backstory는 market-analyst 페르소나와 100% 일치
- Tool은 crewai_tools 또는 custom tools만 사용
- verbose=True + memory=True 기본 활성화

## Code Quality Rules (Claude가 반드시 지킬 것)
- 함수는 30줄 이하 (복잡하면 helper 함수로 분리)
- Docstring: Google 스타일 (""" ... """)
- Error Handling: try-except 구체적 Exception + logging
- f-string만 사용 (%.format, .format 금지)
- List/Dict Comprehension 적극 활용 (가독성 떨어지면 for문)
- async/await 사용 시 awaitable 함수는 await 키워드 반드시 명시
- 환경 변수는 pydantic-settings 또는 dotenv로 관리 (.env.example 제공)

## Do's and Don'ts
**반드시**
- 모든 public 함수·클래스에 type hint + docstring
- requirements.txt와 pyproject.toml (ruff, black 설정) 동기화
- main.py 또는 crew.py에서 if __name__ == "__main__": run_crew()

**절대 하지 말 것**
- console.log / print() 디버깅용으로 남기기 (logging 모듈 사용)
- hard-coded API key
- from xxx import * (명시적 import만)
- bare except: (except Exception as e: 허용)

## Auto Format Command
```bash
ruff check --fix
ruff format