REFORMULACION
Propósito: que `deskops doctor` detecte el layout viejo de `.sldb` y recomiende `sldb stores migrate-layout`; que `deskops init` falle ante ese layout; documentar el procedimiento por repo. Resultado: chequeo con tres señales, issue con remedio exacto, bloqueo de init, README/skill actualizados y tests. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no migrar otros repos, no avisar al ecosistema, no cambiar `sldb`; depende de la tarea que saca graph export/self-reflection de `.sldb/runtime`.

AMBIGUEDADES
1. Cita: “el .gitignore raiz tiene una linea que ignora .sldb/core o .sldb/runtime”. No define coincidencia exacta (`.sldb/core`, `/ .sldb/core/`, comodines, comentarios, excludes globales); obligaría a inventar el parser o el conjunto de patrones.
2. Cita: “lo reporta como issue”. No fija código, severidad ni formato del issue; obligaría a inventar el esquema si no se descubre en el código existente.
3. Cita: “deskops init sobre un repo con .sldb/ en layout viejo falla con el mismo remedio en el mensaje”. No precisa orden respecto de otras validaciones ni formato exacto del mensaje; obligaría a inventar ambos.

DRY-RUN
Lecturas: TaskDoc, `deskops/cli/commands/doctor.py` (zona 220-231 y construcción de findings), `deskops/bootstrap.py`, `README.md`, `.claude/skills/deskops-workflow/SKILL.md`, tests existentes y `sldb stores migrate-layout --help`. Cambios previstos: helper de detección de las tres señales; issue con `sldb stores migrate-layout --store <ruta>/.sldb`; guarda en init con salida distinta de 0; documentación; tests por señal, repo migrado e init. Dependencias: tarea previa ya integrada y comando `sldb` disponible. Validaciones futuras: los dos pytest indicados, `deskops doctor --root .`, suite completa y comparación de fallas en worktree limpio. Sin ejecutar nada.

FUTURO
Otro nodo ejecutor implementará y correrá las validaciones. La tarea dependiente debe entregar primero para que el propio desk no emita la señal `.sldb/runtime/`. Un humano o coordinador decidirá migrar los 48 repos y avisar a otras sesiones; también revisará el commit con `[skip ci]` y el push.
