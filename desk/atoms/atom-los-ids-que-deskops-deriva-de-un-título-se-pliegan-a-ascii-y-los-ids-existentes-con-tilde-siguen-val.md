---
sldb:
  by: agent
  at: '2026-11-18T21:26:36Z'
  authority: generated
  via: create_document
id: atom-los-ids-que-deskops-deriva-de-un-título-se-pliegan-a-ascii-y-los-ids-existentes-con-tilde-siguen-val
title: Los ids que deskops deriva de un título se pliegan a ASCII y los ids existentes
  con tilde siguen validando y resolviendo
five_wh_one_plus: how
tags:
- system:deskops
- topic:ids
---

# Los ids que deskops deriva de un título se pliegan a ASCII y los ids existentes con tilde siguen validando y resolviendo

## Answer

deskops.slugs.ascii_slug (NFKD sin marcas combinantes, después [a-z0-9]+ unidos por '-') es el único pliegue de ids nuevos derivados de un título (specs/compiler.py, doc_access.slugify, services/drawer.py), y cada llamador conserva su default y su largo máximo. Un id dado explícitamente se respeta tal cual. Los ids ya commiteados con tilde no se migran: la validación de la convención (models/atom.py:check_slug_id, para átomos y protoatoms) usa doc_access.slug_form, que acepta letras con acentos, así que siguen validando y 'deskops show' los resuelve por selector exacto. Toda llamada git cuya salida deskops parsea pasa -c core.quotepath=false (integrate._run, closure._git y _git_knows), porque sin eso git cita las rutas con tilde y la búsqueda falla, como le pasó a integrate el 2026-11-18.
