# Resultado
Causa: reap usaba `rev-list --cherry-pick --right-only base...branch`, que descarta commits con patch-id igual al de un commit ya en main (p.ej. el commit 'run:'); contaba 0 y borraba la rama.
Cambios (commit en rama deskops/deskops-e-3fb184ce4673):
- deskops/dispatch.py: `rev-list --reverse --no-merges base..branch`; cherry-pick con --keep-redundant-commits; si cuenta 0 y la punta no esta en base, no borra y sale 8 nombrando rama y punta.
- tests/test_dispatch.py: test de reproduccion (falla sin el arreglo: ver reproduction.log) y test de la guarda.
- CHANGELOG.md.
Validacion: tests/test_dispatch.py -n 4: 42 passed en es_ES y en_US (validation.log). Un fallo aislado en en_US durante una corrida concurrente no se repitio.
Revisar: --keep-redundant-commits deja un commit vacio si el parche ya estaba en main.

Bloqueo: deskops advance task quedo bloqueado: rule-activation-task-debug exige recibos preflight y reproduction aceptados (seen: {}); no es del alcance del ejecutor.

## Segundo commit (carrera reap/commit del ejecutor)
- dispatch.py: antes de parar/borrar un ejecutor, `git status --porcelain` del worktree: con cambios imprime `en espera: el worktree de <n> tiene cambios sin commitear` y sale 3; ejecutor con result-summary pero phase running y activity fuera de completed/stopped/exited: `en espera: <n> sigue vivo`, sale 3; `git worktree remove` sin --force. Mismo chequeo de sucio dentro de _integrate_branch.
- tests: 2 nuevos (fallan antes, pasan despues; salida en reproduction.log). tests/test_dispatch.py -n 4: 44 passed en es_ES y en_US (validation-2.log).
- Nota: un ejecutor con result-summary y activity working ya no se reapea hasta que termine.
