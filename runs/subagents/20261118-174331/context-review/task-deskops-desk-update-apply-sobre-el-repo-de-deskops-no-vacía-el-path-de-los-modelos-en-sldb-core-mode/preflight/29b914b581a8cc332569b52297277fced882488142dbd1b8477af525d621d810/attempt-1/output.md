## REFORMULACION

Encargo de depuración en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: `deskops desk update --apply` vacía `path` en los 30 modelos de `.sldb/core/models/*.yaml`, y además toca `sldb/relation_types/has_model.md` y agrega `reltype-links_to`. El resultado exigido es que, en ese repo, el comando conserve la ruta local de cada modelo y no reescriba `sldb/relation_types/` ni agregue relation types no declarados por el store. Límites: reproducir en clon limpio en `/dev/shm`, localizar archivo y línea, añadir test que falle antes, corregir, actualizar CHANGELOG; no cambiar el layout de `.sldb`. Cierre: test nuevo verde, reproducción sin cambios en modelos y suite completa verde.

## AMBIGUEDADES

1. «con herramientas en 31460a48»: no aclara si ese es el commit a clonar; obliga a inventar la revisión base.
2. «la suite completa pasa (la corre integrate)»: no define si el ejecutor debe ejecutarla o solo el integrador; obliga a inventar el reparto.
3. «el informe lo dice con evidencia»: no indica formato, ruta ni destinatario del informe; obliga a inventar el entregable.
4. «un desk de prueba cuyos modelos tienen path local»: no especifica fixture, creación ni ubicación; obliga a inventar el arnés de test.
5. «conserve la ruta del store.yaml de deskops»: no identifica qué `store.yaml` es la fuente de verdad; obliga a inferir la ruta exacta.
6. «no reescribe sldb/relation_types/ ni agrega relation types que el store no declara» frente a «si lo que agrega […] es correcto […] en vez de revertirlo»: no resuelve si el arreglo debe impedir toda escritura o permitir las declaradas; obliga a inventar el criterio.

## DRY-RUN

Lecturas: TaskDoc, código de `desk update`, `.sldb/core/models/*.yaml`, `sldb/relation_types/`, tests de `test_desk_sync.py`. Cambios previstos: clonar en `/dev/shm`, ejecutar `desk update --apply`, `git diff -- .sldb/core/models sldb/relation_types`, rastrear la ruta de re-registro, añadir test de regresión, corregir, CHANGELOG. Dependencias: commit de deskops, CLI `deskops`, git, pytest. Validaciones futuras: test nuevo, diff de reproducción y suite completa. Nada ejecutado.

## FUTURO

El integrador ejecuta la suite completa y decide el commit; un humano valida si el cambio en `relation_types` es correcto o debe revertirse y aprueba el informe.
