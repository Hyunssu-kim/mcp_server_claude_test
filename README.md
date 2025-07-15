# 🤖 MCP AI Orchestration Server

질문을 받아 Gemini와 Claude CLI에 각각 전달하여 두 AI의 답변을 동시에 받을 수 있는 MCP 서버입니다.

## 📁 프로젝트 구조

```
🤝 MCP Collaborative AI Server/
├── 📂 src/                          # 소스 코드
│   ├── 🚀 servers/                  # MCP 서버들
│   │   ├── orchestration_server.py          # 메인 오케스트레이션 서버
│   │   ├── enhanced_collaborative_server.py # 기존 협업 서버 (레거시)
│   │   ├── basic_collaborative_server.py     # 기본 시뮬레이션 서버
│   │   ├── ultra_simple_server.py           # 테스트용 최소 MCP 서버
│   │   └── simple_test_server.py            # 간단한 테스트 서버
│   ├── 🛠️ tools/                   # 개발 도구들
│   │   └── debug_dashboard.py               # 시각적 협업 과정 대시보드
│   └── ⚙️ utils/                   # 유틸리티 함수들
├── 📂 scripts/                      # 실행 스크립트들
│   ├── start_collaborative_server.sh        # 서버 시작 (로그 포함)
│   ├── start_server.sh                     # 기본 서버 시작
│   ├── monitor_logs.sh                     # 실시간 로그 모니터링
│   └── check_claude_logs.sh               # Claude Desktop 로그 확인
├── 📂 configs/                      # 설정 파일들
│   ├── claude_desktop_config.json          # Claude Desktop 설정 예제
│   ├── config.json.example                 # 기본 설정 예제
│   └── mcp_config.json                     # MCP 서버 설정
├── 📂 examples/                     # 사용 예제들
│   └── run_example.py                      # 기본 사용 예제
├── 📂 docs/                         # 문서들
│   ├── README_COLLABORATIVE.md             # 상세한 협업 시스템 설명
│   ├── SYSTEM_ARCHITECTURE.md             # 시스템 구조 문서
│   ├── system_architecture_diagram.html    # 인터랙티브 다이어그램
│   └── CLAUDE.md                          # MCP 서버 정보
├── 📂 tests/                        # 테스트 코드들 (예정)
├── 📂 logs/                         # 로그 파일들
├── 📄 requirements.txt              # Python 의존성
├── 📄 .gitignore                   # Git 무시 파일들
└── 📄 README.md                    # 이 파일
```

## ✨ 주요 특징

### 🤖 AI 오케스트레이션
- **질문을 두 AI에게 동시 전달**
- **Gemini와 Claude CLI 연동**
- **각 AI의 순수한 답변 제공**
- **성격이나 역할 없이 있는 그대로 응답**

### 🎯 사용 가능한 도구들
1. **ask_both_ai** - 질문을 두 AI에게 동시 전달
2. **get_orchestration_stats** - 오케스트레이션 통계 조회

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/Hyunssu-kim/mcp_server_claude_test.git
cd mcp_server_claude_test
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
# 메인 오케스트레이션 서버 실행
python src/servers/orchestration_server.py

# 기본 시뮬레이션 서버 실행 (CLI 없이)
python src/servers/basic_collaborative_server.py
```

### 4. Claude Desktop 설정
```json
{
  "mcpServers": {
    "orchestration-ai": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/src/servers/orchestration_server.py"]
    }
  }
}
```

## 💡 사용 예제

### 🤖 두 AI에게 동시 질문
```
ask_both_ai 도구로 "Python 웹앱 만드는 방법"을 질문해주세요
```

### 📊 통계 조회
```
get_orchestration_stats 도구로 오케스트레이션 통계를 확인해주세요
```

### 🔍 CLI 도구 확인
```bash
# Gemini CLI 확인
which gemini

# Claude CLI 확인
which claude
```

## 🔍 모니터링

### 기본 로그 확인
```bash
# 서버 실행 시 콘솔 출력 확인
python src/servers/orchestration_server.py
```

## 🛡️ 트러블슈팅

### MCP 서버가 인식되지 않을 때
1. Claude Desktop 재시작
2. 설정 파일 경로 확인
3. Python 경로 확인: `/usr/local/bin/python3`
4. 기본 서버로 테스트: `src/servers/basic_collaborative_server.py`

### CLI 도구가 없을 때
1. Gemini CLI 설치 필요
2. Claude CLI 설치 필요
3. PATH 환경변수 확인

## 📚 추가 문서

- **[기존 협업 시스템](docs/README_COLLABORATIVE.md)** - 레거시 협업 워크플로우 참고
- **[시스템 아키텍처](docs/SYSTEM_ARCHITECTURE.md)** - 기술적 구조 문서
- **[MCP 서버 정보](docs/CLAUDE.md)** - Claude Desktop 연동 가이드

## 🎨 오케스트레이션 워크플로우

```
📝 질문 입력
   ↓
🔄 두 AI에게 동시 전달
   ↓
🔸 Gemini 응답    🔹 Claude 응답
   ↓                ↓
📊 결과 통합 및 표시
```

## 🤖 AI 응답 특성

- **🔸 Gemini**: 각자의 고유한 특성으로 답변
- **🔹 Claude**: 각자의 고유한 특성으로 답변
- **🤝 오케스트레이션**: 두 AI의 서로 다른 답변을 나란히 제공

## 📈 특징

- **동시 실행**으로 빠른 응답 수집
- **CLI 직접 연동**으로 순수한 AI 답변
- **간단한 구조**로 이해하기 쉬움
- **비교 분석**을 통한 다양한 관점 제공

## 🔧 기술적 특징

- **JSON-RPC 2.0** 프로토콜 기반
- **비동기 처리**로 동시 실행
- **CLI 프로세스 관리**
- **간단한 통계 추적**

## 🤝 기여하기

1. 이 저장소를 Fork
2. 새로운 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👥 제작자

- **Hyunssu Kim**
- **Email**: foxkim951@naver.com
- **GitHub**: [Hyunssu-kim](https://github.com/Hyunssu-kim)