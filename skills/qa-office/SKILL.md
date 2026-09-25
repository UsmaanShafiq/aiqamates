---
name: qa-office
description: Open the live QA Office (pixel-art view of the QA team) for the current project, without starting a QA run. Use "/qa-office demo" to watch a simulated run.
argument-hint: "[demo]"
disable-model-invocation: true
---

# Open the QA Office

Show the user the QA Office for the current project. Do **not** start a QA run and do not change any project files except under `qa/live/`.

The office server script is `scripts/qa_office.py` inside the `qa` skill folder, a sibling of this skill's base directory (e.g. `~/.claude/skills/qa/scripts/qa_office.py`). Use the **Bash** tool from the project root.

1. **Reuse a running server.** If `qa/live/office-url.txt` exists, read the URL and check it responds (`curl -s -o /dev/null -w "%{http_code}" <url>/events`). If it returns 200, use it.
2. **Otherwise start one** in the background (Bash `run_in_background: true`): `python "<qa skill dir>/scripts/qa_office.py"`. Wait until `qa/live/office-url.txt` exists and the URL responds (poll a few times, about a second apart), then read the URL.
3. **Open it** in the browser pane with `preview_start` and the URL. If `$ARGUMENTS` contains `demo`, append `?demo=1`. If no browser pane is available, print the URL on its own line so the user can open it.
4. **Tell the user in 1–2 lines** what they're seeing:
   - if `qa/live/events.jsonl` has events: the latest QA run (live if one is in progress), and that **Replay** and the run dropdown show past runs;
   - if there are no events yet: the team is on a break in the lounge until `/qa` starts, and **Demo** shows a simulated run.
   Mention that the server keeps running in the background for this session.

If `python` isn't found, try `python3`. If the script doesn't exist, tell the user to install the QA kit (`install.ps1` / `install.sh` from the aiqamates repo).
