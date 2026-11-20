---
sldb:
  by: agent
  at: '2026-11-20T02:24:07Z'
  authority: generated
  via: create_document
id: atom-los-rituales-context-review-y-phase-describen-la-revision-de-contexto-con-deskops-review-y-la-regla
title: Los rituales context-review y phase describen la revisión de contexto con deskops
  review y la regla de activación como gate
five_wh_one_plus: how
tags:
- system:deskops
- topic:rituals
---

# Los rituales context-review y phase describen la revisión de contexto con deskops review y la regla de activación como gate

## Answer

La revisión de contexto de una tarea se hace con deskops review preflight y deskops review bundle (pi, perfil por defecto del runtime), deja su recibo en desk/reviews/<tarea>/ y se dispone con deskops review dispose. La regla rule-activation-<tipo> es el gate que deja pasar una tarea a ejecución: pide recibos preflight y bundle aceptados e intactos (y de reproducción en task.debug). Así lo describen los rituales ritual-context-review y ritual-phase.
