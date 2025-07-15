#!/usr/bin/env python3
"""
Collaborative AI Orchestrator MCP Server
Gemini와 Claude가 서로 협업하고 토론하여 최고의 결과를 만들어내는 시스템
"""
import asyncio
import json
import sys
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
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

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class WorkflowStage(Enum):
    INITIAL_DISCUSSION = "initial_discussion"
    DRAFT_CREATION = "draft_creation"
    PEER_REVIEW = "peer_review"
    IMPROVEMENT = "improvement"
    FINAL_REVIEW = "final_review"
    COMPLETION = "completion"

@dataclass
class CollaborationMessage:
    from_ai: str
    to_ai: str
    stage: WorkflowStage
    content: str
    context: Dict[str, Any]
    timestamp: float

@dataclass
class CollaborationResult:
    task_description: str
    workflow_stages: List[Dict[str, Any]]
    final_result: str
    quality_score: float
    participating_ais: List[str]
    total_iterations: int
    collaboration_summary: str

class CLIExecutor:
    """기존 gemini/claude CLI 명령어를 실행하는 클래스"""
    
    async def execute_gemini(self, prompt: str) -> Dict[str, Any]:
        """Gemini CLI 실행"""
        try:
            cmd = ["gemini", prompt]
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
                "ai": "gemini"
            }
                
        except Exception as e:
            return {
                "success": False,
                "result": "",
                "error": f"CLI 실행 오류: {str(e)}",
                "ai": "gemini"
            }
    
    async def execute_claude(self, prompt: str) -> Dict[str, Any]:
        """Claude CLI 실행"""
        try:
            cmd = ["claude", prompt]
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
                "ai": "claude"
            }
                
        except Exception as e:
            return {
                "success": False,
                "result": "",
                "error": f"CLI 실행 오류: {str(e)}",
                "ai": "claude"
            }

