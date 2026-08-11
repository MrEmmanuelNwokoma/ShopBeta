CATEGORIES = [
    {"name": "Smartphone"},
    {"name": "Laptop"},
    # {"name": "Tablet"},
    # {"name": "SmartWatch"},
    # {"name": "Headphones"},
    # {"name": "Speakers"},
    # {"name": "Monitor"},
    # {"name": "Gaming console"}
]

STORES = [
    {
        "name": "Jumia",
        "website_url": "https://www.jumia.com",
        "is_active": True,
        "supports_api": False
    },
    {
        "name": "Slot",
        "website_url": "https://slot.ng",
        "is_active": True,
        "supports_api": False
    },
    {
        "name": "Konga",
        "website_url": "https://www.konga.com",
        "is_active": False,
        "supports_api": False
    }
]

# PRODUCTS = [
#     {
#         "name": "Redmi 15c",
    
#         "category": "Smartphone"
#     },
#     {
#         "name": "Redmi 12c",


#         "category": "Smartphone"
#     },
#     {
#         "name": "Redmi 13c",
   
#         "category": "Smartphone"
#     }

# ]

ADMIN_USERS = [
    {
        "first_name": "Emmanuel",
        "last_name": "Nwokoma",
        "phone_number": "09038457340",
        "email": "emmanuelnwokoma364@gmail.com",
        "password": "strings"
    },
     {
        "first_name": "Olamide",
        "last_name": "Bello",
        "phone_number": "0987766554",
        "email": "belkid98@gmail.com",
        "password": "strings"
    },
     {
        "first_name": "Miracle",
        "last_name": "Nwokoma",
        "phone_number": "09038457341",
        "email": "emmanuelnwokoma324@gmail.com",
        "password": "strings"
    }
]
CANONICAL_BRANDS = [
    # Smartphones
    {"name": "apple"},
    {"name": "archos"},
    {"name": "asus"},
    {"name": "atouch"},
    {"name": "blackberry"},
    {"name": "blackview"},
    {"name": "cubot"},
    {"name": "doogee"},
    {"name": "fossibot"},
    {"name": "freeyond"},
    {"name": "gionee"},
    {"name": "google"},
    {"name": "hmd"},
    {"name": "honor"},
    {"name": "huawei"},
    {"name": "infinix"},
    {"name": "innjoo"},
    {"name": "itel"},
    {"name": "lenovo"},
    {"name": "lg"},
    {"name": "meizu"},
    {"name": "microsoft"},
    {"name": "motorola"},
    {"name": "nokia"},
    {"name": "nothing"},
    {"name": "nubia"},
    {"name": "oneplus"},
    {"name": "oppo"},
    {"name": "oukitel"},
    {"name": "philips"},
    {"name": "poco"},
    {"name": "realme"},
    {"name": "redmi"},
    {"name": "samsung"},
    {"name": "tecno"},
    {"name": "umidigi"},
    {"name": "vivo"},
    {"name": "xiaomi"},
    {"name": "zte"},

    # Laptops
    {"name": "acer"},
    {"name": "alienware"},
    {"name": "dell"},
    {"name": "fujitsu"},
    {"name": "hp"},
    {"name": "msi"},
    {"name": "razer"},
    {"name": "toshiba"},
    {"name": "zinox"},

    # Audio
    {"name": "bose"},
    {"name": "jbl"},
    {"name": "oraimo"},
    {"name": "sony"},
    {"name": "sennheiser"},
    {"name": "anker"},
]
BRAND_SIGNALS = [
    {
        "brand": "apple",
        "signals": [
            "iphone",
            "ipad",
            "macbook",
            "imac",
            "airpods",
            "homepod",
        ],
    },
    {
        "brand": "samsung",
        "signals": [
            "galaxy",
            "galaxybook",
            "galaxywatch",
            "galaxybuds",
        ],
    },
    {
        "brand": "infinix",
        "signals": [
            "hot",
            "note",
            "zero",
            "smart",
            "gt",
            "xpad",
            "xbook",
        ],
    },
    {
        "brand": "tecno",
        "signals": [
            "camon",
            "spark",
            "phantom",
            "pop",
            "megabook",
            "megapad",
        ],
    },
    {
        "brand": "xiaomi",
        "signals": [
            "redmi",
            "mix",
            "miwatch",
            "miband",
        ],
    },
    {
        "brand": "poco",
        "signals": [
            "poco",
        ],
    },
    {
        "brand": "oppo",
        "signals": [
            "reno",
            "find",
        ],
    },
    {
        "brand": "vivo",
        "signals": [
            "iqoo",
        ],
    },
    {
        "brand": "oneplus",
        "signals": [
            "nord",
            "ace",
        ],
    },
    {
        "brand": "realme",
        "signals": [
            "narzo",
        ],
    },
    {
        "brand": "google",
        "signals": [
            "pixel",
            "nest",
            "chromecast",
        ],
    },
    {
        "brand": "huawei",
        "signals": [
            "matebook",
            "nova",
            "freebuds",
            "watchgt",
        ],
    },
    {
        "brand": "honor",
        "signals": [
            "magicbook",
            "magic",
        ],
    },
    {
        "brand": "motorola",
        "signals": [
            "moto",
            "razr",
        ],
    },
    {
        "brand": "nokia",
        "signals": [
            "lumia",
        ],
    },
    {
        "brand": "nothing",
        "signals": [
            "cmf",
        ],
    },
    {
        "brand": "sony",
        "signals": [
            "xperia",
            "bravia",
            "playstation",
        ],
    },
    {
        "brand": "lg",
        "signals": [
            "gram",
            "ultragear",
        ],
    },
    {
        "brand": "asus",
        "signals": [
            "zenfone",
            "zenbook",
            "vivobook",
            "rog",
            "tuf",
        ],
    },
    {
        "brand": "lenovo",
        "signals": [
            "thinkpad",
            "ideapad",
            "legion",
            "yoga",
            "thinkbook",
        ],
    },
    {
        "brand": "hp",
        "signals": [
            "hewlett",
            "pavilion",
            "envy",
            "spectre",
            "elitebook",
            "probook",
            "omen",
            "victus",
        ],
    },
    {
        "brand": "dell",
        "signals": [
            "inspiron",
            "latitude",
            "xps",
            "alienware",
            "precision",
            "vostro",
        ],
    },
    {
        "brand": "acer",
        "signals": [
            "aspire",
            "swift",
            "nitro",
            "predator",
        ],
    },
    {
        "brand": "microsoft",
        "signals": [
            "surface",
            "xbox",
        ],
    },
    {
        "brand": "amazon",
        "signals": [
            "kindle",
            "echo",
            "alexa",
        ],
    },
    {
        "brand": "umidigi",
        "signals": [
            "bison",
        ],
    },
]