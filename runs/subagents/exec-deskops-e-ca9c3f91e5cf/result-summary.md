# Intento 2
Commit en la rama deskops/deskops-e-ca9c3f91e5cf (sin trailer Task-Id).
- (a) tests/fixtures/model_contract_hashes.json: hashes nuevos de AtomDoc, PillDoc, TaskDoc y subtipos Task*Doc (heredan el campo). Se agregó también AtomAdrDoc, que faltaba en el snapshot desde main y el test lo exigía.
- (b) goldens regenerados con --update-golden. El diff agrega --pointers en la ayuda y "pointers" en las salidas; además trae deriva ya existente en main (atom.adr, materialize --adr, "phases"). update-golden borró 5 goldens .text sin relación; los restauré y no se tocan.
- (c) --pointers en add task (registry.py, parse_input.py) y test CLI.
- (d) pointers.py acepta tag:area:ui:graph y code:...::foo~2 / ::Clase.metodo~2; tests en test_where_pointers.py.
Validación: ver validation.log. Revisar: la deriva de goldens de (b).
