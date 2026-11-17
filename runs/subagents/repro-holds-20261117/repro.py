"""Reproduccion minima: desk sandbox (como el fixture lifecycle_desk) con una tarea task.code
en ritual-execution sin recibos de preflight; deskops view task --format json da holds true
en task_activates -> ritual-testing junto a un finding de nivel error."""
import contextlib, io, json, os, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO.parent / "sldb" / "src"))
os.environ["HOME"] = tempfile.mkdtemp(prefix="repro-holds-home-")
from deskops.atom_tags import sync_tag_declaration
from deskops.bootstrap import SLDBBootstrap
from deskops.lifecycle import write_lifecycle_graph
from deskops.workspace import seed_desk
from deskops.operations import DeskopsOperations
from deskops.cli.main import main
from tests.view_desk import install_views

root = Path(tempfile.mkdtemp(prefix="repro-holds-")) / "repo"; root.mkdir()
with contextlib.redirect_stdout(io.StringIO()):
    assert SLDBBootstrap().init_local_store(root) == 0
seed_desk(root); write_lifecycle_graph(root); sync_tag_declaration(root)
for a in (["init", "-q"], ["config", "user.email", "t@e.com"], ["config", "user.name", "T"], ["commit", "--allow-empty", "-q", "-m", "seed"]):
    subprocess.run(["git", *a], cwd=root, check=True)
os.chdir(root)
ops = DeskopsOperations(root)
tid = ops.create_task_bundle({"title": "Repro holds", "goal": "g", "scope": "s", "implementation_path": "i",
    "done_when": "d", "validation": ["pytest -q tests/test_x.py"], "task_type": "code"}).task_id
install_views(root)
print("SANDBOX", root); print("TASK", tid)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = main(["view", "task", tid, "--root", str(root), "--format", "json"])
out = buf.getvalue(); print("== deskops view task --format json rc", rc); print(out)
buf2 = io.StringIO()
with contextlib.redirect_stdout(buf2):
    rc2 = main(["show", "task", tid, "--root", str(root)])
print("== deskops show task rc", rc2); print(buf2.getvalue())
data = json.loads(out)
def gates(o):
    if isinstance(o, dict):
        if "holds" in o and "relation_type" in o: yield o
        for v in o.values(): yield from gates(v)
    elif isinstance(o, list):
        for v in o: yield from gates(v)
bad = [g for g in gates(data) if g["holds"] and any(f.get("level") == "error" for f in g.get("findings", []))]
print("== gates con holds true y finding error:", json.dumps(bad, ensure_ascii=False, indent=1))
print("REPRODUCIDO" if bad else "NO REPRODUCIDO")
# Contraste: la API de sldb que sí aplica los findings (edges_holding con document) excluye la arista.
from deskops import lifecycle
path, payload, _ = ops.task_record(tid)
doc = ops.task_document(path)
print("== document", doc)
print("== condition_holds('', payload) [lo que usa show_task]:", lifecycle.condition_holds("", payload))
print("== transitions_holding(document=...) [sldb edges_holding]:", [t.target for t in lifecycle.transitions_holding(root, "ritual-execution", payload, document=doc)])
print("== transitions_blocked(document=...) [sldb edges_blocked]:", [t.target for t in lifecycle.transitions_blocked(root, "ritual-execution", payload, doc)])
