#!/bin/bash

# MCP AI Orchestrator 서버 시작 스크립트

echo "=== MCP AI Orchestrator 서버 시작 ==="

# Python 가상환경 확인
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "가상환경 활성화됨: $VIRTUAL_ENV"
else
    echo "경고: 가상환경이 활성화되지 않았습니다."
fi

# 의존성 설치 확인
echo "의존성 설치 확인 중..."
pip install -r requirements.txt

# gemini, claude CLI 도구 확인
echo "CLI 도구 확인 중..."

if command -v gemini &> /dev/null; then
    echo "✓ gemini CLI 확인됨"
else
    echo "⚠️  gemini CLI가 설치되지 않았습니다"
    echo "  설치 방법: pip install google-generativeai-cli (또는 해당 패키지)"
fi

if command -v claude &> /dev/null; then
    echo "✓ claude CLI 확인됨"
else
    echo "⚠️  claude CLI가 설치되지 않았습니다"
    echo "  설치 방법: pip install claude-cli (또는 해당 패키지)"
fi

# 서버 실행
echo ""
echo "MCP 서버 시작 중..."
echo "클라이언트에서 다음 명령으로 연결하세요:"
echo "python mcp_ai_orchestrator.py"
echo ""

python mcp_ai_orchestrator.py