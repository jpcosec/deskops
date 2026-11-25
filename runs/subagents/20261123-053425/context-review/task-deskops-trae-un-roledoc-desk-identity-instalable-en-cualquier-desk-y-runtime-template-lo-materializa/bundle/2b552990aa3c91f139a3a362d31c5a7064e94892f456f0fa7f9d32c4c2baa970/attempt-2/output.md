## REFORMULACION

Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, empaquetar un RoleDoc `desk-identity` como dato instalable (`deskops/data/roles/desk-identity.yaml`), hacer que `deskops desk update --apply` y `deskops init` lo instalen en `desk/roles/` sin pisar uno existente, y añadir `--mode identity` a `deskops runtime template` para escribir un `agents.md` de identidad persistente que nombre la raíz del desk y el proyecto scion, sin worktree ni instrucciones de ejecutor/tester/coordinador. Resultado observable: tests nuevos verdes, goldens actualizados y `init`/`update` dejando el rol instalado. Límites: no crear el agente en scion, no el hook, no tocar el repo scion, no el mapa de propiedad, no la traducción de tools a claude (dependencia).

## AMBIGUEDADES

1. «si ningun RoleDoc de desk/roles tiene name desk-identity» — no dice qué hacer si existe otro rol con `id: role-desk-identity` y otro `name`, ni si la comprobación es por `name`, `id` o ambos; obliga a inventar la clave de no-colisión.
2. «el dueno sale del registro de repos del desk» — no define formato ni campo del registro que identifica al dueño; obliga a inventar la consulta.
3. «el destino de lo sin dueno que declare el desk» — no indica dónde ni cómo se declara ese destino; obliga a inventar configuración.
4. «deskops add role por debajo» frente a «create_artifact("artifact.role", payload)» — no aclara si debe invocarse el CLI o la función interna; obliga a elegir implementación.

## DRY-RUN

Lecturas: TaskDoc, `pyproject.toml`, `desk.py`, `core.py`, `scion.py`, `runtime.py`, `registry.py`, tests y goldens citados, modelo RoleDoc y ruta de `add role`. Cambios previstos: nuevo YAML del rol; `package-data`; función compartida de instalación en `desk.py`; llamada desde `desk update` (lista en seco, instala con `--apply`) y desde `InitCLI` tras `seed_desk`; rama `identity` y `_render_identity_agents_md` en `scion.py`; `choices` en `registry.py`; dos tests nuevos; regeneración de tres goldens. Dependencias: tarea de traducción de tools; `deskops add role`/`create_artifact`; perfiles runtime. Validaciones futuras: los cuatro pytest del TaskDoc y una corrida de `runtime template ... --mode identity`.

## FUTURO

Otro nodo debe completar la dependencia de tools; un humano decide el formato del registro de dueños y del destino sin dueño, y aprueba el diff de goldens; el dispatcher aporta el worktree y el commit lleva `Task-Id`.
