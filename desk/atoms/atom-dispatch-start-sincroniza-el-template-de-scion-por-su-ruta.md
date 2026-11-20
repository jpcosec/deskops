---
sldb:
  by: agent
  at: '2026-11-20T20:00:01Z'
  authority: generated
  via: create_document
id: atom-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta
title: dispatch start sincroniza el template de scion por su ruta
five_wh_one_plus: how
tags:
- system:deskops
- topic:dispatch
---

# dispatch start sincroniza el template de scion por su ruta

## Answer

deskops dispatch start llama a 'scion templates sync' con la ruta absoluta del directorio del template que acaba de escribir (dispatch.templates_dir/<rol>), no con su nombre. Así el sync funciona en un desk con su propio proyecto scion (IR/.scion), donde el nombre se buscaba en ese grove local y no se encontraba. scion start sigue tomando el template del hub del proyecto.
