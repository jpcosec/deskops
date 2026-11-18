REFORMULACION
Nodo ejecutable `task.code` en el repo `deskops`. Propósito: crear un rol especialista de SLDB que deje limpio el store tras una transición, disparado por un post-hook que solo encola. Resultado: (1) RoleDoc nuevo `sldb-store-specialist`; (2) modo `specialist` en `deskops runtime template`, con resolución automática por nombre/id terminado en `-specialist`, `_render_specialist_agents_md`, instrucciones mecánicas y `scion_child_identity` con prefijo `deskops-s-`; (3) ejemplo de hook `encola-especialista-de-store` en el manual. Límites: solo `scion.py`, `choices` de `--mode`, `tests/test_scion_runtime.py`, `docs/operator-manual.md` y el RoleDoc nuevo; checkout principal sin worktree ni rama; fuera sldb, declarar el hook en un desk, despachar al especialista y el runner de la cola; no tocar los archivos ya modificados enumerados.

AMBIGUEDADES
1. “guardar ambas salidas en el run_dir”: no nombra archivos ni formato. Obligaría a inventar nombres, extensión y ubicación exacta.
2. “gana un ejemplo de hook llamado `encola-especialista-de-store`… agrega una linea `<fecha UTC ISO> <DESKOPS_TASK_ID>`”: no da el `run:` ni cómo crear el directorio. Obligaría a inventar comando/script, shell, timeout y manejo de fallo; los hooks son listas de argumentos sin shell.
3. “la misma `--model` que declara `desk/roles/deskops-tester.md`”: no aclara si copiar el valor del campo `model` o repetir el flag. Obligaría a decidir formato y valor exacto.
4. “el coordinador despacha al especialista con `deskops runtime template sldb-store-specialist --mode specialist` y `scion start`”: no da el argv completo de `scion start`. Obligaría a inventar proyecto, workspace, auth, labels o dejar el ejemplo incompleto.

DRY-RUN
Lecturas: `scion.py` (validación/resolución de modo, renders, identidad), `registry.py`, tests vecinos, sección “Post-hooks on a transition” y RoleDoc tester para `model`. Cambios previstos: crear RoleDoc; aceptar `specialist`; añadir `_render_specialist_agents_md` con los puntos a–f; prefijo `deskops-s-`; `choices`; tests (a)–(e); ejemplo de hook. Dependencias: `deskops add role`, escritores de plantilla, `scion_child_identity`, `deskops message send` y modelo de hooks. Validaciones futuras: las cuatro del TaskDoc, sin ejecutar ahora.

FUTURO
Otro nodo o un humano declara el hook en un desk, implementa el runner que lee `runs/hooks/store-specialist.queue` y despacha con Scion. El especialista repara, deja cambios sin commitear y reporta; el coordinador revisa, commitea y cierra.
