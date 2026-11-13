#!/usr/bin/env python3
"""Compare two lists (CSV or XLSX) line by line, grouped by a link column.

Two commands:

  peek     Print the header and the first rows of a file, as JSON.
           The skill shows this to the user before it compares.

  compare  Match two files on a link column, sum an amount column per key,
           and write the result tables. Prints a JSON summary.

The script reads files and writes files. It calls no outside service.
It never changes an input file.

XLSX needs the openpyxl package. CSV needs nothing outside the standard library.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import OrderedDict
from decimal import Decimal, InvalidOperation
from pathlib import Path

try:
    import openpyxl  # type: ignore
except ImportError:  # pragma: no cover - depends on the machine
    openpyxl = None


# --------------------------------------------------------------------------- reading


class InputError(Exception):
    """A problem the user can fix, such as a wrong column name."""


def read_table(path: Path, sheet: str | None = None) -> tuple[list[str], list[tuple[int, list]]]:
    """Return (header, rows). Each row is (row_number_in_file, cells)."""
    if not path.exists():
        raise InputError(f"file not found: {path}")
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xlsm"):
        return _read_xlsx(path, sheet)
    if suffix in (".csv", ".tsv", ".txt"):
        return _read_csv(path)
    raise InputError(f"unsupported file type: {suffix} (use .xlsx or .csv)")


def _read_csv(path: Path):
    raw = path.read_bytes()
    text = None
    for enc in ("utf-8-sig", "cp1258", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    assert text is not None
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(text.splitlines(), dialect)
    return _split_header(enumerate(reader, start=1))


def _read_xlsx(path: Path, sheet: str | None):
    if openpyxl is None:
        raise InputError("openpyxl_missing: install it with 'pip install openpyxl', or save the file as CSV")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    if sheet:
        if sheet not in wb.sheetnames:
            raise InputError(f"sheet not found: {sheet}. Sheets: {wb.sheetnames}")
        ws = wb[sheet]
    else:
        ws = wb.worksheets[0]
    rows = ((i, list(r)) for i, r in enumerate(ws.iter_rows(values_only=True), start=1))
    result = _split_header(rows)
    wb.close()
    return result


def _is_empty(cells) -> bool:
    return all(c is None or str(c).strip() == "" for c in cells)


def _split_header(numbered_rows):
    header: list[str] | None = None
    rows: list[tuple[int, list]] = []
    for num, cells in numbered_rows:
        if _is_empty(cells):
            continue
        if header is None:
            header = [str(c).strip() if c is not None else "" for c in cells]
            continue
        rows.append((num, list(cells)))
    if header is None:
        raise InputError("the file has no header row")
    return header, rows


def col_index(header: list[str], name: str) -> int:
    wanted = name.strip().casefold()
    for i, h in enumerate(header):
        if h.strip().casefold() == wanted:
            return i
    raise InputError(f"column not found: {name!r}. Columns: {header}")


# --------------------------------------------------------------------------- values

_CURRENCY = re.compile(r"[^\d,.\-()+]")


def parse_amount(value, decimal_mark: str = "auto") -> Decimal | None:
    """Turn a cell into a Decimal. Return None for an empty cell.

    Raise ValueError when the cell holds text that is not a number.
    Handles 1,234.56 / 1.234,56 / 1 234,56 / (123) / -123 / 123- / currency signs.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(str(value))
    if isinstance(value, (int, Decimal)):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(repr(value))
    s = str(value).strip()
    if s in ("", "-", "–"):
        return None
    negative = False
    if s.startswith("(") and s.endswith(")"):
        negative, s = True, s[1:-1]
    s = s.replace(" ", "").replace(" ", "")
    if s.endswith("-"):
        negative, s = True, s[:-1]
    s = _CURRENCY.sub("", s)
    if s.startswith("-"):
        negative, s = (not negative), s[1:]
    elif s.startswith("+"):
        s = s[1:]
    if not s or not re.fullmatch(r"[\d.,]+", s):
        raise ValueError(str(value))
    s = _normalize_separators(s, decimal_mark)
    try:
        d = Decimal(s)
    except InvalidOperation:
        raise ValueError(str(value)) from None
    return -d if negative else d


def _normalize_separators(s: str, decimal_mark: str) -> str:
    if decimal_mark == ".":
        return s.replace(",", "")
    if decimal_mark == ",":
        return s.replace(".", "").replace(",", ".")
    # auto: the last separator is the decimal mark, unless it is followed by
    # exactly three digits and it is the only kind used (then it groups thousands).
    has_dot, has_comma = "." in s, "," in s
    if has_dot and has_comma:
        if s.rfind(",") > s.rfind("."):
            return s.replace(".", "").replace(",", ".")
        return s.replace(",", "")
    sep = "." if has_dot else "," if has_comma else None
    if sep is None:
        return s
    parts = s.split(sep)
    if len(parts) > 2 or (len(parts[-1]) == 3 and parts[0] not in ("", "0")):
        return s.replace(sep, "")  # thousands grouping
    return s.replace(sep, ".")


