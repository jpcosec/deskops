## REFORMULACION
Encargo ejecutable `task.code` en `/mnt/ssd/proyectos/SLDB_1/deskops`: hacer portable el registro de repositorios. `deskops repo register` debe guardar en `path` una ruta relativa a la raíz del registro donde escribe; la lectura debe seguir aceptando entradas antiguas absolutas o con `~`. `deskops doctor` debe añadir, por cada entrada no resoluble, un hallazgo con id, path guardado y ruta resuelta, manteniendo el mensaje actual del store enlazado. Resultado esperado: cambios en `repo.py`, `doc_access.py` o resolución de rutas, `doctor.py` y tests; sin reescribir `~/setup` ni cambiar `RepositoryDoc`. No es agregado: es una tarea única con átomos.

## AMBIGUEDADES
1. “raiz del repo que contiene el registro” frente a “raiz_del_registro”: no queda claro si `relpath` se calcula desde la raíz del repo o desde el directorio que contiene el fichero de registro. Obligaría a inventar la base exacta.
2. “`deskops doctor` reporta […] por cada entrada del registro del desk” frente a “`~/setup/desk/registry`”: no se sabe si doctor cubre solo el registro del desk o también el del ecosistema. Obligaría a inventar el alcance.
3. “la ruta resuelta” para un path que no resuelve: no se define qué valor mostrar ni formato. Obligaría a inventar representación, severidad y texto del hallazgo.
4. “acepta leer entradas viejas con ruta absoluta o con `~`”: no especifica si aplica a todo path leído o solo a entradas del registro, ni dónde se expande `~`. Obligaría a inventar la política de resolución.
5. La validación incluye `tests/test_message_ecosystem_registry.py`, ausente en Scope: obligaría a inventar si ese test entra en el cambio.

## DRY-RUN
Lecturas: `repo.py`, `registered_repositories` en `doc_access.py`, `identity.resolve_registered_root`, `doctor.py` y los tests citados. Cambios previstos: calcular `os.path.relpath(destino, base_del_registro)` al registrar; conservar lectura absoluta/`~`; recorrer entradas en doctor y emitir hallazgo; añadir tests de ruta relativa, entrada absoluta inválida y entrada antigua válida. Dependencias: resolución existente, detección de la raíz del registro y sandbox de desk roots. Validaciones futuras: los pytest listados y suite completa, comparando fallas contra `origin/main`. Sin ejecutar nada.

## FUTURO
El dueño de `~/setup` reescribirá sus entradas con el CLI nuevo; un humano decidirá el formato exacto del hallazgo y aceptará fallas preexistentes; otro nodo ejecutará tests, commit e informe.
