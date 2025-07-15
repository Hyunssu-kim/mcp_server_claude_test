#!/usr/bin/env python3
"""
AI Orchestrator 사용 예제
"""
import asyncio
from ai_orchestrator import TaskOrchestrator

async def example_usage():
    # API 키 설정 (실제 사용시에는 환경변수나 설정파일에서 읽어오세요)
    GEMINI_API_KEY = "your_gemini_key_here"
    CLAUDE_API_KEY = "your_claude_key_here"
    
    # Orchestrator 생성
    orchestrator = TaskOrchestrator(GEMINI_API_KEY, CLAUDE_API_KEY)
    
    # 예제 작업들
    tasks = [
        "Python으로 피보나치 수열을 구하는 함수를 작성해주세요",
        "오늘 날씨에 어울리는 시를 한국어로 써주세요",
        "데이터베이스 정규화의 개념을 설명해주세요",
        "영어 문장 'Hello World'를 5개 언어로 번역해주세요",
        "JSON 파싱 함수를 JavaScript로 작성해주세요"
    ]
    
    print("=== AI Orchestrator 예제 실행 ===\n")
    
    # 작업 실행
    completed_tasks = await orchestrator.execute_multiple_tasks(tasks)
    
    # 결과 출력
    print("\n=== 실행 결과 ===")
    for task in completed_tasks:
        print(f"\n[{task.id}] {task.assigned_to.upper()}가 처리")
        print(f"작업: {task.description}")
        print(f"결과: {task.result[:200]}...")  # 처음 200자만 출력
        print("-" * 50)
    
    # 요약 출력
    summary = orchestrator.get_task_summary()
    print(f"\n=== 작업 요약 ===")
    print(f"총 작업 수: {summary['total_tasks']}")
    print(f"Gemini 담당: {summary['gemini_tasks']}개")
    print(f"Claude 담당: {summary['claude_tasks']}개")
    print(f"완료된 작업: {summary['completed_tasks']}개")

if __name__ == "__main__":
    asyncio.run(example_usage())