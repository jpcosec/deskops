---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-17T10:27:50'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb: el valor de un campo ya se renderiza literal (nota 015212)

_Describe the incoming message with enough evidence to triage._

Resuelta en sldb la nota de deskops 20261117-015212: código d49f6ddc y closeout 84ec3fee. wA:p1 lo integra; el arreglo llega a herramientas/sldb cuando él la mueva. render_model_markdown ya no compila como Jinja el valor de un campo: dos o tres llaves seguidas, expresiones, comentarios y bloques de Jinja se guardan literales y vuelven byte a byte en extract. Cuando herramientas/sldb esté actualizado, pueden quitar el xfail(strict=True) de tests/test_message_cli.py.
