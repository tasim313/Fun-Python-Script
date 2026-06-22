#!/bin/bash
# Casino Data Enrichment Pipeline Runner
# Runs the full enrichment pipeline on casinos_export.csv
# Supports resume from checkpoint on failure

cd /home/mostasim/python/auto_shutdown

echo "=============================================="
echo "Casino Data Enrichment Pipeline"
echo "Started: $(date)"
echo "=============================================="

# Run the enrichment pipeline
python3 -m data_enrichment.enrichment_runner \
    --input casinos_export.csv \
    --output casinos_export_enriched.csv \
    --batch-size 200 \
    --concurrency 25 \
    2>&1 | tee enrichment_output.log

EXIT_CODE=$?

echo ""
echo "=============================================="
echo "Finished: $(date)"
echo "Exit Code: $EXIT_CODE"
echo "=============================================="

if [ $EXIT_CODE -eq 0 ]; then
    echo "Enrichment completed successfully!"
    echo "Output: casinos_export_enriched.csv"
    echo "Reports: reports/"
else
    echo "Enrichment failed or was interrupted."
    echo "Run again to resume from checkpoint."
fi