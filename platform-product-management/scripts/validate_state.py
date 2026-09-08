#!/usr/bin/env python3
"""Read-only validator for this package's schema subset and PM invariants.

No dependencies, network calls, writes, or general JSON Schema compliance claim.
Unknown schema keywords fail explicitly. Use a full Draft 2020-12 validator too
when integrating with a production write service.
"""

import argparse
from datetime import date, datetime
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = (
    "use_cases", "capabilities", "use_case_capabilities", "roadmap_items",
    "dependencies", "decisions", "assumptions", "risks", "metrics", "evidence",
)
SUPPORTED = {
    "$schema", "$defs", "$ref", "title", "description", "type", "properties",
    "additionalProperties", "required", "allOf", "items", "uniqueItems",
    "minItems", "minLength", "minimum", "enum", "const", "pattern", "format",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"Duplicate JSON object key: {key}")
            result[key] = value
        return result
    def bad_constant(value):
        raise ValueError(f"Non-finite JSON number: {value}")
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=pairs, parse_constant=bad_constant)


def inspect_schema(schema):
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise ValueError(f"Unsupported schema keywords: {sorted(unknown)}")
    for container in ("$defs", "properties"):
        for child in schema.get(container, {}).values():
            inspect_schema(child)
    for child in schema.get("allOf", []):
        inspect_schema(child)
    if "items" in schema:
        inspect_schema(schema["items"])


def matches_type(value, kind):
    checks = {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "integer": lambda: type(value) is int,
        "number": lambda: type(value) in (int, float) and math.isfinite(value),
        "boolean": lambda: type(value) is bool,
        "null": lambda: value is None,
    }
    if kind not in checks:
        raise ValueError(f"Unsupported schema type: {kind}")
    return checks[kind]()


def check_shape(value, schema, root, path="$", errors=None):
    errors = [] if errors is None else errors
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            raise ValueError(f"Unsupported schema reference: {ref}")
        check_shape(value, root["$defs"][ref.rsplit("/", 1)[1]], root, path, errors)
    for child in schema.get("allOf", []):
        check_shape(value, child, root, path, errors)
    if "type" in schema:
        kinds = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(matches_type(value, kind) for kind in kinds):
            errors.append(f"{path}: expected {'/'.join(kinds)}")
            return errors
    if "const" in schema and canonical(value) != canonical(schema["const"]):
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and canonical(value) not in [canonical(v) for v in schema["enum"]]:
        errors.append(f"{path}: value outside allowed enum")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{path}: unknown property {key}")
        for key, child in properties.items():
            if key in value:
                check_shape(value[key], child, root, f"{path}.{key}", errors)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if schema.get("uniqueItems") and len({canonical(v) for v in value}) != len(value):
            errors.append(f"{path}: duplicate array values")
        if "items" in schema:
            for index, item in enumerate(value):
                check_shape(item, schema["items"], root, f"{path}[{index}]", errors)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string too short")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: invalid pattern")
        try:
            if schema.get("format") == "date":
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError()
                date.fromisoformat(value)
            elif schema.get("format") == "date-time":
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", value):
                    raise ValueError()
                datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            errors.append(f"{path}: invalid {schema['format']}")
    if type(value) in (int, float) and "minimum" in schema and value < schema["minimum"]:
        errors.append(f"{path}: below minimum")
    return errors


def records(state):
    return [record for collection in COLLECTIONS for record in state[collection]]


