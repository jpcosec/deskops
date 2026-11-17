# Drawer Board

This board routes deferred work only.

## Remaining

Nada. Triaje del 2026-11-16: los 14 ítems sueltos se botaron (5 ya resueltos y 9 cubiertos por una tarea activa que los cita en from_drawer). Detalle en reports/triaje-deskops-20261116.md.


## Retired

The covered use-cases, stress-tests (the CI gap closed by task-test-ci-knowledge-integrity-flow, which added scripts/ci-knowledge-check.sh and tests/test_ci_integration.py), findings archive, answered questions, drawer rituals, attention review, and obsolete feature outlines were retired on 2026-10-19. The runtime-and-launcher feature and the tmux launcher task were retired the same day by the coordinator's decision: `deskops runtime supervise` plus the external harness (Herdr) cover what the tmux launcher would have done. Each retirement commit names the test or replacement that covers it, and git history is the durable record.

## Rule

Nothing in `desk/drawer/` executes. When an item is ready, author a full task with `deskops add task --from-drawer <item>` and remove the drawer item by hand once that task supersedes it; there is no drawer-to-task promotion.
