# csv-profiler

A small command-line tool for a first look at a CSV file.

For each column it shows the type, how many values are missing, and how many distinct values there are. For numeric columns it also shows the mean, standard deviation, min, max, and how many outliers there are. Outliers here means values far outside the middle of the data, using the usual IQR rule.

It's handy before you start cleaning or modelling, since missing values and wrong column types show up right away.

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

## Files

| File | What it does |
| --- | --- |
| `profiler.py` | Profiling logic and the command-line entry point |
| `test_profiler.py` | Tests |
| `requirements.txt` | Dependencies |

## License

MIT
