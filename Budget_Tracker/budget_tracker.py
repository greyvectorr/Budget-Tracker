"""
Budget Tracker
--------------
A simple command-line program for tracking monthly income and expenses.

Features:
    1. Add Income          - record a source of income and its monthly amount
    2. Add Expense         - record an expense and its monthly cost
    3. View Budget Summary - see every entry, the totals, and the net income
    4. Exit

Your entries are saved to a small JSON file after every change, so they are
still there the next time you run the program.
"""

import json
import math
import os

# Change this to "₦", "£", "€", etc. to match your currency.
CURRENCY = "$"

# The data file lives next to this script, wherever you run it from.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget_data.json")


# ---------------------------------------------------------------------------
# Saving and loading
# ---------------------------------------------------------------------------

def load_data():
    """Load saved incomes and expenses. Returns two lists: (incomes, expenses).

    If the file doesn't exist yet (first run) or is damaged, we simply start
    with empty lists instead of crashing.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data["incomes"], data["expenses"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
        return [], []


def save_data(incomes, expenses):
    """Write both lists to the JSON data file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump({"incomes": incomes, "expenses": expenses}, file, indent=2)


# ---------------------------------------------------------------------------
# Input helpers - keep asking until the user gives us something valid
# ---------------------------------------------------------------------------

def get_name(prompt):
    """Ask for a name and keep asking until it isn't blank."""
    while True:
        name = input(prompt).strip()
        if name != "":
            return name
        print("  Name cannot be empty. Please try again.")


def get_amount(prompt):
    """Ask for a money amount and keep asking until it is a valid positive number."""
    while True:
        raw = input(prompt).strip()
        try:
            # Remove commas so "150,000" works as well as "150000".
            amount = float(raw.replace(",", ""))
        except ValueError:
            print("  That isn't a number. Please enter something like 2500 or 2500.50.")
            continue

        # float() happily accepts "nan" and "inf", so we check for those too.
        if not math.isfinite(amount):
            print("  That isn't a valid amount. Please try again.")
        elif amount <= 0:
            print("  The amount must be greater than zero.")
        else:
            return round(amount, 2)


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------

def print_menu():
    """Show the main menu."""
    print("\n===== BUDGET TRACKER =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Budget Summary")
    print("4. Exit")


def add_entry(entries, kind):
    """Ask for a name and monthly amount, then add it to `entries`.

    `kind` is the word "income" or "expense" - it's only used in the prompts,
    which lets one function handle both menu options.
    """
    name = get_name(f"Enter the name of the {kind}: ")
    amount = get_amount(f"Enter the monthly amount of this {kind}: {CURRENCY}")
    entries.append({"name": name, "amount": amount})
    print(f"  Added {kind}: {name} ({CURRENCY}{amount:,.2f} per month)")


def print_section(title, entries):
    """Print one section of the summary (all incomes, or all expenses)."""
    print(f"\n{title}")
    print("-" * 40)
    if len(entries) == 0:
        print("  (nothing recorded yet)")
    for item in entries:
        print(f"  {item['name']:<24} {CURRENCY}{item['amount']:>12,.2f}")


def view_summary(incomes, expenses):
    """Print the full budget report: every entry, the totals, and the net income."""
    total_income = sum(item["amount"] for item in incomes)
    total_expense = sum(item["amount"] for item in expenses)
    net_income = total_income - total_expense

    print("\n========== BUDGET SUMMARY ==========")
    print_section("INCOME", incomes)
    print_section("EXPENSES", expenses)

    print("\n" + "=" * 40)
    print(f"  {'Total Income':<24} {CURRENCY}{total_income:>12,.2f}")
    print(f"  {'Total Expenses':<24} {CURRENCY}{total_expense:>12,.2f}")
    print(f"  {'Net Income':<24} {CURRENCY}{net_income:>12,.2f}")
    print("=" * 40)

    if net_income > 0:
        print("You're spending less than you earn. Nice work!")
    elif net_income < 0:
        print("Warning: you're spending more than you earn.")
    else:
        print("You're breaking even: income equals expenses.")


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main():
    """Run the menu loop until the user chooses Exit."""
    incomes, expenses = load_data()
    print("Welcome to Budget Tracker!")

    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_entry(incomes, "income")
            save_data(incomes, expenses)
        elif choice == "2":
            add_entry(expenses, "expense")
            save_data(incomes, expenses)
        elif choice == "3":
            view_summary(incomes, expenses)
        elif choice == "4":
            print("Goodbye! Your budget has been saved.")
            break
        else:
            print("  Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or Ctrl+D - exit politely. Nothing is lost, because data
        # is saved right after every change.
        print("\nProgram closed. Your saved data is safe. Goodbye!")
