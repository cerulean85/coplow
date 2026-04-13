"""UX 설계자 Crew — Agent와 Task를 조립하고 실행한다."""
from __future__ import annotations

import logging
from pathlib import Path

from crewai import Crew, Process

from src.agents.ux_designer import create_ux_designer_agent
from src.tasks.ux_design_tasks import create_tasks

logger = logging.getLogger(__name__)


class UXDesignerCrew:
    """UX 설계자 Agent Crew.

    PRD 내용을 받아 순차적(Sequential) 프로세스로 6단계 UX 설계를 수행하고
    최종 산출물을 outputs/ 디렉토리에 저장한다.
    """

    OUTPUT_DIR = "outputs"

    def __init__(
        self,
        prd_content: str,
        service_name: str = "Unknown Service",
        model: str | None = None,
    ) -> None:
        """Crew를 초기화한다.

        Args:
            prd_content: 분석할 PRD 원문.
            service_name: 서비스명 (산출물 헤더 및 파일명에 사용).
            model: 사용할 LLM 모델명. None이면 환경변수 또는 기본값 사용.
        """
        self.prd_content = prd_content
        self.service_name = service_name
        self.model = model
        Path(self.OUTPUT_DIR).mkdir(exist_ok=True)

    def run(self) -> str:
        """Crew를 실행하고 최종 산출물 문자열을 반환한다.

        Returns:
            최종 Task의 출력 결과 문자열.
        """
        logger.info(f"[UXDesignerCrew] 시작 — 서비스: {self.service_name}, 모델: {self.model or 'env/default'}")

        agent = create_ux_designer_agent(model=self.model)
        tasks = create_tasks(
            agent=agent,
            prd_content=self.prd_content,
            service_name=self.service_name,
            output_dir=self.OUTPUT_DIR,
        )

        crew = Crew(
            agents=[agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
        )

        result = crew.kickoff()
        logger.info(f"[UXDesignerCrew] 완료 — 산출물: {self.OUTPUT_DIR}/ux_design_output.md")
        return str(result)


def run_crew(
    prd_content: str,
    service_name: str = "Unknown Service",
    model: str | None = None,
) -> str:
    """UXDesignerCrew를 생성하고 실행하는 단일 진입 함수.

    Args:
        prd_content: 분석할 PRD 원문.
        service_name: 서비스명.
        model: 사용할 LLM 모델명. None이면 환경변수 또는 기본값 사용.

    Returns:
        최종 UX 설계 산출물 문자열.
    """
    crew = UXDesignerCrew(prd_content=prd_content, service_name=service_name, model=model)
    return crew.run()


if __name__ == "__main__":
    import sys
    from pathlib import Path

    # 프로젝트 루트를 Python path에 추가
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from dotenv import load_dotenv
    load_dotenv()

    # 기본 실행: example_prd.md를 입력으로 사용
    example_prd_path = Path(__file__).parent.parent / "docs" / "example_prd.md"
    if example_prd_path.exists():
        prd = example_prd_path.read_text(encoding="utf-8")
        run_crew(prd_content=prd, service_name="BookLog")
    else:
        print("[오류] docs/example_prd.md 파일을 찾을 수 없습니다.")
        sys.exit(1)
