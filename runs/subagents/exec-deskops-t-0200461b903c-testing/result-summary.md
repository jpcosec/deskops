PASA

# Revisión de testing

Commit del ejecutor: `f32c12b213f58fb2e4697218f5546327fc22336f`
("review status: show incomplete for human-disposed receipts, technical_failure only for reason technical", Task-Id correcto).

Archivos del commit:
- `deskops/services/review.py`
- `docs/operator-manual.md`
- `tests/test_review_command.py`

## Verificación del cambio

- `_state_for_key` ahora reporta `incomplete` cuando hay recibos vigentes con `verdict: incomplete` y ninguno de ellos tiene `reason: technical`.
- Sigue reportando `technical_failure` para recibos `incomplete` con `reason: technical` (falla de transporte/cuota), incluido el caso mixto humano + técnico.
- `accepted`, `rejected`, `reviewed` (`pending`), `stale` y `missing` conservan su prioridad y comportamiento; los casos existentes del test parametrizado siguen pasando.
- La documentación (`docs/operator-manual.md`) actualiza la descripción de estados incluyendo `incomplete`. La ayuda del CLI no enumera los estados, por lo que no requería cambio de golden.

## Tests ejecutados

Entorno: el `.venv` del proyecto apunta a `/usr/bin/python3.12`, ausente en este host; se usó el intérprete 3.13 disponible en `/workspace/sldb/.venv` con el `PYTHONPATH` del proyecto. Mismos tests y fuentes del commit.

```
TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q tests/test_review_command.py
31 passed, 1 warning (Unknown config option: asyncio_default_fixture_loop_scope)
```

Tests adicionales de módulos de review:

```
TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q tests/test_review_doc.py tests/test_review_record.py
43 passed, 1 xfailed, 1 warning
```

No hubo fallas que requieran comparación contra un worktree limpio de `origin/main`.

## Observación

El caso con un recibo `incomplete` humano y otro `incomplete:technical` para la misma clave reporta `technical_failure`, tal como lo fija explícitamente el nuevo caso parametrizado; es coherente con reservar `technical_failure` para la corrida que falló por transporte o cuota.
