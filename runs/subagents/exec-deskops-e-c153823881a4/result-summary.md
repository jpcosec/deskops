# Resultado del ejecutor deskops-e-c153823881a4

Tarea: task-closeout-verify-no-trata-como-artefacto-generado-un-golden-json-que-tiene-un-golden-yaml-hermano-baj

## Cambios
- `deskops/services/closure.py` (`_generated_artifact_source_finding`): retorno temprano `None` cuando `relative_path.split("/")[:2] == ["tests", "fixtures"]` (precisión 2 del coordinador). Cubre tests/fixtures/ y todos sus subdirectorios; fuera de ahí la regla queda igual.
- `tests/test_closeout_declared_evidence.py`: helper `_generated_artifact_findings` (escribe el par, commitea, declara una task.code en el sandbox `repo`/tmp_path y corre `closeout verify`) y dos casos nuevos:
  - `test_golden_json_with_a_yaml_sibling_under_tests_fixtures_is_not_a_generated_artifact` (par message_ack.json/.yaml bajo tests/fixtures/golden/output/ → sin hallazgo).
  - `test_markdown_with_a_yaml_sibling_outside_tests_fixtures_is_still_a_generated_artifact` (docs/diagrams/flow.md + flow.yaml → hallazgo en flow.md).

## Validación (validation.log)
- tests/test_closeout_declared_evidence.py: 27 passed, rc=0.
- tests/test_closeout.py: 73 passed, rc=0.
- Control: sin el cambio, el test del golden falla y el del .md pasa → los tests discriminan.
- Caso real: en una copia del repo en /dev/shm, `closeout verify` de la tarea de ack --reason (97649c61) da ok=True y findings=[]; ya no aparece generated_artifact_missing_declared_sources.
- Suite completa: no corrida (para el integrador, por orden del brief).

## Riesgos
- Bajo: cualquier .md/.json realmente generado que alguien ponga bajo tests/fixtures/ ya no se exige con source_atoms/provenance; es el alcance pedido.
