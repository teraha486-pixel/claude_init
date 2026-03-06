"""
Dooray 업무 코멘트 ↔ Claude Code 브릿지

[제어 명령어] - 두레이 업무 코멘트 또는 Claude Code에서 직접 제어 가능
  브릿지 켜  /  !켜  /  !on   →  브릿지 활성화 (5초 폴링)
  브릿지 꺼  /  !꺼  /  !off  →  브릿지 비활성화 (30초 폴링)
  브릿지 상태 / !상태          →  현재 상태 확인

[동작]
  - 활성화 상태에서 일반 코멘트 → Claude 실행 → 코멘트로 답변
  - 비활성화 상태에서는 제어 명령어만 처리
"""

import subprocess
import requests
import json
import time
import os
import sys
from datetime import datetime

# Windows 터미널 UTF-8 출력 설정
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ─── 설정 ──────────────────────────────────────────
DOORAY_API_TOKEN = "ajjt1imxmtj4:Xrqw31ahSlKOfPnQWtIolg"
MY_MEMBER_ID     = "2802458672652277190"
PROJECT_ID       = "2802458674191447213"
POST_ID          = "4280771346033842046"

POLL_ON          = 5    # 활성화 시 폴링 주기 (초)
POLL_OFF         = 30   # 비활성화 시 폴링 주기 (초)
CLAUDE_TIMEOUT   = 300  # Claude 응답 타임아웃 (초)
WORK_DIR         = "D:/claude_work"
CLAUDE_BIN       = r"C:\Users\NHN\AppData\Roaming\npm\claude.cmd"

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bridge_state.json")

API_BASE = "https://api.dooray.com/project/v1"
HEADERS  = {
    "Authorization": f"dooray-api {DOORAY_API_TOKEN}",
    "Content-Type": "application/json"
}

CONTROL_CMDS = {
    "브릿지 켜": "on",  "!켜": "on",  "!on": "on",
    "브릿지 꺼": "off", "!꺼": "off", "!off": "off",
    "브릿지 상태": "status", "!상태": "status",
}

# 브릿지가 보낸 코멘트에 삽입하는 마커 (렌더링 시 보이지 않음)
BRIDGE_MARKER = "<!-- bridge -->"
# ────────────────────────────────────────────────────


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_log_id": None, "sent_ids": [], "active": False}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_comments():
    url = f"{API_BASE}/projects/{PROJECT_ID}/posts/{POST_ID}/logs"
    try:
        resp = requests.get(url, headers=HEADERS, params={"limit": 50, "order": "createdAt"}, timeout=10)
        data = resp.json()
        if data.get("header", {}).get("isSuccessful"):
            return data.get("result", [])
    except Exception as e:
        print(f"[폴링 오류] {e}")
    return []


def post_comment(text):
    url = f"{API_BASE}/projects/{PROJECT_ID}/posts/{POST_ID}/logs"
    payload = {"body": {"mimeType": "text/x-markdown", "content": text + f"\n{BRIDGE_MARKER}"}}
    try:
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        data = resp.json()
        if data.get("header", {}).get("isSuccessful"):
            return str(data["result"]["id"])
    except Exception as e:
        print(f"[코멘트 전송 오류] {e}")
    return None


def run_claude(message):
    try:
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)  # 중첩 세션 오류 방지
        result = subprocess.run(
            [CLAUDE_BIN, "-p", "--dangerously-skip-permissions", "--continue", message],
            capture_output=True, text=True, cwd=WORK_DIR, timeout=CLAUDE_TIMEOUT,
            shell=True, env=env
        )
        response = (result.stdout or "").strip() or (result.stderr or "").strip()
        return response or "(응답 없음)"
    except subprocess.TimeoutExpired:
        return f"⚠️ 타임아웃: {CLAUDE_TIMEOUT}초 내에 응답이 없었습니다."
    except Exception as e:
        return f"⚠️ 오류: {e}"


def handle_control(cmd, state):
    """제어 명령 처리. 응답 메시지 반환"""
    action = CONTROL_CMDS.get(cmd)
    if action == "on":
        state["active"] = True
        return "✅ 브릿지 **활성화** 됐습니다. 코멘트를 입력하면 Claude가 작업합니다."
    elif action == "off":
        state["active"] = False
        return "⏸️ 브릿지 **비활성화** 됐습니다. (`!켜` 입력 시 재개)"
    elif action == "status":
        status = "🟢 활성화" if state["active"] else "🔴 비활성화"
        return f"현재 상태: {status}"
    return None


