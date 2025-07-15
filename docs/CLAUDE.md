# MCP AI Orchestrator

## MCP Server Configuration

이 프로젝트는 MCP (Model Context Protocol) 서버를 포함하고 있습니다.

### 서버 정보
- **이름**: ai-orchestrator
- **설명**: Gemini가 작업을 분석하고 Gemini/Claude CLI에 할당하는 오케스트레이터
- **실행 파일**: mcp_ai_orchestrator.py

### 사용 가능한 도구
1. `execute_task` - 작업 자동 할당 및 실행
2. `execute_parallel_tasks` - 여러 작업 병렬 실행
3. `execute_gemini` - Gemini CLI 직접 실행
4. `execute_claude` - Claude CLI 직접 실행
5. `get_statistics` - 작업 통계 조회

### 설정 방법

Claude Desktop의 설정 파일에 다음을 추가:

```json
{
  "mcpServers": {
    "ai-orchestrator": {
      "command": "python3",
      "args": ["/Users/kimhyunsu/Desktop/Developer/MCP_server/mcp_ai_orchestrator.py"],
      "env": {}
    }
  }
}
```

### 필수 조건
- `gemini` CLI 도구가 설치되어 있어야 함
- `claude` CLI 도구가 설치되어 있어야 함
- Python MCP 라이브러리: `pip install mcp`

### 실행 방법
```bash
./start_server.sh
```