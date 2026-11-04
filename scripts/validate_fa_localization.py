#!/usr/bin/env python3
"""Validate the Persian localization assets without requiring a Frappe site."""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "education" / "translations" / "fa.csv"
DOCTYPE_ROOT = ROOT / "education" / "education" / "doctype"
PERSIAN = re.compile(r"[\\u0600-\\u06FF]")
errors = []

rows = []
with TRANSLATIONS.open(encoding="utf-8-sig", newline="") as handle:
    for line_number, row in enumerate(csv.reader(handle), start=1):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != 2 or not row[0].strip() or not row[1].strip():
            errors.append(f"fa.csv:{line_number}: expected two non-empty columns")
            continue
        if not PERSIAN.search(row[1]):
            errors.append(f"fa.csv:{line_number}: translation has no Persian characters")
        rows.append((row[0].strip(), row[1].strip()))

keys = [key for key, _ in rows]
duplicates = sorted({key for key in keys if keys.count(key) > 1})
if duplicates:
    errors.append("duplicate translation keys: " + ", ".join(duplicates[:20]))

required = {"Student", "Instructor", "Course", "Date of Birth", "Save", "Cancel"}
missing = sorted(required.difference(keys))
if missing:
    errors.append("missing required translation keys: " + ", ".join(missing))

json_count = 0
for path in sorted(DOCTYPE_ROOT.rglob("*.json")):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        json_count += 1
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")

print(f"Persian translation rows: {len(rows)}")
print(f"Doctype JSON files validated: {json_count}")
if errors:
    print("\\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
    sys.exit(1)
print("Persian localization asset checks passed.")
