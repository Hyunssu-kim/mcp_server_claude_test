# ⚙️ Configuration Files

MCP 서버 및 Claude Desktop 설정 파일들입니다.

## 📄 설정 파일들

### claude_desktop_config.json
- **Claude Desktop MCP 서버 설정**
- 실제 사용된 설정 예제
- 서버 연결 정보 포함

**설치 위치:**
```bash
# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Windows
%APPDATA%\Claude\claude_desktop_config.json

# Linux
~/.config/Claude/claude_desktop_config.json
```

**기본 설정:**
```json
{
  "mcpServers": {
    "collaborative-ai": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/src/servers/collaborative_ai_orchestrator.py"]
    }
  }
}
```

### config.json.example
- **기본 서버 설정 예제**
- API 키 및 환경 설정
- 개발 환경 설정 템플릿

**사용법:**
```bash
cp configs/config.json.example config.json
# config.json 파일을 편집하여 실제 값 입력
```

### mcp_config.json
- **MCP 서버 메타데이터**
- 서버 정보 및 capabilities
- 개발 참고용

## 🔧 설정 가이드

### 1. Claude Desktop 설정

기본 설정:
```json
{
  "mcpServers": {
    "collaborative-ai": {
      "command": "/usr/local/bin/python3",
      "args": ["/Users/your-username/path/to/src/servers/collaborative_ai_orchestrator.py"],
      "env": {
        "PYTHONPATH": "/usr/local/lib/python3.11/site-packages",
        "PATH": "/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

고급 설정 (환경 변수 포함):
```json
{
  "mcpServers": {
    "collaborative-ai": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/collaborative_ai_orchestrator.py"],
      "env": {
        "PYTHONPATH": "/usr/local/lib/python3.11/site-packages",
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "GEMINI_API_KEY": "your-api-key",
        "CLAUDE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 2. 다중 서버 설정

여러 서버를 동시에 사용:
```json
{
  "mcpServers": {
    "collaborative-ai-full": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/collaborative_ai_orchestrator.py"]
    },
    "collaborative-ai-basic": {
      "command": "/usr/local/bin/python3", 
      "args": ["/path/to/basic_collaborative_server.py"]
    },
    "test-server": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/ultra_simple_server.py"]
    }
  }
}
```

## 🚨 주의사항

### 보안
- API 키는 환경 변수 또는 별도 설정 파일로 관리
- 설정 파일에 민감한 정보 포함 금지
- `.gitignore`에 실제 설정 파일 등록

### 경로 설정
- **절대 경로** 사용 권장
- Python 경로 정확히 확인: `which python3`
- 스크립트 파일 실행 권한 확인: `chmod +x`

### 환경 변수
```bash
# Python 경로 확인
which python3

# MCP 라이브러리 확인
python3 -c "import mcp; print('MCP installed')"

# 서버 테스트
echo '{"jsonrpc":"2.0","method":"initialize"}' | python3 server.py
```

## 🔧 트러블슈팅

### 일반적인 문제들

**서버가 인식되지 않을 때:**
1. Claude Desktop 완전 재시작
2. 설정 파일 JSON 문법 확인
3. 파일 경로 및 권한 확인
4. Python 및 MCP 라이브러리 설치 확인

**설정 파일 확인:**
```bash
# JSON 문법 검증
python3 -m json.tool configs/claude_desktop_config.json

# 파일 권한 확인
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
```