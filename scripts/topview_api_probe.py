#!/usr/bin/env python3
"""Read-only Topview public API capability probe for AI Film.

Run from GitHub Actions with TOPVIEW_API_KEY (secret), TOPVIEW_UID (variable).
Does not publish topview-status.json, infer 6/6 slot occupancy, or submit tasks.
Prints only response codes and safe status metadata; no keys or video URLs.
"""
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://api.topview.ai"
AUTH_PATH = "/v1/tts/list"
QUERY_PATHS = [
    "/v2/common_task/image2video/task/query",
    "/v1/common_task/text2video/task/query",
    "/v1/common_task/omni_reference/task/query",
]

def request(path, *, query=None):
    url = BASE + path + (("?" + urlencode(query)) if query else "")
    headers = {"Authorization": "Bearer " + os.environ["TOPVIEW_API_KEY"].strip(),
               "Topview-Uid": os.environ["TOPVIEW_UID"].strip(),
               "Accept": "application/json"}
    req = Request(url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=20) as response:
            payload = json.loads(response.read(128_000).decode("utf-8"))
            return {"http_status": response.status, "api_code": str(payload.get("code", "")),
                    "api_status": str((payload.get("result") or {}).get("status", ""))[:50],
                    "result_task_id": str((payload.get("result") or {}).get("taskId", ""))[:100],
                    "result_present": payload.get("result") is not None}
    except HTTPError as e:
        return {"http_status": e.code, "api_code": "", "api_status": "", "result_present": False}
    except (URLError, TimeoutError, ValueError) as e:
        return {"http_status": 0, "api_code": "", "api_status": "", "result_present": False,
                "error_type": type(e).__name__}

def main():
    if not os.environ.get("TOPVIEW_API_KEY") or not os.environ.get("TOPVIEW_UID"):
        print(json.dumps({"configured": False, "reason": "TOPVIEW_API_KEY or TOPVIEW_UID absent",
                          "full_board_coverage": "not_verified", "slots_6": "unknown"}))
        return 0
    auth = request(AUTH_PATH)
    out = {"configured": True, "auth_endpoint": AUTH_PATH, "auth": auth,
           "full_board_coverage": "not_verified", "slots_6": "unknown",
           "writes_or_renders": False}
    f = ROOT / "topview-status.json"
    if f.exists():
        data = json.loads(f.read_text(encoding="utf-8"))
        cands = list(data.get("active_tasks") or [])
        tm = ROOT / "topview-task-map.json"
        if not cands and tm.exists():  # no active task: test the most recent known board task instead
            cands = [{"task_id": p.get("task_id")} for p in (json.loads(tm.read_text(encoding="utf-8")).get("processed_tasks") or [])[-1:]]
        for t in cands[:1]:
            tid = str(t.get("task_id", ""))
            if not tid or len(tid) > 100:
                continue
            # Board task IDs may NOT be queryable through public API task endpoints.
            # Probe that hypothesis, but never treat mismatches as a successful scan.
            out["known_board_task_test"] = {
                "task_id": tid,
                "queries": {path: request(path, query={"taskId": tid})
                            for path in QUERY_PATHS}
            }
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    # also as a workflow annotation, readable via the check-runs API (no secrets inside)
    print("::notice title=topview-probe::" + json.dumps(out, ensure_ascii=False, sort_keys=True))
    print("Topview public API board-list coverage and 6 free slots still unverified; "
          "DO NOT publish this diagnostic to topview-status.json.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
