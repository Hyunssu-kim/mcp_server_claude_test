# 🤝 MCP Collaborative AI Server

Gemini와 Claude CLI 도구를 통합하여 협업 작업을 수행하는 MCP 서버 컬렉션입니다.

## 📁 프로젝트 구조

```
🤝 MCP Collaborative AI Server/
├── 📂 src/                          # 소스 코드
│   ├── 🚀 servers/                  # MCP 서버들
│   │   ├── collaborative_ai_orchestrator.py  # 완전한 6단계 협업 워크플로우
│   │   ├── working_collaborative_server.py   # 실제 CLI 연동 협업 서버
│   │   ├── basic_collaborative_server.py     # CLI 없이 작동하는 기본 시뮬레이터
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

### 🧠 AI 협업 시뮬레이션
- **CLI 도구를 통한 작업 분배**
- **6단계 워크플로우**: 토론 → 초안 → 검토 → 개선 → 최종검토 → 평가
- **로그 기반 과정 모니터링**

### 🎯 사용 가능한 도구들
1. **enhanced_collaboration** - 작업 유형별 특화된 협업
2. **specialized_discussion** - 도메인별 전문 토론
3. **get_collaboration_stats** - 협업 통계 조회

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
# 향상된 협업 서버 실행
python src/servers/enhanced_collaborative_server.py

# 기본 시뮬레이션 서버 실행
python src/servers/basic_collaborative_server.py
```

### 4. Claude Desktop 설정
```json
{
  "mcpServers": {
    "collaborative-ai": {
      "command": "/usr/local/bin/python3",
      "args": ["/path/to/src/servers/enhanced_collaborative_server.py"]
    }
  }
}
```

## 💡 사용 예제

### 🤝 작업별 협업
```
enhanced_collaboration 도구로 "Python 웹앱 만들기"를 수행해주세요
```

### 💬 전문 토론
```
specialized_discussion 도구로 "AI의 미래"에 대해 토론해주세요
```

### 📊 통계 조회
```
get_collaboration_stats 도구로 협업 통계를 확인해주세요
```

## 🔍 모니터링

### 기본 로그 확인
```bash
# 서버 실행 시 콘솔 출력 확인
python src/servers/enhanced_collaborative_server.py
```

## 🛡️ 트러블슈팅

### MCP 서버가 인식되지 않을 때
1. Claude Desktop 재시작
2. 설정 파일 경로 확인
3. Python 경로 확인: `/usr/local/bin/python3`
4. 기본 서버로 테스트: `src/servers/basic_collaborative_server.py`

## 📚 추가 문서

- **[협업 시스템 설명](docs/README_COLLABORATIVE.md)** - 협업 워크플로우 상세 내용
- **[시스템 아키텍처](docs/SYSTEM_ARCHITECTURE.md)** - 기술적 구조 문서
- **[MCP 서버 정보](docs/CLAUDE.md)** - Claude Desktop 연동 가이드

## 🎨 협업 워크플로우

```
📝 1단계: 초기 토론
   ↓
✍️ 2단계: 초안 작성
   ↓  
🔍 3단계: 동료 검토
   ↓
🚀 4단계: 피드백 개선
   ↓
✅ 5단계: 최종 검토
   ↓
📊 6단계: 품질 평가
```

## 🤖 AI 역할 분담

- **🔸 Gemini**: 창의적 접근, 혁신적 아이디어, 사용자 중심 관점
- **🔹 Claude**: 논리적 분석, 체계적 구조, 기술적 정확성
- **🤝 협업**: 두 AI의 서로 다른 접근법을 결합한 균형잡힌 결과

## 📈 특징

- **다중 관점**을 고려한 문제 해결
- **작업 유형별** 특화된 응답 제공
- **동적 품질 점수** 생성 시스템
- **구체적 예시**와 실행 가능한 가이드

## 🔧 기술적 특징

- **JSON-RPC 2.0** 프로토콜 기반
- **비동기 처리** 지원
- **작업 유형 자동 분석**
- **통계 및 성과 추적**

## 🤝 기여하기

1. 이 저장소를 Fork
2. 새로운 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👥 제작자

- **AI Collaboration Project**
- **Email**: noreply@anthropic.com
- **GitHub**: [Hyunssu-kim](https://github.com/Hyunssu-kim)

---

Created with ❤️ by AI Collaboration Project  
Version: 2.0.0