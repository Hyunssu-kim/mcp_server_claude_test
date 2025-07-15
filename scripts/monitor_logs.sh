#!/bin/bash

# 실시간 로그 모니터링 스크립트

LOG_DIR="/Users/kimhyunsu/Desktop/Developer/MCP_server/logs"

echo "🔍 Collaborative AI Orchestrator 로그 모니터링"
echo "================================================"

# 로그 디렉토리가 없으면 생성
if [ ! -d "$LOG_DIR" ]; then
    echo "📁 로그 디렉토리 생성: $LOG_DIR"
    mkdir -p "$LOG_DIR"
fi

# 최신 로그 파일 찾기
LATEST_LOG=$(ls -t "$LOG_DIR"/collaborative_ai_*.log 2>/dev/null | head -1)

if [ -z "$LATEST_LOG" ]; then
    echo "❌ 로그 파일을 찾을 수 없습니다."
    echo "💡 먼저 서버를 시작하세요: ./start_collaborative_server.sh"
    exit 1
fi

echo "📋 모니터링 중인 로그 파일: $(basename $LATEST_LOG)"
echo "⏰ 실시간 로그 (Ctrl+C로 종료)"
echo "================================================"
echo ""

# 실시간 로그 추적
tail -f "$LATEST_LOG" | while read line; do
    # 로그 라인에 이모지 추가하여 가독성 향상
    if [[ $line == *"초기 토론"* ]]; then
        echo "🎯 $line"
    elif [[ $line == *"초안 작성"* ]]; then
        echo "✍️ $line"
    elif [[ $line == *"동료 검토"* ]]; then
        echo "🔍 $line"
    elif [[ $line == *"개선"* ]]; then
        echo "🚀 $line"
    elif [[ $line == *"최종 검토"* ]]; then
        echo "✅ $line"
    elif [[ $line == *"품질 평가"* ]]; then
        echo "📊 $line"
    elif [[ $line == *"ERROR"* ]]; then
        echo "❌ $line"
    elif [[ $line == *"WARNING"* ]]; then
        echo "⚠️ $line"
    elif [[ $line == *"INFO"* ]]; then
        echo "ℹ️ $line"
    else
        echo "$line"
    fi
done