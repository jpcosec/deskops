# Resultado
Added optional dispatch.quick_gates (DispatchConfig); dispatch start appends a "Gates rapidos del desk" section to executor (rc 0 before commit) and tester (rc != 0 => FALLA) prompt.md; unchanged without the field. Tests, operator-manual and CHANGELOG updated.
Files: deskops/config.py deskops/dispatch.py tests/test_dispatch.py docs/operator-manual.md CHANGELOG.md
Validation: see validation.log (tests/test_dispatch.py passes).
