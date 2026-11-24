"""Evaluate an offline snapshot against three example cloud storage policies."""
import argparse
import json
import sys
from pathlib import Path

RULES = (
    ("ST-01", "public_read", False, "high", "Review public read access."),
    ("ST-02", "encrypted", True, "high", "Verify encryption at rest."),
    ("ST-03", "access_logging", True, "medium", "Verify access logging."),
)


def evaluate(snapshot):
    if not isinstance(snapshot, list) or not snapshot:
        raise ValueError("Expected a non-empty JSON array of storage objects.")
    seen = set()
    checks = []
    for row in snapshot:
        name = row.get("id") if isinstance(row, dict) else None
        if not isinstance(name, str) or not name.strip() or name in seen:
            raise ValueError("Every storage object needs a unique non-empty id.")
        seen.add(name)
        for rule, field, expected, severity, advice in RULES:
            value = row.get(field)
            if value is not None and not isinstance(value, bool):
                raise ValueError(f"{name}.{field} must be true, false or null.")
            if value is None:
                status = "unknown"
            elif value == expected:
                status = "pass"
            else:
                status = "fail"
            checks.append(dict(resource=name, rule=rule, field=field, observed=value,
                               expected=expected, status=status, severity=severity,
                               action=advice if status != "pass" else ""))
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable checks")
    parser.add_argument("--gate", action="store_true", help="Exit 1 for any fail or unknown")
    args = parser.parse_args()
    try:
        checks = evaluate(json.loads(args.snapshot.read_text(encoding="utf-8")))
    except (ValueError, OSError) as error:
        parser.exit(2, f"Input error: {error}\n")
    if args.json:
        print(json.dumps(checks, indent=2))
    else:
        for item in checks:
            print(f"{item['resource']:18} {item['rule']}  {item['status']:7} {item['action']}")
    return int(args.gate and any(item["status"] != "pass" for item in checks))


if __name__ == "__main__":
    sys.exit(main())
