"""atom.adr: an accepted decision is an atom that answers why (deskops/models/adr.py).

Covers the model (a type only adds; AtomDoc's contract is untouched), ``add atom --atom-type``,
the two seeded rules (owner receipt; supersedes consistency, partial replacement ignored),
the typed listing (accepted by default, ``--all`` for the rest), the Markdown materialization
and a ``task.decision`` that cites the ADR.
"""

from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

import pytest

from deskops.cli.main import main
from deskops.models import ATOM_TYPE_MODELS, AtomAdrDoc, AtomDoc
from deskops.models.adr import ADR_TYPE
from deskops.operations import DeskopsOperations
from deskops.paths import package_pythonpath


def _run(argv: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(argv)
    return code, buffer.getvalue()


def _add_adr(root: Path, title: str, *extra: str) -> tuple[int, str]:
    return _run(
        [
            "add", "atom", "--root", str(root), "--atom-type", ADR_TYPE, "--title", title,
            "--decided-on", "2026-11-25", "--decided-by", "JP",
            "--answer", f"Decision of {title}.", "--context", "Context.", "--consequences", "Consequences.",
            *extra,
        ]
    )


def _findings(root: Path, adr_id: str) -> list[dict]:
    from sldb.api import rules_check

    return [
        finding.as_dict()
        for finding in rules_check(root / ".sldb", subject=f"AtomAdrDoc:{adr_id}", pythonpath=package_pythonpath())
    ]


def _owner_accept(root: Path, adr_id: str) -> str:
    code, out = _run(["review", "record", adr_id, "--kind", "owner", "--reason", "approved by the owner", "--root", str(root)])
    assert code == 0, out
    review_id = next(line.split()[-1] for line in out.splitlines() if "review-" in line and line.split()[-1].startswith("review-"))
    code, out = _run(["review", "dispose", review_id, "--verdict", "accepted", "--reason", "owner ok", "--root", str(root)])
    assert code == 0, out
    return review_id


def _codes(findings: list[dict]) -> set[str]:
    return {item["code"] for item in findings}


# ------------------------------------------------------------------ the model
def test_a_type_only_adds_and_the_untyped_atom_contract_is_unchanged() -> None:
    assert ATOM_TYPE_MODELS == {"atom.adr": AtomAdrDoc}
    assert issubclass(AtomAdrDoc, AtomDoc)
    assert set(AtomDoc.model_fields) <= set(AtomAdrDoc.model_fields)
    assert {"atom_type", "status", "decided_on", "decided_by", "context", "consequences", "alternatives",
            "supersedes", "partial_supersedes", "references"} <= set(AtomAdrDoc.model_fields) - set(AtomDoc.model_fields) | {"references"}
    assert "atom_type" not in AtomDoc.model_fields and "status" not in AtomDoc.model_fields
    # AtomDoc's contract hash is the one the snapshot pins: the subtype did not move it.
    from sldb.store.hashing import hash_model_contract

    snapshot = json.loads(
        (Path(__file__).with_name("fixtures") / "model_contract_hashes.json").read_text()
    )
    assert hash_model_contract(AtomDoc) == snapshot["AtomDoc"]
    assert "decided_by" not in json.dumps(AtomDoc.model_json_schema(), sort_keys=True)


def test_the_adr_answers_why_and_has_two_states() -> None:
    payload = dict(id="atom-x", title="T", answer="A", context="C", consequences="Q", decided_on="2026-11-25", decided_by="JP")
    adr = AtomAdrDoc(**payload)
    assert adr.five_wh_one_plus.value == "why" and adr.status == "accepted"
    with pytest.raises(ValueError):
        AtomAdrDoc(**payload, status="proposed")
    with pytest.raises(ValueError):
        AtomAdrDoc(**{**payload, "context": " "})


# ------------------------------------------------------------------ add atom --atom-type
def test_add_atom_atom_type_creates_the_record_and_it_is_tracked_under_its_model(lifecycle_desk: Path) -> None:
    code, out = _add_adr(lifecycle_desk, "Pron is archived", "--references", "sldb/README.md")
    assert code == 0, out
    path = lifecycle_desk / "desk" / "atoms" / "atom-pron-is-archived.md"
    assert path.is_file()
    from sldb.api.stores.doc_status import doc_status

    assert doc_status(lifecycle_desk / ".sldb", "desk/atoms/atom-pron-is-archived.md").model == "AtomAdrDoc"
    code, out = _run(["show", "atom", "atom-pron-is-archived", "--root", str(lifecycle_desk), "--format", "json"])
    assert code == 0, out
    shown = json.loads(out)
    assert shown["atom_type"] == "atom.adr" and shown["status"] == "accepted" and shown["references"] == ["sldb/README.md"]
    code, out = _run(["atoms", "validate", "atom-pron-is-archived", "--root", str(lifecycle_desk)])
    assert code == 0, out


def test_an_unknown_atom_type_is_refused(lifecycle_desk: Path) -> None:
    code, _out = _run(["add", "atom", "--root", str(lifecycle_desk), "--atom-type", "atom.nope", "--title", "x"])
    assert code != 0
    assert not (lifecycle_desk / "desk" / "atoms" / "atom-x.md").exists()


def test_the_untyped_atom_is_created_as_before(lifecycle_desk: Path) -> None:
    code, out = _run(["add", "atom", "--root", str(lifecycle_desk), "--title", "Plain", "--five-wh-one-plus", "what", "--answer", "a"])
    assert code == 0, out
    text = (lifecycle_desk / "desk" / "atoms" / "atom-plain.md").read_text(encoding="utf-8")
    assert "atom_type" not in text and "## Answer" in text


# ------------------------------------------------------------------ rules
def test_without_an_owner_receipt_the_rule_rejects_the_adr_and_with_one_it_passes(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "One decision")[0] == 0
    adr_id = "atom-one-decision"
    assert "rules/rule-adr-owner-receipt" in _codes(_findings(lifecycle_desk, adr_id))
    _owner_accept(lifecycle_desk, adr_id)
    assert "rules/rule-adr-owner-receipt" not in _codes(_findings(lifecycle_desk, adr_id))


def test_a_pending_owner_receipt_is_not_enough(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Pending one")[0] == 0
    code, out = _run(["review", "record", "atom-pending-one", "--kind", "owner", "--reason", "r", "--root", str(lifecycle_desk)])
    assert code == 0, out
    assert "rules/rule-adr-owner-receipt" in _codes(_findings(lifecycle_desk, "atom-pending-one"))


def test_superseding_marks_the_earlier_adr_and_the_consistency_rule_passes(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Old decision")[0] == 0
    code, out = _add_adr(lifecycle_desk, "New decision", "--supersedes", "atom-old-decision")
    assert code == 0, out
    old = (lifecycle_desk / "desk" / "atoms" / "atom-old-decision.md").read_text(encoding="utf-8")
    assert "status: superseded" in old
    assert "rules/rule-adr-supersedes" not in _codes(_findings(lifecycle_desk, "atom-old-decision"))
    relation = lifecycle_desk / "desk" / "supersessions" / "supersedes-atom-new-decision-atom-old-decision.md"
    assert relation.is_file() and "AtomAdrDoc:atom-old-decision" in relation.read_text(encoding="utf-8")


def test_the_consistency_rule_rejects_an_accepted_adr_replaced_by_an_accepted_one(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Old decision")[0] == 0
    assert _add_adr(lifecycle_desk, "New decision", "--supersedes", "atom-old-decision")[0] == 0
    # Undo only the effect: the earlier ADR is edited back to accepted.
    code, out = _run(["edit", "atom", "atom-old-decision", "status", "accepted", "--root", str(lifecycle_desk)])
    assert code == 0, out
    assert "rules/rule-adr-supersedes" in _codes(_findings(lifecycle_desk, "atom-old-decision"))


def test_a_partial_replacement_leaves_the_earlier_adr_accepted_and_the_rule_ignores_it(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Kgdb absorbed")[0] == 0
    code, out = _add_adr(
        lifecycle_desk, "Pron section replaced", "--partial-supersedes", "atom-kgdb-absorbed",
        "--superseded-section", "pron",
    )
    assert code == 0, out
    old = (lifecycle_desk / "desk" / "atoms" / "atom-kgdb-absorbed.md").read_text(encoding="utf-8")
    assert "status: accepted" in old
    assert "rules/rule-adr-supersedes" not in _codes(_findings(lifecycle_desk, "atom-kgdb-absorbed"))
    relation = (lifecycle_desk / "desk" / "supersessions" / "supersedes-atom-pron-section-replaced-atom-kgdb-absorbed.md").read_text(encoding="utf-8")
    assert "section: pron" in relation


def test_a_partial_replacement_needs_its_section(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Base")[0] == 0
    with pytest.raises(ValueError, match="superseded_section"):
        DeskopsOperations(lifecycle_desk).create_artifact(
            "artifact.atom",
            {"atom_type": ADR_TYPE, "title": "Part", "answer": "a", "context": "c", "consequences": "q",
             "decided_on": "2026-11-25", "decided_by": "JP", "partial_supersedes": ["atom-base"]},
        )


# ------------------------------------------------------------------ listing
def test_listing_the_type_shows_only_accepted_by_default_and_all_shows_the_rest(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Old decision")[0] == 0
    assert _add_adr(lifecycle_desk, "New decision", "--supersedes", "atom-old-decision")[0] == 0
    _run(["add", "atom", "--root", str(lifecycle_desk), "--title", "Plain", "--five-wh-one-plus", "what", "--answer", "a"])
    root = str(lifecycle_desk)
    _, out = _run(["list", "atoms", "--root", root, "--type", ADR_TYPE])
    assert "atom-new-decision" in out and "atom-old-decision" not in out and "atom-plain" not in out
    _, out = _run(["list", "atoms", "--root", root, "--type", ADR_TYPE, "--all"])
    assert "atom-new-decision" in out and "atom-old-decision" in out and "atom-plain" not in out
    _, out = _run(["list", "atoms", "--root", root])
    assert {"atom-new-decision", "atom-old-decision", "atom-plain"} <= {line.split(" | ")[0] for line in out.splitlines()}


# ------------------------------------------------------------------ materialization
def test_materializing_an_adr_writes_the_markdown_sections(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Old decision")[0] == 0
    assert _add_adr(lifecycle_desk, "New decision", "--supersedes", "atom-old-decision", "--references", "sldb/README.md")[0] == 0
    out_file = lifecycle_desk / "docs" / "new-decision.md"
    code, out = _run(["materialize", "--root", str(lifecycle_desk), "--adr", "atom-new-decision", "--out", str(out_file)])
    assert code == 0, out
    text = out_file.read_text(encoding="utf-8")
    for expected in ("- Status: accepted", "- Date: 2026-11-25", "- Decision Maker: JP", "- Supersedes: `atom-old-decision`",
                     "## Context", "## Decision", "## Consequences", "- sldb/README.md"):
        assert expected in text, expected


# ------------------------------------------------------------------ task.decision
def test_a_task_decision_closes_citing_the_adr(lifecycle_desk: Path) -> None:
    assert _add_adr(lifecycle_desk, "Cited decision")[0] == 0
    bundle = DeskopsOperations(lifecycle_desk).create_task_bundle(
        {"title": "Decide it", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d",
         "validation": ["none"], "task_type": "task.decision", "atoms": ["atom-cited-decision"]}
    )
    text = bundle.task_path.read_text(encoding="utf-8")
    assert "atom-cited-decision" in text
    code, out = _run(["show", "task", bundle.task_id, "--root", str(lifecycle_desk)])
    assert code == 0, out
