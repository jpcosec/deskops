---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: scion
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T23:20:23'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# runtime template: scion ignora resources y volumes del template; van como --config del agente

_Describe the incoming message with enough evidence to triage._

Piloto scion en IR, fase 1 (reports/scion-piloto-ir-20261115.md, 'Fase 1: preparación'). En el fork f6e623c6 image, resources, volumes, kubernetes y telemetry son claves de entorno: scion las ignora en scion-agent.yaml (docs-site reference/settings-precedence.md). Lo que --context-file escribe como resources.limits (memory_limit, cpu_limit) y volumes (workspace con la misma ruta, shared_paths) no llega al contenedor: la prueba de humo dio memory.max=max, sin /dev/shm del host y sin /mnt/ssd/proyectos/SLDB_1, mientras DESKOPS_* y PYTHONPATH apuntan ahí. env sí llega (TMPDIR=/dev/shm). Con 'scion start --config <archivo>' (image, resources, volumes) sí se aplica (6Gi, 2 CPU, ambos montajes). Propuesta: que 'deskops runtime template' escriba esas claves en un archivo aparte (p. ej. scion-env.yaml) y no en el template, y que scion_start_argv y el agents.md del coordinador pasen '--config <ese archivo>'. Además, el agents.md del coordinador fija 'role-deskops-executor'/'role-deskops-tester' y '--type deskops-executor'/'deskops-tester': en el desk de IR el ejecutor es 'ir-executor'; el tipo del hijo debería salir del contexto o de un flag.
