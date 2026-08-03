"""The Master Plan contract between Tier 1 and Tier 2. Owned by Track 2.

Its own package rather than part of `orchestrate/` because the schema is a
contract that Track 1 writes to and Track 3 scores against. A malformed plan
must fail loudly at this boundary — the alternative is N builders producing
subtly wrong sections that nobody notices until the results are in.
"""
