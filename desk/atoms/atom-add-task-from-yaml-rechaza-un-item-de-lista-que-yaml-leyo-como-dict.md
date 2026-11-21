---
sldb:
  by: agent
  at: '2026-11-21T18:34:20Z'
  authority: generated
  via: create_document
id: atom-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict
title: add task --from-yaml rechaza un ítem de lista que YAML leyó como dict
five_wh_one_plus: how
tags:
- system:deskops
- topic:cli
---

# add task --from-yaml rechaza un ítem de lista que YAML leyó como dict

## Answer

deskops add task --from-yaml rechaza, igual que edit task, un ítem de una lista de strings que YAML leyó como dict (por ejemplo una línea con ': ' sin comillas), con un error que nombra el campo y el ítem, en vez de guardar el dict.
