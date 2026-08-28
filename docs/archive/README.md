# Superseded documents

Everything in this directory described a real decision at the time and is kept for the
record. **None of it describes the running system.** It was moved out of `docs/` on
27 Aug 2026 because a fresh session reading `docs/` should not be able to pick up a void
decision by accident.

| File | Superseded by | Why |
|---|---|---|
| `12-MODEL_PAIR.md` | `docs/22-MODEL_PAIR_OPENAI.md` | Gemini/Vertex pair; the provider changed 26 Aug |
| `15-VERTEX_GEMINI_CLIENT_PATCH.md` | nothing | Patches a Vertex code path that is no longer used |
| `19-HANDOFF_MARD_ON_FORK.md` | `docs/25-HANDOFF_MARD_ARM.md` | Written for the `replm` fork; the control library changed to `Zhang_RLM` |
| `20-HANDOFF_TRACK3_RERUN.md` | `docs/21`, then `docs/25` | Its job — diagnosing the first garbage run — is done and recorded in `docs/24` §7 |

Do not build against anything here. If you think you need it, read
`docs/00-START_HERE.md` first.
