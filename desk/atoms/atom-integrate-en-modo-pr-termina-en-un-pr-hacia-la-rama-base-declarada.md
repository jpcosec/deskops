---
sldb:
  by: agent
  at: '2026-11-23T01:55:24Z'
  authority: generated
  via: create_document
id: atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada
title: integrate en modo pr termina en un PR hacia la rama base declarada
five_wh_one_plus: how
tags:
- system:deskops
- topic:integrate
---

# integrate en modo pr termina en un PR hacia la rama base declarada

## Answer

IntegrateConfig.mode acepta push (por defecto) o pr. En modo pr, dispatch reap lleva los commits del ejecutor a task/<id> creada desde integrate.branch sin tocar la base; el closeout se commitea en esa rama; integrate corre memoria, suite, store y graph sobre la punta (sin fast-forward), empuja task/<id> y abre el PR con gh pr create --base <integrate.branch> --head task/<id>, o solo empuja si gh pr list ya encuentra uno. Probado con un remoto bare cuyo pre-receive rechaza refs/heads/dev y un gh falso.
