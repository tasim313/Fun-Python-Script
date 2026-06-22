"""
Report Generator
================
Generates data quality and enrichment reports.
"""

import pandas as pd
import logging
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates data quality and enrichment reports."""

    def __init__(self, output_dir: str = 'reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _count_missing(self, series: pd.Series) -> int:
        """Count missing/invalid values in a series."""
        count = 0
        for val in series:
            if pd.isna(val):
                count += 1
            elif isinstance(val, str):
                stripped = val.strip()
                if stripped == '' or stripped.lower() in ('unknown', 'n/a', 'na', 'none', 'null', ''):
                    count += 1
        return count

    def _count_valid(self, series: pd.Series) -> int:
        """Count valid values in a series."""
        return len(series) - self._count_missing(series)

    def generate_completeness_report(self, df_before: pd.DataFrame, df_after: pd.DataFrame,
                                     changes_log: List[Dict] = None) -> str:
        """Generate a comprehensive data quality report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(self.output_dir, f'data_quality_report_{timestamp}.txt')

        lines = []
        lines.append("=" * 80)
        lines.append("DATA QUALITY & ENRICHMENT REPORT")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        lines.append("")

        # Summary
        lines.append("OVERVIEW")
        lines.append("-" * 40)
        lines.append(f"Total Rows: {len(df_before)}")
        lines.append(f"Total Columns: {len(df_before.columns)}")
        lines.append("")

        # Before/After comparison
        lines.append("COMPLETENESS COMPARISON")
        lines.append("-" * 40)
        lines.append(f"{'Column':<45} {'Before':>8} {'After':>8} {'Delta':>8} {'Before%':>10} {'After%':>10}")
        lines.append("-" * 90)

        total_cells_before = 0
        total_filled_before = 0
        total_cells_after = 0
        total_filled_after = 0

        for col in df_before.columns:
            missing_before = self._count_missing(df_before[col])
            missing_after = self._count_missing(df_after[col])
            valid_before = len(df_before) - missing_before
            valid_after = len(df_after) - missing_after
            total_cells_before += len(df_before)
            total_filled_before += valid_before
            total_cells_after += len(df_after)
            total_filled_after += valid_after

            pct_before = (valid_before / len(df_before) * 100) if len(df_before) > 0 else 0
            pct_after = (valid_after / len(df_after) * 100) if len(df_after) > 0 else 0
            delta = pct_after - pct_before

            lines.append(f"{col:<45} {missing_before:>8} {missing_after:>8} {delta:>+7.1f}% {pct_before:>9.1f}% {pct_after:>9.1f}%")

        lines.append("-" * 90)

        overall_before = (total_filled_before / total_cells_before * 100) if total_cells_before > 0 else 0
        overall_after = (total_filled_after / total_cells_after * 100) if total_cells_after > 0 else 0
        overall_delta = overall_after - overall_before

        lines.append(f"{'OVERALL':<45} {'':>8} {'':>8} {overall_delta:>+7.1f}% {overall_before:>9.1f}% {overall_after:>9.1f}%")
        lines.append("")

        # Changes summary
        if changes_log:
            lines.append("ENRICHMENT CHANGES SUMMARY")
            lines.append("-" * 40)
            lines.append(f"Total Changes Made: {len(changes_log)}")

            # Count by column
            col_counts = {}
            for change in changes_log:
                col = change.get('column', 'Unknown')
                col_counts[col] = col_counts.get(col, 0) + 1

            lines.append("\nChanges by Column:")
            for col, count in sorted(col_counts.items(), key=lambda x: -x[1]):
                lines.append(f"  {col:<45} {count:>6} records updated")

            # Count unique records modified
            unique_records = len(set(change.get('record_id', '') for change in changes_log))
            lines.append(f"\nUnique Records Modified: {unique_records}")

            # Records with no changes
            total_records = len(df_before)
            lines.append(f"Records Unchanged: {total_records - unique_records}")

            lines.append("")

            # Sample changes
            lines.append("SAMPLE CHANGES (First 20)")
            lines.append("-" * 40)
            for change in changes_log[:20]:
                lines.append(f"  Record: {change.get('record_id', 'N/A')}")
                lines.append(f"  Column: {change.get('column', 'N/A')}")
                lines.append(f"  Old Value: {change.get('old_value', '')[:80]}")
                lines.append(f"  New Value: {change.get('new_value', '')[:80]}")
                lines.append(f"  Source: {change.get('source', 'N/A')}")
                lines.append(f"  Timestamp: {change.get('timestamp', 'N/A')}")
                lines.append("")

        # Failed/Success counts
        lines.append("PROCESSING STATISTICS")
        lines.append("-" * 40)
        if changes_log:
            successfully_enriched = len(set(c.get('record_id', '') for c in changes_log))
            lines.append(f"Successfully Enriched Records: {successfully_enriched}")
            lines.append(f"Failed Records: {total_records - successfully_enriched}")
            lines.append(f"Enrichment Rate: {successfully_enriched / total_records * 100:.1f}%")
        else:
            lines.append("No changes were made.")

        lines.append("")
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        report_text = '\n'.join(lines)

        with open(report_path, 'w') as f:
            f.write(report_text)

        logger.info(f"Data quality report saved to {report_path}")
        return report_path

    def generate_enrichment_log(self, changes_log: List[Dict]) -> str:
        """Generate detailed enrichment log as CSV."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = os.path.join(self.output_dir, f'enrichment_log_{timestamp}.csv')

        if changes_log:
            df = pd.DataFrame(changes_log)
            df.to_csv(log_path, index=False)
            logger.info(f"Enrichment log saved to {log_path}")
        else:
            logger.info("No changes to log.")

        return log_path