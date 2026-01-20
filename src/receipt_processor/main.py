# main.py
"""Command-line interface for processing receipt images."""

import json
import argparse
from datetime import datetime
from . import file_io as io_mod
from . import gpt


def sanitize_amount(amount):
    """Clean and convert the amount field to a float.

    Removes currency symbols (like $) and converts the string to a float.
    This function handles inconsistent LLM output where amounts may include
    currency symbols or be returned as strings instead of numbers.

    Args:
        amount: The amount string from the receipt (e.g., "$43.83" or "70.74").

    Returns:
        The amount as a float, or None if the amount is invalid or missing.
    """
    if amount is None:
        return None
    # Remove $ symbol if present and convert to float
    cleaned = str(amount).replace("$", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return None


def process_directory(dirpath):
    """Process all receipt images in a directory and extract information.

    Args:
        dirpath: Path to the directory containing receipt images.

    Returns:
        A dictionary mapping each filename to its extracted receipt data.
    """
    results = {}
    for name, path in io_mod.list_files(dirpath):
        image_b64 = io_mod.encode_file(path)
        data = gpt.extract_receipt_info(image_b64)
        # Sanitize the amount field
        data["amount"] = sanitize_amount(data.get("amount"))
        results[name] = data
    return results


def parse_date(date_str):
    """Parse a date string in YYYY-MM-DD format.

    Args:
        date_str: A date string in YYYY-MM-DD format.

    Returns:
        A datetime object, or None if parsing fails.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def calculate_expenses(data, start_date, end_date):
    """Calculate total expenses within a date range.

    Args:
        data: Dictionary mapping filenames to receipt data.
        start_date: Start date string in YYYY-MM-DD format.
        end_date: End date string in YYYY-MM-DD format.

    Returns:
        Total expenses as a float.
    """
    start = parse_date(start_date)
    end = parse_date(end_date)

    if start is None or end is None:
        return 0.0

    total = 0.0
    for receipt in data.values():
        receipt_date = parse_date(receipt.get("date"))
        amount = receipt.get("amount")

        # Skip if date is invalid or outside range
        if receipt_date is None:
            continue
        if receipt_date < start or receipt_date > end:
            continue

        # Skip if amount is invalid
        if amount is None or not isinstance(amount, (int, float)):
            continue

        total += amount

    return total


def aggregate_by_category(data):
    """Aggregate expenses by category.

    Args:
        data: Dictionary mapping filenames to receipt data.

    Returns:
        A dictionary mapping category names to total amounts.
    """
    totals = {}
    for receipt in data.values():
        category = receipt.get("category", "Other")
        amount = receipt.get("amount")

        if amount is None or not isinstance(amount, (int, float)):
            continue

        if category not in totals:
            totals[category] = 0.0
        totals[category] += amount

    return totals


def plot_expenses_by_category(data, output_path="expenses_by_category.png"):
    """Generate a pie chart of expenses by category.

    Args:
        data: Dictionary mapping filenames to receipt data.
        output_path: Path to save the pie chart image.
    """
    import matplotlib.pyplot as plt

    totals = aggregate_by_category(data)

    if not totals:
        print("No valid data to plot.")
        return

    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.figure(figsize=(10, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title("Expenses by Category")
    plt.axis('equal')
    plt.savefig(output_path)
    plt.close()

    print(f"Pie chart saved to {output_path}")


def main():
    """Parse command-line arguments and run the receipt processor.

    Arguments:
        dirpath: Path to directory containing receipt images.
        --print: If provided, print the results as formatted JSON.
        --expenses: If provided with start and end dates (YYYY-MM-DD),
            calculate total expenses within that date range.
        --plot: If provided, generate a pie chart of expenses by category.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("--print", action="store_true")
    parser.add_argument("--expenses", nargs=2, metavar=("START", "END"),
                        help="Calculate expenses between START and END dates (YYYY-MM-DD)")
    parser.add_argument("--plot", action="store_true",
                        help="Generate a pie chart of expenses by category")
    args = parser.parse_args()

    data = process_directory(args.dirpath)

    if args.print:
        print(json.dumps(data, indent=2))

    if args.expenses:
        total = calculate_expenses(data, args.expenses[0], args.expenses[1])
        print(f"Total expenses from {args.expenses[0]} to {args.expenses[1]}: ${total:.2f}")

    if args.plot:
        plot_expenses_by_category(data)

if __name__ == "__main__":
    main()
