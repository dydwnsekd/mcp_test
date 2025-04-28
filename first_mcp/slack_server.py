from mcp.server.fastmcp import FastMCP
import requests
import os

# MCP Server 인스턴스 생성
mcp = FastMCP("SlackMCP")

# Slack Bot Token 불러오기
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

# Slack API 요청 공통 함수
def slack_api_post(endpoint: str, payload: dict) -> dict:
    url = f"https://slack.com/api/{endpoint}"
    headers = {
        "Authorization": f"Bearer {SLACK_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# 1. 채널에 메시지 보내기
@mcp.tool(name="slack.send_message")
def send_message(channel: str, text: str) -> dict:
    """Slack 채널에 메시지를 보냅니다."""
    return slack_api_post("chat.postMessage", {"channel": channel, "text": text})

# 2. 채널 사용자 목록 가져오기
@mcp.tool(name="slack.get_channel_members")
def get_channel_members(channel: str) -> dict:
    """Slack 채널의 사용자 목록을 조회합니다."""
    return slack_api_post("conversations.members", {"channel": channel})

# 3. 메시지에 리액션 달기
@mcp.tool(name="slack.add_reaction")
def add_reaction(channel: str, timestamp: str, emoji: str) -> dict:
    """Slack 메시지에 리액션을 추가합니다."""
    return slack_api_post("reactions.add", {
        "channel": channel,
        "timestamp": timestamp,
        "name": emoji
    })

# 4. 메시지에 쓰레드(reply) 달기
@mcp.tool(name="slack.reply_in_thread")
def reply_in_thread(channel: str, thread_ts: str, text: str) -> dict:
    """Slack 메시지에 쓰레드를 추가합니다."""
    return slack_api_post("chat.postMessage", {
        "channel": channel,
        "text": text,
        "thread_ts": thread_ts
    })

if __name__ == "__main__":
    mcp.run()