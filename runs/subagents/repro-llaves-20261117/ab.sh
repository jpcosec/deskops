#!/bin/bash
# Reproduce (a) closeout verify escribe recibos y (b) --reason con llaves en closeout commit.
# Uso: ab.sh <sandbox> <reason>
set -u
REPO=/mnt/ssd/proyectos/SLDB_1/deskops
SBX=$1; REASON=$2; MODE=${3:-verify}
export TMPDIR=/dev/shm PYTHONPATH=$REPO
D() { echo "\$ deskops $*"; "$REPO/../.venv/bin/python" -m deskops "$@"; echo "rc=$?"; }
/tmp/claude-1001/-mnt-ssd-proyectos-SLDB-1-deskops/a22bbd64-97de-49c2-a830-f2124c831405/scratchpad/sbx.sh "$SBX"
cd "$SBX"
D add task --title "Llaves repro" --goal g --scope s --implementation-path i --done-when d --validation "echo ok" --task-type task.external --root . >/dev/null
TASK=$(ls desk/tasks | grep '^task-llaves-repro' | sed 's/\.md$//')
echo "task=$TASK"
D edit task "$TASK" references '["https://example.com/evidencia"]' --root . >/dev/null
git add -A; git commit -q -m "task autorada"
echo "== HEAD antes =="; git log --oneline -1
echo "== status antes de verify =="; git status --short
if [ "$MODE" != noverify ]; then D closeout verify --task "$TASK" --root . 2>&1 | tail -3; fi
echo "== status despues de verify (contrato (a): vacio) =="; git status --short
if [ "$MODE" != uncommitted ]; then git add -A; git commit -q -m "recibos de verify"; fi
if [ "$MODE" = stale ]; then D edit task "$TASK" references '["https://example.com/evidencia-2"]' --root . >/dev/null; git add -A; git commit -q -m "referencia cambiada: recibo 1 queda changed"; fi
if [ "$MODE" = reverify ]; then D edit task "$TASK" references '["https://example.com/evidencia-2"]' --root . >/dev/null; git add desk/tasks .sldb; git commit -q -m "referencia cambiada"; D closeout verify --task "$TASK" --root . 2>&1 | tail -2; echo "== status tras 2.o verify (sin commitear) =="; git status --short; fi
echo "modo=$MODE"
echo "== closeout commit --no-run --reason =="
printf 'reason enviado: %s\n' "$REASON"
echo cambio >> seed.txt
D closeout commit --task "$TASK" --no-run --reason "$REASON" --paths seed.txt --root . 2>&1
echo "== HEAD despues =="; git log -1 --format='%H%n%B'
echo "== Closeout-Reason del commit =="; git log -1 --format='%(trailers:key=Closeout-Reason,valueonly)'
echo "== status despues del cierre (contrato (b): vacio) =="; git status --short
echo "== recibos en HEAD =="; git ls-files desk/reviews; ls desk/reviews/*/ 2>/dev/null
