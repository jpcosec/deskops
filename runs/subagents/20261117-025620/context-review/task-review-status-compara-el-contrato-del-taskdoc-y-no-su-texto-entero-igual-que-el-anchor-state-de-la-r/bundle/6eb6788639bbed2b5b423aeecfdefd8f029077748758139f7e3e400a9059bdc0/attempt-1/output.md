REFORMULACION
Nodo ejecutable `task.code` en el repo `deskops`. Propósito: que `deskops review status` marque `stale` solo cuando cambie el contrato del TaskDoc o las demás fuentes del input de revisión, no por cabecera `sldb`, tags, status, `current_node`, `history` o `references`. Resultado: un `contract_sha256` en `ReviewDoc`, comparación por contrato en `_state_for_key` y tests que cubran tags/status sin stale y goal con stale. Límites: no cambia `input.md`, ni el `input_sha256` registrado, ni las reglas de activación; en bundle, pills, átomos, rituales y archivos siguen entrando como hoy; recibos viejos sin campo comparan como hoy.

AMBIGUEDADES
1. “el digest es el contract_sha256 del TaskDoc que sldb calcula sobre __contract__ … se ubica con grep -rn contract_sha256 deskops ../sldb/src”: no precisa API, canonización ni si se reutiliza o reimplementa; obliga a inventar llamada y algoritmo.
2. “solo la parte del TaskDoc se reemplaza por su contract_sha256” junto a “No entra: cambiar input.md ni el input_sha256 registrado”: no define cómo combinar ese hash con las demás fuentes para el estado de bundle sin tocar la evidencia; obliga a inventar fórmula o proyección.
3. “TaskDoc.__contract__: title, goal, scope, implementation_path, files, validation, done_when”: no incluye el modelo TaskDoc ni confirma esos nombres; obliga a inventar el mapeo real.

DRY-RUN
Leer `review.py` 440-520 y 740-800, `models/review.py`, `tests/test_review_command.py`, y buscar `contract_sha256`/`__contract__` en `deskops` y `../sldb/src`. Cambios previstos: campo opcional `contract_sha256` en `ReviewDoc`; helper de digest de contrato; escribirlo al crear recibos; `_state_for_key` compara contrato para recibos nuevos y `input_sha256` para viejos; ajustar bundle; tests de tags/status accepted y goal stale. Dependencias: contrato real de TaskDoc y API sldb. Validaciones futuras: los tres comandos pytest indicados y comparación en worktree limpio de `origin/main`.

FUTURO
Un humano dispone veredictos y confirma fallas base; el equipo/sldb provee o valida la función `contract_sha256` si no existe; otro nodo/CI ejecutará la suite completa y el commit.
