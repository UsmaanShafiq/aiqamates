#!/usr/bin/env python3
"""Log a QA progress event for the live QA Office view.

Events are appended to qa/live/events.jsonl in the current project.

Usage:
    python qa_event.py --new-run "My Project"                      # start a new run (archives the previous one)
    python qa_event.py qa-lead phase "Reading the project" --phase discovery
    python qa_event.py functional-test-engineer working "Testing the signup form"
    python qa_event.py functional-test-engineer found "Save button does nothing" --severity P1
    python qa_event.py functional-test-engineer done "4 findings"

States: working, found, waiting, blocked, idle, done, phase
Phases: discovery, context, setup, plan, testing, report, fixing, final
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

STATES = {"working", "found", "waiting", "blocked", "idle", "done", "phase"}
PHASES = ["discovery", "context", "setup", "plan", "testing", "report", "fixing", "final"]

ap = argparse.ArgumentParser(description="Log a QA Office progress event")
ap.add_argument("agent", nargs="?", help="agent name, e.g. qa-lead or api-test-engineer")
ap.add_argument("state", nargs="?", choices=sorted(STATES))
ap.add_argument("message", nargs="?", default="")
ap.add_argument("--severity", choices=["P0", "P1", "P2", "P3", "P4"])
ap.add_argument("--phase", choices=PHASES)
ap.add_argument("--new-run", metavar="PROJECT_NAME", help="start a new run and archive the previous one")
ap.add_argument("--dir", default="qa/live", help="event folder (default: qa/live)")
args = ap.parse_args()

live = Path(args.dir)
live.mkdir(parents=True, exist_ok=True)
events = live / "events.jsonl"
now = datetime.datetime.now().astimezone()

if args.new_run is not None:
    if events.exists() and events.stat().st_size > 0:
        runs = live / "runs"
        runs.mkdir(exist_ok=True)
        stamp = datetime.datetime.fromtimestamp(events.stat().st_mtime).strftime("%Y-%m-%d_%H-%M-%S")
        events.replace(runs / f"{stamp}.jsonl")
    event = {"t": now.isoformat(timespec="seconds"), "agent": "qa-lead", "state": "run", "msg": args.new_run}
else:
    if not args.agent or not args.state:
        ap.error("agent and state are required (or use --new-run)")
    event = {"t": now.isoformat(timespec="seconds"), "agent": args.agent, "state": args.state,
             "msg": " ".join(args.message.split())[:160]}
    if args.severity:
        event["severity"] = args.severity
    if args.phase:
        event["phase"] = args.phase

with events.open("a", encoding="utf-8") as f:
    f.write(json.dumps(event, ensure_ascii=False) + "\n")
sys.exit(0)