def process_comment(comment, state):
    log_id    = str(comment.get("id", ""))
    sender_id = str(comment.get("creator", {}).get("member", {}).get("organizationMemberId", ""))
    text      = (comment.get("body", {}).get("content") or "").strip()

    # 브릿지가 보낸 코멘트 무시 (마커 기반 - 인스턴스/타이밍 무관하게 확실히 차단)
    if BRIDGE_MARKER in text:
        return

    # 내 코멘트만 처리
    if sender_id != MY_MEMBER_ID:
        return

    if not text:
        return

    ts = datetime.now().strftime("%H:%M:%S")

    # 제어 명령 체크
    if text in CONTROL_CMDS:
        reply = handle_control(text, state)
        print(f"[{ts}] 제어 명령: {text} → {'활성화' if state['active'] else '비활성화'}")
        sent_id = post_comment(reply)
        if sent_id:
            state.setdefault("sent_ids", []).append(sent_id)
        return

    # 비활성화 상태에서는 일반 코멘트 무시
    if not state.get("active", False):
        return

    # Claude 실행
    print(f"[{ts}] 수신: {text[:80]}")
    waiting_id = post_comment("⏳ 처리 중...")
    if waiting_id:
        state.setdefault("sent_ids", []).append(waiting_id)

    response = run_claude(text)
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] 응답 완료 ({len(response)}자)")

    MAX_LEN = 5000
    if len(response) > MAX_LEN:
        chunks = [response[i:i+MAX_LEN] for i in range(0, len(response), MAX_LEN)]
        for i, chunk in enumerate(chunks, 1):
            prefix = f"**[{i}/{len(chunks)}]**\n\n" if len(chunks) > 1 else ""
            sent_id = post_comment(prefix + chunk)
            if sent_id:
                state.setdefault("sent_ids", []).append(sent_id)
    else:
        sent_id = post_comment(response)
        if sent_id:
            state.setdefault("sent_ids", []).append(sent_id)

    state["sent_ids"] = state["sent_ids"][-200:]


def main():
    print("=" * 55)
    print("  Dooray 코멘트 ↔ Claude Code 브릿지")
    print(f"  업무 URL: https://nhnent.dooray.com/project/tasks/{POST_ID}")
    print("─" * 55)
    print("  제어 명령어 (두레이 코멘트에 입력)")
    print("    !켜  /  !on   → 활성화 (5초 폴링)")
    print("    !꺼  /  !off  → 비활성화 (30초 폴링)")
    print("    !상태         → 현재 상태 확인")
    print("─" * 55)
    print("  종료: Ctrl+C")
    print("=" * 55)

    state = load_state()

    # 최초 실행 시 기존 코멘트 스킵
    if state["last_log_id"] is None:
        comments = get_comments()
        if comments:
            state["last_log_id"] = str(comments[-1].get("id", ""))
        save_state(state)

    status = "🟢 활성화" if state.get("active") else "🔴 비활성화"
    print(f"\n시작 완료. 현재 상태: {status}\n")

    while True:
        try:
            comments = get_comments()
            new_comments = []

            if state["last_log_id"] and comments:
                found = False
                for c in comments:
                    if found:
                        new_comments.append(c)
                    if str(c.get("id", "")) == state["last_log_id"]:
                        found = True
                if not found:
                    # last_log_id가 삭제됐거나 없음 → 전부 처리하지 않고 스킵 후 최신 ID로 갱신
                    new_comments = []
                    print(f"[경고] last_log_id({state['last_log_id']})를 찾을 수 없음 → 현재 댓글 스킵")
            elif not state["last_log_id"]:
                new_comments = comments

            for comment in new_comments:
                process_comment(comment, state)

            if comments:
                state["last_log_id"] = str(comments[-1].get("id", ""))

            save_state(state)

        except KeyboardInterrupt:
            print("\n\n브릿지 종료.")
            break
        except Exception as e:
            print(f"[오류] {e}")

        interval = POLL_ON if state.get("active") else POLL_OFF
        time.sleep(interval)


if __name__ == "__main__":
    main()
