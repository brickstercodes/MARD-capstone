# The RLM base library: what runs, and what it already does

> ### ⚠️ §1 AND §3 SUPERSEDED, §2 STANDS WITH A CAVEAT — 26 Aug 2026
>
> This document surveys **`alexzhang13/rlm`** (the base paper's own library, vendored at
> `.vendor/rlm` @ `caf0bff`, MIT — see the two corrections below). The vanilla RLM control
> currently runs on a **different
> library** — `replm`, MIT, from Track 3's fork pinned at `a0ca553`. See
> [`18-PROVIDER_MIGRATION.md`](18-PROVIDER_MIGRATION.md) §4.
>
> - **§1 (the 14 examples) and §3 (still blocked) describe a library that is no longer the
>   control.** Superseded.
> - **§2 stands, and §2.2 holds more cleanly than it did.** Verified first-hand in
>   `replm`: the inner orchestrator is constructed with `query=prompt, context=prompt` and
>   a shared budget and **nothing else** — no parent findings, no skeleton, no directive.
>   The upward/observational vs downward/operative distinction is sharper there.
> - **§2.3's `root_prompt` trap does not exist in `replm`** — there is no user-injectable
>   downward slot. It remains valid *as a point about the base paper's reference
>   implementation* and still belongs in related work, but its file-and-line citations must
>   be labelled as citations of `alexzhang13/rlm`, **not** of the system we ran.
> - **§2.5's argument for `runlog` is untouched** and if anything stronger — `replm`'s
>   response object has no notion of a seed, system, document or budget either.
>
> **Open, and Track 1's to answer:** whether the control *should* be `replm` or the RLM
> authors' own library. A reviewer will ask. `18` §7 item 2.

**Owner:** Track 2 (Parth Sangani, @parthparu) · **Serves:** the *"RLM examples run
end-to-end"* box on [#11](https://github.com/brickstercodes/MARD-capstone/issues/11),
and CONTEXT.md §1.2

Vendored at `.vendor/rlm`, installed as `rlms==0.1.3`.
Upstream: `github.com/alexzhang13/rlm`, **MIT**.

> **Two corrections, 26 Aug 2026, both verified first-hand.**
> **(a) The licence is MIT, not CC BY 4.0.** `LICENSE` reads *"MIT License, Copyright
> (c) 2026 Alex Zhang"*, `pyproject.toml` declares `license = "MIT"`, and no "CC BY" or
> "Creative Commons" string exists anywhere in the repository. The W9 attribution was
> about to be wrong.
> **(b) The vendored copy is at `caf0bff`** (8 Aug 2026), not `72d6940` (25 Jun).
> Upstream is further ahead again at `854e688` (25 Aug). Whatever is measured must be
> re-pinned and recorded by its real SHA.

Two parts. §1 is operational — which of the 14 examples can actually be run and
what each needs. §2 is the one CONTEXT.md §1.2 demands and is the more important
of the two: **the base library already ships something depth-and-metadata
shaped**, and the contribution has to be distinguishable from it. It is, but not
for the reason you would guess from the name, and the distinction needs to be
made in the paper before a reviewer makes it for us.

---

## 1. The 14 examples

### 1.1 What each one needs

| Example | Credential | Runtime | Runnable now |
|---|---|---|---|
| `quickstart.py` | `OPENAI_API_KEY` | local REPL | ✗ keys |
| `logger_example.py` | `PORTKEY_API_KEY` | local REPL | ✗ keys |
| `depth_metadata_example.py` | `PORTKEY_API_KEY` | local REPL | ✗ keys |
| `rlm_query_batched_example.py` | `PORTKEY_API_KEY` | local REPL | ✗ keys |
| `custom_tools_example.py` | `OPENAI_API_KEY` + `PORTKEY_API_KEY` | local REPL | ✗ keys |
| `compaction_example.py` | `PORTKEY_API_KEY` | local REPL | ✗ keys |
| `compaction_history_retrieval_example.py` | `PORTKEY_API_KEY` | local REPL | ✗ keys |
| `lm_in_repl.py` | `PORTKEY_API_KEY` | local REPL + socket | ✗ keys |
| `e2b_repl_example.py` | `OPENAI_API_KEY` | E2B cloud sandbox | ✗ keys + account |
| `prime_repl_example.py` | `OPENAI_API_KEY` | Prime Intellect sandbox | ✗ keys + account |
| `lm_in_prime_repl.py` | `PORTKEY_API_KEY` | Prime Intellect sandbox | ✗ keys + account |
| `daytona_repl_example.py` | `DAYTONA_API_KEY` | Daytona sandbox | ✗ keys + account |
| `modal_repl_example.py` | **none** — uses a `MockLM` | Modal account | ✗ Modal account |
| `docker_repl_example.py` | **none** — uses a `MockLM` | Docker daemon | ✗ Docker not running |

