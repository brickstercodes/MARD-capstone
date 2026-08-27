#!/usr/bin/env bash
# Fetch a corpus PDF, verify it against corpus/SOURCES.json, and parse it.
#
# WHY this exists: corpus/*/document.* is gitignored, so a fresh clone has the
# artefacts derived from the parsed text but not the text or the PDF. "Regenerate
# the corpus" and "reproduce the corpus" are therefore different operations, and
# before this script nothing could tell them apart -- an upstream reissue of the
# PDF would produce clean-looking artefacts for a different book. See
# ingest/manifest.py for the full argument.
#
# Usage:  scripts/fetch_corpus.sh introcs
#
set -euo pipefail

DOC_ID="${1:-}"
REGISTRY="corpus/SOURCES.json"
RAW_DIR="corpus/raw"

if [[ -z "$DOC_ID" ]]; then
  echo "usage: $0 <doc-id>    (doc-ids: $(python3 -c "
import json;print(', '.join(k for k in json.load(open('$REGISTRY')) if not k.startswith('_')))"))" >&2
  exit 2
fi

read -r URL FILE_NAME EXPECTED_SHA < <(python3 - "$DOC_ID" <<'PY'
import json, sys
doc_id = sys.argv[1]
entry = json.load(open("corpus/SOURCES.json")).get(doc_id)
if entry is None:
    sys.exit(f"'{doc_id}' is not in corpus/SOURCES.json")
if not entry.get("url"):
    sys.exit(
        f"corpus/SOURCES.json has no url for '{doc_id}'.\n"
        "Fill it from the publisher's own download page, record retrieved_on, and\n"
        "put the file's sha256 in pdf_sha256. Do not guess any of the three."
    )
print(entry["url"], entry.get("file_name") or f"{doc_id}.pdf", entry.get("pdf_sha256") or "-")
PY
)

mkdir -p "$RAW_DIR"
TARGET="$RAW_DIR/$FILE_NAME"

if [[ -f "$TARGET" ]]; then
  echo "already present: $TARGET"
else
  echo "fetching $DOC_ID from $URL"
  curl -fL --retry 3 -o "$TARGET" "$URL"
fi

ACTUAL_SHA="$(python3 -c "
import hashlib,sys
h=hashlib.sha256()
with open('$TARGET','rb') as f:
    while (b:=f.read(1<<20)): h.update(b)
print(h.hexdigest())")"

if [[ "$EXPECTED_SHA" == "-" ]]; then
  # First fetch of this document. Record the hash rather than silently accepting it:
  # an unpinned download is exactly the drift this script exists to prevent.
  echo
  echo "NO PINNED HASH for '$DOC_ID'. The file just downloaded is:"
  echo "  sha256      $ACTUAL_SHA"
  echo "  bytes       $(wc -c <"$TARGET")"
  echo
  echo "Put that in corpus/SOURCES.json as pdf_sha256, set retrieved_on to today,"
  echo "commit it, and re-run. Nothing is parsed until the source is pinned."
  exit 1
fi

if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo >&2
  echo "SOURCE MISMATCH for '$DOC_ID' -- refusing to parse." >&2
  echo "  expected  $EXPECTED_SHA" >&2
  echo "  got       $ACTUAL_SHA" >&2
  echo >&2
  echo "The upstream file has changed since it was pinned. This is not a nuisance:" >&2
  echo "a reissued PDF shifts pagination, which shifts section spans, the skeleton," >&2
  echo "and every score computed from them. Decide deliberately -- re-pin and re-run" >&2
  echo "the whole matrix, or keep the pinned edition -- and record the decision." >&2
  exit 1
fi

echo "source verified: $ACTUAL_SHA"
python3 -m ingest.cli "$TARGET" --doc-id "$DOC_ID"
python3 -m ingest.manifest corpus --document-id "$DOC_ID"
echo
echo "Next: python -m envelope.cli corpus --document-id $DOC_ID"
