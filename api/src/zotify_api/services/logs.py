import json
import os
from typing import List
from datetime import datetime
from zotify_api.config import settings

def read_recent_logs(limit: int = 50, level: str | None = None):
    path = settings.log_file_path
    entries = []
    if not os.path.exists(path):
        return []
    with open(path, "rb") as fh:
        # read last N lines efficiently
        fh.seek(0, os.SEEK_END)
        filesize = fh.tell()
        blocksize = 1024
        data = b""
        # small backread
        while len(entries) < limit and fh.tell() > 0:
            seek = max(0, fh.tell()-blocksize)
            fh.seek(seek)
            data = fh.read(min(blocksize, fh.tell() - seek)) + data
            fh.seek(seek)
            lines = data.splitlines()
            entries = lines[-limit:]
            if seek == 0:
                break
    parsed = []
    for line in reversed(entries):
        try:
            s = line.decode("utf-8")
            # try JSON first
            j = json.loads(s)
            ts = j.get("time") or j.get("timestamp")
            parsed.append({
                "timestamp": ts,
                "level": j.get("level", "INFO"),
                "message": j.get("msg", j.get("message", s))
            })
        except Exception:
            # fallback parse: simple text line to timestamp-less entry
            parsed.append({
                "timestamp": None,
                "level": "INFO",
                "message": line.decode("utf-8", errors="replace")
            })
    if level:
        parsed = [p for p in parsed if p["level"] == level]
    return parsed[:limit]
