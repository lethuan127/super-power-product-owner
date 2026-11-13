"""Checks the marketplace, the plugin manifest and every skill's frontmatter. No model calls."""
import json
import pathlib
import re
import sys

import yaml

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
for entry in market["plugins"]:
    plugin_dir = root / entry["source"]
    manifest = json.loads((plugin_dir / ".claude-plugin/plugin.json").read_text())
    if manifest["name"] != entry["name"]:
        errors.append(f"{entry['name']}: plugin.json name is {manifest['name']}")
    for skill in sorted((plugin_dir / "skills").glob("*/SKILL.md")):
        match = re.match(r"^---\n(.*?)\n---", skill.read_text(), re.S)
        if not match:
            errors.append(f"{skill}: no frontmatter")
            continue
        meta = yaml.safe_load(match.group(1)) or {}
        name, desc = meta.get("name"), meta.get("description", "")
        if name != skill.parent.name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(name)):
            errors.append(f"{skill}: bad name {name!r}")
        if not desc or len(desc) > 1024:
            errors.append(f"{skill}: description is empty or over 1024 chars")
        if len(skill.read_text().splitlines()) >= 500:
            errors.append(f"{skill}: 500 lines or more")
        for link in re.findall(r"\]\(([^)#]+\.md)\)", skill.read_text()):
            if not (skill.parent / link).resolve().exists():
                errors.append(f"{skill}: dead link {link}")

for e in errors:
    print("ERROR", e)
print(f"{len(errors)} errors")
sys.exit(1 if errors else 0)
