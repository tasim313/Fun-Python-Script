#!/usr/bin/env python3
"""Quick test of the enrichment pipeline on 5 records."""

import asyncio
import sys
import os
import pandas as pd

sys.path.insert(0, '.')

from data_enrichment.enrichment_runner import EnrichmentRunner

async def test():
    # Create a small test file
    df = pd.read_csv('casinos_export.csv')
    test_df = df.head(5)
    test_df.to_csv('test_5_records.csv', index=False)
    
    runner = EnrichmentRunner(
        input_file='test_5_records.csv',
        output_file='test_5_enriched.csv',
        batch_size=5,
        concurrency=5,
        resume=False,
    )
    
    await runner.run()

if __name__ == '__main__':
    asyncio.run(test())