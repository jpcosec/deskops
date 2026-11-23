---
sldb:
  by: agent
  at: '2026-11-23T13:16:20Z'
  authority: generated
  via: create_document
id: atom-runtime-template-de-scion-escribe-image-resources-volumes-kubernetes-y-telemetry-en-scion-env-yaml-y
title: runtime-template de scion escribe image, resources, volumes, kubernetes y telemetry
  en scion-env.yaml y el tipo del hijo sale del rol
five_wh_one_plus: how
tags:
- system:deskops
- topic:runtime
---

# runtime-template de scion escribe image, resources, volumes, kubernetes y telemetry en scion-env.yaml y el tipo del hijo sale del rol

## Answer

runtime template materializa scion-env.yaml junto a scion-agent.yaml con image, resources, volumes, kubernetes y telemetry; scion_start_argv agrega --config RUTA justo despues de --workspace; dispatch start pasa el scion-env.yaml del template; --executor-role y --tester-role configuran los roles de los hijos y el --type sale sin el prefijo role-.