def timestamp(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def validate(state, previous=None):
    schema = load_json(ROOT / "schemas/state.schema.json")
    inspect_schema(schema)
    errors = check_shape(state, schema, schema)
    warnings = []
    if errors:
        return errors, warnings
    all_records = records(state)
    by_id = {r["id"]: r for r in all_records}
    if len(by_id) != len(all_records):
        errors.append("Duplicate record IDs")

    def link(source, target, prefixes=None):
        if target not in by_id:
            errors.append(f"{source}: dangling reference {target}")
        if target == source:
            errors.append(f"{source}: self reference")
        if prefixes and target.split("-", 1)[0] not in prefixes:
            errors.append(f"{source}: wrong reference type {target}")

    typed_arrays = {"use_case_ids": {"UC"}, "capability_ids": {"CAP"},
                    "metric_ids": {"MET"}, "assumption_ids": {"ASM"}, "target_ids": None}
    typed_single = {"use_case_id": {"UC"}, "capability_id": {"CAP"},
                    "dependent_id": {"UC", "CAP", "RM"},
                    "prerequisite_id": {"UC", "CAP", "RM"}, "supersedes_id": {"DEC"}}
    for record in all_records:
        rid, attrs = record["id"], record["attributes"]
        if not timestamp(record["created_at"]) <= timestamp(record["updated_at"]) <= timestamp(state["updated_at"]):
            errors.append(f"{rid}: inconsistent timestamps")
        for target in record["evidence_ids"]:
            link(rid, target, {"EVD"})
        for field, prefixes in typed_arrays.items():
            for target in attrs.get(field, []):
                link(rid, target, prefixes)
        for field, prefixes in typed_single.items():
            if field in attrs:
                link(rid, attrs[field], prefixes)
        if record["owner"] is None and record["status"] in {"active", "selected", "in_progress", "production", "available"} and not rid.startswith("LNK-"):
            warnings.append(f"{rid}: active work/service has no recorded owner")
        if rid.startswith("RM-"):
            date_fields = {"date", "date_kind", "date_source"}
            if date_fields & attrs.keys() and not date_fields <= attrs.keys():
                errors.append(f"{rid}: date requires kind and source together")
            if "experiment" in attrs and attrs["kind"] != "learning":
                errors.append(f"{rid}: experiment requires learning kind")
            if not attrs.get("use_case_ids") and not attrs.get("capability_ids"):
                warnings.append(f"{rid}: no linked use case or capability")
            if record["status"] == "achieved" and (not attrs.get("exit_criteria") or not record["evidence_ids"]):
                warnings.append(f"{rid}: achievement needs exit criteria and evidence review")
        if rid.startswith("DEC-"):
            if attrs.get("chosen_option") and attrs["chosen_option"] not in attrs["options"]:
                errors.append(f"{rid}: chosen option is not among options")
            if record["status"] in {"adopted", "superseded"}:
                if not record["owner"] or not attrs.get("chosen_option") or not attrs.get("decided_on"):
                    errors.append(f"{rid}: adopted/superseded decision needs owner, choice and date")
                if attrs["provisional"] and not attrs.get("revisit_trigger"):
                    errors.append(f"{rid}: provisional adopted decision needs revisit trigger")
            prior = by_id.get(attrs.get("supersedes_id"))
            if prior and record["status"] in {"adopted", "superseded"} and prior["status"] != "superseded":
                errors.append(f"{rid}: superseded predecessor status not updated")
        if rid.startswith("RISK-") and record["status"] in {"accepted", "closed"}:
            if not attrs.get("acceptance_or_closure_basis"):
                errors.append(f"{rid}: acceptance/closure requires basis")
            if record["status"] == "accepted" and not record["owner"]:
                errors.append(f"{rid}: risk acceptance requires owner")
        if rid.startswith("ASM-") and record["status"] in {"validated", "invalidated"}:
            if not attrs.get("test_result") or not record["evidence_ids"]:
                warnings.append(f"{rid}: assumption result/evidence needs review")
        if rid.startswith("DEP-"):
            if attrs["dependent_id"] == attrs["prerequisite_id"]:
                errors.append(f"{rid}: self dependency")
            if record["status"] == "resolved" and not attrs.get("resolution"):
                errors.append(f"{rid}: resolved dependency requires resolution")
            if record["status"] == "confirmed" and not record["evidence_ids"]:
                warnings.append(f"{rid}: confirmed dependency lacks linked evidence")

    pairs = [(r["attributes"]["use_case_id"], r["attributes"]["capability_id"]) for r in state["use_case_capabilities"]]
    if len(set(pairs)) != len(pairs):
        errors.append("Duplicate use-case/capability relationship")

    graph = {}
    for dep in state["dependencies"]:
        attrs = dep["attributes"]
        if dep["status"] == "confirmed" and attrs["strength"] == "hard":
            graph.setdefault(attrs["dependent_id"], []).append(attrs["prerequisite_id"])
    # Iterative DFS avoids recursion depth limits on a long dependency chain.
    done = set()
    for start in graph:
        if start in done:
            continue
        path, active = [start], {start}
        stack = [(start, iter(graph.get(start, [])))]
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                done.add(node)
                active.remove(node)
                path.pop()
                stack.pop()
            elif child in active:
                cycle = path[path.index(child):] + [child]
                warnings.append("Hard confirmed dependency cycle; no feasible linear sequence: " + " requires ".join(cycle))
            elif child not in done:
                active.add(child)
                path.append(child)
                stack.append((child, iter(graph.get(child, []))))

    # A supersession chain cannot loop: unlike dependency cycles this is invalid history.
    for dec in state["decisions"]:
        seen, current = set(), dec
        while current and current["id"].startswith("DEC-"):
            if current["id"] in seen:
                errors.append(f"{dec['id']}: cyclic decision supersession")
                break
            seen.add(current["id"])
            current = by_id.get(current["attributes"].get("supersedes_id"))

    if previous is not None:
        prev_errors, _ = validate(previous)
        if prev_errors:
            errors.append("Previous state is invalid; cannot verify transition")
        else:
            old = {r["id"]: r for r in records(previous)}
            if state["store_id"] != previous["store_id"]:
                errors.append("Store identity changed")
            if state["state_revision"] != previous["state_revision"] + 1:
                errors.append("State revision must advance exactly once")
            if timestamp(state["updated_at"]) < timestamp(previous["updated_at"]):
                errors.append("State timestamp moved backwards")
            for rid in old.keys() - by_id.keys():
                errors.append(f"{rid}: removed record; ordinary updates must preserve history via lifecycle status")
            for rid, record in by_id.items():
                if rid not in old:
                    if record["record_version"] != 1:
                        errors.append(f"{rid}: new record must start at version 1")
                    continue
                prior = old[rid]
                if record["created_at"] != prior["created_at"]:
                    errors.append(f"{rid}: creation timestamp changed")
                content = {k: v for k, v in record.items() if k not in {"record_version", "updated_at"}}
                prior_content = {k: v for k, v in prior.items() if k not in {"record_version", "updated_at"}}
                changed = content != prior_content
                if changed:
                    if record["record_version"] != prior["record_version"] + 1:
                        errors.append(f"{rid}: changed record version must advance once")
                    if timestamp(record["updated_at"]) < timestamp(prior["updated_at"]):
                        errors.append(f"{rid}: record timestamp moved backwards")
                elif record != prior:
                    errors.append(f"{rid}: unchanged content must retain version and timestamp")
            if all_records == records(previous):
                errors.append("No record changes; do not increment state revision for a no-op")
    return sorted(set(errors)), sorted(set(warnings))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--previous", type=Path, help="Check an ordinary update against its exact prior state")
    args = parser.parse_args()
    try:
        errors, warnings = validate(load_json(args.state), load_json(args.previous) if args.previous else None)
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    print(f"{len(errors)} errors; {len(warnings)} warnings. Business truth and authority require review.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
