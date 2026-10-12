# csv-profiler

A small command-line tool that gives you a quick first look at a CSV file before any analysis or modelling. For each column it reports the type, missing values, unique count, and, for numeric columns, basic statistics and outliers.

## What it reports

- Row, column, and duplicate-row counts
- Per column: dtype, missing count and percentage, unique values
- Numeric columns: mean, standard deviation, min, max
- Numeric columns: number of outliers using the IQR rule (values beyond 1.5 × IQR from the quartiles)

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python profiler.py data.csv
python profiler.py data.tsv --sep '\t'
```

## Tests

```bash
pytest -q
```

## Project layout

| File | Purpose |
| --- | --- |
| `profiler.py` | Profiling logic and CLI entry point |
| `test_profiler.py` | pytest suite |
| `requirements.txt` | Runtime and test dependencies |

## License

MIT
