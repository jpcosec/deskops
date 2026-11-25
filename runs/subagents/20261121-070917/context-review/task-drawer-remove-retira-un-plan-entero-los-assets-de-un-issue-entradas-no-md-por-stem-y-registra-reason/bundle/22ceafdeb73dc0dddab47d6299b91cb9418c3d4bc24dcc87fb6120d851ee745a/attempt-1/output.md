## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, ampliar `drawer remove` para (1) aceptar un directorio de plan bajo `desk/drawer/plans/` y retirarlo entero con su tracking y bullets del Board; (2) retirar assets de un issue si nadie más los referencia, y permitir que `retire` acepte un asset huérfano de issue inexistente; (3) resolver entradas `.yml/.yaml` por stem o fragmento; (4) aceptar `--reason` y `--ref` registrados como en `retire`. Debe preservarse el comportamiento actual, incluido el bloqueo por `from_drawer` sin `--force`.

Límites: tocar `services/drawer.py`, `services/retire.py`, `cli/registry.py`, golden de ayuda y tests nuevos. Fuera de alcance: `from_drawer` colgante.

## AMBIGUEDADES

1. “si nadie mas la referencia”: no define cómo detectar referencias. Obligaría a inventar el alcance del escaneo (grafo, Board, archivos, historial).
2. “con su tracking y sus bullets del Board del drawer”: no identifica estructura ni criterio de asociación. Obligaría a inventar el esquema y las claves para localizarlos.
3. “resuelve por stem o fragmento”: no fija precedencia entre coincidencia exacta, fragmento, `.md` y `.yml/.yaml`, ni qué hacer con múltiples candidatos. Obligaría a inventar reglas de desambiguación.
4. “igual que deskops retire”: no concreta formato, ubicación ni obligatoriedad de `reason`/`ref`. Obligaría a inventar el contrato si el código existente no lo determina.
5. Validación incluye “tests/test_inbox_promote_cli_gaps.py”, aparentemente ajeno a drawer/retire. Obligaría a inferir si los tests nuevos deben añadirse allí.

## DRY-RUN

Lecturas previstas: `drawer.py` (`resolve_drawer_source` ~52-80, `remove_entry` ~148), `retire.py` (`_DEDICATED_VERBS` ~19 y chequeo ~70-75), `cli/registry.py`, golden `deskops_drawer_remove.txt`, tests de drawer/retire y notas referenciadas.

Cambios previstos: extender resolución a directorios de plan y `.yml/.yaml`; retirar assets asociados; añadir `--reason`/`--ref`; ajustar `retire` para assets huérfanos; actualizar golden y añadir tests por cada conducta. Dependencias: esquema de tracking/Board, implementación existente de `reason/ref` en `retire` y generación de ayuda CLI.

Validaciones futuras: ejecutar los cuatro comandos del TaskDoc; ante fallos de suite completa, repetirlos en worktree limpio de `origin/main` y aceptar solo fallos equivalentes, listándolos en la entrega. No se ejecuta nada ahora.

## FUTURO

Otro nodo implementa y ejecuta pruebas; un humano decide las ambigüedades anteriores antes de fijar contrato y aceptación.
