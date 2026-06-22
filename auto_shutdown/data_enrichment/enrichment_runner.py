#!/usr/bin/env python3
"""
Enrichment Runner
=================
Main pipeline orchestrator for casino data enrichment.
Handles batch processing, checkpoint/resume, and error recovery.
"""

import asyncio
import pandas as pd
import logging
import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_enrichment.collectors.website_collector import WebsiteCollector
from data_enrichment.collectors.dns_collector import DNSCollector
from data_enrichment.collectors.ssl_collector import SSLCollector
from data_enrichment.collectors.review_collector import ReviewCollector
from data_enrichment.validators.data_validators import DataValidators
from data_enrichment.normalizers.data_normalizers import DataNormalizers
from data_enrichment.exporters.csv_exporter import CSVExporter
from data_enrichment.exporters.report_generator import ReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('enrichment_output.log'),
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger('enrichment_runner')

# Column mapping: enrichment keys -> CSV column names
COLUMN_MAPPING = {
    'languages': 'Languages',
    'currencies': 'Currencies',
    'license_type': 'License Type',
    'license_number': 'License Number',
    'ip_address': 'IP Address',
    'hosting_provider': 'Hosting Provider',
    'nameservers': 'Nameservers',
    'ssl_issuer': 'SSL Issuer',
    'contact_email': 'Payment Processor Names',
    'deposit_methods': 'Payment Processor Types',
    'live_chat': 'Payment Processor Detection Methods',
}


