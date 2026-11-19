---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-18T21:01:37'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# dispatch: el ejecutor y el tester no corren los gates estructurales del proyecto, y integrate es el primero en verlos

_Describe the incoming message with enough evidence to triage._

2026-11-18, tarea de undo_changes de sldb (389868dc): el ejecutor corrió tests/mcp y el tester los tests tocados, ambos PASA. El integrate automático falló en la suite por tests/test_clean_code_rules.py: undo_changes con 13 líneas de lógica (máx. 10) y batch_prevalidate.py con 85 líneas efectivas (máx. 80). El coordinador lo arregló a mano (73df19ec). En el sldb del 17-11 pasó lo mismo con stores_build (e7cc3761). Propuesta: que el desk declare en desk/config.json un comando de gates rápidos (en sldb, bash tools/check.sh --fast, que incluye código limpio y capas) y que el prompt de dispatch para executor y tester lo exija antes del commit y del veredicto. integrate sigue corriendo la suite completa.
