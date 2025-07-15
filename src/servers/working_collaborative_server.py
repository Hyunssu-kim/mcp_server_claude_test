#!/usr/bin/env python3
"""
Working Collaborative AI Orchestrator - 안정적인 버전
"""
import asyncio
import json
import sys
import subprocess
from typing import Any, Dict, List, Optional

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

class SimpleCLIExecutor:
    """간단한 CLI 실행기"""
    
    async def execute_command(self, cmd: List[str]) -> Dict[str, Any]:
        """명령어 실행"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "result": stdout.strip() if process.returncode == 0 else "",
                "error": stderr.strip() if process.returncode != 0 else None,
                "command": " ".join(cmd)
            }
                
        except Exception as e:
            return {
                "success": False,
                "result": "",
                "error": f"실행 오류: {str(e)}",
                "command": " ".join(cmd)
            }

class WorkingCollaborativeAI:
    """실제 작동하는 협업 AI"""
    
    def __init__(self):
        self.cli = SimpleCLIExecutor()
        self.session_count = 0
    
    async def simple_collaboration(self, task: str) -> Dict[str, Any]:
        """간단한 협업 수행"""
        self.session_count += 1
        
        print(f"🤝 협업 세션 #{self.session_count} 시작: {task}", file=sys.stderr)
        
        # 1단계: Gemini에게 먼저 물어보기
        gemini_result = await self.cli.execute_command(["gemini", f"이 작업에 대해 분석해주세요: {task}"])
        
        # 2단계: Claude에게도 물어보기  
        claude_result = await self.cli.execute_command(["claude", f"이 작업에 대해 분석해주세요: {task}"])
        
        # 3단계: 두 결과 비교
        if gemini_result["success"] and claude_result["success"]:
            # 두 AI 모두 성공한 경우
            comparison_task = f"""
다음 두 AI의 분석을 비교하고 최선의 방법을 제안해주세요:

작업: {task}

Gemini 분석:
{gemini_result['result']}

Claude 분석:  
{claude_result['result']}

두 분석을 종합하여 최고의 솔루션을 제공해주세요.
"""
            final_result = await self.cli.execute_command(["claude", comparison_task])
            
            return {
                "task": task,
                "session_id": self.session_count,
                "workflow": "complete_collaboration",
                "gemini_analysis": gemini_result['result'],
                "claude_analysis": claude_result['result'], 
                "final_solution": final_result['result'] if final_result['success'] else "최종 분석 실패",
                "success": True,
                "message": "두 AI가 성공적으로 협업했습니다!"
            }
        
        elif gemini_result["success"]:
            # Gemini만 성공
            return {
                "task": task,
                "session_id": self.session_count,
                "workflow": "gemini_only",
                "result": gemini_result['result'],
                "success": True,
                "message": "Gemini가 작업을 완료했습니다."
            }
            
        elif claude_result["success"]:
            # Claude만 성공
            return {
                "task": task,
                "session_id": self.session_count,
                "workflow": "claude_only", 
                "result": claude_result['result'],
                "success": True,
                "message": "Claude가 작업을 완료했습니다."
            }
        
        else:
            # 둘 다 실패
            return {
                "task": task,
                "session_id": self.session_count,
                "workflow": "failed",
                "gemini_error": gemini_result['error'],
                "claude_error": claude_result['error'],
                "success": False,
                "message": "두 AI 모두 작업을 완료하지 못했습니다."
            }
    
    async def quick_chat(self, ai: str, message: str) -> Dict[str, Any]:
        """특정 AI와 빠른 대화"""
        if ai.lower() not in ["gemini", "claude"]:
            return {"error": "AI는 'gemini' 또는 'claude'여야 합니다."}
        
        result = await self.cli.execute_command([ai.lower(), message])
        return {
            "ai": ai,
            "message": message,
            "response": result['result'] if result['success'] else result['error'],
            "success": result['success']
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """통계 반환"""
        return {
            "total_sessions": self.session_count,
            "status": "operational",
            "available_ais": ["gemini", "claude"]
        }

# MCP 서버 설정
server = Server("working-collaborative-ai")
orchestrator = WorkingCollaborativeAI()

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """도구 목록 반환"""
    return ListToolsResult(
        tools=[
            Tool(
                name="collaborate",
                description="Gemini와 Claude가 협업하여 작업을 수행합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "수행할 작업 설명"
                        }
                    },
                    "required": ["task"]
                }
            ),
            Tool(
                name="chat_with_ai",
                description="특정 AI와 직접 대화합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "ai": {
                            "type": "string",
                            "enum": ["gemini", "claude"],
                            "description": "대화할 AI (gemini 또는 claude)"
                        },
                        "message": {
                            "type": "string", 
                            "description": "전달할 메시지"
                        }
                    },
                    "required": ["ai", "message"]
                }
            ),
            Tool(
                name="get_stats",
                description="협업 통계를 조회합니다",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """도구 호출 처리"""
    
    try:
        if request.name == "collaborate":
            task = request.params.get("task", "")
            if not task:
                return CallToolResult(
                    content=[TextContent(type="text", text="❌ 작업 설명이 필요합니다")]
                )
            
            print(f"🚀 협업 작업 시작: {task}", file=sys.stderr)
            result = await orchestrator.simple_collaboration(task)
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "chat_with_ai":
            ai = request.params.get("ai", "")
            message = request.params.get("message", "")
            
            if not ai or not message:
                return CallToolResult(
                    content=[TextContent(type="text", text="❌ AI와 메시지가 모두 필요합니다")]
                )
            
            result = await orchestrator.quick_chat(ai, message)
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "get_stats":
            stats = orchestrator.get_stats()
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(stats, ensure_ascii=False, indent=2))]
            )
        
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"❌ 알 수 없는 도구: {request.name}")]
            )
    
    except Exception as e:
        print(f"❌ 도구 실행 오류: {str(e)}", file=sys.stderr)
        return CallToolResult(
            content=[TextContent(type="text", text=f"❌ 오류: {str(e)}")]
        )

async def main():
    """MCP 서버 실행"""
    init_options = InitializationOptions(
        server_name="working-collaborative-ai",
        server_version="1.0.0",
        capabilities={}
    )
    
    print("🤝 Working Collaborative AI 서버 시작...", file=sys.stderr)
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                init_options
            )
    except Exception as e:
        print(f"❌ 서버 실행 중 오류: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())