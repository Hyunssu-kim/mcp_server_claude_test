#!/usr/bin/env python3
"""
실시간 협업 AI 디버그 대시보드
터미널에서 실시간으로 협업 과정을 시각적으로 모니터링
"""
import time
import os
import sys
from datetime import datetime
import json

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    print("🤝 " + "="*60)
    print("   COLLABORATIVE AI ORCHESTRATOR - DEBUG DASHBOARD")
    print("="*64)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def print_workflow_status(current_stage="idle"):
    stages = [
        ("🎯", "초기 토론", "initial_discussion"),
        ("✍️", "초안 작성", "draft_creation"),
        ("🔍", "동료 검토", "peer_review"),
        ("🚀", "개선", "improvement"),
        ("✅", "최종 검토", "final_review"),
        ("📊", "품질 평가", "completion")
    ]
    
    print("📋 워크플로우 진행 상황:")
    print("-" * 50)
    
    for emoji, name, stage_id in stages:
        if stage_id == current_stage:
            print(f"{emoji} {name} ← 🔄 현재 진행 중")
        elif stages.index((emoji, name, stage_id)) < [s[2] for s in stages].index(current_stage):
            print(f"✅ {name} ← 완료")
        else:
            print(f"⏸️ {name} ← 대기 중")
    print()

def monitor_logs():
    log_dir = "/Users/kimhyunsu/Desktop/Developer/MCP_server/logs"
    
    if not os.path.exists(log_dir):
        print("❌ 로그 디렉토리가 없습니다. 서버를 먼저 시작하세요.")
        return
    
    log_files = [f for f in os.listdir(log_dir) if f.startswith("collaborative_ai_") and f.endswith(".log")]
    
    if not log_files:
        print("❌ 로그 파일을 찾을 수 없습니다.")
        return
    
    latest_log = max([os.path.join(log_dir, f) for f in log_files], key=os.path.getmtime)
    
    print(f"📁 모니터링 중: {os.path.basename(latest_log)}")
    print()
    
    current_stage = "idle"
    ai_activity = {"gemini": 0, "claude": 0}
    collaboration_count = 0
    
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            # 파일 끝으로 이동
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if line:
                    # 현재 단계 감지
                    if "초기 토론" in line:
                        current_stage = "initial_discussion"
                    elif "초안 작성" in line:
                        current_stage = "draft_creation"
                    elif "동료 검토" in line:
                        current_stage = "peer_review"
                    elif "개선" in line:
                        current_stage = "improvement"
                    elif "최종 검토" in line:
                        current_stage = "final_review"
                    elif "품질 평가" in line:
                        current_stage = "completion"
                    elif "협업 작업 시작" in line:
                        collaboration_count += 1
                        current_stage = "initial_discussion"
                    
                    # AI 활동 카운트
                    if "Gemini" in line:
                        ai_activity["gemini"] += 1
                    if "Claude" in line:
                        ai_activity["claude"] += 1
                    
                    # 실시간 업데이트
                    clear_screen()
                    print_header()
                    print_workflow_status(current_stage)
                    
                    print("🤖 AI 활동 통계:")
                    print("-" * 30)
                    print(f"🔸 Gemini 활동: {ai_activity['gemini']}회")
                    print(f"🔹 Claude 활동: {ai_activity['claude']}회")
                    print(f"🤝 총 협업 세션: {collaboration_count}개")
                    print()
                    
                    print("📜 최근 로그:")
                    print("-" * 30)
                    print(f"⏰ {line.strip()}")
                    print()
                    
                    print("💡 도구 사용법:")
                    print("  - collaborative_task: 전체 협업 워크플로우")
                    print("  - quick_discussion: 빠른 토론")
                    print("  - compare_approaches: 접근법 비교")
                    print("  - Ctrl+C: 모니터링 종료")
                
                else:
                    time.sleep(0.5)  # 0.5초마다 확인
                    
    except FileNotFoundError:
        print("❌ 로그 파일에 접근할 수 없습니다.")
    except KeyboardInterrupt:
        print("\n\n🔚 모니터링을 종료합니다.")
        sys.exit(0)

def main():
    clear_screen()
    print_header()
    print("🚀 실시간 로그 모니터링을 시작합니다...")
    print("   Claude Desktop에서 협업 도구를 사용해보세요!")
    print()
    
    monitor_logs()

if __name__ == "__main__":
    main()