def normalize_key(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return re.sub(r"\s+", " ", str(value)).strip().upper()


# --------------------------------------------------------------------------- compare


def load_side(path, sheet, key_col, amount_col, decimal_mark):
    header, rows = read_table(Path(path), sheet)
    ki, ai = col_index(header, key_col), col_index(header, amount_col)
    groups: "OrderedDict[str, dict]" = OrderedDict()
    no_key, bad_amount = [], []
    total = Decimal(0)
    for num, cells in rows:
        cells = cells + [None] * (max(ki, ai) + 1 - len(cells))
        key = normalize_key(cells[ki])
        try:
            amount = parse_amount(cells[ai], decimal_mark)
        except ValueError:
            bad_amount.append({"row": num, "key": key, "value": str(cells[ai])})
            continue
        amount = amount or Decimal(0)
        total += amount
        if not key:
            no_key.append({"row": num, "amount": amount})
            continue
        g = groups.setdefault(key, {"rows": [], "amounts": [], "sum": Decimal(0)})
        g["rows"].append(num)
        g["amounts"].append(amount)
        g["sum"] += amount
    return {
        "header": header,
        "line_count": len(rows),
        "total": total,
        "groups": groups,
        "no_key": no_key,
        "bad_amount": bad_amount,
    }


def flags_for(ga, gb) -> list[str]:
    flags = []
    if ga and len(ga["rows"]) > 1:
        flags.append("many_lines_a")
    if gb and len(gb["rows"]) > 1:
        flags.append("many_lines_b")
    if any(x < 0 for g in (ga, gb) if g for x in g["amounts"]):
        flags.append("negative_amount")
    if ga and gb and ga["sum"] != gb["sum"] and ga["sum"] != 0 and gb["sum"] != 0:
        if (ga["sum"] > 0) == (gb["sum"] > 0) and abs(gb["sum"]) < abs(ga["sum"]):
            flags.append("b_smaller")
        elif (ga["sum"] > 0) == (gb["sum"] > 0):
            flags.append("a_smaller")
    return flags


def compare(a: dict, b: dict) -> dict:
    tables = {"matched": [], "only_a": [], "only_b": [], "amount_differs": []}
    keys = list(a["groups"].keys()) + [k for k in b["groups"] if k not in a["groups"]]
    for key in keys:
        ga, gb = a["groups"].get(key), b["groups"].get(key)
        row = {
            "key": key,
            "rows_a": ga["rows"] if ga else [],
            "rows_b": gb["rows"] if gb else [],
            "sum_a": ga["sum"] if ga else None,
            "sum_b": gb["sum"] if gb else None,
            "difference": (ga["sum"] if ga else Decimal(0)) - (gb["sum"] if gb else Decimal(0)),
            "flags": flags_for(ga, gb),
        }
        if ga and gb:
            tables["matched" if ga["sum"] == gb["sum"] else "amount_differs"].append(row)
        elif ga:
            tables["only_a"].append(row)
        else:
            tables["only_b"].append(row)
    return tables


def check_totals(a: dict, b: dict, tables: dict) -> dict:
    """Prove every line landed in exactly one place, and the sums agree."""
    lines_a = sum(len(r["rows_a"]) for t in tables.values() for r in t) + len(a["no_key"]) + len(a["bad_amount"])
    lines_b = sum(len(r["rows_b"]) for t in tables.values() for r in t) + len(b["no_key"]) + len(b["bad_amount"])
    sum_a = sum((r["sum_a"] for t in tables.values() for r in t if r["sum_a"] is not None), Decimal(0))
    sum_a += sum((x["amount"] for x in a["no_key"]), Decimal(0))
    sum_b = sum((r["sum_b"] for t in tables.values() for r in t if r["sum_b"] is not None), Decimal(0))
    sum_b += sum((x["amount"] for x in b["no_key"]), Decimal(0))
    return {
        "lines_a_ok": lines_a == a["line_count"],
        "lines_b_ok": lines_b == b["line_count"],
        "total_a_ok": sum_a == a["total"],
        "total_b_ok": sum_b == b["total"],
    }


# --------------------------------------------------------------------------- writing

SHEETS = [
    ("matched", "Matched"),
    ("only_a", "Only in A"),
    ("only_b", "Only in B"),
    ("amount_differs", "Amount differs"),
]
COLUMNS = ["key", "sum_a", "sum_b", "difference", "rows_a", "rows_b", "flags"]


def _cell(v):
    if isinstance(v, Decimal):
        return float(v) if openpyxl else str(v)
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return v


def write_results(out: Path, summary: dict, tables: dict, a: dict, b: dict) -> list[str]:
    out.parent.mkdir(parents=True, exist_ok=True)
    extra = {
        "no_key_a": [{"row": x["row"], "amount": x["amount"]} for x in a["no_key"]],
        "no_key_b": [{"row": x["row"], "amount": x["amount"]} for x in b["no_key"]],
        "bad_amount_a": a["bad_amount"],
        "bad_amount_b": b["bad_amount"],
    }
    if openpyxl is not None and out.suffix.lower() == ".xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Summary"
        for k, v in _flatten(summary):
            ws.append([k, _cell(v)])
        for key, title in SHEETS:
            s = wb.create_sheet(title)
            s.append(COLUMNS)
            for r in tables[key]:
                s.append([_cell(r[c]) for c in COLUMNS])
        for key, items in extra.items():
            if items:
                s = wb.create_sheet(key)
                cols = list(items[0].keys())
                s.append(cols)
                for it in items:
                    s.append([_cell(it[c]) for c in cols])
        wb.save(out)
        return [str(out)]
    # CSV fallback: one file per table, next to the requested name.
    base = out.with_suffix("")
    written = []
    for key, _ in SHEETS:
        p = Path(f"{base}-{key}.csv")
        with p.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(COLUMNS)
            for r in tables[key]:
                w.writerow([_cell(r[c]) for c in COLUMNS])
        written.append(str(p))
    p = Path(f"{base}-summary.json")
    p.write_text(json.dumps({**summary, **extra}, default=str, indent=2, ensure_ascii=False))
    written.append(str(p))
    return written


def _flatten(d, prefix=""):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from _flatten(v, f"{prefix}{k}.")
        else:
            yield f"{prefix}{k}", v


# --------------------------------------------------------------------------- commands


def cmd_peek(args) -> dict:
    header, rows = read_table(Path(args.file), args.sheet)
    return {
        "file": args.file,
        "columns": header,
        "line_count": len(rows),
        "first_rows": [[_cell(c) if not isinstance(c, Decimal) else str(c) for c in r] for _, r in rows[: args.rows]],
    }


def cmd_compare(args) -> dict:
    a = load_side(args.a, args.sheet_a, args.key_a, args.amount_a, args.decimal)
    b = load_side(args.b, args.sheet_b, args.key_b or args.key_a, args.amount_b or args.amount_a, args.decimal)
    tables = compare(a, b)
    keys_total = sum(len(t) for t in tables.values())
    match_rate = (len(tables["matched"]) + len(tables["amount_differs"])) / keys_total if keys_total else 0.0
    flag_counts: dict[str, int] = {}
    for t in tables.values():
        for r in t:
            for fl in r["flags"]:
                flag_counts[fl] = flag_counts.get(fl, 0) + 1
    summary = {
        "file_a": {"path": args.a, "lines": a["line_count"], "total": a["total"],
                   "no_key_lines": len(a["no_key"]), "bad_amount_lines": len(a["bad_amount"])},
        "file_b": {"path": args.b, "lines": b["line_count"], "total": b["total"],
                   "no_key_lines": len(b["no_key"]), "bad_amount_lines": len(b["bad_amount"])},
        "tables": {k: {"keys": len(v),
                       "sum_a": sum((r["sum_a"] for r in v if r["sum_a"] is not None), Decimal(0)),
                       "sum_b": sum((r["sum_b"] for r in v if r["sum_b"] is not None), Decimal(0))}
                   for k, v in tables.items()},
        "flags": flag_counts,
        "key_match_rate": round(match_rate, 4),
        "low_match": match_rate < 0.5,
        "checks": check_totals(a, b, tables),
    }
    summary["checks"]["all_ok"] = all(summary["checks"].values()) and not a["bad_amount"] and not b["bad_amount"]
    summary["written"] = write_results(Path(args.out), summary, tables, a, b)
    return summary


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pk = sub.add_parser("peek", help="show the columns and the first rows of a file")
    pk.add_argument("file")
    pk.add_argument("--sheet")
    pk.add_argument("--rows", type=int, default=5)

    c = sub.add_parser("compare", help="compare two files")
    c.add_argument("--a", required=True, help="file A, such as the product export")
    c.add_argument("--b", required=True, help="file B, such as the accounting file")
    c.add_argument("--key-a", required=True, help="link column in file A")
    c.add_argument("--key-b", help="link column in file B (default: same as A)")
    c.add_argument("--amount-a", required=True, help="amount column in file A")
    c.add_argument("--amount-b", help="amount column in file B (default: same as A)")
    c.add_argument("--sheet-a")
    c.add_argument("--sheet-b")
    c.add_argument("--decimal", choices=["auto", ".", ","], default="auto",
                   help="decimal mark in text numbers (default: auto)")
    c.add_argument("--out", required=True, help="result file, .xlsx (or a base name for CSV files)")

    args = p.parse_args(argv)
    try:
        result = cmd_peek(args) if args.cmd == "peek" else cmd_compare(args)
    except InputError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, default=str, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
