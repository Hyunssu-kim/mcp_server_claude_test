#!/usr/bin/env python3
"""
MCP Server for AI Orchestrator
Gemini가 작업을 분석하고 Gemini/Claude CLI 명령어로 실행하는 MCP 서버
"""
import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import logging

# MCP 서버를 위한 기본 imports
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolRequest,
        CallToolResult,
        ListToolsRequest,
        ListToolsResult,
        TextContent,
        Tool,
    )
except ImportError:
    print("MCP 라이브러리가 필요합니다: pip install mcp", file=sys.stderr)
    sys.exit(1)

# 로깅 설정 (stderr로 출력)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

@dataclass
class TaskResult:
    assigned_to: str
    command: str
    result: str
    success: bool
    error: Optional[str] = None

class CLIExecutor:
    """기존 gemini/claude CLI 명령어를 실행하는 클래스"""
    
    async def execute_gemini(self, prompt: str) -> TaskResult:
        """gemini CLI 명령어 실행"""
        try:
            cmd = ["gemini", prompt]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return TaskResult(
                    assigned_to="gemini",
                    command=" ".join(cmd),
                    result=stdout.strip(),
                    success=True
                )
            else:
                return TaskResult(
                    assigned_to="gemini",
                    command=" ".join(cmd),
                    result="",
                    success=False,
                    error=stderr.strip()
                )
                
        except Exception as e:
            return TaskResult(
                assigned_to="gemini",
                command=f"gemini {prompt}",
                result="",
                success=False,
                error=f"CLI 실행 오류: {str(e)}"
            )
    
    async def execute_claude(self, prompt: str) -> TaskResult:
        """claude CLI 명령어 실행"""
        try:
            cmd = ["claude", prompt]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return TaskResult(
                    assigned_to="claude",
                    command=" ".join(cmd),
                    result=stdout.strip(),
                    success=True
                )
            else:
                return TaskResult(
                    assigned_to="claude",
                    command=" ".join(cmd),
                    result="",
                    success=False,
                    error=stderr.strip()
                )
                
        except Exception as e:
            return TaskResult(
                assigned_to="claude",
                command=f"claude {prompt}",
                result="",
                success=False,
                error=f"CLI 실행 오류: {str(e)}"
            )

class TaskAssigner:
    """작업을 어느 AI에 할당할지 결정하는 클래스"""
    
    def __init__(self, cli_executor: CLIExecutor):
        self.cli_executor = cli_executor
    
    async def decide_assignment(self, task_description: str) -> str:
        """Gemini에게 작업 할당을 물어보는 함수"""
        assignment_prompt = f"""
다음 작업을 분석하고 Gemini와 Claude 중 어느 AI가 더 적합한지 결정해주세요:

작업: {task_description}

고려사항:
- Gemini: 창의적 작업, 이미지 분석, 다국어 번역, 최신 정보 검색, 브레인스토밍에 강함
- Claude: 코드 작성, 논리적 분석, 긴 텍스트 처리, 구조화된 작업, 문서 작성에 강함

응답은 반드시 "gemini" 또는 "claude" 중 하나만 답하세요.
"""
        
        try:
            result = await self.cli_executor.execute_gemini(assignment_prompt)
            if result.success:
                assignment = result.result.strip().lower()
                return "gemini" if "gemini" in assignment else "claude"
            else:
                # Gemini 호출 실패시 기본값으로 Claude 사용
                return "claude"
        except Exception:
            return "claude"