**Blocked, not broken** — as #11 already records. Nothing here indicates a defect
in the library.

### 1.2 The useful finding: the `MockLM` pattern, not the two examples

`docker_repl_example.py` and `modal_repl_example.py` both define a local `MockLM`
subclassing `rlm.clients.base_lm.BaseLM`, returning a canned string and a
hand-built `UsageSummary`. They exercise the full REPL execution path — code
blocks, `llm_query`, recursive `rlm_query`, custom tools — with **no provider
call anywhere**.

**The pattern is the finding; the two examples are not.** Both of them wire
`MockLM` to a container runtime — Docker or Modal — and neither runtime is used
by this project. MARD runs on the **local** REPL (§1.3), Docker is not in
CONTEXT.md §4.1's tech stack, and running the Docker example would only prove
that an execution environment we do not use works.

`MockLM` is not environment-specific. Pointed at `LocalREPL` it gives the same
evidence with no daemon, no image pull and no container. Verified on 8 Aug 2026:

```
[1] bare code execution        locals: {'x': 3}   stdout: 6
[2] llm_query via LMHandler    response: Mock: Hello!   batched: 2
[3] recursive rlm_query        stdout: child-answer(explore section 3)
```

`LMHandler(client=MockLM())` + `LocalREPL(lm_handler_address=...)` for the query
path, and `LocalREPL(subcall_fn=...)` for the recursive path.

