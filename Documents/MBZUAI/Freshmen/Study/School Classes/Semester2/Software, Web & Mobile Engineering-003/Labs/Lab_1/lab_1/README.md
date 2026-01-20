# Receipt Processor

A command-line application that processes receipt images using OpenAI's GPT-4.1-mini to extract structured information.

## Features

- Extracts date, amount, vendor name, and category from receipt images
- Outputs results as JSON
- Generates pie chart visualization of expenses by category

## Visualization

The `--plot` option generates a pie chart showing expenses grouped by category. I chose a pie chart because:

1. **Intuitive representation**: Pie charts clearly show the proportion of each category relative to the total
2. **Easy comparison**: Users can quickly see which categories consume the most budget
3. **Familiar format**: Most users are familiar with pie charts for expense breakdowns

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-api-key
   ```

## Usage

Run with make:
```bash
make run
```

Or run directly:
```bash
python -m src.receipt_processor.main receipts --print
```
