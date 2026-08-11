import re
from src.models.brand import Brand
from src.models. brand_signals import BrandSignal

# Words/patterns to always remove from model name
NOISE_WORDS = {
    "rom", "android", "os", "inch", "inches", "dual", "sim", "single",
    "black", "blue", "red", "white", "green", "gold", "silver", "grey",
    "gray", "purple", "pink", "yellow", "orange", "midnight", "starlight",
    "pro", "max", "plus", "ultra", "lite", "mini", "5g", "4g", "lte",
    "wifi", "bluetooth", "nfc", "with", "and", "the", "for", "–", "-",
    "new", "latest", "official", "original", "genuine"
}


NOISE_PATTERNS = [
    r'^\d+(\.\d+)?"$',      # screen size e.g. 6.7"
    r'^\d+(\.\d+)?inch$',   # e.g. 6.7inch
    r'^android\d+$',        # e.g. android14
    r'^\d+mp$',             # camera megapixels e.g. 64mp
    r'^\d+mah$',            # battery e.g. 5000mah
    r'^\d+w$',              # wattage e.g. 65w
    r'^\d+$',               # standalone numbers
]
patterns_to_remove = [
        r'\d+gb\s*[\/\+\,]\s*\d+(?:gb|tb)',          # 4gb/64gb, 4gb+128gb, 4gb,64gb
        r'\d+(?:gb|tb)\s*(?:ram|rom|storage|internal)', # 64gb ram, 128gb rom
        r'ram\s*[\/\+\,\s]\s*\d+(?:gb|tb)',            # ram/64gb, ram+128gb
        r'\d+(?:\.\d+)?\s*(?:inch|inches|")',           # 6.9", 6.9inch
        r'android\s*\d+',                               # android 14
        r'\d+\s*mp',                                    # 64mp
        r'\d+\s*mah',                                   # 5000mah
        r'\d+\s*w\b',                                   # 65w
        r'\d+\s*(?:gb|tb)',                             # standalone 64gb
        r'4g|5g|lte',                                   # network generation
        r'\b(?:black|blue|red|white|green|gold|silver|grey|gray|purple|pink|yellow|orange|midnight|starlight|titanium|graphite|cosmic)\b',  # colors
        r'\b(?:african|edition|version|series|gen)\b',  # edition tags
        r'\b(?:wireless|bluetooth|fm|torch|radio|camera|speaker|keypad|feature|button|small)\b',  # feature words
        r'[,_]',                                        # commas and underscores
        r'\s+',                                         # multiple spaces
    ]


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text

def identify_brand(
    raw_product: dict,
    brands: list[Brand],
    brand_signals: list[BrandSignal],
) -> Brand | None:

    product_words = set(
        normalize_text(raw_product["name"]).split()
    )
    
    # Build a lookup dict once
    brand_by_id = {brand.id: brand for brand in brands}

    # 1. Try canonical brands
    for brand in brands:
        if brand.name in product_words:
            return brand

    # 2. Try brand signals
    for brand_signal in brand_signals:
        if brand_signal.signal in product_words:
            return brand_by_id.get(brand_signal.brand_id)

    return None


def extract_ram(raw_product: dict) -> str | None:
    product_name = raw_product.get("name", "")

    # Matches: 4GB RAM, 4GBRAM, 4GB/64GB (first value), ram/64gb
    match = re.search(
        r"\b(\d+)\s*GB\s*(?:RAM|\/|\+|ram)|\bram[\/\s](\d+)\s*GB\b",
        product_name,
        re.IGNORECASE,
    )

    if not match:
        return None

    value = match.group(1) or match.group(2)
    return f"{value}GB"


def extract_storage(raw_product: dict) -> str | None:
    product_name = raw_product.get("name", "")

    # Matches: 64GB ROM, 64GB storage, second value in 4GB/64GB or 4GB+64GB
    match = re.search(
        r"\b(\d+)\s*GB\s*(?:ROM|storage|internal)\b"
        r"|\b\d+\s*GB\s*[\/\+]\s*(\d+)\s*(GB|TB)\b"
        r"|\b(\d+)\s*(TB)\b",
        product_name,
        re.IGNORECASE,
    )

    if not match:
        return None

    if match.group(1):
        return f"{match.group(1)}GB"
    elif match.group(2):
        return f"{match.group(2)}{match.group(3).upper()}"
    elif match.group(4):
        return f"{match.group(4)}{match.group(5).upper()}"
    
    return None


def extract_model(
    raw_product: dict,
    brand: Brand,
    ram: str | None,
    storage: str | None,
) -> str | None:

    product_name = normalize_text(raw_product.get("name", ""))

    if not product_name:
        return None

    # Pre-clean entire spec patterns
    

    for pattern in patterns_to_remove:
        product_name = re.sub(pattern, ' ', product_name, flags=re.IGNORECASE)

    product_name = product_name.strip()

    words = product_name.split()

    # Remove brand name
    words = [w for w in words if w.lower() != brand.name.lower()]

    # Remove noise words
    words = [w for w in words if w.lower() not in NOISE_WORDS]

    # Remove standalone numbers and single characters
    words = [w for w in words if not re.match(r'^\d+$', w) and len(w) > 1]

    if not words:
        return None

    return " ".join(words)


def build_product_signature(model: str, ram: str | None, storage: str | None) -> str:
    parts = [model]
    if ram:
        parts.append(ram)
    if storage:
        parts.append(storage)
    return " ".join(parts).lower()