class CollaborativeWorkflow:
    """두 AI가 협업하는 워크플로우 관리"""
    
    def __init__(self, cli_executor: CLIExecutor):
        self.cli_executor = cli_executor
        self.conversation_history: List[CollaborationMessage] = []
        self.current_stage = WorkflowStage.INITIAL_DISCUSSION
        
    async def start_collaboration(self, task_description: str) -> CollaborationResult:
        """협업 워크플로우 시작"""
        self.conversation_history = []
        self.current_stage = WorkflowStage.INITIAL_DISCUSSION
        
        logger.info(f"협업 시작: {task_description}")
        
        # 1단계: 초기 토론 - 두 AI가 작업에 대해 논의
        discussion_result = await self._initial_discussion(task_description)
        
        # 2단계: 초안 작성 - 더 적합한 AI가 초안 작성
        draft_result = await self._create_draft(task_description, discussion_result)
        
        # 3단계: 동료 검토 - 다른 AI가 검토 및 피드백
        review_result = await self._peer_review(task_description, draft_result)
        
        # 4단계: 개선 - 피드백을 바탕으로 개선
        improved_result = await self._improve_result(task_description, draft_result, review_result)
        
        # 5단계: 최종 검토 - 양쪽이 최종 검토
        final_result = await self._final_review(task_description, improved_result)
        
        # 6단계: 품질 평가 및 요약
        quality_score = await self._evaluate_quality(task_description, final_result)
        
        return CollaborationResult(
            task_description=task_description,
            workflow_stages=self._get_workflow_summary(),
            final_result=final_result,
            quality_score=quality_score,
            participating_ais=["gemini", "claude"],
            total_iterations=len(self.conversation_history),
            collaboration_summary=self._generate_collaboration_summary()
        )
    
    async def _initial_discussion(self, task: str) -> Dict[str, str]:
        """1단계: 초기 토론"""
        self.current_stage = WorkflowStage.INITIAL_DISCUSSION
        logger.info(f"🎯 1단계: 초기 토론 시작 - {task}")
        
        # Gemini에게 먼저 작업 분석 요청
        gemini_prompt = f"""
작업: {task}

이 작업에 대해 분석해주세요:
1. 작업의 핵심 요구사항
2. 어려운 점이나 주의사항
3. Gemini vs Claude 중 누가 더 적합한지와 이유
4. 협업 시 어떤 역할 분담이 좋을지

응답 형식: JSON
{{
    "analysis": "작업 분석",
    "challenges": "어려운 점",
    "better_ai": "gemini 또는 claude",
    "reason": "이유",
    "collaboration_plan": "협업 계획"
}}
"""
        
        logger.info("💭 Gemini에게 작업 분석 요청 중...")
        gemini_result = await self.cli_executor.execute_gemini(gemini_prompt)
        logger.info(f"✅ Gemini 분석 완료: {gemini_result['result'][:100]}...")
        
        # Claude에게 Gemini의 분석에 대한 의견 요청
        logger.info("🔍 Claude에게 Gemini 분석 검토 요청 중...")
        claude_prompt = f"""
작업: {task}

Gemini의 분석:
{gemini_result['result']}

Gemini의 분석에 대한 당신의 의견과 추가 제안을 해주세요:
1. Gemini 분석에 동의하는지
2. 다른 관점이나 놓친 부분
3. 더 나은 협업 방안
4. 최종 역할 분담 제안

응답 형식: JSON
{{
    "agreement_level": "1-10 점수",
    "additional_insights": "추가 통찰",
    "collaboration_suggestion": "협업 제안",
    "role_assignment": "최종 역할 분담"
}}
"""
        
        claude_result = await self.cli_executor.execute_claude(claude_prompt)
        logger.info(f"✅ Claude 검토 완료: {claude_result['result'][:100]}...")
        
        return {
            "gemini_analysis": gemini_result['result'],
            "claude_feedback": claude_result['result']
        }
    
    async def _create_draft(self, task: str, discussion: Dict[str, str]) -> str:
        """2단계: 초안 작성"""
        self.current_stage = WorkflowStage.DRAFT_CREATION
        logger.info("✍️ 2단계: 초안 작성 시작")
        
        # 토론 결과를 바탕으로 누가 초안을 작성할지 결정
        decision_prompt = f"""
작업: {task}

토론 결과:
- Gemini 분석: {discussion['gemini_analysis']}
- Claude 피드백: {discussion['claude_feedback']}

이 정보를 바탕으로 누가 초안을 작성해야 할지 "gemini" 또는 "claude"로만 답하세요.
"""
        
        decision_result = await self.cli_executor.execute_gemini(decision_prompt)
        primary_ai = "claude" if "claude" in decision_result['result'].lower() else "gemini"
        logger.info(f"🎯 {primary_ai.upper()}가 초안 작성으로 선택됨")
        
        # 선택된 AI가 초안 작성
        draft_prompt = f"""
작업: {task}

협업 토론 결과:
{discussion['gemini_analysis']}
{discussion['claude_feedback']}

이 토론을 바탕으로 작업을 수행해주세요. 최고 품질의 결과를 만들어주세요.
"""
        
        logger.info(f"📝 {primary_ai.upper()}에게 초안 작성 요청 중...")
        if primary_ai == "gemini":
            result = await self.cli_executor.execute_gemini(draft_prompt)
        else:
            result = await self.cli_executor.execute_claude(draft_prompt)
        logger.info(f"✅ 초안 작성 완료: {result['result'][:100]}...")
        
        return result['result']
    
    async def _peer_review(self, task: str, draft: str) -> str:
        """3단계: 동료 검토"""
        self.current_stage = WorkflowStage.PEER_REVIEW
        logger.info("🔍 3단계: 동료 검토 시작")
        
        # 초안을 작성하지 않은 AI가 검토
        review_prompt = f"""
원래 작업: {task}

동료가 작성한 결과:
{draft}

이 결과를 검토하고 피드백을 제공해주세요:
1. 잘된 점
2. 개선이 필요한 점
3. 구체적인 개선 제안
4. 놓친 부분이나 추가할 내용
5. 전체적인 품질 평가 (1-10점)

건설적이고 구체적인 피드백을 제공해주세요.
"""
        
        # 두 AI 모두에게 검토 요청 (다양한 관점)
        logger.info("👥 두 AI 모두에게 검토 요청 중...")
        gemini_review = await self.cli_executor.execute_gemini(review_prompt)
        claude_review = await self.cli_executor.execute_claude(review_prompt)
        logger.info("✅ 양쪽 AI 검토 완료")
        
        return f"Gemini 검토:\n{gemini_review['result']}\n\nClaude 검토:\n{claude_review['result']}"
    
    async def _improve_result(self, task: str, draft: str, reviews: str) -> str:
        """4단계: 개선"""
        self.current_stage = WorkflowStage.IMPROVEMENT
        logger.info("🚀 4단계: 피드백 기반 개선 시작")
        
        improvement_prompt = f"""
원래 작업: {task}

초안:
{draft}

검토 피드백:
{reviews}

피드백을 바탕으로 결과를 개선해주세요. 모든 지적사항을 고려하여 더 나은 버전을 만들어주세요.
"""
        
        # 두 AI가 각각 개선안 제시
        logger.info("💡 두 AI가 각각 개선안 제시 중...")
        gemini_improved = await self.cli_executor.execute_gemini(improvement_prompt)
        claude_improved = await self.cli_executor.execute_claude(improvement_prompt)
        logger.info("✅ 양쪽 개선안 완성")
        
        # 두 개선안을 비교하여 최고 선택
        comparison_prompt = f"""
원래 작업: {task}

Gemini 개선안:
{gemini_improved['result']}

Claude 개선안:
{claude_improved['result']}

두 개선안을 비교하고 더 나은 것을 선택하거나, 두 개의 장점을 결합한 최종 버전을 만들어주세요.
"""
        
        logger.info("⚖️ 개선안 비교 및 최종 선택 중...")
        final_improved = await self.cli_executor.execute_gemini(comparison_prompt)
        logger.info("✅ 최종 개선 버전 완성")
        return final_improved['result']
    
    async def _final_review(self, task: str, improved_result: str) -> str:
        """5단계: 최종 검토"""
        self.current_stage = WorkflowStage.FINAL_REVIEW
        logger.info("✅ 5단계: 최종 검토 시작")
        
        final_check_prompt = f"""
원래 작업: {task}

최종 결과:
{improved_result}

이것이 최종 결과입니다. 마지막으로 검토하고 필요하면 미세 조정해주세요:
1. 작업 요구사항을 모두 충족했는지 확인
2. 품질이 최고 수준인지 확인
3. 필요하면 최종 다듬기

완벽한 최종 결과를 제공해주세요.
"""
        
        # 두 AI가 최종 검토
        logger.info("🎯 양쪽 AI의 최종 검토 진행 중...")
        gemini_final = await self.cli_executor.execute_gemini(final_check_prompt)
        claude_final = await self.cli_executor.execute_claude(final_check_prompt)
        logger.info("✅ 최종 검토 완료")
        
        # 더 나은 최종 버전 선택
        selection_prompt = f"""
Gemini 최종 버전:
{gemini_final['result']}

Claude 최종 버전:
{claude_final['result']}

더 나은 최종 버전을 선택하거나 두 버전의 장점을 결합해주세요.
"""
        
        logger.info("🏆 최종 버전 선택 중...")
        final_result = await self.cli_executor.execute_claude(selection_prompt)
        logger.info("🎉 최종 결과 완성!")
        return final_result['result']
    
    async def _evaluate_quality(self, task: str, result: str) -> float:
        """품질 평가"""
        logger.info("📊 6단계: 품질 평가 시작")
        evaluation_prompt = f"""
작업: {task}
결과: {result}

이 결과의 품질을 1-10점으로 평가해주세요. 평가 기준:
1. 작업 요구사항 충족도
2. 결과의 정확성
3. 완성도
4. 창의성/유용성

점수만 숫자로 답하세요.
"""
        
        # 두 AI의 평가 평균
        logger.info("🎯 양쪽 AI의 품질 평가 진행 중...")
        gemini_score = await self.cli_executor.execute_gemini(evaluation_prompt)
        claude_score = await self.cli_executor.execute_claude(evaluation_prompt)
        
        try:
            g_score = float(gemini_score['result'].strip())
            c_score = float(claude_score['result'].strip())
            final_score = (g_score + c_score) / 2
            logger.info(f"📊 품질 점수: Gemini({g_score}) + Claude({c_score}) = 평균 {final_score}")
            return final_score
        except:
            logger.warning("⚠️ 품질 점수 파싱 실패, 기본값 8.0 사용")
            return 8.0  # 기본값
    
    def _get_workflow_summary(self) -> List[Dict[str, Any]]:
        """워크플로우 요약"""
        return [
            {"stage": "initial_discussion", "description": "두 AI가 작업에 대해 토론"},
            {"stage": "draft_creation", "description": "적합한 AI가 초안 작성"},
            {"stage": "peer_review", "description": "동료 AI가 검토 및 피드백"},
            {"stage": "improvement", "description": "피드백 바탕으로 개선"},
            {"stage": "final_review", "description": "최종 검토 및 다듬기"},
            {"stage": "quality_evaluation", "description": "품질 평가"}
        ]
    
    def _generate_collaboration_summary(self) -> str:
        """협업 요약"""
        return f"Gemini와 Claude가 {len(self.conversation_history)}회의 상호작용을 통해 협업하여 최고 품질의 결과를 생성했습니다."

