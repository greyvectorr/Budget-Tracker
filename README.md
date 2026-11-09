# 💰 Budget Tracker

A command-line program for tracking monthly income and expenses. Add your income sources and expenses, then pull up a clean summary showing exactly where your money stands — total income, total expenses, and net income.

Built with core Python only: no external libraries, no setup beyond having Python installed.

---

## 📖 Overview

Managing money starts with knowing what comes in and what goes out. Budget Tracker gives you a simple, menu-driven way to record both and see the bottom line at a glance.

Your entries are saved automatically to a local JSON file after every change, so your budget is still there the next time you open the program.

---

## ✨ Features

- **Add Income** — record a source of income and the amount it yields per month
- **Add Expense** — record an expense and what it costs per month
- **View Budget Summary** — see every income and expense entry, plus total income, total expenses, and net income, with a plain-English verdict (surplus, deficit, or break-even)
- **Exit** — close the program cleanly
- **Automatic saving** — data is written to disk after every change, so nothing is lost if the program closes unexpectedly
- **Input validation** — blank names, non-numeric amounts, zero, and negative values are all rejected with a clear message, and you're asked again instead of the program crashing
- **Friendly number handling** — amounts like `1,500` work as well as `1500`, and output is formatted with thousands separators (`$1,900.50`)

---

## 🧰 Requirements

- Python 3.6 or later
- No third-party packages — standard library only (`json`, `math`, `os`)

---

## 🚀 Getting Started

Clone the repository and run the script:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
python budget_tracker.py
```

On some systems you may need to use `python3` instead of `python`.

---

## 🖥️ Usage

When the program starts, you'll see a numbered menu:

```
===== BUDGET TRACKER =====
1. Add Income
2. Add Expense
3. View Budget Summary
4. Exit
Enter your choice (1-4):
```

Type a number and press Enter.

### Example session

```
Welcome to Budget Tracker!

===== BUDGET TRACKER =====
1. Add Income
2. Add Expense
3. View Budget Summary
4. Exit
Enter your choice (1-4): 1
Enter the name of the income: Salary
Enter the monthly amount of this income: $1,500
  Added income: Salary ($1,500.00 per month)

===== BUDGET TRACKER =====
1. Add Income
2. Add Expense
3. View Budget Summary
4. Exit
Enter your choice (1-4): 1
Enter the name of the income: Freelance
Enter the monthly amount of this income: $400.5
  Added income: Freelance ($400.50 per month)

===== BUDGET TRACKER =====
1. Add Income
2. Add Expense
3. View Budget Summary
4. Exit
Enter your choice (1-4): 2
Enter the name of the expense: Rent
Enter the monthly amount of this expense: $600
  Added expense: Rent ($600.00 per month)

===== BUDGET TRACKER =====
1. Add Income
2. Add Expense
3. View Budget Summary
4. Exit
Enter your choice (1-4): 2
Enter the name of the expense: Food
Enter the monthly amount of this expense: $250.75
  Added expense: Food ($250.75 per month)

===== BUDGET TRACKER =====
1. Add Income
2. Add Expense
3. View Budget Summary
4. Exit
Enter your choice (1-4): 3

========== BUDGET SUMMARY ==========

INCOME
----------------------------------------
  Salary                   $    1,500.00
  Freelance                $      400.50

EXPENSES
----------------------------------------
  Rent                     $      600.00
  Food                     $      250.75

========================================
  Total Income             $    1,900.50
  Total Expenses           $      850.75
  Net Income               $    1,049.75
========================================
You're spending less than you earn. Nice work!

===== BUDGET TRACKER =====
1. Add Income
2. Add Expense
3. View Budget Summary
4. Exit
Enter your choice (1-4): 4
Goodbye! Your budget has been saved.
```

If your expenses exceed your income, the net income shows as negative and the program warns you: `Warning: you're spending more than you earn.`

### Input validation

The program keeps asking until it gets something valid:

| You enter | What happens |
|---|---|
| A blank name | `Name cannot be empty. Please try again.` |
| Text instead of a number (e.g. `abc`) | `That isn't a number. Please enter something like 2500 or 2500.50.` |
| `0` or a negative number | `The amount must be greater than zero.` |
| `nan` or `inf` | `That isn't a valid amount. Please try again.` |
| A menu choice other than 1–4 | `Invalid choice. Please enter 1, 2, 3, or 4.` |

---

## 💾 How Your Data Is Stored

Entries are saved to `budget_data.json`, created automatically in the same folder as the script the first time you add an entry. It looks like this:

```json
{
  "incomes": [
    { "name": "Salary", "amount": 1500.0 },
    { "name": "Freelance", "amount": 400.5 }
  ],
  "expenses": [
    { "name": "Rent", "amount": 600.0 },
    { "name": "Food", "amount": 250.75 }
  ]
}
```

- To **start fresh**, delete `budget_data.json`.
- If the file is missing or damaged, the program simply starts with an empty budget instead of crashing.

> **Tip:** this file contains your personal financial data, so add `budget_data.json` to your `.gitignore` before pushing to GitHub.

---

## 🗂️ Project Structure

```
.
├── budget_tracker.py    # The entire program
├── README.md            # You are here
└── budget_data.json     # Created automatically on first save (DO NOT COMMIT)
```

---

## 🧠 How It Works

The program is a handful of small functions, each with one job:

| Function | Responsibility |
|---|---|
| `load_data()` / `save_data()` | Read and write the JSON data file |
| `get_name()` / `get_amount()` | Prompt repeatedly until the input is valid |
| `add_entry()` | Add an income or expense — one function serves both menu options |
| `print_menu()` | Display the menu |
| `print_section()` | Print one block of the summary (all incomes or all expenses) |
| `view_summary()` | Calculate totals and net income, then print the full report |
| `main()` | Run the menu loop until the user exits |

### Python concepts demonstrated

- **Functions** — small, single-purpose, reusable (e.g. `add_entry` handles both income and expenses via one `kind` argument)
- **Lists and dictionaries** — each entry is a dictionary stored in a list, which maps directly onto JSON
- **Loops and conditionals** — the menu loop and the validation loops
- **Exception handling** — `try`/`except` around number parsing, file loading, and `Ctrl+C` / `Ctrl+D`
- **File handling** — reading and writing JSON with the `json` module
- **String formatting** — f-strings with alignment and thousands separators (`{amount:>12,.2f}`)

### Design decisions

- **Saving after every change** rather than only on exit, so a crash or `Ctrl+C` can't lose data.
- **Amounts rounded to 2 decimal places** with `round()`. This is fine at this scale; a production finance system would use Python's `decimal.Decimal` to avoid binary floating-point rounding errors.
- **`nan` and `inf` explicitly rejected**, because Python's `float()` accepts both without complaint.
- **A damaged data file never blocks startup** — the program falls back to an empty budget.

---

## 🔧 Customization

**Change the currency symbol** — edit this line near the top of `budget_tracker.py`:

```python
CURRENCY = "$"   # change to "₦", "£", "€", etc.
```

Some Windows terminals can't display certain symbols (such as `₦`) by default. If you see garbled output, try a different terminal or keep a symbol your terminal supports.

---

## 🚧 Possible Improvements

Ideas for extending the project:

- Delete or edit existing entries
- Categorize expenses (food, transport, rent) and show a breakdown by category
- Track entries by month, not just a single running budget
- Show savings rate as a percentage of income
- Export the summary to a CSV file
- Use `decimal.Decimal` for exact money arithmetic

---

## 📄 License

Copyright (c) 2026 GreyVectorr

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.