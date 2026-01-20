# gpt.py
"""OpenAI GPT integration for receipt information extraction."""

import json
from openai import OpenAI

client = OpenAI()

CATEGORIES = ["Meals", "Transport", "Lodging", "Office Supplies",
"Entertainment", "Other"]


def extract_receipt_info(image_b64):
    """Extract structured information from a receipt image using GPT-4.1-mini.

    Sends the base64-encoded image to OpenAI's API and requests extraction
    of date, amount, vendor, and category fields.

    Args:
        image_b64: A base64-encoded string of the receipt image.

    Returns:
        A dictionary containing the extracted fields:
            - date: The receipt date as a string, or None if not found.
            - amount: The total amount paid as a string.
            - vendor: The merchant or vendor name, or None if not found.
            - category: One of the predefined categories (Meals, Transport,
              Lodging, Office Supplies, Entertainment, Other).
    """
    prompt = f"""
You are an information extraction system.
Extract ONLY the following fields from the receipt image:

date: the receipt date as a string
amount: the total amount paid as it appears on the receipt
vendor: the merchant or vendor name
category: one of [{", ".join(CATEGORIES)}]

Return EXACTLY one JSON object with these four keys and NOTHING ELSE.
Do not include explanations, comments, or formatting.
Do not wrap the JSON in markdown.
If a field cannot be determined, use null.

The output must be valid JSON.
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        seed=43,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ]
    )
    return json.loads(response.choices[0].message.content)

