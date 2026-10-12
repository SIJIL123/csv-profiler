"""Profile a CSV file: schema, missing values, numeric stats, and outliers."""

from __future__ import annotations

import argparse
import sys

import pandas as pd


def profile(df: pd.DataFrame) -> dict:
    """Return a summary dict describing the DataFrame."""
    n_rows = len(df)
    summary = {
        'rows': n_rows,
        'columns': df.shape[1],
        'duplicate_rows': int(df.duplicated().sum()),
        'column_details': {},
    }

    for col in df.columns:
        series = df[col]
        n_missing = int(series.isna().sum())
        detail = {
            'dtype': str(series.dtype),
            'missing': n_missing,
            'missing_pct': round(100 * n_missing / n_rows, 2) if n_rows else 0.0,
            'unique': int(series.nunique(dropna=True)),
        }

        if pd.api.types.is_numeric_dtype(series) and series.notna().any():
            q1, q3 = series.quantile([0.25, 0.75])
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            detail.update(
                mean=float(series.mean()),
                std=float(series.std()),
                min=float(series.min()),
                max=float(series.max()),
                outliers=int(((series < lower) | (series > upper)).sum()),
            )

        summary['column_details'][col] = detail

    return summary


def format_report(summary: dict) -> str:
    """Render the summary as a plain-text report."""
    lines = [
        f"Rows: {summary['rows']}",
        f"Columns: {summary['columns']}",
        f"Duplicate rows: {summary['duplicate_rows']}",
        '',
    ]
    for col, d in summary['column_details'].items():
        lines.append(f'[{col}]')
        lines.append(f"  dtype:   {d['dtype']}")
        lines.append(f"  missing: {d['missing']} ({d['missing_pct']}%)")
        lines.append(f"  unique:  {d['unique']}")
        if 'mean' in d:
            lines.append(
                f"  mean={d['mean']:.4g}  std={d['std']:.4g}  "
                f"min={d['min']:.4g}  max={d['max']:.4g}"
            )
            lines.append(f"  outliers (IQR rule): {d['outliers']}")
        lines.append('')
    return '\n'.join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Profile a CSV file.')
    parser.add_argument('path', help='path to the CSV file')
    parser.add_argument('--sep', default=',', help="field separator (default: ',')")
    args = parser.parse_args(argv)

    try:
        df = pd.read_csv(args.path, sep=args.sep)
    except (OSError, pd.errors.ParserError) as exc:
        print(f'error: could not read {args.path}: {exc}', file=sys.stderr)
        return 1

    print(format_report(profile(df)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
