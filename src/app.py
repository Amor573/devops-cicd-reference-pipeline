"""Dependency-free HTTP service for CI/CD and Kubernetes demonstrations."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from urllib.parse import urlsplit


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self._counts = {}

    def add_request(self, path):
        label = path if path in {"/", "/healthz", "/readyz", "/metrics"} else "other"
        with self._lock:
            self._counts[label] = self._counts.get(label, 0) + 1

    def render(self):
        with self._lock:
            counts = dict(self._counts)
        lines = [
            "# HELP demo_http_requests_total Number of requests handled by this process.",
            "# TYPE demo_http_requests_total counter",
        ]
        for name in sorted(counts):
            lines.append(f'demo_http_requests_total{{path="{name}"}} {counts[name]}')
        return "\n".join(lines) + "\n"


METRICS = Metrics()


class Handler(BaseHTTPRequestHandler):
    server_version = "PlatformDemo/1.0"

    def respond(self, code, payload, content_type):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlsplit(self.path).path
        METRICS.add_request(path)
        if path in {"/healthz", "/readyz"}:
            self.respond(200, b'{"status":"ok"}\n', "application/json")
        elif path == "/":
            payload = json.dumps({
                "service": "platform-demo",
                "version": os.getenv("APP_VERSION", "dev"),
                "message": "Hello from a CI/CD and Kubernetes reference workload",
            }).encode("utf-8") + b"\n"
            self.respond(200, payload, "application/json")
        elif path == "/metrics":
            self.respond(200, METRICS.render().encode("utf-8"),
                         "text/plain; version=0.0.4; charset=utf-8")
        else:
            self.respond(404, b'{"error":"not_found"}\n', "application/json")

    def log_message(self, fmt, *args):
        print("http", self.address_string(), fmt % args, flush=True)


def main():
    port = int(os.getenv("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"platform-demo listening on 0.0.0.0:{port}", flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
