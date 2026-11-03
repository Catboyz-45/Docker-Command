"""Minimal web server used to demonstrate building a Docker image.

Uses only the Python standard library, so the image needs no pip install.
"""

import os
import signal
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8000"))


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Hello from Docker!\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def handle_sigterm(signum, frame):
    # In a container this app is PID 1, and Linux gives PID 1 no default
    # signal handlers: without this, "docker stop" sends SIGTERM, nothing
    # happens, and Docker has to SIGKILL the app after 10 seconds.
    raise SystemExit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)

    # Bind to 0.0.0.0, not 127.0.0.1: inside a container, 127.0.0.1 is the
    # container itself, so traffic forwarded by "-p" would never reach the app.
    server = HTTPServer(("0.0.0.0", PORT), HelloHandler)
    print(f"Listening on port {PORT}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        print("Shut down cleanly", flush=True)