class AIOrchestrator:
    """MCP 서버의 메인 오케스트레이터 클래스"""
    
    def __init__(self):
        self.cli_executor = CLIExecutor()
        self.task_assigner = TaskAssigner(self.cli_executor)
        self.task_history: List[Dict] = []
    
    async def execute_task(self, task_description: str, force_ai: Optional[str] = None) -> TaskResult:
        """작업을 실행하는 메인 함수"""
        
        # AI 강제 지정이 없으면 자동 할당
        if force_ai:
            assigned_ai = force_ai.lower()
        else:
            assigned_ai = await self.task_assigner.decide_assignment(task_description)
        
        logger.info(f"작업을 {assigned_ai.upper()}에 할당: {task_description[:50]}...")
        
        # 해당 AI로 작업 실행
        if assigned_ai == "gemini":
            result = await self.cli_executor.execute_gemini(task_description)
        else:
            result = await self.cli_executor.execute_claude(task_description)
        
        # 히스토리에 기록
        self.task_history.append({
            "task": task_description,
            "assigned_to": result.assigned_to,
            "success": result.success,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        return result
    
    async def execute_parallel_tasks(self, tasks: List[Dict]) -> List[TaskResult]:
        """여러 작업을 병렬로 실행"""
        task_coroutines = []
        
        for task_info in tasks:
            task_desc = task_info.get("description", "")
            force_ai = task_info.get("force_ai")
            task_coroutines.append(self.execute_task(task_desc, force_ai))
        
        results = await asyncio.gather(*task_coroutines, return_exceptions=True)
        
        # 예외 처리
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(TaskResult(
                    assigned_to="unknown",
                    command="",
                    result="",
                    success=False,
                    error=str(result)
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_statistics(self) -> Dict:
        """작업 통계 반환"""
        total_tasks = len(self.task_history)
        gemini_tasks = len([t for t in self.task_history if t["assigned_to"] == "gemini"])
        claude_tasks = len([t for t in self.task_history if t["assigned_to"] == "claude"])
        successful_tasks = len([t for t in self.task_history if t["success"]])
        
        return {
            "total_tasks": total_tasks,
            "gemini_tasks": gemini_tasks,
            "claude_tasks": claude_tasks,
            "successful_tasks": successful_tasks,
            "success_rate": successful_tasks / total_tasks if total_tasks > 0 else 0
        }

# MCP 서버 인스턴스 생성
server = Server("ai-orchestrator")
orchestrator = AIOrchestrator()

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """사용 가능한 도구들을 반환"""
    return ListToolsResult(
        tools=[
            Tool(
                name="execute_task",
                description="작업을 분석하고 적절한 AI(Gemini/Claude)에 할당하여 실행합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "실행할 작업 설명"
                        },
                        "force_ai": {
                            "type": "string",
                            "enum": ["gemini", "claude"],
                            "description": "특정 AI 강제 지정 (선택사항)"
                        }
                    },
                    "required": ["task"]
                }
            ),
            Tool(
                name="execute_parallel_tasks",
                description="여러 작업을 병렬로 실행합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "tasks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "description": {
                                        "type": "string",
                                        "description": "작업 설명"
                                    },
                                    "force_ai": {
                                        "type": "string",
                                        "enum": ["gemini", "claude"],
                                        "description": "특정 AI 강제 지정 (선택사항)"
                                    }
                                },
                                "required": ["description"]
                            }
                        }
                    },
                    "required": ["tasks"]
                }
            ),
            Tool(
                name="get_statistics",
                description="작업 실행 통계를 반환합니다",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="execute_gemini",
                description="Gemini CLI로 직접 작업을 실행합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Gemini에게 전달할 프롬프트"
                        }
                    },
                    "required": ["prompt"]
                }
            ),
            Tool(
                name="execute_claude",
                description="Claude CLI로 직접 작업을 실행합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Claude에게 전달할 프롬프트"
                        }
                    },
                    "required": ["prompt"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """도구 호출 처리"""
    
    try:
        if request.name == "execute_task":
            task = request.params.get("task", "")
            force_ai = request.params.get("force_ai")
            
            if not task:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 작업 설명이 필요합니다")]
                )
            
            result = await orchestrator.execute_task(task, force_ai)
            
            response = {
                "assigned_to": result.assigned_to,
                "command": result.command,
                "success": result.success,
                "result": result.result if result.success else "",
                "error": result.error if not result.success else None
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(response, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "execute_parallel_tasks":
            tasks = request.params.get("tasks", [])
            
            if not tasks:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 작업 목록이 필요합니다")]
                )
            
            results = await orchestrator.execute_parallel_tasks(tasks)
            
            response = []
            for result in results:
                response.append({
                    "assigned_to": result.assigned_to,
                    "command": result.command,
                    "success": result.success,
                    "result": result.result if result.success else "",
                    "error": result.error if not result.success else None
                })
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(response, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "get_statistics":
            stats = orchestrator.get_statistics()
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(stats, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "execute_gemini":
            prompt = request.params.get("prompt", "")
            
            if not prompt:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 프롬프트가 필요합니다")]
                )
            
            result = await orchestrator.cli_executor.execute_gemini(prompt)
            
            response = {
                "assigned_to": result.assigned_to,
                "command": result.command,
                "success": result.success,
                "result": result.result if result.success else "",
                "error": result.error if not result.success else None
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(response, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "execute_claude":
            prompt = request.params.get("prompt", "")
            
            if not prompt:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 프롬프트가 필요합니다")]
                )
            
            result = await orchestrator.cli_executor.execute_claude(prompt)
            
            response = {
                "assigned_to": result.assigned_to,
                "command": result.command,
                "success": result.success,
                "result": result.result if result.success else "",
                "error": result.error if not result.success else None
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(response, ensure_ascii=False, indent=2))]
            )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"ERROR: 알 수 없는 도구: {request.name}")]
            )
    
    except Exception as e:
        logger.error(f"도구 실행 중 오류: {str(e)}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"ERROR: {str(e)}")]
        )

async def main():
    """MCP 서버 실행"""
    # 서버 초기화 옵션
    init_options = InitializationOptions(
        server_name="ai-orchestrator",
        server_version="1.0.0",
        capabilities={}
    )
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                init_options
            )
    except Exception as e:
        logger.error(f"서버 실행 중 오류: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())