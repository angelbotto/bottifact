"""Typed filter contract shared with core/src/table-model.ts; no SQL fragments."""

import json
import math
from datetime import datetime, timezone
from portal.search import normalized

COLUMNS = {"title", "space", "category", "visibility", "comments", "updated", "agent"}


def parse(raw):
    if not raw:
        return {"join": "and", "rules": []}
    if len(raw) > 12000:
        raise ValueError("Too many filters")
    q = json.loads(raw)
    if (
        not isinstance(q, dict)
        or q.get("join", "and") not in ("and", "or")
        or not isinstance(q.get("rules"), list)
        or len(q["rules"]) > 12
    ):
        raise ValueError("Invalid filters")
    for r in q["rules"]:
        if (
            not isinstance(r, dict)
            or r.get("column") not in COLUMNS
            or r.get("operator")
            not in ("contains", "eq", "in", "gte", "lte", "between", "empty")
        ):
            raise ValueError("Invalid condition")
        for key in ("value", "upper"):
            value = r.get(key, "")
            if not isinstance(value, (str, int, float, list)) or isinstance(
                value, bool
            ):
                raise ValueError("Invalid value")
            if isinstance(value, list) and (
                len(value) > 100
                or any(not isinstance(x, str) or len(x) > 300 for x in value)
            ):
                raise ValueError("Invalid facet")
            if isinstance(value, str) and len(value) > 300:
                raise ValueError("Long value")
    return q


def matches(value, r):
    op = r["operator"]
    expected = r.get("value", "")
    if op == "empty":
        return value is None or value == ""
    if value is None or value == "":
        return False
    text = normalized(str(value))
    term = normalized(str(expected))
    if op == "contains":
        return term in text
    if op == "eq":
        return text == term
    if op == "in":
        return isinstance(expected, list) and text in [
            normalized(str(x)) for x in expected
        ]
    if op == "between":
        return matches(value, {**r, "operator": "gte"}) and matches(
            value, {**r, "operator": "lte", "value": r.get("upper", "")}
        )
    if op in ("gte", "lte"):
        if expected == "" or isinstance(expected, list):
            return False
        if isinstance(value, (int, float)):
            try:
                right = float(expected)
            except (TypeError, ValueError):
                return False
            if not math.isfinite(right):
                return False
            return value >= right if op == "gte" else value <= right
        return text >= term if op == "gte" else text <= term
    return False


def filter_rows(rows, q):
    def values(a):
        return {
            **{k: a.get(k) for k in COLUMNS},
            "comments": a.get("open_comments", 0),
            "agent": a.get("source", {}).get("agent", ""),
            "updated": datetime.fromtimestamp(a["updated"], timezone.utc)
            .date()
            .isoformat(),
        }

    return [
        a
        for a in rows
        if not q["rules"]
        or (any if q.get("join") == "or" else all)(
            matches(values(a).get(r["column"]), r) for r in q["rules"]
        )
    ]
