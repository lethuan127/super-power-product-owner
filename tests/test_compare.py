"""Unit tests for skills/compare-lists/scripts/compare.py.

Run from the repo root:  python3 -m unittest discover -s tests -t .
"""

import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/compare-lists/scripts/compare.py"
spec = importlib.util.spec_from_file_location("compare", SCRIPT)
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)


class ParseAmount(unittest.TestCase):
    def test_formats(self):
        cases = {
            "1,234.56": Decimal("1234.56"),
            "1.234,56": Decimal("1234.56"),
            "1 234,56": Decimal("1234.56"),
            "1.234.567": Decimal("1234567"),
            "1,234,567": Decimal("1234567"),
            "12,5": Decimal("12.5"),
            "0.250": Decimal("0.250"),
            "(500)": Decimal("-500"),
            "500-": Decimal("-500"),
            "-1.000": Decimal("-1000"),
            "₫ 2.000.000": Decimal("2000000"),
            "$1,000.00": Decimal("1000.00"),
            150: Decimal("150"),
            150.5: Decimal("150.5"),
        }
        for raw, want in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(compare.parse_amount(raw), want)

    def test_empty_and_bad(self):
        self.assertIsNone(compare.parse_amount(None))
        self.assertIsNone(compare.parse_amount(""))
        self.assertIsNone(compare.parse_amount("-"))
        with self.assertRaises(ValueError):
            compare.parse_amount("abc")

    def test_forced_decimal_mark(self):
        self.assertEqual(compare.parse_amount("1.234", ","), Decimal("1234"))
        self.assertEqual(compare.parse_amount("1.234", "."), Decimal("1.234"))

    def test_key(self):
        self.assertEqual(compare.normalize_key(" inv-01 "), "INV-01")
        self.assertEqual(compare.normalize_key(1001.0), "1001")
        self.assertEqual(compare.normalize_key(None), "")


class Compare(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def write(self, name, text):
        p = self.tmp / name
        p.write_text(text, encoding="utf-8")
        return str(p)

    def run_compare(self, a, b, **kw):
        out = self.tmp / "result.xlsx"
        argv = ["compare", "--a", a, "--b", b, "--key-a", kw.get("key_a", "Invoice"),
                "--amount-a", kw.get("amount_a", "Amount"), "--out", str(out)]
        if "key_b" in kw:
            argv += ["--key-b", kw["key_b"]]
        if "amount_b" in kw:
            argv += ["--amount-b", kw["amount_b"]]
        parser_args = self._parse(argv)
        return compare.cmd_compare(parser_args)

    @staticmethod
    def _parse(argv):
        import argparse
        p = argparse.ArgumentParser()
        sub = p.add_subparsers(dest="cmd")
        c = sub.add_parser("compare")
        for flag in ("--a", "--b", "--key-a", "--amount-a", "--out"):
            c.add_argument(flag, required=True)
        for flag in ("--key-b", "--amount-b", "--sheet-a", "--sheet-b"):
            c.add_argument(flag)
        c.add_argument("--decimal", default="auto")
        return p.parse_args(argv)

    def test_real_cases(self):
        a = self.write("orders.csv",
                       "Invoice,Order,Amount\n"
                       "INV-1,O-1,100\n"
                       "INV-2,O-2,200\n"
                       "INV-2,O-3,300\n"      # one invoice, two orders
                       "INV-3,O-4,1000\n"
                       "INV-4,O-5,50\n"        # only in A
                       ",O-6,7\n")             # no key
        b = self.write("accounting.csv",
                       "Invoice;Amount\n"
                       "inv-1;100\n"           # case differs, still matches
                       "INV-2;500\n"           # matches the sum of two lines
                       "INV-3;1.200\n"          # amount differs
                       "INV-3;-200\n"           # credit note -> sum 1000, matched
                       "INV-9;9\n")             # only in B
        s = self.run_compare(a, b)
        t = s["tables"]
        self.assertEqual(t["matched"]["keys"], 3)        # INV-1, INV-2, INV-3
        self.assertEqual(t["only_a"]["keys"], 1)         # INV-4
        self.assertEqual(t["only_b"]["keys"], 1)         # INV-9
        self.assertEqual(t["amount_differs"]["keys"], 0)
        self.assertEqual(s["file_a"]["total"], Decimal("1657"))
        self.assertEqual(s["file_b"]["total"], Decimal("1609"))
        self.assertEqual(s["file_a"]["no_key_lines"], 1)
        self.assertTrue(s["checks"]["all_ok"], s["checks"])
        self.assertEqual(s["flags"]["many_lines_a"], 1)
        self.assertEqual(s["flags"]["negative_amount"], 1)
        self.assertTrue(Path(s["written"][0]).exists())

    def test_amount_differs_and_low_match(self):
        a = self.write("a.csv", "Invoice,Amount\nX1,10\nX2,20\nX3,30\n")
        b = self.write("b.csv", "Ref,Total\nX1,10\nY2,20\nY3,30\n")
        s = self.run_compare(a, b, key_b="Ref", amount_b="Total")
        self.assertTrue(s["low_match"])
        a2 = self.write("a2.csv", "Invoice,Amount\nX1,10\nX2,20\n")
        b2 = self.write("b2.csv", "Invoice,Amount\nX1,10\nX2,15\n")
        s2 = self.run_compare(a2, b2)
        self.assertEqual(s2["tables"]["amount_differs"]["keys"], 1)
        self.assertFalse(s2["low_match"])

    def test_bad_amount_fails_all_ok(self):
        a = self.write("a.csv", "Invoice,Amount\nX1,ten\nX2,20\n")
        b = self.write("b.csv", "Invoice,Amount\nX2,20\n")
        s = self.run_compare(a, b)
        self.assertEqual(s["file_a"]["bad_amount_lines"], 1)
        self.assertFalse(s["checks"]["all_ok"])

    def test_wrong_column_is_input_error(self):
        a = self.write("a.csv", "Invoice,Amount\nX1,1\n")
        with self.assertRaises(compare.InputError):
            self.run_compare(a, a, key_a="Nope")

    @unittest.skipIf(compare.openpyxl is None, "openpyxl not installed")
    def test_xlsx_input(self):
        wb = compare.openpyxl.Workbook()
        ws = wb.active
        ws.append([])                       # empty first row is skipped
        ws.append(["Invoice", "Amount"])
        ws.append(["INV-1", 1500000])
        ws.append([1001, "2.000.000"])
        p = self.tmp / "a.xlsx"
        wb.save(p)
        b = self.write("b.csv", "Invoice,Amount\nINV-1,1500000\n1001,2000000\n")
        s = self.run_compare(str(p), b)
        self.assertEqual(s["tables"]["matched"]["keys"], 2)
        self.assertTrue(s["checks"]["all_ok"])

    def test_peek_cli(self):
        a = self.write("a.csv", "Invoice,Amount\n" + "".join(f"X{i},{i}\n" for i in range(10)))
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = compare.main(["peek", a, "--rows", "3"])
        self.assertEqual(code, 0)
        out = json.loads(buf.getvalue())
        self.assertEqual(out["columns"], ["Invoice", "Amount"])
        self.assertEqual(out["line_count"], 10)
        self.assertEqual(len(out["first_rows"]), 3)


if __name__ == "__main__":
    unittest.main()
