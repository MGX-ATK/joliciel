import sys
import types
import csv
from collections import Counter


# ---- pandas stub ----
class ColumnIndex(list):
    @property
    def str(self):
        class Ops:
            def __init__(self, data):
                self.data = data

            def strip(self):
                return ColumnIndex([s.strip() if isinstance(s, str) else s for s in self.data])

            def replace(self, old, new, regex=False):
                if regex:
                    import re
                    pattern = re.compile(old)
                    return ColumnIndex([pattern.sub(new, s) if isinstance(s, str) else s for s in self.data])
                return ColumnIndex([s.replace(old, new) if isinstance(s, str) else s for s in self.data])

        return Ops(self)

    def tolist(self):
        return list(self)

class Series(list):
    def __eq__(self, other):
        return [x == other for x in self]
    def value_counts(self):
        cnt = Counter(self)
        items = sorted(cnt.items(), key=lambda x: -x[1])
        return ValueCounts(items)

class ValueCounts:
    def __init__(self, items):
        self.items = items
        self.name = None
    def rename_axis(self, name):
        self.name = name
        return self
    def reset_index(self, name="count"):
        rows = [{self.name or "index": v, name: c} for v, c in self.items]
        return DataFrame(rows)

class DataFrame:
    def __init__(self, rows):
        self._rows = rows
        self._columns = ColumnIndex(list(rows[0].keys()) if rows else [])
    @property
    def columns(self):
        return self._columns
    @columns.setter
    def columns(self, value):
        if isinstance(value, ColumnIndex):
            self._columns = value
        else:
            self._columns = ColumnIndex(list(value))
    def __getitem__(self, key):
        if isinstance(key, str):
            return Series([row.get(key) for row in self._rows])
        elif isinstance(key, list):
            rows = [row for row, keep in zip(self._rows, key) if keep]
            return DataFrame(rows)
        raise TypeError
    @property
    def empty(self):
        return not self._rows
    def to_dict(self, orient="records"):
        return [row.copy() for row in self._rows]
    def head(self, n):
        return DataFrame(self._rows[:n])

# functions for stub

def read_csv(path, encoding=None, sep=None, engine=None):
    with open(path, newline="", encoding=encoding) as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    return DataFrame(rows)

def notna(value):
    return value not in (None, "")

pandas_stub = types.ModuleType("pandas")
pandas_stub.read_csv = read_csv
pandas_stub.notna = notna
pandas_stub.DataFrame = DataFrame

sys.modules.setdefault("pandas", pandas_stub)

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "poc_corpus.main", Path(__file__).resolve().parents[1] / "poc_corpus" / "main.py"
)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

PARTIE_EXAMPLE = "Partie 1 – Paroles de maintenanciers"


def test_get_parties_not_empty():
    data = main.get_parties()
    assert isinstance(data, list)
    assert data, "/parties should not be empty"


def test_get_sous_parties_known_value():
    data = main.get_sous_parties(PARTIE_EXAMPLE)
    assert isinstance(data, list)
    # Expect at least one known sous-partie
    assert any(d["sous_partie"] == "Dix parcours inspirants" and d["size"] == 10 for d in data)
