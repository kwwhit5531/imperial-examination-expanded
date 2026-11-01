"""Structural checks for the prototype. Not a replacement for CK3 validation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "imperial_examination_expanded"
TOKEN = re.compile(r'#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|\?=|>=|<=|!=|=|>|<|[^\s{}=<>!?#]+')


def tokens(path):
    return [m.group() for m in TOKEN.finditer(path.read_text(encoding="utf-8-sig"))
            if not m.group().startswith("#")]


def blocks(seq):
    """Extract assignments while preserving duplicate keys (e.g. options)."""
    entries, i = [], 0
    while i < len(seq):
        key = seq[i]
        if i + 1 >= len(seq) or seq[i + 1] not in {"=", "?=", ">=", "<=", "!=", ">", "<"}:
            i += 1  # Bare list members, such as child on-action names.
            continue
        op, i = seq[i + 1], i + 2
        assert i < len(seq), f"Missing value for {key}"
        if seq[i] == "{":
            start, depth, i = i + 1, 1, i + 1
            while i < len(seq) and depth:
                depth += (seq[i] == "{") - (seq[i] == "}")
                i += 1
            assert depth == 0, f"Unclosed block {key}"
            value = seq[start:i - 1]
        else:
            value, i = seq[i], i + 1
        entries.append((key, op, value))
    return entries


def one(entries, key):
    found = [v for k, _, v in entries if k == key]
    assert len(found) == 1, f"Expected one {key}, found {len(found)}"
    return found[0]


def main():
    files = sorted(MOD.rglob("*.txt")) + [MOD / "descriptor.mod"]
    parsed = {}
    for path in files:
        if path.suffix == ".txt":
            assert path.read_bytes().startswith(b"\xef\xbb\xbf"), f"CK3 script requires UTF-8 BOM: {path}"
        seq = tokens(path)
        depth = 0
        for t in seq:
            depth += (t == "{") - (t == "}")
            assert depth >= 0, f"Unmatched closing brace in {path}"
        assert depth == 0, f"Unbalanced braces in {path}"
        parsed[path] = blocks(seq)

    loc_path = MOD / "localization/english/iee_examination_l_english.yml"
    assert loc_path.read_bytes().startswith(b"\xef\xbb\xbf"), "Localization requires UTF-8 BOM"
    loc = loc_path.read_text(encoding="utf-8-sig")
    assert loc.startswith("l_english:\n"), "Missing language header"
    loc_keys = re.findall(r'^ ([\w.]+):\d+ "(?:[^"\\]|\\.)*"$', loc, re.M)
    assert len(loc_keys) == len(set(loc_keys)), "Duplicate localization keys"
    assert len(loc_keys) == sum(bool(line.strip()) for line in loc.splitlines()[1:]), "Malformed localization line"
    loc_keys = set(loc_keys)

    event_path = MOD / "events/iee_examination_events.txt"
    event_entries = parsed[event_path]
    assert one(event_entries, "namespace") == "iee_examination"
    events = {k: blocks(v) for k, _, v in event_entries if k.startswith("iee_examination.")}
    # Require every expected encounter, including the original three. An ID is
    # the game's internal name, not the title displayed to the player.
    assert set(events) == {f"iee_examination.{i:04d}" for i in range(1, 16)}
    for name, event in events.items():
        assert one(event, "type") == "activity_event", name
        assert one(blocks(one(event, "cooldown")), "months") == "12", name
        trigger = one(event, "trigger")
        # IDs 0010-0015 belong to assistants; 0001-0009 belong to candidates.
        # Verify each event uses the checklist for its intended audience.
        gate = "iee_assistant_available_trigger" if int(name.rsplit('.', 1)[1]) >= 10 else "iee_narrative_available_trigger"
        assert gate in trigger, name
        assert any(t.startswith("var:iee_seen_") for t in trigger), name
        assert "iee_mark_narrative_seen_effect" in one(event, "immediate"), name
        assert sum(k == "option" for k, _, _ in event) >= 3, name

    all_seq = [t for p in files for t in tokens(p)]
    referenced_loc = {t for t in all_seq if re.fullmatch(r"iee_examination\.\d{4}\.[\w.]+", t)}
    referenced_loc |= {t for t in all_seq if re.fullmatch(r"iee_score_\w+_tt", t)}
    referenced_loc |= {t for t in all_seq if re.fullmatch(r"iee_\w+_opinion", t)}
    assert referenced_loc <= loc_keys, f"Missing localization: {referenced_loc - loc_keys}"

    definitions = {k for entries in parsed.values() for k, _, _ in entries if k.startswith("iee_")}
    helper_refs = {t for t in all_seq if re.fullmatch(r"iee_\w+_(?:trigger|effect)", t)}
    assert helper_refs <= definitions, f"Undefined helpers: {helper_refs - definitions}"

    hook = parsed[MOD / "common/on_action/iee_examination_on_actions.txt"]
    vanilla_extension = blocks(one(hook, "imperial_examination_exam_entrant_events"))
    assert [k for k, _, _ in vanilla_extension] == ["on_actions"], "Vanilla pool replaced"
    assert one(vanilla_extension, "on_actions") == ["iee_examination_narrative_pulse"]
    child = blocks(one(hook, "iee_examination_narrative_pulse"))
    pool = blocks(one(child, "random_events"))
    assert one(pool, "chance_to_happen") == "20"
    assert {v for k, _, v in pool if k.isdigit()} == {f"iee_examination.{i:04d}" for i in range(1, 10)}
    # Assistants receive the assembly/preparation callback. Check that we only
    # attach our child pool, leaving the base game's own event selection intact.
    assistant_hook = blocks(one(hook, "imperial_examination_pulse"))
    assert [k for k, _, _ in assistant_hook] == ["on_actions"]
    assert one(assistant_hook, "on_actions") == ["iee_assistant_narrative_pulse"]
    assistant = blocks(one(hook, "iee_assistant_narrative_pulse"))
    assert "iee_assistant_available_trigger" in one(assistant, "trigger")
    assistant_pool = blocks(one(assistant, "random_events"))
    assert {v for k, _, v in assistant_pool if k.isdigit()} == {f"iee_examination.{i:04d}" for i in range(10, 16)}
    # Assistance rewards must not invoke our candidate-score helper, either
    # when a panel opens or when a button is clicked. This is a static check;
    # it cannot prove every possible runtime effect inside the actual game.
    for name, event in events.items():
        if int(name.rsplit('.', 1)[1]) >= 10:
            assert "iee_adjust_performance_effect" not in one(event, "immediate")
            for key, _, value in event:
                if key == "option":
                    assert "iee_adjust_performance_effect" not in value

    effects = parsed[MOD / "common/scripted_effects/iee_examination_effects.txt"]
    score = one(effects, "iee_adjust_performance_effect")
    assert "iee_is_exam_candidate_trigger" in score
    for variable in ("temporary_exam_score", "imperial_examination_score"):
        assert score.count(variable) == 3, f"Missing existing/new score handling: {variable}"
    assert "had_essay_examination" not in all_seq
    assert "had_classics_examination" not in all_seq
    assert "had_poetry_examination" not in all_seq
    assert not list((MOD / "common").glob("activities/**/*")), "Unexpected activity override"

    # Parameter names at all calls must match their helper definitions.
    params = {}
    for k, _, v in effects:
        params[k] = set(re.findall(r"\$([A-Z_]+)\$", " ".join(v)))
    def visit(entries):
        for key, _, value in entries:
            if isinstance(value, list):
                if key in params:
                    actual = {k for k, _, _ in blocks(value)}
                    assert actual == params[key], f"Wrong parameters for {key}: {actual}"
                visit(blocks(value))
    for entries in parsed.values():
        for _, _, value in entries:
            if isinstance(value, list):
                visit(blocks(value))

    print(f"PASS: {len(files)} script/descriptor files; {len(events)} events; {len(loc_keys)} localization keys")
    print("PASS: additive dispatch, eligibility/seen guards, cooldowns, three choices, helper parameters, dual score updates")
    print("Runtime dispatch, scopes, effects and UI must also be checked in CK3.")


if __name__ == "__main__":
    main()
