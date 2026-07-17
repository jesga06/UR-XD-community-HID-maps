import json
import sys
from pathlib import Path

MAPS_DIR = Path("maps")
DATABASE_FILE = Path("database.json")


def fail(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


if not MAPS_DIR.exists():
    fail("maps/ directory not found.")

database = {}

for file in sorted(MAPS_DIR.glob("*.json")):
    try:
        with file.open("r", encoding="utf-8") as f:
            hid_map = json.load(f)

        name = hid_map["name"]
        vid = hid_map["vid"].upper()
        pid = hid_map["pid"].upper()

        alias = f"{vid}:{pid}"

        if name in database:
            fail(f'Duplicate controller name "{name}".')

        database[name] = {
            "aliases": [alias],
            "hid_map_file": file.as_posix()
        }

    except KeyError as e:
        fail(f"{file}: missing required key {e}")

    except json.JSONDecodeError as e:
        fail(f"{file}: invalid JSON ({e})")

with DATABASE_FILE.open("w", encoding="utf-8") as f:
    json.dump(database, f, indent=4)
    f.write("\n")

print(f"Generated {DATABASE_FILE}")