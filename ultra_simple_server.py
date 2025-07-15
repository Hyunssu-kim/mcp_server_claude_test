#!/usr/bin/env python3
import asyncio
import sys
import json

# MCP 최소 구현
async def main():
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, input)
            if not line:
                break
                
            data = json.loads(line)
            
            if data.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "ultra-simple-server",
                            "version": "1.0.0"
                        }
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
                
            elif data.get("method") == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "tools": [
                            {
                                "name": "simple_test",
                                "description": "간단한 테스트 도구",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        ]
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
                
            elif data.get("method") == "tools/call":
                response = {
                    "jsonrpc": "2.0", 
                    "id": data.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"테스트 성공! 메시지: {data.get('params', {}).get('arguments', {}).get('message', '없음')}"
                            }
                        ]
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
                
        except EOFError:
            break
        except Exception as e:
            print(f"오류: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())