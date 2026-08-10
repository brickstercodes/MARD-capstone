"""Tier 2 fork-join execution. Owned by Track 2.

Bounded asyncio worker pool, per-builder retry, failure isolation, and a join
that respects Master Plan order rather than book order. Wall-clock is
max(builder), not the sum — that property is a measured claim, so the
orchestrator has to be honest about where time actually goes.
"""
