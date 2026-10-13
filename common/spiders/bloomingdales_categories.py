"""Bloomingdale's product-listing categories, grouped by department.

Every leaf is a crawlable ``/shop/<path>?id=<n>`` product-listing route on the
Bloomingdale's storefront. The Airflow DAG schedules one task per leaf and the
GCS output path uses the bare leaf name, so leaf keys are the full ``<path>``
slug below ``/shop`` (e.g. ``womens-apparel-dresses``) -- globally unique
across departments (no duplicate leaf keys, verified).

Captured 2026-10-14 from Bloomingdale's own catalog sitemap shard
``/dyn_img/sitemap/bcom_sitemap_cat_aa.xml.gz`` (linked from
``robots.txt`` -> ``bcom_sitemapindex.xml``) through the configured ScrapeOps
residential proxy: 3,305 unique product-listing routes across 677 navigation
roots (the 12 documented departments plus 665 brand/collection roots). The
module is pure data so the DAG factory can ``runpy`` it at parse time without
importing ``common.spiders``.
"""
from __future__ import annotations


BLOOMINGDALES_CATEGORIES: dict[str, dict[str, dict[str, str]]] = {
    '100-bloomingdales-fall-exclusives': {
        '100-bloomingdales-fall-exclusives': {
            "url": 'https://www.bloomingdales.com/shop/100-bloomingdales-fall-exclusives?id=1003375',
            "category": '100-bloomingdales-fall-exclusives',
            "department": '100-bloomingdales-fall-exclusives',
        },
        '100-bloomingdales-fall-exclusives-fine-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/100-bloomingdales-fall-exclusives/fine-jewelry?id=1003388',
            "category": '100-bloomingdales-fall-exclusives-fine-jewelry',
            "department": '100-bloomingdales-fall-exclusives',
        },
        '100-bloomingdales-fall-exclusives-kids': {
            "url": 'https://www.bloomingdales.com/shop/100-bloomingdales-fall-exclusives/kids?id=1003390',
            "category": '100-bloomingdales-fall-exclusives-kids',
            "department": '100-bloomingdales-fall-exclusives',
        },
    },
    '7-for-all-mankind': {
        '7-for-all-mankind': {
            "url": 'https://www.bloomingdales.com/shop/7-for-all-mankind?id=1292695',
            "category": '7-for-all-mankind',
            "department": '7-for-all-mankind',
        },
        '7-for-all-mankind-mens': {
            "url": 'https://www.bloomingdales.com/shop/7-for-all-mankind/mens?id=1292698',
            "category": '7-for-all-mankind-mens',
            "department": '7-for-all-mankind',
        },
        '7-for-all-mankind-womens': {
            "url": 'https://www.bloomingdales.com/shop/7-for-all-mankind/womens?id=1292697',
            "category": '7-for-all-mankind-womens',
            "department": '7-for-all-mankind',
        },
    },
    '90s-inspired-kick-it-old-school': {
        '90s-inspired-kick-it-old-school': {
            "url": 'https://www.bloomingdales.com/shop/90s-inspired-kick-it-old-school?id=1007560',
            "category": '90s-inspired-kick-it-old-school',
            "department": '90s-inspired-kick-it-old-school',
        },
    },
    'abercrombie-kids': {
        'abercrombie-kids': {
            "url": 'https://www.bloomingdales.com/shop/abercrombie-kids?id=1306224',
            "category": 'abercrombie-kids',
            "department": 'abercrombie-kids',
        },
    },
    'accessories': {
        'accessories': {
            "url": 'https://www.bloomingdales.com/shop/accessories?id=1323411',
            "category": 'accessories',
            "department": 'accessories',
        },
    },
    'accessories-mothers-day-gifts': {
        'accessories-mothers-day-gifts': {
            "url": 'https://www.bloomingdales.com/shop/accessories-mothers-day-gifts?id=1006719',
            "category": 'accessories-mothers-day-gifts',
            "department": 'accessories-mothers-day-gifts',
        },
    },
    'accessories-on-sale': {
        'accessories-on-sale': {
            "url": 'https://www.bloomingdales.com/shop/accessories-on-sale?id=1237661',
            "category": 'accessories-on-sale',
            "department": 'accessories-on-sale',
        },
    },
    'active-workout': {
        'active-workout': {
            "url": 'https://www.bloomingdales.com/shop/active-workout?id=1027026',
            "category": 'active-workout',
            "department": 'active-workout',
        },
    },
    'ag': {
        'ag': {
            "url": 'https://www.bloomingdales.com/shop/ag?id=1262304',
            "category": 'ag',
            "department": 'ag',
        },
        'ag-jeans': {
            "url": 'https://www.bloomingdales.com/shop/ag/jeans?id=1262401',
            "category": 'ag-jeans',
            "department": 'ag',
        },
        'ag-mens': {
            "url": 'https://www.bloomingdales.com/shop/ag/mens?id=1262305',
            "category": 'ag-mens',
            "department": 'ag',
        },
        'ag-mens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/ag/mens-jeans?id=1262400',
            "category": 'ag-mens-jeans',
            "department": 'ag',
        },
        'ag-sale': {
            "url": 'https://www.bloomingdales.com/shop/ag/sale?id=1262998',
            "category": 'ag-sale',
            "department": 'ag',
        },
        'ag-womens': {
            "url": 'https://www.bloomingdales.com/shop/ag/womens?id=1262306',
            "category": 'ag-womens',
            "department": 'ag',
        },
    },
    'agnostic-registry-homepage': {
        'agnostic-registry-homepage': {
            "url": 'https://www.bloomingdales.com/shop/agnostic-registry-homepage?id=1216665',
            "category": 'agnostic-registry-homepage',
            "department": 'agnostic-registry-homepage',
        },
    },
    'agolde': {
        'agolde': {
            "url": 'https://www.bloomingdales.com/shop/agolde?id=1263195',
            "category": 'agolde',
            "department": 'agolde',
        },
        'agolde-jeans': {
            "url": 'https://www.bloomingdales.com/shop/agolde/jeans?id=1263197',
            "category": 'agolde-jeans',
            "department": 'agolde',
        },
        'agolde-mens': {
            "url": 'https://www.bloomingdales.com/shop/agolde/mens?id=1263199',
            "category": 'agolde-mens',
            "department": 'agolde',
        },
        'agolde-mens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/agolde/mens-jeans?id=1263200',
            "category": 'agolde-mens-jeans',
            "department": 'agolde',
        },
        'agolde-sale': {
            "url": 'https://www.bloomingdales.com/shop/agolde/sale?id=1263201',
            "category": 'agolde-sale',
            "department": 'agolde',
        },
        'agolde-shorts': {
            "url": 'https://www.bloomingdales.com/shop/agolde/shorts?id=1263198',
            "category": 'agolde-shorts',
            "department": 'agolde',
        },
        'agolde-womens': {
            "url": 'https://www.bloomingdales.com/shop/agolde/womens?id=1263196',
            "category": 'agolde-womens',
            "department": 'agolde',
        },
    },
    'akro': {
        'akro': {
            "url": 'https://www.bloomingdales.com/shop/akro?id=1289218',
            "category": 'akro',
            "department": 'akro',
        },
    },
    'alexander-mcqueen': {
        'alexander-mcqueen': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen?id=1158260',
            "category": 'alexander-mcqueen',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-handbags': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/handbags?id=1233982',
            "category": 'alexander-mcqueen-handbags',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-men': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/men?id=1159159',
            "category": 'alexander-mcqueen-men',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-mens-bags-wallets': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/mens-bags-wallets?id=1158959',
            "category": 'alexander-mcqueen-mens-bags-wallets',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/mens-clothing?id=1326495',
            "category": 'alexander-mcqueen-mens-clothing',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-mens-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/mens-jewelry-accessories?id=1159360',
            "category": 'alexander-mcqueen-mens-jewelry-accessories',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/mens-shoes?id=1159359',
            "category": 'alexander-mcqueen-mens-shoes',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-sale': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/sale?id=1319525',
            "category": 'alexander-mcqueen-sale',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-shop-all-men': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/shop-all-men?id=1159059',
            "category": 'alexander-mcqueen-shop-all-men',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-women': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/women?id=1159160',
            "category": 'alexander-mcqueen-women',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-womens': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/womens?id=1159161',
            "category": 'alexander-mcqueen-womens',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-womens-acessories': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/womens-acessories?id=1159959',
            "category": 'alexander-mcqueen-womens-acessories',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/womens-clothing?id=1307498',
            "category": 'alexander-mcqueen-womens-clothing',
            "department": 'alexander-mcqueen',
        },
        'alexander-mcqueen-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/alexander-mcqueen/womens-shoes?id=1159259',
            "category": 'alexander-mcqueen-womens-shoes',
            "department": 'alexander-mcqueen',
        },
    },
    'alexis-bittar': {
        'alexis-bittar': {
            "url": 'https://www.bloomingdales.com/shop/alexis-bittar?id=1003990',
            "category": 'alexis-bittar',
            "department": 'alexis-bittar',
        },
    },
    'alice-olivia': {
        'alice-olivia': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia?id=1003978',
            "category": 'alice-olivia',
            "department": 'alice-olivia',
        },
        'alice-olivia-blazers': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia/blazers?id=1248701',
            "category": 'alice-olivia-blazers',
            "department": 'alice-olivia',
        },
        'alice-olivia-dresses': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia/dresses?id=1248696',
            "category": 'alice-olivia-dresses',
            "department": 'alice-olivia',
        },
        'alice-olivia-jeans': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia/jeans?id=1248698',
            "category": 'alice-olivia-jeans',
            "department": 'alice-olivia',
        },
        'alice-olivia-pants': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia/pants?id=1248700',
            "category": 'alice-olivia-pants',
            "department": 'alice-olivia',
        },
        'alice-olivia-sale': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia/sale?id=1248703',
            "category": 'alice-olivia-sale',
            "department": 'alice-olivia',
        },
        'alice-olivia-skirts': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia/skirts?id=1248699',
            "category": 'alice-olivia-skirts',
            "department": 'alice-olivia',
        },
        'alice-olivia-tops': {
            "url": 'https://www.bloomingdales.com/shop/alice-olivia/tops?id=1248697',
            "category": 'alice-olivia-tops',
            "department": 'alice-olivia',
        },
    },
    'all-clearance': {
        'all-clearance': {
            "url": 'https://www.bloomingdales.com/shop/all-clearance?id=1063568',
            "category": 'all-clearance',
            "department": 'all-clearance',
        },
    },
    'all-fashion-shoes': {
        'all-fashion-shoes': {
            "url": 'https://www.bloomingdales.com/shop/all-fashion-shoes?id=1109559',
            "category": 'all-fashion-shoes',
            "department": 'all-fashion-shoes',
        },
    },
    'all-furniture': {
        'all-furniture': {
            "url": 'https://www.bloomingdales.com/shop/all-furniture?id=1003617',
            "category": 'all-furniture',
            "department": 'all-furniture',
        },
    },
    'all-holiday-gifts': {
        'all-holiday-gifts': {
            "url": 'https://www.bloomingdales.com/shop/all-holiday-gifts?id=1291702',
            "category": 'all-holiday-gifts',
            "department": 'all-holiday-gifts',
        },
    },
    'all-home': {
        'all-home': {
            "url": 'https://www.bloomingdales.com/shop/all-home?id=1003615',
            "category": 'all-home',
            "department": 'all-home',
        },
    },
    'all-home-decor': {
        'all-home-decor': {
            "url": 'https://www.bloomingdales.com/shop/all-home-decor?id=1151582',
            "category": 'all-home-decor',
            "department": 'all-home-decor',
        },
    },
    'all-men': {
        'all-men': {
            "url": 'https://www.bloomingdales.com/shop/all-men?id=1003601',
            "category": 'all-men',
            "department": 'all-men',
        },
    },
    'allsaints': {
        'allsaints': {
            "url": 'https://www.bloomingdales.com/shop/allsaints?id=1212970',
            "category": 'allsaints',
            "department": 'allsaints',
        },
        'allsaints-mens-clothing-shoes': {
            "url": 'https://www.bloomingdales.com/shop/allsaints/mens-clothing-shoes?id=1212972',
            "category": 'allsaints-mens-clothing-shoes',
            "department": 'allsaints',
        },
        'allsaints-new-to-sale': {
            "url": 'https://www.bloomingdales.com/shop/allsaints/new-to-sale?id=1250964',
            "category": 'allsaints-new-to-sale',
            "department": 'allsaints',
        },
        'allsaints-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/allsaints/womens-clothing?id=1212973',
            "category": 'allsaints-womens-clothing',
            "department": 'allsaints',
        },
        'allsaints-womens-shoes-accessories': {
            "url": 'https://www.bloomingdales.com/shop/allsaints/womens-shoes-accessories?id=1212974',
            "category": 'allsaints-womens-shoes-accessories',
            "department": 'allsaints',
        },
    },
    'ami': {
        'ami': {
            "url": 'https://www.bloomingdales.com/shop/ami?id=1308098',
            "category": 'ami',
            "department": 'ami',
        },
    },
    'anabel-aram': {
        'anabel-aram': {
            "url": 'https://www.bloomingdales.com/shop/anabel-aram?id=1314296',
            "category": 'anabel-aram',
            "department": 'anabel-aram',
        },
    },
    'animal-print': {
        'animal-print': {
            "url": 'https://www.bloomingdales.com/shop/animal-print?id=1238671',
            "category": 'animal-print',
            "department": 'animal-print',
        },
    },
    'annick-goutal': {
        'annick-goutal': {
            "url": 'https://www.bloomingdales.com/shop/annick-goutal?id=1335303',
            "category": 'annick-goutal',
            "department": 'annick-goutal',
        },
    },
    'aqua': {
        'aqua': {
            "url": 'https://www.bloomingdales.com/shop/aqua?id=1002851',
            "category": 'aqua',
            "department": 'aqua',
        },
        'aqua-aqua-cashmere': {
            "url": 'https://www.bloomingdales.com/shop/aqua/aqua-cashmere?id=1105659',
            "category": 'aqua-aqua-cashmere',
            "department": 'aqua',
        },
        'aqua-aqua-x-lisa-says-gah': {
            "url": 'https://www.bloomingdales.com/shop/aqua/aqua-x-lisa-says-gah?id=1304997',
            "category": 'aqua-aqua-x-lisa-says-gah',
            "department": 'aqua',
        },
        'aqua-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/aqua/best-sellers?id=1288930',
            "category": 'aqua-best-sellers',
            "department": 'aqua',
        },
        'aqua-handbags': {
            "url": 'https://www.bloomingdales.com/shop/aqua/handbags?id=1037459',
            "category": 'aqua-handbags',
            "department": 'aqua',
        },
        'aqua-home': {
            "url": 'https://www.bloomingdales.com/shop/aqua/home?id=1240770',
            "category": 'aqua-home',
            "department": 'aqua',
        },
        'aqua-kids-clothing': {
            "url": 'https://www.bloomingdales.com/shop/aqua/kids-clothing?id=1002854',
            "category": 'aqua-kids-clothing',
            "department": 'aqua',
        },
        'aqua-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-arrivals?id=1146759',
            "category": 'aqua-new-arrivals',
            "department": 'aqua',
        },
        'aqua-new-collab-aqua-by-nicky-hilton': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-collab-aqua-by-nicky-hilton?id=1327695',
            "category": 'aqua-new-collab-aqua-by-nicky-hilton',
            "department": 'aqua',
        },
        'aqua-new-collab-aqua-designed-by-agua-bendita': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-collab-aqua-designed-by-agua-bendita?id=1316095',
            "category": 'aqua-new-collab-aqua-designed-by-agua-bendita',
            "department": 'aqua',
        },
        'aqua-new-collection-aqua-clubhouse': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-collection-aqua-clubhouse?id=1310807',
            "category": 'aqua-new-collection-aqua-clubhouse',
            "department": 'aqua',
        },
        'aqua-new-collection-aqua-midnight-opulence': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-collection-aqua-midnight-opulence?id=1334895',
            "category": 'aqua-new-collection-aqua-midnight-opulence',
            "department": 'aqua',
        },
        'aqua-new-collection-aqua-rustic-romance': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-collection-aqua-rustic-romance?id=1326497',
            "category": 'aqua-new-collection-aqua-rustic-romance',
            "department": 'aqua',
        },
        'aqua-new-collection-aqua-summer-romance': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-collection-aqua-summer-romance?id=1319603',
            "category": 'aqua-new-collection-aqua-summer-romance',
            "department": 'aqua',
        },
        'aqua-new-collection-the-new-uptown': {
            "url": 'https://www.bloomingdales.com/shop/aqua/new-collection-the-new-uptown?id=1189659',
            "category": 'aqua-new-collection-the-new-uptown',
            "department": 'aqua',
        },
        'aqua-shoes': {
            "url": 'https://www.bloomingdales.com/shop/aqua/shoes?id=1047259',
            "category": 'aqua-shoes',
            "department": 'aqua',
        },
        'aqua-what-to-wear-for-beach': {
            "url": 'https://www.bloomingdales.com/shop/aqua/what-to-wear-for-beach?id=1308608',
            "category": 'aqua-what-to-wear-for-beach',
            "department": 'aqua',
        },
        'aqua-what-to-wear-for-going-out': {
            "url": 'https://www.bloomingdales.com/shop/aqua/what-to-wear-for-going-out?id=1288932',
            "category": 'aqua-what-to-wear-for-going-out',
            "department": 'aqua',
        },
        'aqua-what-to-wear-for-weddings-events': {
            "url": 'https://www.bloomingdales.com/shop/aqua/what-to-wear-for-weddings-events?id=1288933',
            "category": 'aqua-what-to-wear-for-weddings-events',
            "department": 'aqua',
        },
        'aqua-what-to-wear-for-work-internships': {
            "url": 'https://www.bloomingdales.com/shop/aqua/what-to-wear-for-work-internships?id=1288931',
            "category": 'aqua-what-to-wear-for-work-internships',
            "department": 'aqua',
        },
        'aqua-womens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/aqua/womens-accessories?id=1002853',
            "category": 'aqua-womens-accessories',
            "department": 'aqua',
        },
        'aqua-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/aqua/womens-clothing?id=1002852',
            "category": 'aqua-womens-clothing',
            "department": 'aqua',
        },
    },
    'asics': {
        'asics': {
            "url": 'https://www.bloomingdales.com/shop/asics?id=1306109',
            "category": 'asics',
            "department": 'asics',
        },
    },
    'astrology-zone': {
        'astrology-zone': {
            "url": 'https://www.bloomingdales.com/shop/astrology-zone?id=1084459',
            "category": 'astrology-zone',
            "department": 'astrology-zone',
        },
    },
    'audun-collection': {
        'audun-collection': {
            "url": 'https://www.bloomingdales.com/shop/audun-collection?id=1310598',
            "category": 'audun-collection',
            "department": 'audun-collection',
        },
    },
    'augustinus-bader': {
        'augustinus-bader': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader?id=1162061',
            "category": 'augustinus-bader',
            "department": 'augustinus-bader',
        },
        'augustinus-bader-augustinus-bader-beauty': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader/augustinus-bader-beauty?id=1167859',
            "category": 'augustinus-bader-augustinus-bader-beauty',
            "department": 'augustinus-bader',
        },
        'augustinus-bader-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader/bath-body?id=1199371',
            "category": 'augustinus-bader-bath-body',
            "department": 'augustinus-bader',
        },
        'augustinus-bader-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader/best-sellers?id=1310995',
            "category": 'augustinus-bader-best-sellers',
            "department": 'augustinus-bader',
        },
        'augustinus-bader-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader/gift-sets?id=1199372',
            "category": 'augustinus-bader-gift-sets',
            "department": 'augustinus-bader',
        },
        'augustinus-bader-haircare': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader/haircare?id=1199370',
            "category": 'augustinus-bader-haircare',
            "department": 'augustinus-bader',
        },
        'augustinus-bader-skincare': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader/skincare?id=1199369',
            "category": 'augustinus-bader-skincare',
            "department": 'augustinus-bader',
        },
    },
    'augustinus-bader-beauty': {
        'augustinus-bader-beauty': {
            "url": 'https://www.bloomingdales.com/shop/augustinus-bader-beauty?id=1269415',
            "category": 'augustinus-bader-beauty',
            "department": 'augustinus-bader-beauty',
        },
    },
    'award-winning-beauty-products': {
        'award-winning-beauty-products': {
            "url": 'https://www.bloomingdales.com/shop/award-winning-beauty-products?id=1224760',
            "category": 'award-winning-beauty-products',
            "department": 'award-winning-beauty-products',
        },
    },
    'away': {
        'away': {
            "url": 'https://www.bloomingdales.com/shop/away?id=1331419',
            "category": 'away',
            "department": 'away',
        },
    },
    'ba-sh': {
        'ba-sh': {
            "url": 'https://www.bloomingdales.com/shop/ba-sh?id=1304265',
            "category": 'ba-sh',
            "department": 'ba-sh',
        },
        'ba-sh-coats-and-jackets': {
            "url": 'https://www.bloomingdales.com/shop/ba-sh/coats-and-jackets?id=1304268',
            "category": 'ba-sh-coats-and-jackets',
            "department": 'ba-sh',
        },
        'ba-sh-dresses': {
            "url": 'https://www.bloomingdales.com/shop/ba-sh/dresses?id=1304267',
            "category": 'ba-sh-dresses',
            "department": 'ba-sh',
        },
        'ba-sh-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/ba-sh/sweaters?id=1304266',
            "category": 'ba-sh-sweaters',
            "department": 'ba-sh',
        },
    },
    'baby-humidifier-air-purifier': {
        'baby-humidifier-air-purifier': {
            "url": 'https://www.bloomingdales.com/shop/baby-humidifier-air-purifier?id=1110062',
            "category": 'baby-humidifier-air-purifier',
            "department": 'baby-humidifier-air-purifier',
        },
    },
    'baby-inspiration-guides': {
        'baby-inspiration-guides': {
            "url": 'https://www.bloomingdales.com/shop/baby-inspiration-guides?id=1224373',
            "category": 'baby-inspiration-guides',
            "department": 'baby-inspiration-guides',
        },
    },
    'baby-registry-homepage': {
        'baby-registry-homepage': {
            "url": 'https://www.bloomingdales.com/shop/baby-registry-homepage?id=1216659',
            "category": 'baby-registry-homepage',
            "department": 'baby-registry-homepage',
        },
    },
    'baby-room-decor': {
        'baby-room-decor': {
            "url": 'https://www.bloomingdales.com/shop/baby-room-decor?id=1110061',
            "category": 'baby-room-decor',
            "department": 'baby-room-decor',
        },
    },
    'baccarat': {
        'baccarat': {
            "url": 'https://www.bloomingdales.com/shop/baccarat?id=1238759',
            "category": 'baccarat',
            "department": 'baccarat',
        },
        'baccarat-a-new-chapter': {
            "url": 'https://www.bloomingdales.com/shop/baccarat/a-new-chapter?id=1279146',
            "category": 'baccarat-a-new-chapter',
            "department": 'baccarat',
        },
        'baccarat-the-baccarat-lucky-butterfly': {
            "url": 'https://www.bloomingdales.com/shop/baccarat/the-baccarat-lucky-butterfly?id=1278696',
            "category": 'baccarat-the-baccarat-lucky-butterfly',
            "department": 'baccarat',
        },
        'baccarat-top-gifts': {
            "url": 'https://www.bloomingdales.com/shop/baccarat/top-gifts?id=1279147',
            "category": 'baccarat-top-gifts',
            "department": 'baccarat',
        },
    },
    'back-to-campus': {
        'back-to-campus': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus?id=1274917',
            "category": 'back-to-campus',
            "department": 'back-to-campus',
        },
        'back-to-campus-dorm': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus/dorm?id=1274920',
            "category": 'back-to-campus-dorm',
            "department": 'back-to-campus',
        },
        'back-to-campus-men': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus/men?id=1274919',
            "category": 'back-to-campus-men',
            "department": 'back-to-campus',
        },
        'back-to-campus-what-to-wear-for-class': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus/what-to-wear-for-class?id=1283211',
            "category": 'back-to-campus-what-to-wear-for-class',
            "department": 'back-to-campus',
        },
        'back-to-campus-what-to-wear-for-late-night-library': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus/what-to-wear-for-late-night-library?id=1283212',
            "category": 'back-to-campus-what-to-wear-for-late-night-library',
            "department": 'back-to-campus',
        },
        'back-to-campus-what-to-wear-for-nights-out': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus/what-to-wear-for-nights-out?id=1283213',
            "category": 'back-to-campus-what-to-wear-for-nights-out',
            "department": 'back-to-campus',
        },
        'back-to-campus-what-to-wear-for-work-internships': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus/what-to-wear-for-work-internships?id=1283214',
            "category": 'back-to-campus-what-to-wear-for-work-internships',
            "department": 'back-to-campus',
        },
        'back-to-campus-women': {
            "url": 'https://www.bloomingdales.com/shop/back-to-campus/women?id=1274918',
            "category": 'back-to-campus-women',
            "department": 'back-to-campus',
        },
    },
    'backpacks': {
        'backpacks': {
            "url": 'https://www.bloomingdales.com/shop/backpacks?id=1276498',
            "category": 'backpacks',
            "department": 'backpacks',
        },
    },
    'baking-dishes': {
        'baking-dishes': {
            "url": 'https://www.bloomingdales.com/shop/baking-dishes?id=1301868',
            "category": 'baking-dishes',
            "department": 'baking-dishes',
        },
    },
    'baking-pans-sheets': {
        'baking-pans-sheets': {
            "url": 'https://www.bloomingdales.com/shop/baking-pans-sheets?id=1301869',
            "category": 'baking-pans-sheets',
            "department": 'baking-pans-sheets',
        },
    },
    'balenciaga': {
        'balenciaga': {
            "url": 'https://www.bloomingdales.com/shop/balenciaga?id=1194375',
            "category": 'balenciaga',
            "department": 'balenciaga',
        },
        'balenciaga-handbags': {
            "url": 'https://www.bloomingdales.com/shop/balenciaga/handbags?id=1194459',
            "category": 'balenciaga-handbags',
            "department": 'balenciaga',
        },
        'balenciaga-men': {
            "url": 'https://www.bloomingdales.com/shop/balenciaga/men?id=1194378',
            "category": 'balenciaga-men',
            "department": 'balenciaga',
        },
        'balenciaga-mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/balenciaga/mens-accessories?id=1194761',
            "category": 'balenciaga-mens-accessories',
            "department": 'balenciaga',
        },
        'balenciaga-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/balenciaga/mens-shoes?id=1194759',
            "category": 'balenciaga-mens-shoes',
            "department": 'balenciaga',
        },
        'balenciaga-women': {
            "url": 'https://www.bloomingdales.com/shop/balenciaga/women?id=1194377',
            "category": 'balenciaga-women',
            "department": 'balenciaga',
        },
        'balenciaga-womens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/balenciaga/womens-accessories?id=1194559',
            "category": 'balenciaga-womens-accessories',
            "department": 'balenciaga',
        },
    },
    'balmain': {
        'balmain': {
            "url": 'https://www.bloomingdales.com/shop/balmain?id=1329210',
            "category": 'balmain',
            "department": 'balmain',
        },
        'balmain-beauty': {
            "url": 'https://www.bloomingdales.com/shop/balmain/beauty?id=1330896',
            "category": 'balmain-beauty',
            "department": 'balmain',
        },
        'balmain-jewelry-watches': {
            "url": 'https://www.bloomingdales.com/shop/balmain/jewelry-watches?id=1330895',
            "category": 'balmain-jewelry-watches',
            "department": 'balmain',
        },
        'balmain-men': {
            "url": 'https://www.bloomingdales.com/shop/balmain/men?id=1329215',
            "category": 'balmain-men',
            "department": 'balmain',
        },
        'balmain-shoes-handbags': {
            "url": 'https://www.bloomingdales.com/shop/balmain/shoes-handbags?id=1329211',
            "category": 'balmain-shoes-handbags',
            "department": 'balmain',
        },
        'balmain-women': {
            "url": 'https://www.bloomingdales.com/shop/balmain/women?id=1329214',
            "category": 'balmain-women',
            "department": 'balmain',
        },
    },
    'barberinos': {
        'barberinos': {
            "url": 'https://www.bloomingdales.com/shop/barberinos?id=1331903',
            "category": 'barberinos',
            "department": 'barberinos',
        },
    },
    'barbour': {
        'barbour': {
            "url": 'https://www.bloomingdales.com/shop/barbour?id=1285439',
            "category": 'barbour',
            "department": 'barbour',
        },
        'barbour-mens': {
            "url": 'https://www.bloomingdales.com/shop/barbour/mens?id=1285440',
            "category": 'barbour-mens',
            "department": 'barbour',
        },
        'barbour-womens': {
            "url": 'https://www.bloomingdales.com/shop/barbour/womens?id=1285441',
            "category": 'barbour-womens',
            "department": 'barbour',
        },
    },
    'bath-body': {
        'bath-body': {
            "url": 'https://www.bloomingdales.com/shop/bath-body?id=1269418',
            "category": 'bath-body',
            "department": 'bath-body',
        },
    },
    'bath-spa-hair-care-gift-sets': {
        'bath-spa-hair-care-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/bath-spa-hair-care-gift-sets?id=14899',
            "category": 'bath-spa-hair-care-gift-sets',
            "department": 'bath-spa-hair-care-gift-sets',
        },
    },
    'bathing-suits-swimsuits-bikini': {
        'bathing-suits-swimsuits-bikini': {
            "url": 'https://www.bloomingdales.com/shop/bathing-suits-swimsuits-bikini?id=1095659',
            "category": 'bathing-suits-swimsuits-bikini',
            "department": 'bathing-suits-swimsuits-bikini',
        },
    },
    'bathroom-decor-sets-accessories': {
        'bathroom-decor-sets-accessories': {
            "url": 'https://www.bloomingdales.com/shop/bathroom-decor-sets-accessories?id=1005702',
            "category": 'bathroom-decor-sets-accessories',
            "department": 'bathroom-decor-sets-accessories',
        },
    },
    'beach-wear-summer-beach-essentials': {
        'beach-wear-summer-beach-essentials': {
            "url": 'https://www.bloomingdales.com/shop/beach-wear-summer-beach-essentials?id=1307607',
            "category": 'beach-wear-summer-beach-essentials',
            "department": 'beach-wear-summer-beach-essentials',
        },
    },
    'beach-wedding-attire': {
        'beach-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/beach-wedding-attire?id=1179191',
            "category": 'beach-wedding-attire',
            "department": 'beach-wedding-attire',
        },
    },
    'beachy-business': {
        'beachy-business': {
            "url": 'https://www.bloomingdales.com/shop/beachy-business?id=1238680',
            "category": 'beachy-business',
            "department": 'beachy-business',
        },
    },
    'beauty': {
        'beauty': {
            "url": 'https://www.bloomingdales.com/shop/beauty?id=1319128',
            "category": 'beauty',
            "department": 'beauty',
        },
        'makeup-perfume-beauty': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty?id=2921',
            "category": 'makeup-perfume-beauty',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-after-sun-care': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/after-sun-care?id=1195871',
            "category": 'makeup-perfume-beauty-after-sun-care',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-apothecary': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/apothecary?id=1190162',
            "category": 'makeup-perfume-beauty-apothecary',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/bath-body?id=14846',
            "category": 'makeup-perfume-beauty-bath-body',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-bath-body-care-products': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/bath-body-care-products?id=1006037',
            "category": 'makeup-perfume-beauty-bath-body-care-products',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-bb-cc-cream': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/bb-cc-cream?id=1024665',
            "category": 'makeup-perfume-beauty-bb-cc-cream',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-beauty-advent-calendars': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/beauty-advent-calendars?id=1165659',
            "category": 'makeup-perfume-beauty-beauty-advent-calendars',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-berry': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/berry?id=1315496',
            "category": 'makeup-perfume-beauty-berry',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/best-sellers?id=1308607',
            "category": 'makeup-perfume-beauty-best-sellers',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-blush-crush': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/blush-crush?id=1232059',
            "category": 'makeup-perfume-beauty-blush-crush',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-blush-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/blush-makeup?id=1024664',
            "category": 'makeup-perfume-beauty-blush-makeup',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-body-lotions': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/body-lotions?id=1194169',
            "category": 'makeup-perfume-beauty-body-lotions',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-body-oil': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/body-oil?id=1286796',
            "category": 'makeup-perfume-beauty-body-oil',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-body-washes-shower-gels': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/body-washes-shower-gels?id=1286801',
            "category": 'makeup-perfume-beauty-body-washes-shower-gels',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-bridal-beauty': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/bridal-beauty?id=1266906',
            "category": 'makeup-perfume-beauty-bridal-beauty',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-bronzer-highlighter': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/bronzer-highlighter?id=1024667',
            "category": 'makeup-perfume-beauty-bronzer-highlighter',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-cherry': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/cherry?id=1315498',
            "category": 'makeup-perfume-beauty-cherry',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-cinnamon-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/cinnamon-fragrances?id=1315297',
            "category": 'makeup-perfume-beauty-cinnamon-fragrances',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-citrus': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/citrus?id=1315497',
            "category": 'makeup-perfume-beauty-citrus',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-clean-beauty': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/clean-beauty?id=1150659',
            "category": 'makeup-perfume-beauty-clean-beauty',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-coconut-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/coconut-fragrances?id=1315296',
            "category": 'makeup-perfume-beauty-coconut-fragrances',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-cologne': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/cologne?id=1006034',
            "category": 'makeup-perfume-beauty-cologne',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-cologne-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/cologne-gift-sets?id=1006039',
            "category": 'makeup-perfume-beauty-cologne-gift-sets',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-cologne-grooming-kit': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/cologne-grooming-kit?id=1000067',
            "category": 'makeup-perfume-beauty-cologne-grooming-kit',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-concealer-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/concealer-makeup?id=1024663',
            "category": 'makeup-perfume-beauty-concealer-makeup',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-conditioner': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/conditioner?id=1287569',
            "category": 'makeup-perfume-beauty-conditioner',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-contour': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/contour?id=1286802',
            "category": 'makeup-perfume-beauty-contour',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-dermatologist-and-science-backed-skin-care': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/dermatologist-and-science-backed-skin-care?id=1317519',
            "category": 'makeup-perfume-beauty-dermatologist-and-science-backed-skin-care',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-exclusive-offer-beauty': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/exclusive-offer-beauty?id=1038459',
            "category": 'makeup-perfume-beauty-exclusive-offer-beauty',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eye-cream-treatment': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eye-cream-treatment?id=1005922',
            "category": 'makeup-perfume-beauty-eye-cream-treatment',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eye-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eye-makeup?id=14797',
            "category": 'makeup-perfume-beauty-eye-makeup',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyebrow-gel': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyebrow-gel?id=1286805',
            "category": 'makeup-perfume-beauty-eyebrow-gel',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyebrow-makeup-pencil-gel': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyebrow-makeup-pencil-gel?id=1025065',
            "category": 'makeup-perfume-beauty-eyebrow-makeup-pencil-gel',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyebrow-pencil': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyebrow-pencil?id=1286806',
            "category": 'makeup-perfume-beauty-eyebrow-pencil',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyeliner': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyeliner?id=1025063',
            "category": 'makeup-perfume-beauty-eyeliner',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyeshadow': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyeshadow?id=1025062',
            "category": 'makeup-perfume-beauty-eyeshadow',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyeshadow-palettes': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyeshadow-palettes?id=1025165',
            "category": 'makeup-perfume-beauty-eyeshadow-palettes',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyeshadow-primer': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyeshadow-primer?id=1025166',
            "category": 'makeup-perfume-beauty-eyeshadow-primer',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-eyeshadow-sticks': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/eyeshadow-sticks?id=1286808',
            "category": 'makeup-perfume-beauty-eyeshadow-sticks',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-face-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/face-makeup?id=14721',
            "category": 'makeup-perfume-beauty-face-makeup',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-face-masks': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/face-masks?id=1247895',
            "category": 'makeup-perfume-beauty-face-masks',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-face-moisturizer': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/face-moisturizer?id=1005884',
            "category": 'makeup-perfume-beauty-face-moisturizer',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-face-primer': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/face-primer?id=1024666',
            "category": 'makeup-perfume-beauty-face-primer',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-face-serum-oil': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/face-serum-oil?id=1005924',
            "category": 'makeup-perfume-beauty-face-serum-oil',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-facial-cleansers-exfoliants': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/facial-cleansers-exfoliants?id=1005915',
            "category": 'makeup-perfume-beauty-facial-cleansers-exfoliants',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-facial-cleansing-brush-skin-care-tools': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/facial-cleansing-brush-skin-care-tools?id=1032461',
            "category": 'makeup-perfume-beauty-facial-cleansing-brush-skin-care-tools',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-fall-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/fall-fragrances?id=1247795',
            "category": 'makeup-perfume-beauty-fall-fragrances',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-foundation-best-for-combination-skin': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/foundation-best-for-combination-skin?id=1293318',
            "category": 'makeup-perfume-beauty-foundation-best-for-combination-skin',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-foundation-best-for-dry-skin': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/foundation-best-for-dry-skin?id=1293312',
            "category": 'makeup-perfume-beauty-foundation-best-for-dry-skin',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-foundation-best-for-mature-skin': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/foundation-best-for-mature-skin?id=1293104',
            "category": 'makeup-perfume-beauty-foundation-best-for-mature-skin',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-foundation-best-for-oiliness': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/foundation-best-for-oiliness?id=1293102',
            "category": 'makeup-perfume-beauty-foundation-best-for-oiliness',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-fragrance-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/fragrance-gift-sets?id=1005891',
            "category": 'makeup-perfume-beauty-fragrance-gift-sets',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-fruity-floral': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/fruity-floral?id=1316922',
            "category": 'makeup-perfume-beauty-fruity-floral',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-fruity-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/fruity-fragrances?id=1314995',
            "category": 'makeup-perfume-beauty-fruity-fragrances',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/gift-sets?id=1287116',
            "category": 'makeup-perfume-beauty-gift-sets',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-gifts-for-her': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/gifts-for-her?id=1212160',
            "category": 'makeup-perfume-beauty-gifts-for-her',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-gifts-for-him': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/gifts-for-him?id=1212161',
            "category": 'makeup-perfume-beauty-gifts-for-him',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-gifts-under-100': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/gifts-under-100?id=1179861',
            "category": 'makeup-perfume-beauty-gifts-under-100',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-glowhaus-makeup-skin-care': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/glowhaus-makeup-skin-care?id=1035059',
            "category": 'makeup-perfume-beauty-glowhaus-makeup-skin-care',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-gourmand-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/gourmand-fragrances?id=21082',
            "category": 'makeup-perfume-beauty-gourmand-fragrances',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-hair-care': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/hair-care?id=1150663',
            "category": 'makeup-perfume-beauty-hair-care',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-hair-styling-products': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/hair-styling-products?id=1024659',
            "category": 'makeup-perfume-beauty-hair-styling-products',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-hair-tools-accessories': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/hair-tools-accessories?id=1032460',
            "category": 'makeup-perfume-beauty-hair-tools-accessories',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-hair-treatment': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/hair-treatment?id=1024660',
            "category": 'makeup-perfume-beauty-hair-treatment',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-hand-lotion': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/hand-lotion?id=1287117',
            "category": 'makeup-perfume-beauty-hand-lotion',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-hand-wash': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/hand-wash?id=1287115',
            "category": 'makeup-perfume-beauty-hand-wash',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-high-end-makeup-brands': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/high-end-makeup-brands?id=14720',
            "category": 'makeup-perfume-beauty-high-end-makeup-brands',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-holiday-glam': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/holiday-glam?id=1337495',
            "category": 'makeup-perfume-beauty-holiday-glam',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-korean-japanese-beauty-brands': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/korean-japanese-beauty-brands?id=1224841',
            "category": 'makeup-perfume-beauty-korean-japanese-beauty-brands',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-lip-balms-treatments': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/lip-balms-treatments?id=14810',
            "category": 'makeup-perfume-beauty-lip-balms-treatments',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-lip-gloss': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/lip-gloss?id=1215160',
            "category": 'makeup-perfume-beauty-lip-gloss',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-lip-liners-pencils': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/lip-liners-pencils?id=1025060',
            "category": 'makeup-perfume-beauty-lip-liners-pencils',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-lip-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/lip-makeup?id=14806',
            "category": 'makeup-perfume-beauty-lip-makeup',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-lip-palettes': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/lip-palettes?id=1215180',
            "category": 'makeup-perfume-beauty-lip-palettes',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-lip-plumpers': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/lip-plumpers?id=1286804',
            "category": 'makeup-perfume-beauty-lip-plumpers',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-lipstick': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/lipstick?id=1219361',
            "category": 'makeup-perfume-beauty-lipstick',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-luxury-perfume': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/luxury-perfume?id=1005889',
            "category": 'makeup-perfume-beauty-luxury-perfume',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup?id=1150661',
            "category": 'makeup-perfume-beauty-makeup',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup-brushes': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup-brushes?id=1287570',
            "category": 'makeup-perfume-beauty-makeup-brushes',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup-brushes-tools': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup-brushes-tools?id=1032459',
            "category": 'makeup-perfume-beauty-makeup-brushes-tools',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup-foundation': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup-foundation?id=1024662',
            "category": 'makeup-perfume-beauty-makeup-foundation',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup-gift-sets?id=1213971',
            "category": 'makeup-perfume-beauty-makeup-gift-sets',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup-palettes': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup-palettes?id=1000624',
            "category": 'makeup-perfume-beauty-makeup-palettes',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup-tools-brushes': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup-tools-brushes?id=14873',
            "category": 'makeup-perfume-beauty-makeup-tools-brushes',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-makeup-value-sets': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/makeup-value-sets?id=1018466',
            "category": 'makeup-perfume-beauty-makeup-value-sets',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-mascara-waterproof': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/mascara-waterproof?id=1025064',
            "category": 'makeup-perfume-beauty-mascara-waterproof',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-massage-tools': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/massage-tools?id=1287571',
            "category": 'makeup-perfume-beauty-massage-tools',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-mens-hair-products': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/mens-hair-products?id=1286795',
            "category": 'makeup-perfume-beauty-mens-hair-products',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-nail-polish-nail-care': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/nail-polish-nail-care?id=14811',
            "category": 'makeup-perfume-beauty-nail-polish-nail-care',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-our-best-gifts': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/our-best-gifts?id=1252214',
            "category": 'makeup-perfume-beauty-our-best-gifts',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-peach': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/peach?id=1315495',
            "category": 'makeup-perfume-beauty-peach',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-refillable-beauty': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/refillable-beauty?id=1192864',
            "category": 'makeup-perfume-beauty-refillable-beauty',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-rollerball-perfume-travel-size-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/rollerball-perfume-travel-size-fragrance?id=1005892',
            "category": 'makeup-perfume-beauty-rollerball-perfume-travel-size-fragrance',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-salon-hair-products-luxury-hair-care': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/salon-hair-products-luxury-hair-care?id=14861',
            "category": 'makeup-perfume-beauty-salon-hair-products-luxury-hair-care',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-self-tanners': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/self-tanners?id=1286105',
            "category": 'makeup-perfume-beauty-self-tanners',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-setting-powder-spray': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/setting-powder-spray?id=1024670',
            "category": 'makeup-perfume-beauty-setting-powder-spray',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-shampoo': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/shampoo?id=1287544',
            "category": 'makeup-perfume-beauty-shampoo',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-shampoo-conditioner': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/shampoo-conditioner?id=1024559',
            "category": 'makeup-perfume-beauty-shampoo-conditioner',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-shaving-beard-care-products': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/shaving-beard-care-products?id=1006036',
            "category": 'makeup-perfume-beauty-shaving-beard-care-products',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-shaving-tools-accessories': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/shaving-tools-accessories?id=1006038',
            "category": 'makeup-perfume-beauty-shaving-tools-accessories',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-skin-care': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/skin-care?id=1150660',
            "category": 'makeup-perfume-beauty-skin-care',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-skin-care-products': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/skin-care-products?id=1006035',
            "category": 'makeup-perfume-beauty-skin-care-products',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-skincare': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/skincare?id=14812',
            "category": 'makeup-perfume-beauty-skincare',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-skincare-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/skincare-gift-sets?id=1005921',
            "category": 'makeup-perfume-beauty-skincare-gift-sets',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-spf-infused-products': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/spf-infused-products?id=1225180',
            "category": 'makeup-perfume-beauty-spf-infused-products',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-sunscreen': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/sunscreen?id=15967',
            "category": 'makeup-perfume-beauty-sunscreen',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-tinted-moisturizer': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/tinted-moisturizer?id=1024668',
            "category": 'makeup-perfume-beauty-tinted-moisturizer',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-toners': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/toners?id=1067359',
            "category": 'makeup-perfume-beauty-toners',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-tonka-bean-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/tonka-bean-fragrances?id=1315295',
            "category": 'makeup-perfume-beauty-tonka-bean-fragrances',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-tropical': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/tropical?id=1315499',
            "category": 'makeup-perfume-beauty-tropical',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-vanilla-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/vanilla-fragrances?id=1314615',
            "category": 'makeup-perfume-beauty-vanilla-fragrances',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-viral-beauty-products': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/viral-beauty-products?id=1214059',
            "category": 'makeup-perfume-beauty-viral-beauty-products',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-wellchemist-clean-beauty': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/wellchemist-clean-beauty?id=1058060',
            "category": 'makeup-perfume-beauty-wellchemist-clean-beauty',
            "department": 'beauty',
        },
        'makeup-perfume-beauty-winter-beauty-trends': {
            "url": 'https://www.bloomingdales.com/shop/makeup-perfume-beauty/winter-beauty-trends?id=1210362',
            "category": 'makeup-perfume-beauty-winter-beauty-trends',
            "department": 'beauty',
        },
    },
    'beauty-cosmetics-personalization': {
        'beauty-cosmetics-personalization': {
            "url": 'https://www.bloomingdales.com/shop/beauty-cosmetics-personalization?id=1333514',
            "category": 'beauty-cosmetics-personalization',
            "department": 'beauty-cosmetics-personalization',
        },
    },
    'beauty-devices': {
        'beauty-devices': {
            "url": 'https://www.bloomingdales.com/shop/beauty-devices?id=1215059',
            "category": 'beauty-devices',
            "department": 'beauty-devices',
        },
    },
    'beautyspace': {
        'beautyspace': {
            "url": 'https://www.bloomingdales.com/shop/beautyspace?id=1001292',
            "category": 'beautyspace',
            "department": 'beautyspace',
        },
    },
    'beis': {
        'beis': {
            "url": 'https://www.bloomingdales.com/shop/beis?id=1288998',
            "category": 'beis',
            "department": 'beis',
        },
        'beis-all-new-rollers': {
            "url": 'https://www.bloomingdales.com/shop/beis/all-new-rollers?id=1288999',
            "category": 'beis-all-new-rollers',
            "department": 'beis',
        },
        'beis-all-new-weekender-bags': {
            "url": 'https://www.bloomingdales.com/shop/beis/all-new-weekender-bags?id=1289000',
            "category": 'beis-all-new-weekender-bags',
            "department": 'beis',
        },
        'beis-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/beis/best-sellers?id=1289003',
            "category": 'beis-best-sellers',
            "department": 'beis',
        },
        'beis-core-collection': {
            "url": 'https://www.bloomingdales.com/shop/beis/core-collection?id=1289001',
            "category": 'beis-core-collection',
            "department": 'beis',
        },
    },
    'belt-bags': {
        'belt-bags': {
            "url": 'https://www.bloomingdales.com/shop/belt-bags?id=1036995',
            "category": 'belt-bags',
            "department": 'belt-bags',
        },
    },
    'bernardaud': {
        'bernardaud': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud?id=1232659',
            "category": 'bernardaud',
            "department": 'bernardaud',
        },
        'bernardaud-ecume': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud/ecume?id=1237170',
            "category": 'bernardaud-ecume',
            "department": 'bernardaud',
        },
        'bernardaud-louvre': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud/louvre?id=1237171',
            "category": 'bernardaud-louvre',
            "department": 'bernardaud',
        },
        'bernardaud-organza': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud/organza?id=1237168',
            "category": 'bernardaud-organza',
            "department": 'bernardaud',
        },
        'bernardaud-origine': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud/origine?id=1237169',
            "category": 'bernardaud-origine',
            "department": 'bernardaud',
        },
        'bernardaud-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud/shop-all?id=1232660',
            "category": 'bernardaud-shop-all',
            "department": 'bernardaud',
        },
        'bernardaud-shop-by-collection': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud/shop-by-collection?id=1237167',
            "category": 'bernardaud-shop-by-collection',
            "department": 'bernardaud',
        },
        'bernardaud-shop-votives': {
            "url": 'https://www.bloomingdales.com/shop/bernardaud/shop-votives?id=1237172',
            "category": 'bernardaud-shop-votives',
            "department": 'bernardaud',
        },
    },
    'bernhardt': {
        'bernhardt': {
            "url": 'https://www.bloomingdales.com/shop/bernhardt?id=1261895',
            "category": 'bernhardt',
            "department": 'bernhardt',
        },
    },
    'best-sellers': {
        'best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/best-sellers?id=1104620',
            "category": 'best-sellers',
            "department": 'best-sellers',
        },
    },
    'best-selling': {
        'best-selling': {
            "url": 'https://www.bloomingdales.com/shop/best-selling?id=1155460',
            "category": 'best-selling',
            "department": 'best-selling',
        },
    },
    'best-selling-beauty-products': {
        'best-selling-beauty-products': {
            "url": 'https://www.bloomingdales.com/shop/best-selling-beauty-products?id=1267014',
            "category": 'best-selling-beauty-products',
            "department": 'best-selling-beauty-products',
        },
    },
    'beyond-perfecting': {
        'beyond-perfecting': {
            "url": 'https://www.bloomingdales.com/shop/beyond-perfecting?id=1001210',
            "category": 'beyond-perfecting',
            "department": 'beyond-perfecting',
        },
    },
    'biologique-recherche': {
        'biologique-recherche': {
            "url": 'https://www.bloomingdales.com/shop/biologique-recherche?id=1289695',
            "category": 'biologique-recherche',
            "department": 'biologique-recherche',
        },
        'biologique-recherche-masks': {
            "url": 'https://www.bloomingdales.com/shop/biologique-recherche/masks?id=1310798',
            "category": 'biologique-recherche-masks',
            "department": 'biologique-recherche',
        },
        'biologique-recherche-moisturizers': {
            "url": 'https://www.bloomingdales.com/shop/biologique-recherche/moisturizers?id=1310797',
            "category": 'biologique-recherche-moisturizers',
            "department": 'biologique-recherche',
        },
        'biologique-recherche-p50': {
            "url": 'https://www.bloomingdales.com/shop/biologique-recherche/p50?id=1311796',
            "category": 'biologique-recherche-p50',
            "department": 'biologique-recherche',
        },
        'biologique-recherche-serums': {
            "url": 'https://www.bloomingdales.com/shop/biologique-recherche/serums?id=1310795',
            "category": 'biologique-recherche-serums',
            "department": 'biologique-recherche',
        },
    },
    'birkenstock': {
        'birkenstock': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock?id=1191062',
            "category": 'birkenstock',
            "department": 'birkenstock',
        },
        'birkenstock-arizona': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/arizona?id=1275605',
            "category": 'birkenstock-arizona',
            "department": 'birkenstock',
        },
        'birkenstock-boston': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/boston?id=1275604',
            "category": 'birkenstock-boston',
            "department": 'birkenstock',
        },
        'birkenstock-clogs': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/clogs?id=1275602',
            "category": 'birkenstock-clogs',
            "department": 'birkenstock',
        },
        'birkenstock-eva': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/eva?id=1286812',
            "category": 'birkenstock-eva',
            "department": 'birkenstock',
        },
        'birkenstock-kids-shoes': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/kids-shoes?id=1191065',
            "category": 'birkenstock-kids-shoes',
            "department": 'birkenstock',
        },
        'birkenstock-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/mens-shoes?id=1191064',
            "category": 'birkenstock-mens-shoes',
            "department": 'birkenstock',
        },
        'birkenstock-sandals': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/sandals?id=1275603',
            "category": 'birkenstock-sandals',
            "department": 'birkenstock',
        },
        'birkenstock-shearling': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/shearling?id=1286811',
            "category": 'birkenstock-shearling',
            "department": 'birkenstock',
        },
        'birkenstock-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/birkenstock/womens-shoes?id=1191063',
            "category": 'birkenstock-womens-shoes',
            "department": 'birkenstock',
        },
    },
    'black-orchid-collection': {
        'black-orchid-collection': {
            "url": 'https://www.bloomingdales.com/shop/black-orchid-collection?id=1310596',
            "category": 'black-orchid-collection',
            "department": 'black-orchid-collection',
        },
    },
    'black-tie-wedding-attire': {
        'black-tie-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/black-tie-wedding-attire?id=1179192',
            "category": 'black-tie-wedding-attire',
            "department": 'black-tie-wedding-attire',
        },
    },
    'blankets': {
        'blankets': {
            "url": 'https://www.bloomingdales.com/shop/blankets?id=1006108',
            "category": 'blankets',
            "department": 'blankets',
        },
    },
    'blazers': {
        'blazers': {
            "url": 'https://www.bloomingdales.com/shop/blazers?id=1278800',
            "category": 'blazers',
            "department": 'blazers',
        },
    },
    'bloomingdales-collection': {
        'bloomingdales-collection': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection?id=17796',
            "category": 'bloomingdales-collection',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-colored-gemstones': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/colored-gemstones?id=21107',
            "category": 'bloomingdales-collection-colored-gemstones',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-diamonds': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/diamonds?id=20949',
            "category": 'bloomingdales-collection-diamonds',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-flash-sale-preview': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/flash-sale-preview?id=1288399',
            "category": 'bloomingdales-collection-flash-sale-preview',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-gold': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/gold?id=17799',
            "category": 'bloomingdales-collection-gold',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-lab-grown-diamonds': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/lab-grown-diamonds?id=1233984',
            "category": 'bloomingdales-collection-lab-grown-diamonds',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-luxe-collection': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/luxe-collection?id=1183765',
            "category": 'bloomingdales-collection-luxe-collection',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-mens-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/mens-jewelry?id=1240259',
            "category": 'bloomingdales-collection-mens-jewelry',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-pearls': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/pearls?id=22089',
            "category": 'bloomingdales-collection-pearls',
            "department": 'bloomingdales-collection',
        },
        'bloomingdales-collection-tennis-collection': {
            "url": 'https://www.bloomingdales.com/shop/bloomingdales-collection/tennis-collection?id=1254097',
            "category": 'bloomingdales-collection-tennis-collection',
            "department": 'bloomingdales-collection',
        },
    },
    'blue': {
        'blue': {
            "url": 'https://www.bloomingdales.com/shop/blue?id=1002179',
            "category": 'blue',
            "department": 'blue',
        },
    },
    'bold-lips': {
        'bold-lips': {
            "url": 'https://www.bloomingdales.com/shop/bold-lips?id=1247905',
            "category": 'bold-lips',
            "department": 'bold-lips',
        },
    },
    'boll-branch': {
        'boll-branch': {
            "url": 'https://www.bloomingdales.com/shop/boll-branch?id=1243295',
            "category": 'boll-branch',
            "department": 'boll-branch',
        },
    },
    'bond-no-9-new-york': {
        'bond-no-9-new-york': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york?id=1210766',
            "category": 'bond-no-9-new-york',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/bath-body?id=1210762',
            "category": 'bond-no-9-new-york-bath-body',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-candles': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/candles?id=1210763',
            "category": 'bond-no-9-new-york-candles',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-central-park-west-collection': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/central-park-west-collection?id=1210767',
            "category": 'bond-no-9-new-york-central-park-west-collection',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/fragrances?id=1210774',
            "category": 'bond-no-9-new-york-fragrances',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/gift-sets?id=1210761',
            "category": 'bond-no-9-new-york-gift-sets',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-greenwich-village-collection': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/greenwich-village-collection?id=1210768',
            "category": 'bond-no-9-new-york-greenwich-village-collection',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-lipsticks': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/lipsticks?id=1210764',
            "category": 'bond-no-9-new-york-lipsticks',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-madison-ave-collection': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/madison-ave-collection?id=1210769',
            "category": 'bond-no-9-new-york-madison-ave-collection',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-madison-square-park-collection': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/madison-square-park-collection?id=1210770',
            "category": 'bond-no-9-new-york-madison-square-park-collection',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-mens-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/mens-fragrances?id=1210759',
            "category": 'bond-no-9-new-york-mens-fragrances',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-new-york-flowers-collection': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/new-york-flowers-collection?id=1210771',
            "category": 'bond-no-9-new-york-new-york-flowers-collection',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-new-york-nights-collection': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/new-york-nights-collection?id=1210772',
            "category": 'bond-no-9-new-york-new-york-nights-collection',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-nolita-collection': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/nolita-collection?id=1210773',
            "category": 'bond-no-9-new-york-nolita-collection',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/shop-all?id=1210765',
            "category": 'bond-no-9-new-york-shop-all',
            "department": 'bond-no-9-new-york',
        },
        'bond-no-9-new-york-womens-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/bond-no-9-new-york/womens-fragrances?id=1210760',
            "category": 'bond-no-9-new-york-womens-fragrances',
            "department": 'bond-no-9-new-york',
        },
    },
    'bootcut-relaxed-fit-jeans': {
        'bootcut-relaxed-fit-jeans': {
            "url": 'https://www.bloomingdales.com/shop/bootcut-relaxed-fit-jeans?id=1027010',
            "category": 'bootcut-relaxed-fit-jeans',
            "department": 'bootcut-relaxed-fit-jeans',
        },
    },
    'bottega-veneta': {
        'bottega-veneta': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta?id=1149159',
            "category": 'bottega-veneta',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-handbags': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/handbags?id=1154661',
            "category": 'bottega-veneta-handbags',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-men': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/men?id=1154767',
            "category": 'bottega-veneta-men',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/mens-accessories?id=1154769',
            "category": 'bottega-veneta-mens-accessories',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/mens-shoes?id=1154565',
            "category": 'bottega-veneta-mens-shoes',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-mens-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/mens-sunglasses?id=1154770',
            "category": 'bottega-veneta-mens-sunglasses',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-women': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/women?id=1154662',
            "category": 'bottega-veneta-women',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/womens-shoes?id=1154660',
            "category": 'bottega-veneta-womens-shoes',
            "department": 'bottega-veneta',
        },
        'bottega-veneta-womens-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/bottega-veneta/womens-sunglasses?id=1155059',
            "category": 'bottega-veneta-womens-sunglasses',
            "department": 'bottega-veneta',
        },
    },
    'bottled-blooms': {
        'bottled-blooms': {
            "url": 'https://www.bloomingdales.com/shop/bottled-blooms?id=1002610',
            "category": 'bottled-blooms',
            "department": 'bottled-blooms',
        },
    },
    'bowls-trays-vases': {
        'bowls-trays-vases': {
            "url": 'https://www.bloomingdales.com/shop/bowls-trays-vases?id=1151560',
            "category": 'bowls-trays-vases',
            "department": 'bowls-trays-vases',
        },
        'bowls-trays-vases-modern-contemporary-bowls': {
            "url": 'https://www.bloomingdales.com/shop/bowls-trays-vases/modern-contemporary-bowls?id=1151561',
            "category": 'bowls-trays-vases-modern-contemporary-bowls',
            "department": 'bowls-trays-vases',
        },
        'bowls-trays-vases-modern-contemporary-trays': {
            "url": 'https://www.bloomingdales.com/shop/bowls-trays-vases/modern-contemporary-trays?id=1151562',
            "category": 'bowls-trays-vases-modern-contemporary-trays',
            "department": 'bowls-trays-vases',
        },
        'bowls-trays-vases-modern-contemporary-vases': {
            "url": 'https://www.bloomingdales.com/shop/bowls-trays-vases/modern-contemporary-vases?id=1151563',
            "category": 'bowls-trays-vases-modern-contemporary-vases',
            "department": 'bowls-trays-vases',
        },
    },
    'boys-backpacks-accessories': {
        'boys-backpacks-accessories': {
            "url": 'https://www.bloomingdales.com/shop/boys-backpacks-accessories?id=1006222',
            "category": 'boys-backpacks-accessories',
            "department": 'boys-backpacks-accessories',
        },
    },
    'boys-coats-jackets': {
        'boys-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/boys-coats-jackets?id=1213062',
            "category": 'boys-coats-jackets',
            "department": 'boys-coats-jackets',
        },
    },
    'bquick': {
        'bquick': {
            "url": 'https://www.bloomingdales.com/shop/bquick?id=6721',
            "category": 'bquick',
            "department": 'bquick',
        },
    },
    'brand-spotlight-melissa-doug': {
        'brand-spotlight-melissa-doug': {
            "url": 'https://www.bloomingdales.com/shop/brand-spotlight-melissa-doug?id=1292301',
            "category": 'brand-spotlight-melissa-doug',
            "department": 'brand-spotlight-melissa-doug',
        },
    },
    'bras': {
        'bras': {
            "url": 'https://www.bloomingdales.com/shop/bras?id=4358',
            "category": 'bras',
            "department": 'bras',
        },
    },
    'briggs-riley': {
        'briggs-riley': {
            "url": 'https://www.bloomingdales.com/shop/briggs-riley?id=1236859',
            "category": 'briggs-riley',
            "department": 'briggs-riley',
        },
    },
    'brioni': {
        'brioni': {
            "url": 'https://www.bloomingdales.com/shop/brioni?id=1333695',
            "category": 'brioni',
            "department": 'brioni',
        },
    },
    'brunello-cucinelli': {
        'brunello-cucinelli': {
            "url": 'https://www.bloomingdales.com/shop/brunello-cucinelli?id=1312698',
            "category": 'brunello-cucinelli',
            "department": 'brunello-cucinelli',
        },
    },
    'bumble-and-bumble': {
        'bumble-and-bumble': {
            "url": 'https://www.bloomingdales.com/shop/bumble-and-bumble?id=1318395',
            "category": 'bumble-and-bumble',
            "department": 'bumble-and-bumble',
        },
    },
    'burberry': {
        'burberry': {
            "url": 'https://www.bloomingdales.com/shop/burberry?id=1002874',
            "category": 'burberry',
            "department": 'burberry',
        },
        'burberry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/burberry/accessories?id=1002878',
            "category": 'burberry-accessories',
            "department": 'burberry',
        },
        'burberry-beauty-makeup': {
            "url": 'https://www.bloomingdales.com/shop/burberry/beauty-makeup?id=1002879',
            "category": 'burberry-beauty-makeup',
            "department": 'burberry',
        },
        'burberry-burberry-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/burberry/burberry-womens-clothing?id=1250195',
            "category": 'burberry-burberry-womens-clothing',
            "department": 'burberry',
        },
        'burberry-burberry-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/burberry/burberry-womens-shoes?id=1002876',
            "category": 'burberry-burberry-womens-shoes',
            "department": 'burberry',
        },
        'burberry-kids-clothing': {
            "url": 'https://www.bloomingdales.com/shop/burberry/kids-clothing?id=1002881',
            "category": 'burberry-kids-clothing',
            "department": 'burberry',
        },
        'burberry-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/burberry/mens-clothing?id=1250897',
            "category": 'burberry-mens-clothing',
            "department": 'burberry',
        },
        'burberry-mens-clothing-cologne': {
            "url": 'https://www.bloomingdales.com/shop/burberry/mens-clothing-cologne?id=1002880',
            "category": 'burberry-mens-clothing-cologne',
            "department": 'burberry',
        },
        'burberry-mens-wallets-ties-accessories': {
            "url": 'https://www.bloomingdales.com/shop/burberry/mens-wallets-ties-accessories?id=1012560',
            "category": 'burberry-mens-wallets-ties-accessories',
            "department": 'burberry',
        },
        'burberry-sale': {
            "url": 'https://www.bloomingdales.com/shop/burberry/sale?id=1319635',
            "category": 'burberry-sale',
            "department": 'burberry',
        },
        'burberry-scarves': {
            "url": 'https://www.bloomingdales.com/shop/burberry/scarves?id=1293495',
            "category": 'burberry-scarves',
            "department": 'burberry',
        },
        'burberry-shoes': {
            "url": 'https://www.bloomingdales.com/shop/burberry/shoes?id=1067259',
            "category": 'burberry-shoes',
            "department": 'burberry',
        },
        'burberry-women': {
            "url": 'https://www.bloomingdales.com/shop/burberry/women?id=1177764',
            "category": 'burberry-women',
            "department": 'burberry',
        },
        'burberry-womens-handbags': {
            "url": 'https://www.bloomingdales.com/shop/burberry/womens-handbags?id=1002877',
            "category": 'burberry-womens-handbags',
            "department": 'burberry',
        },
    },
    'bvallclothing': {
        'bvallclothing': {
            "url": 'https://www.bloomingdales.com/shop/bvallclothing?id=1066659',
            "category": 'bvallclothing',
            "department": 'bvallclothing',
        },
    },
    'bvbakeware': {
        'bvbakeware': {
            "url": 'https://www.bloomingdales.com/shop/bvbakeware?id=1065861',
            "category": 'bvbakeware',
            "department": 'bvbakeware',
        },
    },
    'bvcoats': {
        'bvcoats': {
            "url": 'https://www.bloomingdales.com/shop/bvcoats?id=1065259',
            "category": 'bvcoats',
            "department": 'bvcoats',
        },
    },
    'bvcutleryknives': {
        'bvcutleryknives': {
            "url": 'https://www.bloomingdales.com/shop/bvcutleryknives?id=1065862',
            "category": 'bvcutleryknives',
            "department": 'bvcutleryknives',
        },
    },
    'bvcwaccessories': {
        'bvcwaccessories': {
            "url": 'https://www.bloomingdales.com/shop/bvcwaccessories?id=1065868',
            "category": 'bvcwaccessories',
            "department": 'bvcwaccessories',
        },
    },
    'bvdresses': {
        'bvdresses': {
            "url": 'https://www.bloomingdales.com/shop/bvdresses?id=1065870',
            "category": 'bvdresses',
            "department": 'bvdresses',
        },
    },
    'bveyemakeup': {
        'bveyemakeup': {
            "url": 'https://www.bloomingdales.com/shop/bveyemakeup?id=1065860',
            "category": 'bveyemakeup',
            "department": 'bveyemakeup',
        },
    },
    'bvfoodbeverage': {
        'bvfoodbeverage': {
            "url": 'https://www.bloomingdales.com/shop/bvfoodbeverage?id=1065865',
            "category": 'bvfoodbeverage',
            "department": 'bvfoodbeverage',
        },
    },
    'bvfoundationconcealer': {
        'bvfoundationconcealer': {
            "url": 'https://www.bloomingdales.com/shop/bvfoundationconcealer?id=1066660',
            "category": 'bvfoundationconcealer',
            "department": 'bvfoundationconcealer',
        },
    },
    'bvhaircare': {
        'bvhaircare': {
            "url": 'https://www.bloomingdales.com/shop/bvhaircare?id=1065859',
            "category": 'bvhaircare',
            "department": 'bvhaircare',
        },
    },
    'bvkitchenelectrics': {
        'bvkitchenelectrics': {
            "url": 'https://www.bloomingdales.com/shop/bvkitchenelectrics?id=1065863',
            "category": 'bvkitchenelectrics',
            "department": 'bvkitchenelectrics',
        },
    },
    'bvlips': {
        'bvlips': {
            "url": 'https://www.bloomingdales.com/shop/bvlips?id=1065260',
            "category": 'bvlips',
            "department": 'bvlips',
        },
    },
    'bvmattressespillows': {
        'bvmattressespillows': {
            "url": 'https://www.bloomingdales.com/shop/bvmattressespillows?id=1065866',
            "category": 'bvmattressespillows',
            "department": 'bvmattressespillows',
        },
    },
    'bvperfumescandles': {
        'bvperfumescandles': {
            "url": 'https://www.bloomingdales.com/shop/bvperfumescandles?id=1065867',
            "category": 'bvperfumescandles',
            "department": 'bvperfumescandles',
        },
    },
    'bvshoes': {
        'bvshoes': {
            "url": 'https://www.bloomingdales.com/shop/bvshoes?id=1065869',
            "category": 'bvshoes',
            "department": 'bvshoes',
        },
    },
    'bvtabletopglassware': {
        'bvtabletopglassware': {
            "url": 'https://www.bloomingdales.com/shop/bvtabletopglassware?id=1065864',
            "category": 'bvtabletopglassware',
            "department": 'bvtabletopglassware',
        },
    },
    'byredo': {
        'byredo': {
            "url": 'https://www.bloomingdales.com/shop/byredo?id=1283822',
            "category": 'byredo',
            "department": 'byredo',
        },
        'byredo-bal-dafrique': {
            "url": 'https://www.bloomingdales.com/shop/byredo/bal-dafrique?id=1283826',
            "category": 'byredo-bal-dafrique',
            "department": 'byredo',
        },
        'byredo-blanche': {
            "url": 'https://www.bloomingdales.com/shop/byredo/blanche?id=1283828',
            "category": 'byredo-blanche',
            "department": 'byredo',
        },
        'byredo-gypsy-water': {
            "url": 'https://www.bloomingdales.com/shop/byredo/gypsy-water?id=1283825',
            "category": 'byredo-gypsy-water',
            "department": 'byredo',
        },
        'byredo-mojave-ghost': {
            "url": 'https://www.bloomingdales.com/shop/byredo/mojave-ghost?id=1283824',
            "category": 'byredo-mojave-ghost',
            "department": 'byredo',
        },
        'byredo-rose-of-no-mans-land': {
            "url": 'https://www.bloomingdales.com/shop/byredo/rose-of-no-mans-land?id=1283827',
            "category": 'byredo-rose-of-no-mans-land',
            "department": 'byredo',
        },
        'byredo-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/byredo/shop-all?id=1283823',
            "category": 'byredo-shop-all',
            "department": 'byredo',
        },
    },
    'c-by-bloomingdales': {
        'c-by-bloomingdales': {
            "url": 'https://www.bloomingdales.com/shop/c-by-bloomingdales?id=1003697',
            "category": 'c-by-bloomingdales',
            "department": 'c-by-bloomingdales',
        },
    },
    'california-coastal': {
        'california-coastal': {
            "url": 'https://www.bloomingdales.com/shop/california-coastal?id=1307402',
            "category": 'california-coastal',
            "department": 'california-coastal',
        },
        'california-coastal-california-brands': {
            "url": 'https://www.bloomingdales.com/shop/california-coastal/california-brands?id=1307403',
            "category": 'california-coastal-california-brands',
            "department": 'california-coastal',
        },
        'california-coastal-golden-hour-glow': {
            "url": 'https://www.bloomingdales.com/shop/california-coastal/golden-hour-glow?id=1307406',
            "category": 'california-coastal-golden-hour-glow',
            "department": 'california-coastal',
        },
        'california-coastal-haircare': {
            "url": 'https://www.bloomingdales.com/shop/california-coastal/haircare?id=1307405',
            "category": 'california-coastal-haircare',
            "department": 'california-coastal',
        },
        'california-coastal-spf': {
            "url": 'https://www.bloomingdales.com/shop/california-coastal/spf?id=1307404',
            "category": 'california-coastal-spf',
            "department": 'california-coastal',
        },
        'california-coastal-vacation-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/california-coastal/vacation-fragrances?id=1307407',
            "category": 'california-coastal-vacation-fragrances',
            "department": 'california-coastal',
        },
    },
    'camisoles-slips': {
        'camisoles-slips': {
            "url": 'https://www.bloomingdales.com/shop/camisoles-slips?id=22880',
            "category": 'camisoles-slips',
            "department": 'camisoles-slips',
        },
    },
    'canada-goose': {
        'canada-goose': {
            "url": 'https://www.bloomingdales.com/shop/canada-goose?id=1004024',
            "category": 'canada-goose',
            "department": 'canada-goose',
        },
        'canada-goose-kids-jackets-parkas': {
            "url": 'https://www.bloomingdales.com/shop/canada-goose/kids-jackets-parkas?id=1004028',
            "category": 'canada-goose-kids-jackets-parkas',
            "department": 'canada-goose',
        },
        'canada-goose-mens-jackets-parkas-vests': {
            "url": 'https://www.bloomingdales.com/shop/canada-goose/mens-jackets-parkas-vests?id=1004027',
            "category": 'canada-goose-mens-jackets-parkas-vests',
            "department": 'canada-goose',
        },
        'canada-goose-womens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/canada-goose/womens-accessories?id=1047359',
            "category": 'canada-goose-womens-accessories',
            "department": 'canada-goose',
        },
        'canada-goose-womens-clothing-jackets-parkas': {
            "url": 'https://www.bloomingdales.com/shop/canada-goose/womens-clothing-jackets-parkas?id=1004025',
            "category": 'canada-goose-womens-clothing-jackets-parkas',
            "department": 'canada-goose',
        },
    },
    'candles': {
        'candles': {
            "url": 'https://www.bloomingdales.com/shop/candles?id=1325225',
            "category": 'candles',
            "department": 'candles',
        },
    },
    'candles-home-scents': {
        'candles-home-scents-all-candles-home-scents': {
            "url": 'https://www.bloomingdales.com/shop/candles-home-scents/all-candles-home-scents?id=1236263',
            "category": 'candles-home-scents-all-candles-home-scents',
            "department": 'candles-home-scents',
        },
    },
    'capucine-de-wulf': {
        'capucine-de-wulf': {
            "url": 'https://www.bloomingdales.com/shop/capucine-de-wulf?id=1333001',
            "category": 'capucine-de-wulf',
            "department": 'capucine-de-wulf',
        },
    },
    'caracole': {
        'caracole': {
            "url": 'https://www.bloomingdales.com/shop/caracole?id=1268498',
            "category": 'caracole',
            "department": 'caracole',
        },
    },
    'carolina-herrera': {
        'carolina-herrera': {
            "url": 'https://www.bloomingdales.com/shop/carolina-herrera?id=1283816',
            "category": 'carolina-herrera',
            "department": 'carolina-herrera',
        },
        'carolina-herrera-bad-boy-cologne': {
            "url": 'https://www.bloomingdales.com/shop/carolina-herrera/bad-boy-cologne?id=1283819',
            "category": 'carolina-herrera-bad-boy-cologne',
            "department": 'carolina-herrera',
        },
        'carolina-herrera-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/carolina-herrera/gift-sets?id=1283820',
            "category": 'carolina-herrera-gift-sets',
            "department": 'carolina-herrera',
        },
        'carolina-herrera-good-girl-perfume': {
            "url": 'https://www.bloomingdales.com/shop/carolina-herrera/good-girl-perfume?id=1283818',
            "category": 'carolina-herrera-good-girl-perfume',
            "department": 'carolina-herrera',
        },
        'carolina-herrera-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/carolina-herrera/shop-all?id=1283817',
            "category": 'carolina-herrera-shop-all',
            "department": 'carolina-herrera',
        },
        'carolina-herrera-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/carolina-herrera/womens-clothing?id=1283821',
            "category": 'carolina-herrera-womens-clothing',
            "department": 'carolina-herrera',
        },
    },
    'cartier': {
        'cartier': {
            "url": 'https://www.bloomingdales.com/shop/cartier?id=1264995',
            "category": 'cartier',
            "department": 'cartier',
        },
    },
    'casablanca': {
        'casablanca': {
            "url": 'https://www.bloomingdales.com/shop/casablanca?id=1327295',
            "category": 'casablanca',
            "department": 'casablanca',
        },
        'casablanca-kids': {
            "url": 'https://www.bloomingdales.com/shop/casablanca/kids?id=1327301',
            "category": 'casablanca-kids',
            "department": 'casablanca',
        },
        'casablanca-men': {
            "url": 'https://www.bloomingdales.com/shop/casablanca/men?id=1327300',
            "category": 'casablanca-men',
            "department": 'casablanca',
        },
        'casablanca-women': {
            "url": 'https://www.bloomingdales.com/shop/casablanca/women?id=1327299',
            "category": 'casablanca-women',
            "department": 'casablanca',
        },
    },
    'casual-dress-sneakers': {
        'casual-dress-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/casual-dress-sneakers?id=1027044',
            "category": 'casual-dress-sneakers',
            "department": 'casual-dress-sneakers',
        },
    },
    'casual-pants': {
        'casual-pants': {
            "url": 'https://www.bloomingdales.com/shop/casual-pants?id=1027027',
            "category": 'casual-pants',
            "department": 'casual-pants',
        },
    },
    'category-name-here': {
        'category-name-here': {
            "url": 'https://www.bloomingdales.com/shop/category-name-here?id=1002663',
            "category": 'category-name-here',
            "department": 'category-name-here',
        },
    },
    'celine': {
        'celine': {
            "url": 'https://www.bloomingdales.com/shop/celine?id=1250099',
            "category": 'celine',
            "department": 'celine',
        },
    },
    'chain-pearls': {
        'chain-pearls': {
            "url": 'https://www.bloomingdales.com/shop/chain-pearls?id=19446',
            "category": 'chain-pearls',
            "department": 'chain-pearls',
        },
    },
    'chains-charms': {
        'chains-charms': {
            "url": 'https://www.bloomingdales.com/shop/chains-charms?id=20139',
            "category": 'chains-charms',
            "department": 'chains-charms',
        },
    },
    'chanel': {
        'chanel': {
            "url": 'https://www.bloomingdales.com/shop/chanel?id=1000926',
            "category": 'chanel',
            "department": 'chanel',
        },
        'chanel-allure-homme-sport': {
            "url": 'https://www.bloomingdales.com/shop/chanel/allure-homme-sport?id=1001281',
            "category": 'chanel-allure-homme-sport',
            "department": 'chanel',
        },
        'chanel-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/chanel/best-sellers?id=1314203',
            "category": 'chanel-best-sellers',
            "department": 'chanel',
        },
        'chanel-chanel-allure': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-allure?id=1001074',
            "category": 'chanel-chanel-allure',
            "department": 'chanel',
        },
        'chanel-chanel-bleu-de-chanel': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-bleu-de-chanel?id=1001151',
            "category": 'chanel-chanel-bleu-de-chanel',
            "department": 'chanel',
        },
        'chanel-chanel-brushes-accessories': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-brushes-accessories?id=1001105',
            "category": 'chanel-chanel-brushes-accessories',
            "department": 'chanel',
        },
        'chanel-chanel-chance': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-chance?id=1001071',
            "category": 'chanel-chanel-chance',
            "department": 'chanel',
        },
        'chanel-chanel-chance-eau-fraiche': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-chance-eau-fraiche?id=1001072',
            "category": 'chanel-chanel-chance-eau-fraiche',
            "department": 'chanel',
        },
        'chanel-chanel-chance-eau-tendre': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-chance-eau-tendre?id=1001073',
            "category": 'chanel-chanel-chance-eau-tendre',
            "department": 'chanel',
        },
        'chanel-chanel-coco': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-coco?id=1001075',
            "category": 'chanel-chanel-coco',
            "department": 'chanel',
        },
        'chanel-chanel-coco-mademoiselle': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-coco-mademoiselle?id=1001076',
            "category": 'chanel-chanel-coco-mademoiselle',
            "department": 'chanel',
        },
        'chanel-chanel-eyes': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-eyes?id=1001103',
            "category": 'chanel-chanel-eyes',
            "department": 'chanel',
        },
        'chanel-chanel-face': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-face?id=1001102',
            "category": 'chanel-chanel-face',
            "department": 'chanel',
        },
        'chanel-chanel-hydra-beauty': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-hydra-beauty?id=1001110',
            "category": 'chanel-chanel-hydra-beauty',
            "department": 'chanel',
        },
        'chanel-chanel-lips': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-lips?id=1001104',
            "category": 'chanel-chanel-lips',
            "department": 'chanel',
        },
        'chanel-chanel-makeup-cosmetics': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-makeup-cosmetics?id=1001022',
            "category": 'chanel-chanel-makeup-cosmetics',
            "department": 'chanel',
        },
        'chanel-chanel-mens-cologne-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-mens-cologne-fragrances?id=1001021',
            "category": 'chanel-chanel-mens-cologne-fragrances',
            "department": 'chanel',
        },
        'chanel-chanel-n1': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-n1?id=1266996',
            "category": 'chanel-chanel-n1',
            "department": 'chanel',
        },
        'chanel-chanel-n5': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-n5?id=1001070',
            "category": 'chanel-chanel-n5',
            "department": 'chanel',
        },
        'chanel-chanel-new-makeup': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-new-makeup?id=1001019',
            "category": 'chanel-chanel-new-makeup',
            "department": 'chanel',
        },
        'chanel-chanel-platinum-egoiste': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-platinum-egoiste?id=1001154',
            "category": 'chanel-chanel-platinum-egoiste',
            "department": 'chanel',
        },
        'chanel-chanel-skincare-cream': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-skincare-cream?id=1001023',
            "category": 'chanel-chanel-skincare-cream',
            "department": 'chanel',
        },
        'chanel-chanel-sublimage': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-sublimage?id=1001108',
            "category": 'chanel-chanel-sublimage',
            "department": 'chanel',
        },
        'chanel-chanel-womens-perfume-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/chanel/chanel-womens-perfume-fragrances?id=1001020',
            "category": 'chanel-chanel-womens-perfume-fragrances',
            "department": 'chanel',
        },
        'chanel-gabrielle-chanel': {
            "url": 'https://www.bloomingdales.com/shop/chanel/gabrielle-chanel?id=1039659',
            "category": 'chanel-gabrielle-chanel',
            "department": 'chanel',
        },
        'chanel-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/chanel/gift-sets?id=1299395',
            "category": 'chanel-gift-sets',
            "department": 'chanel',
        },
        'chanel-la-solution-10-de-chanel': {
            "url": 'https://www.bloomingdales.com/shop/chanel/la-solution-10-de-chanel?id=1005320',
            "category": 'chanel-la-solution-10-de-chanel',
            "department": 'chanel',
        },
        'chanel-le-lift': {
            "url": 'https://www.bloomingdales.com/shop/chanel/le-lift?id=1002098',
            "category": 'chanel-le-lift',
            "department": 'chanel',
        },
        'chanel-les-eaux-de-chanel': {
            "url": 'https://www.bloomingdales.com/shop/chanel/les-eaux-de-chanel?id=1227960',
            "category": 'chanel-les-eaux-de-chanel',
            "department": 'chanel',
        },
        'chanel-shop-all-chanel': {
            "url": 'https://www.bloomingdales.com/shop/chanel/shop-all-chanel?id=1208359',
            "category": 'chanel-shop-all-chanel',
            "department": 'chanel',
        },
    },
    'chanel-brushes-accessories': {
        'chanel-brushes-accessories': {
            "url": 'https://www.bloomingdales.com/shop/chanel-brushes-accessories?id=1208364',
            "category": 'chanel-brushes-accessories',
            "department": 'chanel-brushes-accessories',
        },
    },
    'chanel-eyes': {
        'chanel-eyes': {
            "url": 'https://www.bloomingdales.com/shop/chanel-eyes?id=1208362',
            "category": 'chanel-eyes',
            "department": 'chanel-eyes',
        },
    },
    'chanel-face': {
        'chanel-face': {
            "url": 'https://www.bloomingdales.com/shop/chanel-face?id=1208361',
            "category": 'chanel-face',
            "department": 'chanel-face',
        },
    },
    'chanel-lips': {
        'chanel-lips': {
            "url": 'https://www.bloomingdales.com/shop/chanel-lips?id=1208363',
            "category": 'chanel-lips',
            "department": 'chanel-lips',
        },
    },
    'charlotte-tilbury': {
        'charlotte-tilbury': {
            "url": 'https://www.bloomingdales.com/shop/charlotte-tilbury?id=1191760',
            "category": 'charlotte-tilbury',
            "department": 'charlotte-tilbury',
        },
        'charlotte-tilbury-all-makeup': {
            "url": 'https://www.bloomingdales.com/shop/charlotte-tilbury/all-makeup?id=1191761',
            "category": 'charlotte-tilbury-all-makeup',
            "department": 'charlotte-tilbury',
        },
        'charlotte-tilbury-eye-makeup': {
            "url": 'https://www.bloomingdales.com/shop/charlotte-tilbury/eye-makeup?id=1306895',
            "category": 'charlotte-tilbury-eye-makeup',
            "department": 'charlotte-tilbury',
        },
        'charlotte-tilbury-face-makeup': {
            "url": 'https://www.bloomingdales.com/shop/charlotte-tilbury/face-makeup?id=1306795',
            "category": 'charlotte-tilbury-face-makeup',
            "department": 'charlotte-tilbury',
        },
        'charlotte-tilbury-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/charlotte-tilbury/fragrance?id=1237271',
            "category": 'charlotte-tilbury-fragrance',
            "department": 'charlotte-tilbury',
        },
        'charlotte-tilbury-lip-makeup': {
            "url": 'https://www.bloomingdales.com/shop/charlotte-tilbury/lip-makeup?id=1306796',
            "category": 'charlotte-tilbury-lip-makeup',
            "department": 'charlotte-tilbury',
        },
        'charlotte-tilbury-skincare': {
            "url": 'https://www.bloomingdales.com/shop/charlotte-tilbury/skincare?id=1191762',
            "category": 'charlotte-tilbury-skincare',
            "department": 'charlotte-tilbury',
        },
    },
    'chiara-boni-la-petite-robe': {
        'chiara-boni-la-petite-robe': {
            "url": 'https://www.bloomingdales.com/shop/chiara-boni-la-petite-robe?id=1308199',
            "category": 'chiara-boni-la-petite-robe',
            "department": 'chiara-boni-la-petite-robe',
        },
    },
    'chloe': {
        'chloe': {
            "url": 'https://www.bloomingdales.com/shop/chloe?id=1061960',
            "category": 'chloe',
            "department": 'chloe',
        },
        'chloe-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/chloe/fragrance?id=1229864',
            "category": 'chloe-fragrance',
            "department": 'chloe',
        },
        'chloe-handbags': {
            "url": 'https://www.bloomingdales.com/shop/chloe/handbags?id=1229860',
            "category": 'chloe-handbags',
            "department": 'chloe',
        },
        'chloe-kids': {
            "url": 'https://www.bloomingdales.com/shop/chloe/kids?id=1229863',
            "category": 'chloe-kids',
            "department": 'chloe',
        },
        'chloe-sale': {
            "url": 'https://www.bloomingdales.com/shop/chloe/sale?id=1319600',
            "category": 'chloe-sale',
            "department": 'chloe',
        },
        'chloe-shoes': {
            "url": 'https://www.bloomingdales.com/shop/chloe/shoes?id=1229861',
            "category": 'chloe-shoes',
            "department": 'chloe',
        },
        'chloe-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/chloe/sunglasses?id=1229862',
            "category": 'chloe-sunglasses',
            "department": 'chloe',
        },
    },
    'chocolate-brown': {
        'chocolate-brown': {
            "url": 'https://www.bloomingdales.com/shop/chocolate-brown?id=1242795',
            "category": 'chocolate-brown',
            "department": 'chocolate-brown',
        },
    },
    'christian-louboutin': {
        'christian-louboutin': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin?id=1286901',
            "category": 'christian-louboutin',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-beauty': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/beauty?id=1320701',
            "category": 'christian-louboutin-beauty',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/best-sellers?id=1293111',
            "category": 'christian-louboutin-best-sellers',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/fragrance?id=1286903',
            "category": 'christian-louboutin-fragrance',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-handbags': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/handbags?id=1320697',
            "category": 'christian-louboutin-handbags',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-kids': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/kids?id=1320700',
            "category": 'christian-louboutin-kids',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-makeup': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/makeup?id=1293110',
            "category": 'christian-louboutin-makeup',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/mens-accessories?id=1320699',
            "category": 'christian-louboutin-mens-accessories',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/mens-shoes?id=1320698',
            "category": 'christian-louboutin-mens-shoes',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/sunglasses?id=1286904',
            "category": 'christian-louboutin-sunglasses',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-womens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/womens-accessories?id=1320696',
            "category": 'christian-louboutin-womens-accessories',
            "department": 'christian-louboutin',
        },
        'christian-louboutin-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/christian-louboutin/womens-shoes?id=1320695',
            "category": 'christian-louboutin-womens-shoes',
            "department": 'christian-louboutin',
        },
    },
    'christofle': {
        'christofle': {
            "url": 'https://www.bloomingdales.com/shop/christofle?id=1236759',
            "category": 'christofle',
            "department": 'christofle',
        },
    },
    'christy': {
        'christy': {
            "url": 'https://www.bloomingdales.com/shop/christy?id=1288595',
            "category": 'christy',
            "department": 'christy',
        },
    },
    'cinq-a-sept': {
        'cinq-a-sept': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept?id=1234974',
            "category": 'cinq-a-sept',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-blazers': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/blazers?id=1267497',
            "category": 'cinq-a-sept-blazers',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-dresses': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/dresses?id=1267496',
            "category": 'cinq-a-sept-dresses',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-jeans': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/jeans?id=1267501',
            "category": 'cinq-a-sept-jeans',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-pants': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/pants?id=1267500',
            "category": 'cinq-a-sept-pants',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-sale': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/sale?id=1267503',
            "category": 'cinq-a-sept-sale',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-shoes': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/shoes?id=1274299',
            "category": 'cinq-a-sept-shoes',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-shorts': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/shorts?id=1267502',
            "category": 'cinq-a-sept-shorts',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-skirts': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/skirts?id=1267498',
            "category": 'cinq-a-sept-skirts',
            "department": 'cinq-a-sept',
        },
        'cinq-a-sept-tops': {
            "url": 'https://www.bloomingdales.com/shop/cinq-a-sept/tops?id=1267499',
            "category": 'cinq-a-sept-tops',
            "department": 'cinq-a-sept',
        },
    },
    'clarins': {
        'clarins': {
            "url": 'https://www.bloomingdales.com/shop/clarins?id=1263710',
            "category": 'clarins',
            "department": 'clarins',
        },
    },
    'classic-americana': {
        'classic-americana': {
            "url": 'https://www.bloomingdales.com/shop/classic-americana?id=1239760',
            "category": 'classic-americana',
            "department": 'classic-americana',
        },
    },
    'cle-de-peau-beaute': {
        'cle-de-peau-beaute': {
            "url": 'https://www.bloomingdales.com/shop/cle-de-peau-beaute?id=1331001',
            "category": 'cle-de-peau-beaute',
            "department": 'cle-de-peau-beaute',
        },
        'cle-de-peau-beaute-cle-de-peau-beaute-cleansers': {
            "url": 'https://www.bloomingdales.com/shop/cle-de-peau-beaute/cle-de-peau-beaute-cleansers?id=1332104',
            "category": 'cle-de-peau-beaute-cle-de-peau-beaute-cleansers',
            "department": 'cle-de-peau-beaute',
        },
        'cle-de-peau-beaute-cle-de-peau-beaute-face-makeup': {
            "url": 'https://www.bloomingdales.com/shop/cle-de-peau-beaute/cle-de-peau-beaute-face-makeup?id=1332100',
            "category": 'cle-de-peau-beaute-cle-de-peau-beaute-face-makeup',
            "department": 'cle-de-peau-beaute',
        },
        'cle-de-peau-beaute-cle-de-peau-beaute-lip-makeup': {
            "url": 'https://www.bloomingdales.com/shop/cle-de-peau-beaute/cle-de-peau-beaute-lip-makeup?id=1332105',
            "category": 'cle-de-peau-beaute-cle-de-peau-beaute-lip-makeup',
            "department": 'cle-de-peau-beaute',
        },
        'cle-de-peau-beaute-cle-de-peau-beaute-moisturizers': {
            "url": 'https://www.bloomingdales.com/shop/cle-de-peau-beaute/cle-de-peau-beaute-moisturizers?id=1332103',
            "category": 'cle-de-peau-beaute-cle-de-peau-beaute-moisturizers',
            "department": 'cle-de-peau-beaute',
        },
        'cle-de-peau-beaute-cle-de-peau-beaute-serums-and-toners': {
            "url": 'https://www.bloomingdales.com/shop/cle-de-peau-beaute/cle-de-peau-beaute-serums-and-toners?id=1332102',
            "category": 'cle-de-peau-beaute-cle-de-peau-beaute-serums-and-toners',
            "department": 'cle-de-peau-beaute',
        },
    },
    'clinique': {
        'clinique': {
            "url": 'https://www.bloomingdales.com/shop/clinique?id=1193859',
            "category": 'clinique',
            "department": 'clinique',
        },
        'clinique-black-honey': {
            "url": 'https://www.bloomingdales.com/shop/clinique/black-honey?id=1312197',
            "category": 'clinique-black-honey',
            "department": 'clinique',
        },
        'clinique-clinique-fragrances-perfume': {
            "url": 'https://www.bloomingdales.com/shop/clinique/clinique-fragrances-perfume?id=7514',
            "category": 'clinique-clinique-fragrances-perfume',
            "department": 'clinique',
        },
        'clinique-clinique-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/clinique/clinique-gift-sets?id=1002464',
            "category": 'clinique-clinique-gift-sets',
            "department": 'clinique',
        },
        'clinique-clinique-makeup-cosmetics': {
            "url": 'https://www.bloomingdales.com/shop/clinique/clinique-makeup-cosmetics?id=7512',
            "category": 'clinique-clinique-makeup-cosmetics',
            "department": 'clinique',
        },
        'clinique-clinique-skin-care-products': {
            "url": 'https://www.bloomingdales.com/shop/clinique/clinique-skin-care-products?id=7511',
            "category": 'clinique-clinique-skin-care-products',
            "department": 'clinique',
        },
        'clinique-happy-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/clinique/happy-fragrance?id=1312196',
            "category": 'clinique-happy-fragrance',
            "department": 'clinique',
        },
        'clinique-moisture-surge': {
            "url": 'https://www.bloomingdales.com/shop/clinique/moisture-surge?id=1312195',
            "category": 'clinique-moisture-surge',
            "department": 'clinique',
        },
    },
    'clinique-fragrances-perfume': {
        'clinique-fragrances-perfume': {
            "url": 'https://www.bloomingdales.com/shop/clinique-fragrances-perfume?id=1269461',
            "category": 'clinique-fragrances-perfume',
            "department": 'clinique-fragrances-perfume',
        },
    },
    'clinique-makeup-cosmetics': {
        'clinique-makeup-cosmetics': {
            "url": 'https://www.bloomingdales.com/shop/clinique-makeup-cosmetics?id=1269444',
            "category": 'clinique-makeup-cosmetics',
            "department": 'clinique-makeup-cosmetics',
        },
    },
    'clinique-skin-care-products': {
        'clinique-skin-care-products': {
            "url": 'https://www.bloomingdales.com/shop/clinique-skin-care-products?id=1269432',
            "category": 'clinique-skin-care-products',
            "department": 'clinique-skin-care-products',
        },
    },
    'clone-designer-sale': {
        'clone-designer-sale-accessories': {
            "url": 'https://www.bloomingdales.com/shop/clone-designer-sale/accessories?id=1301610',
            "category": 'clone-designer-sale-accessories',
            "department": 'clone-designer-sale',
        },
        'clone-designer-sale-designer-private-sale': {
            "url": 'https://www.bloomingdales.com/shop/clone-designer-sale/designer-private-sale?id=1301603',
            "category": 'clone-designer-sale-designer-private-sale',
            "department": 'clone-designer-sale',
        },
        'clone-designer-sale-the-designer-event': {
            "url": 'https://www.bloomingdales.com/shop/clone-designer-sale/the-designer-event?id=1301598',
            "category": 'clone-designer-sale-the-designer-event',
            "department": 'clone-designer-sale',
        },
    },
    'clone-new-noteworthy': {
        'clone-new-noteworthy-best-selling': {
            "url": 'https://www.bloomingdales.com/shop/clone-new-noteworthy/best-selling?id=1151603',
            "category": 'clone-new-noteworthy-best-selling',
            "department": 'clone-new-noteworthy',
        },
        'clone-new-noteworthy-shoes-under-200': {
            "url": 'https://www.bloomingdales.com/shop/clone-new-noteworthy/shoes-under-200?id=1151604',
            "category": 'clone-new-noteworthy-shoes-under-200',
            "department": 'clone-new-noteworthy',
        },
    },
    'clubhouse-chic': {
        'clubhouse-chic': {
            "url": 'https://www.bloomingdales.com/shop/clubhouse-chic?id=1303798',
            "category": 'clubhouse-chic',
            "department": 'clubhouse-chic',
        },
    },
    'coach': {
        'coach': {
            "url": 'https://www.bloomingdales.com/shop/coach?id=1004771',
            "category": 'coach',
            "department": 'coach',
        },
        'coach-coach-shoes': {
            "url": 'https://www.bloomingdales.com/shop/coach/coach-shoes?id=1001878',
            "category": 'coach-coach-shoes',
            "department": 'coach',
        },
        'coach-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/coach/fragrances?id=1291605',
            "category": 'coach-fragrances',
            "department": 'coach',
        },
        'coach-handbags-wallets': {
            "url": 'https://www.bloomingdales.com/shop/coach/handbags-wallets?id=1004772',
            "category": 'coach-handbags-wallets',
            "department": 'coach',
        },
        'coach-mens-accessories-shoes': {
            "url": 'https://www.bloomingdales.com/shop/coach/mens-accessories-shoes?id=1005128',
            "category": 'coach-mens-accessories-shoes',
            "department": 'coach',
        },
        'coach-watches': {
            "url": 'https://www.bloomingdales.com/shop/coach/watches?id=1006885',
            "category": 'coach-watches',
            "department": 'coach',
        },
        'coach-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/coach/womens-shoes?id=1004773',
            "category": 'coach-womens-shoes',
            "department": 'coach',
        },
    },
    'coastal-glam': {
        'coastal-glam': {
            "url": 'https://www.bloomingdales.com/shop/coastal-glam?id=1303795',
            "category": 'coastal-glam',
            "department": 'coastal-glam',
        },
    },
    'coats-jackets': {
        'coats-jackets-coats-under-200': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/coats-under-200?id=1078261',
            "category": 'coats-jackets-coats-under-200',
            "department": 'coats-jackets',
        },
        'coats-jackets-down-alternative-coats-puffer-jackets': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/down-alternative-coats-puffer-jackets?id=1078265',
            "category": 'coats-jackets-down-alternative-coats-puffer-jackets',
            "department": 'coats-jackets',
        },
        'coats-jackets-faux-fur-mink-coats': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/faux-fur-mink-coats?id=1078267',
            "category": 'coats-jackets-faux-fur-mink-coats',
            "department": 'coats-jackets',
        },
        'coats-jackets-leather-coats-shearling-coats': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/leather-coats-shearling-coats?id=1078268',
            "category": 'coats-jackets-leather-coats-shearling-coats',
            "department": 'coats-jackets',
        },
        'coats-jackets-vests-fur-denim-vests': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/vests-fur-denim-vests?id=1078264',
            "category": 'coats-jackets-vests-fur-denim-vests',
            "department": 'coats-jackets',
        },
        'coats-jackets-womens-lightweight-jackets': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/womens-lightweight-jackets?id=1078275',
            "category": 'coats-jackets-womens-lightweight-jackets',
            "department": 'coats-jackets',
        },
        'coats-jackets-womens-quilted-jackets-and-coats': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/womens-quilted-jackets-and-coats?id=1078278',
            "category": 'coats-jackets-womens-quilted-jackets-and-coats',
            "department": 'coats-jackets',
        },
        'coats-jackets-womens-utility-jackets-and-denim-jackets': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/womens-utility-jackets-and-denim-jackets?id=1078277',
            "category": 'coats-jackets-womens-utility-jackets-and-denim-jackets',
            "department": 'coats-jackets',
        },
        'coats-jackets-wool-coats-cashmere-coats': {
            "url": 'https://www.bloomingdales.com/shop/coats-jackets/wool-coats-cashmere-coats?id=1078266',
            "category": 'coats-jackets-wool-coats-cashmere-coats',
            "department": 'coats-jackets',
        },
    },
    'collaborations': {
        'collaborations': {
            "url": 'https://www.bloomingdales.com/shop/collaborations?id=1176369',
            "category": 'collaborations',
            "department": 'collaborations',
        },
    },
    'contemporary': {
        'contemporary': {
            "url": 'https://www.bloomingdales.com/shop/contemporary?id=1101367',
            "category": 'contemporary',
            "department": 'contemporary',
        },
    },
    'cool-clogs': {
        'cool-clogs': {
            "url": 'https://www.bloomingdales.com/shop/cool-clogs?id=1135065',
            "category": 'cool-clogs',
            "department": 'cool-clogs',
        },
    },
    'coquette': {
        'coquette': {
            "url": 'https://www.bloomingdales.com/shop/coquette?id=1242695',
            "category": 'coquette',
            "department": 'coquette',
        },
    },
    'creed': {
        'creed': {
            "url": 'https://www.bloomingdales.com/shop/creed?id=1210159',
            "category": 'creed',
            "department": 'creed',
        },
        'creed-amber': {
            "url": 'https://www.bloomingdales.com/shop/creed/amber?id=1245305',
            "category": 'creed-amber',
            "department": 'creed',
        },
        'creed-aventus': {
            "url": 'https://www.bloomingdales.com/shop/creed/aventus?id=1210163',
            "category": 'creed-aventus',
            "department": 'creed',
        },
        'creed-aventus-for-her': {
            "url": 'https://www.bloomingdales.com/shop/creed/aventus-for-her?id=1210164',
            "category": 'creed-aventus-for-her',
            "department": 'creed',
        },
        'creed-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/creed/bath-body?id=1245301',
            "category": 'creed-bath-body',
            "department": 'creed',
        },
        'creed-cologne': {
            "url": 'https://www.bloomingdales.com/shop/creed/cologne?id=1210160',
            "category": 'creed-cologne',
            "department": 'creed',
        },
        'creed-creed-aventus': {
            "url": 'https://www.bloomingdales.com/shop/creed/creed-aventus?id=1279391',
            "category": 'creed-creed-aventus',
            "department": 'creed',
        },
        'creed-creed-silver-mountain-water': {
            "url": 'https://www.bloomingdales.com/shop/creed/creed-silver-mountain-water?id=1279392',
            "category": 'creed-creed-silver-mountain-water',
            "department": 'creed',
        },
        'creed-floral': {
            "url": 'https://www.bloomingdales.com/shop/creed/floral?id=1245303',
            "category": 'creed-floral',
            "department": 'creed',
        },
        'creed-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/creed/fragrances?id=1245310',
            "category": 'creed-fragrances',
            "department": 'creed',
        },
        'creed-fresh': {
            "url": 'https://www.bloomingdales.com/shop/creed/fresh?id=1245304',
            "category": 'creed-fresh',
            "department": 'creed',
        },
        'creed-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/creed/gift-sets?id=1210162',
            "category": 'creed-gift-sets',
            "department": 'creed',
        },
        'creed-home-collection': {
            "url": 'https://www.bloomingdales.com/shop/creed/home-collection?id=1245299',
            "category": 'creed-home-collection',
            "department": 'creed',
        },
        'creed-millesime-imperial': {
            "url": 'https://www.bloomingdales.com/shop/creed/millesime-imperial?id=1210165',
            "category": 'creed-millesime-imperial',
            "department": 'creed',
        },
        'creed-perfume': {
            "url": 'https://www.bloomingdales.com/shop/creed/perfume?id=1210161',
            "category": 'creed-perfume',
            "department": 'creed',
        },
        'creed-woody': {
            "url": 'https://www.bloomingdales.com/shop/creed/woody?id=1245302',
            "category": 'creed-woody',
            "department": 'creed',
        },
    },
    'cuba-travelogue': {
        'cuba-travelogue': {
            "url": 'https://www.bloomingdales.com/shop/cuba-travelogue?id=1006316',
            "category": 'cuba-travelogue',
            "department": 'cuba-travelogue',
        },
    },
    'cult-gaia': {
        'cult-gaia': {
            "url": 'https://www.bloomingdales.com/shop/cult-gaia?id=1265444',
            "category": 'cult-gaia',
            "department": 'cult-gaia',
        },
        'cult-gaia-handbags': {
            "url": 'https://www.bloomingdales.com/shop/cult-gaia/handbags?id=1265445',
            "category": 'cult-gaia-handbags',
            "department": 'cult-gaia',
        },
        'cult-gaia-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/cult-gaia/jewelry-accessories?id=1265447',
            "category": 'cult-gaia-jewelry-accessories',
            "department": 'cult-gaia',
        },
        'cult-gaia-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/cult-gaia/womens-clothing?id=1265448',
            "category": 'cult-gaia-womens-clothing',
            "department": 'cult-gaia',
        },
        'cult-gaia-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/cult-gaia/womens-shoes?id=1265446',
            "category": 'cult-gaia-womens-shoes',
            "department": 'cult-gaia',
        },
    },
    'current-trend-contouring': {
        'current-trend-contouring': {
            "url": 'https://www.bloomingdales.com/shop/current-trend-contouring?id=1005296',
            "category": 'current-trend-contouring',
            "department": 'current-trend-contouring',
        },
    },
    'current-viral-favs': {
        'current-viral-favs': {
            "url": 'https://www.bloomingdales.com/shop/current-viral-favs?id=1275395',
            "category": 'current-viral-favs',
            "department": 'current-viral-favs',
        },
    },
    'customer-top-rated': {
        'customer-top-rated': {
            "url": 'https://www.bloomingdales.com/shop/customer-top-rated?id=1096760',
            "category": 'customer-top-rated',
            "department": 'customer-top-rated',
        },
    },
    'cuyana': {
        'cuyana': {
            "url": 'https://www.bloomingdales.com/shop/cuyana?id=1283995',
            "category": 'cuyana',
            "department": 'cuyana',
        },
    },
    'cybex': {
        'cybex': {
            "url": 'https://www.bloomingdales.com/shop/cybex?id=1304600',
            "category": 'cybex',
            "department": 'cybex',
        },
    },
    'd-p-ghost-category': {
        'd-p-ghost-category': {
            "url": 'https://www.bloomingdales.com/shop/d-p-ghost-category?id=1001501',
            "category": 'd-p-ghost-category',
            "department": 'd-p-ghost-category',
        },
    },
    'dad-me': {
        'dad-me': {
            "url": 'https://www.bloomingdales.com/shop/dad-me?id=1199160',
            "category": 'dad-me',
            "department": 'dad-me',
        },
    },
    'david-webb': {
        'david-webb': {
            "url": 'https://www.bloomingdales.com/shop/david-webb?id=1288697',
            "category": 'david-webb',
            "department": 'david-webb',
        },
    },
    'david-yurman': {
        'david-yurman': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman?id=1040459',
            "category": 'david-yurman',
            "department": 'david-yurman',
        },
        'david-yurman-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/best-sellers?id=1213859',
            "category": 'david-yurman-best-sellers',
            "department": 'david-yurman',
        },
        'david-yurman-cable': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/cable?id=1232259',
            "category": 'david-yurman-cable',
            "department": 'david-yurman',
        },
        'david-yurman-charms-and-amulets': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/charms-and-amulets?id=1179762',
            "category": 'david-yurman-charms-and-amulets',
            "department": 'david-yurman',
        },
        'david-yurman-curb-chain': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/curb-chain?id=1277796',
            "category": 'david-yurman-curb-chain',
            "department": 'david-yurman',
        },
        'david-yurman-david-yurman-pendants': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/david-yurman-pendants?id=1179763',
            "category": 'david-yurman-david-yurman-pendants',
            "department": 'david-yurman',
        },
        'david-yurman-gift': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/gift?id=1249600',
            "category": 'david-yurman-gift',
            "department": 'david-yurman',
        },
        'david-yurman-gifting': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/gifting?id=1180060',
            "category": 'david-yurman-gifting',
            "department": 'david-yurman',
        },
        'david-yurman-luxe-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/luxe-jewelry?id=1279542',
            "category": 'david-yurman-luxe-jewelry',
            "department": 'david-yurman',
        },
        'david-yurman-mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/mens-accessories?id=1002106',
            "category": 'david-yurman-mens-accessories',
            "department": 'david-yurman',
        },
        'david-yurman-mens-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/mens-bracelets?id=1002107',
            "category": 'david-yurman-mens-bracelets',
            "department": 'david-yurman',
        },
        'david-yurman-mens-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/mens-jewelry?id=1002105',
            "category": 'david-yurman-mens-jewelry',
            "department": 'david-yurman',
        },
        'david-yurman-mens-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/mens-necklaces?id=1002108',
            "category": 'david-yurman-mens-necklaces',
            "department": 'david-yurman',
        },
        'david-yurman-mens-rings': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/mens-rings?id=1002109',
            "category": 'david-yurman-mens-rings',
            "department": 'david-yurman',
        },
        'david-yurman-women': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/women?id=1002097',
            "category": 'david-yurman-women',
            "department": 'david-yurman',
        },
        'david-yurman-womens-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/womens-bracelets?id=1002099',
            "category": 'david-yurman-womens-bracelets',
            "department": 'david-yurman',
        },
        'david-yurman-womens-earrings': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/womens-earrings?id=1002100',
            "category": 'david-yurman-womens-earrings',
            "department": 'david-yurman',
        },
        'david-yurman-womens-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/womens-necklaces?id=1002101',
            "category": 'david-yurman-womens-necklaces',
            "department": 'david-yurman',
        },
        'david-yurman-womens-rings': {
            "url": 'https://www.bloomingdales.com/shop/david-yurman/womens-rings?id=1002102',
            "category": 'david-yurman-womens-rings',
            "department": 'david-yurman',
        },
    },
    'dead-cross-sells': {
        'dead-cross-sells': {
            "url": 'https://www.bloomingdales.com/shop/dead-cross-sells?id=17536',
            "category": 'dead-cross-sells',
            "department": 'dead-cross-sells',
        },
    },
    'delsey-paris': {
        'delsey-paris': {
            "url": 'https://www.bloomingdales.com/shop/delsey-paris?id=1322602',
            "category": 'delsey-paris',
            "department": 'delsey-paris',
        },
    },
    'demi-fine-jewelry': {
        'demi-fine-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/demi-fine-jewelry?id=1070059',
            "category": 'demi-fine-jewelry',
            "department": 'demi-fine-jewelry',
        },
    },
    'denim-shirts-jackets': {
        'denim-shirts-jackets': {
            "url": 'https://www.bloomingdales.com/shop/denim-shirts-jackets?id=1148659',
            "category": 'denim-shirts-jackets',
            "department": 'denim-shirts-jackets',
        },
    },
    'designer-bedding': {
        'designer-bedding': {
            "url": 'https://www.bloomingdales.com/shop/designer-bedding?id=1153859',
            "category": 'designer-bedding',
            "department": 'designer-bedding',
        },
    },
    'designer-pillows-throw-blankets': {
        'designer-pillows-throw-blankets': {
            "url": 'https://www.bloomingdales.com/shop/designer-pillows-throw-blankets?id=1151579',
            "category": 'designer-pillows-throw-blankets',
            "department": 'designer-pillows-throw-blankets',
        },
        'designer-pillows-throw-blankets-modern-contemporary-decorative-pillows': {
            "url": 'https://www.bloomingdales.com/shop/designer-pillows-throw-blankets/modern-contemporary-decorative-pillows?id=1151580',
            "category": 'designer-pillows-throw-blankets-modern-contemporary-decorative-pillows',
            "department": 'designer-pillows-throw-blankets',
        },
        'designer-pillows-throw-blankets-modern-contemporary-throw-blankets': {
            "url": 'https://www.bloomingdales.com/shop/designer-pillows-throw-blankets/modern-contemporary-throw-blankets?id=1151581',
            "category": 'designer-pillows-throw-blankets-modern-contemporary-throw-blankets',
            "department": 'designer-pillows-throw-blankets',
        },
    },
    'designers': {
        'all-designers': {
            "url": 'https://www.bloomingdales.com/shop/all-designers?id=1001351',
            "category": 'all-designers',
            "department": 'designers',
        },
        'all-designers-beauty-makeup-skincare-brands': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/beauty-makeup-skincare-brands?id=1001341',
            "category": 'all-designers-beauty-makeup-skincare-brands',
            "department": 'designers',
        },
        'all-designers-best-cookware-kitchen-bedding-furniture-brands': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/best-cookware-kitchen-bedding-furniture-brands?id=1247206',
            "category": 'all-designers-best-cookware-kitchen-bedding-furniture-brands',
            "department": 'designers',
        },
        'all-designers-clothing-brands-for-babies-kids': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/clothing-brands-for-babies-kids?id=1001343',
            "category": 'all-designers-clothing-brands-for-babies-kids',
            "department": 'designers',
        },
        'all-designers-clothing-brands-for-men': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/clothing-brands-for-men?id=1001338',
            "category": 'all-designers-clothing-brands-for-men',
            "department": 'designers',
        },
        'all-designers-clothing-brands-for-women': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/clothing-brands-for-women?id=1001337',
            "category": 'all-designers-clothing-brands-for-women',
            "department": 'designers',
        },
        'all-designers-handbags-purse-brands': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/handbags-purse-brands?id=1001340',
            "category": 'all-designers-handbags-purse-brands',
            "department": 'designers',
        },
        'all-designers-jewelry-brands': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/jewelry-brands?id=1001342',
            "category": 'all-designers-jewelry-brands',
            "department": 'designers',
        },
        'all-designers-shoe-brands-for-women': {
            "url": 'https://www.bloomingdales.com/shop/all-designers/shoe-brands-for-women?id=1001339',
            "category": 'all-designers-shoe-brands-for-women',
            "department": 'designers',
        },
    },
    'develop': {
        'develop': {
            "url": 'https://www.bloomingdales.com/shop/develop?id=1017461',
            "category": 'develop',
            "department": 'develop',
        },
    },
    'dinnerware': {
        'dinnerware': {
            "url": 'https://www.bloomingdales.com/shop/dinnerware?id=1003024',
            "category": 'dinnerware',
            "department": 'dinnerware',
        },
    },
    'dior': {
        'dior': {
            "url": 'https://www.bloomingdales.com/shop/dior?id=1003843',
            "category": 'dior',
            "department": 'dior',
        },
        'dior-dior-cologne': {
            "url": 'https://www.bloomingdales.com/shop/dior/dior-cologne?id=1320498',
            "category": 'dior-dior-cologne',
            "department": 'dior',
        },
        'dior-dior-homme': {
            "url": 'https://www.bloomingdales.com/shop/dior/dior-homme?id=1320517',
            "category": 'dior-dior-homme',
            "department": 'dior',
        },
        'dior-dior-jadore': {
            "url": 'https://www.bloomingdales.com/shop/dior/dior-jadore?id=1269704',
            "category": 'dior-dior-jadore',
            "department": 'dior',
        },
        'dior-dior-perfume': {
            "url": 'https://www.bloomingdales.com/shop/dior/dior-perfume?id=1320497',
            "category": 'dior-dior-perfume',
            "department": 'dior',
        },
        'dior-dior-sauvage': {
            "url": 'https://www.bloomingdales.com/shop/dior/dior-sauvage?id=1320496',
            "category": 'dior-dior-sauvage',
            "department": 'dior',
        },
        'dior-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/dior/fragrances?id=1190065',
            "category": 'dior-fragrances',
            "department": 'dior',
        },
        'dior-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/dior/gift-sets?id=1190071',
            "category": 'dior-gift-sets',
            "department": 'dior',
        },
        'dior-makeup': {
            "url": 'https://www.bloomingdales.com/shop/dior/makeup?id=1190066',
            "category": 'dior-makeup',
            "department": 'dior',
        },
        'dior-skincare': {
            "url": 'https://www.bloomingdales.com/shop/dior/skincare?id=1190067',
            "category": 'dior-skincare',
            "department": 'dior',
        },
        'dior-womens-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/dior/womens-sunglasses?id=1190069',
            "category": 'dior-womens-sunglasses',
            "department": 'dior',
        },
    },
    'diptyque': {
        'diptyque': {
            "url": 'https://www.bloomingdales.com/shop/diptyque?id=1190967',
            "category": 'diptyque',
            "department": 'diptyque',
        },
    },
    'discover-try-ply-stainless': {
        'discover-try-ply-stainless': {
            "url": 'https://www.bloomingdales.com/shop/discover-try-ply-stainless?id=1017460',
            "category": 'discover-try-ply-stainless',
            "department": 'discover-try-ply-stainless',
        },
    },
    'dl1961': {
        'dl1961': {
            "url": 'https://www.bloomingdales.com/shop/dl1961?id=1304720',
            "category": 'dl1961',
            "department": 'dl1961',
        },
        'dl1961-kids': {
            "url": 'https://www.bloomingdales.com/shop/dl1961/kids?id=1304723',
            "category": 'dl1961-kids',
            "department": 'dl1961',
        },
        'dl1961-mens': {
            "url": 'https://www.bloomingdales.com/shop/dl1961/mens?id=1304722',
            "category": 'dl1961-mens',
            "department": 'dl1961',
        },
        'dl1961-womens': {
            "url": 'https://www.bloomingdales.com/shop/dl1961/womens?id=1304721',
            "category": 'dl1961-womens',
            "department": 'dl1961',
        },
    },
    'dolce-gabbana': {
        'dolce-gabbana': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana?id=1316911',
            "category": 'dolce-gabbana',
            "department": 'dolce-gabbana',
        },
        'dolce-gabbana-handbags': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana/handbags?id=1316916',
            "category": 'dolce-gabbana-handbags',
            "department": 'dolce-gabbana',
        },
        'dolce-gabbana-kids': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana/kids?id=1327595',
            "category": 'dolce-gabbana-kids',
            "department": 'dolce-gabbana',
        },
        'dolce-gabbana-mens': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana/mens?id=1316914',
            "category": 'dolce-gabbana-mens',
            "department": 'dolce-gabbana',
        },
        'dolce-gabbana-shoes': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana/shoes?id=1316915',
            "category": 'dolce-gabbana-shoes',
            "department": 'dolce-gabbana',
        },
        'dolce-gabbana-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana/sunglasses?id=1316917',
            "category": 'dolce-gabbana-sunglasses',
            "department": 'dolce-gabbana',
        },
        'dolce-gabbana-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana/womens-clothing?id=1316913',
            "category": 'dolce-gabbana-womens-clothing',
            "department": 'dolce-gabbana',
        },
    },
    'dolce-gabbana-beauty': {
        'dolce-gabbana-beauty': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty?id=1332403',
            "category": 'dolce-gabbana-beauty',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-dolce-gabbana-eyes': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/dolce-gabbana-eyes?id=1332406',
            "category": 'dolce-gabbana-beauty-dolce-gabbana-eyes',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-dolce-gabbana-face': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/dolce-gabbana-face?id=1332408',
            "category": 'dolce-gabbana-beauty-dolce-gabbana-face',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-dolce-gabbana-light-blue': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/dolce-gabbana-light-blue?id=1335995',
            "category": 'dolce-gabbana-beauty-dolce-gabbana-light-blue',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-dolce-gabbana-lips': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/dolce-gabbana-lips?id=1332407',
            "category": 'dolce-gabbana-beauty-dolce-gabbana-lips',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-dolce-gabbana-skincare': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/dolce-gabbana-skincare?id=1332405',
            "category": 'dolce-gabbana-beauty-dolce-gabbana-skincare',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-dolce-gabbana-the-one': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/dolce-gabbana-the-one?id=1335996',
            "category": 'dolce-gabbana-beauty-dolce-gabbana-the-one',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-dolce-gabbana-velvet': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/dolce-gabbana-velvet?id=1332404',
            "category": 'dolce-gabbana-beauty-dolce-gabbana-velvet',
            "department": 'dolce-gabbana-beauty',
        },
        'dolce-gabbana-beauty-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/dolce-gabbana-beauty/fragrance?id=1316912',
            "category": 'dolce-gabbana-beauty-fragrance',
            "department": 'dolce-gabbana-beauty',
        },
    },
    'dolce-vita': {
        'dolce-vita': {
            "url": 'https://www.bloomingdales.com/shop/dolce-vita?id=1003993',
            "category": 'dolce-vita',
            "department": 'dolce-vita',
        },
    },
    'doona': {
        'doona': {
            "url": 'https://www.bloomingdales.com/shop/doona?id=1276596',
            "category": 'doona',
            "department": 'doona',
        },
    },
    'drbarbara-sturm': {
        'drbarbara-sturm': {
            "url": 'https://www.bloomingdales.com/shop/drbarbara-sturm?id=1283832',
            "category": 'drbarbara-sturm',
            "department": 'drbarbara-sturm',
        },
        'drbarbara-sturm-body-haircare': {
            "url": 'https://www.bloomingdales.com/shop/drbarbara-sturm/body-haircare?id=1283834',
            "category": 'drbarbara-sturm-body-haircare',
            "department": 'drbarbara-sturm',
        },
        'drbarbara-sturm-moisturizers': {
            "url": 'https://www.bloomingdales.com/shop/drbarbara-sturm/moisturizers?id=1283835',
            "category": 'drbarbara-sturm-moisturizers',
            "department": 'drbarbara-sturm',
        },
        'drbarbara-sturm-serums': {
            "url": 'https://www.bloomingdales.com/shop/drbarbara-sturm/serums?id=1283836',
            "category": 'drbarbara-sturm-serums',
            "department": 'drbarbara-sturm',
        },
        'drbarbara-sturm-sets': {
            "url": 'https://www.bloomingdales.com/shop/drbarbara-sturm/sets?id=1283837',
            "category": 'drbarbara-sturm-sets',
            "department": 'drbarbara-sturm',
        },
        'drbarbara-sturm-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/drbarbara-sturm/shop-all?id=1283831',
            "category": 'drbarbara-sturm-shop-all',
            "department": 'drbarbara-sturm',
        },
        'drbarbara-sturm-skincare': {
            "url": 'https://www.bloomingdales.com/shop/drbarbara-sturm/skincare?id=1283833',
            "category": 'drbarbara-sturm-skincare',
            "department": 'drbarbara-sturm',
        },
    },
    'dress-pants': {
        'dress-pants': {
            "url": 'https://www.bloomingdales.com/shop/dress-pants?id=1027028',
            "category": 'dress-pants',
            "department": 'dress-pants',
        },
    },
    'dresses': {
        'dresses': {
            "url": 'https://www.bloomingdales.com/shop/dresses?id=1278799',
            "category": 'dresses',
            "department": 'dresses',
        },
    },
    'dries-van-noten': {
        'dries-van-noten': {
            "url": 'https://www.bloomingdales.com/shop/dries-van-noten?id=1328095',
            "category": 'dries-van-noten',
            "department": 'dries-van-noten',
        },
        'dries-van-noten-beauty': {
            "url": 'https://www.bloomingdales.com/shop/dries-van-noten/beauty?id=1328096',
            "category": 'dries-van-noten-beauty',
            "department": 'dries-van-noten',
        },
        'dries-van-noten-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/dries-van-noten/mens-shoes?id=1328099',
            "category": 'dries-van-noten-mens-shoes',
            "department": 'dries-van-noten',
        },
        'dries-van-noten-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/dries-van-noten/womens-shoes?id=1328100',
            "category": 'dries-van-noten-womens-shoes',
            "department": 'dries-van-noten',
        },
    },
    'drop': {
        'drop': {
            "url": 'https://www.bloomingdales.com/shop/drop?id=20549',
            "category": 'drop',
            "department": 'drop',
        },
    },
    'ds-durga': {
        'ds-durga': {
            "url": 'https://www.bloomingdales.com/shop/ds-durga?id=1312805',
            "category": 'ds-durga',
            "department": 'ds-durga',
        },
    },
    'dutch-ovens': {
        'dutch-ovens': {
            "url": 'https://www.bloomingdales.com/shop/dutch-ovens?id=1039378',
            "category": 'dutch-ovens',
            "department": 'dutch-ovens',
        },
    },
    'dyson': {
        'dyson': {
            "url": 'https://www.bloomingdales.com/shop/dyson?id=1210559',
            "category": 'dyson',
            "department": 'dyson',
        },
        'dyson-air-purifiers': {
            "url": 'https://www.bloomingdales.com/shop/dyson/air-purifiers?id=1210564',
            "category": 'dyson-air-purifiers',
            "department": 'dyson',
        },
        'dyson-dyson-airwrap': {
            "url": 'https://www.bloomingdales.com/shop/dyson/dyson-airwrap?id=1281896',
            "category": 'dyson-dyson-airwrap',
            "department": 'dyson',
        },
        'dyson-dyson-hair-care': {
            "url": 'https://www.bloomingdales.com/shop/dyson/dyson-hair-care?id=1309145',
            "category": 'dyson-dyson-hair-care',
            "department": 'dyson',
        },
        'dyson-dyson-hair-dryers': {
            "url": 'https://www.bloomingdales.com/shop/dyson/dyson-hair-dryers?id=1309001',
            "category": 'dyson-dyson-hair-dryers',
            "department": 'dyson',
        },
        'dyson-dyson-hair-straighteners': {
            "url": 'https://www.bloomingdales.com/shop/dyson/dyson-hair-straighteners?id=1308804',
            "category": 'dyson-dyson-hair-straighteners',
            "department": 'dyson',
        },
        'dyson-floor-care': {
            "url": 'https://www.bloomingdales.com/shop/dyson/floor-care?id=1244712',
            "category": 'dyson-floor-care',
            "department": 'dyson',
        },
        'dyson-hair': {
            "url": 'https://www.bloomingdales.com/shop/dyson/hair?id=1244711',
            "category": 'dyson-hair',
            "department": 'dyson',
        },
        'dyson-lighting': {
            "url": 'https://www.bloomingdales.com/shop/dyson/lighting?id=1210565',
            "category": 'dyson-lighting',
            "department": 'dyson',
        },
        'dyson-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/dyson/shop-all?id=1286517',
            "category": 'dyson-shop-all',
            "department": 'dyson',
        },
    },
    'editors-picks-fall-2015': {
        'editors-picks-fall-2015': {
            "url": 'https://www.bloomingdales.com/shop/editors-picks-fall-2015?id=1005130',
            "category": 'editors-picks-fall-2015',
            "department": 'editors-picks-fall-2015',
        },
    },
    'eileen-fisher': {
        'eileen-fisher': {
            "url": 'https://www.bloomingdales.com/shop/eileen-fisher?id=1004040',
            "category": 'eileen-fisher',
            "department": 'eileen-fisher',
        },
        'eileen-fisher-petites': {
            "url": 'https://www.bloomingdales.com/shop/eileen-fisher/petites?id=1004144',
            "category": 'eileen-fisher-petites',
            "department": 'eileen-fisher',
        },
        'eileen-fisher-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/eileen-fisher/womens-clothing?id=1004046',
            "category": 'eileen-fisher-womens-clothing',
            "department": 'eileen-fisher',
        },
    },
    'email-special-offer': {
        'email-special-offer': {
            "url": 'https://www.bloomingdales.com/shop/email-special-offer?id=1307616',
            "category": 'email-special-offer',
            "department": 'email-special-offer',
        },
    },
    'emporio-armani': {
        'emporio-armani': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani?id=1275295',
            "category": 'emporio-armani',
            "department": 'emporio-armani',
        },
        'emporio-armani-acqua-di-gio': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/acqua-di-gio?id=1307028',
            "category": 'emporio-armani-acqua-di-gio',
            "department": 'emporio-armani',
        },
        'emporio-armani-armani-beauty': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/armani-beauty?id=1290207',
            "category": 'emporio-armani-armani-beauty',
            "department": 'emporio-armani',
        },
        'emporio-armani-armani-prive': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/armani-prive?id=1307031',
            "category": 'emporio-armani-armani-prive',
            "department": 'emporio-armani',
        },
        'emporio-armani-eyes': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/eyes?id=1306897',
            "category": 'emporio-armani-eyes',
            "department": 'emporio-armani',
        },
        'emporio-armani-face': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/face?id=1306896',
            "category": 'emporio-armani-face',
            "department": 'emporio-armani',
        },
        'emporio-armani-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/fragrance?id=1306900',
            "category": 'emporio-armani-fragrance',
            "department": 'emporio-armani',
        },
        'emporio-armani-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/gift-sets?id=1306899',
            "category": 'emporio-armani-gift-sets',
            "department": 'emporio-armani',
        },
        'emporio-armani-handbags': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/handbags?id=1285195',
            "category": 'emporio-armani-handbags',
            "department": 'emporio-armani',
        },
        'emporio-armani-lips': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/lips?id=1306898',
            "category": 'emporio-armani-lips',
            "department": 'emporio-armani',
        },
        'emporio-armani-luminous-silk': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/luminous-silk?id=1307895',
            "category": 'emporio-armani-luminous-silk',
            "department": 'emporio-armani',
        },
        'emporio-armani-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/mens-clothing?id=1275296',
            "category": 'emporio-armani-mens-clothing',
            "department": 'emporio-armani',
        },
        'emporio-armani-my-way': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/my-way?id=1307030',
            "category": 'emporio-armani-my-way',
            "department": 'emporio-armani',
        },
        'emporio-armani-stronger-with-you': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/stronger-with-you?id=1307029',
            "category": 'emporio-armani-stronger-with-you',
            "department": 'emporio-armani',
        },
        'emporio-armani-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/emporio-armani/womens-clothing?id=1275297',
            "category": 'emporio-armani-womens-clothing',
            "department": 'emporio-armani',
        },
    },
    'empty-category-recs-bed-bath': {
        'empty-category-recs-bed-bath': {
            "url": 'https://www.bloomingdales.com/shop/empty-category-recs-bed-bath?id=1045862',
            "category": 'empty-category-recs-bed-bath',
            "department": 'empty-category-recs-bed-bath',
        },
    },
    'estee-lauder': {
        'estee-lauder': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder?id=6841',
            "category": 'estee-lauder',
            "department": 'estee-lauder',
        },
        'estee-lauder-advanced-night-repair': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/advanced-night-repair?id=1307431',
            "category": 'estee-lauder-advanced-night-repair',
            "department": 'estee-lauder',
        },
        'estee-lauder-aerin': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/aerin?id=1001689',
            "category": 'estee-lauder-aerin',
            "department": 'estee-lauder',
        },
        'estee-lauder-double-wear': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/double-wear?id=1307430',
            "category": 'estee-lauder-double-wear',
            "department": 'estee-lauder',
        },
        'estee-lauder-estee-lauder-fragrances-perfume': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/estee-lauder-fragrances-perfume?id=7675',
            "category": 'estee-lauder-estee-lauder-fragrances-perfume',
            "department": 'estee-lauder',
        },
        'estee-lauder-estee-lauder-makeup-cosmetics': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/estee-lauder-makeup-cosmetics?id=7639',
            "category": 'estee-lauder-estee-lauder-makeup-cosmetics',
            "department": 'estee-lauder',
        },
        'estee-lauder-estee-lauder-skin-care-products': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/estee-lauder-skin-care-products?id=7657',
            "category": 'estee-lauder-estee-lauder-skin-care-products',
            "department": 'estee-lauder',
        },
        'estee-lauder-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/gift-sets?id=1308620',
            "category": 'estee-lauder-gift-sets',
            "department": 'estee-lauder',
        },
        'estee-lauder-re-nutriv': {
            "url": 'https://www.bloomingdales.com/shop/estee-lauder/re-nutriv?id=7670',
            "category": 'estee-lauder-re-nutriv',
            "department": 'estee-lauder',
        },
    },
    'ex-nihilo': {
        'ex-nihilo': {
            "url": 'https://www.bloomingdales.com/shop/ex-nihilo?id=1274495',
            "category": 'ex-nihilo',
            "department": 'ex-nihilo',
        },
        'ex-nihilo-ex-nihilo-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/ex-nihilo/ex-nihilo-bath-body?id=1281728',
            "category": 'ex-nihilo-ex-nihilo-bath-body',
            "department": 'ex-nihilo',
        },
        'ex-nihilo-ex-nihilo-blue-talisman': {
            "url": 'https://www.bloomingdales.com/shop/ex-nihilo/ex-nihilo-blue-talisman?id=1291322',
            "category": 'ex-nihilo-ex-nihilo-blue-talisman',
            "department": 'ex-nihilo',
        },
        'ex-nihilo-ex-nihilo-fleur-narcotique': {
            "url": 'https://www.bloomingdales.com/shop/ex-nihilo/ex-nihilo-fleur-narcotique?id=1280195',
            "category": 'ex-nihilo-ex-nihilo-fleur-narcotique',
            "department": 'ex-nihilo',
        },
        'ex-nihilo-ex-nihilo-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/ex-nihilo/ex-nihilo-fragrances?id=1281729',
            "category": 'ex-nihilo-ex-nihilo-fragrances',
            "department": 'ex-nihilo',
        },
    },
    'exclusive-designer-offer': {
        'exclusive-designer-offer': {
            "url": 'https://www.bloomingdales.com/shop/exclusive-designer-offer?id=1268322',
            "category": 'exclusive-designer-offer',
            "department": 'exclusive-designer-offer',
        },
    },
    'exclusive-offer-25-off-with-code': {
        'exclusive-offer-25-off-with-code': {
            "url": 'https://www.bloomingdales.com/shop/exclusive-offer-25-off-with-code?id=1268026',
            "category": 'exclusive-offer-25-off-with-code',
            "department": 'exclusive-offer-25-off-with-code',
        },
    },
    'fall-and-halloween': {
        'fall-and-halloween': {
            "url": 'https://www.bloomingdales.com/shop/fall-and-halloween?id=1206965',
            "category": 'fall-and-halloween',
            "department": 'fall-and-halloween',
        },
    },
    'fall-beauty-trends': {
        'fall-beauty-trends': {
            "url": 'https://www.bloomingdales.com/shop/fall-beauty-trends?id=1267047',
            "category": 'fall-beauty-trends',
            "department": 'fall-beauty-trends',
        },
    },
    'fall-style-guide-its-on': {
        'fall-style-guide-its-on': {
            "url": 'https://www.bloomingdales.com/shop/fall-style-guide-its-on?id=1000387',
            "category": 'fall-style-guide-its-on',
            "department": 'fall-style-guide-its-on',
        },
        'fall-style-guide-its-on-accessories-trends': {
            "url": 'https://www.bloomingdales.com/shop/fall-style-guide-its-on/accessories-trends?id=1000388',
            "category": 'fall-style-guide-its-on-accessories-trends',
            "department": 'fall-style-guide-its-on',
        },
        'fall-style-guide-its-on-jewel-tones': {
            "url": 'https://www.bloomingdales.com/shop/fall-style-guide-its-on/jewel-tones?id=1000403',
            "category": 'fall-style-guide-its-on-jewel-tones',
            "department": 'fall-style-guide-its-on',
        },
        'fall-style-guide-its-on-riding-boots': {
            "url": 'https://www.bloomingdales.com/shop/fall-style-guide-its-on/riding-boots?id=1000526',
            "category": 'fall-style-guide-its-on-riding-boots',
            "department": 'fall-style-guide-its-on',
        },
    },
    'farm-rio': {
        'farm-rio': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio?id=1234659',
            "category": 'farm-rio',
            "department": 'farm-rio',
        },
        'farm-rio-dresses': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/dresses?id=1248705',
            "category": 'farm-rio-dresses',
            "department": 'farm-rio',
        },
        'farm-rio-handbags': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/handbags?id=1308995',
            "category": 'farm-rio-handbags',
            "department": 'farm-rio',
        },
        'farm-rio-rompers': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/rompers?id=1248711',
            "category": 'farm-rio-rompers',
            "department": 'farm-rio',
        },
        'farm-rio-sale': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/sale?id=1248710',
            "category": 'farm-rio-sale',
            "department": 'farm-rio',
        },
        'farm-rio-shoes': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/shoes?id=1308895',
            "category": 'farm-rio-shoes',
            "department": 'farm-rio',
        },
        'farm-rio-shorts': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/shorts?id=1248712',
            "category": 'farm-rio-shorts',
            "department": 'farm-rio',
        },
        'farm-rio-skirts': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/skirts?id=1248709',
            "category": 'farm-rio-skirts',
            "department": 'farm-rio',
        },
        'farm-rio-tops': {
            "url": 'https://www.bloomingdales.com/shop/farm-rio/tops?id=1248704',
            "category": 'farm-rio-tops',
            "department": 'farm-rio',
        },
    },
    'favorite-gifts': {
        'favorite-gifts': {
            "url": 'https://www.bloomingdales.com/shop/favorite-gifts?id=1000644',
            "category": 'favorite-gifts',
            "department": 'favorite-gifts',
        },
    },
    'feel-good-fall': {
        'feel-good-fall': {
            "url": 'https://www.bloomingdales.com/shop/feel-good-fall?id=1103260',
            "category": 'feel-good-fall',
            "department": 'feel-good-fall',
        },
    },
    'fendi': {
        'fendi': {
            "url": 'https://www.bloomingdales.com/shop/fendi?id=1294995',
            "category": 'fendi',
            "department": 'fendi',
        },
        'fendi-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fendi/shoes?id=1294996',
            "category": 'fendi-shoes',
            "department": 'fendi',
        },
        'fendi-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/fendi/sunglasses?id=1294997',
            "category": 'fendi-sunglasses',
            "department": 'fendi',
        },
    },
    'fifa-1904': {
        'fifa-1904': {
            "url": 'https://www.bloomingdales.com/shop/fifa-1904?id=1322604',
            "category": 'fifa-1904',
            "department": 'fifa-1904',
        },
    },
    'fine-jewelry': {
        'fine-jewelry-all-designers': {
            "url": 'https://www.bloomingdales.com/shop/fine-jewelry/all-designers?id=23694',
            "category": 'fine-jewelry-all-designers',
            "department": 'fine-jewelry',
        },
    },
    'fit-tips': {
        'fit-tips': {
            "url": 'https://www.bloomingdales.com/shop/fit-tips?id=1002643',
            "category": 'fit-tips',
            "department": 'fit-tips',
        },
    },
    'flatware': {
        'flatware': {
            "url": 'https://www.bloomingdales.com/shop/flatware?id=1003025',
            "category": 'flatware',
            "department": 'flatware',
        },
    },
    'for-her': {
        'for-her': {
            "url": 'https://www.bloomingdales.com/shop/for-her?id=22109',
            "category": 'for-her',
            "department": 'for-her',
        },
    },
    'for-him': {
        'for-him': {
            "url": 'https://www.bloomingdales.com/shop/for-him?id=22110',
            "category": 'for-him',
            "department": 'for-him',
        },
    },
    'for-the-boho-mom': {
        'for-the-boho-mom': {
            "url": 'https://www.bloomingdales.com/shop/for-the-boho-mom?id=1006720',
            "category": 'for-the-boho-mom',
            "department": 'for-the-boho-mom',
        },
    },
    'for-the-coffee-lover': {
        'for-the-coffee-lover': {
            "url": 'https://www.bloomingdales.com/shop/for-the-coffee-lover?id=1021575',
            "category": 'for-the-coffee-lover',
            "department": 'for-the-coffee-lover',
        },
    },
    'for-the-elegant-mom': {
        'for-the-elegant-mom': {
            "url": 'https://www.bloomingdales.com/shop/for-the-elegant-mom?id=1006721',
            "category": 'for-the-elegant-mom',
            "department": 'for-the-elegant-mom',
        },
    },
    'formal-wedding-attire': {
        'formal-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/formal-wedding-attire?id=1179193',
            "category": 'formal-wedding-attire',
            "department": 'formal-wedding-attire',
        },
    },
    'formalwear': {
        'formalwear': {
            "url": 'https://www.bloomingdales.com/shop/formalwear?id=1207560',
            "category": 'formalwear',
            "department": 'formalwear',
        },
    },
    'fragrance': {
        'fragrance': {
            "url": 'https://www.bloomingdales.com/shop/fragrance?id=1269429',
            "category": 'fragrance',
            "department": 'fragrance',
        },
    },
    'frame-clothing': {
        'frame-clothing': {
            "url": 'https://www.bloomingdales.com/shop/frame-clothing?id=1250012',
            "category": 'frame-clothing',
            "department": 'frame-clothing',
        },
        'frame-clothing-frame-mens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/frame-clothing/frame-mens-jeans?id=1250399',
            "category": 'frame-clothing-frame-mens-jeans',
            "department": 'frame-clothing',
        },
        'frame-clothing-frame-sale': {
            "url": 'https://www.bloomingdales.com/shop/frame-clothing/frame-sale?id=1250397',
            "category": 'frame-clothing-frame-sale',
            "department": 'frame-clothing',
        },
        'frame-clothing-frame-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/frame-clothing/frame-womens-clothing?id=1250395',
            "category": 'frame-clothing-frame-womens-clothing',
            "department": 'frame-clothing',
        },
        'frame-clothing-frame-womens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/frame-clothing/frame-womens-jeans?id=1250398',
            "category": 'frame-clothing-frame-womens-jeans',
            "department": 'frame-clothing',
        },
        'frame-clothing-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/frame-clothing/mens-clothing?id=1250396',
            "category": 'frame-clothing-mens-clothing',
            "department": 'frame-clothing',
        },
        'frame-clothing-the-frame-tennis-collection': {
            "url": 'https://www.bloomingdales.com/shop/frame-clothing/the-frame-tennis-collection?id=1327195',
            "category": 'frame-clothing-the-frame-tennis-collection',
            "department": 'frame-clothing',
        },
    },
    'french-garden-collection': {
        'french-garden-collection': {
            "url": 'https://www.bloomingdales.com/shop/french-garden-collection?id=1310599',
            "category": 'french-garden-collection',
            "department": 'french-garden-collection',
        },
    },
    'frette': {
        'frette': {
            "url": 'https://www.bloomingdales.com/shop/frette?id=1286103',
            "category": 'frette',
            "department": 'frette',
        },
    },
    'from-italy-with-love': {
        'from-italy-with-love': {
            "url": 'https://www.bloomingdales.com/shop/from-italy-with-love?id=1239059',
            "category": 'from-italy-with-love',
            "department": 'from-italy-with-love',
        },
    },
    'furniture': {
        'furniture-sale': {
            "url": 'https://www.bloomingdales.com/shop/furniture/sale?id=16711',
            "category": 'furniture-sale',
            "department": 'furniture',
        },
    },
    'futuristic-minimalism': {
        'futuristic-minimalism': {
            "url": 'https://www.bloomingdales.com/shop/futuristic-minimalism?id=1240294',
            "category": 'futuristic-minimalism',
            "department": 'futuristic-minimalism',
        },
    },
    'ganni': {
        'ganni': {
            "url": 'https://www.bloomingdales.com/shop/ganni?id=1321795',
            "category": 'ganni',
            "department": 'ganni',
        },
        'ganni-clothing': {
            "url": 'https://www.bloomingdales.com/shop/ganni/clothing?id=1321796',
            "category": 'ganni-clothing',
            "department": 'ganni',
        },
        'ganni-handbags': {
            "url": 'https://www.bloomingdales.com/shop/ganni/handbags?id=1321797',
            "category": 'ganni-handbags',
            "department": 'ganni',
        },
        'ganni-shoes': {
            "url": 'https://www.bloomingdales.com/shop/ganni/shoes?id=1321798',
            "category": 'ganni-shoes',
            "department": 'ganni',
        },
    },
    'garden-inspired': {
        'garden-inspired': {
            "url": 'https://www.bloomingdales.com/shop/garden-inspired?id=1273095',
            "category": 'garden-inspired',
            "department": 'garden-inspired',
        },
    },
    'georg-jensen': {
        'georg-jensen': {
            "url": 'https://www.bloomingdales.com/shop/georg-jensen?id=1231868',
            "category": 'georg-jensen',
            "department": 'georg-jensen',
        },
        'georg-jensen-home': {
            "url": 'https://www.bloomingdales.com/shop/georg-jensen/home?id=1231869',
            "category": 'georg-jensen-home',
            "department": 'georg-jensen',
        },
    },
    'gianvito-rossi': {
        'gianvito-rossi': {
            "url": 'https://www.bloomingdales.com/shop/gianvito-rossi?id=1332799',
            "category": 'gianvito-rossi',
            "department": 'gianvito-rossi',
        },
    },
    'gift-sets': {
        'gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/gift-sets?id=1269419',
            "category": 'gift-sets',
            "department": 'gift-sets',
        },
    },
    'gifts': {
        'gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts?id=1236267',
            "category": 'gifts',
            "department": 'gifts',
        },
        'gifts-all-fathers-day-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/all-fathers-day-gifts?id=1006752',
            "category": 'gifts-all-fathers-day-gifts',
            "department": 'gifts',
        },
        'gifts-all-mothers-day-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/all-mothers-day-gifts?id=1267909',
            "category": 'gifts-all-mothers-day-gifts',
            "department": 'gifts',
        },
        'gifts-beautifully-boxed-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/beautifully-boxed-gifts?id=1245695',
            "category": 'gifts-beautifully-boxed-gifts',
            "department": 'gifts',
        },
        'gifts-best-fathers-day-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-fathers-day-gifts?id=1004777',
            "category": 'gifts-best-fathers-day-gifts',
            "department": 'gifts',
        },
        'gifts-best-gifts-under-50': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-gifts-under-50?id=1003526',
            "category": 'gifts-best-gifts-under-50',
            "department": 'gifts',
        },
        'gifts-best-graduation-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-graduation-gifts?id=1028267',
            "category": 'gifts-best-graduation-gifts',
            "department": 'gifts',
        },
        'gifts-best-holiday-gifts-under-100': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-holiday-gifts-under-100?id=1005374',
            "category": 'gifts-best-holiday-gifts-under-100',
            "department": 'gifts',
        },
        'gifts-best-holiday-gifts-under-50': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-holiday-gifts-under-50?id=1005787',
            "category": 'gifts-best-holiday-gifts-under-50',
            "department": 'gifts',
        },
        'gifts-best-luxury-anniversary-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-anniversary-gifts?id=1235776',
            "category": 'gifts-best-luxury-anniversary-gifts',
            "department": 'gifts',
        },
        'gifts-best-luxury-baby-shower-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-baby-shower-gifts?id=19459',
            "category": 'gifts-best-luxury-baby-shower-gifts',
            "department": 'gifts',
        },
        'gifts-best-luxury-birthday-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-birthday-gifts?id=1235777',
            "category": 'gifts-best-luxury-birthday-gifts',
            "department": 'gifts',
        },
        'gifts-best-luxury-gifts-for-her': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-gifts-for-her?id=1114062',
            "category": 'gifts-best-luxury-gifts-for-her',
            "department": 'gifts',
        },
        'gifts-best-luxury-gifts-for-him': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-gifts-for-him?id=1028260',
            "category": 'gifts-best-luxury-gifts-for-him',
            "department": 'gifts',
        },
        'gifts-best-luxury-gifts-for-kids': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-gifts-for-kids?id=1028261',
            "category": 'gifts-best-luxury-gifts-for-kids',
            "department": 'gifts',
        },
        'gifts-best-luxury-gifts-for-teens': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-gifts-for-teens?id=1235764',
            "category": 'gifts-best-luxury-gifts-for-teens',
            "department": 'gifts',
        },
        'gifts-best-luxury-gifts-for-the-home': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-gifts-for-the-home?id=1235765',
            "category": 'gifts-best-luxury-gifts-for-the-home',
            "department": 'gifts',
        },
        'gifts-best-luxury-housewarming-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-luxury-housewarming-gifts?id=1028266',
            "category": 'gifts-best-luxury-housewarming-gifts',
            "department": 'gifts',
        },
        'gifts-best-mothers-day-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-mothers-day-gifts?id=1006708',
            "category": 'gifts-best-mothers-day-gifts',
            "department": 'gifts',
        },
        'gifts-best-tech-gadget-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/best-tech-gadget-gifts?id=1028270',
            "category": 'gifts-best-tech-gadget-gifts',
            "department": 'gifts',
        },
        'gifts-check-gift-card-balance': {
            "url": 'https://www.bloomingdales.com/shop/gifts/check-gift-card-balance?id=1036859',
            "category": 'gifts-check-gift-card-balance',
            "department": 'gifts',
        },
        'gifts-designer-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/designer-gifts?id=1292523',
            "category": 'gifts-designer-gifts',
            "department": 'gifts',
        },
        'gifts-e-gift-cards': {
            "url": 'https://www.bloomingdales.com/shop/gifts/e-gift-cards?id=3955',
            "category": 'gifts-e-gift-cards',
            "department": 'gifts',
        },
        'gifts-exclusive-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/exclusive-gifts?id=19507',
            "category": 'gifts-exclusive-gifts',
            "department": 'gifts',
        },
        'gifts-family-matching': {
            "url": 'https://www.bloomingdales.com/shop/gifts/family-matching?id=1075559',
            "category": 'gifts-family-matching',
            "department": 'gifts',
        },
        'gifts-family-matching-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/gifts/family-matching-pajamas?id=1215678',
            "category": 'gifts-family-matching-pajamas',
            "department": 'gifts',
        },
        'gifts-fathers-day-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/fathers-day-gifts?id=1004802',
            "category": 'gifts-fathers-day-gifts',
            "department": 'gifts',
        },
        'gifts-fathers-day-gifts-under-100': {
            "url": 'https://www.bloomingdales.com/shop/gifts/fathers-day-gifts-under-100?id=1004779',
            "category": 'gifts-fathers-day-gifts-under-100',
            "department": 'gifts',
        },
        'gifts-fathers-day-luxe-gifts-for-him': {
            "url": 'https://www.bloomingdales.com/shop/gifts/fathers-day-luxe-gifts-for-him?id=1004778',
            "category": 'gifts-fathers-day-luxe-gifts-for-him',
            "department": 'gifts',
        },
        'gifts-gift-cards': {
            "url": 'https://www.bloomingdales.com/shop/gifts/gift-cards?id=3949',
            "category": 'gifts-gift-cards',
            "department": 'gifts',
        },
        'gifts-gifts-by-price': {
            "url": 'https://www.bloomingdales.com/shop/gifts/gifts-by-price?id=1005373',
            "category": 'gifts-gifts-by-price',
            "department": 'gifts',
        },
        'gifts-holiday-gifts-for-her': {
            "url": 'https://www.bloomingdales.com/shop/gifts/holiday-gifts-for-her?id=1005786',
            "category": 'gifts-holiday-gifts-for-her',
            "department": 'gifts',
        },
        'gifts-holiday-gifts-for-him': {
            "url": 'https://www.bloomingdales.com/shop/gifts/holiday-gifts-for-him?id=1005895',
            "category": 'gifts-holiday-gifts-for-him',
            "department": 'gifts',
        },
        'gifts-holiday-gifts-for-kids': {
            "url": 'https://www.bloomingdales.com/shop/gifts/holiday-gifts-for-kids?id=1002027',
            "category": 'gifts-holiday-gifts-for-kids',
            "department": 'gifts',
        },
        'gifts-holiday-gifts-for-teens': {
            "url": 'https://www.bloomingdales.com/shop/gifts/holiday-gifts-for-teens?id=1249495',
            "category": 'gifts-holiday-gifts-for-teens',
            "department": 'gifts',
        },
        'gifts-holiday-gifts-for-your-home': {
            "url": 'https://www.bloomingdales.com/shop/gifts/holiday-gifts-for-your-home?id=1002028',
            "category": 'gifts-holiday-gifts-for-your-home',
            "department": 'gifts',
        },
        'gifts-jewelry-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/jewelry-gifts?id=1291695',
            "category": 'gifts-jewelry-gifts',
            "department": 'gifts',
        },
        'gifts-luxe-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/luxe-gifts?id=1235974',
            "category": 'gifts-luxe-gifts',
            "department": 'gifts',
        },
        'gifts-luxury-holiday-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/luxury-holiday-gifts?id=1106860',
            "category": 'gifts-luxury-holiday-gifts',
            "department": 'gifts',
        },
        'gifts-mothers-day-gifts-under-100-dollars': {
            "url": 'https://www.bloomingdales.com/shop/gifts/mothers-day-gifts-under-100-dollars?id=1006710',
            "category": 'gifts-mothers-day-gifts-under-100-dollars',
            "department": 'gifts',
        },
        'gifts-newborn-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/newborn-gifts?id=1290003',
            "category": 'gifts-newborn-gifts',
            "department": 'gifts',
        },
        'gifts-our-best-holiday-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/our-best-holiday-gifts?id=1001083',
            "category": 'gifts-our-best-holiday-gifts',
            "department": 'gifts',
        },
        'gifts-personalized-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/personalized-gifts?id=1028269',
            "category": 'gifts-personalized-gifts',
            "department": 'gifts',
        },
        'gifts-sibling-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/sibling-gifts?id=1289796',
            "category": 'gifts-sibling-gifts',
            "department": 'gifts',
        },
        'gifts-stocking-stuffers': {
            "url": 'https://www.bloomingdales.com/shop/gifts/stocking-stuffers?id=1106759',
            "category": 'gifts-stocking-stuffers',
            "department": 'gifts',
        },
        'gifts-travel-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/travel-gifts?id=1292522',
            "category": 'gifts-travel-gifts',
            "department": 'gifts',
        },
        'gifts-under-100': {
            "url": 'https://www.bloomingdales.com/shop/gifts/under-100?id=1235973',
            "category": 'gifts-under-100',
            "department": 'gifts',
        },
        'gifts-valentines-day-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/valentines-day-gifts?id=1254600',
            "category": 'gifts-valentines-day-gifts',
            "department": 'gifts',
        },
        'gifts-valentines-day-gifts-for-her': {
            "url": 'https://www.bloomingdales.com/shop/gifts/valentines-day-gifts-for-her?id=1254601',
            "category": 'gifts-valentines-day-gifts-for-her',
            "department": 'gifts',
        },
        'gifts-valentines-day-gifts-for-him': {
            "url": 'https://www.bloomingdales.com/shop/gifts/valentines-day-gifts-for-him?id=1254602',
            "category": 'gifts-valentines-day-gifts-for-him',
            "department": 'gifts',
        },
        'gifts-valentines-day-gifts-luxe-gifts': {
            "url": 'https://www.bloomingdales.com/shop/gifts/valentines-day-gifts-luxe-gifts?id=1254604',
            "category": 'gifts-valentines-day-gifts-luxe-gifts',
            "department": 'gifts',
        },
        'gifts-valentines-day-gifts-under-100': {
            "url": 'https://www.bloomingdales.com/shop/gifts/valentines-day-gifts-under-100?id=1254603',
            "category": 'gifts-valentines-day-gifts-under-100',
            "department": 'gifts',
        },
        'gifts-wedding-engagement': {
            "url": 'https://www.bloomingdales.com/shop/gifts/wedding-engagement?id=19485',
            "category": 'gifts-wedding-engagement',
            "department": 'gifts',
        },
    },
    'gifts-for-new-parents': {
        'gifts-for-new-parents': {
            "url": 'https://www.bloomingdales.com/shop/gifts-for-new-parents?id=1224170',
            "category": 'gifts-for-new-parents',
            "department": 'gifts-for-new-parents',
        },
    },
    'ginori-1735': {
        'ginori-1735': {
            "url": 'https://www.bloomingdales.com/shop/ginori-1735?id=1331900',
            "category": 'ginori-1735',
            "department": 'ginori-1735',
        },
    },
    'girls-coats-jackets': {
        'girls-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/girls-coats-jackets?id=1213061',
            "category": 'girls-coats-jackets',
            "department": 'girls-coats-jackets',
        },
    },
    'girls-new-arrivals': {
        'girls-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/girls-new-arrivals?id=1144259',
            "category": 'girls-new-arrivals',
            "department": 'girls-new-arrivals',
        },
    },
    'girls-purses-backpacks-accessories': {
        'girls-purses-backpacks-accessories': {
            "url": 'https://www.bloomingdales.com/shop/girls-purses-backpacks-accessories?id=1006189',
            "category": 'girls-purses-backpacks-accessories',
            "department": 'girls-purses-backpacks-accessories',
        },
    },
    'givenchy': {
        'givenchy': {
            "url": 'https://www.bloomingdales.com/shop/givenchy?id=1331898',
            "category": 'givenchy',
            "department": 'givenchy',
        },
    },
    'glam-gala': {
        'glam-gala': {
            "url": 'https://www.bloomingdales.com/shop/glam-gala?id=1253724',
            "category": 'glam-gala',
            "department": 'glam-gala',
        },
    },
    'glassware': {
        'glassware': {
            "url": 'https://www.bloomingdales.com/shop/glassware?id=1003026',
            "category": 'glassware',
            "department": 'glassware',
        },
    },
    'glowhaus-makeup-skin-care': {
        'glowhaus-makeup-skin-care': {
            "url": 'https://www.bloomingdales.com/shop/glowhaus-makeup-skin-care?id=1267004',
            "category": 'glowhaus-makeup-skin-care',
            "department": 'glowhaus-makeup-skin-care',
        },
    },
    'good-sports': {
        'good-sports': {
            "url": 'https://www.bloomingdales.com/shop/good-sports?id=1095759',
            "category": 'good-sports',
            "department": 'good-sports',
        },
    },
    'gq-x-bloomingdales-fit-tips': {
        'gq-x-bloomingdales-fit-tips': {
            "url": 'https://www.bloomingdales.com/shop/gq-x-bloomingdales-fit-tips?id=1027039',
            "category": 'gq-x-bloomingdales-fit-tips',
            "department": 'gq-x-bloomingdales-fit-tips',
        },
    },
    'griddles-and-grill-pans': {
        'griddles-and-grill-pans': {
            "url": 'https://www.bloomingdales.com/shop/griddles-and-grill-pans?id=1039379',
            "category": 'griddles-and-grill-pans',
            "department": 'griddles-and-grill-pans',
        },
    },
    'gucci': {
        'gucci': {
            "url": 'https://www.bloomingdales.com/shop/gucci?id=1004007',
            "category": 'gucci',
            "department": 'gucci',
        },
        'gucci-gucci-eye-makeup': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-eye-makeup?id=1287312',
            "category": 'gucci-gucci-eye-makeup',
            "department": 'gucci',
        },
        'gucci-gucci-face-makeup': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-face-makeup?id=1287311',
            "category": 'gucci-gucci-face-makeup',
            "department": 'gucci',
        },
        'gucci-gucci-flora': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-flora?id=1287314',
            "category": 'gucci-gucci-flora',
            "department": 'gucci',
        },
        'gucci-gucci-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-fragrance?id=1287306',
            "category": 'gucci-gucci-fragrance',
            "department": 'gucci',
        },
        'gucci-gucci-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-gift-sets?id=1287313',
            "category": 'gucci-gucci-gift-sets',
            "department": 'gucci',
        },
        'gucci-gucci-lip-makeup': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-lip-makeup?id=1287309',
            "category": 'gucci-gucci-lip-makeup',
            "department": 'gucci',
        },
        'gucci-gucci-makeup-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-makeup-fragrance?id=1004010',
            "category": 'gucci-gucci-makeup-fragrance',
            "department": 'gucci',
        },
        'gucci-gucci-perfume': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-perfume?id=1287307',
            "category": 'gucci-gucci-perfume',
            "department": 'gucci',
        },
        'gucci-gucci-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/gucci/gucci-womens-shoes?id=1004008',
            "category": 'gucci-gucci-womens-shoes',
            "department": 'gucci',
        },
        'gucci-men': {
            "url": 'https://www.bloomingdales.com/shop/gucci/men?id=1138359',
            "category": 'gucci-men',
            "department": 'gucci',
        },
        'gucci-watches-sunglasses-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/gucci/watches-sunglasses-jewelry?id=1004716',
            "category": 'gucci-watches-sunglasses-jewelry',
            "department": 'gucci',
        },
        'gucci-women': {
            "url": 'https://www.bloomingdales.com/shop/gucci/women?id=1133259',
            "category": 'gucci-women',
            "department": 'gucci',
        },
    },
    'guerlain': {
        'guerlain': {
            "url": 'https://www.bloomingdales.com/shop/guerlain?id=1310799',
            "category": 'guerlain',
            "department": 'guerlain',
        },
        'guerlain-abeille-royale': {
            "url": 'https://www.bloomingdales.com/shop/guerlain/abeille-royale?id=1310804',
            "category": 'guerlain-abeille-royale',
            "department": 'guerlain',
        },
        'guerlain-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/guerlain/fragrance?id=1310800',
            "category": 'guerlain-fragrance',
            "department": 'guerlain',
        },
        'guerlain-lart-la-matiere': {
            "url": 'https://www.bloomingdales.com/shop/guerlain/lart-la-matiere?id=1313996',
            "category": 'guerlain-lart-la-matiere',
            "department": 'guerlain',
        },
        'guerlain-makeup': {
            "url": 'https://www.bloomingdales.com/shop/guerlain/makeup?id=1313995',
            "category": 'guerlain-makeup',
            "department": 'guerlain',
        },
        'guerlain-skincare': {
            "url": 'https://www.bloomingdales.com/shop/guerlain/skincare?id=1310803',
            "category": 'guerlain-skincare',
            "department": 'guerlain',
        },
    },
    'gym-running-shoes': {
        'gym-running-shoes': {
            "url": 'https://www.bloomingdales.com/shop/gym-running-shoes?id=1027043',
            "category": 'gym-running-shoes',
            "department": 'gym-running-shoes',
        },
    },
    'haircare': {
        'haircare': {
            "url": 'https://www.bloomingdales.com/shop/haircare?id=1269417',
            "category": 'haircare',
            "department": 'haircare',
        },
    },
    'hamilton': {
        'hamilton': {
            "url": 'https://www.bloomingdales.com/shop/hamilton?id=1320903',
            "category": 'hamilton',
            "department": 'hamilton',
        },
    },
    'handbags': {
        'handbags': {
            "url": 'https://www.bloomingdales.com/shop/handbags?id=1319129',
            "category": 'handbags',
            "department": 'handbags',
        },
        'handbags-all-handbags-wallets-small-accessories': {
            "url": 'https://www.bloomingdales.com/shop/handbags/all-handbags-wallets-small-accessories?id=1001396',
            "category": 'handbags-all-handbags-wallets-small-accessories',
            "department": 'handbags',
        },
        'handbags-bag-charms': {
            "url": 'https://www.bloomingdales.com/shop/handbags/bag-charms?id=1251795',
            "category": 'handbags-bag-charms',
            "department": 'handbags',
        },
        'handbags-baguette-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/baguette-bags?id=1148965',
            "category": 'handbags-baguette-bags',
            "department": 'handbags',
        },
        'handbags-beach-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/beach-bags?id=1017359',
            "category": 'handbags-beach-bags',
            "department": 'handbags',
        },
        'handbags-belt-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/belt-bags?id=1023266',
            "category": 'handbags-belt-bags',
            "department": 'handbags',
        },
        'handbags-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/handbags/best-sellers?id=23173',
            "category": 'handbags-best-sellers',
            "department": 'handbags',
        },
        'handbags-bucket-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/bucket-bags?id=1004824',
            "category": 'handbags-bucket-bags',
            "department": 'handbags',
        },
        'handbags-card-cases': {
            "url": 'https://www.bloomingdales.com/shop/handbags/card-cases?id=1292336',
            "category": 'handbags-card-cases',
            "department": 'handbags',
        },
        'handbags-clutches-evening-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/clutches-evening-bags?id=17309',
            "category": 'handbags-clutches-evening-bags',
            "department": 'handbags',
        },
        'handbags-cosmetic-makeup-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/cosmetic-makeup-bags?id=1000415',
            "category": 'handbags-cosmetic-makeup-bags',
            "department": 'handbags',
        },
        'handbags-crossbody-bags-mini-crossbody': {
            "url": 'https://www.bloomingdales.com/shop/handbags/crossbody-bags-mini-crossbody?id=17310',
            "category": 'handbags-crossbody-bags-mini-crossbody',
            "department": 'handbags',
        },
        'handbags-evening-occasion-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/evening-occasion-bags?id=1072459',
            "category": 'handbags-evening-occasion-bags',
            "department": 'handbags',
        },
        'handbags-extra-large-handbags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/extra-large-handbags?id=1032764',
            "category": 'handbags-extra-large-handbags',
            "department": 'handbags',
        },
        'handbags-fashion-backpacks': {
            "url": 'https://www.bloomingdales.com/shop/handbags/fashion-backpacks?id=1292496',
            "category": 'handbags-fashion-backpacks',
            "department": 'handbags',
        },
        'handbags-handbags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/handbags?id=16959',
            "category": 'handbags-handbags',
            "department": 'handbags',
        },
        'handbags-handbags-under-500': {
            "url": 'https://www.bloomingdales.com/shop/handbags/handbags-under-500?id=1225359',
            "category": 'handbags-handbags-under-500',
            "department": 'handbags',
        },
        'handbags-hobo-bags-trend': {
            "url": 'https://www.bloomingdales.com/shop/handbags/hobo-bags-trend?id=1086062',
            "category": 'handbags-hobo-bags-trend',
            "department": 'handbags',
        },
        'handbags-hobos-shoulder-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/hobos-shoulder-bags?id=17311',
            "category": 'handbags-hobos-shoulder-bags',
            "department": 'handbags',
        },
        'handbags-large-handbags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/large-handbags?id=1032763',
            "category": 'handbags-large-handbags',
            "department": 'handbags',
        },
        'handbags-lookbooks-guides': {
            "url": 'https://www.bloomingdales.com/shop/handbags/lookbooks-guides?id=1006665',
            "category": 'handbags-lookbooks-guides',
            "department": 'handbags',
        },
        'handbags-medium-sized-handbags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/medium-sized-handbags?id=1032762',
            "category": 'handbags-medium-sized-handbags',
            "department": 'handbags',
        },
        'handbags-mini-bags-small-handbags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/mini-bags-small-handbags?id=1002230',
            "category": 'handbags-mini-bags-small-handbags',
            "department": 'handbags',
        },
        'handbags-pre-owned-luxury': {
            "url": 'https://www.bloomingdales.com/shop/handbags/pre-owned-luxury?id=1211869',
            "category": 'handbags-pre-owned-luxury',
            "department": 'handbags',
        },
        'handbags-raffia-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/raffia-bags?id=1279411',
            "category": 'handbags-raffia-bags',
            "department": 'handbags',
        },
        'handbags-satchels': {
            "url": 'https://www.bloomingdales.com/shop/handbags/satchels?id=17312',
            "category": 'handbags-satchels',
            "department": 'handbags',
        },
        'handbags-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/handbags/shop-all?id=1218559',
            "category": 'handbags-shop-all',
            "department": 'handbags',
        },
        'handbags-small-handbags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/small-handbags?id=1032761',
            "category": 'handbags-small-handbags',
            "department": 'handbags',
        },
        'handbags-suede-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/suede-bags?id=1285895',
            "category": 'handbags-suede-bags',
            "department": 'handbags',
        },
        'handbags-tote-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/tote-bags?id=19993',
            "category": 'handbags-tote-bags',
            "department": 'handbags',
        },
        'handbags-wallets': {
            "url": 'https://www.bloomingdales.com/shop/handbags/wallets?id=1292335',
            "category": 'handbags-wallets',
            "department": 'handbags',
        },
        'handbags-wallets-small-accessories': {
            "url": 'https://www.bloomingdales.com/shop/handbags/wallets-small-accessories?id=1337295',
            "category": 'handbags-wallets-small-accessories',
            "department": 'handbags',
        },
        'handbags-womens-backpacks-travel-bags': {
            "url": 'https://www.bloomingdales.com/shop/handbags/womens-backpacks-travel-bags?id=1000369',
            "category": 'handbags-womens-backpacks-travel-bags',
            "department": 'handbags',
        },
        'handbags-womens-designer-wallets-wristlets': {
            "url": 'https://www.bloomingdales.com/shop/handbags/womens-designer-wallets-wristlets?id=1000417',
            "category": 'handbags-womens-designer-wallets-wristlets',
            "department": 'handbags',
        },
        'handbags-womens-handbags-purses': {
            "url": 'https://www.bloomingdales.com/shop/handbags/womens-handbags-purses?id=17316',
            "category": 'handbags-womens-handbags-purses',
            "department": 'handbags',
        },
    },
    'hearts-on-fire': {
        'hearts-on-fire': {
            "url": 'https://www.bloomingdales.com/shop/hearts-on-fire?id=1307500',
            "category": 'hearts-on-fire',
            "department": 'hearts-on-fire',
        },
    },
    'heritage-prints': {
        'heritage-prints': {
            "url": 'https://www.bloomingdales.com/shop/heritage-prints?id=1242797',
            "category": 'heritage-prints',
            "department": 'heritage-prints',
        },
    },
    'hermes-beauty': {
        'hermes-beauty': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty?id=1085759',
            "category": 'hermes-beauty',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-accessories': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/accessories?id=1299205',
            "category": 'hermes-beauty-accessories',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/bath-body?id=1003568',
            "category": 'hermes-beauty-bath-body',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/fragrance?id=1299696',
            "category": 'hermes-beauty-fragrance',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/gift-sets?id=1299206',
            "category": 'hermes-beauty-gift-sets',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-makeup': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/makeup?id=1088459',
            "category": 'hermes-beauty-makeup',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-mens-fragrances-colognes': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/mens-fragrances-colognes?id=1000530',
            "category": 'hermes-beauty-mens-fragrances-colognes',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-nails': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/nails?id=1323000',
            "category": 'hermes-beauty-nails',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/shop-all?id=1196859',
            "category": 'hermes-beauty-shop-all',
            "department": 'hermes-beauty',
        },
        'hermes-beauty-womens-fragrances-perfumes': {
            "url": 'https://www.bloomingdales.com/shop/hermes-beauty/womens-fragrances-perfumes?id=1000528',
            "category": 'hermes-beauty-womens-fragrances-perfumes',
            "department": 'hermes-beauty',
        },
    },
    'hermes-perfumer': {
        'hermes-perfumer': {
            "url": 'https://www.bloomingdales.com/shop/hermes-perfumer?id=1003109',
            "category": 'hermes-perfumer',
            "department": 'hermes-perfumer',
        },
    },
    'hestan': {
        'hestan': {
            "url": 'https://www.bloomingdales.com/shop/hestan?id=1268995',
            "category": 'hestan',
            "department": 'hestan',
        },
    },
    'hoka': {
        'hoka': {
            "url": 'https://www.bloomingdales.com/shop/hoka?id=1201370',
            "category": 'hoka',
            "department": 'hoka',
        },
        'hoka-bondi': {
            "url": 'https://www.bloomingdales.com/shop/hoka/bondi?id=1287723',
            "category": 'hoka-bondi',
            "department": 'hoka',
        },
        'hoka-kids-shoes': {
            "url": 'https://www.bloomingdales.com/shop/hoka/kids-shoes?id=1268596',
            "category": 'hoka-kids-shoes',
            "department": 'hoka',
        },
        'hoka-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/hoka/mens-shoes?id=1200959',
            "category": 'hoka-mens-shoes',
            "department": 'hoka',
        },
        'hoka-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/hoka/womens-shoes?id=1201372',
            "category": 'hoka-womens-shoes',
            "department": 'hoka',
        },
    },
    'holiday-dinner-party': {
        'holiday-dinner-party': {
            "url": 'https://www.bloomingdales.com/shop/holiday-dinner-party?id=1253725',
            "category": 'holiday-dinner-party',
            "department": 'holiday-dinner-party',
        },
    },
    'holiday-gifts-for-her': {
        'holiday-gifts-for-her': {
            "url": 'https://www.bloomingdales.com/shop/holiday-gifts-for-her?id=1291698',
            "category": 'holiday-gifts-for-her',
            "department": 'holiday-gifts-for-her',
        },
    },
    'holiday-gifts-for-him': {
        'holiday-gifts-for-him': {
            "url": 'https://www.bloomingdales.com/shop/holiday-gifts-for-him?id=1291699',
            "category": 'holiday-gifts-for-him',
            "department": 'holiday-gifts-for-him',
        },
    },
    'holiday-gifts-for-kids': {
        'holiday-gifts-for-kids': {
            "url": 'https://www.bloomingdales.com/shop/holiday-gifts-for-kids?id=1291696',
            "category": 'holiday-gifts-for-kids',
            "department": 'holiday-gifts-for-kids',
        },
    },
    'holiday-gifts-for-teens': {
        'holiday-gifts-for-teens': {
            "url": 'https://www.bloomingdales.com/shop/holiday-gifts-for-teens?id=1291704',
            "category": 'holiday-gifts-for-teens',
            "department": 'holiday-gifts-for-teens',
        },
    },
    'holiday-gifts-for-your-home': {
        'holiday-gifts-for-your-home': {
            "url": 'https://www.bloomingdales.com/shop/holiday-gifts-for-your-home?id=1291697',
            "category": 'holiday-gifts-for-your-home',
            "department": 'holiday-gifts-for-your-home',
        },
    },
    'hollywood': {
        'hollywood': {
            "url": 'https://www.bloomingdales.com/shop/hollywood?id=1238681',
            "category": 'hollywood',
            "department": 'hollywood',
        },
    },
    'home': {
        'home': {
            "url": 'https://www.bloomingdales.com/shop/home?id=1319135',
            "category": 'home',
            "department": 'home',
        },
        'home-10x13-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/10x13-rugs?id=1201859',
            "category": 'home-10x13-rugs',
            "department": 'home',
        },
        'home-5x8-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/5x8-rugs?id=1201860',
            "category": 'home-5x8-rugs',
            "department": 'home',
        },
        'home-8x10-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/8x10-rugs?id=1201861',
            "category": 'home-8x10-rugs',
            "department": 'home',
        },
        'home-9x12-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/9x12-rugs?id=1201862',
            "category": 'home-9x12-rugs',
            "department": 'home',
        },
        'home-air-fryers': {
            "url": 'https://www.bloomingdales.com/shop/home/air-fryers?id=1272598',
            "category": 'home-air-fryers',
            "department": 'home',
        },
        'home-all-home-decor': {
            "url": 'https://www.bloomingdales.com/shop/home/all-home-decor?id=1144109',
            "category": 'home-all-home-decor',
            "department": 'home',
        },
        'home-all-purpose-utility-knives': {
            "url": 'https://www.bloomingdales.com/shop/home/all-purpose-utility-knives?id=1005826',
            "category": 'home-all-purpose-utility-knives',
            "department": 'home',
        },
        'home-bakeware': {
            "url": 'https://www.bloomingdales.com/shop/home/bakeware?id=1000235',
            "category": 'home-bakeware',
            "department": 'home',
        },
        'home-baking-dishes': {
            "url": 'https://www.bloomingdales.com/shop/home/baking-dishes?id=1005803',
            "category": 'home-baking-dishes',
            "department": 'home',
        },
        'home-baking-pans': {
            "url": 'https://www.bloomingdales.com/shop/home/baking-pans?id=16029',
            "category": 'home-baking-pans',
            "department": 'home',
        },
        'home-baking-pans-sheets': {
            "url": 'https://www.bloomingdales.com/shop/home/baking-pans-sheets?id=1005804',
            "category": 'home-baking-pans-sheets',
            "department": 'home',
        },
        'home-bar-carts-and-serving-carts': {
            "url": 'https://www.bloomingdales.com/shop/home/bar-carts-and-serving-carts?id=1005615',
            "category": 'home-bar-carts-and-serving-carts',
            "department": 'home',
        },
        'home-bath': {
            "url": 'https://www.bloomingdales.com/shop/home/bath?id=1000241',
            "category": 'home-bath',
            "department": 'home',
        },
        'home-bath-sheets': {
            "url": 'https://www.bloomingdales.com/shop/home/bath-sheets?id=1006959',
            "category": 'home-bath-sheets',
            "department": 'home',
        },
        'home-bath-towels': {
            "url": 'https://www.bloomingdales.com/shop/home/bath-towels?id=1006960',
            "category": 'home-bath-towels',
            "department": 'home',
        },
        'home-bathroom-decor': {
            "url": 'https://www.bloomingdales.com/shop/home/bathroom-decor?id=1006955',
            "category": 'home-bathroom-decor',
            "department": 'home',
        },
        'home-bathroom-decor-accessories': {
            "url": 'https://www.bloomingdales.com/shop/home/bathroom-decor-accessories?id=1063260',
            "category": 'home-bathroom-decor-accessories',
            "department": 'home',
        },
        'home-bathroom-furnitures-fixtures': {
            "url": 'https://www.bloomingdales.com/shop/home/bathroom-furnitures-fixtures?id=1006956',
            "category": 'home-bathroom-furnitures-fixtures',
            "department": 'home',
        },
        'home-bathroom-rugs-mats': {
            "url": 'https://www.bloomingdales.com/shop/home/bathroom-rugs-mats?id=8207',
            "category": 'home-bathroom-rugs-mats',
            "department": 'home',
        },
        'home-beach-towels': {
            "url": 'https://www.bloomingdales.com/shop/home/beach-towels?id=1005677',
            "category": 'home-beach-towels',
            "department": 'home',
        },
        'home-bed-and-bath': {
            "url": 'https://www.bloomingdales.com/shop/home/bed-and-bath?id=8203',
            "category": 'home-bed-and-bath',
            "department": 'home',
        },
        'home-bed-frames': {
            "url": 'https://www.bloomingdales.com/shop/home/bed-frames?id=1271913',
            "category": 'home-bed-frames',
            "department": 'home',
        },
        'home-bedding-essentials-luxury-bed-pillows': {
            "url": 'https://www.bloomingdales.com/shop/home/bedding-essentials-luxury-bed-pillows?id=1144068',
            "category": 'home-bedding-essentials-luxury-bed-pillows',
            "department": 'home',
        },
        'home-beds': {
            "url": 'https://www.bloomingdales.com/shop/home/beds?id=22300',
            "category": 'home-beds',
            "department": 'home',
        },
        'home-bedskirt': {
            "url": 'https://www.bloomingdales.com/shop/home/bedskirt?id=1055060',
            "category": 'home-bedskirt',
            "department": 'home',
        },
        'home-benches': {
            "url": 'https://www.bloomingdales.com/shop/home/benches?id=1270296',
            "category": 'home-benches',
            "department": 'home',
        },
        'home-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/home/best-sellers?id=1002516',
            "category": 'home-best-sellers',
            "department": 'home',
        },
        'home-big-game-prep': {
            "url": 'https://www.bloomingdales.com/shop/home/big-game-prep?id=1260398',
            "category": 'home-big-game-prep',
            "department": 'home',
        },
        'home-blenders-juicer': {
            "url": 'https://www.bloomingdales.com/shop/home/blenders-juicer?id=1005827',
            "category": 'home-blenders-juicer',
            "department": 'home',
        },
        'home-books': {
            "url": 'https://www.bloomingdales.com/shop/home/books?id=1030672',
            "category": 'home-books',
            "department": 'home',
        },
        'home-bowls': {
            "url": 'https://www.bloomingdales.com/shop/home/bowls?id=1244296',
            "category": 'home-bowls',
            "department": 'home',
        },
        'home-bowls-trays-vases': {
            "url": 'https://www.bloomingdales.com/shop/home/bowls-trays-vases?id=1001541',
            "category": 'home-bowls-trays-vases',
            "department": 'home',
        },
        'home-bread-knives': {
            "url": 'https://www.bloomingdales.com/shop/home/bread-knives?id=1005820',
            "category": 'home-bread-knives',
            "department": 'home',
        },
        'home-cake-plates-tiered-cake-stand': {
            "url": 'https://www.bloomingdales.com/shop/home/cake-plates-tiered-cake-stand?id=1005747',
            "category": 'home-cake-plates-tiered-cake-stand',
            "department": 'home',
        },
        'home-candle-gift-sets-collections': {
            "url": 'https://www.bloomingdales.com/shop/home/candle-gift-sets-collections?id=1005850',
            "category": 'home-candle-gift-sets-collections',
            "department": 'home',
        },
        'home-canisters': {
            "url": 'https://www.bloomingdales.com/shop/home/canisters?id=1272600',
            "category": 'home-canisters',
            "department": 'home',
        },
        'home-canisters-food-storage-containers': {
            "url": 'https://www.bloomingdales.com/shop/home/canisters-food-storage-containers?id=1020060',
            "category": 'home-canisters-food-storage-containers',
            "department": 'home',
        },
        'home-carry-on-bags': {
            "url": 'https://www.bloomingdales.com/shop/home/carry-on-bags?id=1000314',
            "category": 'home-carry-on-bags',
            "department": 'home',
        },
        'home-carving-knife-sets-boning-knives': {
            "url": 'https://www.bloomingdales.com/shop/home/carving-knife-sets-boning-knives?id=1005824',
            "category": 'home-carving-knife-sets-boning-knives',
            "department": 'home',
        },
        'home-chandeliers': {
            "url": 'https://www.bloomingdales.com/shop/home/chandeliers?id=1270298',
            "category": 'home-chandeliers',
            "department": 'home',
        },
        'home-checked-luggage': {
            "url": 'https://www.bloomingdales.com/shop/home/checked-luggage?id=1000318',
            "category": 'home-checked-luggage',
            "department": 'home',
        },
        'home-cheese-board-set': {
            "url": 'https://www.bloomingdales.com/shop/home/cheese-board-set?id=1005748',
            "category": 'home-cheese-board-set',
            "department": 'home',
        },
        'home-chef-and-santoku-knives': {
            "url": 'https://www.bloomingdales.com/shop/home/chef-and-santoku-knives?id=1005821',
            "category": 'home-chef-and-santoku-knives',
            "department": 'home',
        },
        'home-chip-and-dip-bowls': {
            "url": 'https://www.bloomingdales.com/shop/home/chip-and-dip-bowls?id=8312',
            "category": 'home-chip-and-dip-bowls',
            "department": 'home',
        },
        'home-chip-and-dip-bowls-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/chip-and-dip-bowls-sets?id=1005749',
            "category": 'home-chip-and-dip-bowls-sets',
            "department": 'home',
        },
        'home-closet-organization-tools': {
            "url": 'https://www.bloomingdales.com/shop/home/closet-organization-tools?id=1001782',
            "category": 'home-closet-organization-tools',
            "department": 'home',
        },
        'home-cloth-linen-dinner-napkins': {
            "url": 'https://www.bloomingdales.com/shop/home/cloth-linen-dinner-napkins?id=1005756',
            "category": 'home-cloth-linen-dinner-napkins',
            "department": 'home',
        },
        'home-cocktail-beer-wine-accessories-bar-tools': {
            "url": 'https://www.bloomingdales.com/shop/home/cocktail-beer-wine-accessories-bar-tools?id=1054659',
            "category": 'home-cocktail-beer-wine-accessories-bar-tools',
            "department": 'home',
        },
        'home-cocktail-shakers-bar-tools': {
            "url": 'https://www.bloomingdales.com/shop/home/cocktail-shakers-bar-tools?id=1272403',
            "category": 'home-cocktail-shakers-bar-tools',
            "department": 'home',
        },
        'home-coffee-espresso-accessories': {
            "url": 'https://www.bloomingdales.com/shop/home/coffee-espresso-accessories?id=1005808',
            "category": 'home-coffee-espresso-accessories',
            "department": 'home',
        },
        'home-coffee-espresso-tea': {
            "url": 'https://www.bloomingdales.com/shop/home/coffee-espresso-tea?id=1000236',
            "category": 'home-coffee-espresso-tea',
            "department": 'home',
        },
        'home-coffee-grinders': {
            "url": 'https://www.bloomingdales.com/shop/home/coffee-grinders?id=1292399',
            "category": 'home-coffee-grinders',
            "department": 'home',
        },
        'home-coffee-makers': {
            "url": 'https://www.bloomingdales.com/shop/home/coffee-makers?id=1005807',
            "category": 'home-coffee-makers',
            "department": 'home',
        },
        'home-coffee-table-books': {
            "url": 'https://www.bloomingdales.com/shop/home/coffee-table-books?id=1171959',
            "category": 'home-coffee-table-books',
            "department": 'home',
        },
        'home-collectibles': {
            "url": 'https://www.bloomingdales.com/shop/home/collectibles?id=1005856',
            "category": 'home-collectibles',
            "department": 'home',
        },
        'home-contemporary-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/contemporary-rugs?id=1325707',
            "category": 'home-contemporary-rugs',
            "department": 'home',
        },
        'home-cooking-utensil-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/cooking-utensil-sets?id=1020061',
            "category": 'home-cooking-utensil-sets',
            "department": 'home',
        },
        'home-cookware': {
            "url": 'https://www.bloomingdales.com/shop/home/cookware?id=1000237',
            "category": 'home-cookware',
            "department": 'home',
        },
        'home-cookware-pot-pan-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/cookware-pot-pan-sets?id=1005811',
            "category": 'home-cookware-pot-pan-sets',
            "department": 'home',
        },
        'home-cozy-gifts': {
            "url": 'https://www.bloomingdales.com/shop/home/cozy-gifts?id=1215663',
            "category": 'home-cozy-gifts',
            "department": 'home',
        },
        'home-cozy-throws-robes': {
            "url": 'https://www.bloomingdales.com/shop/home/cozy-throws-robes?id=1215667',
            "category": 'home-cozy-throws-robes',
            "department": 'home',
        },
        'home-crossbody-travel-bags': {
            "url": 'https://www.bloomingdales.com/shop/home/crossbody-travel-bags?id=1005640',
            "category": 'home-crossbody-travel-bags',
            "department": 'home',
        },
        'home-cups': {
            "url": 'https://www.bloomingdales.com/shop/home/cups?id=1244297',
            "category": 'home-cups',
            "department": 'home',
        },
        'home-cute-coffee-mugs': {
            "url": 'https://www.bloomingdales.com/shop/home/cute-coffee-mugs?id=1005809',
            "category": 'home-cute-coffee-mugs',
            "department": 'home',
        },
        'home-cutting-boards': {
            "url": 'https://www.bloomingdales.com/shop/home/cutting-boards?id=1005836',
            "category": 'home-cutting-boards',
            "department": 'home',
        },
        'home-decanters': {
            "url": 'https://www.bloomingdales.com/shop/home/decanters?id=1272414',
            "category": 'home-decanters',
            "department": 'home',
        },
        'home-designer-bed-sheets-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-bed-sheets-sets?id=1248195',
            "category": 'home-designer-bed-sheets-sets',
            "department": 'home',
        },
        'home-designer-bedding': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-bedding?id=1004676',
            "category": 'home-designer-bedding',
            "department": 'home',
        },
        'home-designer-bedding-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-bedding-sets?id=1004678',
            "category": 'home-designer-bedding-sets',
            "department": 'home',
        },
        'home-designer-bedding-sets-collections': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-bedding-sets-collections?id=1144065',
            "category": 'home-designer-bedding-sets-collections',
            "department": 'home',
        },
        'home-designer-coffee-tables': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-coffee-tables?id=1000625',
            "category": 'home-designer-coffee-tables',
            "department": 'home',
        },
        'home-designer-pillows-throw-blankets': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-pillows-throw-blankets?id=1001548',
            "category": 'home-designer-pillows-throw-blankets',
            "department": 'home',
        },
        'home-designer-quilts-coverlets': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-quilts-coverlets?id=1144084',
            "category": 'home-designer-quilts-coverlets',
            "department": 'home',
        },
        'home-designer-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-rugs?id=1001971',
            "category": 'home-designer-rugs',
            "department": 'home',
        },
        'home-designer-side-end-tables': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-side-end-tables?id=1073559',
            "category": 'home-designer-side-end-tables',
            "department": 'home',
        },
        'home-designer-tv-stands-console-tables': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-tv-stands-console-tables?id=1073659',
            "category": 'home-designer-tv-stands-console-tables',
            "department": 'home',
        },
        'home-designer-water-bottles-travel-mugs': {
            "url": 'https://www.bloomingdales.com/shop/home/designer-water-bottles-travel-mugs?id=1020059',
            "category": 'home-designer-water-bottles-travel-mugs',
            "department": 'home',
        },
        'home-dining-entertaining': {
            "url": 'https://www.bloomingdales.com/shop/home/dining-entertaining?id=8237',
            "category": 'home-dining-entertaining',
            "department": 'home',
        },
        'home-dining-room-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/dining-room-sets?id=1275007',
            "category": 'home-dining-room-sets',
            "department": 'home',
        },
        'home-dinner-table-settings': {
            "url": 'https://www.bloomingdales.com/shop/home/dinner-table-settings?id=1006940',
            "category": 'home-dinner-table-settings',
            "department": 'home',
        },
        'home-dinnerware': {
            "url": 'https://www.bloomingdales.com/shop/home/dinnerware?id=1000231',
            "category": 'home-dinnerware',
            "department": 'home',
        },
        'home-dutch-ovens': {
            "url": 'https://www.bloomingdales.com/shop/home/dutch-ovens?id=1005812',
            "category": 'home-dutch-ovens',
            "department": 'home',
        },
        'home-duvet-covers': {
            "url": 'https://www.bloomingdales.com/shop/home/duvet-covers?id=1243599',
            "category": 'home-duvet-covers',
            "department": 'home',
        },
        'home-duvets': {
            "url": 'https://www.bloomingdales.com/shop/home/duvets?id=1243597',
            "category": 'home-duvets',
            "department": 'home',
        },
        'home-duvets-quilts-shams': {
            "url": 'https://www.bloomingdales.com/shop/home/duvets-quilts-shams?id=1243595',
            "category": 'home-duvets-quilts-shams',
            "department": 'home',
        },
        'home-elegant-designer-wall-art': {
            "url": 'https://www.bloomingdales.com/shop/home/elegant-designer-wall-art?id=1005868',
            "category": 'home-elegant-designer-wall-art',
            "department": 'home',
        },
        'home-espresso-machines': {
            "url": 'https://www.bloomingdales.com/shop/home/espresso-machines?id=1292395',
            "category": 'home-espresso-machines',
            "department": 'home',
        },
        'home-espresso-machines-under-500': {
            "url": 'https://www.bloomingdales.com/shop/home/espresso-machines-under-500?id=1292397',
            "category": 'home-espresso-machines-under-500',
            "department": 'home',
        },
        'home-everyday-dishes': {
            "url": 'https://www.bloomingdales.com/shop/home/everyday-dishes?id=1244300',
            "category": 'home-everyday-dishes',
            "department": 'home',
        },
        'home-exquisite-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/exquisite-rugs?id=1235259',
            "category": 'home-exquisite-rugs',
            "department": 'home',
        },
        'home-farmhouse-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/farmhouse-rugs?id=1325706',
            "category": 'home-farmhouse-rugs',
            "department": 'home',
        },
        'home-featured-brands': {
            "url": 'https://www.bloomingdales.com/shop/home/featured-brands?id=1232559',
            "category": 'home-featured-brands',
            "department": 'home',
        },
        'home-fine-china': {
            "url": 'https://www.bloomingdales.com/shop/home/fine-china?id=1244299',
            "category": 'home-fine-china',
            "department": 'home',
        },
        'home-fitness-equipment': {
            "url": 'https://www.bloomingdales.com/shop/home/fitness-equipment?id=1302395',
            "category": 'home-fitness-equipment',
            "department": 'home',
        },
        'home-flatware': {
            "url": 'https://www.bloomingdales.com/shop/home/flatware?id=1000233',
            "category": 'home-flatware',
            "department": 'home',
        },
        'home-flatware-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/flatware-sets?id=8304',
            "category": 'home-flatware-sets',
            "department": 'home',
        },
        'home-flowers-plants-planters': {
            "url": 'https://www.bloomingdales.com/shop/home/flowers-plants-planters?id=1154860',
            "category": 'home-flowers-plants-planters',
            "department": 'home',
        },
        'home-flush-mounts': {
            "url": 'https://www.bloomingdales.com/shop/home/flush-mounts?id=1270300',
            "category": 'home-flush-mounts',
            "department": 'home',
        },
        'home-food-prep-tools': {
            "url": 'https://www.bloomingdales.com/shop/home/food-prep-tools?id=1020063',
            "category": 'home-food-prep-tools',
            "department": 'home',
        },
        'home-food-processors': {
            "url": 'https://www.bloomingdales.com/shop/home/food-processors?id=1005828',
            "category": 'home-food-processors',
            "department": 'home',
        },
        'home-furniture-mattresses': {
            "url": 'https://www.bloomingdales.com/shop/home/furniture-mattresses?id=1006362',
            "category": 'home-furniture-mattresses',
            "department": 'home',
        },
        'home-furniture-products': {
            "url": 'https://www.bloomingdales.com/shop/home/furniture-products?id=1004306',
            "category": 'home-furniture-products',
            "department": 'home',
        },
        'home-games-entertainment': {
            "url": 'https://www.bloomingdales.com/shop/home/games-entertainment?id=1307401',
            "category": 'home-games-entertainment',
            "department": 'home',
        },
        'home-garment-bags': {
            "url": 'https://www.bloomingdales.com/shop/home/garment-bags?id=1000316',
            "category": 'home-garment-bags',
            "department": 'home',
        },
        'home-geometric-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/geometric-rugs?id=1025459',
            "category": 'home-geometric-rugs',
            "department": 'home',
        },
        'home-gift-sets-advent-calendars': {
            "url": 'https://www.bloomingdales.com/shop/home/gift-sets-advent-calendars?id=1215665',
            "category": 'home-gift-sets-advent-calendars',
            "department": 'home',
        },
        'home-glassware-stemware-drinkware': {
            "url": 'https://www.bloomingdales.com/shop/home/glassware-stemware-drinkware?id=1000232',
            "category": 'home-glassware-stemware-drinkware',
            "department": 'home',
        },
        'home-gourmet-food-gifts-luxury-gift-baskets': {
            "url": 'https://www.bloomingdales.com/shop/home/gourmet-food-gifts-luxury-gift-baskets?id=1000265',
            "category": 'home-gourmet-food-gifts-luxury-gift-baskets',
            "department": 'home',
        },
        'home-gravy-boat': {
            "url": 'https://www.bloomingdales.com/shop/home/gravy-boat?id=8316',
            "category": 'home-gravy-boat',
            "department": 'home',
        },
        'home-griddles-grill-pans': {
            "url": 'https://www.bloomingdales.com/shop/home/griddles-grill-pans?id=1005813',
            "category": 'home-griddles-grill-pans',
            "department": 'home',
        },
        'home-grilling-tools': {
            "url": 'https://www.bloomingdales.com/shop/home/grilling-tools?id=1005838',
            "category": 'home-grilling-tools',
            "department": 'home',
        },
        'home-hand-mixers': {
            "url": 'https://www.bloomingdales.com/shop/home/hand-mixers?id=1272596',
            "category": 'home-hand-mixers',
            "department": 'home',
        },
        'home-hand-towels-guest-towels': {
            "url": 'https://www.bloomingdales.com/shop/home/hand-towels-guest-towels?id=1006961',
            "category": 'home-hand-towels-guest-towels',
            "department": 'home',
        },
        'home-handmade-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/handmade-rugs?id=1025164',
            "category": 'home-handmade-rugs',
            "department": 'home',
        },
        'home-headboards': {
            "url": 'https://www.bloomingdales.com/shop/home/headboards?id=1270301',
            "category": 'home-headboards',
            "department": 'home',
        },
        'home-high-quality-down-pillows': {
            "url": 'https://www.bloomingdales.com/shop/home/high-quality-down-pillows?id=1005713',
            "category": 'home-high-quality-down-pillows',
            "department": 'home',
        },
        'home-high-quality-knives-cutlery': {
            "url": 'https://www.bloomingdales.com/shop/home/high-quality-knives-cutlery?id=1000238',
            "category": 'home-high-quality-knives-cutlery',
            "department": 'home',
        },
        'home-holiday-desserts-tea': {
            "url": 'https://www.bloomingdales.com/shop/home/holiday-desserts-tea?id=1215666',
            "category": 'home-holiday-desserts-tea',
            "department": 'home',
        },
        'home-holiday-home-fragrances': {
            "url": 'https://www.bloomingdales.com/shop/home/holiday-home-fragrances?id=1213160',
            "category": 'home-holiday-home-fragrances',
            "department": 'home',
        },
        'home-home-accents-accessories': {
            "url": 'https://www.bloomingdales.com/shop/home/home-accents-accessories?id=1144097',
            "category": 'home-home-accents-accessories',
            "department": 'home',
        },
        'home-home-care-electronics': {
            "url": 'https://www.bloomingdales.com/shop/home/home-care-electronics?id=1001393',
            "category": 'home-home-care-electronics',
            "department": 'home',
        },
        'home-home-decor': {
            "url": 'https://www.bloomingdales.com/shop/home/home-decor?id=1001539',
            "category": 'home-home-decor',
            "department": 'home',
        },
        'home-home-guides': {
            "url": 'https://www.bloomingdales.com/shop/home/home-guides?id=1002042',
            "category": 'home-home-guides',
            "department": 'home',
        },
        'home-home-storage-organization': {
            "url": 'https://www.bloomingdales.com/shop/home/home-storage-organization?id=1006331',
            "category": 'home-home-storage-organization',
            "department": 'home',
        },
        'home-housewarming-party-games-home-entertainment': {
            "url": 'https://www.bloomingdales.com/shop/home/housewarming-party-games-home-entertainment?id=1019767',
            "category": 'home-housewarming-party-games-home-entertainment',
            "department": 'home',
        },
        'home-ice-buckets': {
            "url": 'https://www.bloomingdales.com/shop/home/ice-buckets?id=1272413',
            "category": 'home-ice-buckets',
            "department": 'home',
        },
        'home-in-stock-furniture': {
            "url": 'https://www.bloomingdales.com/shop/home/in-stock-furniture?id=1157467',
            "category": 'home-in-stock-furniture',
            "department": 'home',
        },
        'home-indoor-grills-griddles': {
            "url": 'https://www.bloomingdales.com/shop/home/indoor-grills-griddles?id=8178',
            "category": 'home-indoor-grills-griddles',
            "department": 'home',
        },
        'home-jewelry-boxes-ring-holders': {
            "url": 'https://www.bloomingdales.com/shop/home/jewelry-boxes-ring-holders?id=22002',
            "category": 'home-jewelry-boxes-ring-holders',
            "department": 'home',
        },
        'home-judaica': {
            "url": 'https://www.bloomingdales.com/shop/home/judaica?id=1206966',
            "category": 'home-judaica',
            "department": 'home',
        },
        'home-juicers': {
            "url": 'https://www.bloomingdales.com/shop/home/juicers?id=1005829',
            "category": 'home-juicers',
            "department": 'home',
        },
        'home-kiddush-cups': {
            "url": 'https://www.bloomingdales.com/shop/home/kiddush-cups?id=1006951',
            "category": 'home-kiddush-cups',
            "department": 'home',
        },
        'home-kitchen': {
            "url": 'https://www.bloomingdales.com/shop/home/kitchen?id=1000245',
            "category": 'home-kitchen',
            "department": 'home',
        },
        'home-kitchen-gadgets-tools': {
            "url": 'https://www.bloomingdales.com/shop/home/kitchen-gadgets-tools?id=1000240',
            "category": 'home-kitchen-gadgets-tools',
            "department": 'home',
        },
        'home-kitchen-linens-towels-mitts': {
            "url": 'https://www.bloomingdales.com/shop/home/kitchen-linens-towels-mitts?id=1020062',
            "category": 'home-kitchen-linens-towels-mitts',
            "department": 'home',
        },
        'home-kitchen-mats': {
            "url": 'https://www.bloomingdales.com/shop/home/kitchen-mats?id=1272601',
            "category": 'home-kitchen-mats',
            "department": 'home',
        },
        'home-kitchen-measuring-mixing-tools': {
            "url": 'https://www.bloomingdales.com/shop/home/kitchen-measuring-mixing-tools?id=1005840',
            "category": 'home-kitchen-measuring-mixing-tools',
            "department": 'home',
        },
        'home-laundry': {
            "url": 'https://www.bloomingdales.com/shop/home/laundry?id=1272603',
            "category": 'home-laundry',
            "department": 'home',
        },
        'home-loveseats': {
            "url": 'https://www.bloomingdales.com/shop/home/loveseats?id=1271914',
            "category": 'home-loveseats',
            "department": 'home',
        },
        'home-luggage-collections': {
            "url": 'https://www.bloomingdales.com/shop/home/luggage-collections?id=1005594',
            "category": 'home-luggage-collections',
            "department": 'home',
        },
        'home-luggage-travel': {
            "url": 'https://www.bloomingdales.com/shop/home/luggage-travel?id=1005589',
            "category": 'home-luggage-travel',
            "department": 'home',
        },
        'home-luxury-bath-sheets': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-bath-sheets?id=1005697',
            "category": 'home-luxury-bath-sheets',
            "department": 'home',
        },
        'home-luxury-bath-towels': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-bath-towels?id=1005698',
            "category": 'home-luxury-bath-towels',
            "department": 'home',
        },
        'home-luxury-bathroom-accessories-decor': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-bathroom-accessories-decor?id=1005704',
            "category": 'home-luxury-bathroom-accessories-decor',
            "department": 'home',
        },
        'home-luxury-bedding-comforter-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-bedding-comforter-sets?id=1144060',
            "category": 'home-luxury-bedding-comforter-sets',
            "department": 'home',
        },
        'home-luxury-blankets-down-blankets': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-blankets-down-blankets?id=1055059',
            "category": 'home-luxury-blankets-down-blankets',
            "department": 'home',
        },
        'home-luxury-candles': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-candles?id=1005851',
            "category": 'home-luxury-candles',
            "department": 'home',
        },
        'home-luxury-designer-beach-towels': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-designer-beach-towels?id=1005699',
            "category": 'home-luxury-designer-beach-towels',
            "department": 'home',
        },
        'home-luxury-down-comforters': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-down-comforters?id=1005712',
            "category": 'home-luxury-down-comforters',
            "department": 'home',
        },
        'home-luxury-home-fragrances-candles-diffusers': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-home-fragrances-candles-diffusers?id=1001542',
            "category": 'home-luxury-home-fragrances-candles-diffusers',
            "department": 'home',
        },
        'home-luxury-lighting': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-lighting?id=1001009',
            "category": 'home-luxury-lighting',
            "department": 'home',
        },
        'home-luxury-mattress': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-mattress?id=1001973',
            "category": 'home-luxury-mattress',
            "department": 'home',
        },
        'home-luxury-room-oil-diffusers-home-scents': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-room-oil-diffusers-home-scents?id=1005852',
            "category": 'home-luxury-room-oil-diffusers-home-scents',
            "department": 'home',
        },
        'home-luxury-washcloths': {
            "url": 'https://www.bloomingdales.com/shop/home/luxury-washcloths?id=1005701',
            "category": 'home-luxury-washcloths',
            "department": 'home',
        },
        'home-mezuzahs': {
            "url": 'https://www.bloomingdales.com/shop/home/mezuzahs?id=1006950',
            "category": 'home-mezuzahs',
            "department": 'home',
        },
        'home-milk-frothers': {
            "url": 'https://www.bloomingdales.com/shop/home/milk-frothers?id=1292398',
            "category": 'home-milk-frothers',
            "department": 'home',
        },
        'home-mink-home': {
            "url": 'https://www.bloomingdales.com/shop/home/mink-home?id=1235260',
            "category": 'home-mink-home',
            "department": 'home',
        },
        'home-mixers': {
            "url": 'https://www.bloomingdales.com/shop/home/mixers?id=1005830',
            "category": 'home-mixers',
            "department": 'home',
        },
        'home-mixing-bowl-set-measuring-cups-spoons': {
            "url": 'https://www.bloomingdales.com/shop/home/mixing-bowl-set-measuring-cups-spoons?id=1005806',
            "category": 'home-mixing-bowl-set-measuring-cups-spoons',
            "department": 'home',
        },
        'home-modern-beer-glasses-set-pilsner-glass': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-beer-glasses-set-pilsner-glass?id=1005740',
            "category": 'home-modern-beer-glasses-set-pilsner-glass',
            "department": 'home',
        },
        'home-modern-beverage-dispenser-water-pitcher': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-beverage-dispenser-water-pitcher?id=1005745',
            "category": 'home-modern-beverage-dispenser-water-pitcher',
            "department": 'home',
        },
        'home-modern-candle-holders-candlesticks': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-candle-holders-candlesticks?id=1005854',
            "category": 'home-modern-candle-holders-candlesticks',
            "department": 'home',
        },
        'home-modern-contemporary-bowls': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-bowls?id=1144088',
            "category": 'home-modern-contemporary-bowls',
            "department": 'home',
        },
        'home-modern-contemporary-decorative-pillows': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-decorative-pillows?id=1005870',
            "category": 'home-modern-contemporary-decorative-pillows',
            "department": 'home',
        },
        'home-modern-contemporary-designer-bar-stools': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-bar-stools?id=1005619',
            "category": 'home-modern-contemporary-designer-bar-stools',
            "department": 'home',
        },
        'home-modern-contemporary-designer-bedroom-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-bedroom-sets?id=1001858',
            "category": 'home-modern-contemporary-designer-bedroom-sets',
            "department": 'home',
        },
        'home-modern-contemporary-designer-bookcases-shelves': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-bookcases-shelves?id=21669',
            "category": 'home-modern-contemporary-designer-bookcases-shelves',
            "department": 'home',
        },
        'home-modern-contemporary-designer-dining-chairs': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-dining-chairs?id=1005620',
            "category": 'home-modern-contemporary-designer-dining-chairs',
            "department": 'home',
        },
        'home-modern-contemporary-designer-dining-tables': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-dining-tables?id=21658',
            "category": 'home-modern-contemporary-designer-dining-tables',
            "department": 'home',
        },
        'home-modern-contemporary-designer-floor-lamps-lights': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-floor-lamps-lights?id=1005861',
            "category": 'home-modern-contemporary-designer-floor-lamps-lights',
            "department": 'home',
        },
        'home-modern-contemporary-designer-nightstands': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-nightstands?id=1001857',
            "category": 'home-modern-contemporary-designer-nightstands',
            "department": 'home',
        },
        'home-modern-contemporary-designer-sectional-sofas': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-sectional-sofas?id=1003455',
            "category": 'home-modern-contemporary-designer-sectional-sofas',
            "department": 'home',
        },
        'home-modern-contemporary-designer-sleeper-sofas': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-sleeper-sofas?id=1005278',
            "category": 'home-modern-contemporary-designer-sleeper-sofas',
            "department": 'home',
        },
        'home-modern-contemporary-designer-sofas-couches': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-sofas-couches?id=21671',
            "category": 'home-modern-contemporary-designer-sofas-couches',
            "department": 'home',
        },
        'home-modern-contemporary-designer-table-lamps': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-table-lamps?id=1005862',
            "category": 'home-modern-contemporary-designer-table-lamps',
            "department": 'home',
        },
        'home-modern-contemporary-designer-wall-floor-mirrors': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-designer-wall-floor-mirrors?id=1005865',
            "category": 'home-modern-contemporary-designer-wall-floor-mirrors',
            "department": 'home',
        },
        'home-modern-contemporary-dressers-chest-drawers': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-dressers-chest-drawers?id=23527',
            "category": 'home-modern-contemporary-dressers-chest-drawers',
            "department": 'home',
        },
        'home-modern-contemporary-high-end-dining-room-furniture': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-high-end-dining-room-furniture?id=21652',
            "category": 'home-modern-contemporary-high-end-dining-room-furniture',
            "department": 'home',
        },
        'home-modern-contemporary-luxury-bedroom-furniture': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-luxury-bedroom-furniture?id=22299',
            "category": 'home-modern-contemporary-luxury-bedroom-furniture',
            "department": 'home',
        },
        'home-modern-contemporary-luxury-buffet-tables-bar-carts': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-luxury-buffet-tables-bar-carts?id=23614',
            "category": 'home-modern-contemporary-luxury-buffet-tables-bar-carts',
            "department": 'home',
        },
        'home-modern-contemporary-luxury-living-room-furniture': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-luxury-living-room-furniture?id=21653',
            "category": 'home-modern-contemporary-luxury-living-room-furniture',
            "department": 'home',
        },
        'home-modern-contemporary-mirrors-wall-art': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-mirrors-wall-art?id=1001546',
            "category": 'home-modern-contemporary-mirrors-wall-art',
            "department": 'home',
        },
        'home-modern-contemporary-recliners-armchairs-living-room-chairs': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-recliners-armchairs-living-room-chairs?id=21670',
            "category": 'home-modern-contemporary-recliners-armchairs-living-room-chairs',
            "department": 'home',
        },
        'home-modern-contemporary-throw-blankets': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-throw-blankets?id=1005871',
            "category": 'home-modern-contemporary-throw-blankets',
            "department": 'home',
        },
        'home-modern-contemporary-trays': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-trays?id=1005848',
            "category": 'home-modern-contemporary-trays',
            "department": 'home',
        },
        'home-modern-contemporary-vases': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-contemporary-vases?id=1005849',
            "category": 'home-modern-contemporary-vases',
            "department": 'home',
        },
        'home-modern-electric-tea-kettles': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-electric-tea-kettles?id=1005810',
            "category": 'home-modern-electric-tea-kettles',
            "department": 'home',
        },
        'home-modern-elegant-champagne-glasses': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-elegant-champagne-glasses?id=1005741',
            "category": 'home-modern-elegant-champagne-glasses',
            "department": 'home',
        },
        'home-modern-elegant-designer-placemats': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-elegant-designer-placemats?id=1005757',
            "category": 'home-modern-elegant-designer-placemats',
            "department": 'home',
        },
        'home-modern-elegant-designer-tablecloths': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-elegant-designer-tablecloths?id=1005758',
            "category": 'home-modern-elegant-designer-tablecloths',
            "department": 'home',
        },
        'home-modern-elegant-luxury-table-runners': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-elegant-luxury-table-runners?id=1005759',
            "category": 'home-modern-elegant-luxury-table-runners',
            "department": 'home',
        },
        'home-modern-kitchen-canisters-cookie-jars': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-kitchen-canisters-cookie-jars?id=1005750',
            "category": 'home-modern-kitchen-canisters-cookie-jars',
            "department": 'home',
        },
        'home-modern-knife-block-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-knife-block-sets?id=1005822',
            "category": 'home-modern-knife-block-sets',
            "department": 'home',
        },
        'home-modern-linen-bedspreads': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-linen-bedspreads?id=1240769',
            "category": 'home-modern-linen-bedspreads',
            "department": 'home',
        },
        'home-modern-luxury-bath-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-luxury-bath-rugs?id=1005696',
            "category": 'home-modern-luxury-bath-rugs',
            "department": 'home',
        },
        'home-modern-luxury-hand-towels': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-luxury-hand-towels?id=1005700',
            "category": 'home-modern-luxury-hand-towels',
            "department": 'home',
        },
        'home-modern-pendant-lighting-contemporary-ceiling-lights-chandeliers': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-pendant-lighting-contemporary-ceiling-lights-chandeliers?id=1005859',
            "category": 'home-modern-pendant-lighting-contemporary-ceiling-lights-chandeliers',
            "department": 'home',
        },
        'home-modern-picture-frames-luxury-photo-frames': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-picture-frames-luxury-photo-frames?id=1001547',
            "category": 'home-modern-picture-frames-luxury-photo-frames',
            "department": 'home',
        },
        'home-modern-red-white-wine-glasses': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-red-white-wine-glasses?id=1005744',
            "category": 'home-modern-red-white-wine-glasses',
            "department": 'home',
        },
        'home-modern-serving-bowls': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-serving-bowls?id=1005746',
            "category": 'home-modern-serving-bowls',
            "department": 'home',
        },
        'home-modern-teapot-sugar-bowl-serving-accessories': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-teapot-sugar-bowl-serving-accessories?id=1005751',
            "category": 'home-modern-teapot-sugar-bowl-serving-accessories',
            "department": 'home',
        },
        'home-modern-toaster-ovens': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-toaster-ovens?id=1005833',
            "category": 'home-modern-toaster-ovens',
            "department": 'home',
        },
        'home-modern-water-glasses-juice-glass-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-water-glasses-juice-glass-sets?id=1005743',
            "category": 'home-modern-water-glasses-juice-glass-sets',
            "department": 'home',
        },
        'home-modern-whiskey-cocktail-martini-glasses': {
            "url": 'https://www.bloomingdales.com/shop/home/modern-whiskey-cocktail-martini-glasses?id=1005742',
            "category": 'home-modern-whiskey-cocktail-martini-glasses',
            "department": 'home',
        },
        'home-more-for-the-home': {
            "url": 'https://www.bloomingdales.com/shop/home/more-for-the-home?id=1006363',
            "category": 'home-more-for-the-home',
            "department": 'home',
        },
        'home-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/home/new-arrivals?id=1221559',
            "category": 'home-new-arrivals',
            "department": 'home',
        },
        'home-nourison-home': {
            "url": 'https://www.bloomingdales.com/shop/home/nourison-home?id=1235261',
            "category": 'home-nourison-home',
            "department": 'home',
        },
        'home-ottomans': {
            "url": 'https://www.bloomingdales.com/shop/home/ottomans?id=1270295',
            "category": 'home-ottomans',
            "department": 'home',
        },
        'home-outdoor-decor': {
            "url": 'https://www.bloomingdales.com/shop/home/outdoor-decor?id=1005681',
            "category": 'home-outdoor-decor',
            "department": 'home',
        },
        'home-paring-knives': {
            "url": 'https://www.bloomingdales.com/shop/home/paring-knives?id=1005823',
            "category": 'home-paring-knives',
            "department": 'home',
        },
        'home-patio-furniture': {
            "url": 'https://www.bloomingdales.com/shop/home/patio-furniture?id=1055559',
            "category": 'home-patio-furniture',
            "department": 'home',
        },
        'home-pendants': {
            "url": 'https://www.bloomingdales.com/shop/home/pendants?id=1270299',
            "category": 'home-pendants',
            "department": 'home',
        },
        'home-persian-oriental-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/persian-oriental-rugs?id=1025159',
            "category": 'home-persian-oriental-rugs',
            "department": 'home',
        },
        'home-pet-accessories': {
            "url": 'https://www.bloomingdales.com/shop/home/pet-accessories?id=1064759',
            "category": 'home-pet-accessories',
            "department": 'home',
        },
        'home-picture-frames': {
            "url": 'https://www.bloomingdales.com/shop/home/picture-frames?id=16052',
            "category": 'home-picture-frames',
            "department": 'home',
        },
        'home-pillows-comforters': {
            "url": 'https://www.bloomingdales.com/shop/home/pillows-comforters?id=1004679',
            "category": 'home-pillows-comforters',
            "department": 'home',
        },
        'home-place-settings': {
            "url": 'https://www.bloomingdales.com/shop/home/place-settings?id=17211',
            "category": 'home-place-settings',
            "department": 'home',
        },
        'home-plates': {
            "url": 'https://www.bloomingdales.com/shop/home/plates?id=1244295',
            "category": 'home-plates',
            "department": 'home',
        },
        'home-popular-rug-styles': {
            "url": 'https://www.bloomingdales.com/shop/home/popular-rug-styles?id=1232539',
            "category": 'home-popular-rug-styles',
            "department": 'home',
        },
        'home-ralph-lauren': {
            "url": 'https://www.bloomingdales.com/shop/home/ralph-lauren?id=1235262',
            "category": 'home-ralph-lauren',
            "department": 'home',
        },
        'home-red-white-wine-glasses': {
            "url": 'https://www.bloomingdales.com/shop/home/red-white-wine-glasses?id=20742',
            "category": 'home-red-white-wine-glasses',
            "department": 'home',
        },
        'home-registry-manager': {
            "url": 'https://www.bloomingdales.com/shop/home/registry-manager?id=1087764',
            "category": 'home-registry-manager',
            "department": 'home',
        },
        'home-rice-cookers': {
            "url": 'https://www.bloomingdales.com/shop/home/rice-cookers?id=1272599',
            "category": 'home-rice-cookers',
            "department": 'home',
        },
        'home-roasting-pans': {
            "url": 'https://www.bloomingdales.com/shop/home/roasting-pans?id=1005814',
            "category": 'home-roasting-pans',
            "department": 'home',
        },
        'home-round-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/round-rugs?id=1201863',
            "category": 'home-round-rugs',
            "department": 'home',
        },
        'home-rug-clearance': {
            "url": 'https://www.bloomingdales.com/shop/home/rug-clearance?id=1004589',
            "category": 'home-rug-clearance',
            "department": 'home',
        },
        'home-rug-pads': {
            "url": 'https://www.bloomingdales.com/shop/home/rug-pads?id=1005872',
            "category": 'home-rug-pads',
            "department": 'home',
        },
        'home-rugs-under-1000': {
            "url": 'https://www.bloomingdales.com/shop/home/rugs-under-1000?id=1198961',
            "category": 'home-rugs-under-1000',
            "department": 'home',
        },
        'home-runner-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/runner-rugs?id=1025162',
            "category": 'home-runner-rugs',
            "department": 'home',
        },
        'home-safavieh': {
            "url": 'https://www.bloomingdales.com/shop/home/safavieh?id=1235263',
            "category": 'home-safavieh',
            "department": 'home',
        },
        'home-salt-pepper-shakers': {
            "url": 'https://www.bloomingdales.com/shop/home/salt-pepper-shakers?id=1077360',
            "category": 'home-salt-pepper-shakers',
            "department": 'home',
        },
        'home-saucepan-with-lid-saucier': {
            "url": 'https://www.bloomingdales.com/shop/home/saucepan-with-lid-saucier?id=1005815',
            "category": 'home-saucepan-with-lid-saucier',
            "department": 'home',
        },
        'home-saute-pans-with-lid-braiser': {
            "url": 'https://www.bloomingdales.com/shop/home/saute-pans-with-lid-braiser?id=1005816',
            "category": 'home-saute-pans-with-lid-braiser',
            "department": 'home',
        },
        'home-sconces': {
            "url": 'https://www.bloomingdales.com/shop/home/sconces?id=1005864',
            "category": 'home-sconces',
            "department": 'home',
        },
        'home-seder-plates': {
            "url": 'https://www.bloomingdales.com/shop/home/seder-plates?id=1006952',
            "category": 'home-seder-plates',
            "department": 'home',
        },
        'home-serveware': {
            "url": 'https://www.bloomingdales.com/shop/home/serveware?id=1000234',
            "category": 'home-serveware',
            "department": 'home',
        },
        'home-serving-platters': {
            "url": 'https://www.bloomingdales.com/shop/home/serving-platters?id=1006267',
            "category": 'home-serving-platters',
            "department": 'home',
        },
        'home-serving-utensils-spoons-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/serving-utensils-spoons-sets?id=1005752',
            "category": 'home-serving-utensils-spoons-sets',
            "department": 'home',
        },
        'home-shams': {
            "url": 'https://www.bloomingdales.com/shop/home/shams?id=1243598',
            "category": 'home-shams',
            "department": 'home',
        },
        'home-shop-by-size': {
            "url": 'https://www.bloomingdales.com/shop/home/shop-by-size?id=1232538',
            "category": 'home-shop-by-size',
            "department": 'home',
        },
        'home-silver-gold-napkin-rings': {
            "url": 'https://www.bloomingdales.com/shop/home/silver-gold-napkin-rings?id=1005755',
            "category": 'home-silver-gold-napkin-rings',
            "department": 'home',
        },
        'home-skillets-and-frying-pans': {
            "url": 'https://www.bloomingdales.com/shop/home/skillets-and-frying-pans?id=1005817',
            "category": 'home-skillets-and-frying-pans',
            "department": 'home',
        },
        'home-sleep-masks': {
            "url": 'https://www.bloomingdales.com/shop/home/sleep-masks?id=1280696',
            "category": 'home-sleep-masks',
            "department": 'home',
        },
        'home-small-kitchen-appliances': {
            "url": 'https://www.bloomingdales.com/shop/home/small-kitchen-appliances?id=1005832',
            "category": 'home-small-kitchen-appliances',
            "department": 'home',
        },
        'home-small-kitchen-appliances-blenders-electronics': {
            "url": 'https://www.bloomingdales.com/shop/home/small-kitchen-appliances-blenders-electronics?id=1000239',
            "category": 'home-small-kitchen-appliances-blenders-electronics',
            "department": 'home',
        },
        'home-solid-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/solid-rugs?id=1325708',
            "category": 'home-solid-rugs',
            "department": 'home',
        },
        'home-sparrow-wren-apartment-furniture-decor': {
            "url": 'https://www.bloomingdales.com/shop/home/sparrow-wren-apartment-furniture-decor?id=1005146',
            "category": 'home-sparrow-wren-apartment-furniture-decor',
            "department": 'home',
        },
        'home-specialty-cookware': {
            "url": 'https://www.bloomingdales.com/shop/home/specialty-cookware?id=1005818',
            "category": 'home-specialty-cookware',
            "department": 'home',
        },
        'home-spring-break-essentials': {
            "url": 'https://www.bloomingdales.com/shop/home/spring-break-essentials?id=1263453',
            "category": 'home-spring-break-essentials',
            "department": 'home',
        },
        'home-spring-home': {
            "url": 'https://www.bloomingdales.com/shop/home/spring-home?id=1224559',
            "category": 'home-spring-home',
            "department": 'home',
        },
        'home-stand-mixers': {
            "url": 'https://www.bloomingdales.com/shop/home/stand-mixers?id=1272597',
            "category": 'home-stand-mixers',
            "department": 'home',
        },
        'home-steak-knife-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/steak-knife-sets?id=1005825',
            "category": 'home-steak-knife-sets',
            "department": 'home',
        },
        'home-steamers': {
            "url": 'https://www.bloomingdales.com/shop/home/steamers?id=1272604',
            "category": 'home-steamers',
            "department": 'home',
        },
        'home-sugar-bowls-creamers': {
            "url": 'https://www.bloomingdales.com/shop/home/sugar-bowls-creamers?id=1272415',
            "category": 'home-sugar-bowls-creamers',
            "department": 'home',
        },
        'home-summer-bedding-shop': {
            "url": 'https://www.bloomingdales.com/shop/home/summer-bedding-shop?id=1231363',
            "category": 'home-summer-bedding-shop',
            "department": 'home',
        },
        'home-summer-scents': {
            "url": 'https://www.bloomingdales.com/shop/home/summer-scents?id=1225614',
            "category": 'home-summer-scents',
            "department": 'home',
        },
        'home-super-automatic-espresso-machines': {
            "url": 'https://www.bloomingdales.com/shop/home/super-automatic-espresso-machines?id=1292396',
            "category": 'home-super-automatic-espresso-machines',
            "department": 'home',
        },
        'home-surya': {
            "url": 'https://www.bloomingdales.com/shop/home/surya?id=1235264',
            "category": 'home-surya',
            "department": 'home',
        },
        'home-table-linens': {
            "url": 'https://www.bloomingdales.com/shop/home/table-linens?id=1063259',
            "category": 'home-table-linens',
            "department": 'home',
        },
        'home-teapot-cream-sugar-set': {
            "url": 'https://www.bloomingdales.com/shop/home/teapot-cream-sugar-set?id=1077359',
            "category": 'home-teapot-cream-sugar-set',
            "department": 'home',
        },
        'home-towel-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/towel-sets?id=1005694',
            "category": 'home-towel-sets',
            "department": 'home',
        },
        'home-towels': {
            "url": 'https://www.bloomingdales.com/shop/home/towels?id=1005695',
            "category": 'home-towels',
            "department": 'home',
        },
        'home-traditional-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/traditional-rugs?id=1325704',
            "category": 'home-traditional-rugs',
            "department": 'home',
        },
        'home-travel-backpacks': {
            "url": 'https://www.bloomingdales.com/shop/home/travel-backpacks?id=1005638',
            "category": 'home-travel-backpacks',
            "department": 'home',
        },
        'home-travel-bags-briefcases': {
            "url": 'https://www.bloomingdales.com/shop/home/travel-bags-briefcases?id=1005590',
            "category": 'home-travel-bags-briefcases',
            "department": 'home',
        },
        'home-travel-briefcases': {
            "url": 'https://www.bloomingdales.com/shop/home/travel-briefcases?id=1005639',
            "category": 'home-travel-briefcases',
            "department": 'home',
        },
        'home-travel-essentials': {
            "url": 'https://www.bloomingdales.com/shop/home/travel-essentials?id=1005642',
            "category": 'home-travel-essentials',
            "department": 'home',
        },
        'home-travel-tote-bags': {
            "url": 'https://www.bloomingdales.com/shop/home/travel-tote-bags?id=1005641',
            "category": 'home-travel-tote-bags',
            "department": 'home',
        },
        'home-trays': {
            "url": 'https://www.bloomingdales.com/shop/home/trays?id=1005753',
            "category": 'home-trays',
            "department": 'home',
        },
        'home-trending-now-home': {
            "url": 'https://www.bloomingdales.com/shop/home/trending-now-home?id=1002556',
            "category": 'home-trending-now-home',
            "department": 'home',
        },
        'home-trivets': {
            "url": 'https://www.bloomingdales.com/shop/home/trivets?id=18960',
            "category": 'home-trivets',
            "department": 'home',
        },
        'home-vacuum-cleaning-robots': {
            "url": 'https://www.bloomingdales.com/shop/home/vacuum-cleaning-robots?id=1001470',
            "category": 'home-vacuum-cleaning-robots',
            "department": 'home',
        },
        'home-votive-candle-holders': {
            "url": 'https://www.bloomingdales.com/shop/home/votive-candle-holders?id=1005853',
            "category": 'home-votive-candle-holders',
            "department": 'home',
        },
        'home-votives': {
            "url": 'https://www.bloomingdales.com/shop/home/votives?id=1272602',
            "category": 'home-votives',
            "department": 'home',
        },
        'home-waffle-makers': {
            "url": 'https://www.bloomingdales.com/shop/home/waffle-makers?id=1006946',
            "category": 'home-waffle-makers',
            "department": 'home',
        },
        'home-washable-rugs': {
            "url": 'https://www.bloomingdales.com/shop/home/washable-rugs?id=1250406',
            "category": 'home-washable-rugs',
            "department": 'home',
        },
        'home-washcloths': {
            "url": 'https://www.bloomingdales.com/shop/home/washcloths?id=1006962',
            "category": 'home-washcloths',
            "department": 'home',
        },
        'home-weekender-duffel-bags': {
            "url": 'https://www.bloomingdales.com/shop/home/weekender-duffel-bags?id=1288401',
            "category": 'home-weekender-duffel-bags',
            "department": 'home',
        },
        'home-window-curtains': {
            "url": 'https://www.bloomingdales.com/shop/home/window-curtains?id=1144116',
            "category": 'home-window-curtains',
            "department": 'home',
        },
        'home-wine-can-bottle-opener-corkscrews': {
            "url": 'https://www.bloomingdales.com/shop/home/wine-can-bottle-opener-corkscrews?id=1005834',
            "category": 'home-wine-can-bottle-opener-corkscrews',
            "department": 'home',
        },
        'home-wine-chillers': {
            "url": 'https://www.bloomingdales.com/shop/home/wine-chillers?id=1272404',
            "category": 'home-wine-chillers',
            "department": 'home',
        },
        'home-wine-glass-sets': {
            "url": 'https://www.bloomingdales.com/shop/home/wine-glass-sets?id=20743',
            "category": 'home-wine-glass-sets',
            "department": 'home',
        },
        'home-woks': {
            "url": 'https://www.bloomingdales.com/shop/home/woks?id=1272495',
            "category": 'home-woks',
            "department": 'home',
        },
    },
    'home-accents-accessories': {
        'home-accents-accessories': {
            "url": 'https://www.bloomingdales.com/shop/home-accents-accessories?id=1151570',
            "category": 'home-accents-accessories',
            "department": 'home-accents-accessories',
        },
        'home-accents-accessories-collectibles': {
            "url": 'https://www.bloomingdales.com/shop/home-accents-accessories/collectibles?id=1151572',
            "category": 'home-accents-accessories-collectibles',
            "department": 'home-accents-accessories',
        },
    },
    'home-care': {
        'home-care': {
            "url": 'https://www.bloomingdales.com/shop/home-care?id=1236264',
            "category": 'home-care',
            "department": 'home-care',
        },
    },
    'home-cozy-treatments': {
        'home-cozy-treatments': {
            "url": 'https://www.bloomingdales.com/shop/home-cozy-treatments?id=1166781',
            "category": 'home-cozy-treatments',
            "department": 'home-cozy-treatments',
        },
    },
    'home-decor': {
        'home-decor': {
            "url": 'https://www.bloomingdales.com/shop/home-decor?id=1036660',
            "category": 'home-decor',
            "department": 'home-decor',
        },
    },
    'home-test-category': {
        'home-test-category': {
            "url": 'https://www.bloomingdales.com/shop/home-test-category?id=1047659',
            "category": 'home-test-category',
            "department": 'home-test-category',
        },
    },
    'homepage-do-not-touch': {
        'homepage-do-not-touch': {
            "url": 'https://www.bloomingdales.com/shop/homepage-do-not-touch?id=1049359',
            "category": 'homepage-do-not-touch',
            "department": 'homepage-do-not-touch',
        },
    },
    'hoop': {
        'hoop': {
            "url": 'https://www.bloomingdales.com/shop/hoop?id=20551',
            "category": 'hoop',
            "department": 'hoop',
        },
    },
    'hourglass': {
        'hourglass': {
            "url": 'https://www.bloomingdales.com/shop/hourglass?id=1278835',
            "category": 'hourglass',
            "department": 'hourglass',
        },
        'hourglass-hourglass-eye-makeup': {
            "url": 'https://www.bloomingdales.com/shop/hourglass/hourglass-eye-makeup?id=1302713',
            "category": 'hourglass-hourglass-eye-makeup',
            "department": 'hourglass',
        },
        'hourglass-hourglass-face-makeup': {
            "url": 'https://www.bloomingdales.com/shop/hourglass/hourglass-face-makeup?id=1302714',
            "category": 'hourglass-hourglass-face-makeup',
            "department": 'hourglass',
        },
        'hourglass-hourglass-lips': {
            "url": 'https://www.bloomingdales.com/shop/hourglass/hourglass-lips?id=1302715',
            "category": 'hourglass-hourglass-lips',
            "department": 'hourglass',
        },
        'hourglass-hourglass-tools-brushes': {
            "url": 'https://www.bloomingdales.com/shop/hourglass/hourglass-tools-brushes?id=1302716',
            "category": 'hourglass-hourglass-tools-brushes',
            "department": 'hourglass',
        },
    },
    'hudson-park-collection': {
        'hudson-park-collection': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection?id=1004072',
            "category": 'hudson-park-collection',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-bath': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-bath?id=1286097',
            "category": 'hudson-park-collection-hudson-park-collection-bath',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-bedding': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-bedding?id=1286095',
            "category": 'hudson-park-collection-hudson-park-collection-bedding',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-comforters-pillows': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-comforters-pillows?id=1286096',
            "category": 'hudson-park-collection-hudson-park-collection-comforters-pillows',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-dinnerware': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-dinnerware?id=1286098',
            "category": 'hudson-park-collection-hudson-park-collection-dinnerware',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-furniture': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-furniture?id=1286099',
            "category": 'hudson-park-collection-hudson-park-collection-furniture',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-mattresses': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-mattresses?id=1286100',
            "category": 'hudson-park-collection-hudson-park-collection-mattresses',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-sheets': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-sheets?id=1307433',
            "category": 'hudson-park-collection-hudson-park-collection-sheets',
            "department": 'hudson-park-collection',
        },
        'hudson-park-collection-hudson-park-collection-throws-pillows': {
            "url": 'https://www.bloomingdales.com/shop/hudson-park-collection/hudson-park-collection-throws-pillows?id=1286101',
            "category": 'hudson-park-collection-hudson-park-collection-throws-pillows',
            "department": 'hudson-park-collection',
        },
    },
    'hugo-boss': {
        'hugo-boss': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss?id=1003921',
            "category": 'hugo-boss',
            "department": 'hugo-boss',
        },
        'hugo-boss-mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss/mens-accessories?id=1018463',
            "category": 'hugo-boss-mens-accessories',
            "department": 'hugo-boss',
        },
        'hugo-boss-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss/mens-clothing?id=1018461',
            "category": 'hugo-boss-mens-clothing',
            "department": 'hugo-boss',
        },
        'hugo-boss-mens-clothing-accessories-cologne': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss/mens-clothing-accessories-cologne?id=1003925',
            "category": 'hugo-boss-mens-clothing-accessories-cologne',
            "department": 'hugo-boss',
        },
        'hugo-boss-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss/mens-shoes?id=1018462',
            "category": 'hugo-boss-mens-shoes',
            "department": 'hugo-boss',
        },
        'hugo-boss-suits': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss/suits?id=1304395',
            "category": 'hugo-boss-suits',
            "department": 'hugo-boss',
        },
        'hugo-boss-the-carousel-game-day-with-boss': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss/the-carousel-game-day-with-boss?id=1319602',
            "category": 'hugo-boss-the-carousel-game-day-with-boss',
            "department": 'hugo-boss',
        },
        'hugo-boss-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/hugo-boss/womens-clothing?id=1003922',
            "category": 'hugo-boss-womens-clothing',
            "department": 'hugo-boss',
        },
    },
    'hunter': {
        'hunter': {
            "url": 'https://www.bloomingdales.com/shop/hunter?id=1005453',
            "category": 'hunter',
            "department": 'hunter',
        },
    },
    'infiniment-coty-paris': {
        'infiniment-coty-paris': {
            "url": 'https://www.bloomingdales.com/shop/infiniment-coty-paris?id=1262226',
            "category": 'infiniment-coty-paris',
            "department": 'infiniment-coty-paris',
        },
    },
    'initio-parfums-prives': {
        'initio-parfums-prives': {
            "url": 'https://www.bloomingdales.com/shop/initio-parfums-prives?id=1336601',
            "category": 'initio-parfums-prives',
            "department": 'initio-parfums-prives',
        },
    },
    'ippolita': {
        'ippolita': {
            "url": 'https://www.bloomingdales.com/shop/ippolita?id=1003868',
            "category": 'ippolita',
            "department": 'ippolita',
        },
        'ippolita-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/ippolita/bracelets?id=1005860',
            "category": 'ippolita-bracelets',
            "department": 'ippolita',
        },
        'ippolita-earrings': {
            "url": 'https://www.bloomingdales.com/shop/ippolita/earrings?id=1005863',
            "category": 'ippolita-earrings',
            "department": 'ippolita',
        },
        'ippolita-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/ippolita/necklaces?id=1005866',
            "category": 'ippolita-necklaces',
            "department": 'ippolita',
        },
        'ippolita-rings': {
            "url": 'https://www.bloomingdales.com/shop/ippolita/rings?id=1005869',
            "category": 'ippolita-rings',
            "department": 'ippolita',
        },
    },
    'isaia': {
        'isaia': {
            "url": 'https://www.bloomingdales.com/shop/isaia?id=1333697',
            "category": 'isaia',
            "department": 'isaia',
        },
    },
    'james-perse': {
        'james-perse': {
            "url": 'https://www.bloomingdales.com/shop/james-perse?id=1313298',
            "category": 'james-perse',
            "department": 'james-perse',
        },
        'james-perse-mens': {
            "url": 'https://www.bloomingdales.com/shop/james-perse/mens?id=1313299',
            "category": 'james-perse-mens',
            "department": 'james-perse',
        },
        'james-perse-womens': {
            "url": 'https://www.bloomingdales.com/shop/james-perse/womens?id=1313300',
            "category": 'james-perse-womens',
            "department": 'james-perse',
        },
    },
    'jars': {
        'jars': {
            "url": 'https://www.bloomingdales.com/shop/jars?id=1243695',
            "category": 'jars',
            "department": 'jars',
        },
    },
    'jean-paul-gaultier': {
        'jean-paul-gaultier': {
            "url": 'https://www.bloomingdales.com/shop/jean-paul-gaultier?id=1286905',
            "category": 'jean-paul-gaultier',
            "department": 'jean-paul-gaultier',
        },
        'jean-paul-gaultier-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/jean-paul-gaultier/best-sellers?id=1288796',
            "category": 'jean-paul-gaultier-best-sellers',
            "department": 'jean-paul-gaultier',
        },
        'jean-paul-gaultier-le-beau': {
            "url": 'https://www.bloomingdales.com/shop/jean-paul-gaultier/le-beau?id=1286907',
            "category": 'jean-paul-gaultier-le-beau',
            "department": 'jean-paul-gaultier',
        },
        'jean-paul-gaultier-le-male': {
            "url": 'https://www.bloomingdales.com/shop/jean-paul-gaultier/le-male?id=1286906',
            "category": 'jean-paul-gaultier-le-male',
            "department": 'jean-paul-gaultier',
        },
        'jean-paul-gaultier-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/jean-paul-gaultier/shop-all?id=1286908',
            "category": 'jean-paul-gaultier-shop-all',
            "department": 'jean-paul-gaultier',
        },
    },
    'jellycat': {
        'jellycat': {
            "url": 'https://www.bloomingdales.com/shop/jellycat?id=1312895',
            "category": 'jellycat',
            "department": 'jellycat',
        },
    },
    'jewel-tones': {
        'jewel-tones': {
            "url": 'https://www.bloomingdales.com/shop/jewel-tones?id=1003149',
            "category": 'jewel-tones',
            "department": 'jewel-tones',
        },
    },
    'jewelry-accessories': {
        'jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories?id=1319127',
            "category": 'jewelry-accessories',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-all-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/all-jewelry-accessories?id=1003593',
            "category": 'jewelry-accessories-all-jewelry-accessories',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-apple-watch-bands': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/apple-watch-bands?id=1322244',
            "category": 'jewelry-accessories-apple-watch-bands',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-band-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/band-rings?id=1005911',
            "category": 'jewelry-accessories-band-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-bandanas-square-scarves': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/bandanas-square-scarves?id=1007767',
            "category": 'jewelry-accessories-bandanas-square-scarves',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-bangle-cuff-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/bangle-cuff-bracelets?id=1005800',
            "category": 'jewelry-accessories-bangle-cuff-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-beaded-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/beaded-bracelets?id=1005801',
            "category": 'jewelry-accessories-beaded-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/best-sellers?id=1044359',
            "category": 'jewelry-accessories-best-sellers',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-birthstones': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/birthstones?id=1291795',
            "category": 'jewelry-accessories-birthstones',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-blanket-oversized-scarves': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/blanket-oversized-scarves?id=1007768',
            "category": 'jewelry-accessories-blanket-oversized-scarves',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/bracelets?id=1195875',
            "category": 'jewelry-accessories-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-chain-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/chain-bracelets?id=1005802',
            "category": 'jewelry-accessories-chain-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-chain-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/chain-necklaces?id=1005903',
            "category": 'jewelry-accessories-chain-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-charm-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/charm-bracelets?id=1322215',
            "category": 'jewelry-accessories-charm-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-charms-pendants': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/charms-pendants?id=1275600',
            "category": 'jewelry-accessories-charms-pendants',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-clip-on-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/clip-on-earrings?id=1005667',
            "category": 'jewelry-accessories-clip-on-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-cocktail-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/cocktail-rings?id=1005913',
            "category": 'jewelry-accessories-cocktail-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-designer-bangle-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/designer-bangle-bracelets?id=1005925',
            "category": 'jewelry-accessories-designer-bangle-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-designer-beaded-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/designer-beaded-bracelets?id=1005926',
            "category": 'jewelry-accessories-designer-beaded-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-designer-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/designer-bracelets?id=8701',
            "category": 'jewelry-accessories-designer-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-designer-stud-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/designer-stud-earrings?id=1005671',
            "category": 'jewelry-accessories-designer-stud-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-designer-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/designer-sunglasses?id=4520',
            "category": 'jewelry-accessories-designer-sunglasses',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-diamond-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/diamond-bracelets?id=1322211',
            "category": 'jewelry-accessories-diamond-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-diamond-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/diamond-earrings?id=1322223',
            "category": 'jewelry-accessories-diamond-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-diamond-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/diamond-necklaces?id=1322231',
            "category": 'jewelry-accessories-diamond-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-diamond-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/diamond-rings?id=1322238',
            "category": 'jewelry-accessories-diamond-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-diamonds': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/diamonds?id=1308613',
            "category": 'jewelry-accessories-diamonds',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-drop-chandelier-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/drop-chandelier-earrings?id=1005668',
            "category": 'jewelry-accessories-drop-chandelier-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-drop-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/drop-earrings?id=1005764',
            "category": 'jewelry-accessories-drop-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-ear-cuffs': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/ear-cuffs?id=1005670',
            "category": 'jewelry-accessories-ear-cuffs',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/earrings?id=1195874',
            "category": 'jewelry-accessories-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-engagement-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/engagement-rings?id=1322239',
            "category": 'jewelry-accessories-engagement-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-face-masks': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/face-masks?id=1096359',
            "category": 'jewelry-accessories-face-masks',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-fashion-cocktail-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/fashion-cocktail-rings?id=1005662',
            "category": 'jewelry-accessories-fashion-cocktail-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-fashion-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/fashion-jewelry?id=1195559',
            "category": 'jewelry-accessories-fashion-jewelry',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-fine-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/fine-jewelry?id=1005354',
            "category": 'jewelry-accessories-fine-jewelry',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-fine-jewelry-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/fine-jewelry-bracelets?id=17804',
            "category": 'jewelry-accessories-fine-jewelry-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-fine-jewelry-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/fine-jewelry-earrings?id=20548',
            "category": 'jewelry-accessories-fine-jewelry-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-fine-jewelry-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/fine-jewelry-necklaces?id=17805',
            "category": 'jewelry-accessories-fine-jewelry-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-fine-jewelry-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/fine-jewelry-rings?id=17806',
            "category": 'jewelry-accessories-fine-jewelry-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-gloves': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/gloves?id=1005371',
            "category": 'jewelry-accessories-gloves',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-gold-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/gold-bracelets?id=1322212',
            "category": 'jewelry-accessories-gold-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-gold-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/gold-earrings?id=1322228',
            "category": 'jewelry-accessories-gold-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-gold-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/gold-jewelry?id=1166759',
            "category": 'jewelry-accessories-gold-jewelry',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-gold-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/gold-necklaces?id=1322233',
            "category": 'jewelry-accessories-gold-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-gold-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/gold-rings?id=1322241',
            "category": 'jewelry-accessories-gold-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-hair-accessories': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/hair-accessories?id=1070659',
            "category": 'jewelry-accessories-hair-accessories',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-hats': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/hats?id=1005370',
            "category": 'jewelry-accessories-hats',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-hoop-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/hoop-earrings?id=1005669',
            "category": 'jewelry-accessories-hoop-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-huggie-hoop-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/huggie-hoop-earrings?id=1322230',
            "category": 'jewelry-accessories-huggie-hoop-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-infinity-scarves': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/infinity-scarves?id=1007766',
            "category": 'jewelry-accessories-infinity-scarves',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-iphone-cases-tech-accessories': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/iphone-cases-tech-accessories?id=21485',
            "category": 'jewelry-accessories-iphone-cases-tech-accessories',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/jewelry?id=3619',
            "category": 'jewelry-accessories-jewelry',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-jewelry-boxes-ring-holders-and-watch-holders': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/jewelry-boxes-ring-holders-and-watch-holders?id=1005858',
            "category": 'jewelry-accessories-jewelry-boxes-ring-holders-and-watch-holders',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-jewelry-finds-under-200': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/jewelry-finds-under-200?id=1152459',
            "category": 'jewelry-accessories-jewelry-finds-under-200',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-jewelry-under-100-gifts': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/jewelry-under-100-gifts?id=1178359',
            "category": 'jewelry-accessories-jewelry-under-100-gifts',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-lab-grown-diamonds': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/lab-grown-diamonds?id=1233983',
            "category": 'jewelry-accessories-lab-grown-diamonds',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-lariat': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/lariat?id=1005905',
            "category": 'jewelry-accessories-lariat',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-link-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/link-bracelets?id=1006248',
            "category": 'jewelry-accessories-link-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-luxury-brand-jewelry-gifts': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/luxury-brand-jewelry-gifts?id=1176874',
            "category": 'jewelry-accessories-luxury-brand-jewelry-gifts',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-multi-strand-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/multi-strand-necklaces?id=1005906',
            "category": 'jewelry-accessories-multi-strand-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/necklaces?id=1195873',
            "category": 'jewelry-accessories-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-pearl-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/pearl-earrings?id=1322227',
            "category": 'jewelry-accessories-pearl-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-pearl-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/pearl-necklaces?id=1322232',
            "category": 'jewelry-accessories-pearl-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-pendant-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/pendant-necklaces?id=1005907',
            "category": 'jewelry-accessories-pendant-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-personalized-meaningful-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/personalized-meaningful-jewelry?id=1092860',
            "category": 'jewelry-accessories-personalized-meaningful-jewelry',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-pre-owned-watches': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/pre-owned-watches?id=1211965',
            "category": 'jewelry-accessories-pre-owned-watches',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-premium-designer-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/premium-designer-sunglasses?id=1003486',
            "category": 'jewelry-accessories-premium-designer-sunglasses',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-reading-glasses': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/reading-glasses?id=1006684',
            "category": 'jewelry-accessories-reading-glasses',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-rectangle': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/rectangle?id=1007765',
            "category": 'jewelry-accessories-rectangle',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/rings?id=1195876',
            "category": 'jewelry-accessories-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-rose-gold-bracelet': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/rose-gold-bracelet?id=1079863',
            "category": 'jewelry-accessories-rose-gold-bracelet',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-scarves-hats-gloves': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/scarves-hats-gloves?id=21311',
            "category": 'jewelry-accessories-scarves-hats-gloves',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-shawls-evening-wraps': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/shawls-evening-wraps?id=1007770',
            "category": 'jewelry-accessories-shawls-evening-wraps',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-signet-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/signet-rings?id=1322243',
            "category": 'jewelry-accessories-signet-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-silver-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/silver-bracelets?id=1322213',
            "category": 'jewelry-accessories-silver-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-silver-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/silver-earrings?id=1322229',
            "category": 'jewelry-accessories-silver-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-silver-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/silver-necklaces?id=1322237',
            "category": 'jewelry-accessories-silver-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-silver-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/silver-rings?id=1322242',
            "category": 'jewelry-accessories-silver-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-smart-glasses': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/smart-glasses?id=1306122',
            "category": 'jewelry-accessories-smart-glasses',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-sterling-silver-bracelet': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/sterling-silver-bracelet?id=1079864',
            "category": 'jewelry-accessories-sterling-silver-bracelet',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-stud-earrings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/stud-earrings?id=1005767',
            "category": 'jewelry-accessories-stud-earrings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/sunglasses?id=3621',
            "category": 'jewelry-accessories-sunglasses',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-tennis-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/tennis-bracelets?id=1005672',
            "category": 'jewelry-accessories-tennis-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-trending-now-party-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/trending-now-party-jewelry?id=1132066',
            "category": 'jewelry-accessories-trending-now-party-jewelry',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-trendy-chain-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/trendy-chain-jewelry?id=1080459',
            "category": 'jewelry-accessories-trendy-chain-jewelry',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-umbrellas': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/umbrellas?id=20082',
            "category": 'jewelry-accessories-umbrellas',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-watches': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/watches?id=19469',
            "category": 'jewelry-accessories-watches',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-white-gold-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/white-gold-bracelets?id=1079862',
            "category": 'jewelry-accessories-white-gold-bracelets',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-winter-accessories': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/winter-accessories?id=1292495',
            "category": 'jewelry-accessories-winter-accessories',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-band-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-band-rings?id=1005661',
            "category": 'jewelry-accessories-womens-band-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-baseball-caps': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-baseball-caps?id=1031559',
            "category": 'jewelry-accessories-womens-baseball-caps',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-beanies': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-beanies?id=1007859',
            "category": 'jewelry-accessories-womens-beanies',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-capes-ponchos': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-capes-ponchos?id=1007769',
            "category": 'jewelry-accessories-womens-capes-ponchos',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-chain-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-chain-necklaces?id=1005656',
            "category": 'jewelry-accessories-womens-chain-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-chokers-collar-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-chokers-collar-necklaces?id=1005657',
            "category": 'jewelry-accessories-womens-chokers-collar-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-cloche-hats-and-bucket-hats': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-cloche-hats-and-bucket-hats?id=1007864',
            "category": 'jewelry-accessories-womens-cloche-hats-and-bucket-hats',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-fashion-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-fashion-necklaces?id=3629',
            "category": 'jewelry-accessories-womens-fashion-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-fashion-statement-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-fashion-statement-necklaces?id=1005660',
            "category": 'jewelry-accessories-womens-fashion-statement-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-floppy-hats': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-floppy-hats?id=1007861',
            "category": 'jewelry-accessories-womens-floppy-hats',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-luxury-watches': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-luxury-watches?id=22108',
            "category": 'jewelry-accessories-womens-luxury-watches',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-pendant-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-pendant-necklaces?id=1005659',
            "category": 'jewelry-accessories-womens-pendant-necklaces',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-rings?id=3630',
            "category": 'jewelry-accessories-womens-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-scarves-wraps': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-scarves-wraps?id=1005369',
            "category": 'jewelry-accessories-womens-scarves-wraps',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-smart-watches': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-smart-watches?id=1006065',
            "category": 'jewelry-accessories-womens-smart-watches',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-stackable-rings': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-stackable-rings?id=1005663',
            "category": 'jewelry-accessories-womens-stackable-rings',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-sun-hats': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-sun-hats?id=1007860',
            "category": 'jewelry-accessories-womens-sun-hats',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-swiss-watches': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-swiss-watches?id=1006066',
            "category": 'jewelry-accessories-womens-swiss-watches',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-womens-watches': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/womens-watches?id=1230061',
            "category": 'jewelry-accessories-womens-watches',
            "department": 'jewelry-accessories',
        },
        'jewelry-accessories-yellow-gold-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories/yellow-gold-bracelets?id=1079860',
            "category": 'jewelry-accessories-yellow-gold-bracelets',
            "department": 'jewelry-accessories',
        },
    },
    'jewelry-accessories-clearance': {
        'jewelry-accessories-clearance': {
            "url": 'https://www.bloomingdales.com/shop/jewelry-accessories-clearance?id=1122259',
            "category": 'jewelry-accessories-clearance',
            "department": 'jewelry-accessories-clearance',
        },
    },
    'jil-sander': {
        'jil-sander': {
            "url": 'https://www.bloomingdales.com/shop/jil-sander?id=1282995',
            "category": 'jil-sander',
            "department": 'jil-sander',
        },
        'jil-sander-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/jil-sander/fragrance?id=1284112',
            "category": 'jil-sander-fragrance',
            "department": 'jil-sander',
        },
        'jil-sander-mens': {
            "url": 'https://www.bloomingdales.com/shop/jil-sander/mens?id=1284111',
            "category": 'jil-sander-mens',
            "department": 'jil-sander',
        },
        'jil-sander-shoes': {
            "url": 'https://www.bloomingdales.com/shop/jil-sander/shoes?id=1301654',
            "category": 'jil-sander-shoes',
            "department": 'jil-sander',
        },
        'jil-sander-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/jil-sander/womens-clothing?id=1301696',
            "category": 'jil-sander-womens-clothing',
            "department": 'jil-sander',
        },
    },
    'jimmy-choo': {
        'jimmy-choo': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo?id=1061959',
            "category": 'jimmy-choo',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-boots': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/boots?id=1249596',
            "category": 'jimmy-choo-boots',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-bridal': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/bridal?id=1164761',
            "category": 'jimmy-choo-bridal',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-flats': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/flats?id=1249597',
            "category": 'jimmy-choo-flats',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/fragrance?id=1164763',
            "category": 'jimmy-choo-fragrance',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-handbags': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/handbags?id=1164759',
            "category": 'jimmy-choo-handbags',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-heels': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/heels?id=1249595',
            "category": 'jimmy-choo-heels',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-new-arrivals-autumn-winter-2024-collection': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/new-arrivals-autumn-winter-2024-collection?id=1239761',
            "category": 'jimmy-choo-new-arrivals-autumn-winter-2024-collection',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-sale': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/sale?id=1249599',
            "category": 'jimmy-choo-sale',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-shoes': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/shoes?id=1164760',
            "category": 'jimmy-choo-shoes',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/sneakers?id=1249598',
            "category": 'jimmy-choo-sneakers',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-the-icons': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/the-icons?id=1200259',
            "category": 'jimmy-choo-the-icons',
            "department": 'jimmy-choo',
        },
        'jimmy-choo-wardrobe-edit': {
            "url": 'https://www.bloomingdales.com/shop/jimmy-choo/wardrobe-edit?id=1241659',
            "category": 'jimmy-choo-wardrobe-edit',
            "department": 'jimmy-choo',
        },
    },
    'jo-malone-bath-body': {
        'jo-malone-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-bath-body?id=1269577',
            "category": 'jo-malone-bath-body',
            "department": 'jo-malone-bath-body',
        },
    },
    'jo-malone-candles-diffusers': {
        'jo-malone-candles-diffusers': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-candles-diffusers?id=1269581',
            "category": 'jo-malone-candles-diffusers',
            "department": 'jo-malone-candles-diffusers',
        },
    },
    'jo-malone-london': {
        'jo-malone-london': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london?id=17973',
            "category": 'jo-malone-london',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-citrus-fruity': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/citrus-fruity?id=1331103',
            "category": 'jo-malone-london-citrus-fruity',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-floral': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/floral?id=1331102',
            "category": 'jo-malone-london-floral',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-fresh': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/fresh?id=1331104',
            "category": 'jo-malone-london-fresh',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-jo-malone-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/jo-malone-bath-body?id=17976',
            "category": 'jo-malone-london-jo-malone-bath-body',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-jo-malone-candles-diffusers': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/jo-malone-candles-diffusers?id=17985',
            "category": 'jo-malone-london-jo-malone-candles-diffusers',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-jo-malone-london-cologne': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/jo-malone-london-cologne?id=17975',
            "category": 'jo-malone-london-jo-malone-london-cologne',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-jo-malone-london-english-pear-and-freesia': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/jo-malone-london-english-pear-and-freesia?id=1252350',
            "category": 'jo-malone-london-jo-malone-london-english-pear-and-freesia',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-jo-malone-london-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/jo-malone-london-gift-sets?id=17995',
            "category": 'jo-malone-london-jo-malone-london-gift-sets',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-jo-malone-london-perfume': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/jo-malone-london-perfume?id=1252348',
            "category": 'jo-malone-london-jo-malone-london-perfume',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-jo-malone-london-wood-sage-and-sea-salt': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/jo-malone-london-wood-sage-and-sea-salt?id=1252349',
            "category": 'jo-malone-london-jo-malone-london-wood-sage-and-sea-salt',
            "department": 'jo-malone-london',
        },
        'jo-malone-london-woody': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london/woody?id=1331101',
            "category": 'jo-malone-london-woody',
            "department": 'jo-malone-london',
        },
    },
    'jo-malone-london-candles': {
        'jo-malone-london-candles': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london-candles?id=1229088',
            "category": 'jo-malone-london-candles',
            "department": 'jo-malone-london-candles',
        },
    },
    'jo-malone-london-cologne': {
        'jo-malone-london-cologne': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london-cologne?id=1269576',
            "category": 'jo-malone-london-cologne',
            "department": 'jo-malone-london-cologne',
        },
    },
    'jo-malone-london-english-pear-and-freesia': {
        'jo-malone-london-english-pear-and-freesia': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london-english-pear-and-freesia?id=1269592',
            "category": 'jo-malone-london-english-pear-and-freesia',
            "department": 'jo-malone-london-english-pear-and-freesia',
        },
    },
    'jo-malone-london-gift-sets': {
        'jo-malone-london-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london-gift-sets?id=1269586',
            "category": 'jo-malone-london-gift-sets',
            "department": 'jo-malone-london-gift-sets',
        },
    },
    'jo-malone-london-perfume': {
        'jo-malone-london-perfume': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london-perfume?id=1269591',
            "category": 'jo-malone-london-perfume',
            "department": 'jo-malone-london-perfume',
        },
    },
    'jo-malone-london-wood-sage-and-sea-salt': {
        'jo-malone-london-wood-sage-and-sea-salt': {
            "url": 'https://www.bloomingdales.com/shop/jo-malone-london-wood-sage-and-sea-salt?id=1269590',
            "category": 'jo-malone-london-wood-sage-and-sea-salt',
            "department": 'jo-malone-london-wood-sage-and-sea-salt',
        },
    },
    'joes-jeans': {
        'joes-jeans': {
            "url": 'https://www.bloomingdales.com/shop/joes-jeans?id=1262397',
            "category": 'joes-jeans',
            "department": 'joes-jeans',
        },
        'joes-jeans-mens': {
            "url": 'https://www.bloomingdales.com/shop/joes-jeans/mens?id=1262398',
            "category": 'joes-jeans-mens',
            "department": 'joes-jeans',
        },
        'joes-jeans-mens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/joes-jeans/mens-jeans?id=1262402',
            "category": 'joes-jeans-mens-jeans',
            "department": 'joes-jeans',
        },
        'joes-jeans-sale': {
            "url": 'https://www.bloomingdales.com/shop/joes-jeans/sale?id=1262999',
            "category": 'joes-jeans-sale',
            "department": 'joes-jeans',
        },
        'joes-jeans-womens': {
            "url": 'https://www.bloomingdales.com/shop/joes-jeans/womens?id=1262399',
            "category": 'joes-jeans-womens',
            "department": 'joes-jeans',
        },
        'joes-jeans-womens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/joes-jeans/womens-jeans?id=1262403',
            "category": 'joes-jeans-womens-jeans',
            "department": 'joes-jeans',
        },
    },
    'john-hardy': {
        'john-hardy': {
            "url": 'https://www.bloomingdales.com/shop/john-hardy?id=1331696',
            "category": 'john-hardy',
            "department": 'john-hardy',
        },
        'john-hardy-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/john-hardy/bracelets?id=1331697',
            "category": 'john-hardy-bracelets',
            "department": 'john-hardy',
        },
        'john-hardy-earrings': {
            "url": 'https://www.bloomingdales.com/shop/john-hardy/earrings?id=1331700',
            "category": 'john-hardy-earrings',
            "department": 'john-hardy',
        },
        'john-hardy-mens-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/john-hardy/mens-jewelry?id=1331701',
            "category": 'john-hardy-mens-jewelry',
            "department": 'john-hardy',
        },
        'john-hardy-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/john-hardy/necklaces?id=1331698',
            "category": 'john-hardy-necklaces',
            "department": 'john-hardy',
        },
        'john-hardy-rings': {
            "url": 'https://www.bloomingdales.com/shop/john-hardy/rings?id=1331699',
            "category": 'john-hardy-rings',
            "department": 'john-hardy',
        },
    },
    'john-varvatos': {
        'john-varvatos': {
            "url": 'https://www.bloomingdales.com/shop/john-varvatos?id=1003892',
            "category": 'john-varvatos',
            "department": 'john-varvatos',
        },
    },
    'jonathan-adler': {
        'jonathan-adler': {
            "url": 'https://www.bloomingdales.com/shop/jonathan-adler?id=1312595',
            "category": 'jonathan-adler',
            "department": 'jonathan-adler',
        },
    },
    'jordan': {
        'jordan': {
            "url": 'https://www.bloomingdales.com/shop/jordan?id=1276295',
            "category": 'jordan',
            "department": 'jordan',
        },
    },
    'juliska': {
        'juliska': {
            "url": 'https://www.bloomingdales.com/shop/juliska?id=1213563',
            "category": 'juliska',
            "department": 'juliska',
        },
        'juliska-barware': {
            "url": 'https://www.bloomingdales.com/shop/juliska/barware?id=1213565',
            "category": 'juliska-barware',
            "department": 'juliska',
        },
        'juliska-berry-thread-collection': {
            "url": 'https://www.bloomingdales.com/shop/juliska/berry-thread-collection?id=1308802',
            "category": 'juliska-berry-thread-collection',
            "department": 'juliska',
        },
        'juliska-dinnerware': {
            "url": 'https://www.bloomingdales.com/shop/juliska/dinnerware?id=1213566',
            "category": 'juliska-dinnerware',
            "department": 'juliska',
        },
        'juliska-drinkware': {
            "url": 'https://www.bloomingdales.com/shop/juliska/drinkware?id=1213567',
            "category": 'juliska-drinkware',
            "department": 'juliska',
        },
        'juliska-entertaining-accessories': {
            "url": 'https://www.bloomingdales.com/shop/juliska/entertaining-accessories?id=1299203',
            "category": 'juliska-entertaining-accessories',
            "department": 'juliska',
        },
        'juliska-flatware': {
            "url": 'https://www.bloomingdales.com/shop/juliska/flatware?id=1213568',
            "category": 'juliska-flatware',
            "department": 'juliska',
        },
        'juliska-gifts-boxed-sets': {
            "url": 'https://www.bloomingdales.com/shop/juliska/gifts-boxed-sets?id=1229865',
            "category": 'juliska-gifts-boxed-sets',
            "department": 'juliska',
        },
        'juliska-home-decor': {
            "url": 'https://www.bloomingdales.com/shop/juliska/home-decor?id=1213570',
            "category": 'juliska-home-decor',
            "department": 'juliska',
        },
        'juliska-little-white-plates': {
            "url": 'https://www.bloomingdales.com/shop/juliska/little-white-plates?id=1219460',
            "category": 'juliska-little-white-plates',
            "department": 'juliska',
        },
        'juliska-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/juliska/new-arrivals?id=1299204',
            "category": 'juliska-new-arrivals',
            "department": 'juliska',
        },
        'juliska-outdoor-dining': {
            "url": 'https://www.bloomingdales.com/shop/juliska/outdoor-dining?id=1219459',
            "category": 'juliska-outdoor-dining',
            "department": 'juliska',
        },
        'juliska-registry-favorites': {
            "url": 'https://www.bloomingdales.com/shop/juliska/registry-favorites?id=1299199',
            "category": 'juliska-registry-favorites',
            "department": 'juliska',
        },
        'juliska-serveware': {
            "url": 'https://www.bloomingdales.com/shop/juliska/serveware?id=1213571',
            "category": 'juliska-serveware',
            "department": 'juliska',
        },
        'juliska-table-linens': {
            "url": 'https://www.bloomingdales.com/shop/juliska/table-linens?id=1213572',
            "category": 'juliska-table-linens',
            "department": 'juliska',
        },
    },
    'jura': {
        'jura': {
            "url": 'https://www.bloomingdales.com/shop/jura?id=1253197',
            "category": 'jura',
            "department": 'jura',
        },
    },
    'just-imagine': {
        'just-imagine': {
            "url": 'https://www.bloomingdales.com/shop/just-imagine?id=1283218',
            "category": 'just-imagine',
            "department": 'just-imagine',
        },
    },
    'kate-spade-new-york': {
        'kate-spade-new-york': {
            "url": 'https://www.bloomingdales.com/shop/kate-spade-new-york?id=1002760',
            "category": 'kate-spade-new-york',
            "department": 'kate-spade-new-york',
        },
        'kate-spade-new-york-handbags-wallets': {
            "url": 'https://www.bloomingdales.com/shop/kate-spade-new-york/handbags-wallets?id=1002763',
            "category": 'kate-spade-new-york-handbags-wallets',
            "department": 'kate-spade-new-york',
        },
        'kate-spade-new-york-home-decor': {
            "url": 'https://www.bloomingdales.com/shop/kate-spade-new-york/home-decor?id=1002765',
            "category": 'kate-spade-new-york-home-decor',
            "department": 'kate-spade-new-york',
        },
        'kate-spade-new-york-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/kate-spade-new-york/jewelry-accessories?id=1002764',
            "category": 'kate-spade-new-york-jewelry-accessories',
            "department": 'kate-spade-new-york',
        },
        'kate-spade-new-york-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/kate-spade-new-york/womens-clothing?id=1002761',
            "category": 'kate-spade-new-york-womens-clothing',
            "department": 'kate-spade-new-york',
        },
        'kate-spade-new-york-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kate-spade-new-york/womens-shoes?id=1002762',
            "category": 'kate-spade-new-york-womens-shoes',
            "department": 'kate-spade-new-york',
        },
    },
    'katiejnyc': {
        'katiejnyc': {
            "url": 'https://www.bloomingdales.com/shop/katiejnyc?id=1272420',
            "category": 'katiejnyc',
            "department": 'katiejnyc',
        },
    },
    'kendra-scott': {
        'kendra-scott': {
            "url": 'https://www.bloomingdales.com/shop/kendra-scott?id=1323095',
            "category": 'kendra-scott',
            "department": 'kendra-scott',
        },
    },
    'kids': {
        'kids': {
            "url": 'https://www.bloomingdales.com/shop/kids?id=3866',
            "category": 'kids',
            "department": 'kids',
        },
        'kids-active-athleisure-shop': {
            "url": 'https://www.bloomingdales.com/shop/kids/active-athleisure-shop?id=1110159',
            "category": 'kids-active-athleisure-shop',
            "department": 'kids',
        },
        'kids-active-lounge': {
            "url": 'https://www.bloomingdales.com/shop/kids/active-lounge?id=1243995',
            "category": 'kids-active-lounge',
            "department": 'kids',
        },
        'kids-all-boys': {
            "url": 'https://www.bloomingdales.com/shop/kids/all-boys?id=1004562',
            "category": 'kids-all-boys',
            "department": 'kids',
        },
        'kids-all-girls': {
            "url": 'https://www.bloomingdales.com/shop/kids/all-girls?id=1003116',
            "category": 'kids-all-girls',
            "department": 'kids',
        },
        'kids-all-kids': {
            "url": 'https://www.bloomingdales.com/shop/kids/all-kids?id=1003623',
            "category": 'kids-all-kids',
            "department": 'kids',
        },
        'kids-arts-and-crafts': {
            "url": 'https://www.bloomingdales.com/shop/kids/arts-and-crafts?id=1325700',
            "category": 'kids-arts-and-crafts',
            "department": 'kids',
        },
        'kids-arts-crafts': {
            "url": 'https://www.bloomingdales.com/shop/kids/arts-crafts?id=1152559',
            "category": 'kids-arts-crafts',
            "department": 'kids',
        },
        'kids-baby-appliances': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-appliances?id=1336796',
            "category": 'kids-baby-appliances',
            "department": 'kids',
        },
        'kids-baby-bath-toys-hooded-towel-shampoo': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-bath-toys-hooded-towel-shampoo?id=1006100',
            "category": 'kids-baby-bath-toys-hooded-towel-shampoo',
            "department": 'kids',
        },
        'kids-baby-blankets-burp-cloths': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-blankets-burp-cloths?id=1005604',
            "category": 'kids-baby-blankets-burp-cloths',
            "department": 'kids',
        },
        'kids-baby-boy-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-boy-bottoms?id=1006133',
            "category": 'kids-baby-boy-bottoms',
            "department": 'kids',
        },
        'kids-baby-boy-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-boy-clothes?id=23713',
            "category": 'kids-baby-boy-clothes',
            "department": 'kids',
        },
        'kids-baby-boy-onesies': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-boy-onesies?id=1006131',
            "category": 'kids-baby-boy-onesies',
            "department": 'kids',
        },
        'kids-baby-boy-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-boy-shoes?id=1335298',
            "category": 'kids-baby-boy-shoes',
            "department": 'kids',
        },
        'kids-baby-boy-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-boy-swimwear?id=1006136',
            "category": 'kids-baby-boy-swimwear',
            "department": 'kids',
        },
        'kids-baby-boy-tops': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-boy-tops?id=1006137',
            "category": 'kids-baby-boy-tops',
            "department": 'kids',
        },
        'kids-baby-carriers': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-carriers?id=1210777',
            "category": 'kids-baby-carriers',
            "department": 'kids',
        },
        'kids-baby-essentials-gadgets': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-essentials-gadgets?id=1336795',
            "category": 'kids-baby-essentials-gadgets',
            "department": 'kids',
        },
        'kids-baby-feeding-products-and-high-chairs': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-feeding-products-and-high-chairs?id=1006101',
            "category": 'kids-baby-feeding-products-and-high-chairs',
            "department": 'kids',
        },
        'kids-baby-gear': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-gear?id=1054360',
            "category": 'kids-baby-gear',
            "department": 'kids',
        },
        'kids-baby-girl-accessories': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-girl-accessories?id=1335300',
            "category": 'kids-baby-girl-accessories',
            "department": 'kids',
        },
        'kids-baby-girl-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-girl-bottoms?id=1006123',
            "category": 'kids-baby-girl-bottoms',
            "department": 'kids',
        },
        'kids-baby-girl-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-girl-clothes?id=23712',
            "category": 'kids-baby-girl-clothes',
            "department": 'kids',
        },
        'kids-baby-girl-onesies': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-girl-onesies?id=1006121',
            "category": 'kids-baby-girl-onesies',
            "department": 'kids',
        },
        'kids-baby-girl-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-girl-shoes?id=1335297',
            "category": 'kids-baby-girl-shoes',
            "department": 'kids',
        },
        'kids-baby-girl-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-girl-swimwear?id=1006125',
            "category": 'kids-baby-girl-swimwear',
            "department": 'kids',
        },
        'kids-baby-girl-tops': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-girl-tops?id=1006126',
            "category": 'kids-baby-girl-tops',
            "department": 'kids',
        },
        'kids-baby-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-shoes?id=1003141',
            "category": 'kids-baby-shoes',
            "department": 'kids',
        },
        'kids-baby-toddler-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-toddler-toys?id=1325695',
            "category": 'kids-baby-toddler-toys',
            "department": 'kids',
        },
        'kids-baby-toys-plush': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-toys-plush?id=1000307',
            "category": 'kids-baby-toys-plush',
            "department": 'kids',
        },
        'kids-baby-travel-products': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-travel-products?id=1163859',
            "category": 'kids-baby-travel-products',
            "department": 'kids',
        },
        'kids-baby-unisex-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/baby-unisex-clothes?id=1335302',
            "category": 'kids-baby-unisex-clothes',
            "department": 'kids',
        },
        'kids-back-to-school-accessories': {
            "url": 'https://www.bloomingdales.com/shop/kids/back-to-school-accessories?id=1323999',
            "category": 'kids-back-to-school-accessories',
            "department": 'kids',
        },
        'kids-back-to-school-boys-clothing': {
            "url": 'https://www.bloomingdales.com/shop/kids/back-to-school-boys-clothing?id=1323998',
            "category": 'kids-back-to-school-boys-clothing',
            "department": 'kids',
        },
        'kids-back-to-school-essentials': {
            "url": 'https://www.bloomingdales.com/shop/kids/back-to-school-essentials?id=1128566',
            "category": 'kids-back-to-school-essentials',
            "department": 'kids',
        },
        'kids-back-to-school-girls-clothing': {
            "url": 'https://www.bloomingdales.com/shop/kids/back-to-school-girls-clothing?id=1323997',
            "category": 'kids-back-to-school-girls-clothing',
            "department": 'kids',
        },
        'kids-back-to-school-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kids/back-to-school-shoes?id=1324141',
            "category": 'kids-back-to-school-shoes',
            "department": 'kids',
        },
        'kids-backpacks': {
            "url": 'https://www.bloomingdales.com/shop/kids/backpacks?id=1238159',
            "category": 'kids-backpacks',
            "department": 'kids',
        },
        'kids-bedding': {
            "url": 'https://www.bloomingdales.com/shop/kids/bedding?id=1221959',
            "category": 'kids-bedding',
            "department": 'kids',
        },
        'kids-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/kids/best-sellers?id=1044059',
            "category": 'kids-best-sellers',
            "department": 'kids',
        },
        'kids-big-boy-clothes-8-20': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boy-clothes-8-20?id=23723',
            "category": 'kids-big-boy-clothes-8-20',
            "department": 'kids',
        },
        'kids-big-boys-activewear': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-activewear?id=1006210',
            "category": 'kids-big-boys-activewear',
            "department": 'kids',
        },
        'kids-big-boys-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-coats-jackets?id=1006211',
            "category": 'kids-big-boys-coats-jackets',
            "department": 'kids',
        },
        'kids-big-boys-dress-shirts-button-downs': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-dress-shirts-button-downs?id=1006212',
            "category": 'kids-big-boys-dress-shirts-button-downs',
            "department": 'kids',
        },
        'kids-big-boys-hoodies-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-hoodies-sweatshirts?id=1006213',
            "category": 'kids-big-boys-hoodies-sweatshirts',
            "department": 'kids',
        },
        'kids-big-boys-jeans': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-jeans?id=1006214',
            "category": 'kids-big-boys-jeans',
            "department": 'kids',
        },
        'kids-big-boys-outfit-sets': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-outfit-sets?id=1006265',
            "category": 'kids-big-boys-outfit-sets',
            "department": 'kids',
        },
        'kids-big-boys-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-pajamas?id=1006216',
            "category": 'kids-big-boys-pajamas',
            "department": 'kids',
        },
        'kids-big-boys-pants-shorts': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-pants-shorts?id=1006215',
            "category": 'kids-big-boys-pants-shorts',
            "department": 'kids',
        },
        'kids-big-boys-suits-sport-coats': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-suits-sport-coats?id=1006217',
            "category": 'kids-big-boys-suits-sport-coats',
            "department": 'kids',
        },
        'kids-big-boys-sweaters-cardigans': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-sweaters-cardigans?id=1006218',
            "category": 'kids-big-boys-sweaters-cardigans',
            "department": 'kids',
        },
        'kids-big-boys-swimwear-swim-trunks': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-swimwear-swim-trunks?id=1006219',
            "category": 'kids-big-boys-swimwear-swim-trunks',
            "department": 'kids',
        },
        'kids-big-boys-t-shirts-polos': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-t-shirts-polos?id=1006220',
            "category": 'kids-big-boys-t-shirts-polos',
            "department": 'kids',
        },
        'kids-big-boys-underwear-socks': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-boys-underwear-socks?id=1006221',
            "category": 'kids-big-boys-underwear-socks',
            "department": 'kids',
        },
        'kids-big-girl-clothes-7-16': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girl-clothes-7-16?id=23720',
            "category": 'kids-big-girl-clothes-7-16',
            "department": 'kids',
        },
        'kids-big-girls-activewear': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-activewear?id=1006164',
            "category": 'kids-big-girls-activewear',
            "department": 'kids',
        },
        'kids-big-girls-coats-jackets-vests': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-coats-jackets-vests?id=1006165',
            "category": 'kids-big-girls-coats-jackets-vests',
            "department": 'kids',
        },
        'kids-big-girls-dresses-rompers': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-dresses-rompers?id=1006166',
            "category": 'kids-big-girls-dresses-rompers',
            "department": 'kids',
        },
        'kids-big-girls-jeans': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-jeans?id=1006167',
            "category": 'kids-big-girls-jeans',
            "department": 'kids',
        },
        'kids-big-girls-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-pajamas?id=1006170',
            "category": 'kids-big-girls-pajamas',
            "department": 'kids',
        },
        'kids-big-girls-pants-shorts-skirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-pants-shorts-skirts?id=1006172',
            "category": 'kids-big-girls-pants-shorts-skirts',
            "department": 'kids',
        },
        'kids-big-girls-sweaters-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-sweaters-sweatshirts?id=1006174',
            "category": 'kids-big-girls-sweaters-sweatshirts',
            "department": 'kids',
        },
        'kids-big-girls-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-swimwear?id=1006175',
            "category": 'kids-big-girls-swimwear',
            "department": 'kids',
        },
        'kids-big-girls-tops-tees': {
            "url": 'https://www.bloomingdales.com/shop/kids/big-girls-tops-tees?id=1006178',
            "category": 'kids-big-girls-tops-tees',
            "department": 'kids',
        },
        'kids-birthday-gifts': {
            "url": 'https://www.bloomingdales.com/shop/kids/birthday-gifts?id=1289795',
            "category": 'kids-birthday-gifts',
            "department": 'kids',
        },
        'kids-booster-seats': {
            "url": 'https://www.bloomingdales.com/shop/kids/booster-seats?id=1335507',
            "category": 'kids-booster-seats',
            "department": 'kids',
        },
        'kids-bouncers': {
            "url": 'https://www.bloomingdales.com/shop/kids/bouncers?id=1210668',
            "category": 'kids-bouncers',
            "department": 'kids',
        },
        'kids-boys-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-bottoms?id=1099867',
            "category": 'kids-boys-bottoms',
            "department": 'kids',
        },
        'kids-boys-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-coats-jackets?id=1175561',
            "category": 'kids-boys-coats-jackets',
            "department": 'kids',
        },
        'kids-boys-hoodies-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-hoodies-sweatshirts?id=1099870',
            "category": 'kids-boys-hoodies-sweatshirts',
            "department": 'kids',
        },
        'kids-boys-jeans-denim': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-jeans-denim?id=1099871',
            "category": 'kids-boys-jeans-denim',
            "department": 'kids',
        },
        'kids-boys-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-pajamas?id=1335506',
            "category": 'kids-boys-pajamas',
            "department": 'kids',
        },
        'kids-boys-pants': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-pants?id=1335503',
            "category": 'kids-boys-pants',
            "department": 'kids',
        },
        'kids-boys-polo-shirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-polo-shirts?id=1335502',
            "category": 'kids-boys-polo-shirts',
            "department": 'kids',
        },
        'kids-boys-shirts-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-shirts-sweaters?id=1099865',
            "category": 'kids-boys-shirts-sweaters',
            "department": 'kids',
        },
        'kids-boys-shoes-boots': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-shoes-boots?id=1146663',
            "category": 'kids-boys-shoes-boots',
            "department": 'kids',
        },
        'kids-boys-shorts': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-shorts?id=1335504',
            "category": 'kids-boys-shorts',
            "department": 'kids',
        },
        'kids-boys-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-sweaters?id=1103459',
            "category": 'kids-boys-sweaters',
            "department": 'kids',
        },
        'kids-boys-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-swimwear?id=1099868',
            "category": 'kids-boys-swimwear',
            "department": 'kids',
        },
        'kids-boys-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-t-shirts?id=1335501',
            "category": 'kids-boys-t-shirts',
            "department": 'kids',
        },
        'kids-boys-t-shirts-polo': {
            "url": 'https://www.bloomingdales.com/shop/kids/boys-t-shirts-polo?id=1099866',
            "category": 'kids-boys-t-shirts-polo',
            "department": 'kids',
        },
        'kids-chairs-ottomans': {
            "url": 'https://www.bloomingdales.com/shop/kids/chairs-ottomans?id=1221960',
            "category": 'kids-chairs-ottomans',
            "department": 'kids',
        },
        'kids-changing-tables-dressers': {
            "url": 'https://www.bloomingdales.com/shop/kids/changing-tables-dressers?id=1221961',
            "category": 'kids-changing-tables-dressers',
            "department": 'kids',
        },
        'kids-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/coats-jackets?id=1175559',
            "category": 'kids-coats-jackets',
            "department": 'kids',
        },
        'kids-cribs-bassinets': {
            "url": 'https://www.bloomingdales.com/shop/kids/cribs-bassinets?id=1210666',
            "category": 'kids-cribs-bassinets',
            "department": 'kids',
        },
        'kids-decor': {
            "url": 'https://www.bloomingdales.com/shop/kids/decor?id=1228161',
            "category": 'kids-decor',
            "department": 'kids',
        },
        'kids-diaper-bags': {
            "url": 'https://www.bloomingdales.com/shop/kids/diaper-bags?id=1210779',
            "category": 'kids-diaper-bags',
            "department": 'kids',
        },
        'kids-double-strollers': {
            "url": 'https://www.bloomingdales.com/shop/kids/double-strollers?id=1336799',
            "category": 'kids-double-strollers',
            "department": 'kids',
        },
        'kids-easter': {
            "url": 'https://www.bloomingdales.com/shop/kids/easter?id=1307503',
            "category": 'kids-easter',
            "department": 'kids',
        },
        'kids-educational-developmental-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/educational-developmental-toys?id=1133059',
            "category": 'kids-educational-developmental-toys',
            "department": 'kids',
        },
        'kids-first-birthday-gifts': {
            "url": 'https://www.bloomingdales.com/shop/kids/first-birthday-gifts?id=1288948',
            "category": 'kids-first-birthday-gifts',
            "department": 'kids',
        },
        'kids-girls-activewear': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-activewear?id=1118561',
            "category": 'kids-girls-activewear',
            "department": 'kids',
        },
        'kids-girls-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-bottoms?id=1099860',
            "category": 'kids-girls-bottoms',
            "department": 'kids',
        },
        'kids-girls-casual-dresses-rompers': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-casual-dresses-rompers?id=1192067',
            "category": 'kids-girls-casual-dresses-rompers',
            "department": 'kids',
        },
        'kids-girls-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-coats-jackets?id=1099862',
            "category": 'kids-girls-coats-jackets',
            "department": 'kids',
        },
        'kids-girls-dresses-rompers': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-dresses-rompers?id=1191966',
            "category": 'kids-girls-dresses-rompers',
            "department": 'kids',
        },
        'kids-girls-jeans': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-jeans?id=1335496',
            "category": 'kids-girls-jeans',
            "department": 'kids',
        },
        'kids-girls-jeans-denim': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-jeans-denim?id=1099864',
            "category": 'kids-girls-jeans-denim',
            "department": 'kids',
        },
        'kids-girls-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-pajamas?id=1335498',
            "category": 'kids-girls-pajamas',
            "department": 'kids',
        },
        'kids-girls-pants': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-pants?id=1335308',
            "category": 'kids-girls-pants',
            "department": 'kids',
        },
        'kids-girls-party-dresses-rompers': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-party-dresses-rompers?id=1192068',
            "category": 'kids-girls-party-dresses-rompers',
            "department": 'kids',
        },
        'kids-girls-shoes-boots': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-shoes-boots?id=1003142',
            "category": 'kids-girls-shoes-boots',
            "department": 'kids',
        },
        'kids-girls-skirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-skirts?id=1335497',
            "category": 'kids-girls-skirts',
            "department": 'kids',
        },
        'kids-girls-sweaters-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-sweaters-sweatshirts?id=1099863',
            "category": 'kids-girls-sweaters-sweatshirts',
            "department": 'kids',
        },
        'kids-girls-sweatshirts-hoodies': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-sweatshirts-hoodies?id=1335307',
            "category": 'kids-girls-sweatshirts-hoodies',
            "department": 'kids',
        },
        'kids-girls-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-swimwear?id=1099859',
            "category": 'kids-girls-swimwear',
            "department": 'kids',
        },
        'kids-girls-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-t-shirts?id=1335305',
            "category": 'kids-girls-t-shirts',
            "department": 'kids',
        },
        'kids-girls-tank-tops': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-tank-tops?id=1335306',
            "category": 'kids-girls-tank-tops',
            "department": 'kids',
        },
        'kids-girls-tops': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-tops?id=1099861',
            "category": 'kids-girls-tops',
            "department": 'kids',
        },
        'kids-girls-trending-dresses-rompers': {
            "url": 'https://www.bloomingdales.com/shop/kids/girls-trending-dresses-rompers?id=1202070',
            "category": 'kids-girls-trending-dresses-rompers',
            "department": 'kids',
        },
        'kids-graduation': {
            "url": 'https://www.bloomingdales.com/shop/kids/graduation?id=1311795',
            "category": 'kids-graduation',
            "department": 'kids',
        },
        'kids-halloween': {
            "url": 'https://www.bloomingdales.com/shop/kids/halloween?id=1287697',
            "category": 'kids-halloween',
            "department": 'kids',
        },
        'kids-health-safety': {
            "url": 'https://www.bloomingdales.com/shop/kids/health-safety?id=1210675',
            "category": 'kids-health-safety',
            "department": 'kids',
        },
        'kids-infant-travel-systems': {
            "url": 'https://www.bloomingdales.com/shop/kids/infant-travel-systems?id=1210775',
            "category": 'kids-infant-travel-systems',
            "department": 'kids',
        },
        'kids-katiejnyc': {
            "url": 'https://www.bloomingdales.com/shop/kids/katiejnyc?id=1251509',
            "category": 'kids-katiejnyc',
            "department": 'kids',
        },
        'kids-kids-accessories': {
            "url": 'https://www.bloomingdales.com/shop/kids/kids-accessories?id=1101559',
            "category": 'kids-kids-accessories',
            "department": 'kids',
        },
        'kids-kids-books': {
            "url": 'https://www.bloomingdales.com/shop/kids/kids-books?id=1325705',
            "category": 'kids-kids-books',
            "department": 'kids',
        },
        'kids-kids-clothing': {
            "url": 'https://www.bloomingdales.com/shop/kids/kids-clothing?id=1335495',
            "category": 'kids-kids-clothing',
            "department": 'kids',
        },
        'kids-kids-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kids/kids-shoes?id=1001238',
            "category": 'kids-kids-shoes',
            "department": 'kids',
        },
        'kids-kids-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/kids/kids-sneakers?id=1209675',
            "category": 'kids-kids-sneakers',
            "department": 'kids',
        },
        'kids-kids-toys-online': {
            "url": 'https://www.bloomingdales.com/shop/kids/kids-toys-online?id=1001236',
            "category": 'kids-kids-toys-online',
            "department": 'kids',
        },
        'kids-kitchen-food': {
            "url": 'https://www.bloomingdales.com/shop/kids/kitchen-food?id=1133060',
            "category": 'kids-kitchen-food',
            "department": 'kids',
        },
        'kids-little-boy-clothes-2-7': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boy-clothes-2-7?id=23722',
            "category": 'kids-little-boy-clothes-2-7',
            "department": 'kids',
        },
        'kids-little-boys-activewear': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-activewear?id=1006198',
            "category": 'kids-little-boys-activewear',
            "department": 'kids',
        },
        'kids-little-boys-clothing-sets': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-clothing-sets?id=1006264',
            "category": 'kids-little-boys-clothing-sets',
            "department": 'kids',
        },
        'kids-little-boys-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-coats-jackets?id=1006199',
            "category": 'kids-little-boys-coats-jackets',
            "department": 'kids',
        },
        'kids-little-boys-dress-shirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-dress-shirts?id=1006200',
            "category": 'kids-little-boys-dress-shirts',
            "department": 'kids',
        },
        'kids-little-boys-hoodies-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-hoodies-sweatshirts?id=1006201',
            "category": 'kids-little-boys-hoodies-sweatshirts',
            "department": 'kids',
        },
        'kids-little-boys-jeans': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-jeans?id=1006202',
            "category": 'kids-little-boys-jeans',
            "department": 'kids',
        },
        'kids-little-boys-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-pajamas?id=1006204',
            "category": 'kids-little-boys-pajamas',
            "department": 'kids',
        },
        'kids-little-boys-pants-shorts': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-pants-shorts?id=1006203',
            "category": 'kids-little-boys-pants-shorts',
            "department": 'kids',
        },
        'kids-little-boys-suits-blazers': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-suits-blazers?id=1006205',
            "category": 'kids-little-boys-suits-blazers',
            "department": 'kids',
        },
        'kids-little-boys-sweaters-cardigans': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-sweaters-cardigans?id=1006206',
            "category": 'kids-little-boys-sweaters-cardigans',
            "department": 'kids',
        },
        'kids-little-boys-swimwear-swim-trunks': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-swimwear-swim-trunks?id=1006207',
            "category": 'kids-little-boys-swimwear-swim-trunks',
            "department": 'kids',
        },
        'kids-little-boys-t-shirts-polos': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-t-shirts-polos?id=1006208',
            "category": 'kids-little-boys-t-shirts-polos',
            "department": 'kids',
        },
        'kids-little-boys-underwear-socks': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-boys-underwear-socks?id=1006209',
            "category": 'kids-little-boys-underwear-socks',
            "department": 'kids',
        },
        'kids-little-girl-clothes-2-6x': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girl-clothes-2-6x?id=23719',
            "category": 'kids-little-girl-clothes-2-6x',
            "department": 'kids',
        },
        'kids-little-girls-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-coats-jackets?id=1006140',
            "category": 'kids-little-girls-coats-jackets',
            "department": 'kids',
        },
        'kids-little-girls-dresses-rompers': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-dresses-rompers?id=1006141',
            "category": 'kids-little-girls-dresses-rompers',
            "department": 'kids',
        },
        'kids-little-girls-jeans': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-jeans?id=1006142',
            "category": 'kids-little-girls-jeans',
            "department": 'kids',
        },
        'kids-little-girls-outfit-sets': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-outfit-sets?id=1006143',
            "category": 'kids-little-girls-outfit-sets',
            "department": 'kids',
        },
        'kids-little-girls-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-pajamas?id=1006144',
            "category": 'kids-little-girls-pajamas',
            "department": 'kids',
        },
        'kids-little-girls-pants-shorts-skirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-pants-shorts-skirts?id=1006145',
            "category": 'kids-little-girls-pants-shorts-skirts',
            "department": 'kids',
        },
        'kids-little-girls-sweaters-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-sweaters-sweatshirts?id=1006146',
            "category": 'kids-little-girls-sweaters-sweatshirts',
            "department": 'kids',
        },
        'kids-little-girls-swimsuits-cover-ups': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-swimsuits-cover-ups?id=1006147',
            "category": 'kids-little-girls-swimsuits-cover-ups',
            "department": 'kids',
        },
        'kids-little-girls-tops-tees': {
            "url": 'https://www.bloomingdales.com/shop/kids/little-girls-tops-tees?id=1006148',
            "category": 'kids-little-girls-tops-tees',
            "department": 'kids',
        },
        'kids-luxury-car-seats': {
            "url": 'https://www.bloomingdales.com/shop/kids/luxury-car-seats?id=1117268',
            "category": 'kids-luxury-car-seats',
            "department": 'kids',
        },
        'kids-luxury-strollers': {
            "url": 'https://www.bloomingdales.com/shop/kids/luxury-strollers?id=1117261',
            "category": 'kids-luxury-strollers',
            "department": 'kids',
        },
        'kids-multi-packs': {
            "url": 'https://www.bloomingdales.com/shop/kids/multi-packs?id=1230459',
            "category": 'kids-multi-packs',
            "department": 'kids',
        },
        'kids-newborn-baby-bottoms-0-9-months': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-bottoms-0-9-months?id=1006115',
            "category": 'kids-newborn-baby-bottoms-0-9-months',
            "department": 'kids',
        },
        'kids-newborn-baby-boy-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-boy-coats-jackets?id=1006130',
            "category": 'kids-newborn-baby-boy-coats-jackets',
            "department": 'kids',
        },
        'kids-newborn-baby-boy-outfit-sets': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-boy-outfit-sets?id=1006132',
            "category": 'kids-newborn-baby-boy-outfit-sets',
            "department": 'kids',
        },
        'kids-newborn-baby-boy-socks': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-boy-socks?id=1006135',
            "category": 'kids-newborn-baby-boy-socks',
            "department": 'kids',
        },
        'kids-newborn-baby-clothes-unisex': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-clothes-unisex?id=23708',
            "category": 'kids-newborn-baby-clothes-unisex',
            "department": 'kids',
        },
        'kids-newborn-baby-clothing-sets-unisex': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-clothing-sets-unisex?id=1006114',
            "category": 'kids-newborn-baby-clothing-sets-unisex',
            "department": 'kids',
        },
        'kids-newborn-baby-coats-jackets-unisex': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-coats-jackets-unisex?id=1006111',
            "category": 'kids-newborn-baby-coats-jackets-unisex',
            "department": 'kids',
        },
        'kids-newborn-baby-dresses-0-9-months': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-dresses-0-9-months?id=1006112',
            "category": 'kids-newborn-baby-dresses-0-9-months',
            "department": 'kids',
        },
        'kids-newborn-baby-girl-clothing-sets': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-girl-clothing-sets?id=1006122',
            "category": 'kids-newborn-baby-girl-clothing-sets',
            "department": 'kids',
        },
        'kids-newborn-baby-girl-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-girl-coats-jackets?id=1006119',
            "category": 'kids-newborn-baby-girl-coats-jackets',
            "department": 'kids',
        },
        'kids-newborn-baby-girl-dresses': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-girl-dresses?id=1006120',
            "category": 'kids-newborn-baby-girl-dresses',
            "department": 'kids',
        },
        'kids-newborn-baby-girl-socks-tights': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-girl-socks-tights?id=1006127',
            "category": 'kids-newborn-baby-girl-socks-tights',
            "department": 'kids',
        },
        'kids-newborn-baby-onesies-unisex': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-onesies-unisex?id=1006113',
            "category": 'kids-newborn-baby-onesies-unisex',
            "department": 'kids',
        },
        'kids-newborn-baby-socks-unisex': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-socks-unisex?id=1006118',
            "category": 'kids-newborn-baby-socks-unisex',
            "department": 'kids',
        },
        'kids-newborn-baby-tops-t-shirts-unisex': {
            "url": 'https://www.bloomingdales.com/shop/kids/newborn-baby-tops-t-shirts-unisex?id=1006117',
            "category": 'kids-newborn-baby-tops-t-shirts-unisex',
            "department": 'kids',
        },
        'kids-nuna': {
            "url": 'https://www.bloomingdales.com/shop/kids/nuna?id=1247798',
            "category": 'kids-nuna',
            "department": 'kids',
        },
        'kids-nursery-chairs': {
            "url": 'https://www.bloomingdales.com/shop/kids/nursery-chairs?id=1336798',
            "category": 'kids-nursery-chairs',
            "department": 'kids',
        },
        'kids-nursery-furniture': {
            "url": 'https://www.bloomingdales.com/shop/kids/nursery-furniture?id=1336797',
            "category": 'kids-nursery-furniture',
            "department": 'kids',
        },
        'kids-one-pieces': {
            "url": 'https://www.bloomingdales.com/shop/kids/one-pieces?id=1204959',
            "category": 'kids-one-pieces',
            "department": 'kids',
        },
        'kids-outdoor-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/outdoor-toys?id=1325698',
            "category": 'kids-outdoor-toys',
            "department": 'kids',
        },
        'kids-outfit-sets': {
            "url": 'https://www.bloomingdales.com/shop/kids/outfit-sets?id=1204961',
            "category": 'kids-outfit-sets',
            "department": 'kids',
        },
        'kids-pack-plays': {
            "url": 'https://www.bloomingdales.com/shop/kids/pack-plays?id=1210778',
            "category": 'kids-pack-plays',
            "department": 'kids',
        },
        'kids-pajama-shop': {
            "url": 'https://www.bloomingdales.com/shop/kids/pajama-shop?id=1055159',
            "category": 'kids-pajama-shop',
            "department": 'kids',
        },
        'kids-playmats-activity-gyms': {
            "url": 'https://www.bloomingdales.com/shop/kids/playmats-activity-gyms?id=1210667',
            "category": 'kids-playmats-activity-gyms',
            "department": 'kids',
        },
        'kids-pretend-play': {
            "url": 'https://www.bloomingdales.com/shop/kids/pretend-play?id=1292319',
            "category": 'kids-pretend-play',
            "department": 'kids',
        },
        'kids-ride-on-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/ride-on-toys?id=1325696',
            "category": 'kids-ride-on-toys',
            "department": 'kids',
        },
        'kids-ride-ons': {
            "url": 'https://www.bloomingdales.com/shop/kids/ride-ons?id=1204459',
            "category": 'kids-ride-ons',
            "department": 'kids',
        },
        'kids-science-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/science-toys?id=1325703',
            "category": 'kids-science-toys',
            "department": 'kids',
        },
        'kids-shop-by-occasion-holiday': {
            "url": 'https://www.bloomingdales.com/shop/kids/shop-by-occasion-holiday?id=1307502',
            "category": 'kids-shop-by-occasion-holiday',
            "department": 'kids',
        },
        'kids-sleepers-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/sleepers-pajamas?id=1204960',
            "category": 'kids-sleepers-pajamas',
            "department": 'kids',
        },
        'kids-snow-boots-winter-coats': {
            "url": 'https://www.bloomingdales.com/shop/kids/snow-boots-winter-coats?id=1001681',
            "category": 'kids-snow-boots-winter-coats',
            "department": 'kids',
        },
        'kids-special-occasion-dresses-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/special-occasion-dresses-clothes?id=1002580',
            "category": 'kids-special-occasion-dresses-clothes',
            "department": 'kids',
        },
        'kids-sports-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/sports-toys?id=1325702',
            "category": 'kids-sports-toys',
            "department": 'kids',
        },
        'kids-strollers-under-700': {
            "url": 'https://www.bloomingdales.com/shop/kids/strollers-under-700?id=1273895',
            "category": 'kids-strollers-under-700',
            "department": 'kids',
        },
        'kids-swaddle-plush-blankets': {
            "url": 'https://www.bloomingdales.com/shop/kids/swaddle-plush-blankets?id=1006102',
            "category": 'kids-swaddle-plush-blankets',
            "department": 'kids',
        },
        'kids-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/kids/sweaters?id=1286995',
            "category": 'kids-sweaters',
            "department": 'kids',
        },
        'kids-swim': {
            "url": 'https://www.bloomingdales.com/shop/kids/swim?id=1006116',
            "category": 'kids-swim',
            "department": 'kids',
        },
        'kids-the-birthday-shop': {
            "url": 'https://www.bloomingdales.com/shop/kids/the-birthday-shop?id=1291395',
            "category": 'kids-the-birthday-shop',
            "department": 'kids',
        },
        'kids-the-sleepover-shop': {
            "url": 'https://www.bloomingdales.com/shop/kids/the-sleepover-shop?id=1327395',
            "category": 'kids-the-sleepover-shop',
            "department": 'kids',
        },
        'kids-tie-dye-shop': {
            "url": 'https://www.bloomingdales.com/shop/kids/tie-dye-shop?id=1118560',
            "category": 'kids-tie-dye-shop',
            "department": 'kids',
        },
        'kids-toddler-boy-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-bottoms?id=1333207',
            "category": 'kids-toddler-boy-bottoms',
            "department": 'kids',
        },
        'kids-toddler-boy-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-clothes?id=1333204',
            "category": 'kids-toddler-boy-clothes',
            "department": 'kids',
        },
        'kids-toddler-boy-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-coats-jackets?id=1333206',
            "category": 'kids-toddler-boy-coats-jackets',
            "department": 'kids',
        },
        'kids-toddler-boy-jeans-pants': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-jeans-pants?id=1333208',
            "category": 'kids-toddler-boy-jeans-pants',
            "department": 'kids',
        },
        'kids-toddler-boy-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-pajamas?id=1333504',
            "category": 'kids-toddler-boy-pajamas',
            "department": 'kids',
        },
        'kids-toddler-boy-shirts-tops': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-shirts-tops?id=1333210',
            "category": 'kids-toddler-boy-shirts-tops',
            "department": 'kids',
        },
        'kids-toddler-boy-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-shoes?id=1335296',
            "category": 'kids-toddler-boy-shoes',
            "department": 'kids',
        },
        'kids-toddler-boy-shorts': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-shorts?id=1333209',
            "category": 'kids-toddler-boy-shorts',
            "department": 'kids',
        },
        'kids-toddler-boy-suits': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-suits?id=1333506',
            "category": 'kids-toddler-boy-suits',
            "department": 'kids',
        },
        'kids-toddler-boy-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-sweaters?id=1333502',
            "category": 'kids-toddler-boy-sweaters',
            "department": 'kids',
        },
        'kids-toddler-boy-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-swimwear?id=1333505',
            "category": 'kids-toddler-boy-swimwear',
            "department": 'kids',
        },
        'kids-toddler-boy-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-boy-t-shirts?id=1333503',
            "category": 'kids-toddler-boy-t-shirts',
            "department": 'kids',
        },
        'kids-toddler-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-clothes?id=1322504',
            "category": 'kids-toddler-clothes',
            "department": 'kids',
        },
        'kids-toddler-girl-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-bottoms?id=1322508',
            "category": 'kids-toddler-girl-bottoms',
            "department": 'kids',
        },
        'kids-toddler-girl-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-clothes?id=1322505',
            "category": 'kids-toddler-girl-clothes',
            "department": 'kids',
        },
        'kids-toddler-girl-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-coats-jackets?id=1322506',
            "category": 'kids-toddler-girl-coats-jackets',
            "department": 'kids',
        },
        'kids-toddler-girl-dresses': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-dresses?id=1322507',
            "category": 'kids-toddler-girl-dresses',
            "department": 'kids',
        },
        'kids-toddler-girl-jeans-pants': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-jeans-pants?id=1333198',
            "category": 'kids-toddler-girl-jeans-pants',
            "department": 'kids',
        },
        'kids-toddler-girl-matching-sets': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-matching-sets?id=1333203',
            "category": 'kids-toddler-girl-matching-sets',
            "department": 'kids',
        },
        'kids-toddler-girl-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-pajamas?id=1333202',
            "category": 'kids-toddler-girl-pajamas',
            "department": 'kids',
        },
        'kids-toddler-girl-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-shoes?id=1335295',
            "category": 'kids-toddler-girl-shoes',
            "department": 'kids',
        },
        'kids-toddler-girl-shorts': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-shorts?id=1322509',
            "category": 'kids-toddler-girl-shorts',
            "department": 'kids',
        },
        'kids-toddler-girl-skirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-skirts?id=1322510',
            "category": 'kids-toddler-girl-skirts',
            "department": 'kids',
        },
        'kids-toddler-girl-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-sweaters?id=1333200',
            "category": 'kids-toddler-girl-sweaters',
            "department": 'kids',
        },
        'kids-toddler-girl-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-swimwear?id=1333205',
            "category": 'kids-toddler-girl-swimwear',
            "department": 'kids',
        },
        'kids-toddler-girl-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-t-shirts?id=1333201',
            "category": 'kids-toddler-girl-t-shirts',
            "department": 'kids',
        },
        'kids-toddler-girl-tops': {
            "url": 'https://www.bloomingdales.com/shop/kids/toddler-girl-tops?id=1333199',
            "category": 'kids-toddler-girl-tops',
            "department": 'kids',
        },
        'kids-travel': {
            "url": 'https://www.bloomingdales.com/shop/kids/travel?id=1210776',
            "category": 'kids-travel',
            "department": 'kids',
        },
        'kids-travel-strollers': {
            "url": 'https://www.bloomingdales.com/shop/kids/travel-strollers?id=1336296',
            "category": 'kids-travel-strollers',
            "department": 'kids',
        },
        'kids-tween-clothes': {
            "url": 'https://www.bloomingdales.com/shop/kids/tween-clothes?id=1336295',
            "category": 'kids-tween-clothes',
            "department": 'kids',
        },
        'kids-under-25-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/under-25-toys?id=1252700',
            "category": 'kids-under-25-toys',
            "department": 'kids',
        },
        'kids-under-50-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/under-50-toys?id=1252699',
            "category": 'kids-under-50-toys',
            "department": 'kids',
        },
        'kids-wooden-toys': {
            "url": 'https://www.bloomingdales.com/shop/kids/wooden-toys?id=1325697',
            "category": 'kids-wooden-toys',
            "department": 'kids',
        },
    },
    'kiehls-since-1851': {
        'kiehls-since-1851': {
            "url": 'https://www.bloomingdales.com/shop/kiehls-since-1851?id=1203063',
            "category": 'kiehls-since-1851',
            "department": 'kiehls-since-1851',
        },
    },
    'kilian-paris': {
        'kilian-paris': {
            "url": 'https://www.bloomingdales.com/shop/kilian-paris?id=1323096',
            "category": 'kilian-paris',
            "department": 'kilian-paris',
        },
    },
    'korean-japanese-beauty-brands': {
        'korean-japanese-beauty-brands': {
            "url": 'https://www.bloomingdales.com/shop/korean-japanese-beauty-brands?id=1267053',
            "category": 'korean-japanese-beauty-brands',
            "department": 'korean-japanese-beauty-brands',
        },
    },
    'kurt-geiger-london': {
        'kurt-geiger-london': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london?id=1265449',
            "category": 'kurt-geiger-london',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-crossbody-bags': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/crossbody-bags?id=1308605',
            "category": 'kurt-geiger-london-crossbody-bags',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-flats': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/flats?id=1308698',
            "category": 'kurt-geiger-london-flats',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-handbags': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/handbags?id=1268705',
            "category": 'kurt-geiger-london-handbags',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-mini-bags': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/mini-bags?id=1308604',
            "category": 'kurt-geiger-london-mini-bags',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-pumps': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/pumps?id=1308696',
            "category": 'kurt-geiger-london-pumps',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-sandals': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/sandals?id=1308695',
            "category": 'kurt-geiger-london-sandals',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-shoulder-bags': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/shoulder-bags?id=1308606',
            "category": 'kurt-geiger-london-shoulder-bags',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/sneakers?id=1308697',
            "category": 'kurt-geiger-london-sneakers',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-totes': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/totes?id=1308603',
            "category": 'kurt-geiger-london-totes',
            "department": 'kurt-geiger-london',
        },
        'kurt-geiger-london-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/kurt-geiger-london/womens-shoes?id=1268704',
            "category": 'kurt-geiger-london-womens-shoes',
            "department": 'kurt-geiger-london',
        },
    },
    'la-bonne-brosse': {
        'la-bonne-brosse': {
            "url": 'https://www.bloomingdales.com/shop/la-bonne-brosse?id=1317514',
            "category": 'la-bonne-brosse',
            "department": 'la-bonne-brosse',
        },
    },
    'la-mer': {
        'la-mer-cleansers': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/cleansers?id=1311098',
            "category": 'la-mer-cleansers',
            "department": 'la-mer',
        },
        'la-mer-eye-treatments': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/eye-treatments?id=1311097',
            "category": 'la-mer-eye-treatments',
            "department": 'la-mer',
        },
        'la-mer-genaissance-de-la-mer': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/genaissance-de-la-mer?id=1315196',
            "category": 'la-mer-genaissance-de-la-mer',
            "department": 'la-mer',
        },
        'la-mer-la-mer-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/la-mer-bath-body?id=1176360',
            "category": 'la-mer-la-mer-bath-body',
            "department": 'la-mer',
        },
        'la-mer-la-mer-body-care': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/la-mer-body-care?id=17953',
            "category": 'la-mer-la-mer-body-care',
            "department": 'la-mer',
        },
        'la-mer-la-mer-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/la-mer-gift-sets?id=1176361',
            "category": 'la-mer-la-mer-gift-sets',
            "department": 'la-mer',
        },
        'la-mer-la-mer-makeup': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/la-mer-makeup?id=1176362',
            "category": 'la-mer-la-mer-makeup',
            "department": 'la-mer',
        },
        'la-mer-la-mer-masks': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/la-mer-masks?id=1003081',
            "category": 'la-mer-la-mer-masks',
            "department": 'la-mer',
        },
        'la-mer-la-mer-skincare': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/la-mer-skincare?id=1176359',
            "category": 'la-mer-la-mer-skincare',
            "department": 'la-mer',
        },
        'la-mer-moisturizers': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/moisturizers?id=1311095',
            "category": 'la-mer-moisturizers',
            "department": 'la-mer',
        },
        'la-mer-serums-and-toners': {
            "url": 'https://www.bloomingdales.com/shop/la-mer/serums-and-toners?id=1311096',
            "category": 'la-mer-serums-and-toners',
            "department": 'la-mer',
        },
    },
    'la-prairie': {
        'la-prairie': {
            "url": 'https://www.bloomingdales.com/shop/la-prairie?id=19382',
            "category": 'la-prairie',
            "department": 'la-prairie',
        },
        'la-prairie-la-prairie-eye-creams-and-treatments': {
            "url": 'https://www.bloomingdales.com/shop/la-prairie/la-prairie-eye-creams-and-treatments?id=1323922',
            "category": 'la-prairie-la-prairie-eye-creams-and-treatments',
            "department": 'la-prairie',
        },
        'la-prairie-la-prairie-skin-caviar': {
            "url": 'https://www.bloomingdales.com/shop/la-prairie/la-prairie-skin-caviar?id=1323920',
            "category": 'la-prairie-la-prairie-skin-caviar',
            "department": 'la-prairie',
        },
        'la-prairie-la-prairie-skincare': {
            "url": 'https://www.bloomingdales.com/shop/la-prairie/la-prairie-skincare?id=1323921',
            "category": 'la-prairie-la-prairie-skincare',
            "department": 'la-prairie',
        },
        'la-prairie-la-prairie-swiss-pristine': {
            "url": 'https://www.bloomingdales.com/shop/la-prairie/la-prairie-swiss-pristine?id=1333797',
            "category": 'la-prairie-la-prairie-swiss-pristine',
            "department": 'la-prairie',
        },
        'la-prairie-la-prairie-white-caviar': {
            "url": 'https://www.bloomingdales.com/shop/la-prairie/la-prairie-white-caviar?id=1323923',
            "category": 'la-prairie-la-prairie-white-caviar',
            "department": 'la-prairie',
        },
    },
    'lafayette-148-new-york': {
        'lafayette-148-new-york': {
            "url": 'https://www.bloomingdales.com/shop/lafayette-148-new-york?id=1004112',
            "category": 'lafayette-148-new-york',
            "department": 'lafayette-148-new-york',
        },
        'lafayette-148-new-york-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/lafayette-148-new-york/womens-clothing?id=1004116',
            "category": 'lafayette-148-new-york-womens-clothing',
            "department": 'lafayette-148-new-york',
        },
    },
    'lagence': {
        'lagence': {
            "url": 'https://www.bloomingdales.com/shop/lagence?id=1195066',
            "category": 'lagence',
            "department": 'lagence',
        },
        'lagence-belts': {
            "url": 'https://www.bloomingdales.com/shop/lagence/belts?id=1326295',
            "category": 'lagence-belts',
            "department": 'lagence',
        },
        'lagence-dresses': {
            "url": 'https://www.bloomingdales.com/shop/lagence/dresses?id=1285413',
            "category": 'lagence-dresses',
            "department": 'lagence',
        },
        'lagence-jeans': {
            "url": 'https://www.bloomingdales.com/shop/lagence/jeans?id=1285412',
            "category": 'lagence-jeans',
            "department": 'lagence',
        },
        'lagence-sale': {
            "url": 'https://www.bloomingdales.com/shop/lagence/sale?id=1316795',
            "category": 'lagence-sale',
            "department": 'lagence',
        },
        'lagence-shoes': {
            "url": 'https://www.bloomingdales.com/shop/lagence/shoes?id=1294195',
            "category": 'lagence-shoes',
            "department": 'lagence',
        },
        'lagence-swim': {
            "url": 'https://www.bloomingdales.com/shop/lagence/swim?id=1305798',
            "category": 'lagence-swim',
            "department": 'lagence',
        },
    },
    'lagos': {
        'lagos': {
            "url": 'https://www.bloomingdales.com/shop/lagos?id=1003783',
            "category": 'lagos',
            "department": 'lagos',
        },
        'lagos-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/lagos/bracelets?id=1005885',
            "category": 'lagos-bracelets',
            "department": 'lagos',
        },
        'lagos-earrings': {
            "url": 'https://www.bloomingdales.com/shop/lagos/earrings?id=1005886',
            "category": 'lagos-earrings',
            "department": 'lagos',
        },
        'lagos-gold': {
            "url": 'https://www.bloomingdales.com/shop/lagos/gold?id=1252615',
            "category": 'lagos-gold',
            "department": 'lagos',
        },
        'lagos-men': {
            "url": 'https://www.bloomingdales.com/shop/lagos/men?id=1220960',
            "category": 'lagos-men',
            "department": 'lagos',
        },
        'lagos-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/lagos/necklaces?id=1005887',
            "category": 'lagos-necklaces',
            "department": 'lagos',
        },
        'lagos-rings': {
            "url": 'https://www.bloomingdales.com/shop/lagos/rings?id=1005888',
            "category": 'lagos-rings',
            "department": 'lagos',
        },
    },
    'lana': {
        'lana': {
            "url": 'https://www.bloomingdales.com/shop/lana?id=1303417',
            "category": 'lana',
            "department": 'lana',
        },
    },
    'lancome': {
        'lancome': {
            "url": 'https://www.bloomingdales.com/shop/lancome?id=1198278',
            "category": 'lancome',
            "department": 'lancome',
        },
        'lancome-absolue': {
            "url": 'https://www.bloomingdales.com/shop/lancome/absolue?id=1307020',
            "category": 'lancome-absolue',
            "department": 'lancome',
        },
        'lancome-genifique': {
            "url": 'https://www.bloomingdales.com/shop/lancome/genifique?id=1308099',
            "category": 'lancome-genifique',
            "department": 'lancome',
        },
        'lancome-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/lancome/gift-sets?id=7157',
            "category": 'lancome-gift-sets',
            "department": 'lancome',
        },
        'lancome-idole': {
            "url": 'https://www.bloomingdales.com/shop/lancome/idole?id=1307024',
            "category": 'lancome-idole',
            "department": 'lancome',
        },
        'lancome-la-vie-est-belle': {
            "url": 'https://www.bloomingdales.com/shop/lancome/la-vie-est-belle?id=1307026',
            "category": 'lancome-la-vie-est-belle',
            "department": 'lancome',
        },
        'lancome-lancome-fragrances-perfume': {
            "url": 'https://www.bloomingdales.com/shop/lancome/lancome-fragrances-perfume?id=7192',
            "category": 'lancome-lancome-fragrances-perfume',
            "department": 'lancome',
        },
        'lancome-lancome-skin-care': {
            "url": 'https://www.bloomingdales.com/shop/lancome/lancome-skin-care?id=7159',
            "category": 'lancome-lancome-skin-care',
            "department": 'lancome',
        },
        'lancome-makeup': {
            "url": 'https://www.bloomingdales.com/shop/lancome/makeup?id=7177',
            "category": 'lancome-makeup',
            "department": 'lancome',
        },
        'lancome-renergie': {
            "url": 'https://www.bloomingdales.com/shop/lancome/renergie?id=1307018',
            "category": 'lancome-renergie',
            "department": 'lancome',
        },
    },
    'last-chance-to-save-on-juliska-patterns': {
        'last-chance-to-save-on-juliska-patterns': {
            "url": 'https://www.bloomingdales.com/shop/last-chance-to-save-on-juliska-patterns?id=1281296',
            "category": 'last-chance-to-save-on-juliska-patterns',
            "department": 'last-chance-to-save-on-juliska-patterns',
        },
    },
    'le-creuset': {
        'le-creuset': {
            "url": 'https://www.bloomingdales.com/shop/le-creuset?id=1253196',
            "category": 'le-creuset',
            "department": 'le-creuset',
        },
    },
    'le-labo': {
        'le-labo': {
            "url": 'https://www.bloomingdales.com/shop/le-labo?id=1236259',
            "category": 'le-labo',
            "department": 'le-labo',
        },
        'le-labo-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/le-labo/bath-body?id=1236399',
            "category": 'le-labo-bath-body',
            "department": 'le-labo',
        },
        'le-labo-candles': {
            "url": 'https://www.bloomingdales.com/shop/le-labo/candles?id=1236397',
            "category": 'le-labo-candles',
            "department": 'le-labo',
        },
        'le-labo-grooming': {
            "url": 'https://www.bloomingdales.com/shop/le-labo/grooming?id=1236400',
            "category": 'le-labo-grooming',
            "department": 'le-labo',
        },
        'le-labo-santal': {
            "url": 'https://www.bloomingdales.com/shop/le-labo/santal?id=1251898',
            "category": 'le-labo-santal',
            "department": 'le-labo',
        },
    },
    'legacy-handbags': {
        'legacy-handbags': {
            "url": 'https://www.bloomingdales.com/shop/legacy-handbags?id=1000355',
            "category": 'legacy-handbags',
            "department": 'legacy-handbags',
        },
    },
    'legacy-weekend': {
        'legacy-weekend': {
            "url": 'https://www.bloomingdales.com/shop/legacy-weekend?id=1001208',
            "category": 'legacy-weekend',
            "department": 'legacy-weekend',
        },
    },
    'lingerie-bras-panties': {
        'lingerie-bras-panties': {
            "url": 'https://www.bloomingdales.com/shop/lingerie-bras-panties?id=1267472',
            "category": 'lingerie-bras-panties',
            "department": 'lingerie-bras-panties',
        },
    },
    'lobjet': {
        'lobjet': {
            "url": 'https://www.bloomingdales.com/shop/lobjet?id=1307495',
            "category": 'lobjet',
            "department": 'lobjet',
        },
    },
    'loeffler-randall': {
        'loeffler-randall': {
            "url": 'https://www.bloomingdales.com/shop/loeffler-randall?id=1265612',
            "category": 'loeffler-randall',
            "department": 'loeffler-randall',
        },
        'loeffler-randall-handbags': {
            "url": 'https://www.bloomingdales.com/shop/loeffler-randall/handbags?id=1265613',
            "category": 'loeffler-randall-handbags',
            "department": 'loeffler-randall',
        },
        'loeffler-randall-shoes': {
            "url": 'https://www.bloomingdales.com/shop/loeffler-randall/shoes?id=1265611',
            "category": 'loeffler-randall-shoes',
            "department": 'loeffler-randall',
        },
    },
    'loewe': {
        'loewe': {
            "url": 'https://www.bloomingdales.com/shop/loewe?id=1325223',
            "category": 'loewe',
            "department": 'loewe',
        },
        'loewe-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/loewe/bath-body?id=1325224',
            "category": 'loewe-bath-body',
            "department": 'loewe',
        },
        'loewe-candles-home-scents': {
            "url": 'https://www.bloomingdales.com/shop/loewe/candles-home-scents?id=1325227',
            "category": 'loewe-candles-home-scents',
            "department": 'loewe',
        },
        'loewe-eyewear': {
            "url": 'https://www.bloomingdales.com/shop/loewe/eyewear?id=1325226',
            "category": 'loewe-eyewear',
            "department": 'loewe',
        },
        'loewe-perfume': {
            "url": 'https://www.bloomingdales.com/shop/loewe/perfume?id=1325228',
            "category": 'loewe-perfume',
            "department": 'loewe',
        },
    },
    'loewe-perfumes': {
        'loewe-perfumes': {
            "url": 'https://www.bloomingdales.com/shop/loewe-perfumes?id=1322218',
            "category": 'loewe-perfumes',
            "department": 'loewe-perfumes',
        },
        'loewe-perfumes-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/loewe-perfumes/bath-body?id=1322226',
            "category": 'loewe-perfumes-bath-body',
            "department": 'loewe-perfumes',
        },
        'loewe-perfumes-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/loewe-perfumes/best-sellers?id=1326912',
            "category": 'loewe-perfumes-best-sellers',
            "department": 'loewe-perfumes',
        },
        'loewe-perfumes-candles': {
            "url": 'https://www.bloomingdales.com/shop/loewe-perfumes/candles?id=1322225',
            "category": 'loewe-perfumes-candles',
            "department": 'loewe-perfumes',
        },
        'loewe-perfumes-cologne': {
            "url": 'https://www.bloomingdales.com/shop/loewe-perfumes/cologne?id=1322224',
            "category": 'loewe-perfumes-cologne',
            "department": 'loewe-perfumes',
        },
        'loewe-perfumes-home-scents': {
            "url": 'https://www.bloomingdales.com/shop/loewe-perfumes/home-scents?id=1324099',
            "category": 'loewe-perfumes-home-scents',
            "department": 'loewe-perfumes',
        },
        'loewe-perfumes-perfume': {
            "url": 'https://www.bloomingdales.com/shop/loewe-perfumes/perfume?id=1322219',
            "category": 'loewe-perfumes-perfume',
            "department": 'loewe-perfumes',
        },
    },
    'longchamp': {
        'longchamp': {
            "url": 'https://www.bloomingdales.com/shop/longchamp?id=1003784',
            "category": 'longchamp',
            "department": 'longchamp',
        },
        'longchamp-handbags': {
            "url": 'https://www.bloomingdales.com/shop/longchamp/handbags?id=1053559',
            "category": 'longchamp-handbags',
            "department": 'longchamp',
        },
        'longchamp-longchamp-le-pliage': {
            "url": 'https://www.bloomingdales.com/shop/longchamp/longchamp-le-pliage?id=1306003',
            "category": 'longchamp-longchamp-le-pliage',
            "department": 'longchamp',
        },
    },
    'longines': {
        'longines': {
            "url": 'https://www.bloomingdales.com/shop/longines?id=1295396',
            "category": 'longines',
            "department": 'longines',
        },
    },
    'louis-vuitton': {
        'louis-vuitton': {
            "url": 'https://www.bloomingdales.com/shop/louis-vuitton?id=1006785',
            "category": 'louis-vuitton',
            "department": 'louis-vuitton',
        },
    },
    'love-is': {
        'love-is': {
            "url": 'https://www.bloomingdales.com/shop/love-is?id=1066259',
            "category": 'love-is',
            "department": 'love-is',
        },
    },
    'loveshackfancy': {
        'loveshackfancy': {
            "url": 'https://www.bloomingdales.com/shop/loveshackfancy?id=1316296',
            "category": 'loveshackfancy',
            "department": 'loveshackfancy',
        },
        'loveshackfancy-home': {
            "url": 'https://www.bloomingdales.com/shop/loveshackfancy/home?id=1316299',
            "category": 'loveshackfancy-home',
            "department": 'loveshackfancy',
        },
        'loveshackfancy-hunter-x-loveshackfancy': {
            "url": 'https://www.bloomingdales.com/shop/loveshackfancy/hunter-x-loveshackfancy?id=1326195',
            "category": 'loveshackfancy-hunter-x-loveshackfancy',
            "department": 'loveshackfancy',
        },
        'loveshackfancy-kids': {
            "url": 'https://www.bloomingdales.com/shop/loveshackfancy/kids?id=1316298',
            "category": 'loveshackfancy-kids',
            "department": 'loveshackfancy',
        },
        'loveshackfancy-womens': {
            "url": 'https://www.bloomingdales.com/shop/loveshackfancy/womens?id=1316297',
            "category": 'loveshackfancy-womens',
            "department": 'loveshackfancy',
        },
    },
    'luxe-totes': {
        'luxe-totes': {
            "url": 'https://www.bloomingdales.com/shop/luxe-totes?id=1135062',
            "category": 'luxe-totes',
            "department": 'luxe-totes',
        },
    },
    'luxury-duffle-bags': {
        'luxury-duffle-bags': {
            "url": 'https://www.bloomingdales.com/shop/luxury-duffle-bags?id=1000315',
            "category": 'luxury-duffle-bags',
            "department": 'luxury-duffle-bags',
        },
    },
    'luxury-furniture-mattresses': {
        'luxury-furniture-mattresses': {
            "url": 'https://www.bloomingdales.com/shop/luxury-furniture-mattresses?id=1006716',
            "category": 'luxury-furniture-mattresses',
            "department": 'luxury-furniture-mattresses',
        },
    },
    'luxury-handbags-premium-designers': {
        'luxury-handbags-premium-designers': {
            "url": 'https://www.bloomingdales.com/shop/luxury-handbags-premium-designers?id=1104604',
            "category": 'luxury-handbags-premium-designers',
            "department": 'luxury-handbags-premium-designers',
        },
    },
    'luxury-home': {
        'luxury-home-luxury-linens-bedspreads': {
            "url": 'https://www.bloomingdales.com/shop/luxury-home/luxury-linens-bedspreads?id=1006909',
            "category": 'luxury-home-luxury-linens-bedspreads',
            "department": 'luxury-home',
        },
    },
    'luxury-home-fragrances-candles-diffusers': {
        'luxury-home-fragrances-candles-diffusers': {
            "url": 'https://www.bloomingdales.com/shop/luxury-home-fragrances-candles-diffusers?id=1151564',
            "category": 'luxury-home-fragrances-candles-diffusers',
            "department": 'luxury-home-fragrances-candles-diffusers',
        },
        'luxury-home-fragrances-candles-diffusers-candle-gift-sets-collections': {
            "url": 'https://www.bloomingdales.com/shop/luxury-home-fragrances-candles-diffusers/candle-gift-sets-collections?id=1151565',
            "category": 'luxury-home-fragrances-candles-diffusers-candle-gift-sets-collections',
            "department": 'luxury-home-fragrances-candles-diffusers',
        },
        'luxury-home-fragrances-candles-diffusers-luxury-candles': {
            "url": 'https://www.bloomingdales.com/shop/luxury-home-fragrances-candles-diffusers/luxury-candles?id=1151566',
            "category": 'luxury-home-fragrances-candles-diffusers-luxury-candles',
            "department": 'luxury-home-fragrances-candles-diffusers',
        },
        'luxury-home-fragrances-candles-diffusers-luxury-room-oil-diffusers-home-scents': {
            "url": 'https://www.bloomingdales.com/shop/luxury-home-fragrances-candles-diffusers/luxury-room-oil-diffusers-home-scents?id=1151567',
            "category": 'luxury-home-fragrances-candles-diffusers-luxury-room-oil-diffusers-home-scents',
            "department": 'luxury-home-fragrances-candles-diffusers',
        },
        'luxury-home-fragrances-candles-diffusers-modern-candle-holders-candlesticks': {
            "url": 'https://www.bloomingdales.com/shop/luxury-home-fragrances-candles-diffusers/modern-candle-holders-candlesticks?id=1151569',
            "category": 'luxury-home-fragrances-candles-diffusers-modern-candle-holders-candlesticks',
            "department": 'luxury-home-fragrances-candles-diffusers',
        },
        'luxury-home-fragrances-candles-diffusers-votive-candle-holders': {
            "url": 'https://www.bloomingdales.com/shop/luxury-home-fragrances-candles-diffusers/votive-candle-holders?id=1151568',
            "category": 'luxury-home-fragrances-candles-diffusers-votive-candle-holders',
            "department": 'luxury-home-fragrances-candles-diffusers',
        },
    },
    'mac-makeup-cosmetics': {
        'mac-makeup-cosmetics': {
            "url": 'https://www.bloomingdales.com/shop/mac-makeup-cosmetics?id=17745',
            "category": 'mac-makeup-cosmetics',
            "department": 'mac-makeup-cosmetics',
        },
        'mac-makeup-cosmetics-mac-eye-makeup': {
            "url": 'https://www.bloomingdales.com/shop/mac-makeup-cosmetics/mac-eye-makeup?id=17746',
            "category": 'mac-makeup-cosmetics-mac-eye-makeup',
            "department": 'mac-makeup-cosmetics',
        },
        'mac-makeup-cosmetics-mac-face-makeup': {
            "url": 'https://www.bloomingdales.com/shop/mac-makeup-cosmetics/mac-face-makeup?id=17759',
            "category": 'mac-makeup-cosmetics-mac-face-makeup',
            "department": 'mac-makeup-cosmetics',
        },
        'mac-makeup-cosmetics-mac-lip-makeup': {
            "url": 'https://www.bloomingdales.com/shop/mac-makeup-cosmetics/mac-lip-makeup?id=17753',
            "category": 'mac-makeup-cosmetics-mac-lip-makeup',
            "department": 'mac-makeup-cosmetics',
        },
    },
    'mackenzie-childs': {
        'mackenzie-childs': {
            "url": 'https://www.bloomingdales.com/shop/mackenzie-childs?id=1224859',
            "category": 'mackenzie-childs',
            "department": 'mackenzie-childs',
        },
        'mackenzie-childs-the-canister-collective': {
            "url": 'https://www.bloomingdales.com/shop/mackenzie-childs/the-canister-collective?id=1331000',
            "category": 'mackenzie-childs-the-canister-collective',
            "department": 'mackenzie-childs',
        },
    },
    'made-in': {
        'made-in': {
            "url": 'https://www.bloomingdales.com/shop/made-in?id=1263711',
            "category": 'made-in',
            "department": 'made-in',
        },
    },
    'madewell': {
        'madewell': {
            "url": 'https://www.bloomingdales.com/shop/madewell?id=1270402',
            "category": 'madewell',
            "department": 'madewell',
        },
        'madewell-accessories': {
            "url": 'https://www.bloomingdales.com/shop/madewell/accessories?id=1270404',
            "category": 'madewell-accessories',
            "department": 'madewell',
        },
        'madewell-handbags': {
            "url": 'https://www.bloomingdales.com/shop/madewell/handbags?id=1270403',
            "category": 'madewell-handbags',
            "department": 'madewell',
        },
        'madewell-mens': {
            "url": 'https://www.bloomingdales.com/shop/madewell/mens?id=1270405',
            "category": 'madewell-mens',
            "department": 'madewell',
        },
        'madewell-shoes': {
            "url": 'https://www.bloomingdales.com/shop/madewell/shoes?id=1273717',
            "category": 'madewell-shoes',
            "department": 'madewell',
        },
    },
    'maison-de-sabre': {
        'maison-de-sabre': {
            "url": 'https://www.bloomingdales.com/shop/maison-de-sabre?id=1271796',
            "category": 'maison-de-sabre',
            "department": 'maison-de-sabre',
        },
    },
    'maison-francis-kurkdjian': {
        'maison-francis-kurkdjian': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian?id=1181959',
            "category": 'maison-francis-kurkdjian',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-724': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/724?id=1319102',
            "category": 'maison-francis-kurkdjian-724',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-a-la-rose': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/a-la-rose?id=1319104',
            "category": 'maison-francis-kurkdjian-a-la-rose',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-baccarat-rouge-540': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/baccarat-rouge-540?id=1251895',
            "category": 'maison-francis-kurkdjian-baccarat-rouge-540',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/bath-body?id=1210670',
            "category": 'maison-francis-kurkdjian-bath-body',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/best-sellers?id=1307897',
            "category": 'maison-francis-kurkdjian-best-sellers',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-candles': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/candles?id=1210671',
            "category": 'maison-francis-kurkdjian-candles',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/fragrance?id=1287722',
            "category": 'maison-francis-kurkdjian-fragrance',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/gift-sets?id=1210364',
            "category": 'maison-francis-kurkdjian-gift-sets',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-kurky': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/kurky?id=1308395',
            "category": 'maison-francis-kurkdjian-kurky',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-mens-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/mens-fragrance?id=1181960',
            "category": 'maison-francis-kurkdjian-mens-fragrance',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-oud': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/oud?id=1319101',
            "category": 'maison-francis-kurkdjian-oud',
            "department": 'maison-francis-kurkdjian',
        },
        'maison-francis-kurkdjian-womens-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/maison-francis-kurkdjian/womens-fragrance?id=1181961',
            "category": 'maison-francis-kurkdjian-womens-fragrance',
            "department": 'maison-francis-kurkdjian',
        },
    },
    'makeup': {
        'makeup-all-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup/all-makeup?id=1269425',
            "category": 'makeup-all-makeup',
            "department": 'makeup',
        },
        'makeup-eye-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup/eye-makeup?id=1269426',
            "category": 'makeup-eye-makeup',
            "department": 'makeup',
        },
        'makeup-face-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup/face-makeup?id=1269428',
            "category": 'makeup-face-makeup',
            "department": 'makeup',
        },
        'makeup-lip-makeup': {
            "url": 'https://www.bloomingdales.com/shop/makeup/lip-makeup?id=1269427',
            "category": 'makeup-lip-makeup',
            "department": 'makeup',
        },
    },
    'makeup-beauty-gift-sets': {
        'makeup-beauty-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/makeup-beauty-gift-sets?id=14898',
            "category": 'makeup-beauty-gift-sets',
            "department": 'makeup-beauty-gift-sets',
        },
    },
    'marc-by-marc-jacobs-accessories': {
        'marc-by-marc-jacobs-accessories': {
            "url": 'https://www.bloomingdales.com/shop/marc-by-marc-jacobs-accessories?id=1003308',
            "category": 'marc-by-marc-jacobs-accessories',
            "department": 'marc-by-marc-jacobs-accessories',
        },
    },
    'marc-jacobs': {
        'marc-jacobs': {
            "url": 'https://www.bloomingdales.com/shop/marc-jacobs?id=1002924',
            "category": 'marc-jacobs',
            "department": 'marc-jacobs',
        },
        'marc-jacobs-accessories': {
            "url": 'https://www.bloomingdales.com/shop/marc-jacobs/accessories?id=1003313',
            "category": 'marc-jacobs-accessories',
            "department": 'marc-jacobs',
        },
        'marc-jacobs-marc-by-marc-jacobs-handbags': {
            "url": 'https://www.bloomingdales.com/shop/marc-jacobs/marc-by-marc-jacobs-handbags?id=1002927',
            "category": 'marc-jacobs-marc-by-marc-jacobs-handbags',
            "department": 'marc-jacobs',
        },
        'marc-jacobs-perfume-fragrances-cologne': {
            "url": 'https://www.bloomingdales.com/shop/marc-jacobs/perfume-fragrances-cologne?id=1006921',
            "category": 'marc-jacobs-perfume-fragrances-cologne',
            "department": 'marc-jacobs',
        },
    },
    'marco-bicego': {
        'marco-bicego': {
            "url": 'https://www.bloomingdales.com/shop/marco-bicego?id=1004121',
            "category": 'marco-bicego',
            "department": 'marco-bicego',
        },
        'marco-bicego-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/marco-bicego/bracelets?id=1006761',
            "category": 'marco-bicego-bracelets',
            "department": 'marco-bicego',
        },
        'marco-bicego-earrings': {
            "url": 'https://www.bloomingdales.com/shop/marco-bicego/earrings?id=1006762',
            "category": 'marco-bicego-earrings',
            "department": 'marco-bicego',
        },
        'marco-bicego-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/marco-bicego/necklaces?id=1006763',
            "category": 'marco-bicego-necklaces',
            "department": 'marco-bicego',
        },
        'marco-bicego-rings': {
            "url": 'https://www.bloomingdales.com/shop/marco-bicego/rings?id=1006764',
            "category": 'marco-bicego-rings',
            "department": 'marco-bicego',
        },
    },
    'marketplace': {
        'marketplace': {
            "url": 'https://www.bloomingdales.com/shop/marketplace?id=1245995',
            "category": 'marketplace',
            "department": 'marketplace',
        },
    },
    'master-copper-core': {
        'master-copper-core': {
            "url": 'https://www.bloomingdales.com/shop/master-copper-core?id=1017462',
            "category": 'master-copper-core',
            "department": 'master-copper-core',
        },
    },
    'match': {
        'match': {
            "url": 'https://www.bloomingdales.com/shop/match?id=1240159',
            "category": 'match',
            "department": 'match',
        },
    },
    'matching-sets': {
        'matching-sets': {
            "url": 'https://www.bloomingdales.com/shop/matching-sets?id=1039386',
            "category": 'matching-sets',
            "department": 'matching-sets',
        },
    },
    'matouk': {
        'matouk': {
            "url": 'https://www.bloomingdales.com/shop/matouk?id=1166770',
            "category": 'matouk',
            "department": 'matouk',
        },
        'matouk-bath': {
            "url": 'https://www.bloomingdales.com/shop/matouk/bath?id=1166774',
            "category": 'matouk-bath',
            "department": 'matouk',
        },
        'matouk-bedding': {
            "url": 'https://www.bloomingdales.com/shop/matouk/bedding?id=1166771',
            "category": 'matouk-bedding',
            "department": 'matouk',
        },
        'matouk-pillows-comforters': {
            "url": 'https://www.bloomingdales.com/shop/matouk/pillows-comforters?id=1166778',
            "category": 'matouk-pillows-comforters',
            "department": 'matouk',
        },
    },
    'maurizio-baldassari': {
        'maurizio-baldassari': {
            "url": 'https://www.bloomingdales.com/shop/maurizio-baldassari?id=1334100',
            "category": 'maurizio-baldassari',
            "department": 'maurizio-baldassari',
        },
    },
    'mcm': {
        'mcm': {
            "url": 'https://www.bloomingdales.com/shop/mcm?id=1003794',
            "category": 'mcm',
            "department": 'mcm',
        },
        'mcm-mens-handbags-accessories': {
            "url": 'https://www.bloomingdales.com/shop/mcm/mens-handbags-accessories?id=1003798',
            "category": 'mcm-mens-handbags-accessories',
            "department": 'mcm',
        },
        'mcm-womens-handbags-wallets': {
            "url": 'https://www.bloomingdales.com/shop/mcm/womens-handbags-wallets?id=1003796',
            "category": 'mcm-womens-handbags-wallets',
            "department": 'mcm',
        },
    },
    'memo-paris': {
        'memo-paris': {
            "url": 'https://www.bloomingdales.com/shop/memo-paris?id=1283095',
            "category": 'memo-paris',
            "department": 'memo-paris',
        },
    },
    'men': {
        'men': {
            "url": 'https://www.bloomingdales.com/shop/men?id=1006308',
            "category": 'men',
            "department": 'men',
        },
        'men-accessories': {
            "url": 'https://www.bloomingdales.com/shop/men/accessories?id=1123169',
            "category": 'men-accessories',
            "department": 'men',
        },
        'men-clothing': {
            "url": 'https://www.bloomingdales.com/shop/men/clothing?id=1123167',
            "category": 'men-clothing',
            "department": 'men',
        },
        'men-mens-designer-shoes-luxury-shoes': {
            "url": 'https://www.bloomingdales.com/shop/men/mens-designer-shoes-luxury-shoes?id=1123168',
            "category": 'men-mens-designer-shoes-luxury-shoes',
            "department": 'men',
        },
        'mens': {
            "url": 'https://www.bloomingdales.com/shop/mens?id=3864',
            "category": 'mens',
            "department": 'men',
        },
        'mens-active-workout': {
            "url": 'https://www.bloomingdales.com/shop/mens/active-workout?id=1006163',
            "category": 'mens-active-workout',
            "department": 'men',
        },
        'mens-activewear-workout-clothes': {
            "url": 'https://www.bloomingdales.com/shop/mens/activewear-workout-clothes?id=1004734',
            "category": 'mens-activewear-workout-clothes',
            "department": 'men',
        },
        'mens-advanced-contemporary-jeans': {
            "url": 'https://www.bloomingdales.com/shop/mens/advanced-contemporary-jeans?id=1134759',
            "category": 'mens-advanced-contemporary-jeans',
            "department": 'men',
        },
        'mens-all-clothing': {
            "url": 'https://www.bloomingdales.com/shop/mens/all-clothing?id=1005275',
            "category": 'mens-all-clothing',
            "department": 'men',
        },
        'mens-athleisure': {
            "url": 'https://www.bloomingdales.com/shop/mens/athleisure?id=1315898',
            "category": 'mens-athleisure',
            "department": 'men',
        },
        'mens-aviator-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/mens/aviator-sunglasses?id=1006245',
            "category": 'mens-aviator-sunglasses',
            "department": 'men',
        },
        'mens-backpacks': {
            "url": 'https://www.bloomingdales.com/shop/mens/backpacks?id=1006227',
            "category": 'mens-backpacks',
            "department": 'men',
        },
        'mens-baggy-relaxed-fit': {
            "url": 'https://www.bloomingdales.com/shop/mens/baggy-relaxed-fit?id=1250009',
            "category": 'mens-baggy-relaxed-fit',
            "department": 'men',
        },
        'mens-bags-briefcases': {
            "url": 'https://www.bloomingdales.com/shop/mens/bags-briefcases?id=1000059',
            "category": 'mens-bags-briefcases',
            "department": 'men',
        },
        'mens-barn-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/barn-jackets?id=1284108',
            "category": 'mens-barn-jackets',
            "department": 'men',
        },
        'mens-beaded-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/mens/beaded-bracelets?id=1008762',
            "category": 'mens-beaded-bracelets',
            "department": 'men',
        },
        'mens-belt-bags': {
            "url": 'https://www.bloomingdales.com/shop/mens/belt-bags?id=1061859',
            "category": 'mens-belt-bags',
            "department": 'men',
        },
        'mens-best-jeans-for-men': {
            "url": 'https://www.bloomingdales.com/shop/mens/best-jeans-for-men?id=15918',
            "category": 'mens-best-jeans-for-men',
            "department": 'men',
        },
        'mens-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/mens/best-sellers?id=1019059',
            "category": 'mens-best-sellers',
            "department": 'men',
        },
        'mens-bifold-wallets': {
            "url": 'https://www.bloomingdales.com/shop/mens/bifold-wallets?id=1006237',
            "category": 'mens-bifold-wallets',
            "department": 'men',
        },
        'mens-black-jeans': {
            "url": 'https://www.bloomingdales.com/shop/mens/black-jeans?id=1275597',
            "category": 'mens-black-jeans',
            "department": 'men',
        },
        'mens-boat-shoes-slip-ons': {
            "url": 'https://www.bloomingdales.com/shop/mens/boat-shoes-slip-ons?id=1000050',
            "category": 'mens-boat-shoes-slip-ons',
            "department": 'men',
        },
        'mens-bomber-varsity-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/bomber-varsity-jackets?id=1006190',
            "category": 'mens-bomber-varsity-jackets',
            "department": 'men',
        },
        'mens-boots-dress-boots': {
            "url": 'https://www.bloomingdales.com/shop/mens/boots-dress-boots?id=1000046',
            "category": 'mens-boots-dress-boots',
            "department": 'men',
        },
        'mens-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/mens/bracelets?id=1006053',
            "category": 'mens-bracelets',
            "department": 'men',
        },
        'mens-briefcases-portfolios': {
            "url": 'https://www.bloomingdales.com/shop/mens/briefcases-portfolios?id=1006235',
            "category": 'mens-briefcases-portfolios',
            "department": 'men',
        },
        'mens-canali': {
            "url": 'https://www.bloomingdales.com/shop/mens/canali?id=1005311',
            "category": 'mens-canali',
            "department": 'men',
        },
        'mens-cardigans': {
            "url": 'https://www.bloomingdales.com/shop/mens/cardigans?id=1006184',
            "category": 'mens-cardigans',
            "department": 'men',
        },
        'mens-cashmere': {
            "url": 'https://www.bloomingdales.com/shop/mens/cashmere?id=1244895',
            "category": 'mens-cashmere',
            "department": 'men',
        },
        'mens-casual-dress-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/mens/casual-dress-sneakers?id=1006010',
            "category": 'mens-casual-dress-sneakers',
            "department": 'men',
        },
        'mens-casual-pants': {
            "url": 'https://www.bloomingdales.com/shop/mens/casual-pants?id=1006168',
            "category": 'mens-casual-pants',
            "department": 'men',
        },
        'mens-casual-sport-coats': {
            "url": 'https://www.bloomingdales.com/shop/mens/casual-sport-coats?id=1238365',
            "category": 'mens-casual-sport-coats',
            "department": 'men',
        },
        'mens-chinos': {
            "url": 'https://www.bloomingdales.com/shop/mens/chinos?id=1144160',
            "category": 'mens-chinos',
            "department": 'men',
        },
        'mens-chronograph-swiss-watches': {
            "url": 'https://www.bloomingdales.com/shop/mens/chronograph-swiss-watches?id=1006084',
            "category": 'mens-chronograph-swiss-watches',
            "department": 'men',
        },
        'mens-classic-polos': {
            "url": 'https://www.bloomingdales.com/shop/mens/classic-polos?id=1225773',
            "category": 'mens-classic-polos',
            "department": 'men',
        },
        'mens-clogs-mules': {
            "url": 'https://www.bloomingdales.com/shop/mens/clogs-mules?id=1175259',
            "category": 'mens-clogs-mules',
            "department": 'men',
        },
        'mens-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/coats-jackets?id=11548',
            "category": 'mens-coats-jackets',
            "department": 'men',
        },
        'mens-coats-under-250': {
            "url": 'https://www.bloomingdales.com/shop/mens/coats-under-250?id=1005052',
            "category": 'mens-coats-under-250',
            "department": 'men',
        },
        'mens-cuff-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/mens/cuff-bracelets?id=1008763',
            "category": 'mens-cuff-bracelets',
            "department": 'men',
        },
        'mens-cufflinks': {
            "url": 'https://www.bloomingdales.com/shop/mens/cufflinks?id=1005316',
            "category": 'mens-cufflinks',
            "department": 'men',
        },
        'mens-designer-belts': {
            "url": 'https://www.bloomingdales.com/shop/mens/designer-belts?id=1000060',
            "category": 'mens-designer-belts',
            "department": 'men',
        },
        'mens-designer-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens/designer-shoes?id=1000055',
            "category": 'mens-designer-shoes',
            "department": 'men',
        },
        'mens-drawstring': {
            "url": 'https://www.bloomingdales.com/shop/mens/drawstring?id=1144159',
            "category": 'mens-drawstring',
            "department": 'men',
        },
        'mens-dress-pants': {
            "url": 'https://www.bloomingdales.com/shop/mens/dress-pants?id=1006177',
            "category": 'mens-dress-pants',
            "department": 'men',
        },
        'mens-dress-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/dress-shirts?id=17647',
            "category": 'mens-dress-shirts',
            "department": 'men',
        },
        'mens-dress-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens/dress-shoes?id=1001183',
            "category": 'mens-dress-shoes',
            "department": 'men',
        },
        'mens-dress-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/mens/dress-sneakers?id=1209059',
            "category": 'mens-dress-sneakers',
            "department": 'men',
        },
        'mens-dress-socks': {
            "url": 'https://www.bloomingdales.com/shop/mens/dress-socks?id=1003733',
            "category": 'mens-dress-socks',
            "department": 'men',
        },
        'mens-duffel-weekender-bags': {
            "url": 'https://www.bloomingdales.com/shop/mens/duffel-weekender-bags?id=1006238',
            "category": 'mens-duffel-weekender-bags',
            "department": 'men',
        },
        'mens-fall-essentials': {
            "url": 'https://www.bloomingdales.com/shop/mens/fall-essentials?id=1284109',
            "category": 'mens-fall-essentials',
            "department": 'men',
        },
        'mens-fall-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/fall-jackets?id=1211571',
            "category": 'mens-fall-jackets',
            "department": 'men',
        },
        'mens-gloves': {
            "url": 'https://www.bloomingdales.com/shop/mens/gloves?id=1006242',
            "category": 'mens-gloves',
            "department": 'men',
        },
        'mens-gq-x-bloomingdales-fit-tips': {
            "url": 'https://www.bloomingdales.com/shop/mens/gq-x-bloomingdales-fit-tips?id=1006278',
            "category": 'mens-gq-x-bloomingdales-fit-tips',
            "department": 'men',
        },
        'mens-gym-running-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens/gym-running-shoes?id=1006009',
            "category": 'mens-gym-running-shoes',
            "department": 'men',
        },
        'mens-gym-training': {
            "url": 'https://www.bloomingdales.com/shop/mens/gym-training?id=1315897',
            "category": 'mens-gym-training',
            "department": 'men',
        },
        'mens-hart-schaffner-marx': {
            "url": 'https://www.bloomingdales.com/shop/mens/hart-schaffner-marx?id=1005310',
            "category": 'mens-hart-schaffner-marx',
            "department": 'men',
        },
        'mens-hats-beanies': {
            "url": 'https://www.bloomingdales.com/shop/mens/hats-beanies?id=1006243',
            "category": 'mens-hats-beanies',
            "department": 'men',
        },
        'mens-hats-gloves-scarves': {
            "url": 'https://www.bloomingdales.com/shop/mens/hats-gloves-scarves?id=1000062',
            "category": 'mens-hats-gloves-scarves',
            "department": 'men',
        },
        'mens-hiking': {
            "url": 'https://www.bloomingdales.com/shop/mens/hiking?id=1316696',
            "category": 'mens-hiking',
            "department": 'men',
        },
        'mens-hoodies-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/hoodies-sweatshirts?id=1003569',
            "category": 'mens-hoodies-sweatshirts',
            "department": 'men',
        },
        'mens-jewelry-cufflinks': {
            "url": 'https://www.bloomingdales.com/shop/mens/jewelry-cufflinks?id=1000061',
            "category": 'mens-jewelry-cufflinks',
            "department": 'men',
        },
        'mens-knit-polos': {
            "url": 'https://www.bloomingdales.com/shop/mens/knit-polos?id=1211364',
            "category": 'mens-knit-polos',
            "department": 'men',
        },
        'mens-leather-card-cases-holders': {
            "url": 'https://www.bloomingdales.com/shop/mens/leather-card-cases-holders?id=1006239',
            "category": 'mens-leather-card-cases-holders',
            "department": 'men',
        },
        'mens-leather-shearling-suede-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/leather-shearling-suede-jackets?id=1005053',
            "category": 'mens-leather-shearling-suede-jackets',
            "department": 'men',
        },
        'mens-leather-strap-watches': {
            "url": 'https://www.bloomingdales.com/shop/mens/leather-strap-watches?id=1006081',
            "category": 'mens-leather-strap-watches',
            "department": 'men',
        },
        'mens-linen': {
            "url": 'https://www.bloomingdales.com/shop/mens/linen?id=1191070',
            "category": 'mens-linen',
            "department": 'men',
        },
        'mens-linen-suits': {
            "url": 'https://www.bloomingdales.com/shop/mens/linen-suits?id=1304399',
            "category": 'mens-linen-suits',
            "department": 'men',
        },
        'mens-loafers': {
            "url": 'https://www.bloomingdales.com/shop/mens/loafers?id=1211085',
            "category": 'mens-loafers',
            "department": 'men',
        },
        'mens-long-sleeve-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/long-sleeve-shirts?id=1026160',
            "category": 'mens-long-sleeve-shirts',
            "department": 'men',
        },
        'mens-long-sleeve-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/long-sleeve-t-shirts?id=1006188',
            "category": 'mens-long-sleeve-t-shirts',
            "department": 'men',
        },
        'mens-low-profile-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/mens/low-profile-sneakers?id=1301206',
            "category": 'mens-low-profile-sneakers',
            "department": 'men',
        },
        'mens-low-top-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens/low-top-shoes?id=1006011',
            "category": 'mens-low-top-shoes',
            "department": 'men',
        },
        'mens-luxury-underwear-socks-for-men': {
            "url": 'https://www.bloomingdales.com/shop/mens/luxury-underwear-socks-for-men?id=1140959',
            "category": 'mens-luxury-underwear-socks-for-men',
            "department": 'men',
        },
        'mens-luxury-watches': {
            "url": 'https://www.bloomingdales.com/shop/mens/luxury-watches?id=1006078',
            "category": 'mens-luxury-watches',
            "department": 'men',
        },
        'mens-mens-active-workout-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-active-workout-bottoms?id=1294000',
            "category": 'mens-mens-active-workout-bottoms',
            "department": 'men',
        },
        'mens-mens-active-workout-tops': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-active-workout-tops?id=1294001',
            "category": 'mens-mens-active-workout-tops',
            "department": 'men',
        },
        'mens-mens-athletic-shorts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-athletic-shorts?id=1292943',
            "category": 'mens-mens-athletic-shorts',
            "department": 'men',
        },
        'mens-mens-boat-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-boat-shoes?id=1293898',
            "category": 'mens-mens-boat-shoes',
            "department": 'men',
        },
        'mens-mens-bomber-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-bomber-jackets?id=1293100',
            "category": 'mens-mens-bomber-jackets',
            "department": 'men',
        },
        'mens-mens-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-bottoms?id=1292440',
            "category": 'mens-mens-bottoms',
            "department": 'men',
        },
        'mens-mens-camp-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-camp-shirts?id=1292883',
            "category": 'mens-mens-camp-shirts',
            "department": 'men',
        },
        'mens-mens-cargo-pants': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-cargo-pants?id=1292909',
            "category": 'mens-mens-cargo-pants',
            "department": 'men',
        },
        'mens-mens-cashmere-coats': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-cashmere-coats?id=1293096',
            "category": 'mens-mens-cashmere-coats',
            "department": 'men',
        },
        'mens-mens-casual-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-casual-shirts?id=17648',
            "category": 'mens-mens-casual-shirts',
            "department": 'men',
        },
        'mens-mens-crewneck-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-crewneck-sweaters?id=1292901',
            "category": 'mens-mens-crewneck-sweaters',
            "department": 'men',
        },
        'mens-mens-designer-loafers': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-designer-loafers?id=1293899',
            "category": 'mens-mens-designer-loafers',
            "department": 'men',
        },
        'mens-mens-flannel-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-flannel-shirts?id=1292841',
            "category": 'mens-mens-flannel-shirts',
            "department": 'men',
        },
        'mens-mens-golf-pants': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-golf-pants?id=1292910',
            "category": 'mens-mens-golf-pants',
            "department": 'men',
        },
        'mens-mens-golf-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-golf-shirts?id=1292879',
            "category": 'mens-mens-golf-shirts',
            "department": 'men',
        },
        'mens-mens-graphic-tees': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-graphic-tees?id=1292898',
            "category": 'mens-mens-graphic-tees',
            "department": 'men',
        },
        'mens-mens-henley-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-henley-shirts?id=1292888',
            "category": 'mens-mens-henley-shirts',
            "department": 'men',
        },
        'mens-mens-hoodies': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-hoodies?id=1292906',
            "category": 'mens-mens-hoodies',
            "department": 'men',
        },
        'mens-mens-jeans-under-100': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-jeans-under-100?id=1071160',
            "category": 'mens-mens-jeans-under-100',
            "department": 'men',
        },
        'mens-mens-joggers': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-joggers?id=1292912',
            "category": 'mens-mens-joggers',
            "department": 'men',
        },
        'mens-mens-leather-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-leather-jackets?id=1293098',
            "category": 'mens-mens-leather-jackets',
            "department": 'men',
        },
        'mens-mens-long-sleeve-polos': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-long-sleeve-polos?id=1292899',
            "category": 'mens-mens-long-sleeve-polos',
            "department": 'men',
        },
        'mens-mens-messenger-bags': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-messenger-bags?id=1293107',
            "category": 'mens-mens-messenger-bags',
            "department": 'men',
        },
        'mens-mens-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-pajamas?id=1293105',
            "category": 'mens-mens-pajamas',
            "department": 'men',
        },
        'mens-mens-robes': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-robes?id=1293106',
            "category": 'mens-mens-robes',
            "department": 'men',
        },
        'mens-mens-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-shirts?id=1292443',
            "category": 'mens-mens-shirts',
            "department": 'men',
        },
        'mens-mens-shirts-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-shirts-sweaters?id=1292439',
            "category": 'mens-mens-shirts-sweaters',
            "department": 'men',
        },
        'mens-mens-sleep-loungewear': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-sleep-loungewear?id=1004554',
            "category": 'mens-mens-sleep-loungewear',
            "department": 'men',
        },
        'mens-mens-sport-coats-blazers': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-sport-coats-blazers?id=1000074',
            "category": 'mens-mens-sport-coats-blazers',
            "department": 'men',
        },
        'mens-mens-suede-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-suede-jackets?id=1293099',
            "category": 'mens-mens-suede-jackets',
            "department": 'men',
        },
        'mens-mens-suiting': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-suiting?id=1292442',
            "category": 'mens-mens-suiting',
            "department": 'men',
        },
        'mens-mens-sweatpants': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-sweatpants?id=1292911',
            "category": 'mens-mens-sweatpants',
            "department": 'men',
        },
        'mens-mens-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-sweatshirts?id=1292907',
            "category": 'mens-mens-sweatshirts',
            "department": 'men',
        },
        'mens-mens-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-t-shirts?id=11536',
            "category": 'mens-mens-t-shirts',
            "department": 'men',
        },
        'mens-mens-varsity-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-varsity-jackets?id=1293101',
            "category": 'mens-mens-varsity-jackets',
            "department": 'men',
        },
        'mens-mens-wool-coats': {
            "url": 'https://www.bloomingdales.com/shop/mens/mens-wool-coats?id=1293097',
            "category": 'mens-mens-wool-coats',
            "department": 'men',
        },
        'mens-messenger-tote-bags': {
            "url": 'https://www.bloomingdales.com/shop/mens/messenger-tote-bags?id=1006240',
            "category": 'mens-messenger-tote-bags',
            "department": 'men',
        },
        'mens-money-clips': {
            "url": 'https://www.bloomingdales.com/shop/mens/money-clips?id=1006241',
            "category": 'mens-money-clips',
            "department": 'men',
        },
        'mens-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/mens/necklaces?id=1006054',
            "category": 'mens-necklaces',
            "department": 'men',
        },
        'mens-necklaces-chains': {
            "url": 'https://www.bloomingdales.com/shop/mens/necklaces-chains?id=1008760',
            "category": 'mens-necklaces-chains',
            "department": 'men',
        },
        'mens-non-iron-dress-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/non-iron-dress-shirts?id=1004733',
            "category": 'mens-non-iron-dress-shirts',
            "department": 'men',
        },
        'mens-overcoats-peacoats': {
            "url": 'https://www.bloomingdales.com/shop/mens/overcoats-peacoats?id=1211363',
            "category": 'mens-overcoats-peacoats',
            "department": 'men',
        },
        'mens-oxfords-derby-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens/oxfords-derby-shoes?id=1055959',
            "category": 'mens-oxfords-derby-shoes',
            "department": 'men',
        },
        'mens-oxfords-derbys': {
            "url": 'https://www.bloomingdales.com/shop/mens/oxfords-derbys?id=1177459',
            "category": 'mens-oxfords-derbys',
            "department": 'men',
        },
        'mens-pants': {
            "url": 'https://www.bloomingdales.com/shop/mens/pants?id=10189',
            "category": 'mens-pants',
            "department": 'men',
        },
        'mens-parkas': {
            "url": 'https://www.bloomingdales.com/shop/mens/parkas?id=1241865',
            "category": 'mens-parkas',
            "department": 'men',
        },
        'mens-pendant': {
            "url": 'https://www.bloomingdales.com/shop/mens/pendant?id=1008761',
            "category": 'mens-pendant',
            "department": 'men',
        },
        'mens-polarized-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/mens/polarized-sunglasses?id=1031759',
            "category": 'mens-polarized-sunglasses',
            "department": 'men',
        },
        'mens-polos-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/polos-shirts?id=1000663',
            "category": 'mens-polos-shirts',
            "department": 'men',
        },
        'mens-prom-suits': {
            "url": 'https://www.bloomingdales.com/shop/mens/prom-suits?id=1305796',
            "category": 'mens-prom-suits',
            "department": 'men',
        },
        'mens-puffers-jackets-quilted': {
            "url": 'https://www.bloomingdales.com/shop/mens/puffers-jackets-quilted?id=1005068',
            "category": 'mens-puffers-jackets-quilted',
            "department": 'men',
        },
        'mens-pullover-sweaters-hoodies': {
            "url": 'https://www.bloomingdales.com/shop/mens/pullover-sweaters-hoodies?id=1006185',
            "category": 'mens-pullover-sweaters-hoodies',
            "department": 'men',
        },
        'mens-quilted-down-vests': {
            "url": 'https://www.bloomingdales.com/shop/mens/quilted-down-vests?id=1006197',
            "category": 'mens-quilted-down-vests',
            "department": 'men',
        },
        'mens-quilted-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/quilted-jackets?id=1005051',
            "category": 'mens-quilted-jackets',
            "department": 'men',
        },
        'mens-rain-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/rain-jackets?id=1241864',
            "category": 'mens-rain-jackets',
            "department": 'men',
        },
        'mens-religious-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/mens/religious-necklaces?id=1008759',
            "category": 'mens-religious-necklaces',
            "department": 'men',
        },
        'mens-rings': {
            "url": 'https://www.bloomingdales.com/shop/mens/rings?id=1006055',
            "category": 'mens-rings',
            "department": 'men',
        },
        'mens-round-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/mens/round-sunglasses?id=1006246',
            "category": 'mens-round-sunglasses',
            "department": 'men',
        },
        'mens-running': {
            "url": 'https://www.bloomingdales.com/shop/mens/running?id=1315896',
            "category": 'mens-running',
            "department": 'men',
        },
        'mens-scarves': {
            "url": 'https://www.bloomingdales.com/shop/mens/scarves?id=1006244',
            "category": 'mens-scarves',
            "department": 'men',
        },
        'mens-shirt-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/shirt-jackets?id=1173059',
            "category": 'mens-shirt-jackets',
            "department": 'men',
        },
        'mens-shoes-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/mens/shoes-best-sellers?id=1245595',
            "category": 'mens-shoes-best-sellers',
            "department": 'men',
        },
        'mens-shoes-under-100': {
            "url": 'https://www.bloomingdales.com/shop/mens/shoes-under-100?id=1004747',
            "category": 'mens-shoes-under-100',
            "department": 'men',
        },
        'mens-shoes-under-250': {
            "url": 'https://www.bloomingdales.com/shop/mens/shoes-under-250?id=1209159',
            "category": 'mens-shoes-under-250',
            "department": 'men',
        },
        'mens-short-sleeve-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/short-sleeve-shirts?id=1026159',
            "category": 'mens-short-sleeve-shirts',
            "department": 'men',
        },
        'mens-short-sleeve-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/short-sleeve-t-shirts?id=1006187',
            "category": 'mens-short-sleeve-t-shirts',
            "department": 'men',
        },
        'mens-shorts': {
            "url": 'https://www.bloomingdales.com/shop/mens/shorts?id=11576',
            "category": 'mens-shorts',
            "department": 'men',
        },
        'mens-skinny-jeans': {
            "url": 'https://www.bloomingdales.com/shop/mens/skinny-jeans?id=1006161',
            "category": 'mens-skinny-jeans',
            "department": 'men',
        },
        'mens-slides': {
            "url": 'https://www.bloomingdales.com/shop/mens/slides?id=1148559',
            "category": 'mens-slides',
            "department": 'men',
        },
        'mens-slim-jeans': {
            "url": 'https://www.bloomingdales.com/shop/mens/slim-jeans?id=1169259',
            "category": 'mens-slim-jeans',
            "department": 'men',
        },
        'mens-slip-on-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/mens/slip-on-sneakers?id=1006012',
            "category": 'mens-slip-on-sneakers',
            "department": 'men',
        },
        'mens-slippers': {
            "url": 'https://www.bloomingdales.com/shop/mens/slippers?id=1000053',
            "category": 'mens-slippers',
            "department": 'men',
        },
        'mens-smart-touch-screen-watches': {
            "url": 'https://www.bloomingdales.com/shop/mens/smart-touch-screen-watches?id=1006083',
            "category": 'mens-smart-touch-screen-watches',
            "department": 'men',
        },
        'mens-sneakers-tennis-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens/sneakers-tennis-shoes?id=1000054',
            "category": 'mens-sneakers-tennis-shoes',
            "department": 'men',
        },
        'mens-spring-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/spring-jackets?id=1224060',
            "category": 'mens-spring-jackets',
            "department": 'men',
        },
        'mens-square-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/mens/square-sunglasses?id=1006247',
            "category": 'mens-square-sunglasses',
            "department": 'men',
        },
        'mens-straight-jeans': {
            "url": 'https://www.bloomingdales.com/shop/mens/straight-jeans?id=1006162',
            "category": 'mens-straight-jeans',
            "department": 'men',
        },
        'mens-suit-separates': {
            "url": 'https://www.bloomingdales.com/shop/mens/suit-separates?id=1029364',
            "category": 'mens-suit-separates',
            "department": 'men',
        },
        'mens-suiting-under-1000': {
            "url": 'https://www.bloomingdales.com/shop/mens/suiting-under-1000?id=1272298',
            "category": 'mens-suiting-under-1000',
            "department": 'men',
        },
        'mens-suits': {
            "url": 'https://www.bloomingdales.com/shop/mens/suits?id=1006182',
            "category": 'mens-suits',
            "department": 'men',
        },
        'mens-suits-suit-separates': {
            "url": 'https://www.bloomingdales.com/shop/mens/suits-suit-separates?id=1003462',
            "category": 'mens-suits-suit-separates',
            "department": 'men',
        },
        'mens-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/mens/sunglasses?id=1000068',
            "category": 'mens-sunglasses',
            "department": 'men',
        },
        'mens-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/mens/sweaters?id=10258',
            "category": 'mens-sweaters',
            "department": 'men',
        },
        'mens-sweatpants-joggers': {
            "url": 'https://www.bloomingdales.com/shop/mens/sweatpants-joggers?id=1006181',
            "category": 'mens-sweatpants-joggers',
            "department": 'men',
        },
        'mens-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/mens/swimwear?id=1003490',
            "category": 'mens-swimwear',
            "department": 'men',
        },
        'mens-tech-accessories-headphones': {
            "url": 'https://www.bloomingdales.com/shop/mens/tech-accessories-headphones?id=1000833',
            "category": 'mens-tech-accessories-headphones',
            "department": 'men',
        },
        'mens-the-streetwear-edit': {
            "url": 'https://www.bloomingdales.com/shop/mens/the-streetwear-edit?id=1245307',
            "category": 'mens-the-streetwear-edit',
            "department": 'men',
        },
        'mens-ties-bow-ties-pocket-squares': {
            "url": 'https://www.bloomingdales.com/shop/mens/ties-bow-ties-pocket-squares?id=1003731',
            "category": 'mens-ties-bow-ties-pocket-squares',
            "department": 'men',
        },
        'mens-trench-coats-raincoats': {
            "url": 'https://www.bloomingdales.com/shop/mens/trench-coats-raincoats?id=1023860',
            "category": 'mens-trench-coats-raincoats',
            "department": 'men',
        },
        'mens-tuxedos-formalwear': {
            "url": 'https://www.bloomingdales.com/shop/mens/tuxedos-formalwear?id=1242606',
            "category": 'mens-tuxedos-formalwear',
            "department": 'men',
        },
        'mens-undershirts': {
            "url": 'https://www.bloomingdales.com/shop/mens/undershirts?id=1006224',
            "category": 'mens-undershirts',
            "department": 'men',
        },
        'mens-underwear-boxers-briefs-trunks': {
            "url": 'https://www.bloomingdales.com/shop/mens/underwear-boxers-briefs-trunks?id=1006225',
            "category": 'mens-underwear-boxers-briefs-trunks',
            "department": 'men',
        },
        'mens-underwear-multipacks': {
            "url": 'https://www.bloomingdales.com/shop/mens/underwear-multipacks?id=1006226',
            "category": 'mens-underwear-multipacks',
            "department": 'men',
        },
        'mens-underwear-undershirts-socks': {
            "url": 'https://www.bloomingdales.com/shop/mens/underwear-undershirts-socks?id=10237',
            "category": 'mens-underwear-undershirts-socks',
            "department": 'men',
        },
        'mens-walking': {
            "url": 'https://www.bloomingdales.com/shop/mens/walking?id=1315895',
            "category": 'mens-walking',
            "department": 'men',
        },
        'mens-wallets-money-clips': {
            "url": 'https://www.bloomingdales.com/shop/mens/wallets-money-clips?id=1000065',
            "category": 'mens-wallets-money-clips',
            "department": 'men',
        },
        'mens-watches-1000066': {
            "url": 'https://www.bloomingdales.com/shop/mens/watches?id=1000066',
            "category": 'mens-watches-1000066',
            "department": 'men',
        },
        'mens-wedding-bands': {
            "url": 'https://www.bloomingdales.com/shop/mens/wedding-bands?id=1322245',
            "category": 'mens-wedding-bands',
            "department": 'men',
        },
        'mens-wide-width-shoes-for-men': {
            "url": 'https://www.bloomingdales.com/shop/mens/wide-width-shoes-for-men?id=1055960',
            "category": 'mens-wide-width-shoes-for-men',
            "department": 'men',
        },
        'mens-windbreakers-lightweight-jackets': {
            "url": 'https://www.bloomingdales.com/shop/mens/windbreakers-lightweight-jackets?id=1023859',
            "category": 'mens-windbreakers-lightweight-jackets',
            "department": 'men',
        },
        'mens-wool-coats-peacoats': {
            "url": 'https://www.bloomingdales.com/shop/mens/wool-coats-peacoats?id=1005055',
            "category": 'mens-wool-coats-peacoats',
            "department": 'men',
        },
        'mens-zip-up-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/mens/zip-up-sweaters?id=1006186',
            "category": 'mens-zip-up-sweaters',
            "department": 'men',
        },
    },
    'mens-accessories': {
        'mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/mens-accessories?id=1337901',
            "category": 'mens-accessories',
            "department": 'mens-accessories',
        },
    },
    'mens-designer-sale': {
        'mens-designer-sale': {
            "url": 'https://www.bloomingdales.com/shop/mens-designer-sale?id=1063959',
            "category": 'mens-designer-sale',
            "department": 'mens-designer-sale',
        },
    },
    'mens-going-out-outfits': {
        'mens-going-out-outfits': {
            "url": 'https://www.bloomingdales.com/shop/mens-going-out-outfits?id=1179760',
            "category": 'mens-going-out-outfits',
            "department": 'mens-going-out-outfits',
        },
    },
    'mens-leather-belts': {
        'mens-leather-belts': {
            "url": 'https://www.bloomingdales.com/shop/mens-leather-belts?id=1293109',
            "category": 'mens-leather-belts',
            "department": 'mens-leather-belts',
        },
    },
    'mens-matching-sets': {
        'mens-matching-sets': {
            "url": 'https://www.bloomingdales.com/shop/mens-matching-sets?id=1122885',
            "category": 'mens-matching-sets',
            "department": 'mens-matching-sets',
        },
    },
    'mens-shoes': {
        'mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/mens-shoes?id=1337900',
            "category": 'mens-shoes',
            "department": 'mens-shoes',
        },
    },
    'mens-store-bloomingdales-accessories': {
        'mens-store-bloomingdales-accessories': {
            "url": 'https://www.bloomingdales.com/shop/mens-store-bloomingdales-accessories?id=1051159',
            "category": 'mens-store-bloomingdales-accessories',
            "department": 'mens-store-bloomingdales-accessories',
        },
    },
    'mens-watches': {
        'mens-watches': {
            "url": 'https://www.bloomingdales.com/shop/mens-watches?id=1230059',
            "category": 'mens-watches',
            "department": 'mens-watches',
        },
    },
    'merino-wool': {
        'merino-wool': {
            "url": 'https://www.bloomingdales.com/shop/merino-wool?id=1133764',
            "category": 'merino-wool',
            "department": 'merino-wool',
        },
    },
    'messika': {
        'messika': {
            "url": 'https://www.bloomingdales.com/shop/messika?id=1286104',
            "category": 'messika',
            "department": 'messika',
        },
    },
    'michael-aram': {
        'michael-aram': {
            "url": 'https://www.bloomingdales.com/shop/michael-aram?id=1004076',
            "category": 'michael-aram',
            "department": 'michael-aram',
        },
        'michael-aram-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/michael-aram/new-arrivals?id=1287542',
            "category": 'michael-aram-new-arrivals',
            "department": 'michael-aram',
        },
    },
    'michael-kors': {
        'michael-kors': {
            "url": 'https://www.bloomingdales.com/shop/michael-kors?id=1002791',
            "category": 'michael-kors',
            "department": 'michael-kors',
        },
        'michael-kors-accessories-watches-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/michael-kors/accessories-watches-sunglasses?id=1002796',
            "category": 'michael-kors-accessories-watches-sunglasses',
            "department": 'michael-kors',
        },
        'michael-kors-handbags': {
            "url": 'https://www.bloomingdales.com/shop/michael-kors/handbags?id=1002795',
            "category": 'michael-kors-handbags',
            "department": 'michael-kors',
        },
        'michael-kors-mens-clothing-watches': {
            "url": 'https://www.bloomingdales.com/shop/michael-kors/mens-clothing-watches?id=1002798',
            "category": 'michael-kors-mens-clothing-watches',
            "department": 'michael-kors',
        },
        'michael-kors-wardrobe-essentials': {
            "url": 'https://www.bloomingdales.com/shop/michael-kors/wardrobe-essentials?id=1241263',
            "category": 'michael-kors-wardrobe-essentials',
            "department": 'michael-kors',
        },
        'michael-kors-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/michael-kors/womens-clothing?id=1002793',
            "category": 'michael-kors-womens-clothing',
            "department": 'michael-kors',
        },
        'michael-kors-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/michael-kors/womens-shoes?id=1002794',
            "category": 'michael-kors-womens-shoes',
            "department": 'michael-kors',
        },
    },
    'michele': {
        'michele': {
            "url": 'https://www.bloomingdales.com/shop/michele?id=1003996',
            "category": 'michele',
            "department": 'michele',
        },
    },
    'michele-builder-straps': {
        'michele-builder-straps': {
            "url": 'https://www.bloomingdales.com/shop/michele-builder-straps?id=1004564',
            "category": 'michele-builder-straps',
            "department": 'michele-builder-straps',
        },
    },
    'mind-games': {
        'mind-games': {
            "url": 'https://www.bloomingdales.com/shop/mind-games?id=1273205',
            "category": 'mind-games',
            "department": 'mind-games',
        },
        'mind-games-mind-games-candles': {
            "url": 'https://www.bloomingdales.com/shop/mind-games/mind-games-candles?id=1273396',
            "category": 'mind-games-mind-games-candles',
            "department": 'mind-games',
        },
        'mind-games-mind-games-decanters': {
            "url": 'https://www.bloomingdales.com/shop/mind-games/mind-games-decanters?id=1302796',
            "category": 'mind-games-mind-games-decanters',
            "department": 'mind-games',
        },
        'mind-games-mind-games-discovery-sets': {
            "url": 'https://www.bloomingdales.com/shop/mind-games/mind-games-discovery-sets?id=1273206',
            "category": 'mind-games-mind-games-discovery-sets',
            "department": 'mind-games',
        },
        'mind-games-mind-games-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/mind-games/mind-games-fragrance?id=1302795',
            "category": 'mind-games-mind-games-fragrance',
            "department": 'mind-games',
        },
    },
    'miu-miu': {
        'miu-miu': {
            "url": 'https://www.bloomingdales.com/shop/miu-miu?id=1265095',
            "category": 'miu-miu',
            "department": 'miu-miu',
        },
        'miu-miu-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/miu-miu/fragrance?id=1303420',
            "category": 'miu-miu-fragrance',
            "department": 'miu-miu',
        },
        'miu-miu-handbags': {
            "url": 'https://www.bloomingdales.com/shop/miu-miu/handbags?id=1333197',
            "category": 'miu-miu-handbags',
            "department": 'miu-miu',
        },
        'miu-miu-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/miu-miu/sunglasses?id=1265096',
            "category": 'miu-miu-sunglasses',
            "department": 'miu-miu',
        },
        'miu-miu-womens-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/miu-miu/womens-jewelry-accessories?id=1335304',
            "category": 'miu-miu-womens-jewelry-accessories',
            "department": 'miu-miu',
        },
        'miu-miu-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/miu-miu/womens-shoes?id=1265097',
            "category": 'miu-miu-womens-shoes',
            "department": 'miu-miu',
        },
    },
    'mixing-bowl-set-measuring-cups-spoons': {
        'mixing-bowl-set-measuring-cups-spoons': {
            "url": 'https://www.bloomingdales.com/shop/mixing-bowl-set-measuring-cups-spoons?id=1301870',
            "category": 'mixing-bowl-set-measuring-cups-spoons',
            "department": 'mixing-bowl-set-measuring-cups-spoons',
        },
    },
    'modern-beer-glasses-set-pilsner-glass': {
        'modern-beer-glasses-set-pilsner-glass': {
            "url": 'https://www.bloomingdales.com/shop/modern-beer-glasses-set-pilsner-glass?id=1054661',
            "category": 'modern-beer-glasses-set-pilsner-glass',
            "department": 'modern-beer-glasses-set-pilsner-glass',
        },
    },
    'modern-coasters-ice-buckets-bar-wine-accessories': {
        'modern-coasters-ice-buckets-bar-wine-accessories': {
            "url": 'https://www.bloomingdales.com/shop/modern-coasters-ice-buckets-bar-wine-accessories?id=1054660',
            "category": 'modern-coasters-ice-buckets-bar-wine-accessories',
            "department": 'modern-coasters-ice-buckets-bar-wine-accessories',
        },
    },
    'modern-contemporary-mirrors-wall-art': {
        'modern-contemporary-mirrors-wall-art': {
            "url": 'https://www.bloomingdales.com/shop/modern-contemporary-mirrors-wall-art?id=1151574',
            "category": 'modern-contemporary-mirrors-wall-art',
            "department": 'modern-contemporary-mirrors-wall-art',
        },
        'modern-contemporary-mirrors-wall-art-elegant-designer-wall-art': {
            "url": 'https://www.bloomingdales.com/shop/modern-contemporary-mirrors-wall-art/elegant-designer-wall-art?id=1151577',
            "category": 'modern-contemporary-mirrors-wall-art-elegant-designer-wall-art',
            "department": 'modern-contemporary-mirrors-wall-art',
        },
        'modern-contemporary-mirrors-wall-art-modern-contemporary-designer-wall-floor-mirrors': {
            "url": 'https://www.bloomingdales.com/shop/modern-contemporary-mirrors-wall-art/modern-contemporary-designer-wall-floor-mirrors?id=1151575',
            "category": 'modern-contemporary-mirrors-wall-art-modern-contemporary-designer-wall-floor-mirrors',
            "department": 'modern-contemporary-mirrors-wall-art',
        },
    },
    'modern-elegant-champagne-glasses': {
        'modern-elegant-champagne-glasses': {
            "url": 'https://www.bloomingdales.com/shop/modern-elegant-champagne-glasses?id=1054662',
            "category": 'modern-elegant-champagne-glasses',
            "department": 'modern-elegant-champagne-glasses',
        },
    },
    'modern-picture-frames-luxury-photo-frames': {
        'modern-picture-frames-luxury-photo-frames': {
            "url": 'https://www.bloomingdales.com/shop/modern-picture-frames-luxury-photo-frames?id=1151578',
            "category": 'modern-picture-frames-luxury-photo-frames',
            "department": 'modern-picture-frames-luxury-photo-frames',
        },
    },
    'modern-red-white-wine-glasses': {
        'modern-red-white-wine-glasses': {
            "url": 'https://www.bloomingdales.com/shop/modern-red-white-wine-glasses?id=1054665',
            "category": 'modern-red-white-wine-glasses',
            "department": 'modern-red-white-wine-glasses',
        },
    },
    'modern-water-glasses-juice-glass-sets': {
        'modern-water-glasses-juice-glass-sets': {
            "url": 'https://www.bloomingdales.com/shop/modern-water-glasses-juice-glass-sets?id=1054664',
            "category": 'modern-water-glasses-juice-glass-sets',
            "department": 'modern-water-glasses-juice-glass-sets',
        },
    },
    'modern-whiskey-cocktail-martini-glasses': {
        'modern-whiskey-cocktail-martini-glasses': {
            "url": 'https://www.bloomingdales.com/shop/modern-whiskey-cocktail-martini-glasses?id=1054663',
            "category": 'modern-whiskey-cocktail-martini-glasses',
            "department": 'modern-whiskey-cocktail-martini-glasses',
        },
    },
    'mommy-and-me': {
        'mommy-and-me': {
            "url": 'https://www.bloomingdales.com/shop/mommy-and-me?id=1133860',
            "category": 'mommy-and-me',
            "department": 'mommy-and-me',
        },
    },
    'moncler': {
        'moncler': {
            "url": 'https://www.bloomingdales.com/shop/moncler?id=1004056',
            "category": 'moncler',
            "department": 'moncler',
        },
        'moncler-kids-clothing': {
            "url": 'https://www.bloomingdales.com/shop/moncler/kids-clothing?id=1004060',
            "category": 'moncler-kids-clothing',
            "department": 'moncler',
        },
        'moncler-mens-clothing-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/moncler/mens-clothing-coats-jackets?id=1004058',
            "category": 'moncler-mens-clothing-coats-jackets',
            "department": 'moncler',
        },
        'moncler-moncler-grenoble': {
            "url": 'https://www.bloomingdales.com/shop/moncler/moncler-grenoble?id=1177061',
            "category": 'moncler-moncler-grenoble',
            "department": 'moncler',
        },
        'moncler-moncler-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/moncler/moncler-womens-clothing?id=1004057',
            "category": 'moncler-moncler-womens-clothing',
            "department": 'moncler',
        },
        'moncler-womens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/moncler/womens-accessories?id=1081559',
            "category": 'moncler-womens-accessories',
            "department": 'moncler',
        },
    },
    'montblanc': {
        'montblanc': {
            "url": 'https://www.bloomingdales.com/shop/montblanc?id=1214867',
            "category": 'montblanc',
            "department": 'montblanc',
        },
        'montblanc-bags-briefcases': {
            "url": 'https://www.bloomingdales.com/shop/montblanc/bags-briefcases?id=1215860',
            "category": 'montblanc-bags-briefcases',
            "department": 'montblanc',
        },
        'montblanc-belts': {
            "url": 'https://www.bloomingdales.com/shop/montblanc/belts?id=1251510',
            "category": 'montblanc-belts',
            "department": 'montblanc',
        },
        'montblanc-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/montblanc/fragrance?id=1214870',
            "category": 'montblanc-fragrance',
            "department": 'montblanc',
        },
        'montblanc-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/montblanc/jewelry-accessories?id=1215861',
            "category": 'montblanc-jewelry-accessories',
            "department": 'montblanc',
        },
        'montblanc-luxury-pens-stationery': {
            "url": 'https://www.bloomingdales.com/shop/montblanc/luxury-pens-stationery?id=1214869',
            "category": 'montblanc-luxury-pens-stationery',
            "department": 'montblanc',
        },
        'montblanc-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/montblanc/shop-all?id=1214871',
            "category": 'montblanc-shop-all',
            "department": 'montblanc',
        },
        'montblanc-wallets-small-goods': {
            "url": 'https://www.bloomingdales.com/shop/montblanc/wallets-small-goods?id=1214868',
            "category": 'montblanc-wallets-small-goods',
            "department": 'montblanc',
        },
    },
    'moroccanoil': {
        'moroccanoil': {
            "url": 'https://www.bloomingdales.com/shop/moroccanoil?id=1298815',
            "category": 'moroccanoil',
            "department": 'moroccanoil',
        },
        'moroccanoil-moroccanoil-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/moroccanoil/moroccanoil-bath-body?id=1299900',
            "category": 'moroccanoil-moroccanoil-bath-body',
            "department": 'moroccanoil',
        },
        'moroccanoil-moroccanoil-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/moroccanoil/moroccanoil-fragrance?id=1299898',
            "category": 'moroccanoil-moroccanoil-fragrance',
            "department": 'moroccanoil',
        },
        'moroccanoil-moroccanoil-hair-tools': {
            "url": 'https://www.bloomingdales.com/shop/moroccanoil/moroccanoil-hair-tools?id=1299899',
            "category": 'moroccanoil-moroccanoil-hair-tools',
            "department": 'moroccanoil',
        },
        'moroccanoil-moroccanoil-hair-treatment': {
            "url": 'https://www.bloomingdales.com/shop/moroccanoil/moroccanoil-hair-treatment?id=1299902',
            "category": 'moroccanoil-moroccanoil-hair-treatment',
            "department": 'moroccanoil',
        },
        'moroccanoil-moroccanoil-shampoo-conditioner': {
            "url": 'https://www.bloomingdales.com/shop/moroccanoil/moroccanoil-shampoo-conditioner?id=1299901',
            "category": 'moroccanoil-moroccanoil-shampoo-conditioner',
            "department": 'moroccanoil',
        },
    },
    'mother-denim': {
        'mother-denim': {
            "url": 'https://www.bloomingdales.com/shop/mother-denim?id=1206859',
            "category": 'mother-denim',
            "department": 'mother-denim',
        },
        'mother-denim-jeans': {
            "url": 'https://www.bloomingdales.com/shop/mother-denim/jeans?id=1275519',
            "category": 'mother-denim-jeans',
            "department": 'mother-denim',
        },
        'mother-denim-sale': {
            "url": 'https://www.bloomingdales.com/shop/mother-denim/sale?id=1275520',
            "category": 'mother-denim-sale',
            "department": 'mother-denim',
        },
    },
    'mothers-day-gifts-under-50-dollars': {
        'mothers-day-gifts-under-50-dollars': {
            "url": 'https://www.bloomingdales.com/shop/mothers-day-gifts-under-50-dollars?id=1006709',
            "category": 'mothers-day-gifts-under-50-dollars',
            "department": 'mothers-day-gifts-under-50-dollars',
        },
    },
    'movado': {
        'movado': {
            "url": 'https://www.bloomingdales.com/shop/movado?id=1320904',
            "category": 'movado',
            "department": 'movado',
        },
    },
    'mrs-add-test-cat': {
        'mrs-add-test-cat': {
            "url": 'https://www.bloomingdales.com/shop/mrs-add-test-cat?id=1144118',
            "category": 'mrs-add-test-cat',
            "department": 'mrs-add-test-cat',
        },
    },
    'mygemma': {
        'mygemma': {
            "url": 'https://www.bloomingdales.com/shop/mygemma?id=1246796',
            "category": 'mygemma',
            "department": 'mygemma',
        },
    },
    'mz-wallace-handbags': {
        'mz-wallace-handbags': {
            "url": 'https://www.bloomingdales.com/shop/mz-wallace-handbags?id=1003780',
            "category": 'mz-wallace-handbags',
            "department": 'mz-wallace-handbags',
        },
    },
    'naghedi': {
        'naghedi': {
            "url": 'https://www.bloomingdales.com/shop/naghedi?id=1250008',
            "category": 'naghedi',
            "department": 'naghedi',
        },
    },
    'names-to-know': {
        'names-to-know': {
            "url": 'https://www.bloomingdales.com/shop/names-to-know?id=1301229',
            "category": 'names-to-know',
            "department": 'names-to-know',
        },
    },
    'natura-bisse': {
        'natura-bisse': {
            "url": 'https://www.bloomingdales.com/shop/natura-bisse?id=1317515',
            "category": 'natura-bisse',
            "department": 'natura-bisse',
        },
    },
    'naturally-glam': {
        'naturally-glam': {
            "url": 'https://www.bloomingdales.com/shop/naturally-glam?id=1189259',
            "category": 'naturally-glam',
            "department": 'naturally-glam',
        },
    },
    'nespresso': {
        'nespresso': {
            "url": 'https://www.bloomingdales.com/shop/nespresso?id=1171259',
            "category": 'nespresso',
            "department": 'nespresso',
        },
        'nespresso-nespresso-original': {
            "url": 'https://www.bloomingdales.com/shop/nespresso/nespresso-original?id=1171261',
            "category": 'nespresso-nespresso-original',
            "department": 'nespresso',
        },
        'nespresso-nespresso-pods': {
            "url": 'https://www.bloomingdales.com/shop/nespresso/nespresso-pods?id=1171262',
            "category": 'nespresso-nespresso-pods',
            "department": 'nespresso',
        },
        'nespresso-nespresso-vertuo': {
            "url": 'https://www.bloomingdales.com/shop/nespresso/nespresso-vertuo?id=1171260',
            "category": 'nespresso-nespresso-vertuo',
            "department": 'nespresso',
        },
    },
    'new-arrivals': {
        'new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/new-arrivals?id=1062760',
            "category": 'new-arrivals',
            "department": 'new-arrivals',
        },
    },
    'new-balance': {
        'new-balance': {
            "url": 'https://www.bloomingdales.com/shop/new-balance?id=1306110',
            "category": 'new-balance',
            "department": 'new-balance',
        },
        'new-balance-kids-shoes': {
            "url": 'https://www.bloomingdales.com/shop/new-balance/kids-shoes?id=1322896',
            "category": 'new-balance-kids-shoes',
            "department": 'new-balance',
        },
        'new-balance-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/new-balance/mens-shoes?id=1322895',
            "category": 'new-balance-mens-shoes',
            "department": 'new-balance',
        },
        'new-balance-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/new-balance/womens-shoes?id=1322995',
            "category": 'new-balance-womens-shoes',
            "department": 'new-balance',
        },
    },
    'new-fine-jewelry': {
        'new-fine-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/new-fine-jewelry?id=1266900',
            "category": 'new-fine-jewelry',
            "department": 'new-fine-jewelry',
        },
    },
    'new-markdowns': {
        'new-markdowns': {
            "url": 'https://www.bloomingdales.com/shop/new-markdowns?id=1089563',
            "category": 'new-markdowns',
            "department": 'new-markdowns',
        },
    },
    'new-now': {
        'fashion-lookbooks-videos-style-guide-150th-anniversary-collection': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/150th-anniversary-collection?id=1162760',
            "category": 'fashion-lookbooks-videos-style-guide-150th-anniversary-collection',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-accessories': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/accessories?id=1291349',
            "category": 'fashion-lookbooks-videos-style-guide-accessories',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-all-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/all-new-arrivals?id=1214066',
            "category": 'fashion-lookbooks-videos-style-guide-all-new-arrivals',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-asian-owned-brands': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/asian-owned-brands?id=1169061',
            "category": 'fashion-lookbooks-videos-style-guide-asian-owned-brands',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bachelorette': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bachelorette?id=1261714',
            "category": 'fashion-lookbooks-videos-style-guide-bachelorette',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-beach-accessories-and-beach-furniture': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/beach-accessories-and-beach-furniture?id=1069959',
            "category": 'fashion-lookbooks-videos-style-guide-beach-accessories-and-beach-furniture',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-beach-wear-summer-beach-essentials': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/beach-wear-summer-beach-essentials?id=1049959',
            "category": 'fashion-lookbooks-videos-style-guide-beach-wear-summer-beach-essentials',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-beach-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/beach-wedding-attire?id=1148760',
            "category": 'fashion-lookbooks-videos-style-guide-beach-wedding-attire',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-beauty': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/beauty?id=1314706',
            "category": 'fashion-lookbooks-videos-style-guide-beauty',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/best-sellers?id=1050359',
            "category": 'fashion-lookbooks-videos-style-guide-best-sellers',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-black-owned-brands': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/black-owned-brands?id=1154159',
            "category": 'fashion-lookbooks-videos-style-guide-black-owned-brands',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-black-tie-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/black-tie-wedding-attire?id=1148761',
            "category": 'fashion-lookbooks-videos-style-guide-black-tie-wedding-attire',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bloomingdales-x-wuthering-heights': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bloomingdales-x-wuthering-heights?id=1299995',
            "category": 'fashion-lookbooks-videos-style-guide-bloomingdales-x-wuthering-heights',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bold-bohemian': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bold-bohemian?id=1284996',
            "category": 'fashion-lookbooks-videos-style-guide-bold-bohemian',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bridal-gowns-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bridal-gowns-dresses?id=1032661',
            "category": 'fashion-lookbooks-videos-style-guide-bridal-gowns-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bridal-shower': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bridal-shower?id=1261713',
            "category": 'fashion-lookbooks-videos-style-guide-bridal-shower',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bridal-shower-bachelorette-party-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bridal-shower-bachelorette-party-dresses?id=1018659',
            "category": 'fashion-lookbooks-videos-style-guide-bridal-shower-bachelorette-party-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bride-to-be-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bride-to-be-shoes?id=1097059',
            "category": 'fashion-lookbooks-videos-style-guide-bride-to-be-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-bridesmaid-wedding-party-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/bridesmaid-wedding-party-dresses?id=1018660',
            "category": 'fashion-lookbooks-videos-style-guide-bridesmaid-wedding-party-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-british-prep': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/british-prep?id=1326515',
            "category": 'fashion-lookbooks-videos-style-guide-british-prep',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-california-love': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/california-love?id=1306120',
            "category": 'fashion-lookbooks-videos-style-guide-california-love',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-cashmere-for-kids': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/cashmere-for-kids?id=1288941',
            "category": 'fashion-lookbooks-videos-style-guide-cashmere-for-kids',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-ceremony': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/ceremony?id=1308195',
            "category": 'fashion-lookbooks-videos-style-guide-ceremony',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-cherish-your-magic-by-yinka-ilori': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/cherish-your-magic-by-yinka-ilori?id=1285906',
            "category": 'fashion-lookbooks-videos-style-guide-cherish-your-magic-by-yinka-ilori',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-coastal-summer': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/coastal-summer?id=1321996',
            "category": 'fashion-lookbooks-videos-style-guide-coastal-summer',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-cocktail-wedding-guest': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/cocktail-wedding-guest?id=1096160',
            "category": 'fashion-lookbooks-videos-style-guide-cocktail-wedding-guest',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-coniglio-palm-beach': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/coniglio-palm-beach?id=1271395',
            "category": 'fashion-lookbooks-videos-style-guide-coniglio-palm-beach',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-cool-clogs': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/cool-clogs?id=1133163',
            "category": 'fashion-lookbooks-videos-style-guide-cool-clogs',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-cool-crochet': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/cool-crochet?id=1146966',
            "category": 'fashion-lookbooks-videos-style-guide-cool-crochet',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-corset-tops': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/corset-tops?id=1167759',
            "category": 'fashion-lookbooks-videos-style-guide-corset-tops',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-country-chic': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/country-chic?id=1284997',
            "category": 'fashion-lookbooks-videos-style-guide-country-chic',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated?id=1097159',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-home': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-home?id=1096762',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-home',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-kids': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-kids?id=1096761',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-kids',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-men': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-men?id=1096759',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-men',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-sale': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-sale?id=1185759',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-sale',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-women': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-women?id=1096259',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-women',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-women-beauty': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-women-beauty?id=1096266',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-women-beauty',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-women-clothing': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-women-clothing?id=1096267',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-women-clothing',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-women-handbags': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-women-handbags?id=1096269',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-women-handbags',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-women-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-women-jewelry-accessories?id=1096268',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-women-jewelry-accessories',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-customer-top-rated-women-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/customer-top-rated-women-shoes?id=1096260',
            "category": 'fashion-lookbooks-videos-style-guide-customer-top-rated-women-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-denim-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/denim-dresses?id=1066359',
            "category": 'fashion-lookbooks-videos-style-guide-denim-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-denim-jumpsuits': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/denim-jumpsuits?id=1211764',
            "category": 'fashion-lookbooks-videos-style-guide-denim-jumpsuits',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-designer-boutique': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/designer-boutique?id=1074559',
            "category": 'fashion-lookbooks-videos-style-guide-designer-boutique',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-designer-bridal-gown-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/designer-bridal-gown-dresses?id=1097060',
            "category": 'fashion-lookbooks-videos-style-guide-designer-bridal-gown-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-designer-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/designer-coats-jackets?id=1315501',
            "category": 'fashion-lookbooks-videos-style-guide-designer-coats-jackets',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-designer-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/designer-dresses?id=1315500',
            "category": 'fashion-lookbooks-videos-style-guide-designer-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-designer-pants-skirts': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/designer-pants-skirts?id=1315503',
            "category": 'fashion-lookbooks-videos-style-guide-designer-pants-skirts',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-designer-tops-tees': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/designer-tops-tees?id=1315502',
            "category": 'fashion-lookbooks-videos-style-guide-designer-tops-tees',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-destination-wedding-guest': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/destination-wedding-guest?id=1096059',
            "category": 'fashion-lookbooks-videos-style-guide-destination-wedding-guest',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-easy-refinement': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/easy-refinement?id=1326513',
            "category": 'fashion-lookbooks-videos-style-guide-easy-refinement',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-engagement': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/engagement?id=1261712',
            "category": 'fashion-lookbooks-videos-style-guide-engagement',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-essentials-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/essentials-shop?id=1171859',
            "category": 'fashion-lookbooks-videos-style-guide-essentials-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-fall-in-the-city': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/fall-in-the-city?id=1322004',
            "category": 'fashion-lookbooks-videos-style-guide-fall-in-the-city',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-fashion-director-finds': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/fashion-director-finds?id=1135959',
            "category": 'fashion-lookbooks-videos-style-guide-fashion-director-finds',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-fashion-director-gift-picks': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/fashion-director-gift-picks?id=1292207',
            "category": 'fashion-lookbooks-videos-style-guide-fashion-director-gift-picks',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-fine-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/fine-jewelry-accessories?id=1333395',
            "category": 'fashion-lookbooks-videos-style-guide-fine-jewelry-accessories',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-flower-girl': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/flower-girl?id=1273853',
            "category": 'fashion-lookbooks-videos-style-guide-flower-girl',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-formal': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/formal?id=1179759',
            "category": 'fashion-lookbooks-videos-style-guide-formal',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-formal-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/formal-wedding-attire?id=1148762',
            "category": 'fashion-lookbooks-videos-style-guide-formal-wedding-attire',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-formal-wedding-guest': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/formal-wedding-guest?id=1096161',
            "category": 'fashion-lookbooks-videos-style-guide-formal-wedding-guest',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-fourth-of-july-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/fourth-of-july-shop?id=1006872',
            "category": 'fashion-lookbooks-videos-style-guide-fourth-of-july-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-give-pink-get-more': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/give-pink-get-more?id=1005233',
            "category": 'fashion-lookbooks-videos-style-guide-give-pink-get-more',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-going-out-outfits': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/going-out-outfits?id=1136359',
            "category": 'fashion-lookbooks-videos-style-guide-going-out-outfits',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-graphic-impact': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/graphic-impact?id=1066562',
            "category": 'fashion-lookbooks-videos-style-guide-graphic-impact',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-great-outdoors': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/great-outdoors?id=1284105',
            "category": 'fashion-lookbooks-videos-style-guide-great-outdoors',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-halter-tops-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/halter-tops-dresses?id=1148460',
            "category": 'fashion-lookbooks-videos-style-guide-halter-tops-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-hand-sanitizer': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/hand-sanitizer?id=1287297',
            "category": 'fashion-lookbooks-videos-style-guide-hand-sanitizer',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-handbags': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/handbags?id=1076167',
            "category": 'fashion-lookbooks-videos-style-guide-handbags',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-heritage-classics': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/heritage-classics?id=1257497',
            "category": 'fashion-lookbooks-videos-style-guide-heritage-classics',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-holiday-parties': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/holiday-parties?id=1210676',
            "category": 'fashion-lookbooks-videos-style-guide-holiday-parties',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-home': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/home?id=1314708',
            "category": 'fashion-lookbooks-videos-style-guide-home',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-honeymoon': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/honeymoon?id=1303418',
            "category": 'fashion-lookbooks-videos-style-guide-honeymoon',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-hotel-bloomingdales': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/hotel-bloomingdales?id=1329696',
            "category": 'fashion-lookbooks-videos-style-guide-hotel-bloomingdales',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/jewelry-accessories?id=1314705',
            "category": 'fashion-lookbooks-videos-style-guide-jewelry-accessories',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-kids': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/kids?id=1212971',
            "category": 'fashion-lookbooks-videos-style-guide-kids',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-kids-denim-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/kids-denim-shop?id=1301658',
            "category": 'fashion-lookbooks-videos-style-guide-kids-denim-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-latinx-owned-brands': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/latinx-owned-brands?id=1169060',
            "category": 'fashion-lookbooks-videos-style-guide-latinx-owned-brands',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-lgbtq-owned-brands': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/lgbtq-owned-brands?id=1169059',
            "category": 'fashion-lookbooks-videos-style-guide-lgbtq-owned-brands',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-lunar-new-year-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/lunar-new-year-shop?id=1065959',
            "category": 'fashion-lookbooks-videos-style-guide-lunar-new-year-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-luxe-totes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/luxe-totes?id=1133165',
            "category": 'fashion-lookbooks-videos-style-guide-luxe-totes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-massage-tools': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/massage-tools?id=1288701',
            "category": 'fashion-lookbooks-videos-style-guide-massage-tools',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-maternity-nursing': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/maternity-nursing?id=1287295',
            "category": 'fashion-lookbooks-videos-style-guide-maternity-nursing',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-men': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/men?id=1212969',
            "category": 'fashion-lookbooks-videos-style-guide-men',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens?id=1314707',
            "category": 'fashion-lookbooks-videos-style-guide-mens',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-active': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-active?id=1003736',
            "category": 'fashion-lookbooks-videos-style-guide-mens-active',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-business-casual': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-business-casual?id=1166662',
            "category": 'fashion-lookbooks-videos-style-guide-mens-business-casual',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-clothing?id=1075360',
            "category": 'fashion-lookbooks-videos-style-guide-mens-clothing',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-denim-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-denim-shop?id=1275598',
            "category": 'fashion-lookbooks-videos-style-guide-mens-denim-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-designer-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-designer-new-arrivals?id=1317397',
            "category": 'fashion-lookbooks-videos-style-guide-mens-designer-new-arrivals',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-designer-shoes-luxury-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-designer-shoes-luxury-shoes?id=1075361',
            "category": 'fashion-lookbooks-videos-style-guide-mens-designer-shoes-luxury-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-going-out-outfits': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-going-out-outfits?id=1136859',
            "category": 'fashion-lookbooks-videos-style-guide-mens-going-out-outfits',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-new-arrivals?id=20592',
            "category": 'fashion-lookbooks-videos-style-guide-mens-new-arrivals',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-ski-jackets-pants-clothes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-ski-jackets-pants-clothes?id=1139463',
            "category": 'fashion-lookbooks-videos-style-guide-mens-ski-jackets-pants-clothes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-trends': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-trends?id=1257495',
            "category": 'fashion-lookbooks-videos-style-guide-mens-trends',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-weekend': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-weekend?id=1124959',
            "category": 'fashion-lookbooks-videos-style-guide-mens-weekend',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-work-accessories': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-work-accessories?id=1166663',
            "category": 'fashion-lookbooks-videos-style-guide-mens-work-accessories',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-work-clothing': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-work-clothing?id=1166664',
            "category": 'fashion-lookbooks-videos-style-guide-mens-work-clothing',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mens-work-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mens-work-shoes?id=1166665',
            "category": 'fashion-lookbooks-videos-style-guide-mens-work-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-midnight-opulence': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/midnight-opulence?id=1326997',
            "category": 'fashion-lookbooks-videos-style-guide-midnight-opulence',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mix-masters': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mix-masters?id=1060261',
            "category": 'fashion-lookbooks-videos-style-guide-mix-masters',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-modern-workwear': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/modern-workwear?id=1326514',
            "category": 'fashion-lookbooks-videos-style-guide-modern-workwear',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-mother-of-the-bride': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/mother-of-the-bride?id=1018661',
            "category": 'fashion-lookbooks-videos-style-guide-mother-of-the-bride',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-nba-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/nba-shop?id=1288996',
            "category": 'fashion-lookbooks-videos-style-guide-nba-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-new-beauty-products': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/new-beauty-products?id=16541',
            "category": 'fashion-lookbooks-videos-style-guide-new-beauty-products',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-new-designer-handbags-purses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/new-designer-handbags-purses?id=22173',
            "category": 'fashion-lookbooks-videos-style-guide-new-designer-handbags-purses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-new-festival-season': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/new-festival-season?id=1004415',
            "category": 'fashion-lookbooks-videos-style-guide-new-festival-season',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-new-in-names-to-know': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/new-in-names-to-know?id=1301230',
            "category": 'fashion-lookbooks-videos-style-guide-new-in-names-to-know',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-new-to-bloomingdales': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/new-to-bloomingdales?id=1284295',
            "category": 'fashion-lookbooks-videos-style-guide-new-to-bloomingdales',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-nfl-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/nfl-shop?id=1288995',
            "category": 'fashion-lookbooks-videos-style-guide-nfl-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-nighttime-routine': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/nighttime-routine?id=1287299',
            "category": 'fashion-lookbooks-videos-style-guide-nighttime-routine',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-nouveau-minimalism': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/nouveau-minimalism?id=1326998',
            "category": 'fashion-lookbooks-videos-style-guide-nouveau-minimalism',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-out-about': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/out-about?id=1245495',
            "category": 'fashion-lookbooks-videos-style-guide-out-about',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-poolside-prep': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/poolside-prep?id=1148764',
            "category": 'fashion-lookbooks-videos-style-guide-poolside-prep',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-pre-order': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/pre-order?id=1176759',
            "category": 'fashion-lookbooks-videos-style-guide-pre-order',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-pre-owned-luxury': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/pre-owned-luxury?id=1229873',
            "category": 'fashion-lookbooks-videos-style-guide-pre-owned-luxury',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-relaxed-minimalism': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/relaxed-minimalism?id=1299303',
            "category": 'fashion-lookbooks-videos-style-guide-relaxed-minimalism',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-relaxed-sophistication': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/relaxed-sophistication?id=1284107',
            "category": 'fashion-lookbooks-videos-style-guide-relaxed-sophistication',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-relaxed-tailoring': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/relaxed-tailoring?id=1257496',
            "category": 'fashion-lookbooks-videos-style-guide-relaxed-tailoring',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-rustic-romance': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/rustic-romance?id=1326996',
            "category": 'fashion-lookbooks-videos-style-guide-rustic-romance',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-sculpted-silhouettes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/sculpted-silhouettes?id=1284895',
            "category": 'fashion-lookbooks-videos-style-guide-sculpted-silhouettes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-sexual-wellness': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/sexual-wellness?id=1123260',
            "category": 'fashion-lookbooks-videos-style-guide-sexual-wellness',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/shoes?id=1314702',
            "category": 'fashion-lookbooks-videos-style-guide-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-shoes-handbags': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/shoes-handbags?id=1213068',
            "category": 'fashion-lookbooks-videos-style-guide-shoes-handbags',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/shop-all?id=1116359',
            "category": 'fashion-lookbooks-videos-style-guide-shop-all',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-shop-all-diverse-owned-brands': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/shop-all-diverse-owned-brands?id=1169359',
            "category": 'fashion-lookbooks-videos-style-guide-shop-all-diverse-owned-brands',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-shop-all-men': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/shop-all-men?id=1075359',
            "category": 'fashion-lookbooks-videos-style-guide-shop-all-men',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-shop-all-trends': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/shop-all-trends?id=1204164',
            "category": 'fashion-lookbooks-videos-style-guide-shop-all-trends',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-shop-all-women': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/shop-all-women?id=1289498',
            "category": 'fashion-lookbooks-videos-style-guide-shop-all-women',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-soccer-fan-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/soccer-fan-shop?id=1317098',
            "category": 'fashion-lookbooks-videos-style-guide-soccer-fan-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-sporty-chic': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/sporty-chic?id=1326498',
            "category": 'fashion-lookbooks-videos-style-guide-sporty-chic',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-statement-knits': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/statement-knits?id=1133162',
            "category": 'fashion-lookbooks-videos-style-guide-statement-knits',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-summer-wedding-guest-dresses': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/summer-wedding-guest-dresses?id=1228559',
            "category": 'fashion-lookbooks-videos-style-guide-summer-wedding-guest-dresses',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-sustainable-mindful-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/sustainable-mindful-shop?id=1037759',
            "category": 'fashion-lookbooks-videos-style-guide-sustainable-mindful-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-swimsuits-bathing-suits': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/swimsuits-bathing-suits?id=1002625',
            "category": 'fashion-lookbooks-videos-style-guide-swimsuits-bathing-suits',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-tennis-golf': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/tennis-golf?id=1211559',
            "category": 'fashion-lookbooks-videos-style-guide-tennis-golf',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-cashmere-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-cashmere-shop?id=1007004',
            "category": 'fashion-lookbooks-videos-style-guide-the-cashmere-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-denim-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-denim-shop?id=1206359',
            "category": 'fashion-lookbooks-videos-style-guide-the-denim-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-golf-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-golf-shop?id=1189563',
            "category": 'fashion-lookbooks-videos-style-guide-the-golf-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-new-preppy': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-new-preppy?id=1284106',
            "category": 'fashion-lookbooks-videos-style-guide-the-new-preppy',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-outdoors-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-outdoors-shop?id=1171600',
            "category": 'fashion-lookbooks-videos-style-guide-the-outdoors-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-showroom': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-showroom?id=1047159',
            "category": 'fashion-lookbooks-videos-style-guide-the-showroom',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-ski-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-ski-shop?id=1079861',
            "category": 'fashion-lookbooks-videos-style-guide-the-ski-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-surf-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-surf-shop?id=1306695',
            "category": 'fashion-lookbooks-videos-style-guide-the-surf-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-wedding-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-wedding-shop?id=1003152',
            "category": 'fashion-lookbooks-videos-style-guide-the-wedding-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-the-work-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/the-work-shop?id=1307605',
            "category": 'fashion-lookbooks-videos-style-guide-the-work-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-vitamins-supplements': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/vitamins-supplements?id=1287296',
            "category": 'fashion-lookbooks-videos-style-guide-vitamins-supplements',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wardrobe-staples': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wardrobe-staples?id=1240760',
            "category": 'fashion-lookbooks-videos-style-guide-wardrobe-staples',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wedding-guest': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wedding-guest?id=1018662',
            "category": 'fashion-lookbooks-videos-style-guide-wedding-guest',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wedding-guest-dresses-under-200': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wedding-guest-dresses-under-200?id=1308198',
            "category": 'fashion-lookbooks-videos-style-guide-wedding-guest-dresses-under-200',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wedding-guest-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wedding-guest-jewelry-accessories?id=1156759',
            "category": 'fashion-lookbooks-videos-style-guide-wedding-guest-jewelry-accessories',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wedding-shoes-for-men': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wedding-shoes-for-men?id=1148763',
            "category": 'fashion-lookbooks-videos-style-guide-wedding-shoes-for-men',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wedding-suits-groom-tuxedo-shoes-bow-ties': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wedding-suits-groom-tuxedo-shoes-bow-ties?id=1004720',
            "category": 'fashion-lookbooks-videos-style-guide-wedding-suits-groom-tuxedo-shoes-bow-ties',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-weekend': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/weekend?id=1321397',
            "category": 'fashion-lookbooks-videos-style-guide-weekend',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-weekend-adventure': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/weekend-adventure?id=1299302',
            "category": 'fashion-lookbooks-videos-style-guide-weekend-adventure',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-weekend-clothes-brunch-outfits': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/weekend-clothes-brunch-outfits?id=1077759',
            "category": 'fashion-lookbooks-videos-style-guide-weekend-clothes-brunch-outfits',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wellness-products': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wellness-products?id=1078659',
            "category": 'fashion-lookbooks-videos-style-guide-wellness-products',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-wild-ride': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/wild-ride?id=1171603',
            "category": 'fashion-lookbooks-videos-style-guide-wild-ride',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-winter-wear-cold-weather-essentials': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/winter-wear-cold-weather-essentials?id=1017559',
            "category": 'fashion-lookbooks-videos-style-guide-winter-wear-cold-weather-essentials',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-women': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/women?id=1212968',
            "category": 'fashion-lookbooks-videos-style-guide-women',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-women-designer-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/women-designer-new-arrivals?id=1317396',
            "category": 'fashion-lookbooks-videos-style-guide-women-designer-new-arrivals',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-women-owned-brands': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/women-owned-brands?id=1154059',
            "category": 'fashion-lookbooks-videos-style-guide-women-owned-brands',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-clothing?id=1075059',
            "category": 'fashion-lookbooks-videos-style-guide-womens-clothing',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-denim-shop': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-denim-shop?id=1275599',
            "category": 'fashion-lookbooks-videos-style-guide-womens-denim-shop',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-going-out-outfits': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-going-out-outfits?id=1001940',
            "category": 'fashion-lookbooks-videos-style-guide-womens-going-out-outfits',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-new-arrivals?id=1036559',
            "category": 'fashion-lookbooks-videos-style-guide-womens-new-arrivals',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-shoes?id=1076162',
            "category": 'fashion-lookbooks-videos-style-guide-womens-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-ski-jackets-pants-clothes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-ski-jackets-pants-clothes?id=1139462',
            "category": 'fashion-lookbooks-videos-style-guide-womens-ski-jackets-pants-clothes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-trends': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-trends?id=1260795',
            "category": 'fashion-lookbooks-videos-style-guide-womens-trends',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-work-clothing': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-work-clothing?id=1167659',
            "category": 'fashion-lookbooks-videos-style-guide-womens-work-clothing',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-workout-clothes-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-workout-clothes-shoes?id=1003732',
            "category": 'fashion-lookbooks-videos-style-guide-womens-workout-clothes-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-womens-workwear': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/womens-workwear?id=1167661',
            "category": 'fashion-lookbooks-videos-style-guide-womens-workwear',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-work-handbags': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/work-handbags?id=1162759',
            "category": 'fashion-lookbooks-videos-style-guide-work-handbags',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-work-shoes': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/work-shoes?id=1162961',
            "category": 'fashion-lookbooks-videos-style-guide-work-shoes',
            "department": 'new-now',
        },
        'fashion-lookbooks-videos-style-guide-workout-clothes-athleisure-wear': {
            "url": 'https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide/workout-clothes-athleisure-wear?id=1003729',
            "category": 'fashion-lookbooks-videos-style-guide-workout-clothes-athleisure-wear',
            "department": 'new-now',
        },
    },
    'new-registry-homepage': {
        'new-registry-homepage': {
            "url": 'https://www.bloomingdales.com/shop/new-registry-homepage?id=1176159',
            "category": 'new-registry-homepage',
            "department": 'new-registry-homepage',
        },
    },
    'newborn-baby-girl-shoes': {
        'newborn-baby-girl-shoes': {
            "url": 'https://www.bloomingdales.com/shop/newborn-baby-girl-shoes?id=1006124',
            "category": 'newborn-baby-girl-shoes',
            "department": 'newborn-baby-girl-shoes',
        },
    },
    'nike': {
        'nike': {
            "url": 'https://www.bloomingdales.com/shop/nike?id=1265999',
            "category": 'nike',
            "department": 'nike',
        },
        'nike-kids': {
            "url": 'https://www.bloomingdales.com/shop/nike/kids?id=1266005',
            "category": 'nike-kids',
            "department": 'nike',
        },
        'nike-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/nike/mens-clothing?id=1266002',
            "category": 'nike-mens-clothing',
            "department": 'nike',
        },
        'nike-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/nike/mens-shoes?id=1266003',
            "category": 'nike-mens-shoes',
            "department": 'nike',
        },
        'nike-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/nike/womens-clothing?id=1266001',
            "category": 'nike-womens-clothing',
            "department": 'nike',
        },
        'nike-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/nike/womens-shoes?id=1266000',
            "category": 'nike-womens-shoes',
            "department": 'nike',
        },
    },
    'nn07': {
        'nn07': {
            "url": 'https://www.bloomingdales.com/shop/nn07?id=1313618',
            "category": 'nn07',
            "department": 'nn07',
        },
    },
    'nuna': {
        'nuna': {
            "url": 'https://www.bloomingdales.com/shop/nuna?id=1272010',
            "category": 'nuna',
            "department": 'nuna',
        },
    },
    'nyc-style-icons': {
        'nyc-style-icons': {
            "url": 'https://www.bloomingdales.com/shop/nyc-style-icons?id=1003453',
            "category": 'nyc-style-icons',
            "department": 'nyc-style-icons',
        },
    },
    'nydj': {
        'nydj': {
            "url": 'https://www.bloomingdales.com/shop/nydj?id=1004129',
            "category": 'nydj',
            "department": 'nydj',
        },
        'nydj-petites': {
            "url": 'https://www.bloomingdales.com/shop/nydj/petites?id=1004132',
            "category": 'nydj-petites',
            "department": 'nydj',
        },
        'nydj-plus-size-clothing': {
            "url": 'https://www.bloomingdales.com/shop/nydj/plus-size-clothing?id=1004131',
            "category": 'nydj-plus-size-clothing',
            "department": 'nydj',
        },
        'nydj-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/nydj/womens-clothing?id=1004130',
            "category": 'nydj-womens-clothing',
            "department": 'nydj',
        },
    },
    'office-approved': {
        'office-approved': {
            "url": 'https://www.bloomingdales.com/shop/office-approved?id=1122864',
            "category": 'office-approved',
            "department": 'office-approved',
        },
    },
    'olaplex': {
        'olaplex': {
            "url": 'https://www.bloomingdales.com/shop/olaplex?id=1320927',
            "category": 'olaplex',
            "department": 'olaplex',
        },
    },
    'omni-evergreens-s-25': {
        'omni-evergreens-s-25': {
            "url": 'https://www.bloomingdales.com/shop/omni-evergreens-s-25?id=1264895',
            "category": 'omni-evergreens-s-25',
            "department": 'omni-evergreens-s-25',
        },
        'omni-evergreens-s-25-com-evergreens-s-25': {
            "url": 'https://www.bloomingdales.com/shop/omni-evergreens-s-25/com-evergreens-s-25?id=1265896',
            "category": 'omni-evergreens-s-25-com-evergreens-s-25',
            "department": 'omni-evergreens-s-25',
        },
    },
    'on': {
        'on': {
            "url": 'https://www.bloomingdales.com/shop/on?id=1198871',
            "category": 'on',
            "department": 'on',
        },
        'on-cloud-6': {
            "url": 'https://www.bloomingdales.com/shop/on/cloud-6?id=1329495',
            "category": 'on-cloud-6',
            "department": 'on',
        },
        'on-kids': {
            "url": 'https://www.bloomingdales.com/shop/on/kids?id=1203060',
            "category": 'on-kids',
            "department": 'on',
        },
        'on-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/on/mens-shoes?id=1198869',
            "category": 'on-mens-shoes',
            "department": 'on',
        },
        'on-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/on/womens-shoes?id=1198459',
            "category": 'on-womens-shoes',
            "department": 'on',
        },
    },
    'one-piece-swimsuits-bathing-suits': {
        'one-piece-swimsuits-bathing-suits': {
            "url": 'https://www.bloomingdales.com/shop/one-piece-swimsuits-bathing-suits?id=1156961',
            "category": 'one-piece-swimsuits-bathing-suits',
            "department": 'one-piece-swimsuits-bathing-suits',
        },
    },
    'online-exclusives': {
        'online-exclusives': {
            "url": 'https://www.bloomingdales.com/shop/online-exclusives?id=1323795',
            "category": 'online-exclusives',
            "department": 'online-exclusives',
        },
    },
    'only-at-bloomingdales-100-exclusive-products': {
        'only-at-bloomingdales-100-exclusive-products': {
            "url": 'https://www.bloomingdales.com/shop/only-at-bloomingdales-100-exclusive-products?id=1191859',
            "category": 'only-at-bloomingdales-100-exclusive-products',
            "department": 'only-at-bloomingdales-100-exclusive-products',
        },
    },
    'oribe': {
        'oribe': {
            "url": 'https://www.bloomingdales.com/shop/oribe?id=1265002',
            "category": 'oribe',
            "department": 'oribe',
        },
    },
    'our-favorite-gifts': {
        'our-favorite-gifts': {
            "url": 'https://www.bloomingdales.com/shop/our-favorite-gifts?id=1021359',
            "category": 'our-favorite-gifts',
            "department": 'our-favorite-gifts',
        },
    },
    'paige': {
        'paige': {
            "url": 'https://www.bloomingdales.com/shop/paige?id=1190559',
            "category": 'paige',
            "department": 'paige',
        },
        'paige-anessa-denim': {
            "url": 'https://www.bloomingdales.com/shop/paige/anessa-denim?id=1267795',
            "category": 'paige-anessa-denim',
            "department": 'paige',
        },
        'paige-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/paige/mens-clothing?id=1190561',
            "category": 'paige-mens-clothing',
            "department": 'paige',
        },
        'paige-mens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/paige/mens-jeans?id=1275516',
            "category": 'paige-mens-jeans',
            "department": 'paige',
        },
        'paige-sale': {
            "url": 'https://www.bloomingdales.com/shop/paige/sale?id=1275517',
            "category": 'paige-sale',
            "department": 'paige',
        },
        'paige-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/paige/womens-clothing?id=1190560',
            "category": 'paige-womens-clothing',
            "department": 'paige',
        },
        'paige-womens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/paige/womens-jeans?id=1275515',
            "category": 'paige-womens-jeans',
            "department": 'paige',
        },
        'paige-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/paige/womens-shoes?id=1190562',
            "category": 'paige-womens-shoes',
            "department": 'paige',
        },
    },
    'pajama-party': {
        'pajama-party': {
            "url": 'https://www.bloomingdales.com/shop/pajama-party?id=1253726',
            "category": 'pajama-party',
            "department": 'pajama-party',
        },
    },
    'panties': {
        'panties': {
            "url": 'https://www.bloomingdales.com/shop/panties?id=4359',
            "category": 'panties',
            "department": 'panties',
        },
    },
    'pants': {
        'pants': {
            "url": 'https://www.bloomingdales.com/shop/pants?id=1278811',
            "category": 'pants',
            "department": 'pants',
        },
    },
    'pants-jeans-skirts-leggings': {
        'pants-jeans-skirts-leggings': {
            "url": 'https://www.bloomingdales.com/shop/pants-jeans-skirts-leggings?id=1267450',
            "category": 'pants-jeans-skirts-leggings',
            "department": 'pants-jeans-skirts-leggings',
        },
        'pants-jeans-skirts-leggings-plus-size-pants-leggings': {
            "url": 'https://www.bloomingdales.com/shop/pants-jeans-skirts-leggings/plus-size-pants-leggings?id=1267451',
            "category": 'pants-jeans-skirts-leggings-plus-size-pants-leggings',
            "department": 'pants-jeans-skirts-leggings',
        },
        'pants-jeans-skirts-leggings-skirts-shorts': {
            "url": 'https://www.bloomingdales.com/shop/pants-jeans-skirts-leggings/skirts-shorts?id=1267452',
            "category": 'pants-jeans-skirts-leggings-skirts-shorts',
            "department": 'pants-jeans-skirts-leggings',
        },
    },
    'parfums-de-marly': {
        'parfums-de-marly': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly?id=1263816',
            "category": 'parfums-de-marly',
            "department": 'parfums-de-marly',
        },
        'parfums-de-marly-parfums-de-marly-althair': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly/parfums-de-marly-althair?id=1320208',
            "category": 'parfums-de-marly-parfums-de-marly-althair',
            "department": 'parfums-de-marly',
        },
        'parfums-de-marly-parfums-de-marly-cologne': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly/parfums-de-marly-cologne?id=1269719',
            "category": 'parfums-de-marly-parfums-de-marly-cologne',
            "department": 'parfums-de-marly',
        },
        'parfums-de-marly-parfums-de-marly-delina': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly/parfums-de-marly-delina?id=1265297',
            "category": 'parfums-de-marly-parfums-de-marly-delina',
            "department": 'parfums-de-marly',
        },
        'parfums-de-marly-parfums-de-marly-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly/parfums-de-marly-gift-sets?id=1299316',
            "category": 'parfums-de-marly-parfums-de-marly-gift-sets',
            "department": 'parfums-de-marly',
        },
        'parfums-de-marly-parfums-de-marly-home-body': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly/parfums-de-marly-home-body?id=1299315',
            "category": 'parfums-de-marly-parfums-de-marly-home-body',
            "department": 'parfums-de-marly',
        },
        'parfums-de-marly-parfums-de-marly-perfume': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly/parfums-de-marly-perfume?id=1269718',
            "category": 'parfums-de-marly-parfums-de-marly-perfume',
            "department": 'parfums-de-marly',
        },
        'parfums-de-marly-parfums-de-marly-valaya': {
            "url": 'https://www.bloomingdales.com/shop/parfums-de-marly/parfums-de-marly-valaya?id=1269717',
            "category": 'parfums-de-marly-parfums-de-marly-valaya',
            "department": 'parfums-de-marly',
        },
    },
    'parke': {
        'parke': {
            "url": 'https://www.bloomingdales.com/shop/parke?id=1305800',
            "category": 'parke',
            "department": 'parke',
        },
    },
    'party-accessories': {
        'party-accessories': {
            "url": 'https://www.bloomingdales.com/shop/party-accessories?id=1002023',
            "category": 'party-accessories',
            "department": 'party-accessories',
        },
    },
    'party-essentials': {
        'party-essentials-dressed-up-take-out': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/dressed-up-take-out?id=1002567',
            "category": 'party-essentials-dressed-up-take-out',
            "department": 'party-essentials',
        },
        'party-essentials-fall-feast': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/fall-feast?id=1002566',
            "category": 'party-essentials-fall-feast',
            "department": 'party-essentials',
        },
        'party-essentials-game-day-gathering': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/game-day-gathering?id=1002564',
            "category": 'party-essentials-game-day-gathering',
            "department": 'party-essentials',
        },
        'party-essentials-high-tea': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/high-tea?id=1002565',
            "category": 'party-essentials-high-tea',
            "department": 'party-essentials',
        },
        'party-essentials-just-desserts': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/just-desserts?id=1002569',
            "category": 'party-essentials-just-desserts',
            "department": 'party-essentials',
        },
        'party-essentials-recipes': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/recipes?id=1002568',
            "category": 'party-essentials-recipes',
            "department": 'party-essentials',
        },
        'party-essentials-sunday-brunch': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/sunday-brunch?id=1002570',
            "category": 'party-essentials-sunday-brunch',
            "department": 'party-essentials',
        },
        'party-essentials-wine-tasting': {
            "url": 'https://www.bloomingdales.com/shop/party-essentials/wine-tasting?id=1002563',
            "category": 'party-essentials-wine-tasting',
            "department": 'party-essentials',
        },
    },
    'paul-smith': {
        'paul-smith': {
            "url": 'https://www.bloomingdales.com/shop/paul-smith?id=1304396',
            "category": 'paul-smith',
            "department": 'paul-smith',
        },
    },
    'penhaligons': {
        'penhaligons': {
            "url": 'https://www.bloomingdales.com/shop/penhaligons?id=1286895',
            "category": 'penhaligons',
            "department": 'penhaligons',
        },
        'penhaligons-bath-body': {
            "url": 'https://www.bloomingdales.com/shop/penhaligons/bath-body?id=1286898',
            "category": 'penhaligons-bath-body',
            "department": 'penhaligons',
        },
        'penhaligons-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/penhaligons/best-sellers?id=1286899',
            "category": 'penhaligons-best-sellers',
            "department": 'penhaligons',
        },
        'penhaligons-discovery-sets': {
            "url": 'https://www.bloomingdales.com/shop/penhaligons/discovery-sets?id=1286900',
            "category": 'penhaligons-discovery-sets',
            "department": 'penhaligons',
        },
        'penhaligons-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/penhaligons/fragrance?id=1286896',
            "category": 'penhaligons-fragrance',
            "department": 'penhaligons',
        },
        'penhaligons-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/penhaligons/shop-all?id=1286897',
            "category": 'penhaligons-shop-all',
            "department": 'penhaligons',
        },
    },
    'pet-accessories': {
        'pet-accessories': {
            "url": 'https://www.bloomingdales.com/shop/pet-accessories?id=1265424',
            "category": 'pet-accessories',
            "department": 'pet-accessories',
        },
    },
    'peter-millar': {
        'peter-millar': {
            "url": 'https://www.bloomingdales.com/shop/peter-millar?id=1224266',
            "category": 'peter-millar',
            "department": 'peter-millar',
        },
        'peter-millar-kids': {
            "url": 'https://www.bloomingdales.com/shop/peter-millar/kids?id=1224268',
            "category": 'peter-millar-kids',
            "department": 'peter-millar',
        },
        'peter-millar-mens': {
            "url": 'https://www.bloomingdales.com/shop/peter-millar/mens?id=1224267',
            "category": 'peter-millar-mens',
            "department": 'peter-millar',
        },
    },
    'phm-pop-up-shop': {
        'phm-pop-up-shop': {
            "url": 'https://www.bloomingdales.com/shop/phm-pop-up-shop?id=1006384',
            "category": 'phm-pop-up-shop',
            "department": 'phm-pop-up-shop',
        },
    },
    'pickup-delivery': {
        'pickup-delivery': {
            "url": 'https://www.bloomingdales.com/shop/pickup-delivery?id=1132361',
            "category": 'pickup-delivery',
            "department": 'pickup-delivery',
        },
    },
    'pillow-bag': {
        'pillow-bag': {
            "url": 'https://www.bloomingdales.com/shop/pillow-bag?id=1101159',
            "category": 'pillow-bag',
            "department": 'pillow-bag',
        },
    },
    'pillows-comforters-mattress-pads': {
        'pillows-comforters-mattress-pads': {
            "url": 'https://www.bloomingdales.com/shop/pillows-comforters-mattress-pads?id=1020859',
            "category": 'pillows-comforters-mattress-pads',
            "department": 'pillows-comforters-mattress-pads',
        },
    },
    'pink-chicken': {
        'pink-chicken': {
            "url": 'https://www.bloomingdales.com/shop/pink-chicken?id=1276595',
            "category": 'pink-chicken',
            "department": 'pink-chicken',
        },
    },
    'plus-size-clothing': {
        'plus-size-clothing': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-clothing?id=1267300',
            "category": 'plus-size-clothing',
            "department": 'plus-size-clothing',
        },
    },
    'plus-size-coats-jackets': {
        'plus-size-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-coats-jackets?id=1267488',
            "category": 'plus-size-coats-jackets',
            "department": 'plus-size-coats-jackets',
        },
    },
    'plus-size-dresses': {
        'plus-size-dresses': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-dresses?id=1267339',
            "category": 'plus-size-dresses',
            "department": 'plus-size-dresses',
        },
    },
    'plus-size-jeans': {
        'plus-size-jeans': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-jeans?id=1267338',
            "category": 'plus-size-jeans',
            "department": 'plus-size-jeans',
        },
    },
    'plus-size-sweaters': {
        'plus-size-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-sweaters?id=1267447',
            "category": 'plus-size-sweaters',
            "department": 'plus-size-sweaters',
        },
    },
    'plus-size-swimwear-swimsuits': {
        'plus-size-swimwear-swimsuits': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-swimwear-swimsuits?id=1267486',
            "category": 'plus-size-swimwear-swimsuits',
            "department": 'plus-size-swimwear-swimsuits',
        },
    },
    'plus-size-tops-tees': {
        'plus-size-tops-tees': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-tops-tees?id=1267345',
            "category": 'plus-size-tops-tees',
            "department": 'plus-size-tops-tees',
        },
        'plus-size-tops-tees-plus-size-tops': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-tops-tees/plus-size-tops?id=1267354',
            "category": 'plus-size-tops-tees-plus-size-tops',
            "department": 'plus-size-tops-tees',
        },
        'plus-size-tops-tees-tees-tanks': {
            "url": 'https://www.bloomingdales.com/shop/plus-size-tops-tees/tees-tanks?id=1267355',
            "category": 'plus-size-tops-tees-tees-tanks',
            "department": 'plus-size-tops-tees',
        },
    },
    'pot-and-pan-sets': {
        'pot-and-pan-sets': {
            "url": 'https://www.bloomingdales.com/shop/pot-and-pan-sets?id=1039377',
            "category": 'pot-and-pan-sets',
            "department": 'pot-and-pan-sets',
        },
    },
    'prada': {
        'prada': {
            "url": 'https://www.bloomingdales.com/shop/prada?id=1265908',
            "category": 'prada',
            "department": 'prada',
        },
        'prada-cologne': {
            "url": 'https://www.bloomingdales.com/shop/prada/cologne?id=1250403',
            "category": 'prada-cologne',
            "department": 'prada',
        },
        'prada-makeup': {
            "url": 'https://www.bloomingdales.com/shop/prada/makeup?id=1250401',
            "category": 'prada-makeup',
            "department": 'prada',
        },
        'prada-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/prada/mens-clothing?id=1336603',
            "category": 'prada-mens-clothing',
            "department": 'prada',
        },
        'prada-perfume': {
            "url": 'https://www.bloomingdales.com/shop/prada/perfume?id=1250402',
            "category": 'prada-perfume',
            "department": 'prada',
        },
        'prada-prada-beauty': {
            "url": 'https://www.bloomingdales.com/shop/prada/prada-beauty?id=1250400',
            "category": 'prada-prada-beauty',
            "department": 'prada',
        },
        'prada-prada-mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/prada/prada-mens-accessories?id=1265904',
            "category": 'prada-prada-mens-accessories',
            "department": 'prada',
        },
        'prada-prada-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/prada/prada-mens-shoes?id=1265903',
            "category": 'prada-prada-mens-shoes',
            "department": 'prada',
        },
        'prada-prada-womens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/prada/prada-womens-accessories?id=1265900',
            "category": 'prada-prada-womens-accessories',
            "department": 'prada',
        },
        'prada-prada-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/prada/prada-womens-clothing?id=1336802',
            "category": 'prada-prada-womens-clothing',
            "department": 'prada',
        },
        'prada-prada-womens-handbags': {
            "url": 'https://www.bloomingdales.com/shop/prada/prada-womens-handbags?id=1265899',
            "category": 'prada-prada-womens-handbags',
            "department": 'prada',
        },
        'prada-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/prada/shop-all?id=1265907',
            "category": 'prada-shop-all',
            "department": 'prada',
        },
        'prada-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/prada/womens-shoes?id=1265901',
            "category": 'prada-womens-shoes',
            "department": 'prada',
        },
    },
    'pratesi': {
        'pratesi': {
            "url": 'https://www.bloomingdales.com/shop/pratesi?id=1235265',
            "category": 'pratesi',
            "department": 'pratesi',
        },
    },
    'premium-designers': {
        'premium-designers': {
            "url": 'https://www.bloomingdales.com/shop/premium-designers?id=1066159',
            "category": 'premium-designers',
            "department": 'premium-designers',
        },
    },
    'program-rugs': {
        'program-rugs': {
            "url": 'https://www.bloomingdales.com/shop/program-rugs?id=1082959',
            "category": 'program-rugs',
            "department": 'program-rugs',
        },
    },
    'pros-ff': {
        'pros-ff': {
            "url": 'https://www.bloomingdales.com/shop/pros-ff?id=1060959',
            "category": 'pros-ff',
            "department": 'pros-ff',
        },
    },
    'puffer-jackets-vests': {
        'puffer-jackets-vests': {
            "url": 'https://www.bloomingdales.com/shop/puffer-jackets-vests?id=1006193',
            "category": 'puffer-jackets-vests',
            "department": 'puffer-jackets-vests',
        },
    },
    'puro-collection': {
        'puro-collection': {
            "url": 'https://www.bloomingdales.com/shop/puro-collection?id=1310595',
            "category": 'puro-collection',
            "department": 'puro-collection',
        },
    },
    'rabanne': {
        'rabanne': {
            "url": 'https://www.bloomingdales.com/shop/rabanne?id=1284799',
            "category": 'rabanne',
            "department": 'rabanne',
        },
        'rabanne-1-million': {
            "url": 'https://www.bloomingdales.com/shop/rabanne/1-million?id=1289595',
            "category": 'rabanne-1-million',
            "department": 'rabanne',
        },
        'rabanne-cologne': {
            "url": 'https://www.bloomingdales.com/shop/rabanne/cologne?id=1283841',
            "category": 'rabanne-cologne',
            "department": 'rabanne',
        },
        'rabanne-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/rabanne/fragrance?id=1289395',
            "category": 'rabanne-fragrance',
            "department": 'rabanne',
        },
        'rabanne-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/rabanne/gift-sets?id=1291716',
            "category": 'rabanne-gift-sets',
            "department": 'rabanne',
        },
        'rabanne-handbags': {
            "url": 'https://www.bloomingdales.com/shop/rabanne/handbags?id=1283843',
            "category": 'rabanne-handbags',
            "department": 'rabanne',
        },
        'rabanne-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/rabanne/shop-all?id=1283839',
            "category": 'rabanne-shop-all',
            "department": 'rabanne',
        },
        'rabanne-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/rabanne/womens-clothing?id=1283842',
            "category": 'rabanne-womens-clothing',
            "department": 'rabanne',
        },
    },
    'raffia-accessories': {
        'raffia-accessories': {
            "url": 'https://www.bloomingdales.com/shop/raffia-accessories?id=1146960',
            "category": 'raffia-accessories',
            "department": 'raffia-accessories',
        },
    },
    'rag-bone': {
        'rag-bone': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone?id=1005142',
            "category": 'rag-bone',
            "department": 'rag-bone',
        },
        'rag-bone-handbags': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/handbags?id=1090559',
            "category": 'rag-bone-handbags',
            "department": 'rag-bone',
        },
        'rag-bone-mens-clothing-shoes': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/mens-clothing-shoes?id=1005143',
            "category": 'rag-bone-mens-clothing-shoes',
            "department": 'rag-bone',
        },
        'rag-bone-mens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/mens-jeans?id=1248901',
            "category": 'rag-bone-mens-jeans',
            "department": 'rag-bone',
        },
        'rag-bone-miramar': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/miramar?id=1248898',
            "category": 'rag-bone-miramar',
            "department": 'rag-bone',
        },
        'rag-bone-sale': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/sale?id=1248896',
            "category": 'rag-bone-sale',
            "department": 'rag-bone',
        },
        'rag-bone-women': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/women?id=1305797',
            "category": 'rag-bone-women',
            "department": 'rag-bone',
        },
        'rag-bone-womens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/womens-accessories?id=1055759',
            "category": 'rag-bone-womens-accessories',
            "department": 'rag-bone',
        },
        'rag-bone-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/womens-clothing?id=1004123',
            "category": 'rag-bone-womens-clothing',
            "department": 'rag-bone',
        },
        'rag-bone-womens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/womens-jeans?id=1248899',
            "category": 'rag-bone-womens-jeans',
            "department": 'rag-bone',
        },
        'rag-bone-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/womens-shoes?id=1006294',
            "category": 'rag-bone-womens-shoes',
            "department": 'rag-bone',
        },
        'rag-bone-womens-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/rag-bone/womens-sweaters?id=1248900',
            "category": 'rag-bone-womens-sweaters',
            "department": 'rag-bone',
        },
    },
    'rain-shop': {
        'rain-shop': {
            "url": 'https://www.bloomingdales.com/shop/rain-shop?id=1267195',
            "category": 'rain-shop',
            "department": 'rain-shop',
        },
        'rain-shop-kids-rain-jackets': {
            "url": 'https://www.bloomingdales.com/shop/rain-shop/kids-rain-jackets?id=1267198',
            "category": 'rain-shop-kids-rain-jackets',
            "department": 'rain-shop',
        },
        'rain-shop-rain-boots': {
            "url": 'https://www.bloomingdales.com/shop/rain-shop/rain-boots?id=1265000',
            "category": 'rain-shop-rain-boots',
            "department": 'rain-shop',
        },
        'rain-shop-umbrellas': {
            "url": 'https://www.bloomingdales.com/shop/rain-shop/umbrellas?id=1267199',
            "category": 'rain-shop-umbrellas',
            "department": 'rain-shop',
        },
    },
    'ralph-lauren': {
        'ralph-lauren': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren?id=1003114',
            "category": 'ralph-lauren',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-accessories-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/accessories-jewelry?id=1003158',
            "category": 'ralph-lauren-accessories-jewelry',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-artist-in-residence-collection': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/artist-in-residence-collection?id=1296220',
            "category": 'ralph-lauren-artist-in-residence-collection',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-baby': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/baby?id=1162060',
            "category": 'ralph-lauren-baby',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-back-to-school': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/back-to-school?id=1201759',
            "category": 'ralph-lauren-back-to-school',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-basics-sleepwear': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/basics-sleepwear?id=1138869',
            "category": 'ralph-lauren-basics-sleepwear',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/bottoms?id=1312396',
            "category": 'ralph-lauren-bottoms',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-boys': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/boys?id=1161961',
            "category": 'ralph-lauren-boys',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-casual-button-downs': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/casual-button-downs?id=1265796',
            "category": 'ralph-lauren-casual-button-downs',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-cologne': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/cologne?id=1297596',
            "category": 'ralph-lauren-cologne',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-footwear': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/footwear?id=1224263',
            "category": 'ralph-lauren-footwear',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-fragrance-cologne-perfume': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/fragrance-cologne-perfume?id=1003159',
            "category": 'ralph-lauren-fragrance-cologne-perfume',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-girls': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/girls?id=1162059',
            "category": 'ralph-lauren-girls',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-holiday-family-dressing': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/holiday-family-dressing?id=1214973',
            "category": 'ralph-lauren-holiday-family-dressing',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-home-decor': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/home-decor?id=1003161',
            "category": 'ralph-lauren-home-decor',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-home-gifts': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/home-gifts?id=1109066',
            "category": 'ralph-lauren-home-gifts',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-jackets-coats': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/jackets-coats?id=1138866',
            "category": 'ralph-lauren-jackets-coats',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-kids-clothing-accessories': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/kids-clothing-accessories?id=1003115',
            "category": 'ralph-lauren-kids-clothing-accessories',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-kids-gifts': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/kids-gifts?id=1109067',
            "category": 'ralph-lauren-kids-gifts',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-kids-sale': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/kids-sale?id=1161361',
            "category": 'ralph-lauren-kids-sale',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-lauren-ralph-lauren': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/lauren-ralph-lauren?id=1105159',
            "category": 'ralph-lauren-lauren-ralph-lauren',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-lauren-ralph-lauren-dresses': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/lauren-ralph-lauren-dresses?id=1240160',
            "category": 'ralph-lauren-lauren-ralph-lauren-dresses',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-mens-clothing-accessories': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/mens-clothing-accessories?id=1003160',
            "category": 'ralph-lauren-mens-clothing-accessories',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-mens-gifts': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/mens-gifts?id=1109063',
            "category": 'ralph-lauren-mens-gifts',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-mens-loungewear': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/mens-loungewear?id=1138868',
            "category": 'ralph-lauren-mens-loungewear',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-mens-sale': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/mens-sale?id=1161161',
            "category": 'ralph-lauren-mens-sale',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/new-arrivals?id=1332413',
            "category": 'ralph-lauren-new-arrivals',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-new-to-sale': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/new-to-sale?id=1161360',
            "category": 'ralph-lauren-new-to-sale',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-only-polo': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/only-polo?id=1227860',
            "category": 'ralph-lauren-only-polo',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-pants': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/pants?id=1138867',
            "category": 'ralph-lauren-pants',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-pink-pony-collection': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/pink-pony-collection?id=1245795',
            "category": 'ralph-lauren-pink-pony-collection',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-polo-67': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/polo-67?id=1226260',
            "category": 'ralph-lauren-polo-67',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-polo-bear': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/polo-bear?id=1252347',
            "category": 'ralph-lauren-polo-bear',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-polo-ralph-lauren-handbags': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/polo-ralph-lauren-handbags?id=1263712',
            "category": 'ralph-lauren-polo-ralph-lauren-handbags',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-polo-ralph-lauren-the-polo-shirt': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/polo-ralph-lauren-the-polo-shirt?id=1156059',
            "category": 'ralph-lauren-polo-ralph-lauren-the-polo-shirt',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-polo-ralph-lauren-women': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/polo-ralph-lauren-women?id=1105168',
            "category": 'ralph-lauren-polo-ralph-lauren-women',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-polos': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/polos?id=1265795',
            "category": 'ralph-lauren-polos',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-polos-shirts': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/polos-shirts?id=1138861',
            "category": 'ralph-lauren-polos-shirts',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-ralph-lauren-american-icons': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/ralph-lauren-american-icons?id=1172559',
            "category": 'ralph-lauren-ralph-lauren-american-icons',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-ralph-lauren-x-mlb-collection': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/ralph-lauren-x-mlb-collection?id=1313817',
            "category": 'ralph-lauren-ralph-lauren-x-mlb-collection',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-shorts-swim': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/shorts-swim?id=1153760',
            "category": 'ralph-lauren-shorts-swim',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-suit-separates': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/suit-separates?id=1312395',
            "category": 'ralph-lauren-suit-separates',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-sweaters-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/sweaters-sweatshirts?id=1138659',
            "category": 'ralph-lauren-sweaters-sweatshirts',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-team-usa-collection': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/team-usa-collection?id=1234859',
            "category": 'ralph-lauren-team-usa-collection',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-tees': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/tees?id=1265797',
            "category": 'ralph-lauren-tees',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-the-occasion-shop': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/the-occasion-shop?id=1292115',
            "category": 'ralph-lauren-the-occasion-shop',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-wear-to-work': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/wear-to-work?id=1332412',
            "category": 'ralph-lauren-wear-to-work',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/womens-clothing?id=1003154',
            "category": 'ralph-lauren-womens-clothing',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-womens-dresses': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/womens-dresses?id=1312296',
            "category": 'ralph-lauren-womens-dresses',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-womens-gifts': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/womens-gifts?id=1109065',
            "category": 'ralph-lauren-womens-gifts',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-womens-sale': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/womens-sale?id=1161559',
            "category": 'ralph-lauren-womens-sale',
            "department": 'ralph-lauren',
        },
        'ralph-lauren-womens-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/ralph-lauren/womens-sweaters?id=1292195',
            "category": 'ralph-lauren-womens-sweaters',
            "department": 'ralph-lauren',
        },
    },
    'ray-ban': {
        'ray-ban': {
            "url": 'https://www.bloomingdales.com/shop/ray-ban?id=1304261',
            "category": 'ray-ban',
            "department": 'ray-ban',
        },
        'ray-ban-ray-ban-meta': {
            "url": 'https://www.bloomingdales.com/shop/ray-ban/ray-ban-meta?id=1304262',
            "category": 'ray-ban-ray-ban-meta',
            "department": 'ray-ban',
        },
    },
    'rebag': {
        'rebag': {
            "url": 'https://www.bloomingdales.com/shop/rebag?id=1241782',
            "category": 'rebag',
            "department": 'rebag',
        },
        'rebag-handbags': {
            "url": 'https://www.bloomingdales.com/shop/rebag/handbags?id=1241778',
            "category": 'rebag-handbags',
            "department": 'rebag',
        },
        'rebag-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/rebag/jewelry-accessories?id=1241780',
            "category": 'rebag-jewelry-accessories',
            "department": 'rebag',
        },
    },
    'rebecca-minkoff': {
        'rebecca-minkoff': {
            "url": 'https://www.bloomingdales.com/shop/rebecca-minkoff?id=1003757',
            "category": 'rebecca-minkoff',
            "department": 'rebecca-minkoff',
        },
        'rebecca-minkoff-handbags': {
            "url": 'https://www.bloomingdales.com/shop/rebecca-minkoff/handbags?id=1003759',
            "category": 'rebecca-minkoff-handbags',
            "department": 'rebecca-minkoff',
        },
        'rebecca-minkoff-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/rebecca-minkoff/womens-clothing?id=1003782',
            "category": 'rebecca-minkoff-womens-clothing',
            "department": 'rebecca-minkoff',
        },
    },
    'refined-minimalism': {
        'refined-minimalism': {
            "url": 'https://www.bloomingdales.com/shop/refined-minimalism?id=1303796',
            "category": 'refined-minimalism',
            "department": 'refined-minimalism',
        },
    },
    'reformation': {
        'reformation': {
            "url": 'https://www.bloomingdales.com/shop/reformation?id=1266295',
            "category": 'reformation',
            "department": 'reformation',
        },
        'reformation-handbags': {
            "url": 'https://www.bloomingdales.com/shop/reformation/handbags?id=1266297',
            "category": 'reformation-handbags',
            "department": 'reformation',
        },
        'reformation-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/reformation/womens-clothing?id=1282395',
            "category": 'reformation-womens-clothing',
            "department": 'reformation',
        },
        'reformation-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/reformation/womens-shoes?id=1266296',
            "category": 'reformation-womens-shoes',
            "department": 'reformation',
        },
    },
    'registry': {
        'registry-bath-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry/bath-essentials?id=1225160',
            "category": 'registry-bath-essentials',
            "department": 'registry',
        },
        'registry-bedding-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry/bedding-essentials?id=1225161',
            "category": 'registry-bedding-essentials',
            "department": 'registry',
        },
        'registry-best-gifts-under-100': {
            "url": 'https://www.bloomingdales.com/shop/registry/best-gifts-under-100?id=1225162',
            "category": 'registry-best-gifts-under-100',
            "department": 'registry',
        },
        'registry-dining-sets': {
            "url": 'https://www.bloomingdales.com/shop/registry/dining-sets?id=1225163',
            "category": 'registry-dining-sets',
            "department": 'registry',
        },
        'registry-entertaining-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry/entertaining-essentials?id=1225164',
            "category": 'registry-entertaining-essentials',
            "department": 'registry',
        },
        'registry-gifts-for-new-parents': {
            "url": 'https://www.bloomingdales.com/shop/registry/gifts-for-new-parents?id=1228139',
            "category": 'registry-gifts-for-new-parents',
            "department": 'registry',
        },
        'registry-kitchen-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry/kitchen-essentials?id=1225165',
            "category": 'registry-kitchen-essentials',
            "department": 'registry',
        },
        'registry-most-registered-for': {
            "url": 'https://www.bloomingdales.com/shop/registry/most-registered-for?id=1225166',
            "category": 'registry-most-registered-for',
            "department": 'registry',
        },
        'registry-shop-all-registry-items': {
            "url": 'https://www.bloomingdales.com/shop/registry/shop-all-registry-items?id=1224372',
            "category": 'registry-shop-all-registry-items',
            "department": 'registry',
        },
        'registry-special-gifts': {
            "url": 'https://www.bloomingdales.com/shop/registry/special-gifts?id=1245104',
            "category": 'registry-special-gifts',
            "department": 'registry',
        },
        'registry-unexpected-luxuries': {
            "url": 'https://www.bloomingdales.com/shop/registry/unexpected-luxuries?id=1225167',
            "category": 'registry-unexpected-luxuries',
            "department": 'registry',
        },
    },
    'registry-ideas': {
        'registry-ideas-bath-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/bath-essentials?id=1076160',
            "category": 'registry-ideas-bath-essentials',
            "department": 'registry-ideas',
        },
        'registry-ideas-best-brunch-ever': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/best-brunch-ever?id=1062661',
            "category": 'registry-ideas-best-brunch-ever',
            "department": 'registry-ideas',
        },
        'registry-ideas-best-gifts-under-100': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/best-gifts-under-100?id=1193561',
            "category": 'registry-ideas-best-gifts-under-100',
            "department": 'registry-ideas',
        },
        'registry-ideas-bloomingdales-exclusives': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/bloomingdales-exclusives?id=1035376',
            "category": 'registry-ideas-bloomingdales-exclusives',
            "department": 'registry-ideas',
        },
        'registry-ideas-decor-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/decor-essentials?id=1239660',
            "category": 'registry-ideas-decor-essentials',
            "department": 'registry-ideas',
        },
        'registry-ideas-dining-sets': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/dining-sets?id=1004848',
            "category": 'registry-ideas-dining-sets',
            "department": 'registry-ideas',
        },
        'registry-ideas-eclectic-accents': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/eclectic-accents?id=1035367',
            "category": 'registry-ideas-eclectic-accents',
            "department": 'registry-ideas',
        },
        'registry-ideas-hollywood-glamorous': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/hollywood-glamorous?id=1035360',
            "category": 'registry-ideas-hollywood-glamorous',
            "department": 'registry-ideas',
        },
        'registry-ideas-kitchen-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/kitchen-essentials?id=1004849',
            "category": 'registry-ideas-kitchen-essentials',
            "department": 'registry-ideas',
        },
        'registry-ideas-modern-minimalist': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/modern-minimalist?id=1035374',
            "category": 'registry-ideas-modern-minimalist',
            "department": 'registry-ideas',
        },
        'registry-ideas-most-registered-for': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/most-registered-for?id=1192769',
            "category": 'registry-ideas-most-registered-for',
            "department": 'registry-ideas',
        },
        'registry-ideas-new-years-celebration': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/new-years-celebration?id=1062664',
            "category": 'registry-ideas-new-years-celebration',
            "department": 'registry-ideas',
        },
        'registry-ideas-perfect-staycation': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/perfect-staycation?id=1062663',
            "category": 'registry-ideas-perfect-staycation',
            "department": 'registry-ideas',
        },
        'registry-ideas-romantic-dinner': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/romantic-dinner?id=1062662',
            "category": 'registry-ideas-romantic-dinner',
            "department": 'registry-ideas',
        },
        'registry-ideas-rustic-chic': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/rustic-chic?id=1035375',
            "category": 'registry-ideas-rustic-chic',
            "department": 'registry-ideas',
        },
        'registry-ideas-serveware-essentials': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/serveware-essentials?id=1239659',
            "category": 'registry-ideas-serveware-essentials',
            "department": 'registry-ideas',
        },
        'registry-ideas-thanksgiving-feast': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/thanksgiving-feast?id=1062660',
            "category": 'registry-ideas-thanksgiving-feast',
            "department": 'registry-ideas',
        },
        'registry-ideas-timelessly-elegant': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/timelessly-elegant?id=1035373',
            "category": 'registry-ideas-timelessly-elegant',
            "department": 'registry-ideas',
        },
        'registry-ideas-ultimate-birthday-party': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/ultimate-birthday-party?id=1062659',
            "category": 'registry-ideas-ultimate-birthday-party',
            "department": 'registry-ideas',
        },
        'registry-ideas-unexpected-luxuries': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/unexpected-luxuries?id=1193763',
            "category": 'registry-ideas-unexpected-luxuries',
            "department": 'registry-ideas',
        },
        'registry-ideas-urban-industrial': {
            "url": 'https://www.bloomingdales.com/shop/registry-ideas/urban-industrial?id=1035361',
            "category": 'registry-ideas-urban-industrial',
            "department": 'registry-ideas',
        },
    },
    'registry-video-hub': {
        'registry-video-hub': {
            "url": 'https://www.bloomingdales.com/shop/registry-video-hub?id=1040759',
            "category": 'registry-video-hub',
            "department": 'registry-video-hub',
        },
    },
    'reiss': {
        'reiss': {
            "url": 'https://www.bloomingdales.com/shop/reiss?id=1212964',
            "category": 'reiss',
            "department": 'reiss',
        },
        'reiss-mens': {
            "url": 'https://www.bloomingdales.com/shop/reiss/mens?id=1212966',
            "category": 'reiss-mens',
            "department": 'reiss',
        },
        'reiss-sale': {
            "url": 'https://www.bloomingdales.com/shop/reiss/sale?id=1250795',
            "category": 'reiss-sale',
            "department": 'reiss',
        },
        'reiss-womens': {
            "url": 'https://www.bloomingdales.com/shop/reiss/womens?id=1212965',
            "category": 'reiss-womens',
            "department": 'reiss',
        },
    },
    'repossi': {
        'repossi': {
            "url": 'https://www.bloomingdales.com/shop/repossi?id=1326004',
            "category": 'repossi',
            "department": 'repossi',
        },
    },
    'represent': {
        'represent': {
            "url": 'https://www.bloomingdales.com/shop/represent?id=1308097',
            "category": 'represent',
            "department": 'represent',
        },
    },
    'resort-trends': {
        'resort-trends': {
            "url": 'https://www.bloomingdales.com/shop/resort-trends?id=1005512',
            "category": 'resort-trends',
            "department": 'resort-trends',
        },
    },
    'revive': {
        'revive': {
            "url": 'https://www.bloomingdales.com/shop/revive?id=1283215',
            "category": 'revive',
            "department": 'revive',
        },
    },
    'rhone': {
        'rhone': {
            "url": 'https://www.bloomingdales.com/shop/rhone?id=1304604',
            "category": 'rhone',
            "department": 'rhone',
        },
        'rhone-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/rhone/mens-clothing?id=1304606',
            "category": 'rhone-mens-clothing',
            "department": 'rhone',
        },
        'rhone-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/rhone/womens-clothing?id=1304605',
            "category": 'rhone-womens-clothing',
            "department": 'rhone',
        },
    },
    'rib-subcat-1': {
        'rib-subcat-1': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-1?id=1138583',
            "category": 'rib-subcat-1',
            "department": 'rib-subcat-1',
        },
    },
    'rib-subcat-2': {
        'rib-subcat-2': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-2?id=1138580',
            "category": 'rib-subcat-2',
            "department": 'rib-subcat-2',
        },
    },
    'rib-subcat-3': {
        'rib-subcat-3': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-3?id=1138581',
            "category": 'rib-subcat-3',
            "department": 'rib-subcat-3',
        },
    },
    'rib-subcat-4': {
        'rib-subcat-4': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-4?id=1138561',
            "category": 'rib-subcat-4',
            "department": 'rib-subcat-4',
        },
    },
    'rib-subcat-5': {
        'rib-subcat-5': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-5?id=1138562',
            "category": 'rib-subcat-5',
            "department": 'rib-subcat-5',
        },
    },
    'rib-subcat-6': {
        'rib-subcat-6': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-6?id=1138564',
            "category": 'rib-subcat-6',
            "department": 'rib-subcat-6',
        },
    },
    'rib-subcat-7': {
        'rib-subcat-7': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-7?id=1138571',
            "category": 'rib-subcat-7',
            "department": 'rib-subcat-7',
        },
    },
    'rib-subcat-8': {
        'rib-subcat-8': {
            "url": 'https://www.bloomingdales.com/shop/rib-subcat-8?id=1138560',
            "category": 'rib-subcat-8',
            "department": 'rib-subcat-8',
        },
    },
    'roasting-pans': {
        'roasting-pans': {
            "url": 'https://www.bloomingdales.com/shop/roasting-pans?id=1039380',
            "category": 'roasting-pans',
            "department": 'roasting-pans',
        },
    },
    'robert-graham': {
        'robert-graham': {
            "url": 'https://www.bloomingdales.com/shop/robert-graham?id=1006354',
            "category": 'robert-graham',
            "department": 'robert-graham',
        },
    },
    'roberto-coin': {
        'roberto-coin': {
            "url": 'https://www.bloomingdales.com/shop/roberto-coin?id=1003845',
            "category": 'roberto-coin',
            "department": 'roberto-coin',
        },
        'roberto-coin-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/roberto-coin/bracelets?id=1006757',
            "category": 'roberto-coin-bracelets',
            "department": 'roberto-coin',
        },
        'roberto-coin-earrings': {
            "url": 'https://www.bloomingdales.com/shop/roberto-coin/earrings?id=1006758',
            "category": 'roberto-coin-earrings',
            "department": 'roberto-coin',
        },
        'roberto-coin-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/roberto-coin/necklaces?id=1006759',
            "category": 'roberto-coin-necklaces',
            "department": 'roberto-coin',
        },
        'roberto-coin-rings': {
            "url": 'https://www.bloomingdales.com/shop/roberto-coin/rings?id=1006760',
            "category": 'roberto-coin-rings',
            "department": 'roberto-coin',
        },
    },
    'rodd-gunn': {
        'rodd-gunn': {
            "url": 'https://www.bloomingdales.com/shop/rodd-gunn?id=1242594',
            "category": 'rodd-gunn',
            "department": 'rodd-gunn',
        },
        'rodd-gunn-accessories': {
            "url": 'https://www.bloomingdales.com/shop/rodd-gunn/accessories?id=1323502',
            "category": 'rodd-gunn-accessories',
            "department": 'rodd-gunn',
        },
        'rodd-gunn-clothing': {
            "url": 'https://www.bloomingdales.com/shop/rodd-gunn/clothing?id=1323501',
            "category": 'rodd-gunn-clothing',
            "department": 'rodd-gunn',
        },
        'rodd-gunn-multi-buys': {
            "url": 'https://www.bloomingdales.com/shop/rodd-gunn/multi-buys?id=1323503',
            "category": 'rodd-gunn-multi-buys',
            "department": 'rodd-gunn',
        },
    },
    'rosy-hues': {
        'rosy-hues': {
            "url": 'https://www.bloomingdales.com/shop/rosy-hues?id=1003017',
            "category": 'rosy-hues',
            "department": 'rosy-hues',
        },
    },
    'saint-laurent': {
        'saint-laurent': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent?id=1100159',
            "category": 'saint-laurent',
            "department": 'saint-laurent',
        },
        'saint-laurent-boots': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/boots?id=1288298',
            "category": 'saint-laurent-boots',
            "department": 'saint-laurent',
        },
        'saint-laurent-clutches': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/clutches?id=1278838',
            "category": 'saint-laurent-clutches',
            "department": 'saint-laurent',
        },
        'saint-laurent-crossbody-bags': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/crossbody-bags?id=1278836',
            "category": 'saint-laurent-crossbody-bags',
            "department": 'saint-laurent',
        },
        'saint-laurent-flats': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/flats?id=1288302',
            "category": 'saint-laurent-flats',
            "department": 'saint-laurent',
        },
        'saint-laurent-mens-accessories': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/mens-accessories?id=1308611',
            "category": 'saint-laurent-mens-accessories',
            "department": 'saint-laurent',
        },
        'saint-laurent-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/mens-shoes?id=1308612',
            "category": 'saint-laurent-mens-shoes',
            "department": 'saint-laurent',
        },
        'saint-laurent-mini-bags': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/mini-bags?id=1288195',
            "category": 'saint-laurent-mini-bags',
            "department": 'saint-laurent',
        },
        'saint-laurent-pumps': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/pumps?id=1288300',
            "category": 'saint-laurent-pumps',
            "department": 'saint-laurent',
        },
        'saint-laurent-raffia-bags': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/raffia-bags?id=1288197',
            "category": 'saint-laurent-raffia-bags',
            "department": 'saint-laurent',
        },
        'saint-laurent-saint-laurent-bags': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/saint-laurent-bags?id=1136659',
            "category": 'saint-laurent-saint-laurent-bags',
            "department": 'saint-laurent',
        },
        'saint-laurent-saint-laurent-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/saint-laurent-jewelry-accessories?id=1101059',
            "category": 'saint-laurent-saint-laurent-jewelry-accessories',
            "department": 'saint-laurent',
        },
        'saint-laurent-saint-laurent-shoes': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/saint-laurent-shoes?id=1100160',
            "category": 'saint-laurent-saint-laurent-shoes',
            "department": 'saint-laurent',
        },
        'saint-laurent-sandals': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/sandals?id=1288299',
            "category": 'saint-laurent-sandals',
            "department": 'saint-laurent',
        },
        'saint-laurent-shop-all-women': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/shop-all-women?id=1184375',
            "category": 'saint-laurent-shop-all-women',
            "department": 'saint-laurent',
        },
        'saint-laurent-shoulder-bags': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/shoulder-bags?id=1278839',
            "category": 'saint-laurent-shoulder-bags',
            "department": 'saint-laurent',
        },
        'saint-laurent-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/sneakers?id=1288301',
            "category": 'saint-laurent-sneakers',
            "department": 'saint-laurent',
        },
        'saint-laurent-suede-bags': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/suede-bags?id=1288196',
            "category": 'saint-laurent-suede-bags',
            "department": 'saint-laurent',
        },
        'saint-laurent-totes': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/totes?id=1278837',
            "category": 'saint-laurent-totes',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-beauty': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-beauty?id=1100759',
            "category": 'saint-laurent-ysl-beauty',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-black-opium': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-black-opium?id=1265603',
            "category": 'saint-laurent-ysl-black-opium',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-cologne': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-cologne?id=1265599',
            "category": 'saint-laurent-ysl-cologne',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-le-vestiaire-des-parfums': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-le-vestiaire-des-parfums?id=1309895',
            "category": 'saint-laurent-ysl-le-vestiaire-des-parfums',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-libre': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-libre?id=1265601',
            "category": 'saint-laurent-ysl-libre',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-lipstick': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-lipstick?id=1265600',
            "category": 'saint-laurent-ysl-lipstick',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-makeup': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-makeup?id=1265597',
            "category": 'saint-laurent-ysl-makeup',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-perfume': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-perfume?id=1265598',
            "category": 'saint-laurent-ysl-perfume',
            "department": 'saint-laurent',
        },
        'saint-laurent-ysl-y': {
            "url": 'https://www.bloomingdales.com/shop/saint-laurent/ysl-y?id=1265602',
            "category": 'saint-laurent-ysl-y',
            "department": 'saint-laurent',
        },
    },
    'sale': {
        'sale': {
            "url": 'https://www.bloomingdales.com/shop/sale?id=3977',
            "category": 'sale',
            "department": 'sale',
        },
        'sale-baby-shop-gear-essentials': {
            "url": 'https://www.bloomingdales.com/shop/sale/baby-shop-gear-essentials?id=1141060',
            "category": 'sale-baby-shop-gear-essentials',
            "department": 'sale',
        },
        'sale-bath': {
            "url": 'https://www.bloomingdales.com/shop/sale/bath?id=1006797',
            "category": 'sale-bath',
            "department": 'sale',
        },
        'sale-bathing-suits-swimsuits-bikini': {
            "url": 'https://www.bloomingdales.com/shop/sale/bathing-suits-swimsuits-bikini?id=1057659',
            "category": 'sale-bathing-suits-swimsuits-bikini',
            "department": 'sale',
        },
        'sale-beauty': {
            "url": 'https://www.bloomingdales.com/shop/sale/beauty?id=1020359',
            "category": 'sale-beauty',
            "department": 'sale',
        },
        'sale-bedding': {
            "url": 'https://www.bloomingdales.com/shop/sale/bedding?id=1006798',
            "category": 'sale-bedding',
            "department": 'sale',
        },
        'sale-big-boy-clothes': {
            "url": 'https://www.bloomingdales.com/shop/sale/big-boy-clothes?id=1006731',
            "category": 'sale-big-boy-clothes',
            "department": 'sale',
        },
        'sale-big-girls-clothes-dresses': {
            "url": 'https://www.bloomingdales.com/shop/sale/big-girls-clothes-dresses?id=1006728',
            "category": 'sale-big-girls-clothes-dresses',
            "department": 'sale',
        },
        'sale-black-friday-deals': {
            "url": 'https://www.bloomingdales.com/shop/sale/black-friday-deals?id=1005423',
            "category": 'sale-black-friday-deals',
            "department": 'sale',
        },
        'sale-blazers-suits-tuxedos': {
            "url": 'https://www.bloomingdales.com/shop/sale/blazers-suits-tuxedos?id=1006772',
            "category": 'sale-blazers-suits-tuxedos',
            "department": 'sale',
        },
        'sale-boys-shoes-sneakers-boots-hats': {
            "url": 'https://www.bloomingdales.com/shop/sale/boys-shoes-sneakers-boots-hats?id=1006732',
            "category": 'sale-boys-shoes-sneakers-boots-hats',
            "department": 'sale',
        },
        'sale-casual-button-down-shirts': {
            "url": 'https://www.bloomingdales.com/shop/sale/casual-button-down-shirts?id=1006773',
            "category": 'sale-casual-button-down-shirts',
            "department": 'sale',
        },
        'sale-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/clearance?id=1005000',
            "category": 'sale-clearance',
            "department": 'sale',
        },
        'sale-clothing': {
            "url": 'https://www.bloomingdales.com/shop/sale/clothing?id=1063960',
            "category": 'sale-clothing',
            "department": 'sale',
        },
        'sale-clutches-mini-bags': {
            "url": 'https://www.bloomingdales.com/shop/sale/clutches-mini-bags?id=1005683',
            "category": 'sale-clutches-mini-bags',
            "department": 'sale',
        },
        'sale-coffee-makers-blenders-toasters-juicers': {
            "url": 'https://www.bloomingdales.com/shop/sale/coffee-makers-blenders-toasters-juicers?id=1006801',
            "category": 'sale-coffee-makers-blenders-toasters-juicers',
            "department": 'sale',
        },
        'sale-cookware-bakeware': {
            "url": 'https://www.bloomingdales.com/shop/sale/cookware-bakeware?id=1006802',
            "category": 'sale-cookware-bakeware',
            "department": 'sale',
        },
        'sale-crossbody-bags': {
            "url": 'https://www.bloomingdales.com/shop/sale/crossbody-bags?id=1005685',
            "category": 'sale-crossbody-bags',
            "department": 'sale',
        },
        'sale-cutlery-knives': {
            "url": 'https://www.bloomingdales.com/shop/sale/cutlery-knives?id=1006807',
            "category": 'sale-cutlery-knives',
            "department": 'sale',
        },
        'sale-cyber-monday-deals': {
            "url": 'https://www.bloomingdales.com/shop/sale/cyber-monday-deals?id=1005425',
            "category": 'sale-cyber-monday-deals',
            "department": 'sale',
        },
        'sale-designer-private-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/designer-private-sale?id=1127359',
            "category": 'sale-designer-private-sale',
            "department": 'sale',
        },
        'sale-diamond-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/sale/diamond-bracelets?id=1011159',
            "category": 'sale-diamond-bracelets',
            "department": 'sale',
        },
        'sale-diamond-earrings': {
            "url": 'https://www.bloomingdales.com/shop/sale/diamond-earrings?id=1011161',
            "category": 'sale-diamond-earrings',
            "department": 'sale',
        },
        'sale-diamond-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/sale/diamond-necklaces?id=1011162',
            "category": 'sale-diamond-necklaces',
            "department": 'sale',
        },
        'sale-diamond-rings': {
            "url": 'https://www.bloomingdales.com/shop/sale/diamond-rings?id=1011163',
            "category": 'sale-diamond-rings',
            "department": 'sale',
        },
        'sale-diamonds': {
            "url": 'https://www.bloomingdales.com/shop/sale/diamonds?id=1139959',
            "category": 'sale-diamonds',
            "department": 'sale',
        },
        'sale-dinnerware-flatware': {
            "url": 'https://www.bloomingdales.com/shop/sale/dinnerware-flatware?id=1006800',
            "category": 'sale-dinnerware-flatware',
            "department": 'sale',
        },
        'sale-dress-shirts': {
            "url": 'https://www.bloomingdales.com/shop/sale/dress-shirts?id=1006775',
            "category": 'sale-dress-shirts',
            "department": 'sale',
        },
        'sale-dresses-gowns': {
            "url": 'https://www.bloomingdales.com/shop/sale/dresses-gowns?id=1006738',
            "category": 'sale-dresses-gowns',
            "department": 'sale',
        },
        'sale-fashion-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/sale/fashion-jewelry?id=1006047',
            "category": 'sale-fashion-jewelry',
            "department": 'sale',
        },
        'sale-fine-jewelry': {
            "url": 'https://www.bloomingdales.com/shop/sale/fine-jewelry?id=1001014',
            "category": 'sale-fine-jewelry',
            "department": 'sale',
        },
        'sale-fine-jewelry-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/fine-jewelry-clearance?id=1004975',
            "category": 'sale-fine-jewelry-clearance',
            "department": 'sale',
        },
        'sale-fragrance-on-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/fragrance-on-sale?id=1333096',
            "category": 'sale-fragrance-on-sale',
            "department": 'sale',
        },
        'sale-friends-family-deals': {
            "url": 'https://www.bloomingdales.com/shop/sale/friends-family-deals?id=1005426',
            "category": 'sale-friends-family-deals',
            "department": 'sale',
        },
        'sale-furniture': {
            "url": 'https://www.bloomingdales.com/shop/sale/furniture?id=1006809',
            "category": 'sale-furniture',
            "department": 'sale',
        },
        'sale-gift-sets-on-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/gift-sets-on-sale?id=1333098',
            "category": 'sale-gift-sets-on-sale',
            "department": 'sale',
        },
        'sale-girls-shoes-boots-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/sale/girls-shoes-boots-sneakers?id=1006729',
            "category": 'sale-girls-shoes-boots-sneakers',
            "department": 'sale',
        },
        'sale-haircare-on-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/haircare-on-sale?id=1333097',
            "category": 'sale-haircare-on-sale',
            "department": 'sale',
        },
        'sale-handbags-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/handbags-clearance?id=1004976',
            "category": 'sale-handbags-clearance',
            "department": 'sale',
        },
        'sale-handbags-purses': {
            "url": 'https://www.bloomingdales.com/shop/sale/handbags-purses?id=5070',
            "category": 'sale-handbags-purses',
            "department": 'sale',
        },
        'sale-hobo-shoulder-bags': {
            "url": 'https://www.bloomingdales.com/shop/sale/hobo-shoulder-bags?id=1005684',
            "category": 'sale-hobo-shoulder-bags',
            "department": 'sale',
        },
        'sale-home': {
            "url": 'https://www.bloomingdales.com/shop/sale/home?id=6466',
            "category": 'sale-home',
            "department": 'sale',
        },
        'sale-home-decor': {
            "url": 'https://www.bloomingdales.com/shop/sale/home-decor?id=1006803',
            "category": 'sale-home-decor',
            "department": 'sale',
        },
        'sale-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/sale/jewelry-accessories?id=5303',
            "category": 'sale-jewelry-accessories',
            "department": 'sale',
        },
        'sale-jewelry-accessories-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/jewelry-accessories-clearance?id=1005025',
            "category": 'sale-jewelry-accessories-clearance',
            "department": 'sale',
        },
        'sale-jumpsuits-rompers': {
            "url": 'https://www.bloomingdales.com/shop/sale/jumpsuits-rompers?id=1006741',
            "category": 'sale-jumpsuits-rompers',
            "department": 'sale',
        },
        'sale-kids-clothes-shoes': {
            "url": 'https://www.bloomingdales.com/shop/sale/kids-clothes-shoes?id=5320',
            "category": 'sale-kids-clothes-shoes',
            "department": 'sale',
        },
        'sale-lighting': {
            "url": 'https://www.bloomingdales.com/shop/sale/lighting?id=1006808',
            "category": 'sale-lighting',
            "department": 'sale',
        },
        'sale-little-boys-clothes': {
            "url": 'https://www.bloomingdales.com/shop/sale/little-boys-clothes?id=1006730',
            "category": 'sale-little-boys-clothes',
            "department": 'sale',
        },
        'sale-little-girls-clothes-dresses': {
            "url": 'https://www.bloomingdales.com/shop/sale/little-girls-clothes-dresses?id=1006727',
            "category": 'sale-little-girls-clothes-dresses',
            "department": 'sale',
        },
        'sale-luggage-travel': {
            "url": 'https://www.bloomingdales.com/shop/sale/luggage-travel?id=1006804',
            "category": 'sale-luggage-travel',
            "department": 'sale',
        },
        'sale-makeup-on-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/makeup-on-sale?id=1333095',
            "category": 'sale-makeup-on-sale',
            "department": 'sale',
        },
        'sale-mattresses': {
            "url": 'https://www.bloomingdales.com/shop/sale/mattresses?id=1006810',
            "category": 'sale-mattresses',
            "department": 'sale',
        },
        'sale-men': {
            "url": 'https://www.bloomingdales.com/shop/sale/men?id=1001174',
            "category": 'sale-men',
            "department": 'sale',
        },
        'sale-mens-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-clearance?id=1004996',
            "category": 'sale-mens-clearance',
            "department": 'sale',
        },
        'sale-mens-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-coats-jackets?id=1006774',
            "category": 'sale-mens-coats-jackets',
            "department": 'sale',
        },
        'sale-mens-designer-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-designer-sale?id=1005372',
            "category": 'sale-mens-designer-sale',
            "department": 'sale',
        },
        'sale-mens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-jeans?id=1006776',
            "category": 'sale-mens-jeans',
            "department": 'sale',
        },
        'sale-mens-pants-shorts': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-pants-shorts?id=1006777',
            "category": 'sale-mens-pants-shorts',
            "department": 'sale',
        },
        'sale-mens-polos-t-shirts': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-polos-t-shirts?id=1006778',
            "category": 'sale-mens-polos-t-shirts',
            "department": 'sale',
        },
        'sale-mens-shoes-boots-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-shoes-boots-sneakers?id=1006795',
            "category": 'sale-mens-shoes-boots-sneakers',
            "department": 'sale',
        },
        'sale-mens-sweaters-hoodies-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-sweaters-hoodies-sweatshirts?id=1006780',
            "category": 'sale-mens-sweaters-hoodies-sweatshirts',
            "department": 'sale',
        },
        'sale-mens-swimwear-swim-trunks': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-swimwear-swim-trunks?id=1006793',
            "category": 'sale-mens-swimwear-swim-trunks',
            "department": 'sale',
        },
        'sale-mens-underwear-boxers-briefs': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-underwear-boxers-briefs?id=1006794',
            "category": 'sale-mens-underwear-boxers-briefs',
            "department": 'sale',
        },
        'sale-mens-wallets-belts-ties-watches': {
            "url": 'https://www.bloomingdales.com/shop/sale/mens-wallets-belts-ties-watches?id=1006796',
            "category": 'sale-mens-wallets-belts-ties-watches',
            "department": 'sale',
        },
        'sale-new-markdowns': {
            "url": 'https://www.bloomingdales.com/shop/sale/new-markdowns?id=1064059',
            "category": 'sale-new-markdowns',
            "department": 'sale',
        },
        'sale-new-to-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/new-to-sale?id=1319103',
            "category": 'sale-new-to-sale',
            "department": 'sale',
        },
        'sale-newborn-baby-boy-clothes': {
            "url": 'https://www.bloomingdales.com/shop/sale/newborn-baby-boy-clothes?id=1006726',
            "category": 'sale-newborn-baby-boy-clothes',
            "department": 'sale',
        },
        'sale-newborn-baby-clothes-unisex': {
            "url": 'https://www.bloomingdales.com/shop/sale/newborn-baby-clothes-unisex?id=1006724',
            "category": 'sale-newborn-baby-clothes-unisex',
            "department": 'sale',
        },
        'sale-newborn-baby-girl-clothes-dresses': {
            "url": 'https://www.bloomingdales.com/shop/sale/newborn-baby-girl-clothes-dresses?id=1006725',
            "category": 'sale-newborn-baby-girl-clothes-dresses',
            "department": 'sale',
        },
        'sale-offers-promotions': {
            "url": 'https://www.bloomingdales.com/shop/sale/offers-promotions?id=1058459',
            "category": 'sale-offers-promotions',
            "department": 'sale',
        },
        'sale-one-day-home-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/one-day-home-sale?id=1005902',
            "category": 'sale-one-day-home-sale',
            "department": 'sale',
        },
        'sale-pillows-comforters': {
            "url": 'https://www.bloomingdales.com/shop/sale/pillows-comforters?id=1006799',
            "category": 'sale-pillows-comforters',
            "department": 'sale',
        },
        'sale-plus-size-clothing': {
            "url": 'https://www.bloomingdales.com/shop/sale/plus-size-clothing?id=5220',
            "category": 'sale-plus-size-clothing',
            "department": 'sale',
        },
        'sale-rugs': {
            "url": 'https://www.bloomingdales.com/shop/sale/rugs?id=1006805',
            "category": 'sale-rugs',
            "department": 'sale',
        },
        'sale-sale-and-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/sale-and-clearance?id=1003304',
            "category": 'sale-sale-and-clearance',
            "department": 'sale',
        },
        'sale-satchels': {
            "url": 'https://www.bloomingdales.com/shop/sale/satchels?id=1005686',
            "category": 'sale-satchels',
            "department": 'sale',
        },
        'sale-scarves-hats-gloves': {
            "url": 'https://www.bloomingdales.com/shop/sale/scarves-hats-gloves?id=1006048',
            "category": 'sale-scarves-hats-gloves',
            "department": 'sale',
        },
        'sale-shoes': {
            "url": 'https://www.bloomingdales.com/shop/sale/shoes?id=1063961',
            "category": 'sale-shoes',
            "department": 'sale',
        },
        'sale-shoes-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/shoes-clearance?id=1004982',
            "category": 'sale-shoes-clearance',
            "department": 'sale',
        },
        'sale-skincare-on-sale': {
            "url": 'https://www.bloomingdales.com/shop/sale/skincare-on-sale?id=1331595',
            "category": 'sale-skincare-on-sale',
            "department": 'sale',
        },
        'sale-sleepwear-lounge': {
            "url": 'https://www.bloomingdales.com/shop/sale/sleepwear-lounge?id=1141263',
            "category": 'sale-sleepwear-lounge',
            "department": 'sale',
        },
        'sale-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/sale/sunglasses?id=1006051',
            "category": 'sale-sunglasses',
            "department": 'sale',
        },
        'sale-the-final-offer': {
            "url": 'https://www.bloomingdales.com/shop/sale/the-final-offer?id=1063567',
            "category": 'sale-the-final-offer',
            "department": 'sale',
        },
        'sale-under-100-sale-picks': {
            "url": 'https://www.bloomingdales.com/shop/sale/under-100-sale-picks?id=1206165',
            "category": 'sale-under-100-sale-picks',
            "department": 'sale',
        },
        'sale-under-50-sale-picks': {
            "url": 'https://www.bloomingdales.com/shop/sale/under-50-sale-picks?id=1246895',
            "category": 'sale-under-50-sale-picks',
            "department": 'sale',
        },
        'sale-watches': {
            "url": 'https://www.bloomingdales.com/shop/sale/watches?id=1006050',
            "category": 'sale-watches',
            "department": 'sale',
        },
        'sale-wedges-platform-sandals': {
            "url": 'https://www.bloomingdales.com/shop/sale/wedges-platform-sandals?id=1005980',
            "category": 'sale-wedges-platform-sandals',
            "department": 'sale',
        },
        'sale-womens-activewear-workout-clothes': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-activewear-workout-clothes?id=1006736',
            "category": 'sale-womens-activewear-workout-clothes',
            "department": 'sale',
        },
        'sale-womens-backpacks-travel-overnight-bags': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-backpacks-travel-overnight-bags?id=1005682',
            "category": 'sale-womens-backpacks-travel-overnight-bags',
            "department": 'sale',
        },
        'sale-womens-clearance': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-clearance?id=1004977',
            "category": 'sale-womens-clearance',
            "department": 'sale',
        },
        'sale-womens-clothes': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-clothes?id=1319401',
            "category": 'sale-womens-clothes',
            "department": 'sale',
        },
        'sale-womens-coats': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-coats?id=1006737',
            "category": 'sale-womens-coats',
            "department": 'sale',
        },
        'sale-womens-designer-boots': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-designer-boots?id=1005966',
            "category": 'sale-womens-designer-boots',
            "department": 'sale',
        },
        'sale-womens-designer-handbags': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-designer-handbags?id=1065661',
            "category": 'sale-womens-designer-handbags',
            "department": 'sale',
        },
        'sale-womens-designer-shoes': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-designer-shoes?id=4841',
            "category": 'sale-womens-designer-shoes',
            "department": 'sale',
        },
        'sale-womens-flats': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-flats?id=1005969',
            "category": 'sale-womens-flats',
            "department": 'sale',
        },
        'sale-womens-jeans': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-jeans?id=1006740',
            "category": 'sale-womens-jeans',
            "department": 'sale',
        },
        'sale-womens-pants': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-pants?id=1006743',
            "category": 'sale-womens-pants',
            "department": 'sale',
        },
        'sale-womens-pumps': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-pumps?id=1005971',
            "category": 'sale-womens-pumps',
            "department": 'sale',
        },
        'sale-womens-rain-snow-winter-boots': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-rain-snow-winter-boots?id=1005973',
            "category": 'sale-womens-rain-snow-winter-boots',
            "department": 'sale',
        },
        'sale-womens-robes-pajamas-sleepwear': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-robes-pajamas-sleepwear?id=1006745',
            "category": 'sale-womens-robes-pajamas-sleepwear',
            "department": 'sale',
        },
        'sale-womens-sandals-flip-flops': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-sandals-flip-flops?id=1005978',
            "category": 'sale-womens-sandals-flip-flops',
            "department": 'sale',
        },
        'sale-womens-shorts-skirts': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-shorts-skirts?id=1006744',
            "category": 'sale-womens-shorts-skirts',
            "department": 'sale',
        },
        'sale-womens-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-sneakers?id=1005979',
            "category": 'sale-womens-sneakers',
            "department": 'sale',
        },
        'sale-womens-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-sweaters?id=1006746',
            "category": 'sale-womens-sweaters',
            "department": 'sale',
        },
        'sale-womens-sweatpants-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-sweatpants-sweatshirts?id=1021963',
            "category": 'sale-womens-sweatpants-sweatshirts',
            "department": 'sale',
        },
        'sale-womens-tops-blouses-hoodies': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-tops-blouses-hoodies?id=1006748',
            "category": 'sale-womens-tops-blouses-hoodies',
            "department": 'sale',
        },
        'sale-womens-tote-bags': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-tote-bags?id=1005687',
            "category": 'sale-womens-tote-bags',
            "department": 'sale',
        },
        'sale-womens-walking-comfort-shoes': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-walking-comfort-shoes?id=1005968',
            "category": 'sale-womens-walking-comfort-shoes',
            "department": 'sale',
        },
        'sale-womens-wallets-accessories': {
            "url": 'https://www.bloomingdales.com/shop/sale/womens-wallets-accessories?id=1005688',
            "category": 'sale-womens-wallets-accessories',
            "department": 'sale',
        },
    },
    'sam-edelman': {
        'sam-edelman': {
            "url": 'https://www.bloomingdales.com/shop/sam-edelman?id=1003823',
            "category": 'sam-edelman',
            "department": 'sam-edelman',
        },
        'sam-edelman-kids': {
            "url": 'https://www.bloomingdales.com/shop/sam-edelman/kids?id=1003831',
            "category": 'sam-edelman-kids',
            "department": 'sam-edelman',
        },
    },
    'sandro': {
        'sandro': {
            "url": 'https://www.bloomingdales.com/shop/sandro?id=1212960',
            "category": 'sandro',
            "department": 'sandro',
        },
        'sandro-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/sandro/mens-clothing?id=1212963',
            "category": 'sandro-mens-clothing',
            "department": 'sandro',
        },
        'sandro-sandro-sale': {
            "url": 'https://www.bloomingdales.com/shop/sandro/sandro-sale?id=1250962',
            "category": 'sandro-sandro-sale',
            "department": 'sandro',
        },
        'sandro-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/sandro/womens-clothing?id=1212961',
            "category": 'sandro-womens-clothing',
            "department": 'sandro',
        },
        'sandro-womens-shoes-accessories': {
            "url": 'https://www.bloomingdales.com/shop/sandro/womens-shoes-accessories?id=1212962',
            "category": 'sandro-womens-shoes-accessories',
            "department": 'sandro',
        },
    },
    'sauce-pans': {
        'sauce-pans': {
            "url": 'https://www.bloomingdales.com/shop/sauce-pans?id=1039381',
            "category": 'sauce-pans',
            "department": 'sauce-pans',
        },
    },
    'saute-pans': {
        'saute-pans': {
            "url": 'https://www.bloomingdales.com/shop/saute-pans?id=1039382',
            "category": 'saute-pans',
            "department": 'saute-pans',
        },
    },
    'sferra': {
        'sferra': {
            "url": 'https://www.bloomingdales.com/shop/sferra?id=1162867',
            "category": 'sferra',
            "department": 'sferra',
        },
        'sferra-bath': {
            "url": 'https://www.bloomingdales.com/shop/sferra/bath?id=1162871',
            "category": 'sferra-bath',
            "department": 'sferra',
        },
        'sferra-bedding': {
            "url": 'https://www.bloomingdales.com/shop/sferra/bedding?id=1162868',
            "category": 'sferra-bedding',
            "department": 'sferra',
        },
        'sferra-blankets-and-throws': {
            "url": 'https://www.bloomingdales.com/shop/sferra/blankets-and-throws?id=1162872',
            "category": 'sferra-blankets-and-throws',
            "department": 'sferra',
        },
        'sferra-mattresses': {
            "url": 'https://www.bloomingdales.com/shop/sferra/mattresses?id=1162870',
            "category": 'sferra-mattresses',
            "department": 'sferra',
        },
        'sferra-pillows-comforters': {
            "url": 'https://www.bloomingdales.com/shop/sferra/pillows-comforters?id=1162869',
            "category": 'sferra-pillows-comforters',
            "department": 'sferra',
        },
        'sferra-table-linens': {
            "url": 'https://www.bloomingdales.com/shop/sferra/table-linens?id=1162873',
            "category": 'sferra-table-linens',
            "department": 'sferra',
        },
    },
    'shapewear-hosiery': {
        'shapewear-hosiery': {
            "url": 'https://www.bloomingdales.com/shop/shapewear-hosiery?id=4361',
            "category": 'shapewear-hosiery',
            "department": 'shapewear-hosiery',
        },
    },
    'shiseido': {
        'shiseido': {
            "url": 'https://www.bloomingdales.com/shop/shiseido?id=1268310',
            "category": 'shiseido',
            "department": 'shiseido',
        },
    },
    'shoes': {
        'shoes': {
            "url": 'https://www.bloomingdales.com/shop/shoes?id=1319126',
            "category": 'shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes?id=16961',
            "category": 'womens-designer-shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes-all-fashion-shoes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/all-fashion-shoes?id=17411',
            "category": 'womens-designer-shoes-all-fashion-shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes-athleisure': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/athleisure?id=1309098',
            "category": 'womens-designer-shoes-athleisure',
            "department": 'shoes',
        },
        'womens-designer-shoes-athletic-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/athletic-sneakers?id=1005961',
            "category": 'womens-designer-shoes-athletic-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-ballet-flats': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/ballet-flats?id=1005942',
            "category": 'womens-designer-shoes-ballet-flats',
            "department": 'shoes',
        },
        'womens-designer-shoes-best-selling': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/best-selling?id=23268',
            "category": 'womens-designer-shoes-best-selling',
            "department": 'shoes',
        },
        'womens-designer-shoes-booties': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/booties?id=1000692',
            "category": 'womens-designer-shoes-booties',
            "department": 'shoes',
        },
        'womens-designer-shoes-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/boots?id=19212',
            "category": 'womens-designer-shoes-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-chelsea-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/chelsea-boots?id=1292880',
            "category": 'womens-designer-shoes-chelsea-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-combat-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/combat-boots?id=1005936',
            "category": 'womens-designer-shoes-combat-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-designer-boots-under-200': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/designer-boots-under-200?id=1000588',
            "category": 'womens-designer-shoes-designer-boots-under-200',
            "department": 'shoes',
        },
        'womens-designer-shoes-designer-sandals': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/designer-sandals?id=1273698',
            "category": 'womens-designer-shoes-designer-sandals',
            "department": 'shoes',
        },
        'womens-designer-shoes-designer-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/designer-sneakers?id=1271617',
            "category": 'womens-designer-shoes-designer-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-dress-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/dress-boots?id=1292881',
            "category": 'womens-designer-shoes-dress-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-fall-shoes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/fall-shoes?id=1280996',
            "category": 'womens-designer-shoes-fall-shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes-fashion-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/fashion-sneakers?id=1068859',
            "category": 'womens-designer-shoes-fashion-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-flats': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/flats?id=16963',
            "category": 'womens-designer-shoes-flats',
            "department": 'shoes',
        },
        'womens-designer-shoes-gym-training': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/gym-training?id=1309096',
            "category": 'womens-designer-shoes-gym-training',
            "department": 'shoes',
        },
        'womens-designer-shoes-heeled-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/heeled-boots?id=1334097',
            "category": 'womens-designer-shoes-heeled-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-heeled-sandals': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/heeled-sandals?id=1308095',
            "category": 'womens-designer-shoes-heeled-sandals',
            "department": 'shoes',
        },
        'womens-designer-shoes-heels': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/heels?id=1307501',
            "category": 'womens-designer-shoes-heels',
            "department": 'shoes',
        },
        'womens-designer-shoes-high-heels': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/high-heels?id=1060761',
            "category": 'womens-designer-shoes-high-heels',
            "department": 'shoes',
        },
        'womens-designer-shoes-high-top-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/high-top-sneakers?id=1005962',
            "category": 'womens-designer-shoes-high-top-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-kitten-heels': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/kitten-heels?id=1060759',
            "category": 'womens-designer-shoes-kitten-heels',
            "department": 'shoes',
        },
        'womens-designer-shoes-knee-high-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/knee-high-boots?id=1005941',
            "category": 'womens-designer-shoes-knee-high-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-loafers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/loafers?id=1005946',
            "category": 'womens-designer-shoes-loafers',
            "department": 'shoes',
        },
        'womens-designer-shoes-low-heel-sandals': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/low-heel-sandals?id=1057259',
            "category": 'womens-designer-shoes-low-heel-sandals',
            "department": 'shoes',
        },
        'womens-designer-shoes-low-profile': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/low-profile?id=1308800',
            "category": 'womens-designer-shoes-low-profile',
            "department": 'shoes',
        },
        'womens-designer-shoes-low-top-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/low-top-sneakers?id=1005963',
            "category": 'womens-designer-shoes-low-top-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-lug-sole-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/lug-sole-boots?id=1292882',
            "category": 'womens-designer-shoes-lug-sole-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-mary-janes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/mary-janes?id=1292900',
            "category": 'womens-designer-shoes-mary-janes',
            "department": 'shoes',
        },
        'womens-designer-shoes-mid-calf-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/mid-calf-boots?id=1292885',
            "category": 'womens-designer-shoes-mid-calf-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-mid-heel-sandals': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/mid-heel-sandals?id=1273695',
            "category": 'womens-designer-shoes-mid-heel-sandals',
            "department": 'shoes',
        },
        'womens-designer-shoes-mid-heels': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/mid-heels?id=1060760',
            "category": 'womens-designer-shoes-mid-heels',
            "department": 'shoes',
        },
        'womens-designer-shoes-moto-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/moto-boots?id=1292887',
            "category": 'womens-designer-shoes-moto-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-mules-slides-shoes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/mules-slides-shoes?id=1048259',
            "category": 'womens-designer-shoes-mules-slides-shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes-platform-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/platform-sneakers?id=1068959',
            "category": 'womens-designer-shoes-platform-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-platforms-shoes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/platforms-shoes?id=17402',
            "category": 'womens-designer-shoes-platforms-shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes-pumps-high-heels-stilettos': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/pumps-high-heels-stilettos?id=17397',
            "category": 'womens-designer-shoes-pumps-high-heels-stilettos',
            "department": 'shoes',
        },
        'womens-designer-shoes-retro-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/retro-sneakers?id=1292905',
            "category": 'womens-designer-shoes-retro-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-riding-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/riding-boots?id=1292895',
            "category": 'womens-designer-shoes-riding-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-running': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/running?id=1309097',
            "category": 'womens-designer-shoes-running',
            "department": 'shoes',
        },
        'womens-designer-shoes-sandals-flip-flops': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/sandals-flip-flops?id=17398',
            "category": 'womens-designer-shoes-sandals-flip-flops',
            "department": 'shoes',
        },
        'womens-designer-shoes-sandals-under-150': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/sandals-under-150?id=17526',
            "category": 'womens-designer-shoes-sandals-under-150',
            "department": 'shoes',
        },
        'womens-designer-shoes-shoes-under-200': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/shoes-under-200?id=1009359',
            "category": 'womens-designer-shoes-shoes-under-200',
            "department": 'shoes',
        },
        'womens-designer-shoes-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/shop-all?id=1232772',
            "category": 'womens-designer-shoes-shop-all',
            "department": 'shoes',
        },
        'womens-designer-shoes-slide-shoes-for-women': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/slide-shoes-for-women?id=1077660',
            "category": 'womens-designer-shoes-slide-shoes-for-women',
            "department": 'shoes',
        },
        'womens-designer-shoes-slingbacks': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/slingbacks?id=1292902',
            "category": 'womens-designer-shoes-slingbacks',
            "department": 'shoes',
        },
        'womens-designer-shoes-slip-on-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/slip-on-sneakers?id=1005964',
            "category": 'womens-designer-shoes-slip-on-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-slippers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/slippers?id=17399',
            "category": 'womens-designer-shoes-slippers',
            "department": 'shoes',
        },
        'womens-designer-shoes-sneakers': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/sneakers?id=17400',
            "category": 'womens-designer-shoes-sneakers',
            "department": 'shoes',
        },
        'womens-designer-shoes-spring-shoes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/spring-shoes?id=1304717',
            "category": 'womens-designer-shoes-spring-shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes-stilettos': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/stilettos?id=1292903',
            "category": 'womens-designer-shoes-stilettos',
            "department": 'shoes',
        },
        'womens-designer-shoes-suede-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/suede-boots?id=1292897',
            "category": 'womens-designer-shoes-suede-boots',
            "department": 'shoes',
        },
        'womens-designer-shoes-thong-sandals': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/thong-sandals?id=1313895',
            "category": 'womens-designer-shoes-thong-sandals',
            "department": 'shoes',
        },
        'womens-designer-shoes-walking': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/walking?id=1309095',
            "category": 'womens-designer-shoes-walking',
            "department": 'shoes',
        },
        'womens-designer-shoes-wedding-bridal-prom-evening-shoes': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/wedding-bridal-prom-evening-shoes?id=17396',
            "category": 'womens-designer-shoes-wedding-bridal-prom-evening-shoes',
            "department": 'shoes',
        },
        'womens-designer-shoes-wedges': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/wedges?id=1057261',
            "category": 'womens-designer-shoes-wedges',
            "department": 'shoes',
        },
        'womens-designer-shoes-western-boots': {
            "url": 'https://www.bloomingdales.com/shop/womens-designer-shoes/western-boots?id=1292896',
            "category": 'womens-designer-shoes-western-boots',
            "department": 'shoes',
        },
    },
    'shoes-under-200': {
        'shoes-under-200': {
            "url": 'https://www.bloomingdales.com/shop/shoes-under-200?id=1151799',
            "category": 'shoes-under-200',
            "department": 'shoes-under-200',
        },
    },
    'shoes-under-300': {
        'shoes-under-300': {
            "url": 'https://www.bloomingdales.com/shop/shoes-under-300?id=1003752',
            "category": 'shoes-under-300',
            "department": 'shoes-under-300',
        },
    },
    'shop-all': {
        'shop-all': {
            "url": 'https://www.bloomingdales.com/shop/shop-all?id=1269423',
            "category": 'shop-all',
            "department": 'shop-all',
        },
    },
    'shop-all-men': {
        'shop-all-men': {
            "url": 'https://www.bloomingdales.com/shop/shop-all-men?id=1337902',
            "category": 'shop-all-men',
            "department": 'shop-all-men',
        },
    },
    'shop-all-versace': {
        'shop-all-versace': {
            "url": 'https://www.bloomingdales.com/shop/shop-all-versace?id=1182159',
            "category": 'shop-all-versace',
            "department": 'shop-all-versace',
        },
    },
    'shop-all-womens': {
        'shop-all-womens': {
            "url": 'https://www.bloomingdales.com/shop/shop-all-womens?id=1167660',
            "category": 'shop-all-womens',
            "department": 'shop-all-womens',
        },
    },
    'shop-by-color-caribbean': {
        'shop-by-color-caribbean': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-caribbean?id=1021560',
            "category": 'shop-by-color-caribbean',
            "department": 'shop-by-color-caribbean',
        },
    },
    'shop-by-color-cerise': {
        'shop-by-color-cerise': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-cerise?id=1021459',
            "category": 'shop-by-color-cerise',
            "department": 'shop-by-color-cerise',
        },
    },
    'shop-by-color-flame': {
        'shop-by-color-flame': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-flame?id=1021463',
            "category": 'shop-by-color-flame',
            "department": 'shop-by-color-flame',
        },
    },
    'shop-by-color-marine': {
        'shop-by-color-marine': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-marine?id=1032359',
            "category": 'shop-by-color-marine',
            "department": 'shop-by-color-marine',
        },
    },
    'shop-by-color-marseille': {
        'shop-by-color-marseille': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-marseille?id=1021460',
            "category": 'shop-by-color-marseille',
            "department": 'shop-by-color-marseille',
        },
    },
    'shop-by-color-oyster': {
        'shop-by-color-oyster': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-oyster?id=1032360',
            "category": 'shop-by-color-oyster',
            "department": 'shop-by-color-oyster',
        },
    },
    'shop-by-color-palm': {
        'shop-by-color-palm': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-palm?id=1021461',
            "category": 'shop-by-color-palm',
            "department": 'shop-by-color-palm',
        },
    },
    'shop-by-color-soleil': {
        'shop-by-color-soleil': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-soleil?id=1021559',
            "category": 'shop-by-color-soleil',
            "department": 'shop-by-color-soleil',
        },
    },
    'shop-by-color-stainless-steel': {
        'shop-by-color-stainless-steel': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-stainless-steel?id=1021561',
            "category": 'shop-by-color-stainless-steel',
            "department": 'shop-by-color-stainless-steel',
        },
    },
    'shop-by-color-white': {
        'shop-by-color-white': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-color-white?id=1021462',
            "category": 'shop-by-color-white',
            "department": 'shop-by-color-white',
        },
    },
    'shop-by-concern-wrinkles': {
        'shop-by-concern-wrinkles': {
            "url": 'https://www.bloomingdales.com/shop/shop-by-concern-wrinkles?id=1024069',
            "category": 'shop-by-concern-wrinkles',
            "department": 'shop-by-concern-wrinkles',
        },
    },
    'shorts-swim': {
        'shorts-swim': {
            "url": 'https://www.bloomingdales.com/shop/shorts-swim?id=1153759',
            "category": 'shorts-swim',
            "department": 'shorts-swim',
        },
    },
    'silver': {
        'silver': {
            "url": 'https://www.bloomingdales.com/shop/silver?id=1322214',
            "category": 'silver',
            "department": 'silver',
        },
    },
    'silver-cross': {
        'silver-cross': {
            "url": 'https://www.bloomingdales.com/shop/silver-cross?id=1320996',
            "category": 'silver-cross',
            "department": 'silver-cross',
        },
    },
    'simkhai': {
        'simkhai': {
            "url": 'https://www.bloomingdales.com/shop/simkhai?id=1097460',
            "category": 'simkhai',
            "department": 'simkhai',
        },
    },
    'sisley-paris': {
        'sisley-paris': {
            "url": 'https://www.bloomingdales.com/shop/sisley-paris?id=1279157',
            "category": 'sisley-paris',
            "department": 'sisley-paris',
        },
        'sisley-paris-hair-ritual-by-sisley-paris': {
            "url": 'https://www.bloomingdales.com/shop/sisley-paris/hair-ritual-by-sisley-paris?id=1316927',
            "category": 'sisley-paris-hair-ritual-by-sisley-paris',
            "department": 'sisley-paris',
        },
        'sisley-paris-sisley-paris-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/sisley-paris/sisley-paris-fragrance?id=1319097',
            "category": 'sisley-paris-sisley-paris-fragrance',
            "department": 'sisley-paris',
        },
        'sisley-paris-sisley-paris-gift-sets': {
            "url": 'https://www.bloomingdales.com/shop/sisley-paris/sisley-paris-gift-sets?id=1319095',
            "category": 'sisley-paris-sisley-paris-gift-sets',
            "department": 'sisley-paris',
        },
        'sisley-paris-sisley-paris-makeup': {
            "url": 'https://www.bloomingdales.com/shop/sisley-paris/sisley-paris-makeup?id=1316925',
            "category": 'sisley-paris-sisley-paris-makeup',
            "department": 'sisley-paris',
        },
        'sisley-paris-sisley-paris-skincare': {
            "url": 'https://www.bloomingdales.com/shop/sisley-paris/sisley-paris-skincare?id=1316926',
            "category": 'sisley-paris-sisley-paris-skincare',
            "department": 'sisley-paris',
        },
    },
    'sk-ii': {
        'sk-ii': {
            "url": 'https://www.bloomingdales.com/shop/sk-ii?id=1288400',
            "category": 'sk-ii',
            "department": 'sk-ii',
        },
    },
    'skillets-and-frying-pans': {
        'skillets-and-frying-pans': {
            "url": 'https://www.bloomingdales.com/shop/skillets-and-frying-pans?id=1039383',
            "category": 'skillets-and-frying-pans',
            "department": 'skillets-and-frying-pans',
        },
    },
    'skims': {
        'skims': {
            "url": 'https://www.bloomingdales.com/shop/skims?id=1273844',
            "category": 'skims',
            "department": 'skims',
        },
        'skims-mens': {
            "url": 'https://www.bloomingdales.com/shop/skims/mens?id=1273845',
            "category": 'skims-mens',
            "department": 'skims',
        },
        'skims-womens': {
            "url": 'https://www.bloomingdales.com/shop/skims/womens?id=1273846',
            "category": 'skims-womens',
            "department": 'skims',
        },
    },
    'skin-care-products': {
        'skin-care-products': {
            "url": 'https://www.bloomingdales.com/shop/skin-care-products?id=1287725',
            "category": 'skin-care-products',
            "department": 'skin-care-products',
        },
    },
    'skincare': {
        'skincare': {
            "url": 'https://www.bloomingdales.com/shop/skincare?id=1269416',
            "category": 'skincare',
            "department": 'skincare',
        },
    },
    'sleepwear-night-gowns-pajamas': {
        'sleepwear-night-gowns-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/sleepwear-night-gowns-pajamas?id=1267473',
            "category": 'sleepwear-night-gowns-pajamas',
            "department": 'sleepwear-night-gowns-pajamas',
        },
    },
    'slim-skinny-ripped-jeans': {
        'slim-skinny-ripped-jeans': {
            "url": 'https://www.bloomingdales.com/shop/slim-skinny-ripped-jeans?id=1027012',
            "category": 'slim-skinny-ripped-jeans',
            "department": 'slim-skinny-ripped-jeans',
        },
    },
    'slip-on': {
        'slip-on': {
            "url": 'https://www.bloomingdales.com/shop/slip-on?id=1027046',
            "category": 'slip-on',
            "department": 'slip-on',
        },
    },
    'solferino': {
        'solferino': {
            "url": 'https://www.bloomingdales.com/shop/solferino?id=1304269',
            "category": 'solferino',
            "department": 'solferino',
        },
    },
    'space-nk-apothecary-brushes-accessories': {
        'space-nk-apothecary-brushes-accessories': {
            "url": 'https://www.bloomingdales.com/shop/space-nk-apothecary-brushes-accessories?id=1001302',
            "category": 'space-nk-apothecary-brushes-accessories',
            "department": 'space-nk-apothecary-brushes-accessories',
        },
    },
    'space-nk-apothecary-candles': {
        'space-nk-apothecary-candles': {
            "url": 'https://www.bloomingdales.com/shop/space-nk-apothecary-candles?id=1001299',
            "category": 'space-nk-apothecary-candles',
            "department": 'space-nk-apothecary-candles',
        },
    },
    'space-nk-apothecary-new-collections': {
        'space-nk-apothecary-new-collections': {
            "url": 'https://www.bloomingdales.com/shop/space-nk-apothecary-new-collections?id=1190163',
            "category": 'space-nk-apothecary-new-collections',
            "department": 'space-nk-apothecary-new-collections',
        },
    },
    'sparrow-wren-apartment-furniture-decor': {
        'sparrow-wren-apartment-furniture-decor': {
            "url": 'https://www.bloomingdales.com/shop/sparrow-wren-apartment-furniture-decor?id=1265409',
            "category": 'sparrow-wren-apartment-furniture-decor',
            "department": 'sparrow-wren-apartment-furniture-decor',
        },
    },
    'specialty-cookware': {
        'specialty-cookware': {
            "url": 'https://www.bloomingdales.com/shop/specialty-cookware?id=1039384',
            "category": 'specialty-cookware',
            "department": 'specialty-cookware',
        },
    },
    'spf-infused-beauty-products': {
        'spf-infused-beauty-products': {
            "url": 'https://www.bloomingdales.com/shop/spf-infused-beauty-products?id=1277906',
            "category": 'spf-infused-beauty-products',
            "department": 'spf-infused-beauty-products',
        },
    },
    'splendid': {
        'splendid': {
            "url": 'https://www.bloomingdales.com/shop/splendid?id=1003805',
            "category": 'splendid',
            "department": 'splendid',
        },
        'splendid-kids-clothing-dresses': {
            "url": 'https://www.bloomingdales.com/shop/splendid/kids-clothing-dresses?id=1003820',
            "category": 'splendid-kids-clothing-dresses',
            "department": 'splendid',
        },
        'splendid-womens-clothing-bikini-loungewear': {
            "url": 'https://www.bloomingdales.com/shop/splendid/womens-clothing-bikini-loungewear?id=1003814',
            "category": 'splendid-womens-clothing-bikini-loungewear',
            "department": 'splendid',
        },
    },
    'spring-break-essentials': {
        'spring-break-essentials': {
            "url": 'https://www.bloomingdales.com/shop/spring-break-essentials?id=1265442',
            "category": 'spring-break-essentials',
            "department": 'spring-break-essentials',
        },
    },
    'spring-jackets': {
        'spring-jackets': {
            "url": 'https://www.bloomingdales.com/shop/spring-jackets?id=1225082',
            "category": 'spring-jackets',
            "department": 'spring-jackets',
        },
    },
    'spring-scents': {
        'spring-scents': {
            "url": 'https://www.bloomingdales.com/shop/spring-scents?id=1267050',
            "category": 'spring-scents',
            "department": 'spring-scents',
        },
    },
    'spring-table-essentials': {
        'spring-table-essentials': {
            "url": 'https://www.bloomingdales.com/shop/spring-table-essentials?id=1155159',
            "category": 'spring-table-essentials',
            "department": 'spring-table-essentials',
        },
    },
    'spring-trend-paris-chic': {
        'spring-trend-paris-chic': {
            "url": 'https://www.bloomingdales.com/shop/spring-trend-paris-chic?id=1151591',
            "category": 'spring-trend-paris-chic',
            "department": 'spring-trend-paris-chic',
        },
    },
    'staud': {
        'staud': {
            "url": 'https://www.bloomingdales.com/shop/staud?id=1250217',
            "category": 'staud',
            "department": 'staud',
        },
        'staud-all-clothing': {
            "url": 'https://www.bloomingdales.com/shop/staud/all-clothing?id=1322209',
            "category": 'staud-all-clothing',
            "department": 'staud',
        },
        'staud-clothing': {
            "url": 'https://www.bloomingdales.com/shop/staud/clothing?id=1250220',
            "category": 'staud-clothing',
            "department": 'staud',
        },
        'staud-dresses': {
            "url": 'https://www.bloomingdales.com/shop/staud/dresses?id=1270200',
            "category": 'staud-dresses',
            "department": 'staud',
        },
        'staud-handbags': {
            "url": 'https://www.bloomingdales.com/shop/staud/handbags?id=1250218',
            "category": 'staud-handbags',
            "department": 'staud',
        },
        'staud-pants': {
            "url": 'https://www.bloomingdales.com/shop/staud/pants?id=1270202',
            "category": 'staud-pants',
            "department": 'staud',
        },
        'staud-sale': {
            "url": 'https://www.bloomingdales.com/shop/staud/sale?id=1270205',
            "category": 'staud-sale',
            "department": 'staud',
        },
        'staud-shoes': {
            "url": 'https://www.bloomingdales.com/shop/staud/shoes?id=1250219',
            "category": 'staud-shoes',
            "department": 'staud',
        },
        'staud-skirts': {
            "url": 'https://www.bloomingdales.com/shop/staud/skirts?id=1270201',
            "category": 'staud-skirts',
            "department": 'staud',
        },
        'staud-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/staud/sweaters?id=1270203',
            "category": 'staud-sweaters',
            "department": 'staud',
        },
        'staud-swimsuits-cover-ups': {
            "url": 'https://www.bloomingdales.com/shop/staud/swimsuits-cover-ups?id=1270406',
            "category": 'staud-swimsuits-cover-ups',
            "department": 'staud',
        },
        'staud-tops': {
            "url": 'https://www.bloomingdales.com/shop/staud/tops?id=1270204',
            "category": 'staud-tops',
            "department": 'staud',
        },
    },
    'stella-mccartney': {
        'stella-mccartney': {
            "url": 'https://www.bloomingdales.com/shop/stella-mccartney?id=1116459',
            "category": 'stella-mccartney',
            "department": 'stella-mccartney',
        },
        'stella-mccartney-stella-mccartney-handbags': {
            "url": 'https://www.bloomingdales.com/shop/stella-mccartney/stella-mccartney-handbags?id=1116959',
            "category": 'stella-mccartney-stella-mccartney-handbags',
            "department": 'stella-mccartney',
        },
        'stella-mccartney-stella-mccartney-kids-clothes': {
            "url": 'https://www.bloomingdales.com/shop/stella-mccartney/stella-mccartney-kids-clothes?id=1117259',
            "category": 'stella-mccartney-stella-mccartney-kids-clothes',
            "department": 'stella-mccartney',
        },
        'stella-mccartney-stella-mccartney-womens-clothes': {
            "url": 'https://www.bloomingdales.com/shop/stella-mccartney/stella-mccartney-womens-clothes?id=1117264',
            "category": 'stella-mccartney-stella-mccartney-womens-clothes',
            "department": 'stella-mccartney',
        },
    },
    'sterling-silver-collection': {
        'sterling-silver-collection': {
            "url": 'https://www.bloomingdales.com/shop/sterling-silver-collection?id=22865',
            "category": 'sterling-silver-collection',
            "department": 'sterling-silver-collection',
        },
    },
    'steve-madden': {
        'steve-madden': {
            "url": 'https://www.bloomingdales.com/shop/steve-madden?id=1331799',
            "category": 'steve-madden',
            "department": 'steve-madden',
        },
        'steve-madden-kids': {
            "url": 'https://www.bloomingdales.com/shop/steve-madden/kids?id=1331802',
            "category": 'steve-madden-kids',
            "department": 'steve-madden',
        },
        'steve-madden-shoes': {
            "url": 'https://www.bloomingdales.com/shop/steve-madden/shoes?id=1331801',
            "category": 'steve-madden-shoes',
            "department": 'steve-madden',
        },
        'steve-madden-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/steve-madden/womens-clothing?id=1331800',
            "category": 'steve-madden-womens-clothing',
            "department": 'steve-madden',
        },
    },
    'stocking-stuffers': {
        'stocking-stuffers': {
            "url": 'https://www.bloomingdales.com/shop/stocking-stuffers?id=1291700',
            "category": 'stocking-stuffers',
            "department": 'stocking-stuffers',
        },
    },
    'stokke': {
        'stokke': {
            "url": 'https://www.bloomingdales.com/shop/stokke?id=1329913',
            "category": 'stokke',
            "department": 'stokke',
        },
    },
    'stone-island': {
        'stone-island': {
            "url": 'https://www.bloomingdales.com/shop/stone-island?id=1308096',
            "category": 'stone-island',
            "department": 'stone-island',
        },
    },
    'straight-jeans': {
        'straight-jeans': {
            "url": 'https://www.bloomingdales.com/shop/straight-jeans?id=1027013',
            "category": 'straight-jeans',
            "department": 'straight-jeans',
        },
    },
    'stuart-weitzman': {
        'stuart-weitzman': {
            "url": 'https://www.bloomingdales.com/shop/stuart-weitzman?id=1004068',
            "category": 'stuart-weitzman',
            "department": 'stuart-weitzman',
        },
        'stuart-weitzman-boots': {
            "url": 'https://www.bloomingdales.com/shop/stuart-weitzman/boots?id=1250714',
            "category": 'stuart-weitzman-boots',
            "department": 'stuart-weitzman',
        },
        'stuart-weitzman-flats': {
            "url": 'https://www.bloomingdales.com/shop/stuart-weitzman/flats?id=1250715',
            "category": 'stuart-weitzman-flats',
            "department": 'stuart-weitzman',
        },
        'stuart-weitzman-handbags': {
            "url": 'https://www.bloomingdales.com/shop/stuart-weitzman/handbags?id=1222462',
            "category": 'stuart-weitzman-handbags',
            "department": 'stuart-weitzman',
        },
        'stuart-weitzman-heels': {
            "url": 'https://www.bloomingdales.com/shop/stuart-weitzman/heels?id=1250716',
            "category": 'stuart-weitzman-heels',
            "department": 'stuart-weitzman',
        },
        'stuart-weitzman-sale': {
            "url": 'https://www.bloomingdales.com/shop/stuart-weitzman/sale?id=1304598',
            "category": 'stuart-weitzman-sale',
            "department": 'stuart-weitzman',
        },
        'stuart-weitzman-sandals': {
            "url": 'https://www.bloomingdales.com/shop/stuart-weitzman/sandals?id=1304597',
            "category": 'stuart-weitzman-sandals',
            "department": 'stuart-weitzman',
        },
    },
    'stud': {
        'stud': {
            "url": 'https://www.bloomingdales.com/shop/stud?id=20552',
            "category": 'stud',
            "department": 'stud',
        },
    },
    'style-kingdom': {
        'style-kingdom': {
            "url": 'https://www.bloomingdales.com/shop/style-kingdom?id=1074459',
            "category": 'style-kingdom',
            "department": 'style-kingdom',
        },
    },
    'subway-series': {
        'subway-series': {
            "url": 'https://www.bloomingdales.com/shop/subway-series?id=1319695',
            "category": 'subway-series',
            "department": 'subway-series',
        },
    },
    'suit-separates': {
        'suit-separates': {
            "url": 'https://www.bloomingdales.com/shop/suit-separates?id=1154765',
            "category": 'suit-separates',
            "department": 'suit-separates',
        },
    },
    'suits': {
        'suits': {
            "url": 'https://www.bloomingdales.com/shop/suits?id=1027037',
            "category": 'suits',
            "department": 'suits',
        },
    },
    'sulwhasoo': {
        'sulwhasoo': {
            "url": 'https://www.bloomingdales.com/shop/sulwhasoo?id=1323924',
            "category": 'sulwhasoo',
            "department": 'sulwhasoo',
        },
        'sulwhasoo-sulwhasoo-concentrated-ginseng': {
            "url": 'https://www.bloomingdales.com/shop/sulwhasoo/sulwhasoo-concentrated-ginseng?id=1323927',
            "category": 'sulwhasoo-sulwhasoo-concentrated-ginseng',
            "department": 'sulwhasoo',
        },
        'sulwhasoo-sulwhasoo-first-care': {
            "url": 'https://www.bloomingdales.com/shop/sulwhasoo/sulwhasoo-first-care?id=1323926',
            "category": 'sulwhasoo-sulwhasoo-first-care',
            "department": 'sulwhasoo',
        },
        'sulwhasoo-sulwhasoo-serum': {
            "url": 'https://www.bloomingdales.com/shop/sulwhasoo/sulwhasoo-serum?id=1323925',
            "category": 'sulwhasoo-sulwhasoo-serum',
            "department": 'sulwhasoo',
        },
    },
    'summer-bedding-shop': {
        'summer-bedding-shop': {
            "url": 'https://www.bloomingdales.com/shop/summer-bedding-shop?id=1265441',
            "category": 'summer-bedding-shop',
            "department": 'summer-bedding-shop',
        },
    },
    'summer-style-bucket-list': {
        'summer-style-bucket-list': {
            "url": 'https://www.bloomingdales.com/shop/summer-style-bucket-list?id=1006701',
            "category": 'summer-style-bucket-list',
            "department": 'summer-style-bucket-list',
        },
    },
    'sun-protection': {
        'sun-protection': {
            "url": 'https://www.bloomingdales.com/shop/sun-protection?id=15968',
            "category": 'sun-protection',
            "department": 'sun-protection',
        },
        'sun-protection-body': {
            "url": 'https://www.bloomingdales.com/shop/sun-protection/body?id=15971',
            "category": 'sun-protection-body',
            "department": 'sun-protection',
        },
        'sun-protection-face': {
            "url": 'https://www.bloomingdales.com/shop/sun-protection/face?id=15970',
            "category": 'sun-protection-face',
            "department": 'sun-protection',
        },
    },
    'sunglasses-flash-sale': {
        'sunglasses-flash-sale-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/sunglasses-flash-sale/shop-all?id=1072761',
            "category": 'sunglasses-flash-sale-shop-all',
            "department": 'sunglasses-flash-sale',
        },
    },
    'sunset-hues': {
        'sunset-hues': {
            "url": 'https://www.bloomingdales.com/shop/sunset-hues?id=1240275',
            "category": 'sunset-hues',
            "department": 'sunset-hues',
        },
    },
    'supergoop': {
        'supergoop': {
            "url": 'https://www.bloomingdales.com/shop/supergoop?id=1323001',
            "category": 'supergoop',
            "department": 'supergoop',
        },
    },
    'surfer-chic': {
        'surfer-chic': {
            "url": 'https://www.bloomingdales.com/shop/surfer-chic?id=1322005',
            "category": 'surfer-chic',
            "department": 'surfer-chic',
        },
    },
    'sweaters': {
        'sweaters': {
            "url": 'https://www.bloomingdales.com/shop/sweaters?id=1278812',
            "category": 'sweaters',
            "department": 'sweaters',
        },
    },
    'sweatpants-joggers': {
        'sweatpants-joggers': {
            "url": 'https://www.bloomingdales.com/shop/sweatpants-joggers?id=1027029',
            "category": 'sweatpants-joggers',
            "department": 'sweatpants-joggers',
        },
    },
    'swimsuit-bathing-suit-coverups': {
        'swimsuit-bathing-suit-coverups': {
            "url": 'https://www.bloomingdales.com/shop/swimsuit-bathing-suit-coverups?id=1154872',
            "category": 'swimsuit-bathing-suit-coverups',
            "department": 'swimsuit-bathing-suit-coverups',
        },
    },
    'swimsuit-bottoms': {
        'swimsuit-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/swimsuit-bottoms?id=1156965',
            "category": 'swimsuit-bottoms',
            "department": 'swimsuit-bottoms',
        },
    },
    'swimsuits-bathing-suits': {
        'swimsuits-bathing-suits': {
            "url": 'https://www.bloomingdales.com/shop/swimsuits-bathing-suits?id=1307606',
            "category": 'swimsuits-bathing-suits',
            "department": 'swimsuits-bathing-suits',
        },
    },
    'swipe-go-beauty': {
        'swipe-go-beauty': {
            "url": 'https://www.bloomingdales.com/shop/swipe-go-beauty?id=1253997',
            "category": 'swipe-go-beauty',
            "department": 'swipe-go-beauty',
        },
    },
    'sydney-evan': {
        'sydney-evan': {
            "url": 'https://www.bloomingdales.com/shop/sydney-evan?id=1272096',
            "category": 'sydney-evan',
            "department": 'sydney-evan',
        },
        'sydney-evan-bracelets': {
            "url": 'https://www.bloomingdales.com/shop/sydney-evan/bracelets?id=1272097',
            "category": 'sydney-evan-bracelets',
            "department": 'sydney-evan',
        },
        'sydney-evan-earrings': {
            "url": 'https://www.bloomingdales.com/shop/sydney-evan/earrings?id=1272100',
            "category": 'sydney-evan-earrings',
            "department": 'sydney-evan',
        },
        'sydney-evan-necklaces': {
            "url": 'https://www.bloomingdales.com/shop/sydney-evan/necklaces?id=1272098',
            "category": 'sydney-evan-necklaces',
            "department": 'sydney-evan',
        },
        'sydney-evan-rings': {
            "url": 'https://www.bloomingdales.com/shop/sydney-evan/rings?id=1272099',
            "category": 'sydney-evan-rings',
            "department": 'sydney-evan',
        },
    },
    'table-linens': {
        'table-linens': {
            "url": 'https://www.bloomingdales.com/shop/table-linens?id=1000246',
            "category": 'table-linens',
            "department": 'table-linens',
        },
    },
    'tables': {
        'tables': {
            "url": 'https://www.bloomingdales.com/shop/tables?id=1240359',
            "category": 'tables',
            "department": 'tables',
        },
    },
    'tag-heuer': {
        'tag-heuer': {
            "url": 'https://www.bloomingdales.com/shop/tag-heuer?id=1003851',
            "category": 'tag-heuer',
            "department": 'tag-heuer',
        },
    },
    'tankini-swimsuits': {
        'tankini-swimsuits': {
            "url": 'https://www.bloomingdales.com/shop/tankini-swimsuits?id=1156967',
            "category": 'tankini-swimsuits',
            "department": 'tankini-swimsuits',
        },
        'tankini-swimsuits-tankini-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/tankini-swimsuits/tankini-bottoms?id=1156969',
            "category": 'tankini-swimsuits-tankini-bottoms',
            "department": 'tankini-swimsuits',
        },
        'tankini-swimsuits-tankini-tops': {
            "url": 'https://www.bloomingdales.com/shop/tankini-swimsuits/tankini-tops?id=1156968',
            "category": 'tankini-swimsuits-tankini-tops',
            "department": 'tankini-swimsuits',
        },
    },
    'ted-baker': {
        'ted-baker': {
            "url": 'https://www.bloomingdales.com/shop/ted-baker?id=1002438',
            "category": 'ted-baker',
            "department": 'ted-baker',
        },
        'ted-baker-luggage-suitcase-bedding': {
            "url": 'https://www.bloomingdales.com/shop/ted-baker/luggage-suitcase-bedding?id=1045759',
            "category": 'ted-baker-luggage-suitcase-bedding',
            "department": 'ted-baker',
        },
        'ted-baker-mens': {
            "url": 'https://www.bloomingdales.com/shop/ted-baker/mens?id=1002440',
            "category": 'ted-baker-mens',
            "department": 'ted-baker',
        },
        'ted-baker-womens': {
            "url": 'https://www.bloomingdales.com/shop/ted-baker/womens?id=1002442',
            "category": 'ted-baker-womens',
            "department": 'ted-baker',
        },
    },
    'teen-clothing': {
        'teen-clothing': {
            "url": 'https://www.bloomingdales.com/shop/teen-clothing?id=1226659',
            "category": 'teen-clothing',
            "department": 'teen-clothing',
        },
    },
    'temple-st-clair': {
        'temple-st-clair': {
            "url": 'https://www.bloomingdales.com/shop/temple-st-clair?id=1308996',
            "category": 'temple-st-clair',
            "department": 'temple-st-clair',
        },
    },
    'teri-jon': {
        'teri-jon': {
            "url": 'https://www.bloomingdales.com/shop/teri-jon?id=1291706',
            "category": 'teri-jon',
            "department": 'teri-jon',
        },
    },
    'test-cat': {
        'test-cat': {
            "url": 'https://www.bloomingdales.com/shop/test-cat?id=1112772',
            "category": 'test-cat',
            "department": 'test-cat',
        },
    },
    'test-fashion-jewelry-material': {
        'test-fashion-jewelry-material': {
            "url": 'https://www.bloomingdales.com/shop/test-fashion-jewelry-material?id=1043359',
            "category": 'test-fashion-jewelry-material',
            "department": 'test-fashion-jewelry-material',
        },
    },
    'the-christmas-shop': {
        'the-christmas-shop': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop?id=1283801',
            "category": 'the-christmas-shop',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-alice-olivia': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/alice-olivia?id=1321403',
            "category": 'the-christmas-shop-alice-olivia',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-artificial-christmas-trees': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/artificial-christmas-trees?id=1283804',
            "category": 'the-christmas-shop-artificial-christmas-trees',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-caviar-kaspia': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/caviar-kaspia?id=1321404',
            "category": 'the-christmas-shop-caviar-kaspia',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-christmas-candles': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/christmas-candles?id=1283805',
            "category": 'the-christmas-shop-christmas-candles',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-christmas-classics': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/christmas-classics?id=1321406',
            "category": 'the-christmas-shop-christmas-classics',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-christmas-cookware': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/christmas-cookware?id=1283807',
            "category": 'the-christmas-shop-christmas-cookware',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-christmas-decor': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/christmas-decor?id=1283803',
            "category": 'the-christmas-shop-christmas-decor',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-christmas-dishes': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/christmas-dishes?id=1283806',
            "category": 'the-christmas-shop-christmas-dishes',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-christmas-food-gifts': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/christmas-food-gifts?id=1283808',
            "category": 'the-christmas-shop-christmas-food-gifts',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-christmas-ornaments': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/christmas-ornaments?id=1283802',
            "category": 'the-christmas-shop-christmas-ornaments',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-gift-wrap': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/gift-wrap?id=1319415',
            "category": 'the-christmas-shop-gift-wrap',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-new-york-city-ballet': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/new-york-city-ballet?id=1321407',
            "category": 'the-christmas-shop-new-york-city-ballet',
            "department": 'the-christmas-shop',
        },
        'the-christmas-shop-shimmering-pine': {
            "url": 'https://www.bloomingdales.com/shop/the-christmas-shop/shimmering-pine?id=1321405',
            "category": 'the-christmas-shop-shimmering-pine',
            "department": 'the-christmas-shop',
        },
    },
    'the-couple-who-already-lives-together': {
        'the-couple-who-already-lives-together': {
            "url": 'https://www.bloomingdales.com/shop/the-couple-who-already-lives-together?id=1216360',
            "category": 'the-couple-who-already-lives-together',
            "department": 'the-couple-who-already-lives-together',
        },
    },
    'the-couple-who-is-a-little-extra': {
        'the-couple-who-is-a-little-extra': {
            "url": 'https://www.bloomingdales.com/shop/the-couple-who-is-a-little-extra?id=1216363',
            "category": 'the-couple-who-is-a-little-extra',
            "department": 'the-couple-who-is-a-little-extra',
        },
    },
    'the-couple-who-is-always-entertaining': {
        'the-couple-who-is-always-entertaining': {
            "url": 'https://www.bloomingdales.com/shop/the-couple-who-is-always-entertaining?id=1216361',
            "category": 'the-couple-who-is-always-entertaining',
            "department": 'the-couple-who-is-always-entertaining',
        },
    },
    'the-couple-who-likes-to-keep-it-minimal': {
        'the-couple-who-likes-to-keep-it-minimal': {
            "url": 'https://www.bloomingdales.com/shop/the-couple-who-likes-to-keep-it-minimal?id=1216364',
            "category": 'the-couple-who-likes-to-keep-it-minimal',
            "department": 'the-couple-who-likes-to-keep-it-minimal',
        },
    },
    'the-couple-who-loves-to-cook': {
        'the-couple-who-loves-to-cook': {
            "url": 'https://www.bloomingdales.com/shop/the-couple-who-loves-to-cook?id=1216362',
            "category": 'the-couple-who-loves-to-cook',
            "department": 'the-couple-who-loves-to-cook',
        },
    },
    'the-couple-with-a-retro-vibe': {
        'the-couple-with-a-retro-vibe': {
            "url": 'https://www.bloomingdales.com/shop/the-couple-with-a-retro-vibe?id=1216359',
            "category": 'the-couple-with-a-retro-vibe',
            "department": 'the-couple-with-a-retro-vibe',
        },
    },
    'the-coveteur-tastemakers-picks': {
        'the-coveteur-tastemakers-picks': {
            "url": 'https://www.bloomingdales.com/shop/the-coveteur-tastemakers-picks?id=1004596',
            "category": 'the-coveteur-tastemakers-picks',
            "department": 'the-coveteur-tastemakers-picks',
        },
        'the-coveteur-tastemakers-picks-andis-picks': {
            "url": 'https://www.bloomingdales.com/shop/the-coveteur-tastemakers-picks/andis-picks?id=1004600',
            "category": 'the-coveteur-tastemakers-picks-andis-picks',
            "department": 'the-coveteur-tastemakers-picks',
        },
        'the-coveteur-tastemakers-picks-julias-picks': {
            "url": 'https://www.bloomingdales.com/shop/the-coveteur-tastemakers-picks/julias-picks?id=1004597',
            "category": 'the-coveteur-tastemakers-picks-julias-picks',
            "department": 'the-coveteur-tastemakers-picks',
        },
        'the-coveteur-tastemakers-picks-poppys-picks': {
            "url": 'https://www.bloomingdales.com/shop/the-coveteur-tastemakers-picks/poppys-picks?id=1004599',
            "category": 'the-coveteur-tastemakers-picks-poppys-picks',
            "department": 'the-coveteur-tastemakers-picks',
        },
        'the-coveteur-tastemakers-picks-saras-picks': {
            "url": 'https://www.bloomingdales.com/shop/the-coveteur-tastemakers-picks/saras-picks?id=1004601',
            "category": 'the-coveteur-tastemakers-picks-saras-picks',
            "department": 'the-coveteur-tastemakers-picks',
        },
    },
    'the-designer-event': {
        'the-designer-event': {
            "url": 'https://www.bloomingdales.com/shop/the-designer-event?id=1323399',
            "category": 'the-designer-event',
            "department": 'the-designer-event',
        },
        'the-designer-event-designer-private-sale': {
            "url": 'https://www.bloomingdales.com/shop/the-designer-event/designer-private-sale?id=1323404',
            "category": 'the-designer-event-designer-private-sale',
            "department": 'the-designer-event',
        },
    },
    'the-essentials': {
        'the-essentials': {
            "url": 'https://www.bloomingdales.com/shop/the-essentials?id=1003283',
            "category": 'the-essentials',
            "department": 'the-essentials',
        },
    },
    'the-hanukkah-shop': {
        'the-hanukkah-shop': {
            "url": 'https://www.bloomingdales.com/shop/the-hanukkah-shop?id=1283809',
            "category": 'the-hanukkah-shop',
            "department": 'the-hanukkah-shop',
        },
        'the-hanukkah-shop-hanukkah-candles': {
            "url": 'https://www.bloomingdales.com/shop/the-hanukkah-shop/hanukkah-candles?id=1283812',
            "category": 'the-hanukkah-shop-hanukkah-candles',
            "department": 'the-hanukkah-shop',
        },
        'the-hanukkah-shop-hanukkah-candy': {
            "url": 'https://www.bloomingdales.com/shop/the-hanukkah-shop/hanukkah-candy?id=1283815',
            "category": 'the-hanukkah-shop-hanukkah-candy',
            "department": 'the-hanukkah-shop',
        },
        'the-hanukkah-shop-hanukkah-cookware': {
            "url": 'https://www.bloomingdales.com/shop/the-hanukkah-shop/hanukkah-cookware?id=1283814',
            "category": 'the-hanukkah-shop-hanukkah-cookware',
            "department": 'the-hanukkah-shop',
        },
        'the-hanukkah-shop-hanukkah-dishes': {
            "url": 'https://www.bloomingdales.com/shop/the-hanukkah-shop/hanukkah-dishes?id=1283813',
            "category": 'the-hanukkah-shop-hanukkah-dishes',
            "department": 'the-hanukkah-shop',
        },
        'the-hanukkah-shop-menorahs': {
            "url": 'https://www.bloomingdales.com/shop/the-hanukkah-shop/menorahs?id=1283810',
            "category": 'the-hanukkah-shop-menorahs',
            "department": 'the-hanukkah-shop',
        },
    },
    'the-mens-store-at-bloomingdales': {
        'the-mens-store-at-bloomingdales': {
            "url": 'https://www.bloomingdales.com/shop/the-mens-store-at-bloomingdales?id=1005194',
            "category": 'the-mens-store-at-bloomingdales',
            "department": 'the-mens-store-at-bloomingdales',
        },
        'the-mens-store-at-bloomingdales-cashmere': {
            "url": 'https://www.bloomingdales.com/shop/the-mens-store-at-bloomingdales/cashmere?id=1250712',
            "category": 'the-mens-store-at-bloomingdales-cashmere',
            "department": 'the-mens-store-at-bloomingdales',
        },
        'the-mens-store-at-bloomingdales-mens-store-bloomingdales-accessories': {
            "url": 'https://www.bloomingdales.com/shop/the-mens-store-at-bloomingdales/mens-store-bloomingdales-accessories?id=1012562',
            "category": 'the-mens-store-at-bloomingdales-mens-store-bloomingdales-accessories',
            "department": 'the-mens-store-at-bloomingdales',
        },
        'the-mens-store-at-bloomingdales-mens-store-bloomingdales-clothing': {
            "url": 'https://www.bloomingdales.com/shop/the-mens-store-at-bloomingdales/mens-store-bloomingdales-clothing?id=1012561',
            "category": 'the-mens-store-at-bloomingdales-mens-store-bloomingdales-clothing',
            "department": 'the-mens-store-at-bloomingdales',
        },
        'the-mens-store-at-bloomingdales-sale': {
            "url": 'https://www.bloomingdales.com/shop/the-mens-store-at-bloomingdales/sale?id=1250711',
            "category": 'the-mens-store-at-bloomingdales-sale',
            "department": 'the-mens-store-at-bloomingdales',
        },
        'the-mens-store-at-bloomingdales-shoes': {
            "url": 'https://www.bloomingdales.com/shop/the-mens-store-at-bloomingdales/shoes?id=1250713',
            "category": 'the-mens-store-at-bloomingdales-shoes',
            "department": 'the-mens-store-at-bloomingdales',
        },
    },
    'the-north-face': {
        'the-north-face': {
            "url": 'https://www.bloomingdales.com/shop/the-north-face?id=1250953',
            "category": 'the-north-face',
            "department": 'the-north-face',
        },
        'the-north-face-kids': {
            "url": 'https://www.bloomingdales.com/shop/the-north-face/kids?id=1281195',
            "category": 'the-north-face-kids',
            "department": 'the-north-face',
        },
        'the-north-face-mens': {
            "url": 'https://www.bloomingdales.com/shop/the-north-face/mens?id=1250959',
            "category": 'the-north-face-mens',
            "department": 'the-north-face',
        },
        'the-north-face-womens': {
            "url": 'https://www.bloomingdales.com/shop/the-north-face/womens?id=1250960',
            "category": 'the-north-face-womens',
            "department": 'the-north-face',
        },
    },
    'the-outlet-store': {
        'the-outlet-store': {
            "url": 'https://www.bloomingdales.com/shop/the-outlet-store?id=1005292',
            "category": 'the-outlet-store',
            "department": 'the-outlet-store',
        },
    },
    'the-thanksgiving-shop': {
        'the-thanksgiving-shop': {
            "url": 'https://www.bloomingdales.com/shop/the-thanksgiving-shop?id=1283795',
            "category": 'the-thanksgiving-shop',
            "department": 'the-thanksgiving-shop',
        },
        'the-thanksgiving-shop-friendsgiving': {
            "url": 'https://www.bloomingdales.com/shop/the-thanksgiving-shop/friendsgiving?id=1247595',
            "category": 'the-thanksgiving-shop-friendsgiving',
            "department": 'the-thanksgiving-shop',
        },
        'the-thanksgiving-shop-thanksgiving-candles': {
            "url": 'https://www.bloomingdales.com/shop/the-thanksgiving-shop/thanksgiving-candles?id=1283799',
            "category": 'the-thanksgiving-shop-thanksgiving-candles',
            "department": 'the-thanksgiving-shop',
        },
        'the-thanksgiving-shop-thanksgiving-cookware': {
            "url": 'https://www.bloomingdales.com/shop/the-thanksgiving-shop/thanksgiving-cookware?id=1283796',
            "category": 'the-thanksgiving-shop-thanksgiving-cookware',
            "department": 'the-thanksgiving-shop',
        },
        'the-thanksgiving-shop-thanksgiving-decor': {
            "url": 'https://www.bloomingdales.com/shop/the-thanksgiving-shop/thanksgiving-decor?id=1283798',
            "category": 'the-thanksgiving-shop-thanksgiving-decor',
            "department": 'the-thanksgiving-shop',
        },
        'the-thanksgiving-shop-thanksgiving-table-settings': {
            "url": 'https://www.bloomingdales.com/shop/the-thanksgiving-shop/thanksgiving-table-settings?id=1283797',
            "category": 'the-thanksgiving-shop-thanksgiving-table-settings',
            "department": 'the-thanksgiving-shop',
        },
    },
    'the-winter-shop': {
        'the-winter-shop': {
            "url": 'https://www.bloomingdales.com/shop/the-winter-shop?id=1000997',
            "category": 'the-winter-shop',
            "department": 'the-winter-shop',
        },
    },
    'theory-designer-clothing': {
        'theory-designer-clothing': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing?id=1002845',
            "category": 'theory-designer-clothing',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-blazers': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/blazers?id=1277197',
            "category": 'theory-designer-clothing-blazers',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-dresses': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/dresses?id=1277196',
            "category": 'theory-designer-clothing-dresses',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/mens-clothing?id=1002847',
            "category": 'theory-designer-clothing-mens-clothing',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-new-to-sale': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/new-to-sale?id=1250963',
            "category": 'theory-designer-clothing-new-to-sale',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-our-best-basics': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/our-best-basics?id=1091059',
            "category": 'theory-designer-clothing-our-best-basics',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-pants': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/pants?id=1277198',
            "category": 'theory-designer-clothing-pants',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-sale': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/sale?id=1277201',
            "category": 'theory-designer-clothing-sale',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/sweaters?id=1277199',
            "category": 'theory-designer-clothing-sweaters',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-theory-mens-suits-tuxedos': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/theory-mens-suits-tuxedos?id=1005313',
            "category": 'theory-designer-clothing-theory-mens-suits-tuxedos',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-tops': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/tops?id=1277200',
            "category": 'theory-designer-clothing-tops',
            "department": 'theory-designer-clothing',
        },
        'theory-designer-clothing-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/theory-designer-clothing/womens-clothing?id=1002846',
            "category": 'theory-designer-clothing-womens-clothing',
            "department": 'theory-designer-clothing',
        },
    },
    'theory-mens-suits-tuxedos': {
        'theory-mens-suits-tuxedos': {
            "url": 'https://www.bloomingdales.com/shop/theory-mens-suits-tuxedos?id=1278816',
            "category": 'theory-mens-suits-tuxedos',
            "department": 'theory-mens-suits-tuxedos',
        },
    },
    'therabody': {
        'therabody': {
            "url": 'https://www.bloomingdales.com/shop/therabody?id=1298395',
            "category": 'therabody',
            "department": 'therabody',
        },
    },
    'tiktok-made-me-buy-it': {
        'tiktok-made-me-buy-it': {
            "url": 'https://www.bloomingdales.com/shop/tiktok-made-me-buy-it?id=1216671',
            "category": 'tiktok-made-me-buy-it',
            "department": 'tiktok-made-me-buy-it',
        },
    },
    'tom-ford': {
        'tom-ford': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford?id=1187559',
            "category": 'tom-ford',
            "department": 'tom-ford',
        },
        'tom-ford-beauty-perfume-cologne': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/beauty-perfume-cologne?id=1006853',
            "category": 'tom-ford-beauty-perfume-cologne',
            "department": 'tom-ford',
        },
        'tom-ford-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/fragrance?id=1187563',
            "category": 'tom-ford-fragrance',
            "department": 'tom-ford',
        },
        'tom-ford-makeup': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/makeup?id=1187560',
            "category": 'tom-ford-makeup',
            "department": 'tom-ford',
        },
        'tom-ford-men': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/men?id=1187565',
            "category": 'tom-ford-men',
            "department": 'tom-ford',
        },
        'tom-ford-mens-cologne-skincare-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/mens-cologne-skincare-sunglasses?id=1005403',
            "category": 'tom-ford-mens-cologne-skincare-sunglasses',
            "department": 'tom-ford',
        },
        'tom-ford-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/shop-all?id=1187659',
            "category": 'tom-ford-shop-all',
            "department": 'tom-ford',
        },
        'tom-ford-sunglasses-women': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/sunglasses-women?id=1003862',
            "category": 'tom-ford-sunglasses-women',
            "department": 'tom-ford',
        },
        'tom-ford-womens-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/tom-ford/womens-sunglasses?id=1187566',
            "category": 'tom-ford-womens-sunglasses',
            "department": 'tom-ford',
        },
    },
    'top-products': {
        'top-products': {
            "url": 'https://www.bloomingdales.com/shop/top-products?id=1003254',
            "category": 'top-products',
            "department": 'top-products',
        },
    },
    'tops': {
        'tops': {
            "url": 'https://www.bloomingdales.com/shop/tops?id=1278813',
            "category": 'tops',
            "department": 'tops',
        },
    },
    'tops-tees-under-100': {
        'tops-tees-under-100': {
            "url": 'https://www.bloomingdales.com/shop/tops-tees-under-100?id=1005546',
            "category": 'tops-tees-under-100',
            "department": 'tops-tees-under-100',
        },
    },
    'tory-burch': {
        'tory-burch': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch?id=1002727',
            "category": 'tory-burch',
            "department": 'tory-burch',
        },
        'tory-burch-all-sale': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/all-sale?id=1262895',
            "category": 'tory-burch-all-sale',
            "department": 'tory-burch',
        },
        'tory-burch-beauty-perfume': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/beauty-perfume?id=1002732',
            "category": 'tory-burch-beauty-perfume',
            "department": 'tory-burch',
        },
        'tory-burch-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/best-sellers?id=1161162',
            "category": 'tory-burch-best-sellers',
            "department": 'tory-burch',
        },
        'tory-burch-crossbody-bags': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/crossbody-bags?id=1264255',
            "category": 'tory-burch-crossbody-bags',
            "department": 'tory-burch',
        },
        'tory-burch-gifts': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/gifts?id=1139159',
            "category": 'tory-burch-gifts',
            "department": 'tory-burch',
        },
        'tory-burch-handbags-wallets': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/handbags-wallets?id=1002730',
            "category": 'tory-burch-handbags-wallets',
            "department": 'tory-burch',
        },
        'tory-burch-jewelry-sunglasses-accessories': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/jewelry-sunglasses-accessories?id=1002731',
            "category": 'tory-burch-jewelry-sunglasses-accessories',
            "department": 'tory-burch',
        },
        'tory-burch-sale-handbags': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/sale-handbags?id=1264116',
            "category": 'tory-burch-sale-handbags',
            "department": 'tory-burch',
        },
        'tory-burch-sale-shoes': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/sale-shoes?id=1264117',
            "category": 'tory-burch-sale-shoes',
            "department": 'tory-burch',
        },
        'tory-burch-sandals': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/sandals?id=1262396',
            "category": 'tory-burch-sandals',
            "department": 'tory-burch',
        },
        'tory-burch-shoulder-bags': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/shoulder-bags?id=1264262',
            "category": 'tory-burch-shoulder-bags',
            "department": 'tory-burch',
        },
        'tory-burch-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/sunglasses?id=1264115',
            "category": 'tory-burch-sunglasses',
            "department": 'tory-burch',
        },
        'tory-burch-t-monogram': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/t-monogram?id=1264254',
            "category": 'tory-burch-t-monogram',
            "department": 'tory-burch',
        },
        'tory-burch-the-metallic-shop': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/the-metallic-shop?id=1002728',
            "category": 'tory-burch-the-metallic-shop',
            "department": 'tory-burch',
        },
        'tory-burch-tory-burch-wallets': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/tory-burch-wallets?id=1264114',
            "category": 'tory-burch-tory-burch-wallets',
            "department": 'tory-burch',
        },
        'tory-burch-tote-bags': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/tote-bags?id=1264259',
            "category": 'tory-burch-tote-bags',
            "department": 'tory-burch',
        },
        'tory-burch-womens-shoes-sandals': {
            "url": 'https://www.bloomingdales.com/shop/tory-burch/womens-shoes-sandals?id=1002729',
            "category": 'tory-burch-womens-shoes-sandals',
            "department": 'tory-burch',
        },
    },
    'toteme': {
        'toteme': {
            "url": 'https://www.bloomingdales.com/shop/toteme?id=1284802',
            "category": 'toteme',
            "department": 'toteme',
        },
        'toteme-handbags': {
            "url": 'https://www.bloomingdales.com/shop/toteme/handbags?id=1295019',
            "category": 'toteme-handbags',
            "department": 'toteme',
        },
        'toteme-shoes': {
            "url": 'https://www.bloomingdales.com/shop/toteme/shoes?id=1295018',
            "category": 'toteme-shoes',
            "department": 'toteme',
        },
        'toteme-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/toteme/womens-clothing?id=1301699',
            "category": 'toteme-womens-clothing',
            "department": 'toteme',
        },
    },
    'toys-accessories': {
        'toys-accessories': {
            "url": 'https://www.bloomingdales.com/shop/toys-accessories?id=1000326',
            "category": 'toys-accessories',
            "department": 'toys-accessories',
        },
    },
    'travel-sizes-minis': {
        'travel-sizes-minis': {
            "url": 'https://www.bloomingdales.com/shop/travel-sizes-minis?id=1018159',
            "category": 'travel-sizes-minis',
            "department": 'travel-sizes-minis',
        },
    },
    'trending-collections': {
        'trending-collections': {
            "url": 'https://www.bloomingdales.com/shop/trending-collections?id=1322331',
            "category": 'trending-collections',
            "department": 'trending-collections',
        },
        'trending-collections-handbags': {
            "url": 'https://www.bloomingdales.com/shop/trending-collections/handbags?id=1322334',
            "category": 'trending-collections-handbags',
            "department": 'trending-collections',
        },
        'trending-collections-shoes': {
            "url": 'https://www.bloomingdales.com/shop/trending-collections/shoes?id=1322333',
            "category": 'trending-collections-shoes',
            "department": 'trending-collections',
        },
        'trending-collections-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/trending-collections/womens-clothing?id=1322332',
            "category": 'trending-collections-womens-clothing',
            "department": 'trending-collections',
        },
    },
    'trending-now-contouring': {
        'trending-now-contouring': {
            "url": 'https://www.bloomingdales.com/shop/trending-now-contouring?id=1005227',
            "category": 'trending-now-contouring',
            "department": 'trending-now-contouring',
        },
    },
    'trending-now-cuffed-barrel-leg-jeans': {
        'trending-now-cuffed-barrel-leg-jeans': {
            "url": 'https://www.bloomingdales.com/shop/trending-now-cuffed-barrel-leg-jeans?id=1225459',
            "category": 'trending-now-cuffed-barrel-leg-jeans',
            "department": 'trending-now-cuffed-barrel-leg-jeans',
        },
    },
    'trending-now-novelty-denim': {
        'trending-now-novelty-denim': {
            "url": 'https://www.bloomingdales.com/shop/trending-now-novelty-denim?id=1132659',
            "category": 'trending-now-novelty-denim',
            "department": 'trending-now-novelty-denim',
        },
    },
    'tumi': {
        'tumi': {
            "url": 'https://www.bloomingdales.com/shop/tumi?id=1178463',
            "category": 'tumi',
            "department": 'tumi',
        },
    },
    'tuxedos': {
        'tuxedos': {
            "url": 'https://www.bloomingdales.com/shop/tuxedos?id=1027038',
            "category": 'tuxedos',
            "department": 'tuxedos',
        },
    },
    'ugg-shoes-australia': {
        'ugg-shoes-australia': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia?id=1003915',
            "category": 'ugg-shoes-australia',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-big-kid-35-7': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/big-kid-35-7?id=1251514',
            "category": 'ugg-shoes-australia-big-kid-35-7',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-home-decor-pillows': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/home-decor-pillows?id=1005205',
            "category": 'ugg-shoes-australia-home-decor-pillows',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-kids-shoes-toddler-boots': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/kids-shoes-toddler-boots?id=1003918',
            "category": 'ugg-shoes-australia-kids-shoes-toddler-boots',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-little-kid-105-3': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/little-kid-105-3?id=1251512',
            "category": 'ugg-shoes-australia-little-kid-105-3',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-mens-shoes-boots': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/mens-shoes-boots?id=1003917',
            "category": 'ugg-shoes-australia-mens-shoes-boots',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-toddler-45-10': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/toddler-45-10?id=1251513',
            "category": 'ugg-shoes-australia-toddler-45-10',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-ugg-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/ugg-best-sellers?id=1292097',
            "category": 'ugg-shoes-australia-ugg-best-sellers',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-ugg-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/ugg-new-arrivals?id=1330495',
            "category": 'ugg-shoes-australia-ugg-new-arrivals',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-womens-clothing-loungewear': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/womens-clothing-loungewear?id=1003919',
            "category": 'ugg-shoes-australia-womens-clothing-loungewear',
            "department": 'ugg-shoes-australia',
        },
        'ugg-shoes-australia-womens-shoes-boots': {
            "url": 'https://www.bloomingdales.com/shop/ugg-shoes-australia/womens-shoes-boots?id=1003916',
            "category": 'ugg-shoes-australia-womens-shoes-boots',
            "department": 'ugg-shoes-australia',
        },
    },
    'uncommon-goods': {
        'uncommon-goods': {
            "url": 'https://www.bloomingdales.com/shop/uncommon-goods?id=1296502',
            "category": 'uncommon-goods',
            "department": 'uncommon-goods',
        },
    },
    'under-100': {
        'under-100': {
            "url": 'https://www.bloomingdales.com/shop/under-100?id=1005991',
            "category": 'under-100',
            "department": 'under-100',
        },
    },
    'under-50': {
        'under-50': {
            "url": 'https://www.bloomingdales.com/shop/under-50?id=1005990',
            "category": 'under-50',
            "department": 'under-50',
        },
    },
    'untamed-garden': {
        'untamed-garden': {
            "url": 'https://www.bloomingdales.com/shop/untamed-garden?id=1303797',
            "category": 'untamed-garden',
            "department": 'untamed-garden',
        },
    },
    'uppababy': {
        'uppababy': {
            "url": 'https://www.bloomingdales.com/shop/uppababy?id=1247797',
            "category": 'uppababy',
            "department": 'uppababy',
        },
    },
    'urban-explorer': {
        'urban-explorer': {
            "url": 'https://www.bloomingdales.com/shop/urban-explorer?id=1061561',
            "category": 'urban-explorer',
            "department": 'urban-explorer',
        },
    },
    'utilitarian-styles': {
        'utilitarian-styles': {
            "url": 'https://www.bloomingdales.com/shop/utilitarian-styles?id=1238675',
            "category": 'utilitarian-styles',
            "department": 'utilitarian-styles',
        },
    },
    'vacation-beauty': {
        'vacation-beauty': {
            "url": 'https://www.bloomingdales.com/shop/vacation-beauty?id=1307615',
            "category": 'vacation-beauty',
            "department": 'vacation-beauty',
        },
    },
    'vacation-shop': {
        'vacation-shop': {
            "url": 'https://www.bloomingdales.com/shop/vacation-shop?id=1190263',
            "category": 'vacation-shop',
            "department": 'vacation-shop',
        },
    },
    'valentino-garavani': {
        'valentino-garavani': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani?id=1178661',
            "category": 'valentino-garavani',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-ambery': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/ambery?id=1330999',
            "category": 'valentino-garavani-ambery',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-anatomy-of-dreams': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/anatomy-of-dreams?id=1327196',
            "category": 'valentino-garavani-anatomy-of-dreams',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-floral': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/floral?id=1330996',
            "category": 'valentino-garavani-floral',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/fragrance?id=1326895',
            "category": 'valentino-garavani-fragrance',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-fresh': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/fresh?id=1330997',
            "category": 'valentino-garavani-fresh',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-handbags': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/handbags?id=1289895',
            "category": 'valentino-garavani-handbags',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-men': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/men?id=1179203',
            "category": 'valentino-garavani-men',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-mens-leather-goods-accessories': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/mens-leather-goods-accessories?id=1179198',
            "category": 'valentino-garavani-mens-leather-goods-accessories',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/mens-shoes?id=1179196',
            "category": 'valentino-garavani-mens-shoes',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-sale': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/sale?id=1319213',
            "category": 'valentino-garavani-sale',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-sunglasses': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/sunglasses?id=1320028',
            "category": 'valentino-garavani-sunglasses',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-women': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/women?id=1179202',
            "category": 'valentino-garavani-women',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-womens-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/womens-jewelry-accessories?id=1304725',
            "category": 'valentino-garavani-womens-jewelry-accessories',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/womens-shoes?id=1178662',
            "category": 'valentino-garavani-womens-shoes',
            "department": 'valentino-garavani',
        },
        'valentino-garavani-woody': {
            "url": 'https://www.bloomingdales.com/shop/valentino-garavani/woody?id=1330998',
            "category": 'valentino-garavani-woody',
            "department": 'valentino-garavani',
        },
    },
    'van-cleef-arpels-beauty': {
        'van-cleef-arpels-beauty': {
            "url": 'https://www.bloomingdales.com/shop/van-cleef-arpels-beauty?id=1336600',
            "category": 'van-cleef-arpels-beauty',
            "department": 'van-cleef-arpels-beauty',
        },
    },
    'veja': {
        'veja': {
            "url": 'https://www.bloomingdales.com/shop/veja?id=1253895',
            "category": 'veja',
            "department": 'veja',
        },
        'veja-kids': {
            "url": 'https://www.bloomingdales.com/shop/veja/kids?id=1254496',
            "category": 'veja-kids',
            "department": 'veja',
        },
        'veja-mens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/veja/mens-shoes?id=1254495',
            "category": 'veja-mens-shoes',
            "department": 'veja',
        },
        'veja-veja-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/veja/veja-womens-shoes?id=1253896',
            "category": 'veja-veja-womens-shoes',
            "department": 'veja',
        },
    },
    'veronica-beard': {
        'veronica-beard': {
            "url": 'https://www.bloomingdales.com/shop/veronica-beard?id=1195063',
            "category": 'veronica-beard',
            "department": 'veronica-beard',
        },
        'veronica-beard-handbags': {
            "url": 'https://www.bloomingdales.com/shop/veronica-beard/handbags?id=1243104',
            "category": 'veronica-beard-handbags',
            "department": 'veronica-beard',
        },
        'veronica-beard-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/veronica-beard/womens-clothing?id=1195064',
            "category": 'veronica-beard-womens-clothing',
            "department": 'veronica-beard',
        },
        'veronica-beard-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/veronica-beard/womens-shoes?id=1195065',
            "category": 'veronica-beard-womens-shoes',
            "department": 'veronica-beard',
        },
    },
    'versace': {
        'versace': {
            "url": 'https://www.bloomingdales.com/shop/versace?id=1159865',
            "category": 'versace',
            "department": 'versace',
        },
        'versace-clothing': {
            "url": 'https://www.bloomingdales.com/shop/versace/clothing?id=1204259',
            "category": 'versace-clothing',
            "department": 'versace',
        },
        'versace-clothing-accessories': {
            "url": 'https://www.bloomingdales.com/shop/versace/clothing-accessories?id=1159863',
            "category": 'versace-clothing-accessories',
            "department": 'versace',
        },
        'versace-cologne': {
            "url": 'https://www.bloomingdales.com/shop/versace/cologne?id=1160162',
            "category": 'versace-cologne',
            "department": 'versace',
        },
        'versace-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/versace/fragrance?id=1160161',
            "category": 'versace-fragrance',
            "department": 'versace',
        },
        'versace-handbags': {
            "url": 'https://www.bloomingdales.com/shop/versace/handbags?id=1159759',
            "category": 'versace-handbags',
            "department": 'versace',
        },
        'versace-home': {
            "url": 'https://www.bloomingdales.com/shop/versace/home?id=1159862',
            "category": 'versace-home',
            "department": 'versace',
        },
        'versace-jewelry-accessories': {
            "url": 'https://www.bloomingdales.com/shop/versace/jewelry-accessories?id=1159861',
            "category": 'versace-jewelry-accessories',
            "department": 'versace',
        },
        'versace-kids': {
            "url": 'https://www.bloomingdales.com/shop/versace/kids?id=1189159',
            "category": 'versace-kids',
            "department": 'versace',
        },
        'versace-la-medusa-collection': {
            "url": 'https://www.bloomingdales.com/shop/versace/la-medusa-collection?id=1167959',
            "category": 'versace-la-medusa-collection',
            "department": 'versace',
        },
        'versace-men': {
            "url": 'https://www.bloomingdales.com/shop/versace/men?id=1160160',
            "category": 'versace-men',
            "department": 'versace',
        },
        'versace-mens': {
            "url": 'https://www.bloomingdales.com/shop/versace/mens?id=1182462',
            "category": 'versace-mens',
            "department": 'versace',
        },
        'versace-sale': {
            "url": 'https://www.bloomingdales.com/shop/versace/sale?id=1319599',
            "category": 'versace-sale',
            "department": 'versace',
        },
        'versace-shoes': {
            "url": 'https://www.bloomingdales.com/shop/versace/shoes?id=1160164',
            "category": 'versace-shoes',
            "department": 'versace',
        },
        'versace-shop-all-women': {
            "url": 'https://www.bloomingdales.com/shop/versace/shop-all-women?id=1160059',
            "category": 'versace-shop-all-women',
            "department": 'versace',
        },
        'versace-swim': {
            "url": 'https://www.bloomingdales.com/shop/versace/swim?id=1159860',
            "category": 'versace-swim',
            "department": 'versace',
        },
        'versace-versace-jeans-couture': {
            "url": 'https://www.bloomingdales.com/shop/versace/versace-jeans-couture?id=1159864',
            "category": 'versace-versace-jeans-couture',
            "department": 'versace',
        },
        'versace-watches': {
            "url": 'https://www.bloomingdales.com/shop/versace/watches?id=1160163',
            "category": 'versace-watches',
            "department": 'versace',
        },
        'versace-women': {
            "url": 'https://www.bloomingdales.com/shop/versace/women?id=1182461',
            "category": 'versace-women',
            "department": 'versace',
        },
    },
    'victoria-beckham-beauty': {
        'victoria-beckham-beauty': {
            "url": 'https://www.bloomingdales.com/shop/victoria-beckham-beauty?id=1287996',
            "category": 'victoria-beckham-beauty',
            "department": 'victoria-beckham-beauty',
        },
        'victoria-beckham-beauty-victoria-beckham-beauty-accessories': {
            "url": 'https://www.bloomingdales.com/shop/victoria-beckham-beauty/victoria-beckham-beauty-accessories?id=1288003',
            "category": 'victoria-beckham-beauty-victoria-beckham-beauty-accessories',
            "department": 'victoria-beckham-beauty',
        },
        'victoria-beckham-beauty-victoria-beckham-beauty-eyes': {
            "url": 'https://www.bloomingdales.com/shop/victoria-beckham-beauty/victoria-beckham-beauty-eyes?id=1287998',
            "category": 'victoria-beckham-beauty-victoria-beckham-beauty-eyes',
            "department": 'victoria-beckham-beauty',
        },
        'victoria-beckham-beauty-victoria-beckham-beauty-face': {
            "url": 'https://www.bloomingdales.com/shop/victoria-beckham-beauty/victoria-beckham-beauty-face?id=1288000',
            "category": 'victoria-beckham-beauty-victoria-beckham-beauty-face',
            "department": 'victoria-beckham-beauty',
        },
        'victoria-beckham-beauty-victoria-beckham-beauty-fragrance': {
            "url": 'https://www.bloomingdales.com/shop/victoria-beckham-beauty/victoria-beckham-beauty-fragrance?id=1288001',
            "category": 'victoria-beckham-beauty-victoria-beckham-beauty-fragrance',
            "department": 'victoria-beckham-beauty',
        },
        'victoria-beckham-beauty-victoria-beckham-beauty-lips': {
            "url": 'https://www.bloomingdales.com/shop/victoria-beckham-beauty/victoria-beckham-beauty-lips?id=1287999',
            "category": 'victoria-beckham-beauty-victoria-beckham-beauty-lips',
            "department": 'victoria-beckham-beauty',
        },
    },
    'vietri': {
        'vietri': {
            "url": 'https://www.bloomingdales.com/shop/vietri?id=1323215',
            "category": 'vietri',
            "department": 'vietri',
        },
    },
    'view-all': {
        'view-all': {
            "url": 'https://www.bloomingdales.com/shop/view-all?id=20566',
            "category": 'view-all',
            "department": 'view-all',
        },
    },
    'villeroy-boch': {
        'villeroy-boch': {
            "url": 'https://www.bloomingdales.com/shop/villeroy-boch?id=1004055',
            "category": 'villeroy-boch',
            "department": 'villeroy-boch',
        },
    },
    'vince': {
        'vince': {
            "url": 'https://www.bloomingdales.com/shop/vince?id=1004122',
            "category": 'vince',
            "department": 'vince',
        },
        'vince-handbags': {
            "url": 'https://www.bloomingdales.com/shop/vince/handbags?id=1316198',
            "category": 'vince-handbags',
            "department": 'vince',
        },
        'vince-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/vince/mens-clothing?id=1004127',
            "category": 'vince-mens-clothing',
            "department": 'vince',
        },
        'vince-mens-shoes-accessories': {
            "url": 'https://www.bloomingdales.com/shop/vince/mens-shoes-accessories?id=1292197',
            "category": 'vince-mens-shoes-accessories',
            "department": 'vince',
        },
        'vince-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/vince/womens-clothing?id=1004124',
            "category": 'vince-womens-clothing',
            "department": 'vince',
        },
        'vince-womens-shoes': {
            "url": 'https://www.bloomingdales.com/shop/vince/womens-shoes?id=1004125',
            "category": 'vince-womens-shoes',
            "department": 'vince',
        },
    },
    'vince-camuto': {
        'vince-camuto': {
            "url": 'https://www.bloomingdales.com/shop/vince-camuto?id=1004133',
            "category": 'vince-camuto',
            "department": 'vince-camuto',
        },
        'vince-camuto-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/vince-camuto/womens-clothing?id=1004134',
            "category": 'vince-camuto-womens-clothing',
            "department": 'vince-camuto',
        },
    },
    'viral-beauty-products': {
        'viral-beauty-products': {
            "url": 'https://www.bloomingdales.com/shop/viral-beauty-products?id=1224826',
            "category": 'viral-beauty-products',
            "department": 'viral-beauty-products',
        },
    },
    'vuori': {
        'vuori': {
            "url": 'https://www.bloomingdales.com/shop/vuori?id=1291095',
            "category": 'vuori',
            "department": 'vuori',
        },
        'vuori-mens': {
            "url": 'https://www.bloomingdales.com/shop/vuori/mens?id=1291097',
            "category": 'vuori-mens',
            "department": 'vuori',
        },
        'vuori-womens': {
            "url": 'https://www.bloomingdales.com/shop/vuori/womens?id=1291096',
            "category": 'vuori-womens',
            "department": 'vuori',
        },
    },
    'watches': {
        'watches': {
            "url": 'https://www.bloomingdales.com/shop/watches?id=23649',
            "category": 'watches',
            "department": 'watches',
        },
    },
    'watches-under-200': {
        'watches-under-200': {
            "url": 'https://www.bloomingdales.com/shop/watches-under-200?id=1017059',
            "category": 'watches-under-200',
            "department": 'watches-under-200',
        },
    },
    'waterford': {
        'waterford': {
            "url": 'https://www.bloomingdales.com/shop/waterford?id=1296312',
            "category": 'waterford',
            "department": 'waterford',
        },
        'waterford-mastercraft': {
            "url": 'https://www.bloomingdales.com/shop/waterford/mastercraft?id=1296316',
            "category": 'waterford-mastercraft',
            "department": 'waterford',
        },
        'waterford-ready-to-gift': {
            "url": 'https://www.bloomingdales.com/shop/waterford/ready-to-gift?id=1296314',
            "category": 'waterford-ready-to-gift',
            "department": 'waterford',
        },
        'waterford-the-lismore-collection': {
            "url": 'https://www.bloomingdales.com/shop/waterford/the-lismore-collection?id=1296313',
            "category": 'waterford-the-lismore-collection',
            "department": 'waterford',
        },
        'waterford-whats-new': {
            "url": 'https://www.bloomingdales.com/shop/waterford/whats-new?id=1296315',
            "category": 'waterford-whats-new',
            "department": 'waterford',
        },
    },
    'wedding-shoes-for-men': {
        'wedding-shoes-for-men': {
            "url": 'https://www.bloomingdales.com/shop/wedding-shoes-for-men?id=1179180',
            "category": 'wedding-shoes-for-men',
            "department": 'wedding-shoes-for-men',
        },
    },
    'wedding-suits-groom-tuxedo-shoes-bow-ties': {
        'wedding-suits-groom-tuxedo-shoes-bow-ties': {
            "url": 'https://www.bloomingdales.com/shop/wedding-suits-groom-tuxedo-shoes-bow-ties?id=1179164',
            "category": 'wedding-suits-groom-tuxedo-shoes-bow-ties',
            "department": 'wedding-suits-groom-tuxedo-shoes-bow-ties',
        },
        'wedding-suits-groom-tuxedo-shoes-bow-ties-beach-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/wedding-suits-groom-tuxedo-shoes-bow-ties/beach-wedding-attire?id=1179176',
            "category": 'wedding-suits-groom-tuxedo-shoes-bow-ties-beach-wedding-attire',
            "department": 'wedding-suits-groom-tuxedo-shoes-bow-ties',
        },
        'wedding-suits-groom-tuxedo-shoes-bow-ties-black-tie-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/wedding-suits-groom-tuxedo-shoes-bow-ties/black-tie-wedding-attire?id=1179177',
            "category": 'wedding-suits-groom-tuxedo-shoes-bow-ties-black-tie-wedding-attire',
            "department": 'wedding-suits-groom-tuxedo-shoes-bow-ties',
        },
        'wedding-suits-groom-tuxedo-shoes-bow-ties-formal-wedding-attire': {
            "url": 'https://www.bloomingdales.com/shop/wedding-suits-groom-tuxedo-shoes-bow-ties/formal-wedding-attire?id=1179178',
            "category": 'wedding-suits-groom-tuxedo-shoes-bow-ties-formal-wedding-attire',
            "department": 'wedding-suits-groom-tuxedo-shoes-bow-ties',
        },
        'wedding-suits-groom-tuxedo-shoes-bow-ties-wedding-shoes-for-men': {
            "url": 'https://www.bloomingdales.com/shop/wedding-suits-groom-tuxedo-shoes-bow-ties/wedding-shoes-for-men?id=1179165',
            "category": 'wedding-suits-groom-tuxedo-shoes-bow-ties-wedding-shoes-for-men',
            "department": 'wedding-suits-groom-tuxedo-shoes-bow-ties',
        },
    },
    'wellchemist-clean-beauty': {
        'wellchemist-clean-beauty': {
            "url": 'https://www.bloomingdales.com/shop/wellchemist-clean-beauty?id=1224764',
            "category": 'wellchemist-clean-beauty',
            "department": 'wellchemist-clean-beauty',
        },
    },
    'whats-my-size-oval-155-qt': {
        'whats-my-size-oval-155-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-oval-155-qt?id=1021573',
            "category": 'whats-my-size-oval-155-qt',
            "department": 'whats-my-size-oval-155-qt',
        },
    },
    'whats-my-size-oval-5-qt': {
        'whats-my-size-oval-5-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-oval-5-qt?id=1021570',
            "category": 'whats-my-size-oval-5-qt',
            "department": 'whats-my-size-oval-5-qt',
        },
    },
    'whats-my-size-oval-675-qt': {
        'whats-my-size-oval-675-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-oval-675-qt?id=1021571',
            "category": 'whats-my-size-oval-675-qt',
            "department": 'whats-my-size-oval-675-qt',
        },
    },
    'whats-my-size-oval-95-qt': {
        'whats-my-size-oval-95-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-oval-95-qt?id=1021572',
            "category": 'whats-my-size-oval-95-qt',
            "department": 'whats-my-size-oval-95-qt',
        },
    },
    'whats-my-size-round-1325-qt': {
        'whats-my-size-round-1325-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-round-1325-qt?id=1021569',
            "category": 'whats-my-size-round-1325-qt',
            "department": 'whats-my-size-round-1325-qt',
        },
    },
    'whats-my-size-round-2-qt': {
        'whats-my-size-round-2-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-round-2-qt?id=1021562',
            "category": 'whats-my-size-round-2-qt',
            "department": 'whats-my-size-round-2-qt',
        },
    },
    'whats-my-size-round-45-qt': {
        'whats-my-size-round-45-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-round-45-qt?id=1021563',
            "category": 'whats-my-size-round-45-qt',
            "department": 'whats-my-size-round-45-qt',
        },
    },
    'whats-my-size-round-55-qt': {
        'whats-my-size-round-55-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-round-55-qt?id=1021564',
            "category": 'whats-my-size-round-55-qt',
            "department": 'whats-my-size-round-55-qt',
        },
    },
    'whats-my-size-round-725-qt': {
        'whats-my-size-round-725-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-round-725-qt?id=1021565',
            "category": 'whats-my-size-round-725-qt',
            "department": 'whats-my-size-round-725-qt',
        },
    },
    'whats-my-size-round-9-qt': {
        'whats-my-size-round-9-qt': {
            "url": 'https://www.bloomingdales.com/shop/whats-my-size-round-9-qt?id=1021568',
            "category": 'whats-my-size-round-9-qt',
            "department": 'whats-my-size-round-9-qt',
        },
    },
    'white-orchid-collection': {
        'white-orchid-collection': {
            "url": 'https://www.bloomingdales.com/shop/white-orchid-collection?id=1310597',
            "category": 'white-orchid-collection',
            "department": 'white-orchid-collection',
        },
    },
    'william-yeoward-crystal': {
        'william-yeoward-crystal': {
            "url": 'https://www.bloomingdales.com/shop/william-yeoward-crystal?id=1326896',
            "category": 'william-yeoward-crystal',
            "department": 'william-yeoward-crystal',
        },
    },
    'window-curtains': {
        'window-curtains': {
            "url": 'https://www.bloomingdales.com/shop/window-curtains?id=1151589',
            "category": 'window-curtains',
            "department": 'window-curtains',
        },
    },
    'window-into-seoul': {
        'window-into-seoul': {
            "url": 'https://www.bloomingdales.com/shop/window-into-seoul?id=1078059',
            "category": 'window-into-seoul',
            "department": 'window-into-seoul',
        },
    },
    'wine-carafes-decanters': {
        'wine-carafes-decanters': {
            "url": 'https://www.bloomingdales.com/shop/wine-carafes-decanters?id=1054666',
            "category": 'wine-carafes-decanters',
            "department": 'wine-carafes-decanters',
        },
    },
    'winter-accessories': {
        'winter-accessories': {
            "url": 'https://www.bloomingdales.com/shop/winter-accessories?id=1214684',
            "category": 'winter-accessories',
            "department": 'winter-accessories',
        },
    },
    'women': {
        'womens-apparel': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel?id=2910',
            "category": 'womens-apparel',
            "department": 'women',
        },
        'womens-apparel-a-line': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/a-line?id=1231575',
            "category": 'womens-apparel-a-line',
            "department": 'women',
        },
        'womens-apparel-a-line-skirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/a-line-skirts?id=1004870',
            "category": 'womens-apparel-a-line-skirts',
            "department": 'women',
        },
        'womens-apparel-activewear-workout-clothes': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/activewear-workout-clothes?id=11817',
            "category": 'womens-apparel-activewear-workout-clothes',
            "department": 'women',
        },
        'womens-apparel-aqua-french-connection-sunset-spring': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/aqua-french-connection-sunset-spring?id=1329095',
            "category": 'womens-apparel-aqua-french-connection-sunset-spring',
            "department": 'women',
        },
        'womens-apparel-backless-bra': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/backless-bra?id=1006073',
            "category": 'womens-apparel-backless-bra',
            "department": 'women',
        },
        'womens-apparel-barn-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/barn-jackets?id=1132759',
            "category": 'womens-apparel-barn-jackets',
            "department": 'women',
        },
        'womens-apparel-barrel-leg-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/barrel-leg-jeans?id=1211767',
            "category": 'womens-apparel-barrel-leg-jeans',
            "department": 'women',
        },
        'womens-apparel-beach-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/beach-dresses?id=1151459',
            "category": 'womens-apparel-beach-dresses',
            "department": 'women',
        },
        'womens-apparel-best-sellers': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/best-sellers?id=1006685',
            "category": 'womens-apparel-best-sellers',
            "department": 'women',
        },
        'womens-apparel-best-selling-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/best-selling-jeans?id=1034459',
            "category": 'womens-apparel-best-selling-jeans',
            "department": 'women',
        },
        'womens-apparel-bikini-bottoms': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bikini-bottoms?id=1016361',
            "category": 'womens-apparel-bikini-bottoms',
            "department": 'women',
        },
        'womens-apparel-bikini-bottoms-bikini-panties': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bikini-bottoms-bikini-panties?id=1006092',
            "category": 'womens-apparel-bikini-bottoms-bikini-panties',
            "department": 'women',
        },
        'womens-apparel-bikini-sets-high-waisted-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bikini-sets-high-waisted-swimwear?id=1032159',
            "category": 'womens-apparel-bikini-sets-high-waisted-swimwear',
            "department": 'women',
        },
        'womens-apparel-bikini-tops': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bikini-tops?id=1016360',
            "category": 'womens-apparel-bikini-tops',
            "department": 'women',
        },
        'womens-apparel-blazers': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/blazers?id=1005879',
            "category": 'womens-apparel-blazers',
            "department": 'women',
        },
        'womens-apparel-blouses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/blouses?id=1004919',
            "category": 'womens-apparel-blouses',
            "department": 'women',
        },
        'womens-apparel-bodysuits': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bodysuits?id=1056659',
            "category": 'womens-apparel-bodysuits',
            "department": 'women',
        },
        'womens-apparel-bootcut-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bootcut-jeans?id=1004854',
            "category": 'womens-apparel-bootcut-jeans',
            "department": 'women',
        },
        'womens-apparel-bootcut-straight-pants': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bootcut-straight-pants?id=1004859',
            "category": 'womens-apparel-bootcut-straight-pants',
            "department": 'women',
        },
        'womens-apparel-boudoir-sexy-lingerie': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/boudoir-sexy-lingerie?id=1000622',
            "category": 'womens-apparel-boudoir-sexy-lingerie',
            "department": 'women',
        },
        'womens-apparel-boyfriend-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/boyfriend-jeans?id=1004902',
            "category": 'womens-apparel-boyfriend-jeans',
            "department": 'women',
        },
        'womens-apparel-boyshorts-hipster-panties': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/boyshorts-hipster-panties?id=1006093',
            "category": 'womens-apparel-boyshorts-hipster-panties',
            "department": 'women',
        },
        'womens-apparel-bralette-lace-halter-bralettes': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bralette-lace-halter-bralettes?id=1006075',
            "category": 'womens-apparel-bralette-lace-halter-bralettes',
            "department": 'women',
        },
        'womens-apparel-bras': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bras?id=5567',
            "category": 'womens-apparel-bras',
            "department": 'women',
        },
        'womens-apparel-bras-panties-sets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/bras-panties-sets?id=22935',
            "category": 'womens-apparel-bras-panties-sets',
            "department": 'women',
        },
        'womens-apparel-briefs-high-waisted-underwear': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/briefs-high-waisted-underwear?id=1006094',
            "category": 'womens-apparel-briefs-high-waisted-underwear',
            "department": 'women',
        },
        'womens-apparel-button-down-shirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/button-down-shirts?id=1069759',
            "category": 'womens-apparel-button-down-shirts',
            "department": 'women',
        },
        'womens-apparel-buy-more-save-more': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/buy-more-save-more?id=1016960',
            "category": 'womens-apparel-buy-more-save-more',
            "department": 'women',
        },
        'womens-apparel-camisoles': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/camisoles?id=1304289',
            "category": 'womens-apparel-camisoles',
            "department": 'women',
        },
        'womens-apparel-camisoles-slips': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/camisoles-slips?id=5577',
            "category": 'womens-apparel-camisoles-slips',
            "department": 'women',
        },
        'womens-apparel-cardigans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/cardigans?id=1004890',
            "category": 'womens-apparel-cardigans',
            "department": 'women',
        },
        'womens-apparel-cashmere-cardigans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/cashmere-cardigans?id=1328299',
            "category": 'womens-apparel-cashmere-cardigans',
            "department": 'women',
        },
        'womens-apparel-cashmere-crewneck-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/cashmere-crewneck-sweaters?id=1328297',
            "category": 'womens-apparel-cashmere-crewneck-sweaters',
            "department": 'women',
        },
        'womens-apparel-cashmere-turtleneck-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/cashmere-turtleneck-sweaters?id=1328298',
            "category": 'womens-apparel-cashmere-turtleneck-sweaters',
            "department": 'women',
        },
        'womens-apparel-cashmere-v-neck-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/cashmere-v-neck-sweaters?id=1328296',
            "category": 'womens-apparel-cashmere-v-neck-sweaters',
            "department": 'women',
        },
        'womens-apparel-chemises': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/chemises?id=1304260',
            "category": 'womens-apparel-chemises',
            "department": 'women',
        },
        'womens-apparel-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/coats-jackets?id=1001520',
            "category": 'womens-apparel-coats-jackets',
            "department": 'women',
        },
        'womens-apparel-crewneck-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/crewneck-sweaters?id=1004891',
            "category": 'womens-apparel-crewneck-sweaters',
            "department": 'women',
        },
        'womens-apparel-cropped-pants': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/cropped-pants?id=1004860',
            "category": 'womens-apparel-cropped-pants',
            "department": 'women',
        },
        'womens-apparel-day-casual-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/day-casual-dresses?id=1005208',
            "category": 'womens-apparel-day-casual-dresses',
            "department": 'women',
        },
        'womens-apparel-denim': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/denim?id=1231580',
            "category": 'womens-apparel-denim',
            "department": 'women',
        },
        'womens-apparel-denim-skirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/denim-skirts?id=1205959',
            "category": 'womens-apparel-denim-skirts',
            "department": 'women',
        },
        'womens-apparel-designer-cocktail-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/designer-cocktail-dresses?id=1005206',
            "category": 'womens-apparel-designer-cocktail-dresses',
            "department": 'women',
        },
        'womens-apparel-designer-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/designer-dresses?id=21683',
            "category": 'womens-apparel-designer-dresses',
            "department": 'women',
        },
        'womens-apparel-designer-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/designer-jeans?id=1279540',
            "category": 'womens-apparel-designer-jeans',
            "department": 'women',
        },
        'womens-apparel-designer-jeans-under-100-dollars': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/designer-jeans-under-100-dollars?id=1005785',
            "category": 'womens-apparel-designer-jeans-under-100-dollars',
            "department": 'women',
        },
        'womens-apparel-down-alternative-coats-puffer-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/down-alternative-coats-puffer-jackets?id=1005972',
            "category": 'womens-apparel-down-alternative-coats-puffer-jackets',
            "department": 'women',
        },
        'womens-apparel-drawstring-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/drawstring-jeans?id=1304496',
            "category": 'womens-apparel-drawstring-jeans',
            "department": 'women',
        },
        'womens-apparel-exclusive-offer-womens-coats': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/exclusive-offer-womens-coats?id=1044259',
            "category": 'womens-apparel-exclusive-offer-womens-coats',
            "department": 'women',
        },
        'womens-apparel-fall-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/fall-dresses?id=1015859',
            "category": 'womens-apparel-fall-dresses',
            "department": 'women',
        },
        'womens-apparel-fall-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/fall-jackets?id=1001979',
            "category": 'womens-apparel-fall-jackets',
            "department": 'women',
        },
        'womens-apparel-fashion-finds-under-200': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/fashion-finds-under-200?id=1147959',
            "category": 'womens-apparel-fashion-finds-under-200',
            "department": 'women',
        },
        'womens-apparel-faux-fur-mink-coats': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/faux-fur-mink-coats?id=1005975',
            "category": 'womens-apparel-faux-fur-mink-coats',
            "department": 'women',
        },
        'womens-apparel-festive-holiday-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/festive-holiday-sweaters?id=1295002',
            "category": 'womens-apparel-festive-holiday-sweaters',
            "department": 'women',
        },
        'womens-apparel-flare-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/flare-jeans?id=1304495',
            "category": 'womens-apparel-flare-jeans',
            "department": 'women',
        },
        'womens-apparel-fleece-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/fleece-jackets?id=1304259',
            "category": 'womens-apparel-fleece-jackets',
            "department": 'women',
        },
        'womens-apparel-formal-dresses-evening-gowns': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/formal-dresses-evening-gowns?id=1005210',
            "category": 'womens-apparel-formal-dresses-evening-gowns',
            "department": 'women',
        },
        'womens-apparel-full-coverage-bras': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/full-coverage-bras?id=1006080',
            "category": 'womens-apparel-full-coverage-bras',
            "department": 'women',
        },
        'womens-apparel-garden-party-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/garden-party-dresses?id=1201559',
            "category": 'womens-apparel-garden-party-dresses',
            "department": 'women',
        },
        'womens-apparel-going-out-tops': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/going-out-tops?id=1303895',
            "category": 'womens-apparel-going-out-tops',
            "department": 'women',
        },
        'womens-apparel-graduation-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/graduation-dresses?id=1313095',
            "category": 'womens-apparel-graduation-dresses',
            "department": 'women',
        },
        'womens-apparel-holiday-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/holiday-dresses?id=1139359',
            "category": 'womens-apparel-holiday-dresses',
            "department": 'women',
        },
        'womens-apparel-homecoming-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/homecoming-dresses?id=1003094',
            "category": 'womens-apparel-homecoming-dresses',
            "department": 'women',
        },
        'womens-apparel-homecoming-dresses-under-200': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/homecoming-dresses-under-200?id=1005355',
            "category": 'womens-apparel-homecoming-dresses-under-200',
            "department": 'women',
        },
        'womens-apparel-jean-shorts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/jean-shorts?id=1004908',
            "category": 'womens-apparel-jean-shorts',
            "department": 'women',
        },
        'womens-apparel-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/jeans?id=5545',
            "category": 'womens-apparel-jeans',
            "department": 'women',
        },
        'womens-apparel-jeans-to-know': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/jeans-to-know?id=1327495',
            "category": 'womens-apparel-jeans-to-know',
            "department": 'women',
        },
        'womens-apparel-joggers': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/joggers?id=1004863',
            "category": 'womens-apparel-joggers',
            "department": 'women',
        },
        'womens-apparel-jumpsuits': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/jumpsuits?id=15299',
            "category": 'womens-apparel-jumpsuits',
            "department": 'women',
        },
        'womens-apparel-leather': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/leather?id=1231579',
            "category": 'womens-apparel-leather',
            "department": 'women',
        },
        'womens-apparel-leather-coats-shearling-coats': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/leather-coats-shearling-coats?id=1005976',
            "category": 'womens-apparel-leather-coats-shearling-coats',
            "department": 'women',
        },
        'womens-apparel-leggings': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/leggings?id=1004857',
            "category": 'womens-apparel-leggings',
            "department": 'women',
        },
        'womens-apparel-lightweight-denim': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/lightweight-denim?id=1235971',
            "category": 'womens-apparel-lightweight-denim',
            "department": 'women',
        },
        'womens-apparel-linen': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/linen?id=1197859',
            "category": 'womens-apparel-linen',
            "department": 'women',
        },
        'womens-apparel-lingerie': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/lingerie?id=1304257',
            "category": 'womens-apparel-lingerie',
            "department": 'women',
        },
        'womens-apparel-lingerie-accessories': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/lingerie-accessories?id=1073259',
            "category": 'womens-apparel-lingerie-accessories',
            "department": 'women',
        },
        'womens-apparel-lingerie-bras-panties': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/lingerie-bras-panties?id=1304898',
            "category": 'womens-apparel-lingerie-bras-panties',
            "department": 'women',
        },
        'womens-apparel-lingerie-bras-panties-shapewear': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/lingerie-bras-panties-shapewear?id=5566',
            "category": 'womens-apparel-lingerie-bras-panties-shapewear',
            "department": 'women',
        },
        'womens-apparel-lounge-tops': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/lounge-tops?id=1209861',
            "category": 'womens-apparel-lounge-tops',
            "department": 'women',
        },
        'womens-apparel-loungewear': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/loungewear?id=1065461',
            "category": 'womens-apparel-loungewear',
            "department": 'women',
        },
        'womens-apparel-loungewear-sets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/loungewear-sets?id=1082459',
            "category": 'womens-apparel-loungewear-sets',
            "department": 'women',
        },
        'womens-apparel-matching-sets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/matching-sets?id=1068159',
            "category": 'womens-apparel-matching-sets',
            "department": 'women',
        },
        'womens-apparel-maternity': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/maternity?id=1062459',
            "category": 'womens-apparel-maternity',
            "department": 'women',
        },
        'womens-apparel-maxi': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/maxi?id=1231578',
            "category": 'womens-apparel-maxi',
            "department": 'women',
        },
        'womens-apparel-maxi-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/maxi-dresses?id=1069861',
            "category": 'womens-apparel-maxi-dresses',
            "department": 'women',
        },
        'womens-apparel-midi-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/midi-dresses?id=1069860',
            "category": 'womens-apparel-midi-dresses',
            "department": 'women',
        },
        'womens-apparel-midi-skirt': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/midi-skirt?id=1231577',
            "category": 'womens-apparel-midi-skirt',
            "department": 'women',
        },
        'womens-apparel-mini': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/mini?id=1231576',
            "category": 'womens-apparel-mini',
            "department": 'women',
        },
        'womens-apparel-mini-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/mini-dresses?id=1069859',
            "category": 'womens-apparel-mini-dresses',
            "department": 'women',
        },
        'womens-apparel-multipacks': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/multipacks?id=17558',
            "category": 'womens-apparel-multipacks',
            "department": 'women',
        },
        'womens-apparel-new-arrivals': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/new-arrivals?id=3697',
            "category": 'womens-apparel-new-arrivals',
            "department": 'women',
        },
        'womens-apparel-new-now': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/new-now?id=1176460',
            "category": 'womens-apparel-new-now',
            "department": 'women',
        },
        'womens-apparel-nightgowns': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/nightgowns?id=1005103',
            "category": 'womens-apparel-nightgowns',
            "department": 'women',
        },
        'womens-apparel-one-piece-swimsuits-bathing-suits': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/one-piece-swimsuits-bathing-suits?id=1004867',
            "category": 'womens-apparel-one-piece-swimsuits-bathing-suits',
            "department": 'women',
        },
        'womens-apparel-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/pajamas?id=1005101',
            "category": 'womens-apparel-pajamas',
            "department": 'women',
        },
        'womens-apparel-panties': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/panties?id=5576',
            "category": 'womens-apparel-panties',
            "department": 'women',
        },
        'womens-apparel-pants-jeans-skirts-leggings': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/pants-jeans-skirts-leggings?id=16308',
            "category": 'womens-apparel-pants-jeans-skirts-leggings',
            "department": 'women',
        },
        'womens-apparel-pants-leggings': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/pants-leggings?id=17566',
            "category": 'womens-apparel-pants-leggings',
            "department": 'women',
        },
        'womens-apparel-parkas': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/parkas?id=1241860',
            "category": 'womens-apparel-parkas',
            "department": 'women',
        },
        'womens-apparel-pencil-skirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/pencil-skirts?id=1004871',
            "category": 'womens-apparel-pencil-skirts',
            "department": 'women',
        },
        'womens-apparel-petite-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/petite-dresses?id=1006696',
            "category": 'womens-apparel-petite-dresses',
            "department": 'women',
        },
        'womens-apparel-petite-jeans-pants': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/petite-jeans-pants?id=1006697',
            "category": 'womens-apparel-petite-jeans-pants',
            "department": 'women',
        },
        'womens-apparel-petite-sweaters-tops-tees': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/petite-sweaters-tops-tees?id=1006699',
            "category": 'womens-apparel-petite-sweaters-tops-tees',
            "department": 'women',
        },
        'womens-apparel-petites': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/petites?id=17378',
            "category": 'womens-apparel-petites',
            "department": 'women',
        },
        'womens-apparel-plus-size-clothing': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-clothing?id=2917',
            "category": 'womens-apparel-plus-size-clothing',
            "department": 'women',
        },
        'womens-apparel-plus-size-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-coats-jackets?id=5471',
            "category": 'womens-apparel-plus-size-coats-jackets',
            "department": 'women',
        },
        'womens-apparel-plus-size-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-dresses?id=5467',
            "category": 'womens-apparel-plus-size-dresses',
            "department": 'women',
        },
        'womens-apparel-plus-size-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-jeans?id=5466',
            "category": 'womens-apparel-plus-size-jeans',
            "department": 'women',
        },
        'womens-apparel-plus-size-pants-leggings': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-pants-leggings?id=1005351',
            "category": 'womens-apparel-plus-size-pants-leggings',
            "department": 'women',
        },
        'womens-apparel-plus-size-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-sweaters?id=16184',
            "category": 'womens-apparel-plus-size-sweaters',
            "department": 'women',
        },
        'womens-apparel-plus-size-swimwear-swimsuits': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-swimwear-swimsuits?id=1060059',
            "category": 'womens-apparel-plus-size-swimwear-swimsuits',
            "department": 'women',
        },
        'womens-apparel-plus-size-tops': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-tops?id=1005349',
            "category": 'womens-apparel-plus-size-tops',
            "department": 'women',
        },
        'womens-apparel-plus-size-tops-tees': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/plus-size-tops-tees?id=5503',
            "category": 'womens-apparel-plus-size-tops-tees',
            "department": 'women',
        },
        'womens-apparel-push-up-bra': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/push-up-bra?id=1006085',
            "category": 'womens-apparel-push-up-bra',
            "department": 'women',
        },
        'womens-apparel-racerback-bra': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/racerback-bra?id=1006086',
            "category": 'womens-apparel-racerback-bra',
            "department": 'women',
        },
        'womens-apparel-rain-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/rain-jackets?id=1133359',
            "category": 'womens-apparel-rain-jackets',
            "department": 'women',
        },
        'womens-apparel-ripped': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/ripped?id=1004904',
            "category": 'womens-apparel-ripped',
            "department": 'women',
        },
        'womens-apparel-robes': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/robes?id=1005102',
            "category": 'womens-apparel-robes',
            "department": 'women',
        },
        'womens-apparel-rompers': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/rompers?id=1004899',
            "category": 'womens-apparel-rompers',
            "department": 'women',
        },
        'womens-apparel-shapewear': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/shapewear?id=1000089',
            "category": 'womens-apparel-shapewear',
            "department": 'women',
        },
        'womens-apparel-shop-all': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/shop-all?id=1001581',
            "category": 'womens-apparel-shop-all',
            "department": 'women',
        },
        'womens-apparel-shorts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/shorts?id=19950',
            "category": 'womens-apparel-shorts',
            "department": 'women',
        },
        'womens-apparel-silk-pajamas-robes': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/silk-pajamas-robes?id=1210459',
            "category": 'womens-apparel-silk-pajamas-robes',
            "department": 'women',
        },
        'womens-apparel-skinny-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/skinny-jeans?id=1004906',
            "category": 'womens-apparel-skinny-jeans',
            "department": 'women',
        },
        'womens-apparel-skinny-pants': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/skinny-pants?id=1004862',
            "category": 'womens-apparel-skinny-pants',
            "department": 'women',
        },
        'womens-apparel-skirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/skirts?id=19951',
            "category": 'womens-apparel-skirts',
            "department": 'women',
        },
        'womens-apparel-skirts-shorts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/skirts-shorts?id=1005352',
            "category": 'womens-apparel-skirts-shorts',
            "department": 'women',
        },
        'womens-apparel-sleepwear-night-gowns-pajamas': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sleepwear-night-gowns-pajamas?id=1005121',
            "category": 'womens-apparel-sleepwear-night-gowns-pajamas',
            "department": 'women',
        },
        'womens-apparel-sleepwear-robes': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sleepwear-robes?id=21429',
            "category": 'womens-apparel-sleepwear-robes',
            "department": 'women',
        },
        'womens-apparel-socks': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/socks?id=1335301',
            "category": 'womens-apparel-socks',
            "department": 'women',
        },
        'womens-apparel-socks-no-show-socks-ankle-socks': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/socks-no-show-socks-ankle-socks?id=1006098',
            "category": 'womens-apparel-socks-no-show-socks-ankle-socks',
            "department": 'women',
        },
        'womens-apparel-sports-bras': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sports-bras?id=1066959',
            "category": 'womens-apparel-sports-bras',
            "department": 'women',
        },
        'womens-apparel-spring-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/spring-dresses?id=1006843',
            "category": 'womens-apparel-spring-dresses',
            "department": 'women',
        },
        'womens-apparel-spring-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/spring-jackets?id=1225185',
            "category": 'womens-apparel-spring-jackets',
            "department": 'women',
        },
        'womens-apparel-straight': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/straight?id=1135661',
            "category": 'womens-apparel-straight',
            "department": 'women',
        },
        'womens-apparel-straight-leg-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/straight-leg-jeans?id=1004907',
            "category": 'womens-apparel-straight-leg-jeans',
            "department": 'women',
        },
        'womens-apparel-strapless-bras-convertible-bras': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/strapless-bras-convertible-bras?id=1006088',
            "category": 'womens-apparel-strapless-bras-convertible-bras',
            "department": 'women',
        },
        'womens-apparel-suede-shearling': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/suede-shearling?id=1241859',
            "category": 'womens-apparel-suede-shearling',
            "department": 'women',
        },
        'womens-apparel-summer-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/summer-dresses?id=1006842',
            "category": 'womens-apparel-summer-dresses',
            "department": 'women',
        },
        'womens-apparel-summer-skirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/summer-skirts?id=1231581',
            "category": 'womens-apparel-summer-skirts',
            "department": 'women',
        },
        'womens-apparel-sunset-spring': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sunset-spring?id=1008159',
            "category": 'womens-apparel-sunset-spring',
            "department": 'women',
        },
        'womens-apparel-sutton-studio': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sutton-studio?id=1005127',
            "category": 'womens-apparel-sutton-studio',
            "department": 'women',
        },
        'womens-apparel-sweater-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sweater-dresses?id=1173260',
            "category": 'womens-apparel-sweater-dresses',
            "department": 'women',
        },
        'womens-apparel-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sweaters?id=12374',
            "category": 'womens-apparel-sweaters',
            "department": 'women',
        },
        'womens-apparel-sweaters-under-100': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sweaters-under-100?id=1003699',
            "category": 'womens-apparel-sweaters-under-100',
            "department": 'women',
        },
        'womens-apparel-sweatpants': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sweatpants?id=1135660',
            "category": 'womens-apparel-sweatpants',
            "department": 'women',
        },
        'womens-apparel-sweatshirts-pullover-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/sweatshirts-pullover-sweaters?id=1021566',
            "category": 'womens-apparel-sweatshirts-pullover-sweaters',
            "department": 'women',
        },
        'womens-apparel-swimsuit-bathing-suit-coverups': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/swimsuit-bathing-suit-coverups?id=1004874',
            "category": 'womens-apparel-swimsuit-bathing-suit-coverups',
            "department": 'women',
        },
        'womens-apparel-t-shirt-bra-t-back-bra': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/t-shirt-bra-t-back-bra?id=1006089',
            "category": 'womens-apparel-t-shirt-bra-t-back-bra',
            "department": 'women',
        },
        'womens-apparel-tank-tops-camisoles': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tank-tops-camisoles?id=1004921',
            "category": 'womens-apparel-tank-tops-camisoles',
            "department": 'women',
        },
        'womens-apparel-tankini-swimsuits': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tankini-swimsuits?id=1004872',
            "category": 'womens-apparel-tankini-swimsuits',
            "department": 'women',
        },
        'womens-apparel-tees': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tees?id=1004920',
            "category": 'womens-apparel-tees',
            "department": 'women',
        },
        'womens-apparel-tees-tanks': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tees-tanks?id=1005350',
            "category": 'womens-apparel-tees-tanks',
            "department": 'women',
        },
        'womens-apparel-the-new-view': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/the-new-view?id=1005163',
            "category": 'womens-apparel-the-new-view',
            "department": 'women',
        },
        'womens-apparel-thongs': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/thongs?id=1006095',
            "category": 'womens-apparel-thongs',
            "department": 'women',
        },
        'womens-apparel-tights-hosiery-pantyhose': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tights-hosiery-pantyhose?id=1006096',
            "category": 'womens-apparel-tights-hosiery-pantyhose',
            "department": 'women',
        },
        'womens-apparel-tights-socks-hosiery': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tights-socks-hosiery?id=22314',
            "category": 'womens-apparel-tights-socks-hosiery',
            "department": 'women',
        },
        'womens-apparel-tops-tees': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tops-tees?id=5619',
            "category": 'womens-apparel-tops-tees',
            "department": 'women',
        },
        'womens-apparel-tops-under-100-dollars': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tops-under-100-dollars?id=1002083',
            "category": 'womens-apparel-tops-under-100-dollars',
            "department": 'women',
        },
        'womens-apparel-trending-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/trending-dresses?id=1313197',
            "category": 'womens-apparel-trending-dresses',
            "department": 'women',
        },
        'womens-apparel-trending-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/trending-jeans?id=1311495',
            "category": 'womens-apparel-trending-jeans',
            "department": 'women',
        },
        'womens-apparel-trending-swimwear': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/trending-swimwear?id=1315395',
            "category": 'womens-apparel-trending-swimwear',
            "department": 'women',
        },
        'womens-apparel-turtleneck-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/turtleneck-sweaters?id=1004892',
            "category": 'womens-apparel-turtleneck-sweaters',
            "department": 'women',
        },
        'womens-apparel-tweed-lady-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/tweed-lady-jackets?id=1263295',
            "category": 'womens-apparel-tweed-lady-jackets',
            "department": 'women',
        },
        'womens-apparel-underwire-bra': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/underwire-bra?id=1006090',
            "category": 'womens-apparel-underwire-bra',
            "department": 'women',
        },
        'womens-apparel-utility-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/utility-jackets?id=1304258',
            "category": 'womens-apparel-utility-jackets',
            "department": 'women',
        },
        'womens-apparel-v-neck-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/v-neck-sweaters?id=1004893',
            "category": 'womens-apparel-v-neck-sweaters',
            "department": 'women',
        },
        'womens-apparel-vests': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/vests?id=1232762',
            "category": 'womens-apparel-vests',
            "department": 'women',
        },
        'womens-apparel-vests-fur-denim-vests': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/vests-fur-denim-vests?id=1005883',
            "category": 'womens-apparel-vests-fur-denim-vests',
            "department": 'women',
        },
        'womens-apparel-wedding-lingerie-bridal-robes': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/wedding-lingerie-bridal-robes?id=1000321',
            "category": 'womens-apparel-wedding-lingerie-bridal-robes',
            "department": 'women',
        },
        'womens-apparel-white-denim': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/white-denim?id=1004780',
            "category": 'womens-apparel-white-denim',
            "department": 'women',
        },
        'womens-apparel-wide-leg-jeans': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/wide-leg-jeans?id=1004905',
            "category": 'womens-apparel-wide-leg-jeans',
            "department": 'women',
        },
        'womens-apparel-wide-leg-pants': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/wide-leg-pants?id=1004861',
            "category": 'womens-apparel-wide-leg-pants',
            "department": 'women',
        },
        'womens-apparel-winter-coats-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/winter-coats-jackets?id=1003366',
            "category": 'womens-apparel-winter-coats-jackets',
            "department": 'women',
        },
        'womens-apparel-wireless-bras': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/wireless-bras?id=1006091',
            "category": 'womens-apparel-wireless-bras',
            "department": 'women',
        },
        'womens-apparel-womens-activewear-sets-and-matching-workout-sets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-activewear-sets-and-matching-workout-sets?id=1067559',
            "category": 'womens-apparel-womens-activewear-sets-and-matching-workout-sets',
            "department": 'women',
        },
        'womens-apparel-womens-cashmere-sweaters': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-cashmere-sweaters?id=1063159',
            "category": 'womens-apparel-womens-cashmere-sweaters',
            "department": 'women',
        },
        'womens-apparel-womens-designer-hoodies-and-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-designer-hoodies-and-sweatshirts?id=1066859',
            "category": 'womens-apparel-womens-designer-hoodies-and-sweatshirts',
            "department": 'women',
        },
        'womens-apparel-womens-lightweight-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-lightweight-jackets?id=1059860',
            "category": 'womens-apparel-womens-lightweight-jackets',
            "department": 'women',
        },
        'womens-apparel-womens-luxury-loungewear': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-luxury-loungewear?id=1090360',
            "category": 'womens-apparel-womens-luxury-loungewear',
            "department": 'women',
        },
        'womens-apparel-womens-pajama-sets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-pajama-sets?id=1081360',
            "category": 'womens-apparel-womens-pajama-sets',
            "department": 'women',
        },
        'womens-apparel-womens-quilted-jackets-and-coats': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-quilted-jackets-and-coats?id=1072261',
            "category": 'womens-apparel-womens-quilted-jackets-and-coats',
            "department": 'women',
        },
        'womens-apparel-womens-swimsuits': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-swimsuits?id=1027052',
            "category": 'womens-apparel-womens-swimsuits',
            "department": 'women',
        },
        'womens-apparel-womens-utility-jackets-and-denim-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/womens-utility-jackets-and-denim-jackets?id=1072260',
            "category": 'womens-apparel-womens-utility-jackets-and-denim-jackets',
            "department": 'women',
        },
        'womens-apparel-wool-and-wool-blend-coats': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/wool-and-wool-blend-coats?id=1005974',
            "category": 'womens-apparel-wool-and-wool-blend-coats',
            "department": 'women',
        },
        'womens-apparel-work-business-professional-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/work-business-professional-dresses?id=1005214',
            "category": 'womens-apparel-work-business-professional-dresses',
            "department": 'women',
        },
        'womens-apparel-workout-dresses': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/workout-dresses?id=1186667',
            "category": 'womens-apparel-workout-dresses',
            "department": 'women',
        },
        'womens-apparel-workout-jackets': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/workout-jackets?id=1186665',
            "category": 'womens-apparel-workout-jackets',
            "department": 'women',
        },
        'womens-apparel-workout-leggings': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/workout-leggings?id=1186559',
            "category": 'womens-apparel-workout-leggings',
            "department": 'women',
        },
        'womens-apparel-workout-shorts-skirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/workout-shorts-skirts?id=1186668',
            "category": 'womens-apparel-workout-shorts-skirts',
            "department": 'women',
        },
        'womens-apparel-workout-tops': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/workout-tops?id=1186664',
            "category": 'womens-apparel-workout-tops',
            "department": 'women',
        },
        'womens-apparel-yoga-pilates': {
            "url": 'https://www.bloomingdales.com/shop/womens-apparel/yoga-pilates?id=1206566',
            "category": 'womens-apparel-yoga-pilates',
            "department": 'women',
        },
    },
    'womens-cashmere-clothing': {
        'womens-cashmere-clothing': {
            "url": 'https://www.bloomingdales.com/shop/womens-cashmere-clothing?id=1000658',
            "category": 'womens-cashmere-clothing',
            "department": 'womens-cashmere-clothing',
        },
    },
    'womens-clothes': {
        'womens-clothes': {
            "url": 'https://www.bloomingdales.com/shop/womens-clothes?id=1250496',
            "category": 'womens-clothes',
            "department": 'womens-clothes',
        },
    },
    'womens-clothing': {
        'womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/womens-clothing?id=1319125',
            "category": 'womens-clothing',
            "department": 'womens-clothing',
        },
    },
    'womens-fall-trends': {
        'womens-fall-trends': {
            "url": 'https://www.bloomingdales.com/shop/womens-fall-trends?id=1265496',
            "category": 'womens-fall-trends',
            "department": 'womens-fall-trends',
        },
    },
    'womens-luxury-loungewear': {
        'womens-luxury-loungewear': {
            "url": 'https://www.bloomingdales.com/shop/womens-luxury-loungewear?id=1324104',
            "category": 'womens-luxury-loungewear',
            "department": 'womens-luxury-loungewear',
        },
    },
    'womens-sweatpants-sweatshirts': {
        'womens-sweatpants-sweatshirts': {
            "url": 'https://www.bloomingdales.com/shop/womens-sweatpants-sweatshirts?id=1141264',
            "category": 'womens-sweatpants-sweatshirts',
            "department": 'womens-sweatpants-sweatshirts',
        },
    },
    'womens-swimsuits': {
        'womens-swimsuits': {
            "url": 'https://www.bloomingdales.com/shop/womens-swimsuits?id=1156960',
            "category": 'womens-swimsuits',
            "department": 'womens-swimsuits',
        },
    },
    'womens-watches-under-200': {
        'womens-watches-under-200': {
            "url": 'https://www.bloomingdales.com/shop/womens-watches-under-200?id=1015159',
            "category": 'womens-watches-under-200',
            "department": 'womens-watches-under-200',
        },
    },
    'world-bazaar': {
        'world-bazaar': {
            "url": 'https://www.bloomingdales.com/shop/world-bazaar?id=1088359',
            "category": 'world-bazaar',
            "department": 'world-bazaar',
        },
    },
    'woven-accessories': {
        'woven-accessories': {
            "url": 'https://www.bloomingdales.com/shop/woven-accessories?id=1117161',
            "category": 'woven-accessories',
            "department": 'woven-accessories',
        },
    },
    'xerjoff': {
        'xerjoff': {
            "url": 'https://www.bloomingdales.com/shop/xerjoff?id=1286518',
            "category": 'xerjoff',
            "department": 'xerjoff',
        },
    },
    'yacht-club': {
        'yacht-club': {
            "url": 'https://www.bloomingdales.com/shop/yacht-club?id=1238679',
            "category": 'yacht-club',
            "department": 'yacht-club',
        },
    },
    'zadig-voltaire': {
        'zadig-voltaire': {
            "url": 'https://www.bloomingdales.com/shop/zadig-voltaire?id=1278795',
            "category": 'zadig-voltaire',
            "department": 'zadig-voltaire',
        },
        'zadig-voltaire-handbags': {
            "url": 'https://www.bloomingdales.com/shop/zadig-voltaire/handbags?id=1278818',
            "category": 'zadig-voltaire-handbags',
            "department": 'zadig-voltaire',
        },
        'zadig-voltaire-mens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/zadig-voltaire/mens-clothing?id=1278815',
            "category": 'zadig-voltaire-mens-clothing',
            "department": 'zadig-voltaire',
        },
        'zadig-voltaire-new-to-sale': {
            "url": 'https://www.bloomingdales.com/shop/zadig-voltaire/new-to-sale?id=1278819',
            "category": 'zadig-voltaire-new-to-sale',
            "department": 'zadig-voltaire',
        },
        'zadig-voltaire-womens-clothing': {
            "url": 'https://www.bloomingdales.com/shop/zadig-voltaire/womens-clothing?id=1278805',
            "category": 'zadig-voltaire-womens-clothing',
            "department": 'zadig-voltaire',
        },
    },
    'zegna': {
        'zegna': {
            "url": 'https://www.bloomingdales.com/shop/zegna?id=1304397',
            "category": 'zegna',
            "department": 'zegna',
        },
    },
    'zimmermann': {
        'zimmermann': {
            "url": 'https://www.bloomingdales.com/shop/zimmermann?id=1319295',
            "category": 'zimmermann',
            "department": 'zimmermann',
        },
    },
}
