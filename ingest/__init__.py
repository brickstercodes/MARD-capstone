"""PDF to text with structural markers and page mapping. Owned by Track 4.

Separate from `corpus/` because parsing is code and the parsed output is data;
the O4 structure-dependence result depends on knowing which documents parsed
cleanly and which did not, so the quality report this produces is evidence, not
a build artefact.
"""
