#!/usr/bin/env python3
"""Serve the live QA Office view for a project.

Usage (from the project folder):
    python qa_office.py                 # serves http://localhost:4477 (or the next free port)
    python qa_office.py --port 5000 --project path/to/project

Open the printed URL. Add ?demo=1 to watch a simulated run.
"""
import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PAGE = Path(__file__).resolve().parent.parent / "office" / "index.html"

ap = argparse.ArgumentParser(description="Serve the live QA Office view")
ap.add_argument("--project", default=".", help="project folder (default: current folder)")
ap.add_argument("--port", type=int, default=4477)
args = ap.parse_args()

project = Path(args.project).resolve()
live = project / "qa" / "live"


def read_events(path):
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # partially written line; it will be complete on the next poll
    return out


class Handler(BaseHTTPRequestHandler):
    def send(self, body, ctype, status=200):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)
        if url.path in ("/", "/index.html"):
            self.send(PAGE.read_bytes(), "text/html; charset=utf-8")
        elif url.path == "/events":
            run = Path(q.get("run", [""])[0]).name  # .name blocks path traversal
            path = live / "runs" / run if run else live / "events.jsonl"
            since = max(0, int(q.get("since", ["0"])[0] or 0))
            events = read_events(path)
            self.send(json.dumps({"project": project.name, "total": len(events), "events": events[since:]}),
                      "application/json")
        elif url.path == "/runs":
            runs = sorted((p.name for p in (live / "runs").glob("*.jsonl")), reverse=True) if (live / "runs").exists() else []
            self.send(json.dumps(runs), "application/json")
        else:
            self.send("Not found", "text/plain", 404)

    def log_message(self, *a):
        pass


for port in range(args.port, args.port + 20):
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        break
    except OSError:
        continue
else:
    sys.exit(f"No free port between {args.port} and {args.port + 19}")

live.mkdir(parents=True, exist_ok=True)
(live / "office-url.txt").write_text(f"http://localhost:{port}\n", encoding="utf-8")
print(f"QA Office running at http://localhost:{port}", flush=True)
server.serve_forever()
