# 💡 Examples

MCP Collaborative AI Server 사용 예제들입니다.

## 📄 예제 파일들

### run_example.py
- **기본 사용 예제**
- AI Orchestrator 기본 사용법
- 다양한 협업 시나리오 데모

**실행 방법:**
```bash
python examples/run_example.py
```

## 🎯 예제 시나리오들

### 1. 기본 협업 예제
```python
from src.servers.collaborative_ai_orchestrator import TaskOrchestrator

# 오케스트레이터 생성
orchestrator = TaskOrchestrator(gemini_key, claude_key)

# 협업 작업 실행
result = await orchestrator.create_and_execute_task(
    "Python으로 웹 크롤러를 만들어주세요"
)
```

### 2. 빠른 토론 예제
```python
# AI 간 토론
discussion = await orchestrator.quick_discussion(
    "인공지능의 미래 발전 방향"
)
```

### 3. 접근법 비교 예제
```python
# 두 AI의 접근법 비교
comparison = await orchestrator.compare_approaches(
    "대용량 데이터 처리 시스템 설계"
)
```

## 🔧 MCP 클라이언트 예제

### Claude Desktop에서 사용
```
collaborative_task 도구를 사용해서 "React 컴포넌트 설계"를 수행해주세요
```

### 직접 JSON-RPC 호출
```python
import json
import asyncio

# MCP 서버에 직접 요청
request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "collaborative_task",
        "arguments": {
            "task": "데이터베이스 스키마 설계"
        }
    }
}
```

## 📊 실시간 모니터링 예제

### 터미널 대시보드
```bash
# 시각적 모니터링
python src/tools/debug_dashboard.py
```

### 로그 스트리밍
```bash
# 실시간 로그 확인
./scripts/monitor_logs.sh
```

## 🎨 커스텀 워크플로우 예제

### 특화된 협업 시나리오
```python
# 코딩 특화 협업
coding_result = await orchestrator.execute_collaborative_task(
    "Python Flask API 서버 구현"
)

# 창작 특화 협업  
creative_result = await orchestrator.execute_collaborative_task(
    "마케팅 캠페인 아이디어 개발"
)

# 분석 특화 협업
analysis_result = await orchestrator.execute_collaborative_task(
    "시장 조사 데이터 분석 및 인사이트 도출"
)
```