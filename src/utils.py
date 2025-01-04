import csv
from datetime import datetime
import logging
from pathlib import Path
import pandas as pd
from typing import List, Union, Dict, Any
from src.schema import Report
from src.metrics_schema import TokenAnalysis

FLATTENED_REPORT_COLUMNS = 123


def save_report(report: Report, output_path: str) -> None:
    """Save a report to a JSON file"""
    with open(output_path, 'w') as f:
        f.write(report.model_dump_json(indent=2))


def load_single_report(json_path: Union[str, Path]) -> Report:
    """Load a single JSON file into a Report object"""
    return Report.from_json(json_path)


def load_multiple_reports(json_paths: List[str]) -> List[Report]:
    """Load all report JSON files from a directory into Report objects"""
    reports = []

    for json_file in json_paths:
        try:
            report = Report.from_json(json_file)
            reports.append(report)
        except Exception as e:
            logging.info(f"Error loading {json_file}: {e}")
            continue

    return reports


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flatten nested dictionaries, handling nested objects and datetime values"""
    items: List[tuple] = []

    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, datetime):
            items.append((new_key, v.strftime('%Y-%m-%d %H:%M:%S')))
        else:
            items.append((new_key, v))

    return dict(items)


def reports_to_csv(reports: List[Report], output_path: str) -> None:
    """Convert a list of reports to a CSV file using Pydantic model_dump"""
    if not reports:
        raise ValueError("No reports provided")

    # Get all fields from first report
    first_report = reports[0].model_dump()
    flattened = flatten_dict(first_report)
    assert len(flattened.keys()) == FLATTENED_REPORT_COLUMNS, f"Flattened report columns {len(flattened.keys())} do not match expected number of columns: 123"
    headers = list(flattened.keys())

    rows = []
    for report in reports:
        # Convert report to dict and flatten
        report_dict = report.model_dump()
        flat_row = flatten_dict(report_dict)

        row = {}
        for k in headers:
            if k in flat_row:
                row[k] = flat_row[k]
            else:
                row[k] = None

        row = pd.Series(row)
        rows.append(row)

    df = pd.concat(rows, axis=1).T
    df.columns = headers
    df.to_csv(output_path, index=False)


def save_token_analysis(analysis: TokenAnalysis, output_path: str) -> None:
    """Save a TokenAnalysis object to a JSON file"""
    with open(output_path, 'w') as f:
        f.write(analysis.model_dump_json(indent=2))
