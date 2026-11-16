REFORMULACION

Encargo ejecutable de código en el repo `deskops`: hacer que `deskops closeout verify --task <id> --run-dir <dir>` acepte `--run-dir` opcional y, cuando se aporte, devuelva `ok:false` si falta algún archivo de `REQUIRED_EVIDENCE`, usando el mismo texto que `closeout commit`. Resultado: un helper compartido `missing_run_evidence(run_dir)`, commit sin cambio de comportamiento, verify capaz de anticipar el fallo de commit, golden de ayuda actualizado y tests. Límites: no cambiar la evidencia exigida por commit ni el formato JSON fuera del nuevo hallazgo; los números de línea son orientativos; los tests usan un desk temporal. No es un agregado: es una tarea de implementación.

AMBIGUEDADES

1. “reporta como falla (ok:false) cada archivo de REQUIRED_EVIDENCE que falte” frente a “con el mismo texto que usa commit”: no aclara si se emite un hallazgo por archivo o uno agregado. Obligaría a inventar la estructura de hallazgos.
2. “Missing required evidence in <run_dir>: <archivos separados por coma>”: no fija orden, deduplicación ni separador exacto de archivos. Obligaría a inventar el orden y formato preciso.
3. “cuando se da, reporta como falla”: no define qué ocurre si `--run-dir` no existe o no es directorio. Obligaría a inventar si cuenta como todos los archivos faltantes u otro error.
4. “el formato del reporte JSON fuera del nuevo hallazgo”: no define claves, severidad ni ubicación del nuevo hallazgo. Obligaría a inventar su esquema.
5. “verify se comporta igual que hoy” sin `--run-dir`: no explicita si también debe conservarse literalmente el código de salida y el JSON actual. Obligaría a inventar el alcance de “igual”.

DRY-RUN

Lecturas previstas: TaskDoc, pill de evidencia, `closeout.py`, `closure.py`, golden de ayuda y tests citados. Cambios: extraer helper, reutilizarlo en commit y verify, añadir `--run-dir` al parser, actualizar golden y añadir casos de test. Dependencias: `REQUIRED_EVIDENCE`, texto actual de commit y entorno pytest indicado. Validaciones futuras: ejecutar los pytest listados y comparar fallas en worktree limpio de `origin/main`.

FUTURO

Otro ejecutor implementará y ejecutará pruebas; un humano o nodo de cierre decidirá la aceptación, incluida la lista de fallas preexistentes.
