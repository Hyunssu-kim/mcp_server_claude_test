#!/usr/bin/env python3
"""
간단한 테스트용 MCP 서버
"""
import asyncio
import json
import sys

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

# MCP 서버 생성
server = Server("test-collaborative-ai")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """사용 가능한 도구들 반환"""
    return ListToolsResult(
        tools=[
            Tool(
                name="test_collaboration",
                description="간단한 협업 테스트 도구입니다",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "테스트 메시지"
                        }
                    },
                    "required": ["message"]
                }
            ),
            Tool(
                name="hello_world",
                description="Hello World를 반환합니다",
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
    
    if request.name == "test_collaboration":
        message = request.params.get("message", "")
        response = {
            "status": "success",
            "message": f"협업 테스트 완료: {message}",
            "timestamp": asyncio.get_event_loop().time()
        }
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(response, ensure_ascii=False, indent=2))]
        )
    
    elif request.name == "hello_world":
        response = {
            "message": "Hello from Collaborative AI Server!",
            "status": "working"
        }
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(response, ensure_ascii=False, indent=2))]
        )
    
    else:
        return CallToolResult(
            content=[TextContent(type="text", text=f"ERROR: 알 수 없는 도구: {request.name}")]
        )

async def main():
    """MCP 서버 실행"""
    init_options = InitializationOptions(
        server_name="test-collaborative-ai",
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
        print(f"서버 실행 중 오류: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())