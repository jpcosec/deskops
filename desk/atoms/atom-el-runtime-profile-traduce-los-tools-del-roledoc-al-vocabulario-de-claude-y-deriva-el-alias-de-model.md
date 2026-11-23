---
sldb:
  by: agent
  at: '2026-11-23T09:08:58Z'
  authority: generated
  via: create_document
id: atom-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-deriva-el-alias-de-model
title: El runtime-profile traduce los tools del RoleDoc al vocabulario de Claude y
  deriva el alias de modelo
five_wh_one_plus: how
tags:
- system:deskops
- topic:runtime
---

# El runtime-profile traduce los tools del RoleDoc al vocabulario de Claude y deriva el alias de modelo

## Answer

build_agent_spec_args traduce los tools del RoleDoc a nombres de Claude (read->Read, grep->Grep, find/ls->Glob, bash->Bash, edit->Edit, write->Write) solo para harness claude, sin duplicados y con error ante un tool sin traduccion; model_alias_for deriva large/medium/small de opus/sonnet/haiku y cae a medium con comentario en scion-agent.yaml.
