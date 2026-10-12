import pandas as pd

from profiler import main, profile


def test_basic_counts():
    df = pd.DataFrame({'a': [1, 2, 2], 'b': ['x', None, 'y']})
    s = profile(df)
    assert s['rows'] == 3
    assert s['columns'] == 2
    assert s['duplicate_rows'] == 0
    assert s['column_details']['b']['missing'] == 1


def test_duplicate_rows_detected():
    df = pd.DataFrame({'a': [1, 1], 'b': [2, 2]})
    assert profile(df)['duplicate_rows'] == 1


def test_numeric_outlier_detected():
    df = pd.DataFrame({'x': [10, 11, 12, 11, 10, 1000]})
    detail = profile(df)['column_details']['x']
    assert detail['outliers'] == 1
    assert detail['max'] == 1000.0


def test_empty_column_does_not_fail():
    df = pd.DataFrame({'a': pd.Series([], dtype='float64')})
    detail = profile(df)['column_details']['a']
    assert detail['missing_pct'] == 0.0
    assert 'mean' not in detail


def test_main_reads_file(tmp_path, capsys):
    csv = tmp_path / 'data.csv'
    csv.write_text('a,b\n1,x\n2,y\n')
    assert main([str(csv)]) == 0
    assert 'Rows: 2' in capsys.readouterr().out


def test_main_missing_file_returns_error(tmp_path, capsys):
    assert main([str(tmp_path / 'nope.csv')]) == 1
    assert 'could not read' in capsys.readouterr().err
