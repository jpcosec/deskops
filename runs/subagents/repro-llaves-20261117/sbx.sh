#!/bin/bash
# Crea un desk sandbox con deskops init y una tarea task.code
set -u
REPO=/mnt/ssd/proyectos/SLDB_1/deskops
SBX=$1
export TMPDIR=/dev/shm PYTHONPATH=$REPO
D() { "$REPO/../.venv/bin/python" -m deskops "$@"; }
rm -rf "$SBX"; mkdir -p "$SBX"; cd "$SBX"
git init -q; git config user.email t@e.com; git config user.name T
D init . >/dev/null
echo seed > seed.txt
printf '.deskops.log\n.sldb_cache/\n.sldb/runtime/\n' > .gitignore
git add -A; git commit -q -m seed
