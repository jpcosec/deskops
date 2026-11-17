# Sandbox de compatibilidad (punto 2 del brief)
Desks repo-a/b/c en /dev/shm/tester-bfb4-sbx, iniciados con `deskops init` sobre el código de HEAD (git archive en /dev/shm/tester-bfb4-head; el store tiene el contrato viejo de InboxNoteDoc, b163632f…). Después se operan con el código del checkout (PYTHONPATH).
- La nota vieja (enviada con HEAD) y la nueva (enviada con el checkout, que lleva `ack_reason: ''`) llegan bien al desk viejo.
- message read: la vieja da rc=0 (json ack_reason ''); la nueva da ack_reason ''.
- ack de la vieja con --reason "aviso leido" da rc=0, Tracked, y read la muestra con "Ack reason: aviso leido" justo después de acknowledged_at. El ack de la nueva sin --reason da rc=0, sin línea Ack reason.
- Desk viejo con nota vieja, antes de cualquier escritura del código nuevo (repo-c): `sldb stores check` (PYTHONPATH al checkout) da **PASS con 2 alertas** (store/contract-moved InboxNoteDoc + store/contract-mutation de la nota, "safe to run: sldb stores update"). `deskops doctor` dice "Desk is healthy, with 2 alert(s)", rc=0.
- La primera escritura tracked con el código nuevo (ack) reindexa el modelo: contract_hash pasa a 963ba769… y stores check queda PASS limpio. `sldb stores update --pythonpath <install>` también lo limpia.
- Al revés (código de HEAD leyendo una nota con ack_reason): read da rc=0 e incluye ack_reason.
- Caveat del sandbox: sldb sin PYTHONPATH importa el deskops instalado (viejo), así que da las mismas alertas. En producción la instalación es única y eso no pasa.
Conclusión: no bloquea. Cada desk ve alertas (no fallos) hasta su primer ack/send tracked o hasta correr `sldb stores update`. Recomendado: que el coordinador corra `sldb stores update` en cada desk registrado (o al menos en este repo) al desplegar la versión en herramientas/deskops.
