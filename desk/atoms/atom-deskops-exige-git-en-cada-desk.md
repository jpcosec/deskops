---
sldb:
  by: agent
  at: '2026-11-25T18:56:06Z'
  authority: generated
  via: create_document
id: atom-deskops-exige-git-en-cada-desk
title: deskops exige git en cada desk
five_wh_one_plus: where
tags:
- system:deskops
- system:sldb
- topic:architecture
provenance: desk/drawer/plans/deskops-plugin-de-sldb/decisiones.md
---

# deskops exige git en cada desk

## Answer

Decisión de JP del 25-11-2026: todo desk que usa deskops vive en un repositorio git. deskops y sldb pueden apoyarse en git para detectar cambios (git status, git diff --name-only), para el hash del texto (blob ids de git ls-files -s) y para la evidencia de cierre (commits con trailer Task-Id). No hace falta soportar evidencia de cierre sin git.
