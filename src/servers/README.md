# 🚀 MCP Servers Collection

다양한 협업 AI MCP 서버들을 포함합니다.

## 📂 서버 파일들

### 🤝 collaborative_ai_orchestrator.py
- **완전한 6단계 협업 워크플로우**
- Gemini와 Claude가 실제로 대화하고 협업
- 실시간 로깅 및 모니터링
- 모든 협업 도구 포함

**사용법:**
```bash
python collaborative_ai_orchestrator.py
```

**Claude Desktop 설정:**
```json
{
  "mcpServers": {
    "collaborative-ai": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/collaborative_ai_orchestrator.py"]
    }
  }
}
```

### 💼 working_collaborative_server.py
- **실제 CLI 연동 협업 서버**
- gemini/claude CLI 명령어 활용
- 간소화된 협업 워크플로우
- 안정적인 구조

### 🎯 basic_collaborative_server.py
- **CLI 없이 작동하는 기본 시뮬레이터**
- gemini/claude CLI 도구가 없어도 사용 가능
- 협업 과정 시뮬레이션
- 테스트 및 데모용

### 🔧 ultra_simple_server.py
- **테스트용 최소 MCP 서버**
- 기본 MCP 프로토콜 구현
- 연결 테스트용
- 디버깅 및 문제 해결용

### 📝 simple_test_server.py
- **간단한 테스트 서버**
- MCP 서버 기능 검증
- 기본 도구 테스트

### 🎭 mcp_ai_orchestrator.py
- **초기 버전 MCP 서버**
- 기본적인 오케스트레이션 기능
- 레거시 버전

### 🏗️ ai_orchestrator.py
- **CLI 기반 오케스트레이터**
- 터미널에서 직접 실행 가능
- 비-MCP 버전

## 🎯 추천 사용 순서

1. **ultra_simple_server.py** - 연결 테스트
2. **basic_collaborative_server.py** - 기본 협업 체험
3. **collaborative_ai_orchestrator.py** - 완전한 협업 시스템

## 🔧 공통 요구사항

- Python 3.11+
- MCP 라이브러리: `pip install mcp`
- Claude Desktop
- (선택사항) Gemini/Claude CLI 도구

## 🚀 서버 선택 가이드

| 상황 | 추천 서버 |
|------|-----------|
| 처음 테스트 | ultra_simple_server.py |
| CLI 도구 없음 | basic_collaborative_server.py |
| 완전한 협업 체험 | collaborative_ai_orchestrator.py |
| 안정성 우선 | working_collaborative_server.py |
| 문제 해결 | simple_test_server.py |