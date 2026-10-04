"""Levi's (levi.com) header-navigation category inventory.

Captured 2026-10-02 from the SSR mega-menu in
`__LSCO_INITIAL_STATE__.ssrGlobalStoreCMSHeaderFooter.ssrL1Group` on
`https://www.levi.com/`. Nested as section -> mega-menu group -> link.

Only product-listing (PLP) links are kept: a link qualifies when its path
contains a `/c/` category segment. The merged mega-menu also carries CMS
landing pages (`/features/...`), PDP links (`/p/<sku>`), blogs and the
off-domain Secondhand marketplace; none of those hydrate
`ssrViewStoreProductList`, so they are excluded here rather than being
allowed to fail mid-crawl.

Note the required locale prefix: nav `link_url` values are relative and
without it, `https://www.levi.com/clothing/men/jeans/c/...` answers with an
SSR error page. Always build `https://www.levi.com/US/en_US` + link_url.
"""

import re

LEVI_SITE_BASE = "https://www.levi.com/US/en_US"

LEVI_CATEGORY_INVENTORY = {
    'New': {
        'New': {
            "Men's New Arrivals": '/new-arrivals/mens-new-arrivals/c/levi_clothing_men_new_arrivals_us',
            "Women's New Arrivals": '/new-arrivals/womens-new-arrivals/c/levi_clothing_women_new_arrivals_us',
            "Kids' New Arrivals": '/new-arrivals/kids-new-arrivals/c/levi_clothing_kids_new_arrivals_us',
        },
    },
    'Men': {
        'Men’s Jeans': {
            'Shop All Men’s Jeans': '/clothing/men/jeans/c/levi_clothing_men_jeans',
            'Straight Jeans': '/clothing/men/jeans/straight/c/levi_clothing_men_jeans_straight',
            'Loose & Baggy Jeans': '/clothing/men/jeans/loose/c/levi_clothing_men_jeans_loose',
            'Relaxed Jeans': '/clothing/men/jeans/relaxed/c/levi_clothing_men_jeans_relaxed',
            'Slim & Skinny Jeans': '/clothing/men/jeans/slim/c/levi_clothing_men_jeans_slim',
            'Tapered Jeans': '/clothing/men/jeans/taper/c/levi_clothing_men_jeans_taper',
            'Bootcut Jeans': '/clothing/men/jeans/bootcut/c/levi_clothing_men_jeans_bootcut',
        },
        'Styles We Love': {
            '501 Original': '/jeans-by-fit-number/men/jeans/501/c/levi_jeans_by_fit_number_men_jeans_501',
            'Extra Baggy Jeans': '/clothing/men/jeans/loose/c/levi_clothing_men_jeans_loose/facets/feature-fit_name/extra%20baggy',
            'Selvedge Denim': '/selvedge-denim/selvedge/c/levi_clothing_men_selvedge_us',
        },
        'Men’s Clothes': {
            'Shop All Men’s': '/clothing/men/c/levi_clothing_men',
            'Jeans': '/clothing/men/jeans/c/levi_clothing_men_jeans',
            'Pants & Chinos': '/clothing/men/pants/c/levi_clothing_men_trousers_pants',
            'Shirts & T-Shirts': '/clothing/men/shirts/c/levi_clothing_men_shirts',
            'Sweaters & Sweatshirts': '/clothing/men/sweaters-sweatshirts/c/levi_clothing_men_sweaters_sweatshirts',
            'Denim Jackets & Outerwear': '/clothing/men/outerwear/c/levi_clothing_men_outerwear',
            'Shorts': '/clothing/men/shorts/c/levi_clothing_men_shorts',
            'Overalls': '/overalls/c/levi_clothing_men_overalls',
            'Big & Tall': '/big-tall/c/levi_clothing_men_big_tall',
            'Underwear & Socks': '/underwear-socks/men/c/levi_underwear_socks_men',
            'Accessories': '/accessories/men/c/levi_accessories_men',
            'Sale': '/sale/mens-sale/c/levi_clothing_men_sale_us',
        },
        'Featured': {
            "Men's New Arrivals": '/new-arrivals/mens-new-arrivals/c/levi_clothing_men_new_arrivals_us',
            "Men's Bestsellers": '/best-sellers/men/c/levi_clothing_men_bestsellers_us',
            'Wear to Work': '/wear-to-work/c/levi_clothing_wear_to_work_us',
            "Levi's® Workwear": '/workwear/c/levi_clothing_men_workwear',
            'Blue Tab™': '/blue-tab/c/levi_clothing_blue_tab_us',
            'Selvedge Denim': '/selvedge-denim/selvedge/c/levi_clothing_men_selvedge_us',
        },
    },
    'Women': {
        "Women's Jeans": {
            "Shop All Women's Jeans": '/clothing/women/jeans/c/levi_clothing_women_jeans',
            'Trending Low Rise': '/clothing/women/jeans/low-rise/c/levi_clothing_women_jeans_low_rise',
            'Loose & Baggy Jeans': '/clothing/women/jeans/loose/c/levi_clothing_women_jeans_loose',
            'Straight Jeans': '/clothing/women/jeans/straight/c/levi_clothing_women_jeans_straight',
            'Barrel & Taper Jeans': '/clothing/women/jeans/barrel/c/levi_clothing_women_jeans_barrel',
            'Wide-Leg Jeans': '/clothing/women/jeans/wide-leg/c/levi_clothing_women_jeans_wide_leg',
            'Bootcut & Flare Jeans': '/clothing/women/jeans/bootcut/c/levi_clothing_women_jeans_bootcut',
            'Slim & Skinny Jeans': '/clothing/women/jeans/slim/c/levi_clothing_women_jeans_slim',
        },
        'Styles We Love': {
            '501® Jeans': '/jeans-by-fit-number/women/jeans/501/c/levi_jeans_by_fit_number_women_jeans_501',
            '700 Series': '/700-series/c/levi_clothing_women_700_series_us/',
            'Ribcage': '/clothing/women/jeans/ribcage-jeans/c/levi_clothing_women_jeans_ribcage',
            'Cinch': '/clothing/women/jeans/cinch-jeans/c/levi_clothing_women_jeans_cinch',
        },
        'Women’s Clothes': {
            'Shop All Women’s': '/clothing/women/c/levi_clothing_women',
            'Jeans': '/clothing/women/jeans/c/levi_clothing_women_jeans',
            'Tops': '/clothing/women/shirts-blouses-tops/c/levi_clothing_women_shirts_blouses_tops',
            'Dresses & Skirts': '/clothing/women/dresses-skirts/c/levi_clothing_women_dresses_skirts',
            'Pants': '/clothing/women/pants/c/levi_clothing_women_pants',
            'Sweaters & Sweatshirts': '/clothing/women/sweaters-sweatshirts/c/levi_clothing_women_sweaters_sweatshirts',
            'Denim Jackets & Outerwear': '/clothing/women/outerwear/c/levi_clothing_women_outerwear',
            'Overalls & Jumpsuits': '/clothing/women/overalls-jumpsuits/c/levi_clothing_women_overalls_jumpsuits',
            'Shorts': '/clothing/women/shorts/c/levi_clothing_women_shorts',
            'Accessories': '/accessories/women/c/levi_accessories_women',
            'Plus Size (14-26)': '/clothing/women/plus-size/c/levi_clothing_women_plus_sizes',
            'Sale': '/sale/womens-sale/c/levi_clothing_women_sale_us',
        },
        'Featured': {
            "Women's New Arrivals": '/new-arrivals/womens-new-arrivals/c/levi_clothing_women_new_arrivals_us',
            "Women's Bestsellers": '/best-sellers/women/c/levi_clothing_women_bestsellers_us',
            'Curve-Friendly Denim': '/curve-friendly/c/levi_clothing_curve_friendly_fits',
            'Wear to Work': '/wear-to-work/c/levi_clothing_wear_to_work_us',
            'Y2K Revival': '/trend-edits/c/levi_clothing_trend_edits_us',
            'Blue Tab™': '/blue-tab/c/levi_clothing_blue_tab_us',
            'Selvedge Denim': '/selvedge-denim/selvedge/c/levi_clothing_women_selvedge_us',
        },
    },
    'Kids': {
        'Kids’ Clothes': {
            'Shop All Kids': '/clothing/kids/c/levi_clothing_kids',
            'Boys (8-20)': '/clothing/kids/big-boys/c/levi_clothing_kids_big_boys',
            'Little Boys (4–7x)': '/clothing/kids/little-boys/c/levi_clothing_kids_little_boys',
            'Girls (7–16)': '/clothing/kids/big-girls/c/levi_clothing_kids_big_girls',
            'Little Girls (4–6x)': '/clothing/kids/little-girls/c/levi_clothing_kids_little_girls',
            'Toddler': '/clothing/kids/toddler/c/levi_clothing_kids_toddler',
            'Baby': '/clothing/kids/baby/c/levi_clothing_kids_baby',
            'Sale': '/sale/kids-sale/c/levi_clothing_kids_sale_us',
        },
        'Featured': {
            "Kids' New Arrivals": '/new-arrivals/kids-new-arrivals/c/levi_clothing_kids_new_arrivals_us',
            "Kids' Bestsellers": '/best-sellers/kids/c/levi_clothing_kids_bestsellers_us',
        },
    },
    'Sale': {
        'Men': {
            "Shop All Men's Sale": '/sale/mens-sale/c/levi_clothing_men_sale_us',
            "New to Men's Sale": '/sale/mens-sale/new-to-mens-sale/c/new_levi_clothing_men_sale_us',
            'Jeans': '/sale/mens-sale/c/levi_clothing_men_sale_us/facets/productitemtype/jeans',
            'Shirts & T-Shirts': '/sale/mens-sale/c/levi_clothing_men_sale_us/facets/productitemtype/t-shirts/productitemtype/shirts/productitemtype/tank%20tops/productitemtype/polos/productitemtype/henleys',
            'Pants & Chinos': '/sale/mens-sale/c/levi_clothing_men_sale_us/facets/productitemtype/pants/productitemtype/sweatpants',
            'Jean Jackets & Outerwear': '/sale/mens-sale/c/levi_clothing_men_sale_us/facets/productitemtype/trucker%20jean%20jacket/productitemtype/coats/productitemtype/vests/productitemtype/jackets',
            'Sweaters & Sweatshirts': '/sale/mens-sale/c/levi_clothing_men_sale_us/facets/productitemtype/sweatshirts/productitemtype/sweaters',
            'Shorts': '/sale/mens-sale/c/levi_clothing_men_sale_us/facets/productitemtype/shorts',
            'Accessories': '/sale/sale-accessories/c/levi_accessories_sale_us',
            'Big & Tall': '/sale/mens-sale/c/levi_clothing_men_sale_us/facets/feature-size_group/men%27s%20big%20%26%20tall/feature-size_group/men%27s%20tall',
        },
        'Women': {
            "Shop All Women's Sale": '/sale/womens-sale/c/levi_clothing_women_sale_us',
            "New to Women's Sale": '/sale/womens-sale/new-to-womens-sale/c/new_levi_clothing_women_sale_us',
            'Jeans': '/sale/womens-sale/jeans/c/levi_clothing_women_sale_jeans_us',
            'Tops': '/sale/womens-sale/tops/c/levi_clothing_women_sale_tops_us',
            'Pants': '/sale/womens-sale/pants/c/levi_clothing_women_sale_pants_us',
            'Jean Jackets & Outerwear': '/sale/womens-sale/outerwear/c/levi_clothing_women_sale_jackets_us',
            'Sweaters & Sweatshirts': '/sale/womens-sale/tops/c/levi_clothing_women_sale_tops_us/facets/productitemtype/sweatshirts/productitemtype/sweaters',
            'Shorts': '/sale/womens-sale/shorts-capris/c/levi_clothing_women_sale_shorts_capris_us',
            'Dresses & Skirts': '/sale/womens-sale/dresses-skirts/c/levi_clothing_women_sale_dresses_skirts_us',
            'Accessories': '/sale/sale-accessories/womens-sale-accessories/c/levi_accessories_women_sale_us',
            'Plus': '/sale/womens-sale/c/levi_clothing_women_sale_us/facets/feature-size_group/women%27s%20plus%20size',
        },
        'Kids': {
            "Shop All Kid's Sale": '/sale/kids-sale/c/levi_clothing_kids_sale_us',
        },
    },
}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _flatten_categories() -> list[dict[str, str]]:
    """Flatten the inventory into unique {category, department, url} rows.

    Section is exposed as `department` and the mega-menu group as
    `subcategory`. Names repeat across sections ("Jeans" exists under both
    Men and Women), so a bare slug is only used when it is still free;
    otherwise the section slug is prefixed, matching the Staples inventory.
    """
    categories: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    used_names: set[str] = set()
    for section, groups in LEVI_CATEGORY_INVENTORY.items():
        for group, links in groups.items():
            for label, url in links.items():
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                base = _slug(label)
                name = base
                if name in used_names:
                    name = f"{_slug(section)}-{base}"
                suffix = 2
                while name in used_names:
                    name = f"{_slug(section)}-{base}-{suffix}"
                    suffix += 1
                used_names.add(name)
                categories.append(
                    {
                        "category": name,
                        "department": section,
                        "subcategory": group,
                        "label": label,
                        "url": LEVI_SITE_BASE + url,
                    }
                )
    return categories


LEVI_CATEGORIES = _flatten_categories()
