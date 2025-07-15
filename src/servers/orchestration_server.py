#!/usr/bin/env python3
"""
Orchestration Server - 질문을 받아 gemini와 claude에 각각 전달하여 두 답변을 반환하는 서버
"""
import asyncio
import json
import sys
from datetime import datetime

class AIOrchestrator:
    """AI 오케스트레이터 - 질문을 두 AI에게 전달하고 답변 수집"""
    
    def __init__(self):
        self.request_count = 0
    
    async def ask_gemini(self, question: str) -> str:
        """Gemini CLI에 질문 전달"""
        try:
            process = await asyncio.create_subprocess_exec(
                'gemini', question,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return stdout.decode().strip()
            else:
                return f"Gemini 오류: {stderr.decode().strip()}"
        except FileNotFoundError:
            return "Gemini CLI가 설치되지 않았습니다."
        except Exception as e:
            return f"Gemini 실행 오류: {str(e)}"
    
    async def ask_claude(self, question: str) -> str:
        """Claude CLI에 질문 전달"""
        try:
            process = await asyncio.create_subprocess_exec(
                'claude', question,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return stdout.decode().strip()
            else:
                return f"Claude 오류: {stderr.decode().strip()}"
        except FileNotFoundError:
            return "Claude CLI가 설치되지 않았습니다."
        except Exception as e:
            return f"Claude 실행 오류: {str(e)}"
    
    async def orchestrate_question(self, question: str) -> str:
        """질문을 두 AI에게 동시에 전달하고 답변 수집"""
        self.request_count += 1
        
        # 두 AI에게 동시에 질문 전달
        gemini_task = self.ask_gemini(question)
        claude_task = self.ask_claude(question)
        
        # 동시 실행하여 답변 수집
        gemini_response, claude_response = await asyncio.gather(
            gemini_task, claude_task, return_exceptions=True
        )
        
        # 예외 처리
        if isinstance(gemini_response, Exception):
            gemini_response = f"Gemini 오류: {str(gemini_response)}"
        if isinstance(claude_response, Exception):
            claude_response = f"Claude 오류: {str(claude_response)}"
        
        # 결과 포맷팅
        return f"""🤖 AI 오케스트레이션 결과

📋 질문: {question}

🔸 Gemini 답변:
{gemini_response}

🔹 Claude 답변:
{claude_response}

⏰ 처리 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 총 요청 수: {self.request_count}"""

    def get_stats(self) -> str:
        """오케스트레이션 통계"""
        return f"""📊 오케스트레이션 통계

🎯 총 요청 수: {self.request_count}회
🤖 연동 AI: Gemini, Claude
⏰ 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🚀 시스템 상태: 정상 작동"""

# 전역 오케스트레이터
orchestrator = AIOrchestrator()

async def main():
    """MCP 서버 메인 루프"""
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, input)
            if not line:
                break
                
            data = json.loads(line)
            
            if data.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "orchestration-ai",
                            "version": "1.0.0"
                        }
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
                
            elif data.get("method") == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "ask_both_ai",
                                "description": "질문을 Gemini와 Claude에게 동시에 전달하여 두 답변을 받습니다",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "question": {"type": "string", "description": "질문 내용"}
                                    },
                                    "required": ["question"]
                                }
                            },
                            {
                                "name": "get_orchestration_stats",
                                "description": "오케스트레이션 통계 정보를 조회합니다",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            }
                        ]
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
                
            elif data.get("method") == "tools/call":
                tool_name = data.get("params", {}).get("name")
                arguments = data.get("params", {}).get("arguments", {})
                
                if tool_name == "ask_both_ai":
                    question = arguments.get("question", "")
                    result_text = await orchestrator.orchestrate_question(question)
                    
                elif tool_name == "get_orchestration_stats":
                    result_text = orchestrator.get_stats()
                    
                else:
                    result_text = f"❌ 알 수 없는 도구: {tool_name}"
                
                response = {
                    "jsonrpc": "2.0", 
                    "id": data.get("id"),
                    "result": {
                        "content": [{"type": "text", "text": result_text}]
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
                
        except EOFError:
            break
        except Exception as e:
            print(f"오류: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())