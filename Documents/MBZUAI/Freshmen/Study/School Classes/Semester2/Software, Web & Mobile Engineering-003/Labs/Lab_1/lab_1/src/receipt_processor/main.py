# main.py
"""Command-line interface for processing receipt images."""

import json
import argparse
from . import file_io as io_mod
from . import gpt


def sanitize_amount(amount):
    """Clean and convert the amount field to a float.

    Removes currency symbols (like $) and converts the string to a float.

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


def main():
    """Parse command-line arguments and run the receipt processor.

    Arguments:
        dirpath: Path to directory containing receipt images.
        --print: If provided, print the results as formatted JSON.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()

    data = process_directory(args.dirpath)
    if args.print:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()

