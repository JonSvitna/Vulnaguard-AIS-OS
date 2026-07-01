#!/bin/bash
# export.sh — Convert a playbook markdown template to Word (.docx) and optionally PDF.
#
# Usage:
#   ./playbook/export.sh <template.md> "<Client Name>" [--pdf]
#
# Requires: pandoc, and optionally a Vulnaguard reference.docx for branded output.
#
# Examples:
#   ./playbook/export.sh templates/sow.md "Acme Defense LLC"
#   ./playbook/export.sh templates/executive-summary.md "Acme Defense LLC" --pdf
#
# Output lands in: engagements/{client-slug}/

set -e

TEMPLATE="${1}"
CLIENT_NAME="${2}"
PDF_FLAG="${3}"

if [[ -z "$TEMPLATE" || -z "$CLIENT_NAME" ]]; then
  echo "Usage: $0 <template.md> \"<Client Name>\" [--pdf]"
  exit 1
fi

if ! command -v pandoc &>/dev/null; then
  echo "Error: pandoc is not installed. Install it with: brew install pandoc"
  exit 1
fi

# Build client slug (lowercase, hyphens)
CLIENT_SLUG=$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')

# Output directory
OUTPUT_DIR="playbook/engagements/${CLIENT_SLUG}"
mkdir -p "$OUTPUT_DIR"

# Base filename from template name
BASENAME=$(basename "$TEMPLATE" .md)
OUTFILE="${OUTPUT_DIR}/${CLIENT_SLUG}_${BASENAME}"

# Reference doc for Vulnaguard branding (optional — place at playbook/reference.docx)
REFARG=""
REFFILE="playbook/reference.docx"
if [[ -f "$REFFILE" ]]; then
  REFARG="--reference-doc=${REFFILE}"
fi

# Replace placeholder tokens with client name in a temp file
TMPFILE=$(mktemp /tmp/vg-export-XXXXXX.md)
sed "s/{{CLIENT_NAME}}/${CLIENT_NAME}/g" "$TEMPLATE" > "$TMPFILE"

# Convert to Word
pandoc "$TMPFILE" \
  -o "${OUTFILE}.docx" \
  --from markdown \
  --to docx \
  $REFARG

echo "Created: ${OUTFILE}.docx"

# Optionally convert to PDF
if [[ "$PDF_FLAG" == "--pdf" ]]; then
  if command -v libreoffice &>/dev/null; then
    libreoffice --headless --convert-to pdf "${OUTFILE}.docx" --outdir "$OUTPUT_DIR" 2>/dev/null
    echo "Created: ${OUTFILE}.pdf"
  elif pandoc --list-output-formats 2>/dev/null | grep -q "^pdf$"; then
    pandoc "$TMPFILE" -o "${OUTFILE}.pdf" --from markdown $REFARG 2>/dev/null
    echo "Created: ${OUTFILE}.pdf"
  else
    echo "PDF conversion skipped: install LibreOffice or a pandoc PDF engine (brew install --cask libreoffice)"
  fi
fi

rm -f "$TMPFILE"
echo "Done. Output: ${OUTPUT_DIR}/"