What this buys Track 2, which is more than the checkbox: the orchestrator's
fork-join, retry, failure-isolation and provenance plumbing (W2, #13) can be
developed and tested against `MockLM` with **zero API spend and zero rate-limit
exposure**, and W1's stub Tier 2 builder (#12) never needs a key to prove the
plan contract holds. Deterministic, free, and fast enough for CI — which matters
most in W3 and W6, when the real thing is expensive and rate-limited.

### 1.3 Recommended order once keys land

Per #11, and unchanged: `quickstart.py` → `logger_example.py` →
`depth_metadata_example.py`. The first proves the install, the second proves
trajectory capture, the third is §2's subject matter.

**Five of the fourteen are off the critical path.** The four sandbox examples
(E2B, Prime, Daytona, Modal) each need a separate third-party account, and
`docker_repl_example.py` needs a Docker daemon. All five exercise **remote or
containerised execution environments that MARD does not use** — the local REPL is
what MARD runs on. Skip them unless W5 concurrency work turns out to need remote
execution, and note that if it ever does, that is a change to the tech stack in
CONTEXT.md §4.1 and belongs in a decision, not in a dependency that arrived by
accident.

---

## 2. What the base library already does — and where MARD begins

CONTEXT.md §1.2: *"Say this before someone else does, or the architecture reads as
a restatement of the base paper."* §1.2 makes that point about the
frontier-root/cheap-worker split. Reading the source, **there is a second and
sharper version of the same hazard**, and it lands directly on the word
"metadata" in MARD's own name.

### 2.1 The library ships a great deal of what sounds like our contribution

First-hand from `.vendor/rlm/rlm/core/types.py`:

| Type | Carries |
|---|---|
| `RLMMetadata` | `root_model`, `max_depth`, `max_iterations`, `backend`, `backend_kwargs`, `environment_type`, `environment_kwargs` |
| `RLMChatCompletion.metadata` | the full trajectory — iterations → code blocks → `REPLResult` → nested `llm_calls` / `rlm_calls`, each child carrying **its own** metadata, recursively |
| `UsageSummary` / `ModelUsageSummary` | per-model `total_calls`, input/output tokens, `total_cost` |
| `QueryMetadata` | `context_lengths`, `context_total_length`, `context_type` |
| `RLMLogger` | captures the above in memory; optional JSONL to disk |

And `depth_metadata_example.py` exists specifically to demonstrate metadata
captured at every depth level and flowing back up the recursion tree.

A reviewer who reads that example and then reads "Metadata-Augmented Recursive
Decomposition" will reasonably ask what we added.

### 2.2 The answer: direction of flow

The distinction is clean, and it is checkable in the source rather than a matter
of framing.

**In the base library, metadata flows *upward* and is *observational*.** It is a
record of what happened, assembled for inspection and logging after the fact. It
never re-enters a prompt and never influences a child call. When a parent RLM
spawns a child (`rlm/core/rlm.py:807–836`), the child is constructed with:

- `logger=RLMLogger() if self.logger else None` — a **fresh, empty** logger
  (`rlm.py:824`). The parent's accumulated trajectory is explicitly not passed
  down. The library's own comment says why: *"Give child its own logger so its
  trajectory is captured in metadata"* — capture, not inform.
- `child.completion(prompt, root_prompt=None)` (`rlm.py:836`) — the child
  receives **only the prompt string** the parent's REPL code passed to
  `rlm_query()`. Nothing else.

**In MARD, the envelope flows *downward* and is *operative*.** Skeleton,
accumulated findings and parent directive are injected into the child's context
*before* it runs, changing what the child can see and therefore what it does.
That is the entire claim in CONTEXT.md §1.1 — exploration that *confirms a
hypothesis* instead of *discovering blindly*.

So: same word, opposite direction, and only one of them changes the model's
behaviour. That sentence belongs in the paper.

### 2.3 The trap inside the answer

There is a `root_prompt` parameter (`rlm.py:303`, documented at `rlm.py:337`)
which does exactly what it sounds like — lets the root LM see a small
user-specified prompt alongside the context. Children are passed
`root_prompt=None`.

So the library **has a downward-injection slot and deliberately declines to use
it for children.** Expect precisely this objection: *"you just used
`root_prompt`."*

The rebuttal has to be about what fills the slot, not the slot's existence.
`root_prompt` is designed for a **fixed, small, user-authored string** — the
example given in the docstring is the user's original question. The envelope is
**accumulated state that grows across calls**: a structural skeleton extracted in
Pass 0, findings compounded from every prior call, and a parent-issued directive
specific to *this* child. Nothing in the library constructs, propagates or
compounds that; there is no mechanism that carries one child's findings to the
next.

Worth stating plainly, because it is also the honest version: the base library
gives us a *place to put* the envelope. What is ours is the envelope — what goes
in it, how it accumulates across the pass structure, and the typed Master Plan
that makes Tier 2 dispatch structure-aware rather than section-blind.

### 2.4 Consequence for O1

O1 is *"formalise MARD — define the metadata envelope and its pass structure."*
The formalisation should open by naming what the base library already provides
and drawing the upward/downward line explicitly, before defining the envelope.
Written that way it reads as precision. Written the other way — envelope first,
distinction buried in related work — it reads as an omission a reviewer caught.

**For Track 1 (@brickstercodes):** §2.2 and §2.3 are paper content, not
implementation notes, and they belong in §3 rather than related work. The
citations are file-and-line into the pinned vendored copy, so they are checkable.

### 2.5 Why `runlog/` still earns its place

Related question, since `RLMLogger` already writes JSONL trajectories with token
counts and cost, and CLAUDE.md's rule 1 says code that isn't serving the
manuscripts is a net loss.

`RLMLogger` captures **one completion**. `runlog` captures **a campaign**: run
identity (system × document × seed), config snapshot with git SHA and dirty flag,
package versions and platform, rate provenance that refuses to quote a stale
price, a spend ledger across runs, and crash-survivable partial output.
`RLMLogger` has no notion of a seed, a system, a document or a budget, because it
was never meant to.

The decisive argument is simpler, though: **four of the five systems in the
matrix never touch the RLM library at all.** Full-context, naive chunking and
embedding RAG have no trajectory for `RLMLogger` to capture. A harness that only
logs RLM runs cannot produce a comparable row for the other four-fifths of
Table 1.

They compose rather than compete — `RLMLogger`'s trajectory is one of the things
`runlog` records for the two systems that have one.

---

## 3. Still blocked

| What | On whom |
|---|---|
| 9 of 14 examples — the local-REPL ones that matter | API keys — mine |
| 5 examples on container/sandbox runtimes | third-party accounts or a Docker daemon; **recommend skipping** — they test environments MARD does not use (§1.3) |

Nothing here is blocked on another track. The REPL execution path itself is
already verified keyless (§1.2), so what the remaining examples add is
**provider** coverage — that the library talks to a real model correctly — and
that arrives with the keys.
