import time
import random
import json
import re
from google import genai
from google.genai import types, errors
from src.core.pydantic_configuration import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

RETRYABLE_CODES = {500, 503, 504}
FALLBACK_MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite"]

PROMPT_TEMPLATE = """CRITICAL INSTRUCTIONS:
- Return ONLY a raw JSON array.
- Do NOT wrap the JSON in markdown code blocks (no ```json or ```).
- Do NOT include any introductory text, explanations, or conversational filler.
- The output must start with '[' and end with ']'.

You clean up messy, partially-processed product text from a \
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

Products:
{products}"""


def _generate_with_retry(contents, gen_config, models=FALLBACK_MODELS, max_attempts=4, base_delay=3):
    """Try each model in order; retry overload/server errors with backoff."""
    last_error = None

    for model in models:
        for attempt in range(1, max_attempts + 1):
            try:
                return client.models.generate_content(
                    model=model, contents=contents, config=gen_config
                )
            except errors.APIError as e:
                last_error = e

                if e.code == 429 and "PerDay" in str(e):
                    print(f"{model}: daily quota exhausted, trying next model")
                    break

                retryable = e.code in RETRYABLE_CODES or e.code == 429
                if not retryable:
                    raise

                if attempt == max_attempts:
                    print(f"{model}: still failing after {max_attempts} attempts, trying next model")
                    break

                delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
                print(f"{model}: error {e.code}, retry {attempt}/{max_attempts - 1} in {delay:.1f}s")
                time.sleep(delay)

    raise last_error


def _parse_json_array(raw_text: str, chunk_index: int):
    """Parse Gemini's response into a JSON array, tolerating markdown fences and trailing junk."""
    raw_text = raw_text.strip()

    # Strip markdown code blocks if the model included them
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)
        raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    # Fallback: slice out the first [...] block and try that
    start_idx = raw_text.find("[")
    end_idx = raw_text.rfind("]")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = raw_text[start_idx:end_idx + 1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

    print(f"Chunk {chunk_index}: failed to parse JSON. Raw text was:\n{raw_text[:500]}")
    raise ValueError(f"Chunk {chunk_index}: could not parse Gemini response as JSON")


async def clean_products(raw_products: list[dict]) -> list[dict]:
    results = []
    chunk_size = 50
    failed_chunks = []

    for i in range(0, len(raw_products), chunk_size):
        chunk = raw_products[i:i + chunk_size]
        product_names = [p["name"] for p in chunk]

        prompt = PROMPT_TEMPLATE.format(products=json.dumps(product_names, indent=2))

        try:
            response = _generate_with_retry(
                contents=prompt,
                gen_config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            enriched_chunk = _parse_json_array(response.text, chunk_index=i)
            results.extend(enriched_chunk)
        except Exception as e:
            print(f"Chunk {i}-{i + len(chunk)} failed: {type(e).__name__}: {e}")
            failed_chunks.append(chunk)

    if failed_chunks:
        print(f"{len(failed_chunks)} chunk(s) failed and were skipped ({sum(len(c) for c in failed_chunks)} products)")

    return results