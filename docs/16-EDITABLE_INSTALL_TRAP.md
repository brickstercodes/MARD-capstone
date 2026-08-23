# The editable-install trap

**Status:** Root cause found and fixed 22 Aug 2026 · Owner: Track 2 · **Read this
if `import rlm` or `import runlog` fails, or if a test that used to run starts
skipping.**

This lived in Track 2's personal working notes, which nobody else reads. It is an
environment fact about macOS rather than a Track 2 fact, it cost sixteen days
once, and it will do the same to anyone who keeps this repo in a synced folder —
so it belongs somewhere the whole team can find it.

Recorded because it cost sixteen days and will recur on any machine that does
the same thing.

`import rlm` died on **4 Aug** and nobody noticed until **20 Aug**.

**Root cause, found 20 Aug: iCloud Drive.** The repo lived in `~/Desktop`, and
"Desktop & Documents Folders" sync was on — `~/Library/Mobile Documents/com~apple~CloudDocs/Desktop`
is a symlink to it. The iCloud file provider flags every dot-file and
dot-directory it syncs as `hidden`, recursively, and **re-applies the flag as it
re-syncs** — it came back twice within minutes of being cleared. CPython 3.14's
`site.addpackage` **silently skips a hidden `.pth`**, and both editable installs
(`mard`, `rlms`) resolve through one. No warning, no error, exit code zero.

The evidence was unambiguous once the scope was checked: `.git`, `.venv`,
`.vendor` and `.gitignore` were all flagged, across four unrelated Desktop
projects — while `~/.zshrc` and `~/.ssh` were untouched. Home is not synced;
Desktop is.

It survived sixteen days because **`pytest` puts the repo root on `sys.path`**, so
every test passed and `./scripts/check.sh` stayed green while the install was dead
for anything run from another directory. Arav would have hit it on his first
script outside the repo root.

- **Fixed at the source** — the repo now lives at `~/dev/Capstonee`, outside the
  synced tree, with the inherited flags cleared and the venv rebuilt. A fresh
  venv comes out clean and `import rlm` works from `/` with no help.
- **Guard made honest** — `scripts/check.sh` probes with `env -u PYTHONPATH`. It
  already ran from `/` so cwd could not mask a dead install, but it inherited the
  `PYTHONPATH` that `.venv/bin/activate` exported, so it reported what the local
  crutch did rather than what a teammate's clone would do. That crutch is gone
  and is not needed.
- **Silent skip removed** — `tests/test_lm_builder.py` used `importorskip`, so a
  broken install turned the only test of the RLM seam into a skip inside a green
  suite. A vendored copy that is present but not importable now loads from the
  vendored tree and the test still runs; only a genuinely un-bootstrapped clone
  skips.

**If this recurs, check the folder before the machine.** Anything under `~/Desktop`
or `~/Documents` on a Mac with iCloud Drive sync will do this to `.venv` and
`.git` — and syncing `.git` risks worse than a broken import.

## The short version, for whoever hits this next

1. `ls -lO .venv/lib/python*/site-packages/__editable__*` — if they say `hidden`,
   this is your bug.
2. Check *where the repo lives* before you debug the machine. `~/Desktop` and
   `~/Documents` are synced by iCloud Drive on a default macOS setup;
   `ls -l ~/Library/Mobile\ Documents/com~apple~CloudDocs/` will show symlinks to
   them if sync is on.
3. Move the repo somewhere unsynced (`~/dev/...`), clear the flags with
   `chflags -R nohidden`, and rebuild the venv — it hardcodes absolute paths, so
   it cannot survive the move.
4. `./scripts/check.sh` verifies the repair: its import probe runs from `/` with
   `PYTHONPATH` cleared, so neither cwd nor a local crutch can mask a dead install.

**Syncing `.git` is the part to actually worry about.** A broken import is loud
once you know to look. iCloud evicting git objects to the cloud is not.
