REFORMULACION
Propósito: quitar de `README.md` y `docs/` las menciones a rutas y símbolos borrados en CC30 (`spec/artifacts`, `spec/fields`, `SpecRegistry`), remitiendo a atributos de clase de `deskops/models` o a `deskops/doc_access.py`. Resultado: grep de validación vacío y `tests/test_operator_manual.py` en verde. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo README.md y docs/; no reescribir ni migrar diagramas; solo ese test; el commit debe declarar que el `.mmd` se edita junto a su `.md` por no tener spec fuente. Es un nodo ejecutable (`task.docs`), no un agregado.

AMBIGUEDADES
1. «Solo se corre test_operator_manual.py» frente a «y los tests de docs»: obliga a inventar si hay otros tests.
2. «El .mmd ... se edita junto con su .md» frente a «No entra: reescribir los diagramas»: el grep exige tocar el `.mmd`, que contiene `spec/artifacts/*.yaml` y `spec/fields/*.yaml`. Habría que inventar si editar la etiqueta es «reescribir».
3. README: «`deskops/spec/fields/` may define artifact schema vocabulary». Ninguna regla de destino encaja; obliga a inventar si borrar, remitir a modelos o a doc_access.
4. Vocabulary: ejemplo «`spec:spec/artifacts/atom.yaml`» y kind `spec`. Es vocabulario, no mención operativa; obliga a inventar si eliminar el kind, cambiar solo el ejemplo o dejarlo.
5. «spec2viz se archiva, 80d32903» frente a la sección activa «Spec2viz Boundary» del README. No puedo verificar el hash; obliga a inventar si esa sección también cambia.
6. «README.md:90, ...:63, ...:63 y su .mmd:29»: sin números de línea en el input, obliga a inventar la correspondencia.
7. «atributos de clase de los modelos (deskops/models)»: el bundle no trae nombres; sin leer código habría que inventarlos.

DRY-RUN
Lecturas: README.md, vocabulary, diagrama `.md`/`.mmd`; luego `deskops/models` y `doc_access.py` para nombrar destinos. Cambios previstos: reescribir la frase de README sobre `spec/fields`; sustituir en vocabulary el ejemplo `spec/artifacts/...`; quitar del nodo `specs` del diagrama ambas rutas, conservando `deskops/spec/workflows/*.yaml`; commit con el mensaje exigido. Dependencias: checkout, `grep`, `../.venv/bin/python`, pytest, git. Validaciones futuras: grep exacto y pytest; sin ejecutar.

FUTURO
Un humano o nodo posterior debe verificar `80d32903` y el estado de spec2viz, decidir la política del `.mmd`, y ejecutar el commit/closeout.
