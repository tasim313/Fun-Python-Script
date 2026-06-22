"""
CSV Exporter
============
Exports enriched data back to CSV format.
Preserves original schema and only fills missing fields.
"""

import pandas as pd
import logging
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CSVExporter:
    """Exports enriched data to CSV while preserving original structure."""

    def __init__(self, input_file: str, output_file: str = None):
        self.input_file = input_file
        self.output_file = output_file or input_file.replace('.csv', '_enriched.csv')
        self.changes_log: List[Dict[str, Any]] = []

    def log_change(self, row_idx: int, column: str, old_value: Any, new_value: Any,
                   source: str = '', record_id: str = ''):
        """Log a change for the enrichment report."""
        self.changes_log.append({
            'row_index': row_idx,
            'record_id': record_id,
            'column': column,
            'old_value': str(old_value) if old_value is not None else '',
            'new_value': str(new_value) if new_value is not None else '',
            'source': source,
            'timestamp': datetime.now().isoformat(),
        })

    def apply_enrichment(self, df: pd.DataFrame, enrichment_data: Dict[int, Dict[str, Any]],
                        column_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Apply enrichment data to the dataframe.
        
        Args:
            df: Original dataframe
            enrichment_data: Dict of {row_index: {csv_column: value}}
            column_mapping: Maps enrichment keys to CSV column names
        """
        # Pre-convert columns that might need string values but are float64 (all NaN)
        columns_to_enrich = set()
        for data in enrichment_data.values():
            for enrich_key in data:
                if enrich_key in column_mapping:
                    columns_to_enrich.add(column_mapping[enrich_key])

        for col in columns_to_enrich:
            if col in df.columns and df[col].dtype in ('float64', 'int64'):
                df[col] = df[col].astype(object)

        for row_idx, data in enrichment_data.items():
            if row_idx not in df.index:
                continue

            for enrich_key, value in data.items():
                if value is None or enrich_key not in column_mapping:
                    continue

                csv_column = column_mapping[enrich_key]

                if csv_column not in df.columns:
                    continue

                current_value = df.at[row_idx, csv_column]

                # Only fill missing/invalid values - never overwrite existing valid data
                if self._is_missing(current_value):
                    # Validate the new value
                    if value is not None and str(value).strip() != '':
                        try:
                            df.at[row_idx, csv_column] = value
                        except (TypeError, ValueError):
                            # If type conversion fails, convert column to object first
                            df[csv_column] = df[csv_column].astype(object)
                            df.at[row_idx, csv_column] = value
                        self.log_change(
                            row_idx=row_idx,
                            column=csv_column,
                            old_value=current_value,
                            new_value=value,
                            source=enrich_key,
                            record_id=str(df.at[row_idx, 'Domain'] if 'Domain' in df.columns else row_idx),
                        )

        return df

    def _is_missing(self, value: Any) -> bool:
        """Check if a value is missing or placeholder."""
        if pd.isna(value):
            return True
        if isinstance(value, str):
            stripped = value.strip()
            if stripped == '':
                return True
            if stripped.lower() in ('unknown', 'n/a', 'na', 'none', 'null', 'undefined'):
                return True
        return False

    def save(self, df: pd.DataFrame) -> str:
        """Save the enriched dataframe to CSV."""
        df.to_csv(self.output_file, index=False)
        logger.info(f"Enriched data saved to {self.output_file}")
        return self.output_file

    def get_changes_log(self) -> List[Dict[str, Any]]:
        """Get the changes log."""
        return self.changes_log

    def save_changes_log(self, filepath: str):
        """Save the changes log to a CSV file."""
        if self.changes_log:
            changes_df = pd.DataFrame(self.changes_log)
            changes_df.to_csv(filepath, index=False)
            logger.info(f"Changes log saved to {filepath}")