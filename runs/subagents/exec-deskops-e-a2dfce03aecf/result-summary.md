# Resultado
run_id: exec-deskops-e-a2dfce03aecf

dispatch start ya no responde ocupado por cualquier agente running: usa wait_reason (gate de memoria de la cola) y rechaza solo si la misma tarea/rol tiene un agente running (prefijo de scion_child_identity). Sin tope configurable. Exit 3 con 'ocupado: memoria ...' o 'ocupado: la tarea ya tiene agente <name>'.

Archivos: deskops/dispatch.py, tests/test_dispatch.py, docs/operator-manual.md, CHANGELOG.md
Tests nuevos: lanza con agente de otra tarea; rechaza misma tarea; rechaza por memoria. El fixture fija queue_min_available_gb=0 y queue_max_psi_avg60=1000 para no depender de la maquina.
Validacion: tests/test_dispatch.py 24 passed.
Revisar: session/session_sha256 no disponibles para este run.
