---
sldb:
  by: agent
  at: '2026-11-20T02:10:20Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: hbc_latina
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-19T23:09:58'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# guiar a los repos que usan deskops a migrar el layout de .sldb (sldb stores migrate-layout)

_Describe the incoming message with enough evidence to triage._

Desde el 2026-11-04 (sldb c420809c) `.sldb/` se versiona entero y el caché vive en `.sldb_cache/`, que va ignorado. Los repos que hicieron `deskops init` antes de esa fecha siguen con el layout viejo y nada les avisa:
- tienen `.sldb/runtime/` en disco;
- su `.gitignore` ignora `.sldb/runtime/` y a veces `.sldb/core/`, así que el store puede no estar en git.

Escaneo local del 2026-11-19: 48 stores con `.sldb/runtime/` en `~/AntonIA`, `~/proyectos` y `~/setup`.
- Seis de ellos además conservan la línea vieja en el `.gitignore`: setup, plantilla_cliente, antonia-teva-portal, antonia_gateway, sldb-ui y marcado.
- `heyantonia/plantilla_cliente` la hereda a cada repo de cliente que genera (su commit 37a4be9 agrega `.sldb/runtime/` al `.gitignore`).

La migración existe y es idempotente: `sldb stores migrate-layout [--store <ruta>] [--force]`. Mueve `.sldb/runtime/` a `.sldb_cache/`, borra el journal sin archivarlo, quita las líneas `.sldb/core/` y `.sldb/runtime/` del `.gitignore` raíz y agrega `.sldb_cache/`. Lo que falta es que deskops lleve a cada repo a correrla.

Propuesta:
1. **`deskops doctor`** detecta el layout viejo y lo reporta como issue con el remedio exacto. El layout viejo es cualquiera de estas tres señales:
   - existe `.sldb/runtime/`;
   - existe `.sldb/journal`;
   - el `.gitignore` raíz tiene una línea que ignora `.sldb/core` o `.sldb/runtime`.
   El remedio es `sldb stores migrate-layout --store <repo>/.sldb`. Mientras el repo no migre, doctor no dice «Desk is healthy».
2. **`deskops init`** sobre un repo que ya tiene `.sldb/` corre la migración, o falla diciendo que hay que correrla.
3. **El procedimiento en el README y en la skill `deskops-workflow`**, como pasos para cada repo:
   1. Ponerse al día con la rama de integración.
   2. Correr `sldb stores migrate-layout`.
   3. Correr `git status`. Si `.sldb/core/` antes estaba ignorado, aparece como nuevo y hay que agregarlo.
   4. Correr `git add .gitignore .sldb`, nunca `git add -A`.
   5. Correr `deskops doctor`.
   6. Hacer commit con `[skip ci]` y push.
   7. Avisar a las otras sesiones del repo. El commit toca `.sldb/` entero y choca con cualquier rebase en curso.
4. **Un aviso al ecosistema**: un `deskops message send` a cada repo registrado que tenga el layout viejo, para que lo migre la sesión que trabaja en él y no una sesión ajena.

Origen: lo vi al inicializar hbc_latina. Copié el `.gitignore` de plantilla_cliente, y con eso el layout viejo reapareció en un repo nuevo.
