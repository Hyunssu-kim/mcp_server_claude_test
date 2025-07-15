# 📜 Scripts Collection

서버 실행 및 모니터링을 위한 스크립트들입니다.

## 🚀 실행 스크립트들

### start_collaborative_server.sh
- **협업 서버 시작 (로그 포함)**
- 자동 로그 파일 생성
- 실시간 로그 출력
- CLI 도구 확인

**사용법:**
```bash
./start_collaborative_server.sh
```

### start_server.sh
- **기본 서버 시작**
- 간단한 서버 실행
- 기본 환경 확인

## 📊 모니터링 스크립트들

### monitor_logs.sh
- **실시간 로그 모니터링**
- 최신 로그 파일 자동 추적
- 색상 구분 로그 출력

**사용법:**
```bash
./monitor_logs.sh
```

### check_claude_logs.sh
- **Claude Desktop 로그 확인**
- 시스템 로그 분석
- 설정 파일 상태 확인
- 문제 진단 도구

**사용법:**
```bash
./check_claude_logs.sh
```

## 🔧 스크립트 권한 설정

모든 스크립트를 실행 가능하게 만들기:
```bash
chmod +x scripts/*.sh
```

## 💡 사용 팁

### 개발 워크플로우
```bash
# 1. 서버 시작 (별도 터미널)
./scripts/start_collaborative_server.sh

# 2. 로그 모니터링 (별도 터미널)
./scripts/monitor_logs.sh

# 3. 문제 발생 시 진단
./scripts/check_claude_logs.sh
```

### 디버깅 워크플로우
```bash
# 1. 기본 환경 확인
./scripts/check_claude_logs.sh

# 2. 간단한 서버로 테스트
python src/servers/ultra_simple_server.py

# 3. 로그 확인
tail -f logs/*.log
```