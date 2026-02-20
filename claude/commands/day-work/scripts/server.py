#!/usr/bin/env python3
"""Day-work Dashboard Server

Simple HTTP server to serve day-work.html dashboard.
Runs on port 8765.

Usage:
    python server.py start   # Start server in background
    python server.py stop    # Stop server
    python server.py status  # Check server status
"""

import http.server
import socketserver
import os
import sys
import signal
import socket

PORT = 8765
HTML_DIR = "/tmp/day-work-server"
PID_FILE = "/tmp/day-work-server.pid"

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that suppresses access logs"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HTML_DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress logging

def get_pid():
    """Get server PID from file"""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            return int(f.read().strip())
    return None

def is_running():
    """Check if server is running"""
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    return False

def start_server():
    """Start server in background"""
    ip = get_local_ip()
    if is_running():
        print(f"Server already running on http://{ip}:{PORT}")
        return True

    # Ensure HTML directory exists
    os.makedirs(HTML_DIR, exist_ok=True)

    # Create default index.html if not exists
    index_path = os.path.join(HTML_DIR, "index.html")
    if not os.path.exists(index_path):
        with open(index_path, 'w') as f:
            f.write("<html><body><h1>Day-work Dashboard Loading...</h1></body></html>")

    # Fork and start server
    pid = os.fork()
    if pid == 0:
        # Child process - run server
        os.setsid()
        with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
            httpd.serve_forever()
    else:
        # Parent process - save PID and exit
        with open(PID_FILE, 'w') as f:
            f.write(str(pid))
        print(f"Server started on http://{ip}:{PORT} (PID: {pid})")
        return True

def stop_server():
    """Stop server"""
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            os.remove(PID_FILE)
            print("Server stopped")
            return True
        except OSError:
            os.remove(PID_FILE)
            print("Server was not running")
            return False
    print("Server not running")
    return False

def status():
    """Check server status"""
    if is_running():
        ip = get_local_ip()
        print(f"Server running on http://{ip}:{PORT}")
        return True
    print("Server not running")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: server.py [start|stop|status]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "start":
        start_server()
    elif cmd == "stop":
        stop_server()
    elif cmd == "status":
        status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
