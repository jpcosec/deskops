## REFORMULACION

Nodo ejecutable `task.code` en el repo `deskops`. Propósito: que `deskops doctor` detecte stores `.sldb` con layout viejo mediante tres señales —`.sldb/runtime/`, `.sldb/journal` o una línea del `.gitignore` raíz que ignore `.sldb/core` o `.sldb/runtime`— y reporte el remedio exacto `sldb stores migrate-layout --store <ruta>/.sldb`; mientras exista una señal no debe imprimir `Desk is healthy`. Resultado: chequeo en doctor, fallo de `init` con el mismo remedio, documentación en README y skill, y tests. Límites: no ejecutar migraciones en otros repos, no avisar al ecosistema y no cambiar `sldb`.

## AMBIGUEDADES

1. «el .gitignore raiz tiene una linea que ignora .sldb/core o .sldb/runtime»: no define sintaxis admitida, comentarios, negaciones ni coincidencia exacta; obligaría a inventar la regla de detección.
2. «alrededor de las lineas 220-231 donde imprime Desk is healthy» y «o el servicio que arma sus findings»: no fija archivo ni punto exacto; obligaría a elegir ubicación.
3. «salir con codigo distinto de 0»: no fija el código; obligaría a inventarlo.
4. «tests nuevos»: no nombra archivos ni ubicación; obligaría a decidir nombres y organización.
5. «El README y la skill .claude/skills/deskops-workflow/SKILL.md documentan el procedimiento»: no fija sección ni formato; obligaría a inventar dónde insertarlo.

## DRY-RUN

Sin ejecutar nada, un ejecutor futuro leería `doctor.py`, el servicio de findings, `bootstrap.py`, README, la skill, tests existentes y `sldb stores migrate-layout --help`. Cambios previstos: añadir detección de las tres señales y un issue con remedio; impedir `Desk is healthy` mientras exista señal; hacer fallar `init` con el remedio; documentar el procedimiento; crear tests por señal y para repo migrado. Dependencias: tarea previa que saca salidas derivadas de `.sldb/runtime`; disponibilidad de `sldb`; desk de `deskops` ya migrado; entorno de tests con venv. Validaciones futuras: `pytest tests/test_doctor_alerts.py`, `pytest tests/test_gitignore_policy.py`, `deskops doctor --root .` y suite completa, comparando fallas en worktree limpio de `origin/main`.

## FUTURO

Otro nodo implementará y entregará los cambios. Un humano o coordinador decidirá migrar los 48 stores y avisar a las sesiones de cada repo. La revisión decidirá si acepta fallas preexistentes documentadas.