class EnrichmentRunner:
    """Main pipeline orchestrator for casino data enrichment."""

    def __init__(self, input_file: str, output_file: str = None,
                 batch_size: int = 100, concurrency: int = 20,
                 checkpoint_interval: int = 500, resume: bool = True):
        """
        Initialize the enrichment runner.

        Args:
            input_file: Path to input CSV
            output_file: Path to output CSV (defaults to input_enriched.csv)
            batch_size: Number of records per batch
            concurrency: Number of concurrent requests
            checkpoint_interval: Save checkpoint every N records
            resume: Whether to resume from checkpoint
        """
        self.input_file = input_file
        self.output_file = output_file or input_file.replace('.csv', '_enriched.csv')
        self.batch_size = batch_size
        self.concurrency = concurrency
        self.checkpoint_interval = checkpoint_interval
        self.resume = resume

        # Initialize collectors - optimized for speed
        self.website_collector = WebsiteCollector(timeout=10, max_retries=2)
        self.dns_collector = DNSCollector()
        self.ssl_collector = SSLCollector()
        self.review_collector = ReviewCollector(timeout=10)

        # Initialize exporters
        self.csv_exporter = CSVExporter(input_file, output_file)
        self.report_generator = ReportGenerator(output_dir='reports')

        # Checkpoint file
        self.checkpoint_file = input_file.replace('.csv', '_checkpoint.json')

        # Ensure directories exist
        os.makedirs('reports', exist_ok=True)
        os.makedirs('data_enrichment/logs', exist_ok=True)

    def _load_checkpoint(self) -> Dict[int, Dict[str, Any]]:
        """Load checkpoint data if available."""
        if not self.resume or not os.path.exists(self.checkpoint_file):
            return {}

        try:
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
                # Convert string keys back to int
                return {int(k): v for k, v in data.items()}
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")
            return {}

    def _save_checkpoint(self, enrichment_data: Dict[int, Dict[str, Any]]):
        """Save enrichment data to checkpoint."""
        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump({str(k): v for k, v in enrichment_data.items()}, f)
        except Exception as e:
            logger.warning(f"Failed to save checkpoint: {e}")

    def _clear_checkpoint(self):
        """Remove checkpoint file after successful completion."""
        try:
            if os.path.exists(self.checkpoint_file):
                os.remove(self.checkpoint_file)
        except Exception:
            pass

    def _save_incremental_csv(self, df_original: pd.DataFrame, enrichment_data: Dict[int, Dict[str, Any]]):
        """Save the enriched CSV incrementally after each batch."""
        df = df_original.copy()

        # Pre-convert columns that might need string values
        columns_to_enrich = set()
        for data in enrichment_data.values():
            for enrich_key in data:
                if enrich_key in COLUMN_MAPPING:
                    columns_to_enrich.add(COLUMN_MAPPING[enrich_key])
        for col in columns_to_enrich:
            if col in df.columns and df[col].dtype in ('float64', 'int64'):
                df[col] = df[col].astype(object)

        # Apply enrichment directly without logging
        for row_idx, data in enrichment_data.items():
            if row_idx not in df.index:
                continue
            for enrich_key, value in data.items():
                if value is None or enrich_key not in COLUMN_MAPPING:
                    continue
                csv_column = COLUMN_MAPPING[enrich_key]
                if csv_column not in df.columns:
                    continue
                current_value = df.at[row_idx, csv_column]
                if self.csv_exporter._is_missing(current_value):
                    if value is not None and str(value).strip() != '':
                        try:
                            df.at[row_idx, csv_column] = value
                        except (TypeError, ValueError):
                            df[csv_column] = df[csv_column].astype(object)
                            df.at[row_idx, csv_column] = value

        df.to_csv(self.output_file, index=False)
        logger.info(f"  -> Incremental CSV saved ({len(enrichment_data)} records enriched)")

    def _count_missing_in_row(self, row: pd.Series) -> int:
        """Count missing fields in a row."""
        missing_fields = []
        for col in row.index:
            val = row[col]
            if pd.isna(val) or (isinstance(val, str) and val.strip().lower() in ('', 'unknown', 'n/a', 'na', 'none')):
                missing_fields.append(col)
        return missing_fields

    def _enrich_row_from_website(self, website_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform website collection data to CSV column values."""
        enriched = {}

        # Languages
        if website_data.get('languages'):
            normalized = DataNormalizers.normalize_languages(website_data['languages'])
            if normalized:
                enriched['languages'] = normalized

        # Currencies
        if website_data.get('currencies'):
            normalized = DataNormalizers.normalize_currencies(website_data['currencies'])
            if normalized:
                enriched['currencies'] = normalized

        # License type
        if website_data.get('license_type'):
            validated = DataValidators.validate_license_type(website_data['license_type'])
            if validated:
                enriched['license_type'] = validated

        # License number
        if website_data.get('license_number'):
            normalized = DataNormalizers.normalize_license_number(website_data['license_number'])
            if normalized:
                enriched['license_number'] = normalized

        # Payment methods (deposit)
        if website_data.get('deposit_methods'):
            normalized = DataNormalizers.normalize_payment_methods(website_data['deposit_methods'])
            if normalized:
                enriched['deposit_methods'] = normalized

        # Live chat
        if website_data.get('live_chat') is True:
            enriched['live_chat'] = 'Yes'

        return enriched

    def _enrich_row_from_dns(self, dns_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform DNS collection data to CSV column values."""
        enriched = {}

        if dns_data.get('ip_address'):
            normalized = DataNormalizers.normalize_ip(dns_data['ip_address'])
            if normalized:
                enriched['ip_address'] = normalized

        if dns_data.get('nameservers'):
            enriched['nameservers'] = dns_data['nameservers']

        if dns_data.get('hosting_provider'):
            enriched['hosting_provider'] = dns_data['hosting_provider']

        return enriched

    def _enrich_row_from_ssl(self, ssl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform SSL collection data to CSV column values."""
        enriched = {}

        if ssl_data.get('ssl_issuer'):
            normalized = DataNormalizers.normalize_ssl_issuer(ssl_data['ssl_issuer'])
            if normalized:
                enriched['ssl_issuer'] = normalized

        return enriched

    async def process_batch(self, batch_df: pd.DataFrame, batch_start_idx: int) -> Dict[int, Dict[str, Any]]:
        """Process a batch of records through all collectors."""
        enrichment_results = {}

        urls = []
        domains = []
        row_indices = []

        for idx, row in batch_df.iterrows():
            url = row.get('Website URL', '')
            domain = row.get('Domain', '')
            if url and isinstance(url, str) and url.strip():
                urls.append(url.strip())
                domains.append(domain.strip() if isinstance(domain, str) else domain)
                row_indices.append(idx)

        if not urls:
            return enrichment_results

        logger.info(f"  Processing {len(urls)} websites...")

        # Collect website data
        try:
            website_results = await self.website_collector.collect_batch(
                urls, concurrency=min(self.concurrency, 20)
            )
        except Exception as e:
            logger.error(f"  Website collection failed: {e}")
            website_results = {url: {} for url in urls}

        # Collect DNS data
        logger.info(f"  Collecting DNS information...")
        try:
            dns_results = await self.dns_collector.collect_batch(
                domains, concurrency=min(self.concurrency, 30)
            )
        except Exception as e:
            logger.error(f"  DNS collection failed: {e}")
            dns_results = {domain: {} for domain in domains}

        # Collect SSL data
        logger.info(f"  Collecting SSL information...")
        try:
            ssl_results = await self.ssl_collector.collect_batch(
                domains, concurrency=min(self.concurrency, 30)
            )
        except Exception as e:
            logger.error(f"  SSL collection failed: {e}")
            ssl_results = {domain: {} for domain in domains}

        # Merge results for each row
        for i, (idx, url, domain) in enumerate(zip(row_indices, urls, domains)):
            row_data = {}

            # Website data
            web_data = website_results.get(url, {})
            row_data.update(self._enrich_row_from_website(web_data))

            # DNS data
            dns_data = dns_results.get(domain, {})
            row_data.update(self._enrich_row_from_dns(dns_data))

            # SSL data
            ssl_data = ssl_results.get(domain, {})
            row_data.update(self._enrich_row_from_ssl(ssl_data))

            if row_data:
                enrichment_results[idx] = row_data

        return enrichment_results

    async def run(self):
        """Run the full enrichment pipeline."""
        start_time = time.time()
        logger.info("=" * 60)
        logger.info("CASINO DATA ENRICHMENT PIPELINE")
        logger.info("=" * 60)

        # Load data
        logger.info(f"Loading data from {self.input_file}...")
        df_original = pd.read_csv(self.input_file)
        df = df_original.copy()
        total_rows = len(df)
        logger.info(f"Loaded {total_rows} rows, {len(df.columns)} columns")

        # Load checkpoint
        all_enrichment = self._load_checkpoint()
        if all_enrichment:
            logger.info(f"Resuming from checkpoint: {len(all_enrichment)} records already processed")
        
        # Determine which rows need processing
        remaining_indices = []
        for idx in df.index:
            if idx not in all_enrichment:
                # Check if this row has missing data worth enriching
                missing = self._count_missing_in_row(df.loc[idx])
                if missing:
                    remaining_indices.append(idx)

        logger.info(f"Records to process: {len(remaining_indices)}")
        logger.info(f"Records already enriched: {len(all_enrichment)}")

        # Process in batches
        processed_count = 0
        total_batches = (len(remaining_indices) + self.batch_size - 1) // self.batch_size

        for batch_num in range(0, len(remaining_indices), self.batch_size):
            batch_indices = remaining_indices[batch_num:batch_num + self.batch_size]
            batch_df = df.loc[batch_indices]
            current_batch = batch_num // self.batch_size + 1

            logger.info(f"\n--- Batch {current_batch}/{total_batches} "
                       f"(records {batch_num + 1}-{min(batch_num + self.batch_size, len(remaining_indices))}"
                       f" of {len(remaining_indices)}) ---")

            try:
                batch_results = await self.process_batch(batch_df, batch_num)
                all_enrichment.update(batch_results)
                processed_count += len(batch_indices)

                # Log batch results
                enriched_in_batch = sum(1 for r in batch_results.values() if r)
                total_fields = sum(len(r) for r in batch_results.values())
                logger.info(f"  Batch {current_batch} complete: "
                          f"{enriched_in_batch}/{len(batch_indices)} records enriched, "
                          f"{total_fields} fields populated")

            except Exception as e:
                logger.error(f"  Batch {current_batch} failed: {e}")
                processed_count += len(batch_indices)

            # Save checkpoint AND incrementally update CSV after each batch
            self._save_checkpoint(all_enrichment)
            self._save_incremental_csv(df, all_enrichment)

        # Final save
        logger.info("\nFinal save...")
        self._save_incremental_csv(df, all_enrichment)
        output_path = self.output_file

        # Save changes log
        changes_log = self.csv_exporter.get_changes_log()
        if changes_log:
            self.csv_exporter.save_changes_log(
                os.path.join('reports', 'enrichment_changes.csv')
            )

        # Generate reports
        logger.info("Generating reports...")
        df_enriched = pd.read_csv(self.output_file)
        report_path = self.report_generator.generate_completeness_report(
            df_original, df_enriched, changes_log
        )

        log_path = self.report_generator.generate_enrichment_log(changes_log)

        # Clear checkpoint on success
        self._clear_checkpoint()

        elapsed = time.time() - start_time
        logger.info("\n" + "=" * 60)
        logger.info("ENRICHMENT COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Output file: {output_path}")
        logger.info(f"Quality report: {report_path}")
        logger.info(f"Changes log: {log_path}")
        logger.info(f"Total changes: {len(changes_log)}")
        logger.info(f"Total time: {elapsed:.1f} seconds")
        logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Casino Data Enrichment Pipeline')
    parser.add_argument('--input', '-i', default='casinos_export.csv',
                       help='Input CSV file (default: casinos_export.csv)')
    parser.add_argument('--output', '-o', default=None,
                       help='Output CSV file (default: input_enriched.csv)')
    parser.add_argument('--batch-size', '-b', type=int, default=100,
                       help='Batch size (default: 100)')
    parser.add_argument('--concurrency', '-c', type=int, default=20,
                       help='Concurrent requests (default: 20)')
    parser.add_argument('--no-resume', action='store_true',
                       help='Do not resume from checkpoint')
    parser.add_argument('--max-rows', '-m', type=int, default=None,
                       help='Maximum number of rows to process')

    args = parser.parse_args()

    runner = EnrichmentRunner(
        input_file=args.input,
        output_file=args.output,
        batch_size=args.batch_size,
        concurrency=args.concurrency,
        resume=not args.no_resume,
    )

    asyncio.run(runner.run())


if __name__ == '__main__':
    main()