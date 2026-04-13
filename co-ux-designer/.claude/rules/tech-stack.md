# Tech Stack & Environment Rules

## Project Environment
- Language: Python 3.11+
- Framework: CrewAI (최신 버전)
- LLM: Anthropic Claude Opus (Claude 3 Opus 또는 최신 Opus 모델)
- API: Anthropic SDK (ChatAnthropic)

## Mandatory Dependencies (requirements.txt에 반드시 포함)
crewai
crewai-tools
anthropic
python-dotenv
pydantic
langchain-anthropic  # CrewAI 내부에서 Claude 사용 시 필요

## LLM Configuration (항상 이렇게 설정)
- Model: Claude or OpenAI 모델 사용
- Temperature: 0.0 (시장 분석처럼 사실 기반 작업 시)
- Max tokens: 4096 이상
- API Key: .env 파일의 ANTHROPIC_API_KEY, OPEN_API_KEY 사용

## Code Generation Rules
- CrewAI Agent/Task/Crew 구조를 반드시 사용
- 각 Agent는 market-analyst 페르소나를 상속하거나 준수
- Tool은 CrewAI built-in tool + custom tool만 사용
- async/await 패턴을 적절히 활용
- 에러 핸들링은 try-except + CrewAI의 verbose=True 로깅 필수
- config/crew.py 또는 main.py에서 Crew를 실행하는 single entry point 유지

## Project Structure (강제)
src/
├── agents/
├── tasks/
├── tools/
├── crew.py
├── main.py
├── .env.example
└── requirements.txt
