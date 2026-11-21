#!/bin/bash
# IFT3295 - TP3 - Script d'execution (fourni, NE PAS MODIFIER).
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

echo "=== Exemple de l'enonce ==="
"$PY" main.py -i CGTAGTCGGCTAACGCATACGCTTGATAAGCGTAAGAGCCC -db tRNAs.fasta -E 5 -ss 10
