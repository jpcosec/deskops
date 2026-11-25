## REFORMULACION

**Propósito:** que `deskops dispatch start` no lance un rol cuyo `env_config` no garantice el workspace, requisito para poder retirar el montaje global de SLDB_1 y /dev/shm que scion inyecta a todo agente claude.

**Resultado:** (1) `start` lee `DispatchRole.env_config`; si el archivo no existe, no declara volumes o ninguno cubre `cfg.workspace`, imprime «env_config <ruta> no declara un volume que contenga <workspace>» y sale con código ≠0 no reintentable; (2) `doctor` avisa lo mismo por rol de dispatch; (3) `docs/operator-manual.md` documenta que cada rol declara sus volumes y que el montaje global se retira por decisión de JP.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. Superficie: `deskops/dispatch.py`, `docs/operator-manual.md`, `tests/test_dispatch.py`, test de doctor.

**Límites:** no editar el `settings.yaml` de scion ni reiniciar el server (scion-coordination, con OK de JP); no tocar los `env_config` de `.bootstrap`; no tocar el piloto wf-desks. Orden: no corre antes de cerrar `task-runtime-template-…`.

## AMBIGUEDADES

1. «si el archivo no existe, no declara volumes, o ninguno de sus volumes contiene cfg.workspace» — no se define el esquema YAML de `volumes` (claves, cadenas `host:target` u objetos). Obligaría a inventar el parser.
2. «sale con un código distinto de 0 (no reintentable por la cola)» — no fija el número y ya existen 3–8. Obligaría a inventar el código.
3. «ninguno de sus volumes contiene cfg.workspace» — «contiene» ¿igualdad exacta o prefijo (workspace anidado en un mount mayor)? Obligaría a inventar la comparación.
4. «deskops doctor avisa lo mismo» — sin texto, severidad ni forma del alert. Obligaría a inventar mensaje y estructura.
5. «en la sección de despacho» de `operator-manual.md` — no identifica sección. Obligaría a inventar su ubicación.
6. «el test de doctor que corresponda» — no nombra archivo; la validación cita `tests/test_doctor_alerts.py`. Obligaría a decidir dónde escribirlo.

## DRY-RUN

Lecturas: `dispatch.py` (función `start`, justo antes de `scion_start_argv`), `config.py` (`DispatchRole`, `DispatchConfig.workspace`), el módulo de doctor, `operator-manual.md`, `tests/test_dispatch.py`, `tests/test_doctor_alerts.py`, y un `env.yaml` de `.bootstrap` como muestra de formato. Cambios previstos: helper que parsea volumes y comprueba cobertura de `cfg.workspace`; llamada en `start` con salida y código nuevos; alerta equivalente en doctor; párrafo en el manual; los tres tests p1 más el de doctor p2. Dependencias: `task-runtime-template-…` cerrada, `env_config` de `.bootstrap` ya con volumes, scion falso del fixture. Validaciones futuras: los tres comandos pytest del TaskDoc, más revisión de que `doctor --root .` no emite el aviso nuevo. No se ejecuta nada.

## FUTURO

Cierre de `task-runtime-template-…`; JP decide y autoriza retirar el montaje global; scion-coordination edita `settings.yaml` en ventana; revisión humana del commit con trailer `Task-Id`.
