
import json
from google import genai
from google.genai import types
from src.core.pydantic_configuration import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

PROMPT_TEMPLATE = """You clean up messy, partially-processed product text from a \
Nigerian e-commerce price comparison pipeline. Input often \
still contains leftover junk: screen sizes, condition words ("renewed"), warranty \
mentions, colors, and inconsistent casing.

For each product, return:
- original_name: the exact text as given
- brand: manufacturer brand in lowercase (e.g. "samsung", "xiaomi", "hp"), or null if unclear
- model: clean model name without specs, colors, condition, or warranty noise \
(e.g. "galaxy a36", "redmi note 13 pro"), or null if the text has no real model in it
- ram: RAM in format "4GB", "8GB" etc, or null if not present
- storage: storage in format "128GB", "1TB" etc, or null if not present


Rules:
- The smaller RAM/storage number is RAM, the larger is storage, unless labeled.
- If the text is too vague to contain a real model (e.g. "smart", "phone month \
warranty", "smart unlike"), set model to null rather than inventing one.
- Never guess a brand or model you're not reasonably confident about — null is \
better than wrong.
- After cleaning, remove duplicates: if two products have same properties (original name, brand, model, ram and storage), keep only one of them.

Return ONLY a JSON array, no explanation, no markdown.

Products:
{products}"""


async def clean_products(raw_products: list[dict]) -> list[dict]:
    results = []
    chunk_size = 50

    for i in range(0, len(raw_products), chunk_size):
        chunk = raw_products[i:i + chunk_size]
        product_names = [p["name"] for p in chunk]

        prompt = PROMPT_TEMPLATE.format(products=json.dumps(product_names, indent=2))

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                # temperature=0,
                response_mime_type="application/json",
            ),
        )

        raw_text = response.text.strip()
        enriched_chunk = json.loads(raw_text)
        results.extend(enriched_chunk)

    return results


