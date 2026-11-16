---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:24:53'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# piloto scion fase 1: brechas del coordinador y del ejecutor claude en contenedor

_Describe the incoming message with enough evidence to triage._

Piloto scion en IR, fase 1 (reports/scion-piloto-ir-20261115.md, sección Fase 1). Arreglado en deskops 366f24d2: command_args sale como flag=valor, porque --allowedTools de claude es variádico y se tragaba el prompt de la tarea (el coordinador arrancaba sin tarea). Quedan abiertas: (1) la imagen scion-claude no trae pi, así que el coordinador no puede correr deskops review preflight/bundle (engine por defecto runtime-pi-deepseek-flash). Hoy los corre el supervisor en el host. Falta un engine de review que funcione dentro del contenedor (claude) o que el hook instale pi con su secret. (2) Los tools del RoleDoc están en vocabulario pi (read, grep, find, ls, bash) y pasan tal cual a --allowedTools de claude, donde no son nombres válidos (Read, Grep, Glob, Bash). Con bypass permissions no tiene efecto, pero el runtime profile debería traducirlos. (3) El coordinador despachó sin escribir el RunDoc de intención que pide su agents.md, y con los recibos preflight/bundle en stale: resolver las ambigüedades con edit task cambia el input. Es la misma brecha de la fase 0, pero el contrato del coordinador no dice qué hacer. (4) El ejecutor no tiene pytest ni pytest-xdist en el entorno de sldb: armó un PYTHONPATH con el .venv de IR y los site-packages del tool sldb. El hook deskops-tools debería instalar los extras de test del repo de la tarea. (5) El template pone model medium, que en el harness claude es sonnet-5-5, mientras que el RoleDoc pide opus. El alias debería salir del RoleDoc o quedar declarado.
