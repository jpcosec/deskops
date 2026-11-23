# Intento 2
Commit en rama deskops/deskops-e-2192f0386599-a2. Archivos: tests/test_command_registry.py (("queue","job") y ("queue","job","set") en MUTATING_COMMANDS; el registro marca el grupo como mutante), goldens help deskops_queue.txt, deskops_queue_job.txt, deskops_queue_job_set.txt, y scaffold init.json/update.json (hash de config.json con retry del reap).
--update-golden de help tocó además goldens ajenos (wrap por ancho de terminal) y los revertí.
Validación: ver validation.log. Suite completa: 1340 passed, 2 scaffold fallos corregidos y re-ejecutados (3 passed); no se re-corrió la suite entera tras eso.
