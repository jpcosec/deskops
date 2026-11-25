## REFORMULACION

Propósito: impedir que el tester arranque contra `main` antes de que el commit del ejecutor esté integrado. Resultado: en `deskops/dispatch.py`, `start` con rol tester debe salir con `EXIT_BUSY` (3, para que la cola reintente) e imprimir `en espera: la rama deskops/<ejecutor> de la tarea no está integrada` si existe una rama `deskops/<nombre>` de un ejecutor de esa tarea (según `scion_child_identity`, intentos 1 y 2) con commits fuera de la rama principal; si no, debe lanzar. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Nodo ejecutable `task.code`, no agregado. Límites declarados: `deskops/dispatch.py` (start, rol tester), `tests/test_dispatch.py` y `CHANGELOG`; el input no fija fuera de alcance.

## AMBIGUEDADES

1. «por scion_child_identity, intentos 1 y 2»: no define estructura, fuente ni cómo mapear tarea→ramas; obligaría a inventar el esquema de identidad y nombres.
2. «Cuando el reap la integra y la borra, el tester lanza» frente a «con commits que no están en la rama principal»: ¿bloquea solo commits no integrados o también una rama integrada sin borrar? Obligaría a decidir esa condición.
3. «imprime 'en espera: la rama deskops/<ejecutor>...'»: ¿`<ejecutor>` se sustituye?, ¿qué mensaje si hay varias ramas? Obligaría a inventar formato y selección.
4. «Dentro: ... CHANGELOG»: no hay fuera de alcance; obligaría a inventar si se puede tocar reap/cola.
5. «la rama principal» / «main»: no fija si es literalmente `main` o la rama por defecto; obligaría a elegir.

## DRY-RUN

Lecturas: TaskDoc, `dispatch.py` (start y rol tester), `tests/test_dispatch.py`, `CHANGELOG`, utilidades de identidad/scion y git. Cambios previstos: test de regresión con repo git temporal (rama `deskops/<ejecutor>` con commit fuera de main ⇒ exit 3 y mensaje; sin rama ⇒ lanza), implementación en start tester, CHANGELOG y commit con `git commit -- <rutas>` y trailer `Task-Id`. Dependencias: `EXIT_BUSY`, `scion_child_identity`, git (`branch`/`merge-base`/`rev-list`) y cola que reintenta con 3. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`; comprobar que el test falla antes y pasa después. Sin ejecutar nada.

## FUTURO

El nodo de reap integra y borra la rama; la cola interpreta `EXIT_BUSY` y reintenta; un humano revisa el CHANGELOG/commit y el nodo de test/CI valida.