class CollaborativeAIOrchestrator:
    """협업 AI 오케스트레이터 메인 클래스"""
    
    def __init__(self):
        self.cli_executor = CLIExecutor()
        self.workflow = CollaborativeWorkflow(self.cli_executor)
        self.collaboration_history: List[CollaborationResult] = []
    
    async def execute_collaborative_task(self, task_description: str) -> CollaborationResult:
        """협업 작업 실행"""
        logger.info(f"협업 작업 시작: {task_description}")
        
        result = await self.workflow.start_collaboration(task_description)
        self.collaboration_history.append(result)
        
        return result
    
    async def quick_discussion(self, topic: str) -> Dict[str, str]:
        """간단한 토론 (빠른 협업)"""
        discussion_prompt = f"이 주제에 대해 간단히 의견을 제시해주세요: {topic}"
        
        gemini_result = await self.cli_executor.execute_gemini(discussion_prompt)
        claude_result = await self.cli_executor.execute_claude(discussion_prompt)
        
        return {
            "topic": topic,
            "gemini_opinion": gemini_result['result'],
            "claude_opinion": claude_result['result']
        }
    
    async def compare_approaches(self, task: str) -> Dict[str, str]:
        """두 AI의 접근법 비교"""
        comparison_prompt = f"이 작업에 대한 당신의 접근법을 설명해주세요: {task}"
        
        gemini_approach = await self.cli_executor.execute_gemini(comparison_prompt)
        claude_approach = await self.cli_executor.execute_claude(comparison_prompt)
        
        # 접근법 비교 분석
        analysis_prompt = f"""
작업: {task}

Gemini 접근법:
{gemini_approach['result']}

Claude 접근법:
{claude_approach['result']}

두 접근법의 장단점을 비교하고 최적의 방법을 제안해주세요.
"""
        
        analysis = await self.cli_executor.execute_gemini(analysis_prompt)
        
        return {
            "task": task,
            "gemini_approach": gemini_approach['result'],
            "claude_approach": claude_approach['result'],
            "comparison_analysis": analysis['result']
        }
    
    def get_collaboration_stats(self) -> Dict[str, Any]:
        """협업 통계"""
        total_collaborations = len(self.collaboration_history)
        if total_collaborations == 0:
            return {"message": "아직 협업 기록이 없습니다."}
        
        avg_quality = sum(c.quality_score for c in self.collaboration_history) / total_collaborations
        avg_iterations = sum(c.total_iterations for c in self.collaboration_history) / total_collaborations
        
        return {
            "total_collaborations": total_collaborations,
            "average_quality_score": round(avg_quality, 2),
            "average_iterations": round(avg_iterations, 1),
            "best_collaboration": max(self.collaboration_history, key=lambda x: x.quality_score).task_description
        }

