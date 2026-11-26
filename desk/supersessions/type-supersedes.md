---
sldb:
  by: agent
  at: '2026-11-26T02:59:54Z'
  authority: generated
  via: create_document
name: supersedes
direction: directed
cardinality: many_to_many
axis: PROVENANCE
source_types:
- AtomAdrDoc
target_types:
- AtomAdrDoc
condition: ''
---

# Supersedes

## Description

An accepted ADR replaces an earlier one. Attribute 'section' (optional): the earlier ADR is replaced only in that section and stays accepted. Written by `deskops add atom --atom-type atom.adr`.
