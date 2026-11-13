---
name: compare-lists
description: "Compares two lists line by line and explains every gap, with a script that does the matching and the sums. The main case is reconciling costs and revenue with accounting; it also fits two exports of master data or a stock count. Handles Excel and CSV, one-to-many lines, credit notes, duplicate keys and number formats like 1.234,56. Use when the user says 'reconcile', 'compare file A with file B', 'match these two lists', 'đối soát', 'đối chiếu chi phí doanh thu', 'so sánh hai file'."
---

# Compare two lists

Read [../core/reference/rules.md](../core/reference/rules.md) first.

This skill can move money decisions. A wrong number costs more than a bad sentence. Follow every
step. Never do the matching or the sums yourself: the script does them. You read long tables
badly. The script does not skip a row.

The script is [scripts/compare.py](scripts/compare.py). Run it with `python3`.

## Steps

1. Get the two files. File A is usually the product export. File B is usually the accounting
   file. Each one is `.xlsx`, `.xlsm` or `.csv`. Never change either file.
2. Check the tools. Run `python3 -c "import openpyxl"`.
   - If it fails and a file is `.xlsx`, run `pip install openpyxl`. If that fails too, ask the
     user to save each file as CSV, and stop until they do.
3. Peek at each file:

   ```bash
   python3 scripts/compare.py peek "<file A>" [--sheet "<sheet>"]
   python3 scripts/compare.py peek "<file B>"
   ```

   Use the full path of the script in this skill's folder.
4. Read `money.md` in the wiki, if it exists. It may name the link column, the amount column and
   the number format.
5. Show the user the columns and the first rows of each file. Propose:
   - the **link column** in each file: the column both files share, such as an invoice number;
   - the **amount column** in each file;
   - the **decimal mark** in text numbers: `.`, `,` or `auto`.
6. Wait for the user to confirm or correct. Do not compare before that.
7. Run the compare:

   ```bash
   python3 scripts/compare.py compare \
     --a "<file A>" --b "<file B>" \
     --key-a "<column>" --key-b "<column>" \
     --amount-a "<column>" --amount-b "<column>" \
     --decimal auto \
     --out "<output folder>/<YYYY-MM-DD>-compare.xlsx"
   ```

   Pick the output folder with [../core/reference/save-output.md](../core/reference/save-output.md).
8. Read the JSON the script prints. Check in this order:
   1. `error`: tell the user the message, and how to fix it.
   2. `low_match: true`: fewer than half the keys match. Stop. Show the user 5 keys from each
      file, and ask if the link column is right. Do not report gaps yet.
   3. `checks.all_ok: false`: tell the user which check failed. A `bad_amount` line holds text
      that is not a number. Show its row numbers.
9. Report to the user with the template below.
10. Offer an artifact for accounting or the manager. See
    [../core/reference/artifact.md](../core/reference/artifact.md). The `.xlsx` file is always
    the file version.
11. Offer to save the confirmed columns and the decimal mark to `money.md`, so the next compare
    skips step 5.
12. Add one `compare` line to `log.md`.

## Report template

Write it in the project language (rule 5).

```
Compared <file A> (<lines> lines, total <total>) with <file B> (<lines> lines, total <total>).

| Result | Keys | Sum A | Sum B |
|---|---|---|---|
| Matched | ... | ... | ... |
| Only in A | ... | ... | ... |
| Only in B | ... | ... | ... |
| Amount differs | ... | ... | ... |

Lines with no key: A <n>, B <n>.  Lines with a bad amount: A <n>, B <n>.
Special cases: <n> keys with many lines (one invoice, many orders), <n> with a negative amount (credit notes).

Biggest gaps:
1. <key>: A <sum>, B <sum>, difference <diff>. Cause: <only what the data shows, or "?">.
...

All lines counted, totals agree: <yes / no, and why>.
Result file: <path>
```

## Rules

- Copy every number from the script's JSON. Never round, never retype a sum from memory.
- Name a cause only when the data shows it, such as a negative line (a credit note) or a key on
  two lines. Otherwise write exactly "Cause: ?", in the project language, and nothing after it. Do not add "maybe" or
  "probably" guesses. The user knows the business; you do not.
- The flags `a_smaller` and `b_smaller` only say which side is bigger. They do not prove a part
  payment. Say "may be a part payment" at most.

## Done when

- The user confirmed the columns before the compare.
- `checks.all_ok` is true, or the user knows exactly which lines broke it.
- Every number in the report matches the script's JSON.
- The result file exists, and the user has its path.
