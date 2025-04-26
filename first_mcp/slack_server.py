from mcp.server.fastmcp import FastMCP
import requests
import os

mcp = FastMCP("SlackMCP")

SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

# slack.send_message Tool 등록
@mcp.tool(name="slack.send_message")
def send_message(channel: str, text: str) -> dict:
    """Slack 채널에 메시지를 보냅니다."""
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == "__main__":
    mcp.run()