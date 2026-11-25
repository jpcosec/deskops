## REFORMULACION

Encargo de ejecución (task.code) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: hacer que `dispatch start` lea `DispatchRole.env_config` antes de lanzar y rechace el lanzamiento si el archivo no existe, no declara volumes, o ningún volume contiene `cfg.workspace`; debe imprimir `env_config <ruta> no declara un volume que contenga <workspace>` y salir con código ≠ 0, no reintentable por la cola. Además, `doctor` debe avisar lo mismo por cada rol de dispatch, y `docs/operator-manual.md` debe documentar que cada rol declara sus volumes y que el montaje global se retira tras decisión de JP. Límites: no editar el `settings.yaml` de scion, no reiniciar el server, no tocar env_config de `.bootstrap`, no tocar el piloto wf-desks. Orden: no corre antes de cerrar `task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale`.

## AMBIGUEDADES

1. «ninguno de sus volumes contiene cfg.workspace»: no define el esquema de `env_config` ni la semántica de contención (prefijo textual, límite de path, realpath, relativos). Obliga a inventar formato y comparación.
2. «sale con un código distinto de 0 (no reintentable por la cola)»: no fija el código ni cómo la cola distingue no reintentable. Obliga a inventar convención de exit codes.
3. «deskops doctor avisa lo mismo»: no fija severidad, formato ni si altera el exit code. Obliga a inventar contrato de alerta.
4. «el test de doctor que corresponda»: no nombra archivo; Validation cita `tests/test_doctor_alerts.py`. Obliga a decidir ubicación.
5. «los env_config de .bootstrap (son de la máquina)»: no aclara la raíz de `.bootstrap` ni sus rutas. Obliga a inventar resolución.
6. «con el desk/config.json real de deskops»: no indica ruta exacta. Obliga a asumir ubicación.

## DRY-RUN

Lecturas: `deskops/dispatch.py`, implementación de doctor, `docs/operator-manual.md`, `tests/test_dispatch.py`, `tests/test_doctor_alerts.py`, `desk/config.json`, env_config de `.bootstrap` y el TaskDoc dependiente. Cambios previstos: primero los tres tests de `start` con scion falso y el test de doctor; luego validación en dispatch antes de lanzar, alerta en doctor y sección en el manual. Dependencias: cierre previo de la tarea runtime-template; env_configs ya con volumes para `Done When`. Validaciones futuras: los dos pytest indicados, suite completa `-n 4`, `doctor --root .` sin aviso nuevo, y commit con trailer `Task-Id:`.

## FUTURO

JP decide retirar el montaje global; scion-coordination lo ejecuta en ventana. La tarea runtime-template produce los env_config con volumes. La cola interpreta el código de salida; el commit lo produce el ejecutor.