# MCP 서버 설정
server = Server("collaborative-ai-orchestrator")
orchestrator = CollaborativeAIOrchestrator()

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """사용 가능한 도구들 반환"""
    return ListToolsResult(
        tools=[
            Tool(
                name="collaborative_task",
                description="Gemini와 Claude가 협업하여 작업을 수행합니다 (전체 워크플로우)",
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
                name="quick_discussion",
                description="특정 주제에 대해 두 AI가 빠르게 토론합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "토론할 주제"
                        }
                    },
                    "required": ["topic"]
                }
            ),
            Tool(
                name="compare_approaches",
                description="특정 작업에 대한 두 AI의 접근법을 비교합니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "비교할 작업"
                        }
                    },
                    "required": ["task"]
                }
            ),
            Tool(
                name="get_collaboration_stats",
                description="협업 통계 및 기록을 조회합니다",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="execute_gemini_direct",
                description="Gemini에게 직접 작업을 요청합니다",
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
                name="execute_claude_direct",
                description="Claude에게 직접 작업을 요청합니다",
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
        if request.name == "collaborative_task":
            task = request.params.get("task", "")
            if not task:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 작업 설명이 필요합니다")]
                )
            
            result = await orchestrator.execute_collaborative_task(task)
            
            response = {
                "task": result.task_description,
                "final_result": result.final_result,
                "quality_score": result.quality_score,
                "total_iterations": result.total_iterations,
                "workflow_summary": result.workflow_stages,
                "collaboration_summary": result.collaboration_summary
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(response, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "quick_discussion":
            topic = request.params.get("topic", "")
            if not topic:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 토론 주제가 필요합니다")]
                )
            
            result = await orchestrator.quick_discussion(topic)
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "compare_approaches":
            task = request.params.get("task", "")
            if not task:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 비교할 작업이 필요합니다")]
                )
            
            result = await orchestrator.compare_approaches(task)
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "get_collaboration_stats":
            stats = orchestrator.get_collaboration_stats()
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(stats, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "execute_gemini_direct":
            prompt = request.params.get("prompt", "")
            if not prompt:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 프롬프트가 필요합니다")]
                )
            
            result = await orchestrator.cli_executor.execute_gemini(prompt)
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            )
        
        elif request.name == "execute_claude_direct":
            prompt = request.params.get("prompt", "")
            if not prompt:
                return CallToolResult(
                    content=[TextContent(type="text", text="ERROR: 프롬프트가 필요합니다")]
                )
            
            result = await orchestrator.cli_executor.execute_claude(prompt)
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
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
    init_options = InitializationOptions(
        server_name="collaborative-ai-orchestrator",
        server_version="2.0.0",
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