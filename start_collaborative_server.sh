#!/bin/bash

# Collaborative AI Orchestrator 서버 시작 스크립트 (실시간 로그 포함)

echo "=== 🤝 Collaborative AI Orchestrator 서버 시작 ==="

# 로그 디렉토리 생성
LOG_DIR="/Users/kimhyunsu/Desktop/Developer/MCP_server/logs"
mkdir -p "$LOG_DIR"

# 현재 시간으로 로그 파일명 생성
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/collaborative_ai_$TIMESTAMP.log"

echo "📁 로그 파일: $LOG_FILE"

# Python 가상환경 확인
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 가상환경 활성화됨: $VIRTUAL_ENV"
else
    echo "⚠️  가상환경이 활성화되지 않았습니다."
fi

# CLI 도구 확인
echo "🔍 CLI 도구 확인 중..."

if command -v gemini &> /dev/null; then
    echo "✅ gemini CLI 확인됨"
else
    echo "❌ gemini CLI가 설치되지 않았습니다"
    echo "   설치 방법: npm install -g @google-ai/generativelanguage"
fi

if command -v claude &> /dev/null; then
    echo "✅ claude CLI 확인됨"
else
    echo "❌ claude CLI가 설치되지 않았습니다" 
    echo "   설치 방법: npm install -g @anthropic/claude-cli"
fi

echo ""
echo "🚀 MCP 서버 시작 중..."
echo "📋 실시간 로그는 다음 명령으로 확인하세요:"
echo "   tail -f $LOG_FILE"
echo ""
echo "🎯 Claude Desktop에서 다음 도구들을 사용할 수 있습니다:"
echo "   - collaborative_task (완전 협업)"
echo "   - quick_discussion (빠른 토론)"
echo "   - compare_approaches (접근법 비교)"
echo "   - get_collaboration_stats (통계)"
echo ""
echo "💡 Ctrl+C로 서버를 중지할 수 있습니다."
echo "=" | tr '=' '='
echo ""

# 서버 실행 (로그 파일과 터미널 동시 출력)
/usr/local/bin/python3 /Users/kimhyunsu/Desktop/Developer/MCP_server/collaborative_ai_orchestrator.py 2>&1 | tee "$LOG_FILE"