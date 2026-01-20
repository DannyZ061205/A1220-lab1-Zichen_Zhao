run:
	python -m src.receipt_processor.main receipts --print

# Calculate expenses within a date range
expenses:
	python -m src.receipt_processor.main receipts --expenses 2025-01-01 2025-12-31

plot:
	python -m src.receipt_processor.main receipts --plot
