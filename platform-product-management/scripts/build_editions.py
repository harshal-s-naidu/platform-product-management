#!/usr/bin/env python3
"""Assemble portable review editions and an allowlisted transfer archive.

Generated documents are derived from source modules, never from work context.
Refuses to package a populated or changed starter store. Does not install skills.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.1"
METHOD = [
    "references/operating-model.md", "references/workflows.md",
    "references/capabilities-and-target-state.md", "references/prioritization-and-roadmaps.md",
    "references/decisions-evidence-and-value.md", "references/reviews-and-communication.md",
    "references/data-contract.md", "references/persistence-and-handoffs.md",
    "references/excel-storage.md", "references/context-policy.md",
]
MASTER = ["DESIGN_REVIEW.md", "SKILL.md", "CLAUDE.md", "COPILOT_SKILL.md"] + METHOD + [
    "references/tool-adapters.md", "templates/work-products.md", "examples/worked-examples.md",
    "optional/BUILDER_BRIEF.md", "optional/UI_SPECIFICATION.md",
]
COPILOT = ["COPILOT_SKILL.md"] + METHOD + ["templates/work-products.md", "examples/worked-examples.md"]
SOURCE_FILES = [
    "START_HERE.md", "DESIGN_REVIEW.md", "SKILL.md", "CLAUDE.md", "COPILOT_SKILL.md",
    *METHOD, "references/tool-adapters.md", "templates/work-products.md", "examples/worked-examples.md",
    "optional/BUILDER_BRIEF.md", "optional/UI_SPECIFICATION.md", "context/organization.template.md",
    "schemas/state.schema.json", "data/state.json", "examples/sample-state.json", "VALIDATION.md",
    "scripts/validate_state.py", "scripts/test_validate_state.py", "scripts/build_editions.py",
]
GENERATED = ["MASTER_SPECIFICATION.md", "COPILOT_COMPLETE.md", "COPILOT_SKILL.txt", "COPILOT_COMPLETE.txt"]


def rewrite_links(text, origin):
    def replace(match):
        target = match.group(2)
        if target.startswith(("https://", "http://", "#", "mailto:")):
            return match.group(0)
        path, sep, anchor = target.partition("#")
        resolved = (origin.parent / path).resolve()
        relative = resolved.relative_to(ROOT).as_posix()
        return f"[{match.group(1)}]({relative}{sep}{anchor})"
    return re.sub(r"\[([^\]\n]+)\]\(([^)\s]+)\)", replace, text)


def assemble(title, sources, instruction):
    sections, toc = [], []
    for index, name in enumerate(sources, 1):
        path = ROOT / name
        body = path.read_text(encoding="utf-8")
        body = re.sub(r"\A---\n.*?\n---\n", "", body, flags=re.S).lstrip()
        heading = next((line.lstrip("# ") for line in body.splitlines() if line.startswith("# ")), name)
        anchor = f"section-{index}"
        toc.append(f"{index}. [{heading}](#{anchor}) — `{name}`")
        sections.append(f'<a id="{anchor}"></a>\n\nSource module: `{name}`\n\n' + rewrite_links(body, path))
    return (f"# {title}\n\nVersion {VERSION}. Generated from canonical modules; edit those sources, then regenerate.\n\n"
            + instruction + "\n\n## Contents\n\n" + "\n".join(toc) + "\n\n---\n\n"
            + "\n\n---\n\n".join(sections).rstrip() + "\n")


def check_links(names):
    errors = []
    for name in names:
        if not name.endswith(".md"):
            continue
        source = ROOT / name
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", source.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            path = target.split("#", 1)[0]
            resolved = (source.parent / path).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                errors.append(f"{name}: invalid local link {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated editions without writing")
    args = parser.parse_args()
    outputs = {
        "MASTER_SPECIFICATION.md": assemble(
            "Platform Product Management — complete specification", MASTER,
            "Full methodology, operating contracts and optional tool design. Do not load this entire edition for everyday tasks. SKILL.md routes to smaller modules. The machine-readable schema and fixtures remain companion files."),
        "COPILOT_COMPLETE.md": assemble(
            "Platform Product Management — complete Copilot reference", COPILOT,
            "Use the first section as runtime instructions and consult the remaining sections for the relevant task. All methodology is included here; companion file links are navigation aids and are not claims that Copilot can read a local folder. Fictional examples are not work data. The compact edition is preferable when its guidance is sufficient."),
    }
    outputs["COPILOT_SKILL.txt"] = (ROOT / "COPILOT_SKILL.md").read_text(encoding="utf-8")
    outputs["COPILOT_COMPLETE.txt"] = outputs["COPILOT_COMPLETE.md"]
    for name, content in outputs.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise ValueError(f"Generated edition is stale: {name}")
        else:
            path.write_text(content, encoding="utf-8")
    names = list(dict.fromkeys(SOURCE_FILES + GENERATED))
    errors = check_links(names)
    if errors:
        raise ValueError("\n".join(errors))
    manifest = {
        "package": "platform-product-management", "version": VERSION,
        "note": "Approximate tokens = characters/4, not a tokenizer or usage forecast. Excludes work context/history. Manifest excludes itself.",
        "files": [{"path": name, "bytes": (ROOT / name).stat().st_size,
                   "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                   "approx_tokens": round(len((ROOT / name).read_text(encoding="utf-8")) / 4)} for name in names],
    }
    manifest_path = ROOT / "MANIFEST.json"
    if args.check:
        if json.loads(manifest_path.read_text(encoding="utf-8")) != manifest:
            raise ValueError("Manifest is stale")
        print(f"PASS: {len(names)} allowlisted files, generated editions, local links and manifest.")
        return
    state = json.loads((ROOT / "data/state.json").read_text(encoding="utf-8"))
    if state["store_id"] != "pm-local-starter" or state["state_revision"] != 0 or any(value for value in state.values() if isinstance(value, list)):
        raise ValueError("Refusing transfer archive: starter state contains work data or has changed. Package from a clean portable copy.")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    archive = ROOT.parent / f"platform-product-management-{VERSION}.zip"
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        for name in names + ["MANIFEST.json"]:
            bundle.write(ROOT / name, arcname=f"platform-product-management/{name}")
    print(f"Built {len(names) + 1} files: {archive}")
    for name in ["SKILL.md", "COPILOT_SKILL.md", "COPILOT_COMPLETE.md", "MASTER_SPECIFICATION.md"]:
        item = next(item for item in manifest["files"] if item["path"] == name)
        print(f"{name}: {item['bytes']} bytes, ~{item['approx_tokens']} tokens (rough estimate)")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
