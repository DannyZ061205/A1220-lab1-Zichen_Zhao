# Receipt Processor

A command-line application that processes receipt images using OpenAI's GPT-4.1-mini to extract structured information.

## Features

- Extracts date, amount, vendor name, and category from receipt images
- Outputs results as JSON

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
