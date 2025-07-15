#!/bin/bash

echo "🔍 Claude Desktop 로그 확인"
echo "=========================="

# Console.app에서 Claude 관련 로그 확인
echo "📋 최근 Claude 관련 로그:"
log show --predicate 'subsystem contains "Claude" OR process contains "Claude"' --last 5m --style compact 2>/dev/null | tail -20

echo ""
echo "📁 Claude 설정 파일 상태:"
echo "------------------------"
echo "설정 파일 존재: $(test -f '/Users/kimhyunsu/Library/Application Support/Claude/claude_desktop_config.json' && echo '✅' || echo '❌')"
echo "설정 파일 크기: $(stat -f%z '/Users/kimhyunsu/Library/Application Support/Claude/claude_desktop_config.json' 2>/dev/null || echo '0') bytes"

echo ""
echo "🔧 트러블슈팅 제안:"
echo "- Claude Desktop을 완전 재시작"
echo "- 설정 파일 문법 확인"
echo "- 새 대화 시작"