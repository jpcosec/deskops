# Intento 2 (corrige veredicto FALLA del tester)
Commit: acdce770 en rama deskops/deskops-e-85084b2b474c-a2.
Archivos: deskops/runtime/scion.py, deskops/dispatch.py, tests/test_scion_runtime.py, tests/test_dispatch.py.
1. image/kubernetes/telemetry en SCION_CONTEXT_OPTIONAL_KEYS (validadas por tipo) y pasadas tal cual a scion-env.yaml; test nuevo.
2. scion_start_argv: parametro `config`, --config justo despues de --workspace (test fija la posicion).
3. dispatch start pasa target/scion-env.yaml cuando existe (si no, role_cfg.env_config); tests de dispatch actualizados.
Validacion: 100 passed (test_scion_runtime + test_dispatch), ver validation.log. No se corrio la suite completa ni goldens (no tocados en este intento).
Revisar: el tester de dispatch ahora ve --config siempre que el contexto genere scion-env.yaml.
