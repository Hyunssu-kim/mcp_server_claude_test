# 🧪 Tests

MCP 서버 및 협업 기능을 위한 테스트 코드들입니다.

## 📋 테스트 계획

### 단위 테스트 (예정)
- [ ] MCP 서버 기본 기능 테스트
- [ ] CLI 실행기 테스트
- [ ] 워크플로우 단계별 테스트
- [ ] 에러 처리 테스트

### 통합 테스트 (예정)
- [ ] 전체 협업 워크플로우 테스트
- [ ] Claude Desktop 연동 테스트
- [ ] 실시간 로깅 테스트

### 성능 테스트 (예정)
- [ ] 동시 요청 처리 테스트
- [ ] 메모리 사용량 테스트
- [ ] 응답 시간 측정

## 🚀 테스트 실행

```bash
# 단위 테스트
python -m pytest tests/unit/

# 통합 테스트  
python -m pytest tests/integration/

# 전체 테스트
python -m pytest tests/
```

## 📂 테스트 구조 (예정)

```
tests/
├── unit/
│   ├── test_mcp_server.py
│   ├── test_cli_executor.py
│   └── test_workflow.py
├── integration/
│   ├── test_collaboration_flow.py
│   └── test_claude_desktop.py
└── fixtures/
    ├── sample_requests.json
    └── mock_responses.json
```