#!/usr/bin/env python3
import asyncio
import json
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import openai
import google.generativeai as genai
from datetime import datetime

@dataclass
class Task:
    id: str
    description: str
    assigned_to: str
    status: str = "pending"
    result: Optional[str] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class AIClient(ABC):
    @abstractmethod
    async def execute_task(self, task_description: str) -> str:
        pass

class GeminiClient(AIClient):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def execute_task(self, task_description: str) -> str:
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.model.generate_content(task_description)
            )
            return response.text
        except Exception as e:
            return f"Gemini 실행 오류: {str(e)}"

class ClaudeClient(AIClient):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.anthropic.com/v1",
        )
    
    async def execute_task(self, task_description: str) -> str:
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="claude-3-sonnet-20240229",
                    messages=[{"role": "user", "content": task_description}],
                    max_tokens=1000
                )
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Claude 실행 오류: {str(e)}"

class TaskOrchestrator:
    def __init__(self, gemini_api_key: str, claude_api_key: str):
        self.gemini = GeminiClient(gemini_api_key)
        self.claude = ClaudeClient(claude_api_key)
        self.tasks: List[Task] = []
        self.task_counter = 0
    
    def assign_task_to_ai(self, task_description: str) -> str:
        prompt = f"""
다음 작업을 분석하고 Gemini와 Claude 중 어느 AI가 더 적합한지 결정해주세요:

작업: {task_description}

고려사항:
- Gemini: 창의적 작업, 이미지 분석, 다국어 번역, 최신 정보 검색에 강함
- Claude: 코드 작성, 논리적 분석, 긴 텍스트 처리, 구조화된 작업에 강함

응답 형식: "gemini" 또는 "claude"만 답하세요.
        """
        
        try:
            response = self.gemini.model.generate_content(prompt)
            assignment = response.text.strip().lower()
            return "gemini" if "gemini" in assignment else "claude"
        except:
            return "claude"
    
    async def create_and_execute_task(self, description: str) -> Task:
        self.task_counter += 1
        assigned_ai = self.assign_task_to_ai(description)
        
        task = Task(
            id=f"task_{self.task_counter}",
            description=description,
            assigned_to=assigned_ai
        )
        
        self.tasks.append(task)
        
        print(f"[{task.id}] 작업을 {assigned_ai.upper()}에 할당: {description}")
        
        if assigned_ai == "gemini":
            result = await self.gemini.execute_task(description)
        else:
            result = await self.claude.execute_task(description)
        
        task.result = result
        task.status = "completed"
        
        return task
    
    async def execute_multiple_tasks(self, descriptions: List[str]) -> List[Task]:
        tasks = []
        for desc in descriptions:
            task = await self.create_and_execute_task(desc)
            tasks.append(task)
        return tasks
    
    def get_task_summary(self) -> Dict:
        return {
            "total_tasks": len(self.tasks),
            "gemini_tasks": len([t for t in self.tasks if t.assigned_to == "gemini"]),
            "claude_tasks": len([t for t in self.tasks if t.assigned_to == "claude"]),
            "completed_tasks": len([t for t in self.tasks if t.status == "completed"])
        }

async def main():
    parser = argparse.ArgumentParser(description="AI Orchestrator - Gemini & Claude 작업 분배 시스템")
    parser.add_argument("command", help="실행할 명령어")
    parser.add_argument("--gemini-key", required=True, help="Gemini API 키")
    parser.add_argument("--claude-key", required=True, help="Claude API 키")
    parser.add_argument("--tasks", nargs="+", help="실행할 작업들")
    parser.add_argument("--interactive", action="store_true", help="대화형 모드")
    
    args = parser.parse_args()
    
    orchestrator = TaskOrchestrator(args.gemini_key, args.claude_key)
    
    if args.interactive:
        print("=== AI Orchestrator 대화형 모드 ===")
        print("'exit'를 입력하면 종료됩니다.")
        
        while True:
            try:
                user_input = input("\n작업을 입력하세요: ").strip()
                if user_input.lower() in ['exit', 'quit', '종료']:
                    break
                
                if user_input:
                    task = await orchestrator.create_and_execute_task(user_input)
                    print(f"\n[결과] {task.result}")
                    
            except KeyboardInterrupt:
                break
        
        print(f"\n=== 작업 요약 ===")
        summary = orchestrator.get_task_summary()
        print(f"총 작업: {summary['total_tasks']}")
        print(f"Gemini 작업: {summary['gemini_tasks']}")
        print(f"Claude 작업: {summary['claude_tasks']}")
        
    elif args.tasks:
        print("=== 배치 작업 모드 ===")
        tasks = await orchestrator.execute_multiple_tasks(args.tasks)
        
        for task in tasks:
            print(f"\n[{task.id}] {task.assigned_to.upper()}")
            print(f"작업: {task.description}")
            print(f"결과: {task.result}")
    
    else:
        print("작업을 지정하거나 --interactive 모드를 사용하세요.")

if __name__ == "__main__":
    asyncio.run(main())