#!/bin/bash
# Reproduce (c): edit task y message send con llaves, con traceback completo.
# Uso: c.sh <sandbox> <valor>
set -u
REPO=/mnt/ssd/proyectos/SLDB_1/deskops
SBX=$1; VAL=$2
export TMPDIR=/dev/shm PYTHONPATH=$REPO
PY="$REPO/../.venv/bin/python"
D() { echo "\$ deskops $*"; "$PY" -m deskops "$@"; echo "rc=$?"; }
if [ ! -d "$SBX/desk" ]; then
  /tmp/claude-1001/-mnt-ssd-proyectos-SLDB-1-deskops/a22bbd64-97de-49c2-a830-f2124c831405/scratchpad/sbx.sh "$SBX"
  cd "$SBX"; "$PY" -m deskops add task --title "Llaves c" --goal g --scope s --implementation-path i --done-when d --validation "echo ok" --root . >/dev/null 2>&1
fi
cd "$SBX"
TASK=task-llaves-c
printf 'valor enviado: %s\n' "$VAL"
D --debug edit task $TASK scope "$VAL" --root . 2>&1
echo "== scope guardado =="; sed -n '/^## Scope/,/^## /p' desk/tasks/$TASK.md | sed -n '3,6p'
D --debug message send --title "llaves" --kind unclear --root . "$VAL" 2>&1
echo "== inbox =="; ls desk/inbox; for n in desk/inbox/*.md; do sed -n "/^# /,\$p" "$n"; done
