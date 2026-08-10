# DRAFT — chase comment for #11, to Arav

**Not sent.** Post to
[#11](https://github.com/brickstercodes/MARD-capstone/issues/11) after review.

Two days late — the chase was planned for Thu 6 Aug. Kept short and made it easy
to answer with one word, because a five-day silence usually means the ask was too
big, not that it was ignored.

---

@FalseAdvertising — following up on the handoff from 3 Aug. W0 closes tomorrow
and this is the last box on #11 that is neither mine nor Anugrah's, so I want to
make it as small as possible to close.

**If the harness looks fine, just say "signed off" and I will tick the box.** You
can find the gaps in W1 and I will fix them then — that is much cheaper than you
reading 129 lines of handoff doc today.

If you would rather sanity-check one thing first, make it this: **do the token
counts `runlog` records match what your provider reports for the same call?**
Everything in both manuscripts is downstream of that number being right. The
other checks in the doc can wait.

The one thing I genuinely cannot defer past this week:

> **What identifies a run for you?** `params` is a free-form dict right now. If
> depth, chunk size or top-k need to be first-class fields so your W4/W7 tables
> can group on them, changing that is cheap today and expensive after **Feature
> freeze A on Sun 23 Aug**.

A one-line answer — "params is fine" or "make depth and top-k first-class" — is
enough.

Two things from my side since the handoff, both relevant to you:

- **`scripts/check.sh` now verifies the editable installs import from outside the
  repo root.** Mine silently broke for four days while the full test suite stayed
  green, because pytest puts the repo root on `sys.path` and masked it. If you
  cloned before today, pull — you would have hit it on your first script run from
  another directory.
- **`docs/RLM_BASELINE_SURVEY.md`** classifies all 14 RLM examples by what they
  need. Two of them run with **no API key at all** using a local `MockLM`, which
  may be useful for your W1 scorer work before keys land.

If nothing has come back by tomorrow I will raise it at the Friday gate — not as
an escalation, just so it stops sitting silently on a `blocker` box.
