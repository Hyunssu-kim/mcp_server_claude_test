# 🤝 MCP Collaborative AI Server

Gemini와 Claude가 협업하여 최고 품질의 결과를 만들어내는 혁신적인 MCP 서버 컬렉션입니다.

## 📁 프로젝트 구조

### 🚀 메인 서버들
- `collaborative_ai_orchestrator.py` - 완전한 6단계 협업 워크플로우
- `working_collaborative_server.py` - 실제 CLI 연동 협업 서버
- `basic_collaborative_server.py` - CLI 없이 작동하는 기본 협업 시뮬레이터
- `ultra_simple_server.py` - 테스트용 최소 MCP 서버

### 🛠️ 유틸리티
- `start_collaborative_server.sh` - 서버 시작 스크립트 (로그 포함)
- `monitor_logs.sh` - 실시간 로그 모니터링
- `debug_dashboard.py` - 시각적 협업 과정 대시보드
- `check_claude_logs.sh` - Claude Desktop 로그 확인

### 📋 설정 및 예제
- `claude_desktop_config.json.example` - Claude Desktop 설정 예제
- `mcp_config.json` - MCP 서버 설정
- `requirements.txt` - Python 의존성
- `run_example.py` - 사용 예제

### 📚 문서
- `README_COLLABORATIVE.md` - 상세한 협업 시스템 설명
- `CLAUDE.md` - MCP 서버 정보

## ✨ 주요 특징

### 🧠 진짜 협업 AI
- **Gemini와 Claude가 실제로 대화하고 토론**
- **6단계 협업 워크플로우**: 토론 → 초안 → 검토 → 개선 → 최종검토 → 평가
- **실시간 협업 과정 모니터링**

### 🎯 사용 가능한 도구들
1. **collaborative_task** - 완전한 협업 워크플로우
2. **quick_discussion** - 빠른 AI 토론
3. **compare_approaches** - 접근법 비교 분석
4. **get_collaboration_stats** - 협업 통계 조회
5. **simulate_collaboration** - 협업 시뮬레이션
6. **ai_discussion** - AI 토론 시뮬레이션

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Claude Desktop 설정
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

### 3. 서버 실행
```bash
# 기본 실행
python3 collaborative_ai_orchestrator.py

# 로그와 함께 실행
./start_collaborative_server.sh

# 실시간 모니터링
python3 debug_dashboard.py
```

## 💡 사용 예제

### 🤝 완전한 협업
```
collaborative_task 도구로 "Python 웹앱 만들기"를 수행해주세요
```

### 💬 빠른 토론
```
quick_discussion 도구로 "AI의 미래"에 대해 토론해주세요
```

### ⚖️ 접근법 비교
```
compare_approaches 도구로 "데이터베이스 설계" 방법을 비교해주세요
```

## 🔍 실시간 모니터링

### 터미널 대시보드
```bash
python3 debug_dashboard.py
```

### 로그 모니터링
```bash
./monitor_logs.sh
```

## 🛡️ 트러블슈팅

### MCP 서버가 인식되지 않을 때
1. Claude Desktop 완전 재시작
2. 설정 파일 경로 확인
3. Python 경로 확인: `/usr/local/bin/python3`
4. 간단한 테스트 서버로 시작: `ultra_simple_server.py`

### CLI 도구 확인
```bash
# Gemini CLI 확인
which gemini

# Claude CLI 확인  
which claude
```

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

- **🔸 Gemini**: 창의성, 최신 정보, 다국어, 브레인스토밍
- **🔹 Claude**: 논리성, 코딩, 구조화, 문서 작성
- **🤝 협업**: 두 AI의 **최고 장점만** 결합!

## 📈 품질 보장

- **다중 관점** 문제 해결
- **상호 검토**로 오류 최소화  
- **반복 개선**으로 완성도 극대화
- **객관적 품질 점수** 산출

## 🔧 개발자 도구

- **실시간 로그 스트리밍**
- **시각적 워크플로우 대시보드**
- **협업 통계 및 성과 분석**
- **디버깅 및 모니터링 도구**

---

**🎉 이제 진짜 AI 팀워크를 경험해보세요!**

Created by: AI Collaboration Project  
License: MIT  
Version: 2.0.0