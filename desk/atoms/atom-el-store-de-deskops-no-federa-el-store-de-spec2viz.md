---
sldb:
  by: agent
  at: '2026-11-16T20:38:10Z'
  authority: generated
  via: create_document
id: atom-el-store-de-deskops-no-federa-el-store-de-spec2viz
title: El store de deskops no federa el store de spec2viz
five_wh_one_plus: what
tags:
- system:deskops
- topic:sldb-store
provenance: desk/inbox/20261116-130201-suggestion-g5-opci-n-b-decisi-n-de-jp-deskops-quita-su-enlace-al-store-de-spec2viz-ir-espera-con-un-espejo.md
---

# El store de deskops no federa el store de spec2viz

## Answer

Decision de JP 2026-11-16 (G5, opcion b): el .sldb de deskops no declara ni indexa un enlace al store de spec2viz (../spec2viz/.sldb), porque G5 archiva ese store con su repo y una sesion sldb que federa el store de deskops no debe leer el store real de spec2viz. Los enlaces federados de deskops son sldb, pron y scion. Para quitar un enlace se usa sldb stores remove <nombre> seguido de sldb stores declare --write, asi la declaracion de store.yaml y el indice store_index.yaml quedan de acuerdo.
