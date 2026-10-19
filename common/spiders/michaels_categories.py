"""Michaels (michaels.com) category inventory, derived from the category sitemap.

Source of truth: https://www.michaels.com/sitemap_MIK_category.xml

The sitemap is advertised in ``robots.txt`` and carries every PLP the storefront
can render, as an absolute ``<loc>`` URL of the form::

    https://www.michaels.com/shop/<department>/<subcategory>/[/<leaf>]

Verified 2026-10-18 through the repository's configured US residential proxy:
3,644 category URLs, all unique, nested under 34 top-level departments, up to
five levels deep.

Why the sitemap and not the header navigation: the PLP is a Next.js App Router
page whose React Server Component payload (``self.__next_f``) embeds the whole
taxonomy tree, but only for the branch being viewed -- the megamenu links to
departments the sitemap does not spell out as leaf paths, and several header
entries are campaign landing pages that hydrate zero products. The sitemap is
the only source that enumerates the complete set, so it is the single category
source this spider uses.

``MICHAELS_CATEGORIES`` is the grouped inventory the Airflow DAG schedules from:
``{department: {leaf: {url, subcategory}}}``, matching the
``BaseListingSpider`` category contract. The spider still parses the sitemap at
crawl time to resolve the target, so a taxonomy change is picked up by the next
crawl while the committed snapshot keeps the DAG's task graph reviewable.
"""

from __future__ import annotations

import re
from typing import Any

MICHAELS_SITE_BASE = "https://www.michaels.com"
MICHAELS_CATEGORY_SITEMAP_URL = f"{MICHAELS_SITE_BASE}/sitemap_MIK_category.xml"

_LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.IGNORECASE)

# The PLP always routes through /shop/; anything else in the category sitemap is
# not a product listing (e.g. a help or brand landing page).
_SHOP_PREFIX = "/shop/"


def category_path_parts(url: str) -> list[str]:
    """`.../shop/kids/art-supplies/art-storage` -> ``['kids', 'art-supplies', 'art-storage']``.

    Strips the scheme/host and every other prefix segment so the caller gets the
    taxonomy path itself. Returns ``[]`` for a non-``/shop/`` URL.
    """
    path = (url or "").split("#", 1)[0].split("?", 1)[0].strip()
    marker = "michaels.com"
    if marker in path:
        path = path.split(marker, 1)[-1]
    segments = [segment for segment in path.split("/") if segment]
    if not segments or segments[0] != "shop":
        return []
    return segments[1:]


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def parse_category_sitemap(payload: str | bytes) -> list[dict[str, str]]:
    """Parse the category sitemap into ``BaseListingSpider.categories`` entries.

    Each entry is ``{"category", "department", "subcategory", "url"}``. The
    ``category`` value is the leaf slug, or ``<department>-<leaf>`` when that leaf
    slug is already taken by a different department -- 648 of the 3,611 leaves
    repeat (``decor``, ``pencils``, ``lanterns``, ...), so keying on the bare leaf
    alone would silently collapse two departments into one.
    """
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", "replace")

    paths: list[list[str]] = []
    seen_urls: set[str] = set()
    for match in _LOC_RE.finditer(payload or ""):
        url = match.group(1).strip()
        if url in seen_urls:
            continue
        parts = category_path_parts(url)
        if not parts:
            continue
        seen_urls.add(url)
        paths.append(parts)

    leaf_counts: dict[str, int] = {}
    for parts in paths:
        leaf = parts[-1]
        leaf_counts[leaf] = leaf_counts.get(leaf, 0) + 1

    categories: list[dict[str, str]] = []
    used: set[str] = set()
    for parts in paths:
        department, leaf = parts[0], parts[-1]
        name = leaf if leaf_counts[leaf] == 1 else f"{_slug(department)}-{leaf}"
        # Belt and braces: a department can itself repeat a leaf ("food/crafts"
        # under two roots), so keep disambiguating until the name is free.
        candidate, suffix = name, 2
        while candidate in used:
            candidate = f"{name}-{suffix}"
            suffix += 1
        used.add(candidate)
        url = "/".join([MICHAELS_SITE_BASE, _SHOP_PREFIX.strip("/"), *parts]) + "/"
        categories.append(
            {
                "category": candidate,
                "department": department,
                "subcategory": "/".join(parts[1:]) or department,
                "url": url,
            }
        )
    return categories


MICHAELS_CATEGORIES: dict[str, dict[str, dict[str, str]]] = {
    "apparel-crafts": {
        "adult": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/adult/",
            "subcategory": "t-shirts-clothing/adult",
        },
        "adult-costume-accessories": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories",
        },
        "adult-costume-diy": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/adult-costume-diy/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/adult-costume-diy",
        },
        "adult-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costumes/",
            "subcategory": "seasonal-apparel-costumes/adult-costumes",
        },
        "animal-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/animal-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/animal-halloween-costumes",
        },
        "apparel-accessories": {
            "url": "https://www.michaels.com/shop/apparel-crafts/apparel-accessories/",
            "subcategory": "apparel-accessories",
        },
        "apparel-crafts": {
            "url": "https://www.michaels.com/shop/apparel-crafts/",
            "subcategory": "apparel-crafts",
        },
        "apparel-crafts-aprons": {
            "url": "https://www.michaels.com/shop/apparel-crafts/apparel-accessories/aprons/",
            "subcategory": "apparel-accessories/aprons",
        },
        "apparel-crafts-bags-totes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/bags-totes/",
            "subcategory": "bags-totes",
        },
        "apparel-crafts-embellishments": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/adult-costume-diy/embellishments/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/adult-costume-diy/embellishments",
        },
        "apparel-crafts-fabric-paint": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-paint/",
            "subcategory": "fabric-paint",
        },
        "apparel-crafts-face-body-paint": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/kids-costume-diy/face-body-paint/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/kids-costume-diy/face-body-paint",
        },
        "apparel-crafts-face-body-paint-2": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/adult-costume-diy/face-body-paint/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/adult-costume-diy/face-body-paint",
        },
        "apparel-crafts-face-body-paint-3": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/face-body-paint/",
            "subcategory": "seasonal-apparel-costumes/face-body-paint",
        },
        "apparel-crafts-jewelry": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/jewelry/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/jewelry",
        },
        "apparel-crafts-leather-paint": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-paint/leather-paint/",
            "subcategory": "fabric-paint/leather-paint",
        },
        "apparel-crafts-letters-numbers": {
            "url": "https://www.michaels.com/shop/apparel-crafts/iron-ons-appliques/letters-numbers/",
            "subcategory": "iron-ons-appliques/letters-numbers",
        },
        "apparel-crafts-masks": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/masks/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/masks",
        },
        "apparel-crafts-paint": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/kids-costume-diy/paint/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/kids-costume-diy/paint",
        },
        "apparel-crafts-paint-2": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/adult-costume-diy/paint/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/adult-costume-diy/paint",
        },
        "apparel-crafts-paint-3": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/face-body-paint/paint/",
            "subcategory": "seasonal-apparel-costumes/face-body-paint/paint",
        },
        "apparel-crafts-t-shirts": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/adult-costume-diy/t-shirts/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/adult-costume-diy/t-shirts",
        },
        "apparel-crafts-t-shirts-2": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/kids-costume-diy/t-shirts/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/kids-costume-diy/t-shirts",
        },
        "apparel-crafts-tie-dye-fabric-dye": {
            "url": "https://www.michaels.com/shop/apparel-crafts/tie-dye-fabric-dye/",
            "subcategory": "tie-dye-fabric-dye",
        },
        "apparel-crafts-tools": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/face-body-paint/tools/",
            "subcategory": "seasonal-apparel-costumes/face-body-paint/tools",
        },
        "apparel-crafts-transfer-paper": {
            "url": "https://www.michaels.com/shop/apparel-crafts/iron-ons-appliques/transfer-paper/",
            "subcategory": "iron-ons-appliques/transfer-paper",
        },
        "apparel-crafts-vinyl": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/kids-costume-diy/vinyl/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/kids-costume-diy/vinyl",
        },
        "apparel-crafts-vinyl-2": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/adult-costume-diy/vinyl/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/adult-costume-diy/vinyl",
        },
        "appliques-patches": {
            "url": "https://www.michaels.com/shop/apparel-crafts/iron-ons-appliques/appliques-patches/",
            "subcategory": "iron-ons-appliques/appliques-patches",
        },
        "athletic": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/athletic/",
            "subcategory": "t-shirts-clothing/athletic",
        },
        "baby-toddler": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/baby-toddler/",
            "subcategory": "t-shirts-clothing/baby-toddler",
        },
        "baby-toddler-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/baby-toddler-costumes/",
            "subcategory": "seasonal-apparel-costumes/baby-toddler-costumes",
        },
        "bandanas": {
            "url": "https://www.michaels.com/shop/apparel-crafts/apparel-accessories/bandanas/",
            "subcategory": "apparel-accessories/bandanas",
        },
        "belts": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/belts/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/belts",
        },
        "bottoms": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/bottoms/",
            "subcategory": "t-shirts-clothing/bottoms",
        },
        "brush-on-paints": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-paint/brush-on-paints/",
            "subcategory": "fabric-paint/brush-on-paints",
        },
        "capes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/capes/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/capes",
        },
        "career-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/career-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/career-halloween-costumes",
        },
        "comfort-colors": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/comfort-colors/",
            "subcategory": "t-shirts-clothing/comfort-colors",
        },
        "costume-making-supplies": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/costume-making-supplies/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/costume-making-supplies",
        },
        "couples-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/couples-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/couples-halloween-costumes",
        },
        "dimensional-paints": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-paint/dimensional-paints/",
            "subcategory": "fabric-paint/dimensional-paints",
        },
        "diy-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes",
        },
        "fabric-adhesives": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-adhesives/",
            "subcategory": "fabric-adhesives",
        },
        "fabric-dye-supplies": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-paint/fabric-dye-supplies/",
            "subcategory": "fabric-paint/fabric-dye-supplies",
        },
        "fabric-markers": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-markers/",
            "subcategory": "fabric-markers",
        },
        "fabric-spray-paint": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-paint/fabric-spray-paint/",
            "subcategory": "fabric-paint/fabric-spray-paint",
        },
        "family-group-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/family-group-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/family-group-halloween-costumes",
        },
        "funny-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/funny-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/funny-halloween-costumes",
        },
        "gildan": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/gildan/",
            "subcategory": "t-shirts-clothing/gildan",
        },
        "glitter-crystals": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/face-body-paint/glitter-crystals/",
            "subcategory": "seasonal-apparel-costumes/face-body-paint/glitter-crystals",
        },
        "gloves": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/gloves/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/gloves",
        },
        "handheld-accessories": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/handheld-accessories/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/handheld-accessories",
        },
        "hats": {
            "url": "https://www.michaels.com/shop/apparel-crafts/apparel-accessories/hats/",
            "subcategory": "apparel-accessories/hats",
        },
        "hats-headpieces": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/hats-headpieces/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/hats-headpieces",
        },
        "iron-on-transfers": {
            "url": "https://www.michaels.com/shop/apparel-crafts/iron-ons-appliques/iron-on-transfers/",
            "subcategory": "iron-ons-appliques/iron-on-transfers",
        },
        "iron-ons-appliques": {
            "url": "https://www.michaels.com/shop/apparel-crafts/iron-ons-appliques/",
            "subcategory": "iron-ons-appliques",
        },
        "kids-costume-diy": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/diy-costumes/kids-costume-diy/",
            "subcategory": "seasonal-apparel-costumes/diy-costumes/kids-costume-diy",
        },
        "kids-costumes-accessories": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/kids-costumes-accessories/",
            "subcategory": "seasonal-apparel-costumes/kids-costumes-accessories",
        },
        "magical-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/magical-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/magical-halloween-costumes",
        },
        "movie-celebrity-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/movie-celebrity-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/movie-celebrity-halloween-costumes",
        },
        "outerwear": {
            "url": "https://www.michaels.com/shop/apparel-crafts/outerwear/",
            "subcategory": "outerwear",
        },
        "pet": {
            "url": "https://www.michaels.com/shop/apparel-crafts/apparel-accessories/pet/",
            "subcategory": "apparel-accessories/pet",
        },
        "rit-dye": {
            "url": "https://www.michaels.com/shop/apparel-crafts/tie-dye-fabric-dye/rit-dye/",
            "subcategory": "tie-dye-fabric-dye/rit-dye",
        },
        "scary-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/scary-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/scary-halloween-costumes",
        },
        "seasonal-apparel-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/",
            "subcategory": "seasonal-apparel-costumes",
        },
        "shoes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/shoes/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/shoes",
        },
        "shop-by-theme": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme",
        },
        "stencils-forms": {
            "url": "https://www.michaels.com/shop/apparel-crafts/fabric-paint/stencils-forms/",
            "subcategory": "fabric-paint/stencils-forms",
        },
        "t-shirts-clothing": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/",
            "subcategory": "t-shirts-clothing",
        },
        "temporary-tattoos": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/face-body-paint/temporary-tattoos/",
            "subcategory": "seasonal-apparel-costumes/face-body-paint/temporary-tattoos",
        },
        "throwback-halloween-costumes": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/shop-by-theme/throwback-halloween-costumes/",
            "subcategory": "seasonal-apparel-costumes/shop-by-theme/throwback-halloween-costumes",
        },
        "tie-dye-kits": {
            "url": "https://www.michaels.com/shop/apparel-crafts/tie-dye-fabric-dye/tie-dye-kits/",
            "subcategory": "tie-dye-fabric-dye/tie-dye-kits",
        },
        "tutus": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/tutus/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/tutus",
        },
        "wigs": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/wigs/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/wigs",
        },
        "wings": {
            "url": "https://www.michaels.com/shop/apparel-crafts/seasonal-apparel-costumes/adult-costume-accessories/wings/",
            "subcategory": "seasonal-apparel-costumes/adult-costume-accessories/wings",
        },
        "youth": {
            "url": "https://www.michaels.com/shop/apparel-crafts/t-shirts-clothing/youth/",
            "subcategory": "t-shirts-clothing/youth",
        },
    },
    "art-supplies": {
        "acetate": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drafting/acetate/",
            "subcategory": "drawing-supplies/drafting/acetate",
        },
        "acrylic-gouache": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/acrylic-gouache/",
            "subcategory": "paint-painting-supplies/liquitex/acrylic-gouache",
        },
        "acrylic-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint/acrylic-ink/",
            "subcategory": "paint-painting-supplies/fine-art-paint/acrylic-paint/acrylic-ink",
        },
        "acrylic-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/acrylic-markers/",
            "subcategory": "drawing-supplies/markers/acrylic-markers",
        },
        "acrylic-mediums": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/acrylic-mediums/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/acrylic-mediums",
        },
        "acrylic-paint-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint/acrylic-paint-sets/",
            "subcategory": "paint-painting-supplies/fine-art-paint/acrylic-paint/acrylic-paint-sets",
        },
        "adult-coloring-books": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/books/adult-coloring-books/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/books/adult-coloring-books",
        },
        "airbrushing": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/airbrushing/",
            "subcategory": "paint-painting-supplies/airbrushing",
        },
        "alcohol-based": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pens/alcohol-based/",
            "subcategory": "paint-painting-supplies/paint-pens/alcohol-based",
        },
        "alcohol-based-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/alcohol-based-markers/",
            "subcategory": "drawing-supplies/markers/alcohol-based-markers",
        },
        "art-activity-kits": {
            "url": "https://www.michaels.com/shop/art-supplies/art-gift-sets/art-activity-kits/",
            "subcategory": "art-gift-sets/art-activity-kits",
        },
        "art-illustration-boards": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/art-illustration-boards/",
            "subcategory": "paper-drawing-pads/art-illustration-boards",
        },
        "art-painting-kits": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/shop-by-skill-level/art-painting-kits/",
            "subcategory": "paint-painting-supplies/shop-by-skill-level/art-painting-kits",
        },
        "art-supplies-acrylic": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/acrylic/",
            "subcategory": "paint-painting-supplies/paint-brushes/acrylic",
        },
        "art-supplies-acrylic-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/brush-sets/acrylic/",
            "subcategory": "paint-painting-supplies/paint-brushes/brush-sets/acrylic",
        },
        "art-supplies-acrylic-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint/acrylic-paint",
        },
        "art-supplies-acrylic-paint-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pouring/acrylic-paint/",
            "subcategory": "paint-painting-supplies/paint-pouring/acrylic-paint",
        },
        "art-supplies-adhesives": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/adhesives/",
            "subcategory": "paint-painting-supplies/painting-accessories/adhesives",
        },
        "art-supplies-alcohol-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/alcohol-ink/",
            "subcategory": "drawing-supplies/ink-calligraphy/alcohol-ink",
        },
        "art-supplies-art-desks-easels": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/",
            "subcategory": "art-desks-easels",
        },
        "art-supplies-art-desks-easels-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/art-desks-easels/",
            "subcategory": "paint-painting-supplies/art-desks-easels",
        },
        "art-supplies-art-gift-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/art-gift-sets/",
            "subcategory": "art-gift-sets",
        },
        "art-supplies-art-storage": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/art-storage/",
            "subcategory": "storage-studio-supplies/art-storage",
        },
        "art-supplies-art-supplies": {
            "url": "https://www.michaels.com/shop/art-supplies/",
            "subcategory": "art-supplies",
        },
        "art-supplies-art-technology": {
            "url": "https://www.michaels.com/shop/art-supplies/art-technology/",
            "subcategory": "art-technology",
        },
        "art-supplies-art-technology-2": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/art-technology/",
            "subcategory": "storage-studio-supplies/art-technology",
        },
        "art-supplies-artist-canvas": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/artist-canvas/",
            "subcategory": "paint-painting-supplies/artist-canvas",
        },
        "art-supplies-artist-canvas-2": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/",
            "subcategory": "artist-canvas",
        },
        "art-supplies-books": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/books/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/books",
        },
        "art-supplies-brushes": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/shop-by-skill-level/brushes/",
            "subcategory": "paint-painting-supplies/shop-by-skill-level/brushes",
        },
        "art-supplies-brushes-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/brushes/",
            "subcategory": "paint-painting-supplies/liquitex/brushes",
        },
        "art-supplies-canvas-frames": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-tools-accessories/canvas-frames/",
            "subcategory": "artist-canvas/canvas-tools-accessories/canvas-frames",
        },
        "art-supplies-canvas-pads-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/canvas-pads-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/canvas-pads-paper",
        },
        "art-supplies-canvas-pads-paper-2": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-pads-paper/",
            "subcategory": "artist-canvas/canvas-pads-paper",
        },
        "art-supplies-canvas-painting-kits": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-painting-kits/",
            "subcategory": "artist-canvas/canvas-painting-kits",
        },
        "art-supplies-colored-pencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pencils/colored-pencils/",
            "subcategory": "drawing-supplies/pencils/colored-pencils",
        },
        "art-supplies-cutting-tools": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/printmaking-tools/cutting-tools/",
            "subcategory": "printmaking/printmaking-tools/cutting-tools",
        },
        "art-supplies-cutting-tools-2": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/cutting-tools/",
            "subcategory": "storage-studio-supplies/cutting-tools",
        },
        "art-supplies-desks": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/desks/",
            "subcategory": "art-desks-easels/desks",
        },
        "art-supplies-drawing-supplies": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/",
            "subcategory": "drawing-supplies",
        },
        "art-supplies-erasers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/erasers/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/erasers",
        },
        "art-supplies-fluid-acrylics": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/fluid-acrylics/",
            "subcategory": "paint-painting-supplies/golden/fluid-acrylics",
        },
        "art-supplies-fluid-acrylics-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint/fluid-acrylics/",
            "subcategory": "paint-painting-supplies/fine-art-paint/acrylic-paint/fluid-acrylics",
        },
        "art-supplies-heavy-body-acrylics": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint/heavy-body-acrylics/",
            "subcategory": "paint-painting-supplies/fine-art-paint/acrylic-paint/heavy-body-acrylics",
        },
        "art-supplies-heavy-body-acrylics-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/heavy-body-acrylics/",
            "subcategory": "paint-painting-supplies/golden/heavy-body-acrylics",
        },
        "art-supplies-highlighters": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/highlighters/",
            "subcategory": "drawing-supplies/markers/highlighters",
        },
        "art-supplies-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/ink/",
            "subcategory": "paint-painting-supplies/liquitex/ink",
        },
        "art-supplies-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/",
            "subcategory": "paper-drawing-pads/journals",
        },
        "art-supplies-lamps-lighting": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/lamps-lighting/",
            "subcategory": "storage-studio-supplies/lamps-lighting",
        },
        "art-supplies-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/",
            "subcategory": "drawing-supplies/markers",
        },
        "art-supplies-measuring-tools": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drafting/measuring-tools/",
            "subcategory": "drawing-supplies/drafting/measuring-tools",
        },
        "art-supplies-mediums": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/shop-by-skill-level/mediums/",
            "subcategory": "paint-painting-supplies/shop-by-skill-level/mediums",
        },
        "art-supplies-mediums-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/mediums/",
            "subcategory": "paint-painting-supplies/golden/mediums",
        },
        "art-supplies-mediums-3": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/mediums/",
            "subcategory": "paint-painting-supplies/liquitex/mediums",
        },
        "art-supplies-multi-purpose": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/multi-purpose/",
            "subcategory": "paint-painting-supplies/paint-brushes/multi-purpose",
        },
        "art-supplies-multi-purpose-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/brush-sets/multi-purpose/",
            "subcategory": "paint-painting-supplies/paint-brushes/brush-sets/multi-purpose",
        },
        "art-supplies-oil": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/oil/",
            "subcategory": "paint-painting-supplies/paint-brushes/oil",
        },
        "art-supplies-oil-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/brush-sets/oil/",
            "subcategory": "paint-painting-supplies/paint-brushes/brush-sets/oil",
        },
        "art-supplies-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/shop-by-skill-level/paint/",
            "subcategory": "paint-painting-supplies/shop-by-skill-level/paint",
        },
        "art-supplies-paint-by-number": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-by-number/",
            "subcategory": "paint-painting-supplies/paint-by-number",
        },
        "art-supplies-paint-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/paint-markers/",
            "subcategory": "paint-painting-supplies/liquitex/paint-markers",
        },
        "art-supplies-paint-markers-2": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/paint-markers/",
            "subcategory": "drawing-supplies/markers/paint-markers",
        },
        "art-supplies-paint-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pens/",
            "subcategory": "paint-painting-supplies/paint-pens",
        },
        "art-supplies-paint-pouring": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pouring/",
            "subcategory": "paint-painting-supplies/paint-pouring",
        },
        "art-supplies-painting-accessories": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/",
            "subcategory": "paint-painting-supplies/painting-accessories",
        },
        "art-supplies-paper-pads": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/",
            "subcategory": "paper-drawing-pads/paper-pads",
        },
        "art-supplies-paper-rolls": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-rolls/",
            "subcategory": "paper-drawing-pads/paper-rolls",
        },
        "art-supplies-pastels": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pastels/",
            "subcategory": "drawing-supplies/pastels",
        },
        "art-supplies-pencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pencils/",
            "subcategory": "drawing-supplies/pencils",
        },
        "art-supplies-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/",
            "subcategory": "drawing-supplies/pens",
        },
        "art-supplies-portfolios": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/portfolios/",
            "subcategory": "storage-studio-supplies/portfolios",
        },
        "art-supplies-pouring-mediums": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pouring/pouring-mediums/",
            "subcategory": "paint-painting-supplies/paint-pouring/pouring-mediums",
        },
        "art-supplies-pouring-mediums-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/pouring-mediums/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/pouring-mediums",
        },
        "art-supplies-printmaking-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/printmaking-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/printmaking-paper",
        },
        "art-supplies-printmaking-paper-2": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/printmaking-paper/",
            "subcategory": "printmaking/printmaking-paper",
        },
        "art-supplies-rulers": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/rulers/",
            "subcategory": "storage-studio-supplies/rulers",
        },
        "art-supplies-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/sets/",
            "subcategory": "paint-painting-supplies/liquitex/sets",
        },
        "art-supplies-sets-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/sets/",
            "subcategory": "paint-painting-supplies/golden/sets",
        },
        "art-supplies-specialty": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/specialty/",
            "subcategory": "paint-painting-supplies/paint-brushes/specialty",
        },
        "art-supplies-sponges": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/sponges/",
            "subcategory": "paint-painting-supplies/painting-accessories/sponges",
        },
        "art-supplies-spray-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/spray-paint/",
            "subcategory": "paint-painting-supplies/liquitex/spray-paint",
        },
        "art-supplies-spray-paint-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/spray-paint/",
            "subcategory": "paint-painting-supplies/spray-paint",
        },
        "art-supplies-surfaces-supplies": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pouring/surfaces-supplies/",
            "subcategory": "paint-painting-supplies/paint-pouring/surfaces-supplies",
        },
        "art-supplies-tabletop-easels": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/easels/tabletop-easels/",
            "subcategory": "art-desks-easels/easels/tabletop-easels",
        },
        "art-supplies-transfer-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/transfer-paper/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/transfer-paper",
        },
        "art-supplies-watercolor": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/brush-sets/watercolor/",
            "subcategory": "paint-painting-supplies/paint-brushes/brush-sets/watercolor",
        },
        "art-supplies-watercolor-2": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/watercolor/",
            "subcategory": "paint-painting-supplies/paint-brushes/watercolor",
        },
        "art-supplies-wood-hardboard-panels": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/wood-hardboard-panels/",
            "subcategory": "artist-canvas/wood-hardboard-panels",
        },
        "art-techniques": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/books/art-techniques/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/books/art-techniques",
        },
        "artist-palettes": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/artist-palettes/",
            "subcategory": "paint-painting-supplies/painting-accessories/artist-palettes",
        },
        "artist-photo-inkjet-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/artist-photo-inkjet-paper/",
            "subcategory": "paper-drawing-pads/artist-photo-inkjet-paper",
        },
        "artist-spray-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/spray-paint/artist-spray-paint/",
            "subcategory": "paint-painting-supplies/spray-paint/artist-spray-paint",
        },
        "artist-tiles-trading-cards": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/artist-tiles-trading-cards/",
            "subcategory": "paper-drawing-pads/artist-tiles-trading-cards",
        },
        "artists-loft": {
            "url": "https://www.michaels.com/shop/art-supplies/artists-loft/",
            "subcategory": "artists-loft",
        },
        "ballpoint-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/ballpoint-pens/",
            "subcategory": "drawing-supplies/pens/ballpoint-pens",
        },
        "basics": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/basics/",
            "subcategory": "paint-painting-supplies/liquitex/basics",
        },
        "blending-tools": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/blending-tools/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/blending-tools",
        },
        "blockprinting": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/blockprinting/",
            "subcategory": "printmaking/blockprinting",
        },
        "blockprinting-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/blockprinting/blockprinting-ink/",
            "subcategory": "printmaking/blockprinting/blockprinting-ink",
        },
        "blockprinting-kits": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/blockprinting/blockprinting-kits/",
            "subcategory": "printmaking/blockprinting/blockprinting-kits",
        },
        "blocks": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/blockprinting/blocks/",
            "subcategory": "printmaking/blockprinting/blocks",
        },
        "brayers-barens": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/printmaking-tools/brayers-barens/",
            "subcategory": "printmaking/printmaking-tools/brayers-barens",
        },
        "brush-cleaners": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/brush-cleaners/",
            "subcategory": "paint-painting-supplies/painting-accessories/brush-cleaners",
        },
        "brush-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/brush-markers/",
            "subcategory": "drawing-supplies/markers/brush-markers",
        },
        "brush-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/brush-pens/",
            "subcategory": "drawing-supplies/pens/brush-pens",
        },
        "brush-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/brush-sets/",
            "subcategory": "paint-painting-supplies/paint-brushes/brush-sets",
        },
        "calligraphy-brushes": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/calligraphy-brushes/",
            "subcategory": "drawing-supplies/ink-calligraphy/calligraphy-brushes",
        },
        "calligraphy-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/calligraphy-ink/",
            "subcategory": "drawing-supplies/ink-calligraphy/calligraphy-ink",
        },
        "calligraphy-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/calligraphy-markers/",
            "subcategory": "drawing-supplies/ink-calligraphy/calligraphy-markers",
        },
        "canvas-folds-rolls": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-folds-rolls/",
            "subcategory": "artist-canvas/canvas-folds-rolls",
        },
        "canvas-hanging-mounting": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-tools-accessories/canvas-hanging-mounting/",
            "subcategory": "artist-canvas/canvas-tools-accessories/canvas-hanging-mounting",
        },
        "canvas-panels": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-panels/",
            "subcategory": "artist-canvas/canvas-panels",
        },
        "canvas-surfaces": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/shop-by-skill-level/canvas-surfaces/",
            "subcategory": "paint-painting-supplies/shop-by-skill-level/canvas-surfaces",
        },
        "canvas-tools-accessories": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-tools-accessories/",
            "subcategory": "artist-canvas/canvas-tools-accessories",
        },
        "charcoal": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/charcoal/",
            "subcategory": "drawing-supplies/charcoal",
        },
        "classic-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/classic-journals/",
            "subcategory": "paper-drawing-pads/journals/classic-journals",
        },
        "color-by-numbers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/color-by-numbers/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/color-by-numbers",
        },
        "color-guides": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/color-guides/",
            "subcategory": "paint-painting-supplies/painting-accessories/color-guides",
        },
        "comic-manga-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/comic-manga-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/comic-manga-paper",
        },
        "cork-dry-erase-boards": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/cork-dry-erase-boards/",
            "subcategory": "storage-studio-supplies/cork-dry-erase-boards",
        },
        "craft-spray-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/spray-paint/craft-spray-paint/",
            "subcategory": "paint-painting-supplies/spray-paint/craft-spray-paint",
        },
        "cutting-mats-accessories": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/cutting-mats-accessories/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/cutting-mats-accessories",
        },
        "cyanotype-solar-printing": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/cyanotype-solar-printing/",
            "subcategory": "printmaking/cyanotype-solar-printing",
        },
        "dip-pens-accessories": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/dip-pens-accessories/",
            "subcategory": "drawing-supplies/ink-calligraphy/dip-pens-accessories",
        },
        "display-easels": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/easels/display-easels/",
            "subcategory": "art-desks-easels/easels/display-easels",
        },
        "dot-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/dot-journals/",
            "subcategory": "paper-drawing-pads/journals/dot-journals",
        },
        "drafting": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drafting/",
            "subcategory": "drawing-supplies/drafting",
        },
        "drafting-tapes": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drafting/drafting-tapes/",
            "subcategory": "drawing-supplies/drafting/drafting-tapes",
        },
        "drafting-templates-stencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drafting/drafting-templates-stencils/",
            "subcategory": "drawing-supplies/drafting/drafting-templates-stencils",
        },
        "drawing-fixatives": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/drawing-fixatives/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/drawing-fixatives",
        },
        "drawing-gift-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/art-gift-sets/drawing-gift-sets/",
            "subcategory": "art-gift-sets/drawing-gift-sets",
        },
        "drawing-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/drawing-ink/",
            "subcategory": "drawing-supplies/ink-calligraphy/drawing-ink",
        },
        "drawing-sketching-boards": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/drawing-sketching-boards/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/drawing-sketching-boards",
        },
        "drawing-tools-accessories": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/",
            "subcategory": "drawing-supplies/drawing-tools-accessories",
        },
        "droppers-syringes-nozzles": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/droppers-syringes-nozzles/",
            "subcategory": "paint-painting-supplies/painting-accessories/droppers-syringes-nozzles",
        },
        "dual-tip-art-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/dual-tip-art-markers/",
            "subcategory": "drawing-supplies/markers/dual-tip-art-markers",
        },
        "easels": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/easels/",
            "subcategory": "art-desks-easels/easels",
        },
        "empty-markers-nibs": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pens/empty-markers-nibs/",
            "subcategory": "paint-painting-supplies/paint-pens/empty-markers-nibs",
        },
        "encaustic-painting": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/specialty-painting/encaustic-painting/",
            "subcategory": "paint-painting-supplies/specialty-painting/encaustic-painting",
        },
        "etching": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/etching/",
            "subcategory": "printmaking/etching",
        },
        "fabric-screenprinting-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/screenprinting/fabric-screenprinting-ink/",
            "subcategory": "printmaking/screenprinting/fabric-screenprinting-ink",
        },
        "fashion-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/fashion-journals/",
            "subcategory": "paper-drawing-pads/journals/fashion-journals",
        },
        "fashion-sketchbooks": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/sketchbooks/fashion-sketchbooks/",
            "subcategory": "paper-drawing-pads/sketchbooks/fashion-sketchbooks",
        },
        "felt-tip-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/felt-tip-pens/",
            "subcategory": "drawing-supplies/pens/felt-tip-pens",
        },
        "fine-art-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint",
        },
        "fineliner-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/fineliner-pens/",
            "subcategory": "drawing-supplies/pens/fineliner-pens",
        },
        "fountain-cartridge-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/fountain-cartridge-pens/",
            "subcategory": "drawing-supplies/ink-calligraphy/fountain-cartridge-pens",
        },
        "fountain-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/fountain-pens/",
            "subcategory": "drawing-supplies/pens/fountain-pens",
        },
        "gel-pens": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/gel-pens/",
            "subcategory": "drawing-supplies/pens/gel-pens",
        },
        "general-purpose-spray-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/spray-paint/general-purpose-spray-paint/",
            "subcategory": "paint-painting-supplies/spray-paint/general-purpose-spray-paint",
        },
        "golden": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/",
            "subcategory": "paint-painting-supplies/golden",
        },
        "gouache": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/gouache/",
            "subcategory": "paint-painting-supplies/fine-art-paint/gouache",
        },
        "graphite-drawing-pencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pencils/graphite-drawing-pencils/",
            "subcategory": "drawing-supplies/pencils/graphite-drawing-pencils",
        },
        "grid-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/grid-journals/",
            "subcategory": "paper-drawing-pads/journals/grid-journals",
        },
        "grid-layout-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drafting/grid-layout-paper/",
            "subcategory": "drawing-supplies/drafting/grid-layout-paper",
        },
        "hand-lettering-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/hand-lettering-sets/",
            "subcategory": "drawing-supplies/ink-calligraphy/hand-lettering-sets",
        },
        "hard-cover-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/hard-cover-journals/",
            "subcategory": "paper-drawing-pads/journals/hard-cover-journals",
        },
        "hardbound-sketchbooks": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/sketchbooks/hardbound-sketchbooks/",
            "subcategory": "paper-drawing-pads/sketchbooks/hardbound-sketchbooks",
        },
        "heavy-body": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/heavy-body/",
            "subcategory": "paint-painting-supplies/liquitex/heavy-body",
        },
        "india-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/india-ink/",
            "subcategory": "drawing-supplies/ink-calligraphy/india-ink",
        },
        "ink-calligraphy": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/",
            "subcategory": "drawing-supplies/ink-calligraphy",
        },
        "ink-modifiers": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/printmaking-tools/ink-modifiers/",
            "subcategory": "printmaking/printmaking-tools/ink-modifiers",
        },
        "lined-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/lined-journals/",
            "subcategory": "paper-drawing-pads/journals/lined-journals",
        },
        "liquid-watercolor": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/watercolor-paint/liquid-watercolor/",
            "subcategory": "paint-painting-supplies/fine-art-paint/watercolor-paint/liquid-watercolor",
        },
        "liquitex": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/liquitex/",
            "subcategory": "paint-painting-supplies/liquitex",
        },
        "manikins": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/manikins/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/manikins",
        },
        "marker-accessories-refills": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/marker-accessories-refills/",
            "subcategory": "drawing-supplies/markers/marker-accessories-refills",
        },
        "masking-fluids-frisket": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/masking-fluids-frisket/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/masking-fluids-frisket",
        },
        "matte-acrylics": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint/matte-acrylics/",
            "subcategory": "paint-painting-supplies/fine-art-paint/acrylic-paint/matte-acrylics",
        },
        "mechanical-pencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pencils/mechanical-pencils/",
            "subcategory": "drawing-supplies/pencils/mechanical-pencils",
        },
        "mediums-varnishes": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/",
            "subcategory": "paint-painting-supplies/mediums-varnishes",
        },
        "mini-canvas": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/mini-canvas/",
            "subcategory": "artist-canvas/mini-canvas",
        },
        "mixed-media-gift-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/art-gift-sets/mixed-media-gift-sets/",
            "subcategory": "art-gift-sets/mixed-media-gift-sets",
        },
        "mixed-media-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/mixed-media-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/mixed-media-paper",
        },
        "newsprint-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/newsprint-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/newsprint-paper",
        },
        "oil-based": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pens/oil-based/",
            "subcategory": "paint-painting-supplies/paint-pens/oil-based",
        },
        "oil-mediums": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/oil-mediums/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/oil-mediums",
        },
        "oil-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/oil-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint/oil-paint",
        },
        "oil-paint-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/oil-paint/oil-paint-sets/",
            "subcategory": "paint-painting-supplies/fine-art-paint/oil-paint/oil-paint-sets",
        },
        "oil-painting-solvents": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/oil-painting-solvents/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/oil-painting-solvents",
        },
        "oil-painting-sticks": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/oil-paint/oil-painting-sticks/",
            "subcategory": "paint-painting-supplies/fine-art-paint/oil-paint/oil-painting-sticks",
        },
        "oil-pastels": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pastels/oil-pastels/",
            "subcategory": "drawing-supplies/pastels/oil-pastels",
        },
        "open-acrylics": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/open-acrylics/",
            "subcategory": "paint-painting-supplies/golden/open-acrylics",
        },
        "open-stock-acrylic-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/acrylic-paint/open-stock-acrylic-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint/acrylic-paint/open-stock-acrylic-paint",
        },
        "open-stock-oil-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/oil-paint/open-stock-oil-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint/oil-paint/open-stock-oil-paint",
        },
        "open-stock-watercolor-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/watercolor-paint/open-stock-watercolor-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint/watercolor-paint/open-stock-watercolor-paint",
        },
        "paint-brushes": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-brushes/",
            "subcategory": "paint-painting-supplies/paint-brushes",
        },
        "paint-by-numbers": {
            "url": "https://www.michaels.com/shop/art-supplies/art-gift-sets/paint-by-numbers/",
            "subcategory": "art-gift-sets/paint-by-numbers",
        },
        "paint-marbling": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/specialty-painting/paint-marbling/",
            "subcategory": "paint-painting-supplies/specialty-painting/paint-marbling",
        },
        "paint-painting-supplies": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/",
            "subcategory": "paint-painting-supplies",
        },
        "paint-pouring-kits": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pouring/paint-pouring-kits/",
            "subcategory": "paint-painting-supplies/paint-pouring/paint-pouring-kits",
        },
        "painting-gift-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/art-gift-sets/painting-gift-sets/",
            "subcategory": "art-gift-sets/painting-gift-sets",
        },
        "palette-knives": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/palette-knives/",
            "subcategory": "paint-painting-supplies/painting-accessories/palette-knives",
        },
        "paper-drawing-pads": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/",
            "subcategory": "paper-drawing-pads",
        },
        "pastel-pencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pastels/pastel-pencils/",
            "subcategory": "drawing-supplies/pastels/pastel-pencils",
        },
        "pastel-tools-accessories": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pastels/pastel-tools-accessories/",
            "subcategory": "drawing-supplies/pastels/pastel-tools-accessories",
        },
        "pen-accessories-refills": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pens/pen-accessories-refills/",
            "subcategory": "drawing-supplies/pens/pen-accessories-refills",
        },
        "pencil-marker-cases": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/pencil-marker-cases/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/pencil-marker-cases",
        },
        "permanent-markers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/markers/permanent-markers/",
            "subcategory": "drawing-supplies/markers/permanent-markers",
        },
        "pigment-powders": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/pigment-powders/",
            "subcategory": "drawing-supplies/ink-calligraphy/pigment-powders",
        },
        "portable-outdoor-easels": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/easels/portable-outdoor-easels/",
            "subcategory": "art-desks-easels/easels/portable-outdoor-easels",
        },
        "premium-journals": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/journals/premium-journals/",
            "subcategory": "paper-drawing-pads/journals/premium-journals",
        },
        "primers-gessoes": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/primers-gessoes/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/primers-gessoes",
        },
        "print-racks": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/printmaking-tools/print-racks/",
            "subcategory": "printmaking/printmaking-tools/print-racks",
        },
        "printmaking": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/",
            "subcategory": "printmaking",
        },
        "printmaking-tools": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/printmaking-tools/",
            "subcategory": "printmaking/printmaking-tools",
        },
        "projectors-lightpads-tracers": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/projectors-lightpads-tracers/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/projectors-lightpads-tracers",
        },
        "ready-mixed-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pouring/ready-mixed-paint/",
            "subcategory": "paint-painting-supplies/paint-pouring/ready-mixed-paint",
        },
        "safety-clean-up": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/safety-clean-up/",
            "subcategory": "storage-studio-supplies/safety-clean-up",
        },
        "scratchboard": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/scratchboard/",
            "subcategory": "printmaking/scratchboard",
        },
        "screenprinting": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/screenprinting/",
            "subcategory": "printmaking/screenprinting",
        },
        "screenprinting-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/screenprinting/screenprinting-ink/",
            "subcategory": "printmaking/screenprinting/screenprinting-ink",
        },
        "screenprinting-kits": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/screenprinting/screenprinting-kits/",
            "subcategory": "printmaking/screenprinting/screenprinting-kits",
        },
        "screens-frames": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/screenprinting/screens-frames/",
            "subcategory": "printmaking/screenprinting/screens-frames",
        },
        "sharpeners": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drawing-tools-accessories/sharpeners/",
            "subcategory": "drawing-supplies/drawing-tools-accessories/sharpeners",
        },
        "shop-by-skill-level": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/shop-by-skill-level/",
            "subcategory": "paint-painting-supplies/shop-by-skill-level",
        },
        "silk-painting": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/specialty-painting/silk-painting/",
            "subcategory": "paint-painting-supplies/specialty-painting/silk-painting",
        },
        "sketchbooks": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/sketchbooks/",
            "subcategory": "paper-drawing-pads/sketchbooks",
        },
        "soflat-acrylic": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/soflat-acrylic/",
            "subcategory": "paint-painting-supplies/golden/soflat-acrylic",
        },
        "soft-pastels": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pastels/soft-pastels/",
            "subcategory": "drawing-supplies/pastels/soft-pastels",
        },
        "softbound-sketchbooks": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/sketchbooks/softbound-sketchbooks/",
            "subcategory": "paper-drawing-pads/sketchbooks/softbound-sketchbooks",
        },
        "specialty-painting": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/specialty-painting/",
            "subcategory": "paint-painting-supplies/specialty-painting",
        },
        "spray-lacquers-sealers": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/spray-paint/spray-lacquers-sealers/",
            "subcategory": "paint-painting-supplies/spray-paint/spray-lacquers-sealers",
        },
        "spray-painting-accessories": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/spray-paint/spray-painting-accessories/",
            "subcategory": "paint-painting-supplies/spray-paint/spray-painting-accessories",
        },
        "squeegees": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/printmaking-tools/squeegees/",
            "subcategory": "printmaking/printmaking-tools/squeegees",
        },
        "stenciling": {
            "url": "https://www.michaels.com/shop/art-supplies/printmaking/screenprinting/stenciling/",
            "subcategory": "printmaking/screenprinting/stenciling",
        },
        "storage-containers": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/painting-accessories/storage-containers/",
            "subcategory": "paint-painting-supplies/painting-accessories/storage-containers",
        },
        "storage-studio-supplies": {
            "url": "https://www.michaels.com/shop/art-supplies/storage-studio-supplies/",
            "subcategory": "storage-studio-supplies",
        },
        "stretched-canvas": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/stretched-canvas/",
            "subcategory": "artist-canvas/stretched-canvas",
        },
        "stretcher-bars": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/canvas-tools-accessories/stretcher-bars/",
            "subcategory": "artist-canvas/canvas-tools-accessories/stretcher-bars",
        },
        "studio-easels": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/easels/studio-easels/",
            "subcategory": "art-desks-easels/easels/studio-easels",
        },
        "studio-furniture": {
            "url": "https://www.michaels.com/shop/art-supplies/art-desks-easels/studio-furniture/",
            "subcategory": "art-desks-easels/studio-furniture",
        },
        "sumi-ink": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/ink-calligraphy/sumi-ink/",
            "subcategory": "drawing-supplies/ink-calligraphy/sumi-ink",
        },
        "super-value-pack-canvas": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/super-value-pack-canvas/",
            "subcategory": "artist-canvas/super-value-pack-canvas",
        },
        "technical-pens-pencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/drafting/technical-pens-pencils/",
            "subcategory": "drawing-supplies/drafting/technical-pens-pencils",
        },
        "tracing-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/tracing-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/tracing-paper",
        },
        "value-pack-canvas": {
            "url": "https://www.michaels.com/shop/art-supplies/artist-canvas/value-pack-canvas/",
            "subcategory": "artist-canvas/value-pack-canvas",
        },
        "varnishes": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/golden/varnishes/",
            "subcategory": "paint-painting-supplies/golden/varnishes",
        },
        "varnishes-topcoats": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/varnishes-topcoats/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/varnishes-topcoats",
        },
        "water-based": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/paint-pens/water-based/",
            "subcategory": "paint-painting-supplies/paint-pens/water-based",
        },
        "water-mixable-oil-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/oil-paint/water-mixable-oil-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint/oil-paint/water-mixable-oil-paint",
        },
        "watercolor-dot-cards": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/watercolor-paint/watercolor-dot-cards/",
            "subcategory": "paint-painting-supplies/fine-art-paint/watercolor-paint/watercolor-dot-cards",
        },
        "watercolor-mediums": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/mediums-varnishes/watercolor-mediums/",
            "subcategory": "paint-painting-supplies/mediums-varnishes/watercolor-mediums",
        },
        "watercolor-paint": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/watercolor-paint/",
            "subcategory": "paint-painting-supplies/fine-art-paint/watercolor-paint",
        },
        "watercolor-pan-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/watercolor-paint/watercolor-pan-sets/",
            "subcategory": "paint-painting-supplies/fine-art-paint/watercolor-paint/watercolor-pan-sets",
        },
        "watercolor-pencils": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pencils/watercolor-pencils/",
            "subcategory": "drawing-supplies/pencils/watercolor-pencils",
        },
        "watercolor-tube-sets": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/fine-art-paint/watercolor-paint/watercolor-tube-sets/",
            "subcategory": "paint-painting-supplies/fine-art-paint/watercolor-paint/watercolor-tube-sets",
        },
        "wax-pastels-crayons": {
            "url": "https://www.michaels.com/shop/art-supplies/drawing-supplies/pastels/wax-pastels-crayons/",
            "subcategory": "drawing-supplies/pastels/wax-pastels-crayons",
        },
        "winsor-newton": {
            "url": "https://www.michaels.com/shop/art-supplies/paint-painting-supplies/winsor-newton/",
            "subcategory": "paint-painting-supplies/winsor-newton",
        },
        "wirebound-sketchbooks": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/sketchbooks/wirebound-sketchbooks/",
            "subcategory": "paper-drawing-pads/sketchbooks/wirebound-sketchbooks",
        },
        "writing-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/writing-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/writing-paper",
        },
        "xsketch-drawing-paper": {
            "url": "https://www.michaels.com/shop/art-supplies/paper-drawing-pads/paper-pads/xsketch-drawing-paper/",
            "subcategory": "paper-drawing-pads/paper-pads/xsketch-drawing-paper",
        },
    },
    "baking-kitchen": {
        "bag-tip-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/bags-tips/bag-tip-tools/",
            "subcategory": "decorating-tools/bags-tips/bag-tip-tools",
        },
        "bags-tips": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/bags-tips/",
            "subcategory": "decorating-tools/bags-tips",
        },
        "bakeware-cookware": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/",
            "subcategory": "bakeware-cookware",
        },
        "baking-cups": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/baking-cups/",
            "subcategory": "decorating-tools/baking-cups",
        },
        "baking-ingredients": {
            "url": "https://www.michaels.com/shop/baking-kitchen/baking-ingredients/",
            "subcategory": "baking-ingredients",
        },
        "baking-kitchen": {
            "url": "https://www.michaels.com/shop/baking-kitchen/",
            "subcategory": "baking-kitchen",
        },
        "baking-kitchen-cake-stands": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/cake-stands/",
            "subcategory": "packaging-display/cake-stands",
        },
        "baking-kitchen-candles": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/candles/",
            "subcategory": "decorations/candles",
        },
        "baking-kitchen-decorations": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/",
            "subcategory": "decorations",
        },
        "baking-kitchen-measuring-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/measuring-tools/",
            "subcategory": "kitchen-tools/measuring-tools",
        },
        "baking-kitchen-timers": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/timers/",
            "subcategory": "kitchen-tools/timers",
        },
        "basic-baking-pans": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/basic-baking-pans/",
            "subcategory": "bakeware-cookware/basic-baking-pans",
        },
        "cake-boards": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/cake-boards/",
            "subcategory": "packaging-display/cake-boards",
        },
        "cake-boxes": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/cake-boxes/",
            "subcategory": "packaging-display/cake-boxes",
        },
        "cake-cupcake-storage": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/cake-cupcake-storage/",
            "subcategory": "decorating-tools/cake-cupcake-storage",
        },
        "cake-cupcake-toppers": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/cake-cupcake-toppers/",
            "subcategory": "decorations/cake-cupcake-toppers",
        },
        "cake-decorating-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/cake-decorating-tools/",
            "subcategory": "decorating-tools/cake-decorating-tools",
        },
        "cake-mixes": {
            "url": "https://www.michaels.com/shop/baking-kitchen/baking-ingredients/cake-mixes/",
            "subcategory": "baking-ingredients/cake-mixes",
        },
        "candy-decorations": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/sprinkles-edible-decorations/candy-decorations/",
            "subcategory": "decorations/sprinkles-edible-decorations/candy-decorations",
        },
        "candy-making": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/",
            "subcategory": "candy-making",
        },
        "candy-making-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/candy-making-tools/",
            "subcategory": "candy-making/candy-making-tools",
        },
        "candy-melts": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/candy-melts/",
            "subcategory": "candy-making/candy-melts",
        },
        "candy-mixes": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/candy-mixes/",
            "subcategory": "candy-making/candy-mixes",
        },
        "chocolate-fountains": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/chocolate-fountains/",
            "subcategory": "candy-making/chocolate-fountains",
        },
        "colanders": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/colanders/",
            "subcategory": "kitchen-tools/colanders",
        },
        "cookie-cutters": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/cookie-cutters/",
            "subcategory": "decorating-tools/cookie-cutters",
        },
        "cookie-decorating-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/cookie-decorating-tools/",
            "subcategory": "decorating-tools/cookie-decorating-tools",
        },
        "cookie-mixes": {
            "url": "https://www.michaels.com/shop/baking-kitchen/baking-ingredients/cookie-mixes/",
            "subcategory": "baking-ingredients/cookie-mixes",
        },
        "cookie-sheets": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/cookie-sheets/",
            "subcategory": "bakeware-cookware/cookie-sheets",
        },
        "cookware-sets": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/cookware-sets/",
            "subcategory": "bakeware-cookware/cookware-sets",
        },
        "cupcake-boxes": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/cupcake-boxes/",
            "subcategory": "packaging-display/cupcake-boxes",
        },
        "cupcake-muffin-pans": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/cupcake-muffin-pans/",
            "subcategory": "bakeware-cookware/cupcake-muffin-pans",
        },
        "cupcake-stands": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/cupcake-stands/",
            "subcategory": "packaging-display/cupcake-stands",
        },
        "cutlery-knives": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/cutlery-knives/",
            "subcategory": "kitchen-tools/cutlery-knives",
        },
        "cutting-boards": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/cutting-boards/",
            "subcategory": "kitchen-tools/cutting-boards",
        },
        "decorating-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/",
            "subcategory": "decorating-tools",
        },
        "flavor-extracts-emulsions": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/flavor-extracts-emulsions/",
            "subcategory": "candy-making/flavor-extracts-emulsions",
        },
        "flavorings": {
            "url": "https://www.michaels.com/shop/baking-kitchen/baking-ingredients/flavorings/",
            "subcategory": "baking-ingredients/flavorings",
        },
        "fondant-gum-paste": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/fondant-gum-paste/",
            "subcategory": "decorations/fondant-gum-paste",
        },
        "fondant-molds-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/fondant-molds-tools/",
            "subcategory": "decorating-tools/fondant-molds-tools",
        },
        "food-coloring-dyes": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/food-coloring-dyes/",
            "subcategory": "decorations/food-coloring-dyes",
        },
        "food-markers": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/sprinkles-edible-decorations/food-markers/",
            "subcategory": "decorations/sprinkles-edible-decorations/food-markers",
        },
        "glitter-powders": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/sprinkles-edible-decorations/glitter-powders/",
            "subcategory": "decorations/sprinkles-edible-decorations/glitter-powders",
        },
        "icing": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/icing/",
            "subcategory": "decorations/icing",
        },
        "icing-decorations": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/sprinkles-edible-decorations/icing-decorations/",
            "subcategory": "decorations/sprinkles-edible-decorations/icing-decorations",
        },
        "icing-ingredients": {
            "url": "https://www.michaels.com/shop/baking-kitchen/baking-ingredients/icing-ingredients/",
            "subcategory": "baking-ingredients/icing-ingredients",
        },
        "kettles": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/kettles/",
            "subcategory": "bakeware-cookware/kettles",
        },
        "kitchen-gadgets": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/kitchen-gadgets/",
            "subcategory": "kitchen-tools/kitchen-gadgets",
        },
        "kitchen-storage-organization": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-storage-organization/",
            "subcategory": "kitchen-storage-organization",
        },
        "kitchen-tools": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/",
            "subcategory": "kitchen-tools",
        },
        "kitchen-utensils": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/kitchen-utensils/",
            "subcategory": "kitchen-tools/kitchen-utensils",
        },
        "mixing-bowls": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/mixing-bowls/",
            "subcategory": "kitchen-tools/mixing-bowls",
        },
        "molds": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/molds/",
            "subcategory": "candy-making/molds",
        },
        "other-packaging": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/other-packaging/",
            "subcategory": "packaging-display/other-packaging",
        },
        "ovenware": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/ovenware/",
            "subcategory": "bakeware-cookware/ovenware",
        },
        "packaging-accessories": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/packaging-accessories/",
            "subcategory": "packaging-display/packaging-accessories",
        },
        "packaging-display": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/",
            "subcategory": "packaging-display",
        },
        "pan-liners": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/pan-liners/",
            "subcategory": "kitchen-tools/pan-liners",
        },
        "pan-sets": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/pan-sets/",
            "subcategory": "bakeware-cookware/pan-sets",
        },
        "piping-bags": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/bags-tips/piping-bags/",
            "subcategory": "decorating-tools/bags-tips/piping-bags",
        },
        "piping-tips": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorating-tools/bags-tips/piping-tips/",
            "subcategory": "decorating-tools/bags-tips/piping-tips",
        },
        "pots-saucepans": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/pots-saucepans/",
            "subcategory": "bakeware-cookware/pots-saucepans",
        },
        "satin-ice": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/satin-ice/",
            "subcategory": "decorations/satin-ice",
        },
        "scales": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/scales/",
            "subcategory": "kitchen-tools/scales",
        },
        "skillets": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/skillets/",
            "subcategory": "bakeware-cookware/skillets",
        },
        "small-kitchen-appliances": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/small-kitchen-appliances/",
            "subcategory": "kitchen-tools/small-kitchen-appliances",
        },
        "specialty-baking-pans": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/specialty-baking-pans/",
            "subcategory": "bakeware-cookware/specialty-baking-pans",
        },
        "specialty-cookware": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/specialty-cookware/",
            "subcategory": "bakeware-cookware/specialty-cookware",
        },
        "springform-pans": {
            "url": "https://www.michaels.com/shop/baking-kitchen/bakeware-cookware/springform-pans/",
            "subcategory": "bakeware-cookware/springform-pans",
        },
        "sprinkles": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/sprinkles-edible-decorations/sprinkles/",
            "subcategory": "decorations/sprinkles-edible-decorations/sprinkles",
        },
        "sprinkles-edible-decorations": {
            "url": "https://www.michaels.com/shop/baking-kitchen/decorations/sprinkles-edible-decorations/",
            "subcategory": "decorations/sprinkles-edible-decorations",
        },
        "sticks": {
            "url": "https://www.michaels.com/shop/baking-kitchen/candy-making/sticks/",
            "subcategory": "candy-making/sticks",
        },
        "thermometers": {
            "url": "https://www.michaels.com/shop/baking-kitchen/kitchen-tools/thermometers/",
            "subcategory": "kitchen-tools/thermometers",
        },
        "treat-bags": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/treat-bags/",
            "subcategory": "packaging-display/treat-bags",
        },
        "treat-boxes": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/treat-boxes/",
            "subcategory": "packaging-display/treat-boxes",
        },
        "treat-tins": {
            "url": "https://www.michaels.com/shop/baking-kitchen/packaging-display/treat-tins/",
            "subcategory": "packaging-display/treat-tins",
        },
    },
    "beads-jewelry": {
        "acrylic-props": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/acrylic-props/",
            "subcategory": "display-packaging/acrylic-props",
        },
        "alphabet-numbers": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/charms/alphabet-numbers/",
            "subcategory": "charm-shop-pendants/charms/alphabet-numbers",
        },
        "alphabet-pony-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/alphabet-pony-beads/",
            "subcategory": "beads/crafting-beads/alphabet-pony-beads",
        },
        "austrian-crystal": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/austrian-crystal/",
            "subcategory": "gems-rhinestones/austrian-crystal",
        },
        "austrian-crystal-charms": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/austrian-crystal/austrian-crystal-charms/",
            "subcategory": "gems-rhinestones/austrian-crystal/austrian-crystal-charms",
        },
        "bails": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/bails/",
            "subcategory": "jewelry-findings/bails",
        },
        "bead-boards": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/bead-boards/",
            "subcategory": "tools/bead-boards",
        },
        "bead-frames": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/bead-frames/",
            "subcategory": "jewelry-findings/bead-frames",
        },
        "bead-reamers": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/bead-reamers/",
            "subcategory": "tools/bead-reamers",
        },
        "beads-jewelry-acrylic": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/acrylic/",
            "subcategory": "beads/strung-beads/acrylic",
        },
        "beads-jewelry-adhesives": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/adhesives/",
            "subcategory": "tools/adhesives",
        },
        "beads-jewelry-bead-jewelry-storage": {
            "url": "https://www.michaels.com/shop/beads-jewelry/bead-jewelry-storage/",
            "subcategory": "bead-jewelry-storage",
        },
        "beads-jewelry-bead-kits": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/bead-kits/",
            "subcategory": "beads/crafting-beads/bead-kits",
        },
        "beads-jewelry-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/",
            "subcategory": "beads",
        },
        "beads-jewelry-beads-jewelry": {
            "url": "https://www.michaels.com/shop/beads-jewelry/",
            "subcategory": "beads-jewelry",
        },
        "beads-jewelry-bracelets": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/bracelets/",
            "subcategory": "finished-jewelry/bracelets",
        },
        "beads-jewelry-bracelets-2": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/bracelets/",
            "subcategory": "jewelry-findings/bracelets",
        },
        "beads-jewelry-charms": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/charms/",
            "subcategory": "charm-shop-pendants/charms",
        },
        "beads-jewelry-czech-glass-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/czech-glass-beads/",
            "subcategory": "beads/crafting-beads/czech-glass-beads",
        },
        "beads-jewelry-czech-glass-beads-2": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/seed-beads/czech-glass-beads/",
            "subcategory": "beads/seed-beads/czech-glass-beads",
        },
        "beads-jewelry-czech-glass-beads-3": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/czech-glass-beads/",
            "subcategory": "beads/strung-beads/czech-glass-beads",
        },
        "beads-jewelry-earrings": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/earrings/",
            "subcategory": "jewelry-findings/earrings",
        },
        "beads-jewelry-earrings-2": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/earrings/",
            "subcategory": "finished-jewelry/earrings",
        },
        "beads-jewelry-eye-head-pins": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/eye-head-pins/",
            "subcategory": "jewelry-findings/eye-head-pins",
        },
        "beads-jewelry-fillers": {
            "url": "https://www.michaels.com/shop/beads-jewelry/uv-resin/fillers/",
            "subcategory": "uv-resin/fillers",
        },
        "beads-jewelry-finished-jewelry": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/",
            "subcategory": "finished-jewelry",
        },
        "beads-jewelry-gems-rhinestones": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/",
            "subcategory": "gems-rhinestones",
        },
        "beads-jewelry-glass": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/glass/",
            "subcategory": "beads/strung-beads/glass",
        },
        "beads-jewelry-hemp": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-cording/hemp/",
            "subcategory": "jewelry-cording/hemp",
        },
        "beads-jewelry-jewelry-findings": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/",
            "subcategory": "jewelry-findings",
        },
        "beads-jewelry-jump-split-double-rings": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/jump-split-double-rings/",
            "subcategory": "jewelry-findings/jump-split-double-rings",
        },
        "beads-jewelry-jute": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-cording/jute/",
            "subcategory": "jewelry-cording/jute",
        },
        "beads-jewelry-macrame": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-cording/macrame/",
            "subcategory": "jewelry-cording/macrame",
        },
        "beads-jewelry-necklaces": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/necklaces/",
            "subcategory": "finished-jewelry/necklaces",
        },
        "beads-jewelry-necklaces-2": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/necklaces/",
            "subcategory": "jewelry-findings/necklaces",
        },
        "beads-jewelry-needles": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/needles/",
            "subcategory": "tools/needles",
        },
        "beads-jewelry-safety-bar-pins": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/safety-bar-pins/",
            "subcategory": "jewelry-findings/safety-bar-pins",
        },
        "beads-jewelry-stringing-materials": {
            "url": "https://www.michaels.com/shop/beads-jewelry/stringing-materials/",
            "subcategory": "stringing-materials",
        },
        "beads-jewelry-tools": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/",
            "subcategory": "tools",
        },
        "beads-jewelry-tools-2": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/tools/",
            "subcategory": "gems-rhinestones/tools",
        },
        "beads-jewelry-uv-resin": {
            "url": "https://www.michaels.com/shop/beads-jewelry/uv-resin/uv-resin/",
            "subcategory": "uv-resin/uv-resin",
        },
        "beads-jewelry-uv-resin-2": {
            "url": "https://www.michaels.com/shop/beads-jewelry/uv-resin/",
            "subcategory": "uv-resin",
        },
        "beads-jewelry-wood": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/wood/",
            "subcategory": "beads/strung-beads/wood",
        },
        "beads-jewelry-wood-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/wood-beads/",
            "subcategory": "beads/crafting-beads/wood-beads",
        },
        "bracelet-making": {
            "url": "https://www.michaels.com/shop/beads-jewelry/metal-stamping/bracelet-making/",
            "subcategory": "metal-stamping/bracelet-making",
        },
        "bracelet-stands": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/bracelet-stands/",
            "subcategory": "display-packaging/bracelet-stands",
        },
        "caps": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/caps/",
            "subcategory": "jewelry-findings/caps",
        },
        "ceramic-clay": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/ceramic-clay/",
            "subcategory": "beads/strung-beads/ceramic-clay",
        },
        "chain": {
            "url": "https://www.michaels.com/shop/beads-jewelry/stringing-materials/chain/",
            "subcategory": "stringing-materials/chain",
        },
        "charm-bracelets": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/charms/charm-bracelets/",
            "subcategory": "charm-shop-pendants/charms/charm-bracelets",
        },
        "charm-shop-pendants": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/",
            "subcategory": "charm-shop-pendants",
        },
        "charms-molds": {
            "url": "https://www.michaels.com/shop/beads-jewelry/uv-resin/charms-molds/",
            "subcategory": "uv-resin/charms-molds",
        },
        "clasps-toggles-closures": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/clasps-toggles-closures/",
            "subcategory": "jewelry-findings/clasps-toggles-closures",
        },
        "clay-tools": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-clay/clay-tools/",
            "subcategory": "jewelry-clay/clay-tools",
        },
        "clips-buckles": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/clips-buckles/",
            "subcategory": "jewelry-findings/clips-buckles",
        },
        "connectors": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/connectors/",
            "subcategory": "jewelry-findings/connectors",
        },
        "crafting-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/",
            "subcategory": "beads/crafting-beads",
        },
        "crimps": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/crimps/",
            "subcategory": "jewelry-findings/crimps",
        },
        "crystal-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/crystal-beads/",
            "subcategory": "beads/strung-beads/crystal-beads",
        },
        "design-stamps": {
            "url": "https://www.michaels.com/shop/beads-jewelry/metal-stamping/design-stamps/",
            "subcategory": "metal-stamping/design-stamps",
        },
        "display-packaging": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/",
            "subcategory": "display-packaging",
        },
        "earring-displays": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/earring-displays/",
            "subcategory": "display-packaging/earring-displays",
        },
        "enamel-pins": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/enamel-pins/",
            "subcategory": "finished-jewelry/enamel-pins",
        },
        "findings-assortments": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/findings-assortments/",
            "subcategory": "jewelry-findings/findings-assortments",
        },
        "flatback": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/flatback/",
            "subcategory": "gems-rhinestones/flatback",
        },
        "flatback-austrian-crystals": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/austrian-crystal/flatback-austrian-crystals/",
            "subcategory": "gems-rhinestones/austrian-crystal/flatback-austrian-crystals",
        },
        "found-objects": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-collections/found-objects/",
            "subcategory": "jewelry-collections/found-objects",
        },
        "glass-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/glass-beads/",
            "subcategory": "beads/crafting-beads/glass-beads",
        },
        "glass-pearls": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/glass-pearls/",
            "subcategory": "beads/strung-beads/glass-pearls",
        },
        "hair-accessory-findings": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/hair-accessory-findings/",
            "subcategory": "jewelry-findings/hair-accessory-findings",
        },
        "hammers-mallets": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/hammers-mallets/",
            "subcategory": "tools/hammers-mallets",
        },
        "heishi-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/heishi-beads/",
            "subcategory": "beads/crafting-beads/heishi-beads",
        },
        "hotfix": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/hotfix/",
            "subcategory": "gems-rhinestones/hotfix",
        },
        "hotfix-austrian-crystals": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/austrian-crystal/hotfix-austrian-crystals/",
            "subcategory": "gems-rhinestones/austrian-crystal/hotfix-austrian-crystals",
        },
        "ink-dyes-pigments": {
            "url": "https://www.michaels.com/shop/beads-jewelry/uv-resin/ink-dyes-pigments/",
            "subcategory": "uv-resin/ink-dyes-pigments",
        },
        "jewelry-clay": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-clay/",
            "subcategory": "jewelry-clay",
        },
        "jewelry-collections": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-collections/",
            "subcategory": "jewelry-collections",
        },
        "jewelry-cording": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-cording/",
            "subcategory": "jewelry-cording",
        },
        "jewelry-packaging": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/jewelry-packaging/",
            "subcategory": "display-packaging/jewelry-packaging",
        },
        "jewelry-storage": {
            "url": "https://www.michaels.com/shop/beads-jewelry/bead-jewelry-storage/jewelry-storage/",
            "subcategory": "bead-jewelry-storage/jewelry-storage",
        },
        "keychains-lanyards": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/keychains-lanyards/",
            "subcategory": "finished-jewelry/keychains-lanyards",
        },
        "kids-beads-jewelry": {
            "url": "https://www.michaels.com/shop/beads-jewelry/kids-beads-jewelry/",
            "subcategory": "kids-beads-jewelry",
        },
        "kits-tools": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/seed-beads/kits-tools/",
            "subcategory": "beads/seed-beads/kits-tools",
        },
        "lamps-magnifiers": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/lamps-magnifiers/",
            "subcategory": "tools/lamps-magnifiers",
        },
        "lampwork-glass-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/lampwork-glass-beads/",
            "subcategory": "beads/strung-beads/lampwork-glass-beads",
        },
        "large-hole-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/large-hole-beads/",
            "subcategory": "beads/strung-beads/large-hole-beads",
        },
        "leather-suede": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-cording/leather-suede/",
            "subcategory": "jewelry-cording/leather-suede",
        },
        "letter-stamps": {
            "url": "https://www.michaels.com/shop/beads-jewelry/metal-stamping/letter-stamps/",
            "subcategory": "metal-stamping/letter-stamps",
        },
        "licensed-charms": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/charms/licensed-charms/",
            "subcategory": "charm-shop-pendants/charms/licensed-charms",
        },
        "looms": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/looms/",
            "subcategory": "tools/looms",
        },
        "memory-wire": {
            "url": "https://www.michaels.com/shop/beads-jewelry/stringing-materials/memory-wire/",
            "subcategory": "stringing-materials/memory-wire",
        },
        "metal": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/metal/",
            "subcategory": "beads/strung-beads/metal",
        },
        "metal-props": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/metal-props/",
            "subcategory": "display-packaging/metal-props",
        },
        "metal-stamping": {
            "url": "https://www.michaels.com/shop/beads-jewelry/metal-stamping/",
            "subcategory": "metal-stamping",
        },
        "metal-stamping-blanks": {
            "url": "https://www.michaels.com/shop/beads-jewelry/metal-stamping/metal-stamping-blanks/",
            "subcategory": "metal-stamping/metal-stamping-blanks",
        },
        "metal-stamping-kits": {
            "url": "https://www.michaels.com/shop/beads-jewelry/metal-stamping/metal-stamping-kits/",
            "subcategory": "metal-stamping/metal-stamping-kits",
        },
        "metal-stamping-tools": {
            "url": "https://www.michaels.com/shop/beads-jewelry/metal-stamping/metal-stamping-tools/",
            "subcategory": "metal-stamping/metal-stamping-tools",
        },
        "metal-work": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/metal-work/",
            "subcategory": "tools/metal-work",
        },
        "millefiori-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/millefiori-beads/",
            "subcategory": "beads/strung-beads/millefiori-beads",
        },
        "mini": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/charms/mini/",
            "subcategory": "charm-shop-pendants/charms/mini",
        },
        "miscellaneous-jewelry-cording": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-cording/miscellaneous-jewelry-cording/",
            "subcategory": "jewelry-cording/miscellaneous-jewelry-cording",
        },
        "miscellaneous-props": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/miscellaneous-props/",
            "subcategory": "display-packaging/miscellaneous-props",
        },
        "mixed-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/mixed-beads/",
            "subcategory": "beads/strung-beads/mixed-beads",
        },
        "miyuki-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/seed-beads/miyuki-beads/",
            "subcategory": "beads/seed-beads/miyuki-beads",
        },
        "nail": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/nail/",
            "subcategory": "gems-rhinestones/nail",
        },
        "natural-stone-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/natural-stone-beads/",
            "subcategory": "beads/crafting-beads/natural-stone-beads",
        },
        "natural-stone-shell-pearl": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/natural-stone-shell-pearl/",
            "subcategory": "beads/strung-beads/natural-stone-shell-pearl",
        },
        "natural-stones": {
            "url": "https://www.michaels.com/shop/beads-jewelry/natural-stones/",
            "subcategory": "natural-stones",
        },
        "neck-forms-necklace-displays": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/neck-forms-necklace-displays/",
            "subcategory": "display-packaging/neck-forms-necklace-displays",
        },
        "other-jewelry-tools": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/other-jewelry-tools/",
            "subcategory": "tools/other-jewelry-tools",
        },
        "paracord": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-cording/paracord/",
            "subcategory": "jewelry-cording/paracord",
        },
        "pendants": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/pendants/",
            "subcategory": "charm-shop-pendants/pendants",
        },
        "plastic-acrylic-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/plastic-acrylic-beads/",
            "subcategory": "beads/crafting-beads/plastic-acrylic-beads",
        },
        "plastic-bead-storage": {
            "url": "https://www.michaels.com/shop/beads-jewelry/bead-jewelry-storage/plastic-bead-storage/",
            "subcategory": "bead-jewelry-storage/plastic-bead-storage",
        },
        "plated-charms": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/charms/plated-charms/",
            "subcategory": "charm-shop-pendants/charms/plated-charms",
        },
        "pliers": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/pliers/",
            "subcategory": "tools/pliers",
        },
        "rings": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/rings/",
            "subcategory": "jewelry-findings/rings",
        },
        "seed-bead-findings": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/seed-beads/seed-bead-findings/",
            "subcategory": "beads/seed-beads/seed-bead-findings",
        },
        "seed-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/seed-beads/",
            "subcategory": "beads/seed-beads",
        },
        "sew-on-austrian-crystals": {
            "url": "https://www.michaels.com/shop/beads-jewelry/gems-rhinestones/austrian-crystal/sew-on-austrian-crystals/",
            "subcategory": "gems-rhinestones/austrian-crystal/sew-on-austrian-crystals",
        },
        "silicone-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/crafting-beads/silicone-beads/",
            "subcategory": "beads/crafting-beads/silicone-beads",
        },
        "sliders": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/sliders/",
            "subcategory": "beads/strung-beads/sliders",
        },
        "spacers": {
            "url": "https://www.michaels.com/shop/beads-jewelry/jewelry-findings/spacers/",
            "subcategory": "jewelry-findings/spacers",
        },
        "sterling-silver-charms": {
            "url": "https://www.michaels.com/shop/beads-jewelry/charm-shop-pendants/charms/sterling-silver-charms/",
            "subcategory": "charm-shop-pendants/charms/sterling-silver-charms",
        },
        "stretchy-cord": {
            "url": "https://www.michaels.com/shop/beads-jewelry/stringing-materials/stretchy-cord/",
            "subcategory": "stringing-materials/stretchy-cord",
        },
        "stringing-thread": {
            "url": "https://www.michaels.com/shop/beads-jewelry/stringing-materials/stringing-thread/",
            "subcategory": "stringing-materials/stringing-thread",
        },
        "stringing-tools": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/stringing-tools/",
            "subcategory": "tools/stringing-tools",
        },
        "stringing-wire": {
            "url": "https://www.michaels.com/shop/beads-jewelry/stringing-materials/stringing-wire/",
            "subcategory": "stringing-materials/stringing-wire",
        },
        "strung-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/strung-beads/",
            "subcategory": "beads/strung-beads",
        },
        "tech-accessories": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/tech-accessories/",
            "subcategory": "finished-jewelry/tech-accessories",
        },
        "toho-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/seed-beads/toho-beads/",
            "subcategory": "beads/seed-beads/toho-beads",
        },
        "tool-sets-kits": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/tool-sets-kits/",
            "subcategory": "tools/tool-sets-kits",
        },
        "tools-kits": {
            "url": "https://www.michaels.com/shop/beads-jewelry/uv-resin/tools-kits/",
            "subcategory": "uv-resin/tools-kits",
        },
        "torches-irons": {
            "url": "https://www.michaels.com/shop/beads-jewelry/tools/torches-irons/",
            "subcategory": "tools/torches-irons",
        },
        "two-hole-duo-beads": {
            "url": "https://www.michaels.com/shop/beads-jewelry/beads/seed-beads/two-hole-duo-beads/",
            "subcategory": "beads/seed-beads/two-hole-duo-beads",
        },
        "velvet-props": {
            "url": "https://www.michaels.com/shop/beads-jewelry/display-packaging/velvet-props/",
            "subcategory": "display-packaging/velvet-props",
        },
        "wallets-cases": {
            "url": "https://www.michaels.com/shop/beads-jewelry/finished-jewelry/wallets-cases/",
            "subcategory": "finished-jewelry/wallets-cases",
        },
        "wire-wrapping-wire": {
            "url": "https://www.michaels.com/shop/beads-jewelry/stringing-materials/wire-wrapping-wire/",
            "subcategory": "stringing-materials/wire-wrapping-wire",
        },
    },
    "canvas": {
        "canvas-canvas": {
            "url": "https://www.michaels.com/shop/canvas/",
            "subcategory": "canvas",
        },
    },
    "christmas": {
        "christmas-christmas": {
            "url": "https://www.michaels.com/shop/christmas/",
            "subcategory": "christmas",
        },
    },
    "christmas-trees": {
        "christmas-trees-christmas-trees": {
            "url": "https://www.michaels.com/shop/christmas-trees/",
            "subcategory": "christmas-trees",
        },
    },
    "concert-prep": {
        "concert-bracelets": {
            "url": "https://www.michaels.com/shop/concert-prep/concert-bracelets/",
            "subcategory": "concert-bracelets",
        },
        "concert-prep": {
            "url": "https://www.michaels.com/shop/concert-prep/",
            "subcategory": "concert-prep",
        },
        "concert-tees": {
            "url": "https://www.michaels.com/shop/concert-prep/concert-tees/",
            "subcategory": "concert-tees",
        },
        "custom-bags-accessories": {
            "url": "https://www.michaels.com/shop/concert-prep/custom-bags-accessories/",
            "subcategory": "custom-bags-accessories",
        },
        "finishing-touches": {
            "url": "https://www.michaels.com/shop/concert-prep/finishing-touches/",
            "subcategory": "finishing-touches",
        },
        "memories": {
            "url": "https://www.michaels.com/shop/concert-prep/memories/",
            "subcategory": "memories",
        },
        "party-decor": {
            "url": "https://www.michaels.com/shop/concert-prep/party-decor/",
            "subcategory": "party-decor",
        },
        "poster-making": {
            "url": "https://www.michaels.com/shop/concert-prep/poster-making/",
            "subcategory": "poster-making",
        },
    },
    "craft-machines": {
        "3d-printers": {
            "url": "https://www.michaels.com/shop/craft-machines/3d-printers/",
            "subcategory": "3d-printers",
        },
        "apparel-surfaces": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/apparel-surfaces/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/apparel-surfaces",
        },
        "camera-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/cameras-accessories/camera-accessories/",
            "subcategory": "cameras-accessories/camera-accessories",
        },
        "cameras": {
            "url": "https://www.michaels.com/shop/craft-machines/cameras-accessories/cameras/",
            "subcategory": "cameras-accessories/cameras",
        },
        "cameras-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/cameras-accessories/",
            "subcategory": "cameras-accessories",
        },
        "cling": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/cling/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials/cling",
        },
        "craft-machines": {
            "url": "https://www.michaels.com/shop/craft-machines/",
            "subcategory": "craft-machines",
        },
        "craft-machines-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-tools-accessories/accessories/",
            "subcategory": "cutting-tools-accessories/accessories",
        },
        "craft-machines-adhesive-vinyl": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/adhesive-vinyl/",
            "subcategory": "cricut/cricut-materials-tools-accessories/adhesive-vinyl",
        },
        "craft-machines-adhesive-vinyl-2": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/",
            "subcategory": "cutting-materials/adhesive-vinyl",
        },
        "craft-machines-art-technology": {
            "url": "https://www.michaels.com/shop/craft-machines/art-technology/",
            "subcategory": "art-technology",
        },
        "craft-machines-cricut": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/",
            "subcategory": "cricut",
        },
        "craft-machines-cutting-machines": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-machines/",
            "subcategory": "cutting-machines",
        },
        "craft-machines-heat-presses": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/heat-presses/",
            "subcategory": "sublimation/heat-presses",
        },
        "craft-machines-heat-presses-2": {
            "url": "https://www.michaels.com/shop/craft-machines/heat-presses/",
            "subcategory": "heat-presses",
        },
        "craft-machines-label-makers": {
            "url": "https://www.michaels.com/shop/craft-machines/label-makers/",
            "subcategory": "label-makers",
        },
        "craft-machines-materials": {
            "url": "https://www.michaels.com/shop/craft-machines/glowforge/materials/",
            "subcategory": "glowforge/materials",
        },
        "craft-machines-mats": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-tools-accessories/mats/",
            "subcategory": "cutting-tools-accessories/mats",
        },
        "craft-machines-paper": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/paper/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials/paper",
        },
        "craft-machines-patterns": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/permanent/patterns/",
            "subcategory": "cutting-materials/adhesive-vinyl/permanent/patterns",
        },
        "craft-machines-patterns-2": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/heat-transfer-vinyl/patterns/",
            "subcategory": "cutting-materials/heat-transfer-vinyl/patterns",
        },
        "craft-machines-sewing-machines": {
            "url": "https://www.michaels.com/shop/craft-machines/sewing-machines/",
            "subcategory": "sewing-machines",
        },
        "craft-machines-solids": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/permanent/solids/",
            "subcategory": "cutting-materials/adhesive-vinyl/permanent/solids",
        },
        "craft-machines-solids-2": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/removable/solids/",
            "subcategory": "cutting-materials/adhesive-vinyl/removable/solids",
        },
        "craft-machines-solids-3": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/heat-transfer-vinyl/solids/",
            "subcategory": "cutting-materials/heat-transfer-vinyl/solids",
        },
        "craft-machines-specialty": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/removable/specialty/",
            "subcategory": "cutting-materials/adhesive-vinyl/removable/specialty",
        },
        "craft-machines-specialty-2": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/permanent/specialty/",
            "subcategory": "cutting-materials/adhesive-vinyl/permanent/specialty",
        },
        "craft-machines-specialty-3": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/heat-transfer-vinyl/specialty/",
            "subcategory": "cutting-materials/heat-transfer-vinyl/specialty",
        },
        "craft-machines-specialty-materials": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials",
        },
        "craft-machines-specialty-materials-2": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/specialty-materials/",
            "subcategory": "cutting-materials/specialty-materials",
        },
        "craft-machines-tools": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-tools-accessories/tools/",
            "subcategory": "cutting-tools-accessories/tools",
        },
        "craft-machines-transfer-tape": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/transfer-tape/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/transfer-tape",
        },
        "craft-machines-transfer-tape-2": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-tools-accessories/transfer-tape/",
            "subcategory": "cutting-tools-accessories/transfer-tape",
        },
        "cricut-autopress": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-autopress/",
            "subcategory": "cricut/cricut-machines/cricut-autopress",
        },
        "cricut-brightpad": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-brightpad/",
            "subcategory": "cricut/cricut-machines/cricut-brightpad",
        },
        "cricut-cutting-mats": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-cutting-mats/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-cutting-mats",
        },
        "cricut-easypress": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-easypress/",
            "subcategory": "cricut/cricut-machines/cricut-easypress",
        },
        "cricut-easypress-30": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-easypress/cricut-easypress-30/",
            "subcategory": "cricut/cricut-machines/cricut-easypress/cricut-easypress-30",
        },
        "cricut-easypress-mini": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-easypress/cricut-easypress-mini/",
            "subcategory": "cricut/cricut-machines/cricut-easypress/cricut-easypress-mini",
        },
        "cricut-explore": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-explore/",
            "subcategory": "cricut/cricut-machines/cricut-explore",
        },
        "cricut-glue-gun": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-glue-gun/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-glue-gun",
        },
        "cricut-joy": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-joy/",
            "subcategory": "cricut/cricut-machines/cricut-joy",
        },
        "cricut-joy-smart-iron-on": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/smart-materials/cricut-joy-smart-iron-on/",
            "subcategory": "cricut/cricut-materials-tools-accessories/smart-materials/cricut-joy-smart-iron-on",
        },
        "cricut-joy-smart-vinyl": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/smart-materials/cricut-joy-smart-vinyl/",
            "subcategory": "cricut/cricut-materials-tools-accessories/smart-materials/cricut-joy-smart-vinyl",
        },
        "cricut-joy-xtra": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-joy-xtra/",
            "subcategory": "cricut/cricut-machines/cricut-joy-xtra",
        },
        "cricut-machines": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/",
            "subcategory": "cricut/cricut-machines",
        },
        "cricut-maker": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-maker/",
            "subcategory": "cricut/cricut-machines/cricut-maker",
        },
        "cricut-materials-tools-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/",
            "subcategory": "cricut/cricut-materials-tools-accessories",
        },
        "cricut-mug-press": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/cricut-mug-press/",
            "subcategory": "cricut/cricut-machines/cricut-mug-press",
        },
        "cricut-pens-markers": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-pens-markers/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-pens-markers",
        },
        "cricut-storage": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-storage/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-storage",
        },
        "cutting-materials": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/",
            "subcategory": "cutting-materials",
        },
        "cutting-tools-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-tools-accessories/",
            "subcategory": "cutting-tools-accessories",
        },
        "cutting-weeding-tools": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/cutting-weeding-tools/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/cutting-weeding-tools",
        },
        "easypress-heat-mats": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/easypress-heat-mats/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/easypress-heat-mats",
        },
        "explore-blades-tips": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips/explore-blades-tips/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips/explore-blades-tips",
        },
        "faux-leather": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/faux-leather/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials/faux-leather",
        },
        "filament-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/3d-printers/filament-accessories/",
            "subcategory": "3d-printers/filament-accessories",
        },
        "foil": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/foil/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials/foil",
        },
        "foil-transfer": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/foil-transfer/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials/foil-transfer",
        },
        "glowforge": {
            "url": "https://www.michaels.com/shop/craft-machines/glowforge/",
            "subcategory": "glowforge",
        },
        "glowforge-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/glowforge/glowforge-accessories/",
            "subcategory": "glowforge/glowforge-accessories",
        },
        "glowforge-printers": {
            "url": "https://www.michaels.com/shop/craft-machines/glowforge/glowforge-printers/",
            "subcategory": "glowforge/glowforge-printers",
        },
        "heat-resistant-tape": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/infusible-ink/heat-resistant-tape/",
            "subcategory": "cricut/cricut-materials-tools-accessories/infusible-ink/heat-resistant-tape",
        },
        "heat-transfer": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-materials-tools-accessories/heat-transfer/",
            "subcategory": "silhouette/silhouette-materials-tools-accessories/heat-transfer",
        },
        "heat-transfer-vinyl": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/heat-transfer-vinyl/",
            "subcategory": "cutting-materials/heat-transfer-vinyl",
        },
        "infusible-ink": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/infusible-ink/",
            "subcategory": "cricut/cricut-materials-tools-accessories/infusible-ink",
        },
        "infusible-ink-apparel": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-apparel/",
            "subcategory": "cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-apparel",
        },
        "infusible-ink-blanks": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-blanks/",
            "subcategory": "cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-blanks",
        },
        "infusible-ink-mugs": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-mugs/",
            "subcategory": "cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-mugs",
        },
        "infusible-ink-transfer-sheets": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-transfer-sheets/",
            "subcategory": "cricut/cricut-materials-tools-accessories/infusible-ink/infusible-ink-transfer-sheets",
        },
        "insert-cards": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/insert-cards/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials/insert-cards",
        },
        "iron-on": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/iron-on/",
            "subcategory": "cricut/cricut-materials-tools-accessories/iron-on",
        },
        "iron-on-designs": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/iron-on/iron-on-designs/",
            "subcategory": "cricut/cricut-materials-tools-accessories/iron-on/iron-on-designs",
        },
        "joy-blades-tips": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips/joy-blades-tips/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips/joy-blades-tips",
        },
        "juliet": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-cutting-machines/juliet/",
            "subcategory": "siser/siser-cutting-machines/juliet",
        },
        "label-maker-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/label-makers/label-maker-accessories/",
            "subcategory": "label-makers/label-maker-accessories",
        },
        "light-pads-tablets": {
            "url": "https://www.michaels.com/shop/craft-machines/light-pads-tablets/",
            "subcategory": "light-pads-tablets",
        },
        "maker-blades-tips": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips/maker-blades-tips/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips/maker-blades-tips",
        },
        "mats-tools-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories",
        },
        "mics": {
            "url": "https://www.michaels.com/shop/craft-machines/cameras-accessories/camera-accessories/mics/",
            "subcategory": "cameras-accessories/camera-accessories/mics",
        },
        "oher-sublimation-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-housewares/oher-sublimation-accessories/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-housewares/oher-sublimation-accessories",
        },
        "paper-cards": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/paper-cards/",
            "subcategory": "cutting-materials/paper-cards",
        },
        "party-foil": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/specialty-materials/party-foil/",
            "subcategory": "cricut/cricut-materials-tools-accessories/specialty-materials/party-foil",
        },
        "permanent": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/permanent/",
            "subcategory": "cutting-materials/adhesive-vinyl/permanent",
        },
        "permanent-smart-vinyl": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/smart-materials/permanent-smart-vinyl/",
            "subcategory": "cricut/cricut-materials-tools-accessories/smart-materials/permanent-smart-vinyl",
        },
        "removable": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/adhesive-vinyl/removable/",
            "subcategory": "cutting-materials/adhesive-vinyl/removable",
        },
        "removable-smart-vinyl": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/smart-materials/removable-smart-vinyl/",
            "subcategory": "cricut/cricut-materials-tools-accessories/smart-materials/removable-smart-vinyl",
        },
        "replacement-blades": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-tools-accessories/replacement-blades/",
            "subcategory": "cutting-tools-accessories/replacement-blades",
        },
        "replacement-blades-tips": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips/",
            "subcategory": "cricut/cricut-materials-tools-accessories/mats-tools-accessories/replacement-blades-tips",
        },
        "romeo": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-cutting-machines/romeo/",
            "subcategory": "siser/siser-cutting-machines/romeo",
        },
        "samplers": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/samplers/",
            "subcategory": "cutting-materials/samplers",
        },
        "shotbox": {
            "url": "https://www.michaels.com/shop/craft-machines/cameras-accessories/shotbox/",
            "subcategory": "cameras-accessories/shotbox",
        },
        "silhouette": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/",
            "subcategory": "silhouette",
        },
        "silhouette-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-materials-tools-accessories/silhouette-accessories/",
            "subcategory": "silhouette/silhouette-materials-tools-accessories/silhouette-accessories",
        },
        "silhouette-cameo-4": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-machines/silhouette-cameo-4/",
            "subcategory": "silhouette/silhouette-machines/silhouette-cameo-4",
        },
        "silhouette-cameo-5": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-machines/silhouette-cameo-5/",
            "subcategory": "silhouette/silhouette-machines/silhouette-cameo-5",
        },
        "silhouette-cutting-materials": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-materials-tools-accessories/silhouette-cutting-materials/",
            "subcategory": "silhouette/silhouette-materials-tools-accessories/silhouette-cutting-materials",
        },
        "silhouette-cutting-mats": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-materials-tools-accessories/silhouette-cutting-mats/",
            "subcategory": "silhouette/silhouette-materials-tools-accessories/silhouette-cutting-mats",
        },
        "silhouette-machines": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-machines/",
            "subcategory": "silhouette/silhouette-machines",
        },
        "silhouette-materials-tools-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-materials-tools-accessories/",
            "subcategory": "silhouette/silhouette-materials-tools-accessories",
        },
        "siser": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/",
            "subcategory": "siser",
        },
        "siser-bulk-vinyl-rolls": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-bulk-vinyl-rolls/",
            "subcategory": "siser/siser-bulk-vinyl-rolls",
        },
        "siser-cutting-machines": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-cutting-machines/",
            "subcategory": "siser/siser-cutting-machines",
        },
        "siser-easypatterns-htv": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-heat-transfer-vinyl/siser-easypatterns-htv/",
            "subcategory": "siser/siser-heat-transfer-vinyl/siser-easypatterns-htv",
        },
        "siser-easypatterns-plus-htv": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-heat-transfer-vinyl/siser-easypatterns-plus-htv/",
            "subcategory": "siser/siser-heat-transfer-vinyl/siser-easypatterns-plus-htv",
        },
        "siser-easypatterns-psv": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-pressure-sensitive-vinyl/siser-easypatterns-psv/",
            "subcategory": "siser/siser-pressure-sensitive-vinyl/siser-easypatterns-psv",
        },
        "siser-easypsv": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-pressure-sensitive-vinyl/siser-easypsv/",
            "subcategory": "siser/siser-pressure-sensitive-vinyl/siser-easypsv",
        },
        "siser-easyweed-htv": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-heat-transfer-vinyl/siser-easyweed-htv/",
            "subcategory": "siser/siser-heat-transfer-vinyl/siser-easyweed-htv",
        },
        "siser-glitter-htv": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-heat-transfer-vinyl/siser-glitter-htv/",
            "subcategory": "siser/siser-heat-transfer-vinyl/siser-glitter-htv",
        },
        "siser-heat-press": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-heat-press/",
            "subcategory": "siser/siser-heat-press",
        },
        "siser-heat-transfer-vinyl": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-heat-transfer-vinyl/",
            "subcategory": "siser/siser-heat-transfer-vinyl",
        },
        "siser-pressure-sensitive-vinyl": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-pressure-sensitive-vinyl/",
            "subcategory": "siser/siser-pressure-sensitive-vinyl",
        },
        "siser-sampler-packs": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-sampler-packs/",
            "subcategory": "siser/siser-sampler-packs",
        },
        "siser-specialty-htv": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-heat-transfer-vinyl/siser-specialty-htv/",
            "subcategory": "siser/siser-heat-transfer-vinyl/siser-specialty-htv",
        },
        "siser-tools": {
            "url": "https://www.michaels.com/shop/craft-machines/siser/siser-tools/",
            "subcategory": "siser/siser-tools",
        },
        "smart-iron-on": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/smart-materials/smart-iron-on/",
            "subcategory": "cricut/cricut-materials-tools-accessories/smart-materials/smart-iron-on",
        },
        "smart-materials": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/smart-materials/",
            "subcategory": "cricut/cricut-materials-tools-accessories/smart-materials",
        },
        "smart-paper": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/smart-materials/smart-paper/",
            "subcategory": "cricut/cricut-materials-tools-accessories/smart-materials/smart-paper",
        },
        "stickerpix": {
            "url": "https://www.michaels.com/shop/craft-machines/cricut/cricut-machines/stickerpix/",
            "subcategory": "cricut/cricut-machines/stickerpix",
        },
        "sublimation": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/",
            "subcategory": "sublimation",
        },
        "sublimation-apparel": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-apparel/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-apparel",
        },
        "sublimation-coasters": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-housewares/sublimation-coasters/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-housewares/sublimation-coasters",
        },
        "sublimation-drinkware": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-drinkware/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-drinkware",
        },
        "sublimation-fabric": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-fabric/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-fabric",
        },
        "sublimation-frames-photo-panels": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-housewares/sublimation-frames-photo-panels/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-housewares/sublimation-frames-photo-panels",
        },
        "sublimation-housewares": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-housewares/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-housewares",
        },
        "sublimation-inks-markers": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-inks-markers/",
            "subcategory": "sublimation/sublimation-inks-markers",
        },
        "sublimation-mouse-pads": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-housewares/sublimation-mouse-pads/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-housewares/sublimation-mouse-pads",
        },
        "sublimation-oven": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-oven/",
            "subcategory": "sublimation/sublimation-oven",
        },
        "sublimation-pet-accessories": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/sublimation-pet-accessories/",
            "subcategory": "sublimation/sublimation-surfaces/sublimation-pet-accessories",
        },
        "sublimation-printers": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-printers/",
            "subcategory": "sublimation/sublimation-printers",
        },
        "sublimation-surfaces": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-surfaces/",
            "subcategory": "sublimation/sublimation-surfaces",
        },
        "sublimation-tools-stencils": {
            "url": "https://www.michaels.com/shop/craft-machines/sublimation/sublimation-tools-stencils/",
            "subcategory": "sublimation/sublimation-tools-stencils",
        },
        "tools-blades": {
            "url": "https://www.michaels.com/shop/craft-machines/silhouette/silhouette-materials-tools-accessories/tools-blades/",
            "subcategory": "silhouette/silhouette-materials-tools-accessories/tools-blades",
        },
        "transfer-sheets": {
            "url": "https://www.michaels.com/shop/craft-machines/cutting-materials/transfer-sheets/",
            "subcategory": "cutting-materials/transfer-sheets",
        },
        "typewriters": {
            "url": "https://www.michaels.com/shop/craft-machines/typewriters/",
            "subcategory": "typewriters",
        },
    },
    "crafts-hobbies": {
        "acrylic-craft-paints": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/acrylic-craft-paints/",
            "subcategory": "craft-paint/acrylic-craft-paints",
        },
        "acrylic-paints": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/cosplay-costume-making/acrylic-paints/",
            "subcategory": "cosplay-costume-making/acrylic-paints",
        },
        "acrylic-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/acrylic-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/acrylic-surfaces",
        },
        "additives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/additives/",
            "subcategory": "soap-making/additives",
        },
        "adhesive-remover": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/adhesive-remover/",
            "subcategory": "adhesives-magnets/adhesive-remover",
        },
        "adhesive-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/adhesive-stencils/",
            "subcategory": "craft-paint/stencils/adhesive-stencils",
        },
        "air-drying-clay": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/air-drying-clay/",
            "subcategory": "sculpture-modeling/air-drying-clay",
        },
        "animal-nature-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/animal-nature-stencils/",
            "subcategory": "craft-paint/stencils/animal-nature-stencils",
        },
        "animals": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/figurines/animals/",
            "subcategory": "miniatures/figurines/animals",
        },
        "armatures": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/armatures/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/armatures",
        },
        "arts-crafts-books": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/kids-books/arts-crafts-books/",
            "subcategory": "books/kids-books/arts-crafts-books",
        },
        "basic-crafts-supplies": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/basic-crafts-supplies/",
            "subcategory": "basic-crafts-supplies",
        },
        "bath-bomb-molds-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/bath-bomb-molds-kits/",
            "subcategory": "soap-making/bath-bomb-molds-kits",
        },
        "benches-tables-chairs": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/benches-tables-chairs/",
            "subcategory": "miniatures/benches-tables-chairs",
        },
        "brick-art": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/brick-art/",
            "subcategory": "diamond-painting/brick-art",
        },
        "bridges-paths": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/trees-plants-mushrooms/bridges-paths/",
            "subcategory": "miniatures/trees-plants-mushrooms/bridges-paths",
        },
        "brushes-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/",
            "subcategory": "craft-paint/brushes-accessories",
        },
        "building-materials": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/building-materials/",
            "subcategory": "miniatures/building-materials",
        },
        "bulk-value-pack-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/bulk-value-pack-paint/",
            "subcategory": "craft-paint/bulk-value-pack-paint",
        },
        "candle-dyes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/candle-dyes/",
            "subcategory": "candle-making/candle-dyes",
        },
        "candle-jars-containers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/candle-jars-containers/",
            "subcategory": "candle-making/candle-jars-containers",
        },
        "candle-making": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/",
            "subcategory": "candle-making",
        },
        "candle-making-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/candle-making-kits/",
            "subcategory": "candle-making/candle-making-kits",
        },
        "candle-molds-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/candle-molds-tools/",
            "subcategory": "candle-making/candle-molds-tools",
        },
        "candle-wax-gel-bases": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/candle-wax-gel-bases/",
            "subcategory": "candle-making/candle-wax-gel-bases",
        },
        "candle-wicks": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/candle-wicks/",
            "subcategory": "candle-making/candle-wicks",
        },
        "card-making-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/card-making-kits/",
            "subcategory": "diamond-painting/card-making-kits",
        },
        "carving-blocks": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/carving-blocks/",
            "subcategory": "sculpture-modeling/carving-blocks",
        },
        "ceramic-plaster-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/ceramic-plaster-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/ceramic-plaster-surfaces",
        },
        "chalk-markers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/paint-chalk-markers/chalk-markers/",
            "subcategory": "craft-paint/paint-chalk-markers/chalk-markers",
        },
        "chalkboard-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/chalkboard-paint/",
            "subcategory": "craft-paint/specialty-paints/chalkboard-paint",
        },
        "chalkboard-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/chalkboard-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/chalkboard-surfaces",
        },
        "chipboard-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/chipboard-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/chipboard-surfaces",
        },
        "clay": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/pottery/clay/",
            "subcategory": "sculpture-modeling/pottery/clay",
        },
        "clay-cutters": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/clay-cutters/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/clay-cutters",
        },
        "clay-molds": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/clay-molds/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/clay-molds",
        },
        "clean-up-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/clean-up-accessories/",
            "subcategory": "resin/clean-up-accessories",
        },
        "cleaning-supplies-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/cleaning-supplies-accessories/",
            "subcategory": "craft-paint/cleaning-supplies-accessories",
        },
        "clockmaking": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/clockmaking/",
            "subcategory": "clockmaking",
        },
        "coins-currency": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/collecting/coins-currency/",
            "subcategory": "collecting/coins-currency",
        },
        "collecting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/collecting/",
            "subcategory": "collecting",
        },
        "color": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/project-tape/color/",
            "subcategory": "adhesives-magnets/project-tape/color",
        },
        "color-shift": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/glitter-metallic-paint/color-shift/",
            "subcategory": "craft-paint/glitter-metallic-paint/color-shift",
        },
        "cording-lacing": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/cording-lacing/",
            "subcategory": "leather-crafting/cording-lacing",
        },
        "cosplay-costume-making": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/cosplay-costume-making/",
            "subcategory": "cosplay-costume-making",
        },
        "cosplay-craft-materials": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/cosplay-costume-making/cosplay-craft-materials/",
            "subcategory": "cosplay-costume-making/cosplay-craft-materials",
        },
        "craft-brush-sets": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/craft-brush-sets/",
            "subcategory": "craft-paint/brushes-accessories/craft-brush-sets",
        },
        "craft-paint-mediums": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/craft-paint-mediums/",
            "subcategory": "craft-paint/specialty-paints/craft-paint-mediums",
        },
        "crafting-adhesives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/crafting-adhesives/",
            "subcategory": "adhesives-magnets/crafting-adhesives",
        },
        "crafting-paint-sets": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/crafting-paint-sets/",
            "subcategory": "craft-paint/crafting-paint-sets",
        },
        "crafts-hobbies": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/",
            "subcategory": "crafts-hobbies",
        },
        "crafts-hobbies-adhesive": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/adhesive/",
            "subcategory": "leather-crafting/adhesive",
        },
        "crafts-hobbies-adhesives-magnets": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/",
            "subcategory": "adhesives-magnets",
        },
        "crafts-hobbies-birdhouses": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/birdhouses/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/birdhouses",
        },
        "crafts-hobbies-bonding-stabilizers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/bonding-stabilizers/",
            "subcategory": "adhesives-magnets/bonding-stabilizers",
        },
        "crafts-hobbies-books": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/",
            "subcategory": "books",
        },
        "crafts-hobbies-books-2": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/books/",
            "subcategory": "modeling-rocketry/books",
        },
        "crafts-hobbies-boxes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/crates-boxes/boxes/",
            "subcategory": "wood-blank-crafting-surfaces/crates-boxes/boxes",
        },
        "crafts-hobbies-canvas-painting-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/canvas-painting-kits/",
            "subcategory": "craft-paint/canvas-painting-kits",
        },
        "crafts-hobbies-coasters": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/unfinished-decor/coasters/",
            "subcategory": "wood-blank-crafting-surfaces/unfinished-decor/coasters",
        },
        "crafts-hobbies-command-strips-hooks": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/command-strips-hooks/",
            "subcategory": "adhesives-magnets/command-strips-hooks",
        },
        "crafts-hobbies-craft-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/",
            "subcategory": "craft-paint",
        },
        "crafts-hobbies-crates-boxes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/crates-boxes/",
            "subcategory": "wood-blank-crafting-surfaces/crates-boxes",
        },
        "crafts-hobbies-decor": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/decor/",
            "subcategory": "miniatures/decor",
        },
        "crafts-hobbies-diamond-painting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/",
            "subcategory": "diamond-painting",
        },
        "crafts-hobbies-dollhouses": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/dollhouses/",
            "subcategory": "miniatures/dollhouses",
        },
        "crafts-hobbies-drinkware": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/unfinished-decor/drinkware/",
            "subcategory": "wood-blank-crafting-surfaces/unfinished-decor/drinkware",
        },
        "crafts-hobbies-fabric-glue": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/fabric-glue/",
            "subcategory": "adhesives-magnets/fabric-glue",
        },
        "crafts-hobbies-fabric-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/fabric-paint/",
            "subcategory": "craft-paint/specialty-paints/fabric-paint",
        },
        "crafts-hobbies-figurines": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/figurines/",
            "subcategory": "miniatures/figurines",
        },
        "crafts-hobbies-fillers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/fillers/",
            "subcategory": "resin/fillers",
        },
        "crafts-hobbies-foam": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/basic-crafts-supplies/foam/",
            "subcategory": "basic-crafts-supplies/foam",
        },
        "crafts-hobbies-glass": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors/glass/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors/glass",
        },
        "crafts-hobbies-glitter": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/glitter/",
            "subcategory": "resin/glitter",
        },
        "crafts-hobbies-glue-guns": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/glue-guns/",
            "subcategory": "adhesives-magnets/glue-guns",
        },
        "crafts-hobbies-glue-sticks": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/glue-sticks/",
            "subcategory": "adhesives-magnets/glue-sticks",
        },
        "crafts-hobbies-hardware": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/hardware/",
            "subcategory": "leather-crafting/hardware",
        },
        "crafts-hobbies-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/kits/",
            "subcategory": "leather-crafting/kits",
        },
        "crafts-hobbies-knitting-crochet": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/needle-crafts/knitting-crochet/",
            "subcategory": "books/needle-crafts/knitting-crochet",
        },
        "crafts-hobbies-knives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/tools-accessories/knives/",
            "subcategory": "tools-accessories/knives",
        },
        "crafts-hobbies-leather": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/leather/",
            "subcategory": "leather-crafting/leather",
        },
        "crafts-hobbies-leather-crafting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/",
            "subcategory": "leather-crafting",
        },
        "crafts-hobbies-leather-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/leather-paint/",
            "subcategory": "craft-paint/specialty-paints/leather-paint",
        },
        "crafts-hobbies-letters-numbers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/letters-numbers/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/letters-numbers",
        },
        "crafts-hobbies-lights": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/lights/",
            "subcategory": "miniatures/lights",
        },
        "crafts-hobbies-magnets": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/magnets/",
            "subcategory": "diamond-painting/magnets",
        },
        "crafts-hobbies-magnets-2": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/magnets/",
            "subcategory": "adhesives-magnets/magnets",
        },
        "crafts-hobbies-mason-jars": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors/mason-jars/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors/mason-jars",
        },
        "crafts-hobbies-miniature-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/miniature-kits/",
            "subcategory": "miniatures/miniature-kits",
        },
        "crafts-hobbies-mirrors": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors/mirrors/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors/mirrors",
        },
        "crafts-hobbies-model-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/model-kits/",
            "subcategory": "modeling-rocketry/model-kits",
        },
        "crafts-hobbies-paint-markers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/paint-chalk-markers/paint-markers/",
            "subcategory": "craft-paint/paint-chalk-markers/paint-markers",
        },
        "crafts-hobbies-paint-pens": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/paint-pens/",
            "subcategory": "craft-paint/paint-pens",
        },
        "crafts-hobbies-paint-pouring": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/paint-pouring/",
            "subcategory": "craft-paint/specialty-paints/paint-pouring",
        },
        "crafts-hobbies-painting-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/painting-accessories/",
            "subcategory": "craft-paint/brushes-accessories/painting-accessories",
        },
        "crafts-hobbies-paper-mache": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/paper-mache/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/paper-mache",
        },
        "crafts-hobbies-power-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/tools-accessories/power-tools/",
            "subcategory": "tools-accessories/power-tools",
        },
        "crafts-hobbies-project-tape": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/project-tape/",
            "subcategory": "adhesives-magnets/project-tape",
        },
        "crafts-hobbies-resin": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/",
            "subcategory": "resin",
        },
        "crafts-hobbies-resin-2": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/resin/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/resin",
        },
        "crafts-hobbies-scissors": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/tools-accessories/scissors/",
            "subcategory": "tools-accessories/scissors",
        },
        "crafts-hobbies-sculpture-modeling": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/",
            "subcategory": "sculpture-modeling",
        },
        "crafts-hobbies-sponges": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/sponges/",
            "subcategory": "craft-paint/brushes-accessories/sponges",
        },
        "crafts-hobbies-spray-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/spray-paints/spray-paint/",
            "subcategory": "craft-paint/spray-paints/spray-paint",
        },
        "crafts-hobbies-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/",
            "subcategory": "craft-paint/stencils",
        },
        "crafts-hobbies-stepping-stone-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/stepping-stone-kits/",
            "subcategory": "mosaics-stepping-stones/stepping-stone-kits",
        },
        "crafts-hobbies-studio-supplies": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/studio-supplies/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/studio-supplies",
        },
        "crafts-hobbies-studio-supplies-2": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/pottery/studio-supplies/",
            "subcategory": "sculpture-modeling/pottery/studio-supplies",
        },
        "crafts-hobbies-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/clockmaking/surfaces/",
            "subcategory": "clockmaking/surfaces",
        },
        "crafts-hobbies-surfaces-supplies": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/surfaces-supplies/",
            "subcategory": "resin/surfaces-supplies",
        },
        "crafts-hobbies-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/cosplay-costume-making/tools/",
            "subcategory": "cosplay-costume-making/tools",
        },
        "crafts-hobbies-tools-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/mod-podge/tools-accessories/",
            "subcategory": "adhesives-magnets/mod-podge/tools-accessories",
        },
        "crafts-hobbies-tools-accessories-2": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/tools-accessories/",
            "subcategory": "tools-accessories",
        },
        "crafts-hobbies-tools-accessories-3": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/tools-accessories/",
            "subcategory": "mosaics-stepping-stones/tools-accessories",
        },
        "crafts-hobbies-tools-accessories-4": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/stained-glass/tools-accessories/",
            "subcategory": "mosaics-stepping-stones/stained-glass/tools-accessories",
        },
        "crafts-hobbies-tools-accessories-5": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/clockmaking/tools-accessories/",
            "subcategory": "clockmaking/tools-accessories",
        },
        "crafts-hobbies-tools-accessories-6": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/tools-accessories/",
            "subcategory": "leather-crafting/tools-accessories",
        },
        "crafts-hobbies-unfinished-decor": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/unfinished-decor/",
            "subcategory": "wood-blank-crafting-surfaces/unfinished-decor",
        },
        "crafts-hobbies-uv-resin": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/uv-resin/",
            "subcategory": "resin/uv-resin",
        },
        "crafts-hobbies-wearables": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/wearables/",
            "subcategory": "diamond-painting/wearables",
        },
        "crafts-hobbies-wood-burning-carving": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/wood-burning-carving/",
            "subcategory": "wood-blank-crafting-surfaces/wood-burning-carving",
        },
        "crafts-hobbies-words-shapes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/words-shapes/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/words-shapes",
        },
        "crates": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/crates-boxes/crates/",
            "subcategory": "wood-blank-crafting-surfaces/crates-boxes/crates",
        },
        "cuttable-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/cuttable-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/cuttable-surfaces",
        },
        "diamond-painting-decor": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/diamond-painting-decor/",
            "subcategory": "diamond-painting/diamond-painting-decor",
        },
        "diamond-painting-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/diamond-painting-kits/",
            "subcategory": "diamond-painting/diamond-painting-kits",
        },
        "diamond-painting-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/diamond-painting-tools/",
            "subcategory": "diamond-painting/diamond-painting-tools",
        },
        "diy-decor-multi-surface-brushes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/diy-decor-multi-surface-brushes/",
            "subcategory": "craft-paint/brushes-accessories/diy-decor-multi-surface-brushes",
        },
        "diy-decor-outdoor-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/diy-decor-outdoor-paint/",
            "subcategory": "craft-paint/diy-decor-outdoor-paint",
        },
        "dotzies": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/dotzies/",
            "subcategory": "diamond-painting/dotzies",
        },
        "enamels": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/enamels/",
            "subcategory": "craft-paint/specialty-paints/enamels",
        },
        "environment-props": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/environment-props/",
            "subcategory": "miniatures/environment-props",
        },
        "epoxy-resin": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/epoxy-resin/",
            "subcategory": "resin/epoxy-resin",
        },
        "extruders-rollers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/extruders-rollers/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/extruders-rollers",
        },
        "facial-body-soap": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/facial-body-soap/",
            "subcategory": "soap-making/facial-body-soap",
        },
        "fairies": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/figurines/fairies/",
            "subcategory": "miniatures/figurines/fairies",
        },
        "finishes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stains-finishes/finishes/",
            "subcategory": "craft-paint/stains-finishes/finishes",
        },
        "finishing-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stains-finishes/finishing-tools/",
            "subcategory": "craft-paint/stains-finishes/finishing-tools",
        },
        "fish-nets": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/basic-crafts-supplies/fish-nets/",
            "subcategory": "basic-crafts-supplies/fish-nets",
        },
        "floral-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/floral-stencils/",
            "subcategory": "craft-paint/stencils/floral-stencils",
        },
        "foam-brushes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/foam-brushes/",
            "subcategory": "craft-paint/brushes-accessories/foam-brushes",
        },
        "formulas": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/mod-podge/formulas/",
            "subcategory": "adhesives-magnets/mod-podge/formulas",
        },
        "fragrance-oils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/candle-making/fragrance-oils/",
            "subcategory": "candle-making/fragrance-oils",
        },
        "framed-diamond-painting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/framed-diamond-painting/",
            "subcategory": "diamond-painting/framed-diamond-painting",
        },
        "frames-came": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/stained-glass/frames-came/",
            "subcategory": "mosaics-stepping-stones/stained-glass/frames-came",
        },
        "freestyle-diamond-art": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/freestyle-diamond-art/",
            "subcategory": "diamond-painting/freestyle-diamond-art",
        },
        "gallon-glue": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/gallon-glue/",
            "subcategory": "adhesives-magnets/gallon-glue",
        },
        "glass-bevels": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/stained-glass/glass-bevels/",
            "subcategory": "mosaics-stepping-stones/stained-glass/glass-bevels",
        },
        "glass-etching": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/glass-etching/",
            "subcategory": "craft-paint/specialty-paints/glass-etching",
        },
        "glass-porcelain-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/glass-porcelain-paint/",
            "subcategory": "craft-paint/specialty-paints/glass-porcelain-paint",
        },
        "glass-sheets": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/stained-glass/glass-sheets/",
            "subcategory": "mosaics-stepping-stones/stained-glass/glass-sheets",
        },
        "glass-surfaces-mirrors": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/glass-surfaces-mirrors",
        },
        "glaze": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/pottery/glaze/",
            "subcategory": "sculpture-modeling/pottery/glaze",
        },
        "glazes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/glazes/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/glazes",
        },
        "glitter-glue": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/glitter-glue/",
            "subcategory": "adhesives-magnets/glitter-glue",
        },
        "glitter-metallic-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/glitter-metallic-paint/",
            "subcategory": "craft-paint/glitter-metallic-paint",
        },
        "glitter-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/glitter-metallic-paint/glitter-paint/",
            "subcategory": "craft-paint/glitter-metallic-paint/glitter-paint",
        },
        "gnomes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/figurines/gnomes/",
            "subcategory": "miniatures/figurines/gnomes",
        },
        "gold-leaf": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stains-finishes/gold-leaf/",
            "subcategory": "craft-paint/stains-finishes/gold-leaf",
        },
        "grout-adhesives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/grout-adhesives/",
            "subcategory": "mosaics-stepping-stones/grout-adhesives",
        },
        "guided-wood-crafts": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/guided-wood-crafts/",
            "subcategory": "wood-blank-crafting-surfaces/guided-wood-crafts",
        },
        "hand-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/tools-accessories/hand-tools/",
            "subcategory": "tools-accessories/hand-tools",
        },
        "inks-dyes-pigments": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/inks-dyes-pigments/",
            "subcategory": "resin/inks-dyes-pigments",
        },
        "jewelry-adhesives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/jewelry-adhesives/",
            "subcategory": "adhesives-magnets/jewelry-adhesives",
        },
        "kids-books-2": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/kids-books/",
            "subcategory": "books/kids-books",
        },
        "kids-diamond-painting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/kids-diamond-painting/",
            "subcategory": "diamond-painting/kids-diamond-painting",
        },
        "kids-glue": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/kids-glue/",
            "subcategory": "adhesives-magnets/kids-glue",
        },
        "kids-reading": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/kids-books/kids-reading/",
            "subcategory": "books/kids-books/kids-reading",
        },
        "large-area-brushes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/large-area-brushes/",
            "subcategory": "craft-paint/brushes-accessories/large-area-brushes",
        },
        "leather-adhesive": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/leather-adhesive/",
            "subcategory": "adhesives-magnets/leather-adhesive",
        },
        "leather-care": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/leather-care/",
            "subcategory": "leather-crafting/leather-care",
        },
        "leather-paint-dye": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/leather-paint-dye/",
            "subcategory": "leather-crafting/leather-paint-dye",
        },
        "letter-boards": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/unfinished-decor/letter-boards/",
            "subcategory": "wood-blank-crafting-surfaces/unfinished-decor/letter-boards",
        },
        "letter-number-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/letter-number-stencils/",
            "subcategory": "craft-paint/stencils/letter-number-stencils",
        },
        "literature": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/literature/",
            "subcategory": "books/literature",
        },
        "mandala-medallion-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/mandala-medallion-stencils/",
            "subcategory": "craft-paint/stencils/mandala-medallion-stencils",
        },
        "marble-stone-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/marble-stone-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/marble-stone-surfaces",
        },
        "metal-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/metal-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/metal-surfaces",
        },
        "metallic-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/glitter-metallic-paint/metallic-paint/",
            "subcategory": "craft-paint/glitter-metallic-paint/metallic-paint",
        },
        "mini-diamond-painting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/mini-diamond-painting/",
            "subcategory": "diamond-painting/mini-diamond-painting",
        },
        "miniature-food": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/miniature-food/",
            "subcategory": "miniatures/miniature-food",
        },
        "miniature-structures": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/miniature-structures/",
            "subcategory": "miniatures/miniature-structures",
        },
        "miniatures": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/",
            "subcategory": "miniatures",
        },
        "mod-podge": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/mod-podge/",
            "subcategory": "adhesives-magnets/mod-podge",
        },
        "model-eva-foam": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/cosplay-costume-making/model-eva-foam/",
            "subcategory": "cosplay-costume-making/model-eva-foam",
        },
        "model-making-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/model-making-accessories/",
            "subcategory": "modeling-rocketry/model-making-accessories",
        },
        "model-making-paints": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/model-making-paints/",
            "subcategory": "modeling-rocketry/model-making-paints",
        },
        "model-making-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/model-making-tools/",
            "subcategory": "modeling-rocketry/model-making-tools",
        },
        "modeling-rocketry": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/",
            "subcategory": "modeling-rocketry",
        },
        "modeling-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/modeling-tools/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/modeling-tools",
        },
        "modeling-tools-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories",
        },
        "moldmaking-casting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/moldmaking-casting/",
            "subcategory": "sculpture-modeling/moldmaking-casting",
        },
        "mosaic-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/mosaic-kits/",
            "subcategory": "mosaics-stepping-stones/mosaic-kits",
        },
        "mosaics-stepping-stones": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/",
            "subcategory": "mosaics-stepping-stones",
        },
        "mounting-adhesives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/mounting-adhesives/",
            "subcategory": "adhesives-magnets/mounting-adhesives",
        },
        "multi-surface-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/multi-surface-paint/",
            "subcategory": "craft-paint/multi-surface-paint",
        },
        "mythical-creatures": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/figurines/mythical-creatures/",
            "subcategory": "miniatures/figurines/mythical-creatures",
        },
        "natural-wood": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/natural-wood/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/natural-wood",
        },
        "needle-crafts": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/needle-crafts/",
            "subcategory": "books/needle-crafts",
        },
        "needlework-quilting": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/needle-crafts/needlework-quilting/",
            "subcategory": "books/needle-crafts/needlework-quilting",
        },
        "neon-glow-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/neon-glow-paint/",
            "subcategory": "craft-paint/neon-glow-paint",
        },
        "non-hardening-clay": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/non-hardening-clay/",
            "subcategory": "sculpture-modeling/non-hardening-clay",
        },
        "outdoor-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/outdoor-stencils/",
            "subcategory": "craft-paint/stencils/outdoor-stencils",
        },
        "oven-bake-polymer-clay": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/oven-bake-polymer-clay/",
            "subcategory": "sculpture-modeling/oven-bake-polymer-clay",
        },
        "paint-chalk-markers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/paint-chalk-markers/",
            "subcategory": "craft-paint/paint-chalk-markers",
        },
        "paper-sculpture-paper-mache": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/paper-sculpture-paper-mache/",
            "subcategory": "sculpture-modeling/paper-sculpture-paper-mache",
        },
        "papercraft-adhesive": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/papercraft-adhesive/",
            "subcategory": "adhesives-magnets/papercraft-adhesive",
        },
        "pattern-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/pattern-stencils/",
            "subcategory": "craft-paint/stencils/pattern-stencils",
        },
        "people": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/figurines/people/",
            "subcategory": "miniatures/figurines/people",
        },
        "permanent-adhesives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/permanent-adhesives/",
            "subcategory": "adhesives-magnets/permanent-adhesives",
        },
        "pillow-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/diamond-painting/pillow-kits/",
            "subcategory": "diamond-painting/pillow-kits",
        },
        "planting-gardening": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/planting-gardening/",
            "subcategory": "books/planting-gardening",
        },
        "plants-flowers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/trees-plants-mushrooms/plants-flowers/",
            "subcategory": "miniatures/trees-plants-mushrooms/plants-flowers",
        },
        "pottery": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/pottery/",
            "subcategory": "sculpture-modeling/pottery",
        },
        "pottery-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/pottery/pottery-accessories/",
            "subcategory": "sculpture-modeling/pottery/pottery-accessories",
        },
        "pottery-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/pottery/pottery-tools/",
            "subcategory": "sculpture-modeling/pottery/pottery-tools",
        },
        "pottery-wheels": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/pottery/pottery-wheels/",
            "subcategory": "sculpture-modeling/pottery/pottery-wheels",
        },
        "printed": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/project-tape/printed/",
            "subcategory": "adhesives-magnets/project-tape/printed",
        },
        "resin-molds": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/resin-molds/",
            "subcategory": "resin/resin-molds",
        },
        "ribs-scrapers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/sculpture-modeling/modeling-tools-accessories/ribs-scrapers/",
            "subcategory": "sculpture-modeling/modeling-tools-accessories/ribs-scrapers",
        },
        "rockets": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/rockets/",
            "subcategory": "modeling-rocketry/rockets",
        },
        "sealers-finishes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/sealers-finishes/",
            "subcategory": "adhesives-magnets/sealers-finishes",
        },
        "sewing-supplies": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/cosplay-costume-making/sewing-supplies/",
            "subcategory": "cosplay-costume-making/sewing-supplies",
        },
        "shoe-care": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/leather-crafting/shoe-care/",
            "subcategory": "leather-crafting/shoe-care",
        },
        "silkscreen-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/silkscreen-stencils/",
            "subcategory": "craft-paint/stencils/silkscreen-stencils",
        },
        "slime-making-glue": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/slime-making-glue/",
            "subcategory": "adhesives-magnets/slime-making-glue",
        },
        "soap-bases": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/soap-bases/",
            "subcategory": "soap-making/soap-bases",
        },
        "soap-colorants": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/soap-colorants/",
            "subcategory": "soap-making/soap-colorants",
        },
        "soap-fragrance-oils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/soap-fragrance-oils/",
            "subcategory": "soap-making/soap-fragrance-oils",
        },
        "soap-making": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/",
            "subcategory": "soap-making",
        },
        "soap-making-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/soap-making-kits/",
            "subcategory": "soap-making/soap-making-kits",
        },
        "soap-making-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/soap-making-tools/",
            "subcategory": "soap-making/soap-making-tools",
        },
        "soap-molds": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/soap-making/soap-molds/",
            "subcategory": "soap-making/soap-molds",
        },
        "specialty-brushes-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/specialty-brushes-tools/",
            "subcategory": "craft-paint/brushes-accessories/specialty-brushes-tools",
        },
        "specialty-formulas": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/mod-podge/specialty-formulas/",
            "subcategory": "adhesives-magnets/mod-podge/specialty-formulas",
        },
        "specialty-paints": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/",
            "subcategory": "craft-paint/specialty-paints",
        },
        "spray-adhesives": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/spray-adhesives/",
            "subcategory": "adhesives-magnets/spray-adhesives",
        },
        "spray-paints": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/spray-paints/",
            "subcategory": "craft-paint/spray-paints",
        },
        "spray-primers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/spray-paints/spray-primers/",
            "subcategory": "craft-paint/spray-paints/spray-primers",
        },
        "spray-sealers": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/mod-podge/spray-sealers/",
            "subcategory": "adhesives-magnets/mod-podge/spray-sealers",
        },
        "spray-sealers-finishes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/spray-paints/spray-sealers-finishes/",
            "subcategory": "craft-paint/spray-paints/spray-sealers-finishes",
        },
        "stained-glass": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/stained-glass/",
            "subcategory": "mosaics-stepping-stones/stained-glass",
        },
        "stained-glass-kits": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/stained-glass/stained-glass-kits/",
            "subcategory": "mosaics-stepping-stones/stained-glass/stained-glass-kits",
        },
        "stains": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stains-finishes/stains/",
            "subcategory": "craft-paint/stains-finishes/stains",
        },
        "stains-finishes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stains-finishes/",
            "subcategory": "craft-paint/stains-finishes",
        },
        "stamps": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/collecting/stamps/",
            "subcategory": "collecting/stamps",
        },
        "stencil-brushes": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/brushes-accessories/stencil-brushes/",
            "subcategory": "craft-paint/brushes-accessories/stencil-brushes",
        },
        "stenciling-tools": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/stenciling-tools/",
            "subcategory": "craft-paint/stencils/stenciling-tools",
        },
        "surface-types": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types",
        },
        "tapes-dots": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/tapes-dots/",
            "subcategory": "adhesives-magnets/tapes-dots",
        },
        "tempera-paint": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/tempera-paint/",
            "subcategory": "craft-paint/specialty-paints/tempera-paint",
        },
        "tiles-gems-stones": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/mosaics-stepping-stones/tiles-gems-stones/",
            "subcategory": "mosaics-stepping-stones/tiles-gems-stones",
        },
        "timing-mechanisms": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/clockmaking/timing-mechanisms/",
            "subcategory": "clockmaking/timing-mechanisms",
        },
        "trees-plants-mushrooms": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/miniatures/trees-plants-mushrooms/",
            "subcategory": "miniatures/trees-plants-mushrooms",
        },
        "tumbler-turner-accessories": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/resin/tumbler-turner-accessories/",
            "subcategory": "resin/tumbler-turner-accessories",
        },
        "unfinished-wood-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces",
        },
        "water-marbling": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/specialty-paints/water-marbling/",
            "subcategory": "craft-paint/specialty-paints/water-marbling",
        },
        "wire-lights": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/cosplay-costume-making/wire-lights/",
            "subcategory": "cosplay-costume-making/wire-lights",
        },
        "wood-beads-turnings-dowels": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/wood-beads-turnings-dowels/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/wood-beads-turnings-dowels",
        },
        "wood-blank-crafting-surfaces": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/",
            "subcategory": "wood-blank-crafting-surfaces",
        },
        "wood-boards-panels": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/wood-boards-panels/",
            "subcategory": "wood-blank-crafting-surfaces/surface-types/unfinished-wood-surfaces/wood-boards-panels",
        },
        "wood-dowels": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/modeling-rocketry/wood-dowels/",
            "subcategory": "modeling-rocketry/wood-dowels",
        },
        "wood-glue": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/adhesives-magnets/wood-glue/",
            "subcategory": "adhesives-magnets/wood-glue",
        },
        "word-phrase-stencils": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/craft-paint/stencils/word-phrase-stencils/",
            "subcategory": "craft-paint/stencils/word-phrase-stencils",
        },
        "xadult-coloring": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/xadult-coloring/",
            "subcategory": "books/xadult-coloring",
        },
        "xbaking-cooking": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/xbaking-cooking/",
            "subcategory": "books/xbaking-cooking",
        },
        "xfine-art-books": {
            "url": "https://www.michaels.com/shop/crafts-hobbies/books/xfine-art-books/",
            "subcategory": "books/xfine-art-books",
        },
    },
    "cricut": {
        "cricut-cricut": {
            "url": "https://www.michaels.com/shop/cricut/",
            "subcategory": "cricut",
        },
    },
    "fabric": {
        "100-cotton": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/100-cotton/",
            "subcategory": "shop-fabric-by-material/100-cotton",
        },
        "100-cotton-fabric": {
            "url": "https://www.michaels.com/shop/fabric/100-cotton-fabric/",
            "subcategory": "100-cotton-fabric",
        },
        "anti-pill-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/anti-pill-fabric/",
            "subcategory": "shop-fabric-by-feature/anti-pill-fabric",
        },
        "apparel-costume-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-project/apparel-costume-fabric/",
            "subcategory": "shop-fabric-by-project/apparel-costume-fabric",
        },
        "bamboo": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/bamboo/",
            "subcategory": "shop-fabric-by-material/bamboo",
        },
        "batik": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/batik/",
            "subcategory": "shop-fabric-by-type/batik",
        },
        "chenille": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/chenille/",
            "subcategory": "shop-fabric-by-type/chenille",
        },
        "cosplay-fabric": {
            "url": "https://www.michaels.com/shop/fabric/cosplay-fabric/",
            "subcategory": "cosplay-fabric",
        },
        "cotton-blends": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/cotton-blends/",
            "subcategory": "shop-fabric-by-material/cotton-blends",
        },
        "dobby": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/dobby/",
            "subcategory": "shop-fabric-by-type/dobby",
        },
        "fabric-acrylic": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/acrylic/",
            "subcategory": "shop-fabric-by-material/acrylic",
        },
        "fabric-broadcloth": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/broadcloth/",
            "subcategory": "shop-fabric-by-type/broadcloth",
        },
        "fabric-brocade": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/brocade/",
            "subcategory": "shop-fabric-by-type/brocade",
        },
        "fabric-burlap": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/burlap/",
            "subcategory": "shop-fabric-by-type/burlap",
        },
        "fabric-canvas": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/canvas/",
            "subcategory": "shop-fabric-by-type/canvas",
        },
        "fabric-chambray": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/chambray/",
            "subcategory": "shop-fabric-by-type/chambray",
        },
        "fabric-chiffon": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/chiffon/",
            "subcategory": "shop-fabric-by-type/chiffon",
        },
        "fabric-corduroy": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/corduroy/",
            "subcategory": "shop-fabric-by-type/corduroy",
        },
        "fabric-cork": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/cork/",
            "subcategory": "shop-fabric-by-material/cork",
        },
        "fabric-crafting-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-project/crafting-fabric/",
            "subcategory": "shop-fabric-by-project/crafting-fabric",
        },
        "fabric-denim": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/denim/",
            "subcategory": "shop-fabric-by-type/denim",
        },
        "fabric-embroidered-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/embroidered-fabric/",
            "subcategory": "shop-fabric-by-feature/embroidered-fabric",
        },
        "fabric-fabric": {
            "url": "https://www.michaels.com/shop/fabric/",
            "subcategory": "fabric",
        },
        "fabric-faux-fur": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/faux-fur/",
            "subcategory": "shop-fabric-by-type/faux-fur",
        },
        "fabric-felt": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/felt/",
            "subcategory": "shop-fabric-by-type/felt",
        },
        "fabric-flannel": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/flannel/",
            "subcategory": "shop-fabric-by-type/flannel",
        },
        "fabric-fleece": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/fleece/",
            "subcategory": "shop-fabric-by-type/fleece",
        },
        "fabric-hemp": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/hemp/",
            "subcategory": "shop-fabric-by-material/hemp",
        },
        "fabric-home-decor-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-project/home-decor-fabric/",
            "subcategory": "shop-fabric-by-project/home-decor-fabric",
        },
        "fabric-jute": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/jute/",
            "subcategory": "shop-fabric-by-material/jute",
        },
        "fabric-lace": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/lace/",
            "subcategory": "shop-fabric-by-type/lace",
        },
        "fabric-leather": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/leather/",
            "subcategory": "shop-fabric-by-material/leather",
        },
        "fabric-licensed-character-fabric": {
            "url": "https://www.michaels.com/shop/fabric/licensed-character-fabric/",
            "subcategory": "licensed-character-fabric",
        },
        "fabric-mesh": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/mesh/",
            "subcategory": "shop-fabric-by-type/mesh",
        },
        "fabric-muslin": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/muslin/",
            "subcategory": "shop-fabric-by-type/muslin",
        },
        "fabric-nylon": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/nylon/",
            "subcategory": "shop-fabric-by-material/nylon",
        },
        "fabric-organza": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/organza/",
            "subcategory": "shop-fabric-by-type/organza",
        },
        "fabric-outdoor-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-project/outdoor-fabric/",
            "subcategory": "shop-fabric-by-project/outdoor-fabric",
        },
        "fabric-satin": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/satin/",
            "subcategory": "shop-fabric-by-type/satin",
        },
        "fabric-sport-team-fabric": {
            "url": "https://www.michaels.com/shop/fabric/sport-team-fabric/",
            "subcategory": "sport-team-fabric",
        },
        "fabric-tulle": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/tulle/",
            "subcategory": "shop-fabric-by-type/tulle",
        },
        "fabric-utility-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-project/utility-fabric/",
            "subcategory": "shop-fabric-by-project/utility-fabric",
        },
        "fabric-velvet": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/velvet/",
            "subcategory": "shop-fabric-by-type/velvet",
        },
        "fabric-vinyl": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/vinyl/",
            "subcategory": "shop-fabric-by-material/vinyl",
        },
        "fade-resistant-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/fade-resistant-fabric/",
            "subcategory": "shop-fabric-by-feature/fade-resistant-fabric",
        },
        "gauze": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/gauze/",
            "subcategory": "shop-fabric-by-type/gauze",
        },
        "high-performance-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/high-performance-fabric/",
            "subcategory": "shop-fabric-by-feature/high-performance-fabric",
        },
        "jersey": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/jersey/",
            "subcategory": "shop-fabric-by-type/jersey",
        },
        "linen": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/linen/",
            "subcategory": "shop-fabric-by-material/linen",
        },
        "minky": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/minky/",
            "subcategory": "shop-fabric-by-type/minky",
        },
        "mlb-fabric": {
            "url": "https://www.michaels.com/shop/fabric/sport-team-fabric/mlb-fabric/",
            "subcategory": "sport-team-fabric/mlb-fabric",
        },
        "modal": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/modal/",
            "subcategory": "shop-fabric-by-material/modal",
        },
        "moisture-wicking-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/moisture-wicking-fabric/",
            "subcategory": "shop-fabric-by-feature/moisture-wicking-fabric",
        },
        "nba-fabric": {
            "url": "https://www.michaels.com/shop/fabric/sport-team-fabric/nba-fabric/",
            "subcategory": "sport-team-fabric/nba-fabric",
        },
        "ncaa-fabric": {
            "url": "https://www.michaels.com/shop/fabric/sport-team-fabric/ncaa-fabric/",
            "subcategory": "sport-team-fabric/ncaa-fabric",
        },
        "neoprene": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/neoprene/",
            "subcategory": "shop-fabric-by-material/neoprene",
        },
        "nfl-fabric": {
            "url": "https://www.michaels.com/shop/fabric/sport-team-fabric/nfl-fabric/",
            "subcategory": "sport-team-fabric/nfl-fabric",
        },
        "olyfun": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/olyfun/",
            "subcategory": "shop-fabric-by-type/olyfun",
        },
        "polyester": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/polyester/",
            "subcategory": "shop-fabric-by-material/polyester",
        },
        "polyester-blends": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/polyester-blends/",
            "subcategory": "shop-fabric-by-material/polyester-blends",
        },
        "polypropylene": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/polypropylene/",
            "subcategory": "shop-fabric-by-material/polypropylene",
        },
        "quilting-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-project/quilting-fabric/",
            "subcategory": "shop-fabric-by-project/quilting-fabric",
        },
        "rayon": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/rayon/",
            "subcategory": "shop-fabric-by-material/rayon",
        },
        "sheer-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/sheer-fabric/",
            "subcategory": "shop-fabric-by-feature/sheer-fabric",
        },
        "shop-fabric-by-feature": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/",
            "subcategory": "shop-fabric-by-feature",
        },
        "shop-fabric-by-material": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/",
            "subcategory": "shop-fabric-by-material",
        },
        "shop-fabric-by-project": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-project/",
            "subcategory": "shop-fabric-by-project",
        },
        "shop-fabric-by-type": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-type/",
            "subcategory": "shop-fabric-by-type",
        },
        "silk": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-material/silk/",
            "subcategory": "shop-fabric-by-material/silk",
        },
        "strain-resistant-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/strain-resistant-fabric/",
            "subcategory": "shop-fabric-by-feature/strain-resistant-fabric",
        },
        "stretch-fabric": {
            "url": "https://www.michaels.com/shop/fabric/shop-fabric-by-feature/stretch-fabric/",
            "subcategory": "shop-fabric-by-feature/stretch-fabric",
        },
        "upholstery-fabric": {
            "url": "https://www.michaels.com/shop/fabric/upholstery-fabric/",
            "subcategory": "upholstery-fabric",
        },
    },
    "fabric-sewing-shop": {
        "108-quilter-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilter-solids/108-quilter-solids/",
            "subcategory": "fabrics/quilt-fabric/quilter-solids/108-quilter-solids",
        },
        "45-home-decor": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/45-home-decor/",
            "subcategory": "fabrics/home-decor-fabric/45-home-decor",
        },
        "anti-pill-fleece-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-prints/anti-pill-fleece-prints/",
            "subcategory": "fabrics/fleece/fleece-prints/anti-pill-fleece-prints",
        },
        "anti-pill-fleece-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-solids/anti-pill-fleece-solids/",
            "subcategory": "fabrics/fleece/fleece-solids/anti-pill-fleece-solids",
        },
        "apparel-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/",
            "subcategory": "fabrics/apparel-fabric",
        },
        "apparel-satin": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/apparel-satin/",
            "subcategory": "fabrics/apparel-fabric/apparel-satin",
        },
        "bamboo-knit": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bamboo-knit/",
            "subcategory": "fabrics/apparel-fabric/bamboo-knit",
        },
        "batiks": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/batiks/",
            "subcategory": "fabrics/quilt-fabric/batiks",
        },
        "bluey": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/bluey/",
            "subcategory": "fabrics/licensed-character-fabric/bluey",
        },
        "bobbins": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/thread-bobbins/bobbins/",
            "subcategory": "sewing-notions/thread-bobbins/bobbins",
        },
        "boning-foundations": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/boning-foundations/",
            "subcategory": "sewing-notions/bonding-stabilizers/boning-foundations",
        },
        "bottom-weights": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/bottom-weights/",
            "subcategory": "fabrics/apparel-fabric/fashion/bottom-weights",
        },
        "bridal-special-occasion": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion",
        },
        "brushed-knit": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/brushed-knit/",
            "subcategory": "fabrics/apparel-fabric/brushed-knit",
        },
        "cargo-netting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/cargo-netting/",
            "subcategory": "fabrics/utility-fabric/cargo-netting",
        },
        "clothing-care-dyes": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/clothing-care-dyes/",
            "subcategory": "clothing-care-dyes",
        },
        "costume-cosplay": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/costume-cosplay/",
            "subcategory": "fabrics/apparel-fabric/costume-cosplay",
        },
        "costumes": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-patterns/costumes/",
            "subcategory": "sewing-patterns/costumes",
        },
        "cotton": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/nursery-fabric/cotton/",
            "subcategory": "fabrics/nursery-fabric/cotton",
        },
        "cotton-cotton-blend-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/cotton-cotton-blend-fabric/",
            "subcategory": "fabrics/cotton-cotton-blend-fabric",
        },
        "cotton-solid-knit": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/cotton-solid-knit/",
            "subcategory": "fabrics/apparel-fabric/cotton-solid-knit",
        },
        "cotton-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/cotton-solids/",
            "subcategory": "fabrics/crafting-fabric/cotton-solids",
        },
        "craft-knives-blades": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/craft-knives-blades/",
            "subcategory": "shop-by-brand/fiskars/craft-knives-blades",
        },
        "craft-vinyl": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/craft-vinyl/",
            "subcategory": "fabrics/crafting-fabric/craft-vinyl",
        },
        "crepe": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/crepe/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/crepe",
        },
        "crinoline": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/crinoline/",
            "subcategory": "sewing-notions/bonding-stabilizers/crinoline",
        },
        "cutting-measuring": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/",
            "subcategory": "cutting-measuring",
        },
        "dc-comics": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/dc-comics/",
            "subcategory": "fabrics/licensed-character-fabric/dc-comics",
        },
        "decor-drapery": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/decor-drapery/",
            "subcategory": "fabrics/home-decor-fabric/decor-drapery",
        },
        "desk-lamps": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/desk-lamps/",
            "subcategory": "lighting/desk-lamps",
        },
        "diy-sewing-kits": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/diy-sewing-kits/",
            "subcategory": "diy-sewing-kits",
        },
        "dress-forms": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/dress-forms/",
            "subcategory": "dress-forms",
        },
        "duck-canvas": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/duck-canvas/",
            "subcategory": "fabrics/utility-fabric/duck-canvas",
        },
        "eco-velcro": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/velcro-brand/eco-velcro/",
            "subcategory": "shop-by-brand/velcro-brand/eco-velcro",
        },
        "elastic": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/elastic/",
            "subcategory": "sewing-notions/elastic",
        },
        "embroidery-scissors-thread-snips": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/embroidery-scissors-thread-snips/",
            "subcategory": "cutting-measuring/embroidery-scissors-thread-snips",
        },
        "fabric-care": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/fabric-care/",
            "subcategory": "shop-by-brand/singer/fabric-care",
        },
        "fabric-clips": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/fabric-clips/",
            "subcategory": "sewing-notions/fabric-clips",
        },
        "fabric-marking-tools": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/fabric-marking-tools/",
            "subcategory": "sewing-notions/fabric-marking-tools",
        },
        "fabric-sewing-shop": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/",
            "subcategory": "fabric-sewing-shop",
        },
        "fabric-sewing-shop-accessories": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-patterns/accessories/",
            "subcategory": "sewing-patterns/accessories",
        },
        "fabric-sewing-shop-accessories-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/accessories/",
            "subcategory": "lighting/accessories",
        },
        "fabric-sewing-shop-batting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/foam-fiber/batting/",
            "subcategory": "foam-fiber/batting",
        },
        "fabric-sewing-shop-batting-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/batting/",
            "subcategory": "quilting/batting",
        },
        "fabric-sewing-shop-bonding-stabilizers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/",
            "subcategory": "sewing-notions/bonding-stabilizers",
        },
        "fabric-sewing-shop-broadcloth": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilter-solids/broadcloth/",
            "subcategory": "fabrics/quilt-fabric/quilter-solids/broadcloth",
        },
        "fabric-sewing-shop-broadcloth-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/broadcloth/",
            "subcategory": "fabrics/crafting-fabric/broadcloth",
        },
        "fabric-sewing-shop-broadcloth-3": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/broadcloth/",
            "subcategory": "fabrics/quilt-fabric/broadcloth",
        },
        "fabric-sewing-shop-brocade": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/brocade/",
            "subcategory": "fabrics/apparel-fabric/fashion/brocade",
        },
        "fabric-sewing-shop-burlap": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/burlap/",
            "subcategory": "fabrics/crafting-fabric/burlap",
        },
        "fabric-sewing-shop-burlap-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/burlap/",
            "subcategory": "fabrics/utility-fabric/burlap",
        },
        "fabric-sewing-shop-buttons": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/buttons/",
            "subcategory": "sewing-notions/buttons",
        },
        "fabric-sewing-shop-chambray": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/chambray/",
            "subcategory": "fabrics/apparel-fabric/chambray",
        },
        "fabric-sewing-shop-chiffon": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/chiffon/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/chiffon",
        },
        "fabric-sewing-shop-christmas": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/christmas/",
            "subcategory": "fabrics/holiday-seasonal-fabric/christmas",
        },
        "fabric-sewing-shop-college": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/sport-team-fleece/college/",
            "subcategory": "fabrics/fleece/sport-team-fleece/college",
        },
        "fabric-sewing-shop-college-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/sport-team-fabric/college/",
            "subcategory": "fabrics/sport-team-fabric/college",
        },
        "fabric-sewing-shop-corduroy": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/corduroy/",
            "subcategory": "fabrics/apparel-fabric/corduroy",
        },
        "fabric-sewing-shop-cork": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/cork/",
            "subcategory": "fabrics/crafting-fabric/cork",
        },
        "fabric-sewing-shop-crafting-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/",
            "subcategory": "fabrics/crafting-fabric",
        },
        "fabric-sewing-shop-cutting-machines": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/cutting-machines/",
            "subcategory": "cutting-measuring/cutting-machines",
        },
        "fabric-sewing-shop-cutting-mats": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/cutting-mats/",
            "subcategory": "cutting-measuring/cutting-mats",
        },
        "fabric-sewing-shop-cutting-mats-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/cutting-mats/",
            "subcategory": "quilting/cutting-mats",
        },
        "fabric-sewing-shop-denim": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/denim/",
            "subcategory": "fabrics/apparel-fabric/denim",
        },
        "fabric-sewing-shop-disney": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/disney/",
            "subcategory": "fabrics/licensed-character-fabric/disney",
        },
        "fabric-sewing-shop-easter": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/easter/",
            "subcategory": "fabrics/holiday-seasonal-fabric/easter",
        },
        "fabric-sewing-shop-embroidered-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/decor-drapery/embroidered-fabric/",
            "subcategory": "fabrics/home-decor-fabric/decor-drapery/embroidered-fabric",
        },
        "fabric-sewing-shop-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/fabric/",
            "subcategory": "shop-by-brand/singer/fabric",
        },
        "fabric-sewing-shop-fabric-glue": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/fabric-glue/",
            "subcategory": "sewing-notions/bonding-stabilizers/fabric-glue",
        },
        "fabric-sewing-shop-faux-fur": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/faux-fur/",
            "subcategory": "fabrics/crafting-fabric/faux-fur",
        },
        "fabric-sewing-shop-felt": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/felt/",
            "subcategory": "fabrics/utility-fabric/felt",
        },
        "fabric-sewing-shop-felt-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/felt/",
            "subcategory": "fabrics/crafting-fabric/felt",
        },
        "fabric-sewing-shop-flannel": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/flannel/",
            "subcategory": "fabrics/flannel",
        },
        "fabric-sewing-shop-flannel-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/nursery-fabric/flannel/",
            "subcategory": "fabrics/nursery-fabric/flannel",
        },
        "fabric-sewing-shop-fleece": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/",
            "subcategory": "fabrics/fleece",
        },
        "fabric-sewing-shop-floor-lamps": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/floor-lamps/",
            "subcategory": "lighting/floor-lamps",
        },
        "fabric-sewing-shop-foam": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/foam-fiber/foam/",
            "subcategory": "foam-fiber/foam",
        },
        "fabric-sewing-shop-foam-fiber": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/foam-fiber/",
            "subcategory": "foam-fiber",
        },
        "fabric-sewing-shop-halloween": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/halloween/",
            "subcategory": "fabrics/holiday-seasonal-fabric/halloween",
        },
        "fabric-sewing-shop-harry-potter": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/harry-potter/",
            "subcategory": "fabrics/licensed-character-fabric/harry-potter",
        },
        "fabric-sewing-shop-hello-kitty": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/hello-kitty/",
            "subcategory": "fabrics/licensed-character-fabric/hello-kitty",
        },
        "fabric-sewing-shop-home-decor-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/",
            "subcategory": "fabrics/home-decor-fabric",
        },
        "fabric-sewing-shop-hoops-frames": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/hoops-frames/",
            "subcategory": "quilting/hoops-frames",
        },
        "fabric-sewing-shop-kids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-patterns/kids/",
            "subcategory": "sewing-patterns/kids",
        },
        "fabric-sewing-shop-knives": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/knives/",
            "subcategory": "cutting-measuring/knives",
        },
        "fabric-sewing-shop-lace": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/lace/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/lace",
        },
        "fabric-sewing-shop-licensed-character-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/",
            "subcategory": "fabrics/licensed-character-fabric",
        },
        "fabric-sewing-shop-lighting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/",
            "subcategory": "lighting",
        },
        "fabric-sewing-shop-loops-threads": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/loops-threads/",
            "subcategory": "shop-by-brand/loops-threads",
        },
        "fabric-sewing-shop-mesh": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/mesh/",
            "subcategory": "fabrics/apparel-fabric/fashion/mesh",
        },
        "fabric-sewing-shop-mesh-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/costume-cosplay/mesh/",
            "subcategory": "fabrics/apparel-fabric/costume-cosplay/mesh",
        },
        "fabric-sewing-shop-muslin": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/muslin/",
            "subcategory": "fabrics/crafting-fabric/muslin",
        },
        "fabric-sewing-shop-muslin-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/muslin/",
            "subcategory": "fabrics/utility-fabric/muslin",
        },
        "fabric-sewing-shop-needles": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/needles/",
            "subcategory": "sewing-notions/needles",
        },
        "fabric-sewing-shop-nfl": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/sport-team-fabric/nfl/",
            "subcategory": "fabrics/sport-team-fabric/nfl",
        },
        "fabric-sewing-shop-nfl-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/sport-team-fleece/nfl/",
            "subcategory": "fabrics/fleece/sport-team-fleece/nfl",
        },
        "fabric-sewing-shop-novelty": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/novelty/",
            "subcategory": "fabrics/quilt-fabric/novelty",
        },
        "fabric-sewing-shop-nylon": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/nylon/",
            "subcategory": "fabrics/utility-fabric/nylon",
        },
        "fabric-sewing-shop-organza": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/organza/",
            "subcategory": "fabrics/apparel-fabric/organza",
        },
        "fabric-sewing-shop-ottlite": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/ottlite/",
            "subcategory": "lighting/ottlite",
        },
        "fabric-sewing-shop-ottlite-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/ottlite/",
            "subcategory": "shop-by-brand/ottlite",
        },
        "fabric-sewing-shop-outdoor-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/outdoor-fabric/",
            "subcategory": "fabrics/home-decor-fabric/outdoor-fabric",
        },
        "fabric-sewing-shop-paper-trimmers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/paper-trimmers/",
            "subcategory": "shop-by-brand/fiskars/paper-trimmers",
        },
        "fabric-sewing-shop-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/flannel/prints/",
            "subcategory": "fabrics/flannel/prints",
        },
        "fabric-sewing-shop-prints-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/decor-drapery/prints/",
            "subcategory": "fabrics/home-decor-fabric/decor-drapery/prints",
        },
        "fabric-sewing-shop-prints-3": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/outdoor-fabric/prints/",
            "subcategory": "fabrics/home-decor-fabric/outdoor-fabric/prints",
        },
        "fabric-sewing-shop-prints-4": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/45-home-decor/prints/",
            "subcategory": "fabrics/home-decor-fabric/45-home-decor/prints",
        },
        "fabric-sewing-shop-quilting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/",
            "subcategory": "quilting",
        },
        "fabric-sewing-shop-quilting-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/nursery-fabric/quilting/",
            "subcategory": "fabrics/nursery-fabric/quilting",
        },
        "fabric-sewing-shop-rotary-cutters": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/rotary-cutters/",
            "subcategory": "quilting/rotary-cutters",
        },
        "fabric-sewing-shop-rotary-cutters-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/rotary-cutters/",
            "subcategory": "shop-by-brand/fiskars/rotary-cutters",
        },
        "fabric-sewing-shop-satin": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/satin/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/satin",
        },
        "fabric-sewing-shop-satin-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/costume-cosplay/satin/",
            "subcategory": "fabrics/apparel-fabric/costume-cosplay/satin",
        },
        "fabric-sewing-shop-scissors": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/scissors/",
            "subcategory": "shop-by-brand/fiskars/scissors",
        },
        "fabric-sewing-shop-sewing-baskets-organization": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-baskets-organization/",
            "subcategory": "sewing-baskets-organization",
        },
        "fabric-sewing-shop-sewing-machine-accessories": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/sewing-machine-accessories/",
            "subcategory": "shop-by-brand/singer/sewing-machine-accessories",
        },
        "fabric-sewing-shop-sewing-machine-accessories-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-machines-accessories/sewing-machine-accessories/",
            "subcategory": "sewing-machines-accessories/sewing-machine-accessories",
        },
        "fabric-sewing-shop-sewing-machines": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-machines-accessories/sewing-machines/",
            "subcategory": "sewing-machines-accessories/sewing-machines",
        },
        "fabric-sewing-shop-sewing-notions": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/",
            "subcategory": "sewing-notions",
        },
        "fabric-sewing-shop-sewing-notions-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/sewing-notions/",
            "subcategory": "shop-by-brand/singer/sewing-notions",
        },
        "fabric-sewing-shop-sheer": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/costume-cosplay/sheer/",
            "subcategory": "fabrics/apparel-fabric/costume-cosplay/sheer",
        },
        "fabric-sewing-shop-sheer-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/sheer/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/sheer",
        },
        "fabric-sewing-shop-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/decor-drapery/solids/",
            "subcategory": "fabrics/home-decor-fabric/decor-drapery/solids",
        },
        "fabric-sewing-shop-solids-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/outdoor-fabric/solids/",
            "subcategory": "fabrics/home-decor-fabric/outdoor-fabric/solids",
        },
        "fabric-sewing-shop-solids-3": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/45-home-decor/solids/",
            "subcategory": "fabrics/home-decor-fabric/45-home-decor/solids",
        },
        "fabric-sewing-shop-solids-4": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/flannel/solids/",
            "subcategory": "fabrics/flannel/solids",
        },
        "fabric-sewing-shop-specialty": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/nursery-fabric/specialty/",
            "subcategory": "fabrics/nursery-fabric/specialty",
        },
        "fabric-sewing-shop-sport-team-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/sport-team-fabric/",
            "subcategory": "fabrics/sport-team-fabric",
        },
        "fabric-sewing-shop-st-patricks-day": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/st-patricks-day/",
            "subcategory": "fabrics/holiday-seasonal-fabric/st-patricks-day",
        },
        "fabric-sewing-shop-star-wars": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/star-wars/",
            "subcategory": "fabrics/licensed-character-fabric/star-wars",
        },
        "fabric-sewing-shop-tools": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/tools/",
            "subcategory": "quilting/tools",
        },
        "fabric-sewing-shop-tulle": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/tulle/",
            "subcategory": "fabrics/crafting-fabric/tulle",
        },
        "fabric-sewing-shop-tulle-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/tulle/",
            "subcategory": "fabrics/apparel-fabric/tulle",
        },
        "fabric-sewing-shop-utility-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/",
            "subcategory": "fabrics/utility-fabric",
        },
        "fabric-sewing-shop-valentines-day": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/valentines-day/",
            "subcategory": "fabrics/holiday-seasonal-fabric/valentines-day",
        },
        "fabric-sewing-shop-velvet": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/velvet/",
            "subcategory": "fabrics/apparel-fabric/velvet",
        },
        "fabric-sewing-shop-velvet-2": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/decor-drapery/velvet/",
            "subcategory": "fabrics/home-decor-fabric/decor-drapery/velvet",
        },
        "fabric-shears": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/fabric-shears/",
            "subcategory": "cutting-measuring/fabric-shears",
        },
        "fabric-velcro": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/velcro-brand/fabric-velcro/",
            "subcategory": "shop-by-brand/velcro-brand/fabric-velcro",
        },
        "fabrics": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/",
            "subcategory": "fabrics",
        },
        "fall-harvest": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/fall-harvest/",
            "subcategory": "fabrics/holiday-seasonal-fabric/fall-harvest",
        },
        "fashion": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/",
            "subcategory": "fabrics/apparel-fabric/fashion",
        },
        "fashion-faux-fur": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/fashion-faux-fur/",
            "subcategory": "fabrics/apparel-fabric/fashion/fashion-faux-fur",
        },
        "fasteners-belting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/fasteners-belting/",
            "subcategory": "sewing-notions/fasteners-belting",
        },
        "faux-leather-suede": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/faux-leather-suede/",
            "subcategory": "fabrics/apparel-fabric/fashion/faux-leather-suede",
        },
        "fiskars": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/",
            "subcategory": "shop-by-brand/fiskars",
        },
        "fleece-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-prints/",
            "subcategory": "fabrics/fleece/fleece-prints",
        },
        "fleece-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-solids/",
            "subcategory": "fabrics/fleece/fleece-solids",
        },
        "fusible-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/fusible-fabric/",
            "subcategory": "sewing-notions/bonding-stabilizers/fusible-fabric",
        },
        "gaming": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/gaming/",
            "subcategory": "fabrics/licensed-character-fabric/gaming",
        },
        "general-purpose-scissors": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/general-purpose-scissors/",
            "subcategory": "cutting-measuring/general-purpose-scissors",
        },
        "general-purpose-velcro": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/velcro-brand/general-purpose-velcro/",
            "subcategory": "shop-by-brand/velcro-brand/general-purpose-velcro",
        },
        "grinch": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/grinch/",
            "subcategory": "fabrics/licensed-character-fabric/grinch",
        },
        "grommets-eyelets-rivets": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/fasteners-belting/grommets-eyelets-rivets/",
            "subcategory": "sewing-notions/fasteners-belting/grommets-eyelets-rivets",
        },
        "handheld-menders": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-machines-accessories/handheld-menders/",
            "subcategory": "sewing-machines-accessories/handheld-menders",
        },
        "heavy-duty-velcro": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/velcro-brand/heavy-duty-velcro/",
            "subcategory": "shop-by-brand/velcro-brand/heavy-duty-velcro",
        },
        "high-performance": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/high-performance/",
            "subcategory": "fabrics/home-decor-fabric/high-performance",
        },
        "holiday-seasonal-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/",
            "subcategory": "fabrics/holiday-seasonal-fabric",
        },
        "hook-loop": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/fasteners-belting/hook-loop/",
            "subcategory": "sewing-notions/fasteners-belting/hook-loop",
        },
        "interfacing-stabilizers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/interfacing-stabilizers/",
            "subcategory": "sewing-notions/bonding-stabilizers/interfacing-stabilizers",
        },
        "interfacings-interlinings": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/interfacings-interlinings/",
            "subcategory": "fabrics/quilt-fabric/interfacings-interlinings",
        },
        "interfacings-linings": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/interfacings-linings/",
            "subcategory": "fabrics/utility-fabric/interfacings-linings",
        },
        "iron-on-adhesives": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/iron-on-adhesives/",
            "subcategory": "sewing-notions/bonding-stabilizers/iron-on-adhesives",
        },
        "irons-steamers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/irons-steamers/",
            "subcategory": "irons-steamers",
        },
        "jersey-knit": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/jersey-knit/",
            "subcategory": "fabrics/apparel-fabric/jersey-knit",
        },
        "knits": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/knits/",
            "subcategory": "fabrics/apparel-fabric/fashion/knits",
        },
        "kona-premium-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/kona-premium-solids/",
            "subcategory": "fabrics/quilt-fabric/kona-premium-solids",
        },
        "licensed-character-fleece": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/licensed-character-fleece/",
            "subcategory": "fabrics/fleece/licensed-character-fleece",
        },
        "linen-linen-looks": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/linen-linen-looks/",
            "subcategory": "fabrics/apparel-fabric/fashion/linen-linen-looks",
        },
        "lining": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/lining/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/lining",
        },
        "machine-cases": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/machine-cases/",
            "subcategory": "shop-by-brand/singer/machine-cases",
        },
        "magnifier-lamps": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/magnifier-lamps/",
            "subcategory": "lighting/magnifier-lamps",
        },
        "marvel": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/marvel/",
            "subcategory": "fabrics/licensed-character-fabric/marvel",
        },
        "mats-rulers-sewing-notions": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/mats-rulers-sewing-notions/",
            "subcategory": "shop-by-brand/fiskars/mats-rulers-sewing-notions",
        },
        "mechanical-sewing-machines": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/mechanical-sewing-machines/",
            "subcategory": "shop-by-brand/singer/mechanical-sewing-machines",
        },
        "men": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-patterns/men/",
            "subcategory": "sewing-patterns/men",
        },
        "mesh-netting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/mesh-netting/",
            "subcategory": "fabrics/utility-fabric/mesh-netting",
        },
        "metallic-knits": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/costume-cosplay/metallic-knits/",
            "subcategory": "fabrics/apparel-fabric/costume-cosplay/metallic-knits",
        },
        "middle-weights": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/middle-weights/",
            "subcategory": "fabrics/apparel-fabric/fashion/middle-weights",
        },
        "minky-chenille": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/crafting-fabric/minky-chenille/",
            "subcategory": "fabrics/crafting-fabric/minky-chenille",
        },
        "misc-lamps": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/misc-lamps/",
            "subcategory": "lighting/misc-lamps",
        },
        "mlb": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/sport-team-fabric/mlb/",
            "subcategory": "fabrics/sport-team-fabric/mlb",
        },
        "movies-tv-shows": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/movies-tv-shows/",
            "subcategory": "fabrics/licensed-character-fabric/movies-tv-shows",
        },
        "nba": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/sport-team-fabric/nba/",
            "subcategory": "fabrics/sport-team-fabric/nba",
        },
        "nintendo": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/nintendo/",
            "subcategory": "fabrics/licensed-character-fabric/nintendo",
        },
        "no-sew-throws-kits": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/no-sew-throws-kits/",
            "subcategory": "fabrics/no-sew-throws-kits",
        },
        "novelty-mesh": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/novelty-mesh/",
            "subcategory": "fabrics/apparel-fabric/novelty-mesh",
        },
        "nu-foam": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/foam-fiber/nu-foam/",
            "subcategory": "foam-fiber/nu-foam",
        },
        "nursery-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/nursery-fabric/",
            "subcategory": "fabrics/nursery-fabric",
        },
        "other-45-fabric-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/45-home-decor/other-45-fabric-prints/",
            "subcategory": "fabrics/home-decor-fabric/45-home-decor/other-45-fabric-prints",
        },
        "other-licensed-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/other-licensed-fabric/",
            "subcategory": "fabrics/licensed-character-fabric/other-licensed-fabric",
        },
        "other-outdoor-fabric-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/outdoor-fabric/other-outdoor-fabric-prints/",
            "subcategory": "fabrics/home-decor-fabric/outdoor-fabric/other-outdoor-fabric-prints",
        },
        "other-quilter-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilter-solids/other-quilter-solids/",
            "subcategory": "fabrics/quilt-fabric/quilter-solids/other-quilter-solids",
        },
        "paper-punches-die-cutting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/paper-punches-die-cutting/",
            "subcategory": "shop-by-brand/fiskars/paper-punches-die-cutting",
        },
        "patches": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/patches/",
            "subcategory": "sewing-notions/bonding-stabilizers/patches",
        },
        "patriotic": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/holiday-seasonal-fabric/patriotic/",
            "subcategory": "fabrics/holiday-seasonal-fabric/patriotic",
        },
        "peanuts": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/peanuts/",
            "subcategory": "fabrics/licensed-character-fabric/peanuts",
        },
        "pillow-forms-bedding": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/foam-fiber/pillow-forms-bedding/",
            "subcategory": "foam-fiber/pillow-forms-bedding",
        },
        "pins": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/pins/",
            "subcategory": "sewing-notions/pins",
        },
        "plush-fleece-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-prints/plush-fleece-prints/",
            "subcategory": "fabrics/fleece/fleece-prints/plush-fleece-prints",
        },
        "plush-fleece-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-solids/plush-fleece-solids/",
            "subcategory": "fabrics/fleece/fleece-solids/plush-fleece-solids",
        },
        "pokemon": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/licensed-character-fabric/pokemon/",
            "subcategory": "fabrics/licensed-character-fabric/pokemon",
        },
        "poly-fleece-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-prints/poly-fleece-prints/",
            "subcategory": "fabrics/fleece/fleece-prints/poly-fleece-prints",
        },
        "poly-fleece-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/fleece-solids/poly-fleece-solids/",
            "subcategory": "fabrics/fleece/fleece-solids/poly-fleece-solids",
        },
        "pre-cut-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/pre-cut-fabric/",
            "subcategory": "fabrics/pre-cut-fabric",
        },
        "presser-feet": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/presser-feet/",
            "subcategory": "shop-by-brand/singer/presser-feet",
        },
        "quilt-blenders": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilt-blenders/",
            "subcategory": "fabrics/quilt-fabric/quilt-blenders",
        },
        "quilt-fabric": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/",
            "subcategory": "fabrics/quilt-fabric",
        },
        "quilt-flannel-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilt-flannel-prints/",
            "subcategory": "fabrics/quilt-fabric/quilt-flannel-prints",
        },
        "quilt-flannel-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilt-flannel-solids/",
            "subcategory": "fabrics/quilt-fabric/quilt-flannel-solids",
        },
        "quilter-premium": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilter-premium/",
            "subcategory": "fabrics/quilt-fabric/quilter-premium",
        },
        "quilter-prints": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilter-prints/",
            "subcategory": "fabrics/quilt-fabric/quilter-prints",
        },
        "quilter-solids": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilt-fabric/quilter-solids/",
            "subcategory": "fabrics/quilt-fabric/quilter-solids",
        },
        "quilting-kits": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/quilting-kits/",
            "subcategory": "fabrics/quilting-kits",
        },
        "quilting-patterns": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/quilting-patterns/",
            "subcategory": "quilting/quilting-patterns",
        },
        "quilting-rulers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/quilting-rulers/",
            "subcategory": "quilting/quilting-rulers",
        },
        "rayon-challis": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/rayon-challis/",
            "subcategory": "fabrics/apparel-fabric/rayon-challis",
        },
        "reading-glasses-magnifiers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/reading-glasses-magnifiers/",
            "subcategory": "sewing-notions/reading-glasses-magnifiers",
        },
        "rick-rack-binding": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/bonding-stabilizers/rick-rack-binding/",
            "subcategory": "sewing-notions/bonding-stabilizers/rick-rack-binding",
        },
        "rotary-cutting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/rotary-cutting/",
            "subcategory": "cutting-measuring/rotary-cutting",
        },
        "sergers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-machines-accessories/sergers/",
            "subcategory": "sewing-machines-accessories/sergers",
        },
        "sewing-embroidery-machine": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/sewing-embroidery-machine/",
            "subcategory": "shop-by-brand/singer/sewing-embroidery-machine",
        },
        "sewing-essentials": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/sewing-essentials/",
            "subcategory": "shop-by-brand/singer/sewing-essentials",
        },
        "sewing-machine-needles": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-machines-accessories/sewing-machine-needles/",
            "subcategory": "sewing-machines-accessories/sewing-machine-needles",
        },
        "sewing-machine-storage": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-machines-accessories/sewing-machine-storage/",
            "subcategory": "sewing-machines-accessories/sewing-machine-storage",
        },
        "sewing-machines-accessories": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-machines-accessories/",
            "subcategory": "sewing-machines-accessories",
        },
        "sewing-machines-sergers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/sewing-machines-sergers/",
            "subcategory": "shop-by-brand/singer/sewing-machines-sergers",
        },
        "sewing-patterns": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-patterns/",
            "subcategory": "sewing-patterns",
        },
        "sewing-tables-furniture": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-tables-furniture/",
            "subcategory": "sewing-tables-furniture",
        },
        "sewing-tools": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/sewing-tools/",
            "subcategory": "sewing-notions/sewing-tools",
        },
        "shop-by-brand": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/",
            "subcategory": "shop-by-brand",
        },
        "singer": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/",
            "subcategory": "shop-by-brand/singer",
        },
        "snaps-fasteners": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/fasteners-belting/snaps-fasteners/",
            "subcategory": "sewing-notions/fasteners-belting/snaps-fasteners",
        },
        "specialty-tools": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/fiskars/specialty-tools/",
            "subcategory": "shop-by-brand/fiskars/specialty-tools",
        },
        "sport-team-fleece": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/fleece/sport-team-fleece/",
            "subcategory": "fabrics/fleece/sport-team-fleece",
        },
        "stuffings-fillings": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/foam-fiber/stuffings-fillings/",
            "subcategory": "foam-fiber/stuffings-fillings",
        },
        "swim-dance": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/swim-dance/",
            "subcategory": "fabrics/apparel-fabric/fashion/swim-dance",
        },
        "taffeta": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/taffeta/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/taffeta",
        },
        "tape-measures-rulers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/cutting-measuring/tape-measures-rulers/",
            "subcategory": "cutting-measuring/tape-measures-rulers",
        },
        "tapes-adhesives": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/quilting/tapes-adhesives/",
            "subcategory": "quilting/tapes-adhesives",
        },
        "task-lamps": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/task-lamps/",
            "subcategory": "lighting/task-lamps",
        },
        "thread": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/thread-bobbins/thread/",
            "subcategory": "sewing-notions/thread-bobbins/thread",
        },
        "thread-bobbins": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/thread-bobbins/",
            "subcategory": "sewing-notions/thread-bobbins",
        },
        "tommy-bahama": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/tommy-bahama/",
            "subcategory": "fabrics/home-decor-fabric/tommy-bahama",
        },
        "top-weights": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/top-weights/",
            "subcategory": "fabrics/apparel-fabric/fashion/top-weights",
        },
        "trims-embellishments": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/trims-embellishments/",
            "subcategory": "fabrics/trims-embellishments",
        },
        "tulle-netting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/bridal-special-occasion/tulle-netting/",
            "subcategory": "fabrics/apparel-fabric/bridal-special-occasion/tulle-netting",
        },
        "upholstery": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/upholstery/",
            "subcategory": "fabrics/home-decor-fabric/upholstery",
        },
        "upholstery-drapery-supplies": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/upholstery-drapery-supplies/",
            "subcategory": "upholstery-drapery-supplies",
        },
        "usb-charging-lamps": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/lighting/usb-charging-lamps/",
            "subcategory": "lighting/usb-charging-lamps",
        },
        "velcro-brand": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/velcro-brand/",
            "subcategory": "shop-by-brand/velcro-brand",
        },
        "velcro-ties-straps": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/velcro-brand/velcro-ties-straps/",
            "subcategory": "shop-by-brand/velcro-brand/velcro-ties-straps",
        },
        "velour": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/costume-cosplay/velour/",
            "subcategory": "fabrics/apparel-fabric/costume-cosplay/velour",
        },
        "velvet-velvet-looks": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/velvet-velvet-looks/",
            "subcategory": "fabrics/apparel-fabric/fashion/velvet-velvet-looks",
        },
        "vinyl-leather": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/utility-fabric/vinyl-leather/",
            "subcategory": "fabrics/utility-fabric/vinyl-leather",
        },
        "wearable-cotton": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/apparel-fabric/fashion/wearable-cotton/",
            "subcategory": "fabrics/apparel-fabric/fashion/wearable-cotton",
        },
        "webbing-belting": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/fasteners-belting/webbing-belting/",
            "subcategory": "sewing-notions/fasteners-belting/webbing-belting",
        },
        "women": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-patterns/women/",
            "subcategory": "sewing-patterns/women",
        },
        "wovens": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/fabrics/home-decor-fabric/decor-drapery/wovens/",
            "subcategory": "fabrics/home-decor-fabric/decor-drapery/wovens",
        },
        "xcomputerized-sewing-machines": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/xcomputerized-sewing-machines/",
            "subcategory": "shop-by-brand/singer/xcomputerized-sewing-machines",
        },
        "xheavy-duty-sewing-machines": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/xheavy-duty-sewing-machines/",
            "subcategory": "shop-by-brand/singer/xheavy-duty-sewing-machines",
        },
        "xsergers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/shop-by-brand/singer/xsergers/",
            "subcategory": "shop-by-brand/singer/xsergers",
        },
        "zippers": {
            "url": "https://www.michaels.com/shop/fabric-sewing-shop/sewing-notions/zippers/",
            "subcategory": "sewing-notions/zippers",
        },
    },
    "fall": {
        "fall-fall": {
            "url": "https://www.michaels.com/shop/fall/",
            "subcategory": "fall",
        },
    },
    "floral": {
        "artificial-trees": {
            "url": "https://www.michaels.com/shop/floral/greenery/greenery-arrangements/artificial-trees/",
            "subcategory": "greenery/greenery-arrangements/artificial-trees",
        },
        "birds-butterflies-feathers": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/birds-butterflies-feathers/",
            "subcategory": "floral-supplies/birds-butterflies-feathers",
        },
        "bowl-vase-filler": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/",
            "subcategory": "bowl-vase-filler",
        },
        "bundles-bouquets": {
            "url": "https://www.michaels.com/shop/floral/floral-arrangements/bundles-bouquets/",
            "subcategory": "floral-arrangements/bundles-bouquets",
        },
        "clay-pots-saucers": {
            "url": "https://www.michaels.com/shop/floral/vases-containers/clay-pots-saucers/",
            "subcategory": "vases-containers/clay-pots-saucers",
        },
        "craft-foam": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/foam/craft-foam/",
            "subcategory": "floral-supplies/foam/craft-foam",
        },
        "decorative-filler": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/decorative-filler/",
            "subcategory": "bowl-vase-filler/decorative-filler",
        },
        "dried-floral-foam": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/foam/floral-foam/dried-floral-foam/",
            "subcategory": "floral-supplies/foam/floral-foam/dried-floral-foam",
        },
        "excelsior-raffia-straw": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/excelsior-raffia-straw/",
            "subcategory": "bowl-vase-filler/excelsior-raffia-straw",
        },
        "faux-floral-foam": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/foam/floral-foam/faux-floral-foam/",
            "subcategory": "floral-supplies/foam/floral-foam/faux-floral-foam",
        },
        "floor-vases": {
            "url": "https://www.michaels.com/shop/floral/vases-containers/vases/floor-vases/",
            "subcategory": "vases-containers/vases/floor-vases",
        },
        "floral-baskets": {
            "url": "https://www.michaels.com/shop/floral/vases-containers/baskets/",
            "subcategory": "vases-containers/baskets",
        },
        "floral-bushes": {
            "url": "https://www.michaels.com/shop/floral/floral-stems-bushes-picks/floral-bushes/",
            "subcategory": "floral-stems-bushes-picks/floral-bushes",
        },
        "floral-dried-floral": {
            "url": "https://www.michaels.com/shop/floral/dried-floral/",
            "subcategory": "dried-floral",
        },
        "floral-dried-floral-2": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/dried-floral/",
            "subcategory": "bowl-vase-filler/dried-floral",
        },
        "floral-floral": {
            "url": "https://www.michaels.com/shop/floral/",
            "subcategory": "floral",
        },
        "floral-floral-arrangements": {
            "url": "https://www.michaels.com/shop/floral/floral-arrangements/",
            "subcategory": "floral-arrangements",
        },
        "floral-floral-supplies": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/",
            "subcategory": "floral-supplies",
        },
        "floral-foam": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/foam/floral-foam/",
            "subcategory": "floral-supplies/foam/floral-foam",
        },
        "floral-foam-2": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/foam/",
            "subcategory": "floral-supplies/foam",
        },
        "floral-garlands": {
            "url": "https://www.michaels.com/shop/floral/garlands/",
            "subcategory": "garlands",
        },
        "floral-garlands-2": {
            "url": "https://www.michaels.com/shop/floral/greenery/garlands/",
            "subcategory": "greenery/garlands",
        },
        "floral-glue-guns": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/glue-guns/",
            "subcategory": "floral-supplies/glue-guns",
        },
        "floral-glue-sticks": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/glue-sticks/",
            "subcategory": "floral-supplies/glue-sticks",
        },
        "floral-greenery-arrangements": {
            "url": "https://www.michaels.com/shop/floral/greenery/greenery-arrangements/",
            "subcategory": "greenery/greenery-arrangements",
        },
        "floral-hangers": {
            "url": "https://www.michaels.com/shop/floral/wreaths/floral-hangers/",
            "subcategory": "wreaths/floral-hangers",
        },
        "floral-lights": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/lights/",
            "subcategory": "floral-supplies/lights",
        },
        "floral-mason-jars": {
            "url": "https://www.michaels.com/shop/floral/vases-containers/mason-jars/",
            "subcategory": "vases-containers/mason-jars",
        },
        "floral-mats": {
            "url": "https://www.michaels.com/shop/floral/greenery/mats/",
            "subcategory": "greenery/mats",
        },
        "floral-memorial": {
            "url": "https://www.michaels.com/shop/floral/memorial/",
            "subcategory": "memorial",
        },
        "floral-moss": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/moss/",
            "subcategory": "bowl-vase-filler/moss",
        },
        "floral-moss-2": {
            "url": "https://www.michaels.com/shop/floral/greenery/moss/",
            "subcategory": "greenery/moss",
        },
        "floral-picks": {
            "url": "https://www.michaels.com/shop/floral/floral-stems-bushes-picks/floral-picks/",
            "subcategory": "floral-stems-bushes-picks/floral-picks",
        },
        "floral-potted-plants": {
            "url": "https://www.michaels.com/shop/floral/greenery/greenery-arrangements/potted-plants/",
            "subcategory": "greenery/greenery-arrangements/potted-plants",
        },
        "floral-potted-plants-2": {
            "url": "https://www.michaels.com/shop/floral/floral-arrangements/potted-plants/",
            "subcategory": "floral-arrangements/potted-plants",
        },
        "floral-sand": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/sand/",
            "subcategory": "bowl-vase-filler/sand",
        },
        "floral-stems": {
            "url": "https://www.michaels.com/shop/floral/floral-stems-bushes-picks/floral-stems/",
            "subcategory": "floral-stems-bushes-picks/floral-stems",
        },
        "floral-stems-bushes-picks": {
            "url": "https://www.michaels.com/shop/floral/floral-stems-bushes-picks/",
            "subcategory": "floral-stems-bushes-picks",
        },
        "floral-tools": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/tools/",
            "subcategory": "floral-supplies/tools",
        },
        "floral-trees-floor-plants": {
            "url": "https://www.michaels.com/shop/floral/trees-floor-plants/",
            "subcategory": "trees-floor-plants",
        },
        "floral-vases-containers": {
            "url": "https://www.michaels.com/shop/floral/vases-containers/",
            "subcategory": "vases-containers",
        },
        "floral-wire": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/wire/",
            "subcategory": "floral-supplies/wire",
        },
        "floral-wreaths": {
            "url": "https://www.michaels.com/shop/floral/greenery/wreaths/",
            "subcategory": "greenery/wreaths",
        },
        "floral-wreaths-2": {
            "url": "https://www.michaels.com/shop/floral/wreaths/",
            "subcategory": "wreaths",
        },
        "fresh-floral-foam": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/foam/floral-foam/fresh-floral-foam/",
            "subcategory": "floral-supplies/foam/floral-foam/fresh-floral-foam",
        },
        "fruits-vegetables": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/fruits-vegetables/",
            "subcategory": "bowl-vase-filler/fruits-vegetables",
        },
        "gems-rocks": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/gems-rocks/",
            "subcategory": "bowl-vase-filler/gems-rocks",
        },
        "greenery": {
            "url": "https://www.michaels.com/shop/floral/greenery/",
            "subcategory": "greenery",
        },
        "greenery-bushes": {
            "url": "https://www.michaels.com/shop/floral/greenery/greenery-stems-bushes-picks/greenery-bushes/",
            "subcategory": "greenery/greenery-stems-bushes-picks/greenery-bushes",
        },
        "greenery-picks": {
            "url": "https://www.michaels.com/shop/floral/greenery/greenery-stems-bushes-picks/greenery-picks/",
            "subcategory": "greenery/greenery-stems-bushes-picks/greenery-picks",
        },
        "greenery-stems": {
            "url": "https://www.michaels.com/shop/floral/greenery/greenery-stems-bushes-picks/greenery-stems/",
            "subcategory": "greenery/greenery-stems-bushes-picks/greenery-stems",
        },
        "greenery-stems-bushes-picks": {
            "url": "https://www.michaels.com/shop/floral/greenery/greenery-stems-bushes-picks/",
            "subcategory": "greenery/greenery-stems-bushes-picks",
        },
        "live-plants": {
            "url": "https://www.michaels.com/shop/floral/live-plants/",
            "subcategory": "live-plants",
        },
        "pinecones": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/pinecones/",
            "subcategory": "bowl-vase-filler/pinecones",
        },
        "plant": {
            "url": "https://www.michaels.com/shop/floral/live-plants/plant/",
            "subcategory": "live-plants/plant",
        },
        "planters-containers": {
            "url": "https://www.michaels.com/shop/floral/vases-containers/planters-containers/",
            "subcategory": "vases-containers/planters-containers",
        },
        "shells": {
            "url": "https://www.michaels.com/shop/floral/bowl-vase-filler/shells/",
            "subcategory": "bowl-vase-filler/shells",
        },
        "succulents": {
            "url": "https://www.michaels.com/shop/floral/succulents/",
            "subcategory": "succulents",
        },
        "tabletop-floral-arrangements": {
            "url": "https://www.michaels.com/shop/floral/floral-arrangements/tabletop-floral-arrangements/",
            "subcategory": "floral-arrangements/tabletop-floral-arrangements",
        },
        "teardrops-swags": {
            "url": "https://www.michaels.com/shop/floral/teardrops-swags/",
            "subcategory": "teardrops-swags",
        },
        "vases": {
            "url": "https://www.michaels.com/shop/floral/vases-containers/vases/",
            "subcategory": "vases-containers/vases",
        },
        "wedding-floral": {
            "url": "https://www.michaels.com/shop/floral/wedding-floral/",
            "subcategory": "wedding-floral",
        },
        "wraps": {
            "url": "https://www.michaels.com/shop/floral/floral-supplies/wraps/",
            "subcategory": "floral-supplies/wraps",
        },
        "wreath-frames": {
            "url": "https://www.michaels.com/shop/floral/wreaths/wreath-frames/",
            "subcategory": "wreaths/wreath-frames",
        },
    },
    "frames": {
        "11x14-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/11x14-frames/",
            "subcategory": "shop-by-frame-size/11x14-frames",
        },
        "16x20-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/16x20-frames/",
            "subcategory": "shop-by-frame-size/16x20-frames",
        },
        "18x24-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/18x24-frames/",
            "subcategory": "shop-by-frame-size/18x24-frames",
        },
        "4x6-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/4x6-frames/",
            "subcategory": "shop-by-frame-size/4x6-frames",
        },
        "5x7-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/5x7-frames/",
            "subcategory": "shop-by-frame-size/5x7-frames",
        },
        "8x10-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/8x10-frames/",
            "subcategory": "shop-by-frame-size/8x10-frames",
        },
        "acrylic-floating-frames": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/acrylic-floating-frames/",
            "subcategory": "wall-frames/acrylic-floating-frames",
        },
        "acrylic-shadow-boxes": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/acrylic-shadow-boxes/",
            "subcategory": "shadow-boxes-display-cases/acrylic-shadow-boxes",
        },
        "acrylic-table-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/acrylic-table-frames/",
            "subcategory": "table-frames/acrylic-table-frames",
        },
        "album-record-frames": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/album-record-frames/",
            "subcategory": "shadow-boxes-display-cases/album-record-frames",
        },
        "aspect-wall-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/aspect-wall-frames/",
            "subcategory": "frame-collections/aspect-wall-frames",
        },
        "back-loading": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/shadow-boxes/back-loading/",
            "subcategory": "shadow-boxes-display-cases/shadow-boxes/back-loading",
        },
        "basics-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/basics-frames/",
            "subcategory": "frame-collections/basics-frames",
        },
        "bathroom-hooks": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/bathroom-hooks/",
            "subcategory": "command-strips-hooks/bathroom-hooks",
        },
        "belmont-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/belmont-frames/",
            "subcategory": "frame-collections/belmont-frames",
        },
        "canvas-hangers": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/canvas-hangers/",
            "subcategory": "framing-hardware/frame-hangers/canvas-hangers",
        },
        "clear-command-hooks": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/clear-command-hooks/",
            "subcategory": "command-strips-hooks/clear-command-hooks",
        },
        "clip-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/clip-frames/",
            "subcategory": "table-frames/clip-frames",
        },
        "collage-collection": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/collage-collection/",
            "subcategory": "frame-collections/collage-collection",
        },
        "collage-frames": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/collage-frames/",
            "subcategory": "multipacks-frame-sets/collage-frames",
        },
        "d-rings": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/d-rings/",
            "subcategory": "framing-hardware/frame-hangers/d-rings",
        },
        "decorative-hooks": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/decorative-hooks/",
            "subcategory": "command-strips-hooks/decorative-hooks",
        },
        "diploma-frames": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/diploma-frames/",
            "subcategory": "wall-frames/diploma-frames",
        },
        "display-cases": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/display-cases/",
            "subcategory": "shadow-boxes-display-cases/display-cases",
        },
        "document-frames": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/document-frames/",
            "subcategory": "wall-frames/document-frames",
        },
        "expressions-table-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/expressions-table-frames/",
            "subcategory": "frame-collections/expressions-table-frames",
        },
        "flag-case": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/flag-case/",
            "subcategory": "shadow-boxes-display-cases/flag-case",
        },
        "float-wall-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/float-wall-frames/",
            "subcategory": "frame-collections/float-wall-frames",
        },
        "floor-easels": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/floor-easels/",
            "subcategory": "picture-stands-shelves/floor-easels",
        },
        "football-jersey-frames": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/football-jersey-frames/",
            "subcategory": "shadow-boxes-display-cases/football-jersey-frames",
        },
        "frame-collections": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/",
            "subcategory": "frame-collections",
        },
        "frame-hangers": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/",
            "subcategory": "framing-hardware/frame-hangers",
        },
        "frames-adhesive": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/adhesive/",
            "subcategory": "framing-hardware/frame-hangers/adhesive",
        },
        "frames-canvas-frames": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/canvas-frames/",
            "subcategory": "wall-frames/canvas-frames",
        },
        "frames-collage-picture-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/collage-picture-frames/",
            "subcategory": "table-frames/collage-picture-frames",
        },
        "frames-collage-picture-frames-2": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/collage-picture-frames/",
            "subcategory": "wall-frames/collage-picture-frames",
        },
        "frames-collage-picture-frames-3": {
            "url": "https://www.michaels.com/shop/frames/collage-picture-frames/",
            "subcategory": "collage-picture-frames",
        },
        "frames-command-strips-hooks": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/",
            "subcategory": "command-strips-hooks",
        },
        "frames-digital-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/digital-frames/",
            "subcategory": "table-frames/digital-frames",
        },
        "frames-digital-frames-2": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/digital-frames/",
            "subcategory": "frame-collections/digital-frames",
        },
        "frames-floating-frames": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/floating-frames/",
            "subcategory": "wall-frames/floating-frames",
        },
        "frames-floating-frames-2": {
            "url": "https://www.michaels.com/shop/frames/table-frames/floating-frames/",
            "subcategory": "table-frames/floating-frames",
        },
        "frames-frame-mats": {
            "url": "https://www.michaels.com/shop/frames/frame-mats/",
            "subcategory": "frame-mats",
        },
        "frames-frames": {
            "url": "https://www.michaels.com/shop/frames/",
            "subcategory": "frames",
        },
        "frames-gallery-wall-frames": {
            "url": "https://www.michaels.com/shop/frames/gallery-wall-frames/",
            "subcategory": "gallery-wall-frames",
        },
        "frames-gallery-wall-frames-2": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/gallery-wall-frames/",
            "subcategory": "frame-collections/gallery-wall-frames",
        },
        "frames-holiday-frames": {
            "url": "https://www.michaels.com/shop/frames/holiday-frames/",
            "subcategory": "holiday-frames",
        },
        "frames-kits": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/kits/",
            "subcategory": "framing-hardware/frame-hangers/kits",
        },
        "frames-mini-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/mini-frames/",
            "subcategory": "frame-collections/mini-frames",
        },
        "frames-poster-frames": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/poster-frames/",
            "subcategory": "multipacks-frame-sets/poster-frames",
        },
        "frames-poster-frames-2": {
            "url": "https://www.michaels.com/shop/frames/poster-frames/",
            "subcategory": "poster-frames",
        },
        "frames-shadow-boxes": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/shadow-boxes/",
            "subcategory": "multipacks-frame-sets/shadow-boxes",
        },
        "frames-shadow-boxes-2": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/shadow-boxes/",
            "subcategory": "shadow-boxes-display-cases/shadow-boxes",
        },
        "frames-shadow-boxes-display-cases": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/",
            "subcategory": "shadow-boxes-display-cases",
        },
        "frames-single-opening": {
            "url": "https://www.michaels.com/shop/frames/table-frames/single-opening/",
            "subcategory": "table-frames/single-opening",
        },
        "frames-single-opening-2": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/single-opening/",
            "subcategory": "wall-frames/single-opening",
        },
        "frames-table-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/",
            "subcategory": "table-frames",
        },
        "frames-table-frames-2": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/table-frames/",
            "subcategory": "multipacks-frame-sets/table-frames",
        },
        "frames-tabletop-easels": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/tabletop-easels/",
            "subcategory": "picture-stands-shelves/tabletop-easels",
        },
        "frames-uncut-matboard": {
            "url": "https://www.michaels.com/shop/frames/frame-mats/uncut-matboard/",
            "subcategory": "frame-mats/uncut-matboard",
        },
        "frames-wall-frames": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/wall-frames/",
            "subcategory": "multipacks-frame-sets/wall-frames",
        },
        "frames-wall-frames-2": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/",
            "subcategory": "wall-frames",
        },
        "frames-wire": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/wire/",
            "subcategory": "framing-hardware/frame-hangers/wire",
        },
        "framing-hardware": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/",
            "subcategory": "framing-hardware",
        },
        "front-loading": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/shadow-boxes/front-loading/",
            "subcategory": "shadow-boxes-display-cases/shadow-boxes/front-loading",
        },
        "general-purpose-hooks": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/general-purpose-hooks/",
            "subcategory": "command-strips-hooks/general-purpose-hooks",
        },
        "graduation-frames": {
            "url": "https://www.michaels.com/shop/frames/graduation-frames/",
            "subcategory": "graduation-frames",
        },
        "heavy-duty-hooks": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/heavy-duty-hooks/",
            "subcategory": "command-strips-hooks/heavy-duty-hooks",
        },
        "home-collection": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/home-collection/",
            "subcategory": "frame-collections/home-collection",
        },
        "hooks-nails": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/hooks-nails/",
            "subcategory": "framing-hardware/frame-hangers/hooks-nails",
        },
        "houseware-hooks": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/houseware-hooks/",
            "subcategory": "command-strips-hooks/houseware-hooks",
        },
        "keepsake": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/keepsake/",
            "subcategory": "shadow-boxes-display-cases/keepsake",
        },
        "kids-art-frames": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/kids-art-frames/",
            "subcategory": "shadow-boxes-display-cases/kids-art-frames",
        },
        "large-picture-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/large-picture-frames/",
            "subcategory": "shop-by-frame-size/large-picture-frames",
        },
        "ledges-shelves": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/ledges-shelves/",
            "subcategory": "picture-stands-shelves/ledges-shelves",
        },
        "lifestyles-wall-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/lifestyles-wall-frames/",
            "subcategory": "frame-collections/lifestyles-wall-frames",
        },
        "lighted-display-cases": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/lighted-display-cases/",
            "subcategory": "shadow-boxes-display-cases/lighted-display-cases",
        },
        "logan-2-pack-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/logan-2-pack-frames/",
            "subcategory": "frame-collections/logan-2-pack-frames",
        },
        "mini-picture-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/mini-picture-frames/",
            "subcategory": "table-frames/mini-picture-frames",
        },
        "movie-poster-frames": {
            "url": "https://www.michaels.com/shop/frames/poster-frames/movie-poster-frames/",
            "subcategory": "poster-frames/movie-poster-frames",
        },
        "multipack-frames": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/multipack-frames/",
            "subcategory": "multipacks-frame-sets/multipack-frames",
        },
        "multipack-picture-stands": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/multipack-picture-stands/",
            "subcategory": "picture-stands-shelves/multipack-picture-stands",
        },
        "multipack-poster-frames": {
            "url": "https://www.michaels.com/shop/frames/poster-frames/multipack-poster-frames/",
            "subcategory": "poster-frames/multipack-poster-frames",
        },
        "multipack-shadow-boxes": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/multipack-shadow-boxes/",
            "subcategory": "shadow-boxes-display-cases/multipack-shadow-boxes",
        },
        "multipack-table-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/multipack-table-frames/",
            "subcategory": "table-frames/multipack-table-frames",
        },
        "multipack-wall-frames": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/multipack-wall-frames/",
            "subcategory": "wall-frames/multipack-wall-frames",
        },
        "multipacks": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/shadow-boxes/multipacks/",
            "subcategory": "shadow-boxes-display-cases/shadow-boxes/multipacks",
        },
        "multipacks-frame-sets": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/",
            "subcategory": "multipacks-frame-sets",
        },
        "non-standard-sizes": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/non-standard-sizes/",
            "subcategory": "shop-by-frame-size/non-standard-sizes",
        },
        "open-back-frames": {
            "url": "https://www.michaels.com/shop/frames/wall-frames/open-back-frames/",
            "subcategory": "wall-frames/open-back-frames",
        },
        "outdoor-command-hooks-strips": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/outdoor-command-hooks-strips/",
            "subcategory": "command-strips-hooks/outdoor-command-hooks-strips",
        },
        "pedestal-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/pedestal-frames/",
            "subcategory": "table-frames/pedestal-frames",
        },
        "photo-clips": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/photo-clips/",
            "subcategory": "picture-stands-shelves/photo-clips",
        },
        "photo-mounting": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/photo-mounting/",
            "subcategory": "framing-hardware/photo-mounting",
        },
        "picture-frame-sets": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/picture-frame-sets/",
            "subcategory": "multipacks-frame-sets/picture-frame-sets",
        },
        "picture-hanger-hooks-poster-strips": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/picture-hanger-hooks-poster-strips/",
            "subcategory": "command-strips-hooks/picture-hanger-hooks-poster-strips",
        },
        "picture-stands": {
            "url": "https://www.michaels.com/shop/frames/multipacks-frame-sets/picture-stands/",
            "subcategory": "multipacks-frame-sets/picture-stands",
        },
        "picture-stands-shelves": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/",
            "subcategory": "picture-stands-shelves",
        },
        "pins-adhesives": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/shadow-boxes/pins-adhesives/",
            "subcategory": "shadow-boxes-display-cases/shadow-boxes/pins-adhesives",
        },
        "plate-hangers": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/plate-hangers/",
            "subcategory": "picture-stands-shelves/plate-hangers",
        },
        "pre-cut-mats": {
            "url": "https://www.michaels.com/shop/frames/frame-mats/pre-cut-mats/",
            "subcategory": "frame-mats/pre-cut-mats",
        },
        "refill-strips": {
            "url": "https://www.michaels.com/shop/frames/command-strips-hooks/refill-strips/",
            "subcategory": "command-strips-hooks/refill-strips",
        },
        "round-picture-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/round-picture-frames/",
            "subcategory": "shop-by-frame-size/round-picture-frames",
        },
        "sawtooth": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/sawtooth/",
            "subcategory": "framing-hardware/frame-hangers/sawtooth",
        },
        "shop-by-frame-size": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/",
            "subcategory": "shop-by-frame-size",
        },
        "simply-essentials-frames": {
            "url": "https://www.michaels.com/shop/frames/frame-collections/simply-essentials-frames/",
            "subcategory": "frame-collections/simply-essentials-frames",
        },
        "small-picture-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/small-picture-frames/",
            "subcategory": "shop-by-frame-size/small-picture-frames",
        },
        "sports-frames": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/sports-frames/",
            "subcategory": "shadow-boxes-display-cases/sports-frames",
        },
        "square-picture-frames": {
            "url": "https://www.michaels.com/shop/frames/shop-by-frame-size/square-picture-frames/",
            "subcategory": "shop-by-frame-size/square-picture-frames",
        },
        "theme-picture-frames": {
            "url": "https://www.michaels.com/shop/frames/table-frames/theme-picture-frames/",
            "subcategory": "table-frames/theme-picture-frames",
        },
        "tool-free": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/frame-hangers/tool-free/",
            "subcategory": "framing-hardware/frame-hangers/tool-free",
        },
        "tools-hardware": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/tools-hardware/",
            "subcategory": "framing-hardware/tools-hardware",
        },
        "top-loading": {
            "url": "https://www.michaels.com/shop/frames/shadow-boxes-display-cases/shadow-boxes/top-loading/",
            "subcategory": "shadow-boxes-display-cases/shadow-boxes/top-loading",
        },
        "wall-hooks": {
            "url": "https://www.michaels.com/shop/frames/framing-hardware/wall-hooks/",
            "subcategory": "framing-hardware/wall-hooks",
        },
        "wall-lighting": {
            "url": "https://www.michaels.com/shop/frames/picture-stands-shelves/wall-lighting/",
            "subcategory": "picture-stands-shelves/wall-lighting",
        },
    },
    "halloween": {
        "halloween-halloween": {
            "url": "https://www.michaels.com/shop/halloween/",
            "subcategory": "halloween",
        },
    },
    "holidays-occasions": {
        "albums-scrapbooks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/crafting/albums-scrapbooks/",
            "subcategory": "graduation/crafting/albums-scrapbooks",
        },
        "angel-tree-toppers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-tree-toppers/angel-tree-toppers/",
            "subcategory": "christmas/christmas-decorations/christmas-tree-toppers/angel-tree-toppers",
        },
        "animal-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/animal-ornaments/",
            "subcategory": "christmas/christmas-ornaments/animal-ornaments",
        },
        "back-to-class-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/back-to-school-supplies/back-to-class-decor/",
            "subcategory": "back-to-school-supplies/back-to-class-decor",
        },
        "back-to-school-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/back-to-school-supplies/",
            "subcategory": "back-to-school-supplies",
        },
        "baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/baking/",
            "subcategory": "red-white-blue/baking",
        },
        "baking-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-baking/baking-accessories/",
            "subcategory": "christmas/christmas-party-baking/christmas-baking/baking-accessories",
        },
        "baking-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/baking-gifts/",
            "subcategory": "mothers-day/baking-gifts",
        },
        "ball-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/ball-ornaments/",
            "subcategory": "christmas/christmas-ornaments/ball-ornaments",
        },
        "berry-jolly": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/berry-jolly/",
            "subcategory": "christmas/christmas-decor-collections/berry-jolly",
        },
        "best-gifts-for-dad": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/best-gifts-for-dad/",
            "subcategory": "fathers-day/best-gifts-for-dad",
        },
        "boho-coast": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-collections/boho-coast/",
            "subcategory": "spring/spring-decor-collections/boho-coast",
        },
        "bound-by-magic": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decor-collections/bound-by-magic/",
            "subcategory": "halloween/halloween-decor-collections/bound-by-magic",
        },
        "bouquets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/bouquets/",
            "subcategory": "summer/summer-floral/bouquets",
        },
        "boxed-christmas-cards": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/boxed-christmas-cards/",
            "subcategory": "christmas/boxed-christmas-cards",
        },
        "buckets-toys": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-crafts-for-kids/buckets-toys/",
            "subcategory": "halloween/halloween-crafts-for-kids/buckets-toys",
        },
        "candle-holders-rings": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/candle-holders-rings/",
            "subcategory": "christmas/christmas-candles-fragrance/candle-holders-rings",
        },
        "candle-lamps": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/candle-lamps/",
            "subcategory": "christmas/christmas-candles-fragrance/candle-lamps",
        },
        "chairs": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/chairs/",
            "subcategory": "summer/outdoor-living/chairs",
        },
        "christmas-advent-calendars": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-advent-calendars/",
            "subcategory": "christmas/christmas-decorations/christmas-advent-calendars",
        },
        "christmas-apparel-jewelry": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-apparel-jewelry/",
            "subcategory": "christmas/christmas-apparel-jewelry",
        },
        "christmas-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-baking/",
            "subcategory": "christmas/christmas-party-baking/christmas-baking",
        },
        "christmas-baskets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-baskets/",
            "subcategory": "christmas/christmas-decorations/christmas-baskets",
        },
        "christmas-bathroom-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-bathroom-decor/",
            "subcategory": "christmas/christmas-decorations/christmas-bathroom-decor",
        },
        "christmas-birds": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-birds/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-birds",
        },
        "christmas-bouquets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-bouquets/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-bouquets",
        },
        "christmas-buildings": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/lemax-christmas-village/christmas-buildings/",
            "subcategory": "christmas/lemax-christmas-village/christmas-buildings",
        },
        "christmas-bushes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks/christmas-bushes/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks/christmas-bushes",
        },
        "christmas-bushes-stems-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks",
        },
        "christmas-candles-fragrance": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/",
            "subcategory": "christmas/christmas-candles-fragrance",
        },
        "christmas-candy": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-candy/",
            "subcategory": "christmas/christmas-party-baking/christmas-candy",
        },
        "christmas-crafts-diy": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/",
            "subcategory": "christmas/christmas-crafts-diy",
        },
        "christmas-decor-collections": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/",
            "subcategory": "christmas/christmas-decor-collections",
        },
        "christmas-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/",
            "subcategory": "christmas/christmas-decorations",
        },
        "christmas-decorative-boxes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-decorative-boxes/",
            "subcategory": "christmas/christmas-decorations/christmas-decorative-boxes",
        },
        "christmas-diamond-art": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-diamond-art/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-diamond-art",
        },
        "christmas-die-cuts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-die-cuts/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-die-cuts",
        },
        "christmas-dies-punches": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-dies-punches/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-dies-punches",
        },
        "christmas-door-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-door-decorations/",
            "subcategory": "christmas/christmas-decorations/christmas-door-decorations",
        },
        "christmas-doormats": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/outdoor-christmas-decorations/christmas-doormats/",
            "subcategory": "christmas/outdoor-christmas-decorations/christmas-doormats",
        },
        "christmas-embellishments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-embellishments/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-embellishments",
        },
        "christmas-fabric": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-fabric/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-fabric",
        },
        "christmas-figurines": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-figurines/",
            "subcategory": "christmas/christmas-decorations/christmas-figurines",
        },
        "christmas-fillers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-fillers/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-fillers",
        },
        "christmas-flags": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/outdoor-christmas-decorations/christmas-flags/",
            "subcategory": "christmas/outdoor-christmas-decorations/christmas-flags",
        },
        "christmas-floral-arrangements": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-floral-arrangements/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-floral-arrangements",
        },
        "christmas-floral-arrangements-greenery": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery",
        },
        "christmas-floral-containers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-floral-containers/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-floral-containers",
        },
        "christmas-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-garlands/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-garlands",
        },
        "christmas-gift-baskets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-gift-baskets/",
            "subcategory": "christmas/christmas-party-baking/christmas-gift-baskets",
        },
        "christmas-gift-wrap-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-storage/christmas-gift-wrap-storage/",
            "subcategory": "christmas/christmas-storage/christmas-gift-wrap-storage",
        },
        "christmas-glitter": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-glitter/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-glitter",
        },
        "christmas-inflatables": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-inflatables/",
            "subcategory": "christmas/christmas-inflatables",
        },
        "christmas-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/",
            "subcategory": "christmas/christmas-lights",
        },
        "christmas-lights-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-storage/christmas-lights-storage/",
            "subcategory": "christmas/christmas-storage/christmas-lights-storage",
        },
        "christmas-miniature-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-miniature-kits/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-miniature-kits",
        },
        "christmas-miniatures": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-miniatures/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-miniatures",
        },
        "christmas-minis": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-minis/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-minis",
        },
        "christmas-nativity": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-nativity/",
            "subcategory": "christmas/christmas-decorations/christmas-nativity",
        },
        "christmas-needle-art-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-needle-art-crafts/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-needle-art-crafts",
        },
        "christmas-nutcrackers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-nutcrackers/",
            "subcategory": "christmas/christmas-decorations/christmas-nutcrackers",
        },
        "christmas-ornament-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-ornament-kits/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-ornament-kits",
        },
        "christmas-ornament-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-storage/christmas-ornament-storage/",
            "subcategory": "christmas/christmas-storage/christmas-ornament-storage",
        },
        "christmas-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/",
            "subcategory": "christmas/christmas-ornaments",
        },
        "christmas-paper-craft-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-paper-craft-kits/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-paper-craft-kits",
        },
        "christmas-paper-pads": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-paper-pads/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-paper-pads",
        },
        "christmas-papercrafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting",
        },
        "christmas-party-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/",
            "subcategory": "christmas/christmas-party-baking",
        },
        "christmas-party-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-party-decorations/",
            "subcategory": "christmas/christmas-party-baking/christmas-party-decorations",
        },
        "christmas-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks/christmas-picks/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks/christmas-picks",
        },
        "christmas-pillows": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-pillows/",
            "subcategory": "christmas/christmas-decorations/christmas-pillows",
        },
        "christmas-ribbon-trimming": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ribbon-trimming/",
            "subcategory": "christmas/christmas-ribbon-trimming",
        },
        "christmas-santas": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-santas/",
            "subcategory": "christmas/christmas-decorations/christmas-santas",
        },
        "christmas-snow-globes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-snow-globes/",
            "subcategory": "christmas/christmas-decorations/christmas-snow-globes",
        },
        "christmas-stamps": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-stamps/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-stamps",
        },
        "christmas-stems": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks/christmas-stems/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-bushes-stems-picks/christmas-stems",
        },
        "christmas-stickers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-stickers/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-stickers",
        },
        "christmas-stitchery-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-stitchery-kits/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-stitchery-kits",
        },
        "christmas-stocking-holders": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-stockings-holders/christmas-stocking-holders/",
            "subcategory": "christmas/christmas-decorations/christmas-stockings-holders/christmas-stocking-holders",
        },
        "christmas-stocking-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-stocking-kits/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-needle-art-crafts/christmas-stocking-kits",
        },
        "christmas-stockings": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-stockings-holders/christmas-stockings/",
            "subcategory": "christmas/christmas-decorations/christmas-stockings-holders/christmas-stockings",
        },
        "christmas-stockings-holders": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-stockings-holders/",
            "subcategory": "christmas/christmas-decorations/christmas-stockings-holders",
        },
        "christmas-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-storage/",
            "subcategory": "christmas/christmas-storage",
        },
        "christmas-table-linens-runners": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-table-linens-runners/",
            "subcategory": "christmas/christmas-decorations/christmas-table-linens-runners",
        },
        "christmas-tabletop-accent-trees": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-tabletop-accent-trees/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-tabletop-accent-trees",
        },
        "christmas-tabletop-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-tabletop-decor/",
            "subcategory": "christmas/christmas-decorations/christmas-tabletop-decor",
        },
        "christmas-throws": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-throws/",
            "subcategory": "christmas/christmas-decorations/christmas-throws",
        },
        "christmas-tree-skirts-collars": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-tree-skirts-collars/",
            "subcategory": "christmas/christmas-tree-skirts-collars",
        },
        "christmas-tree-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-storage/christmas-tree-storage/",
            "subcategory": "christmas/christmas-storage/christmas-tree-storage",
        },
        "christmas-tree-toppers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-tree-toppers/",
            "subcategory": "christmas/christmas-decorations/christmas-tree-toppers",
        },
        "christmas-wall-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-wall-decor/",
            "subcategory": "christmas/christmas-decorations/christmas-wall-decor",
        },
        "christmas-washi-tape": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/christmas-washi-tape/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/christmas-washi-tape",
        },
        "christmas-wearables": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-wearables/",
            "subcategory": "christmas/christmas-party-baking/christmas-wearables",
        },
        "christmas-wood-ceramic-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-wood-ceramic-crafts/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-wood-ceramic-crafts",
        },
        "christmas-wrapping-paper-gift-bags": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags",
        },
        "christmas-wreath-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-storage/christmas-wreath-storage/",
            "subcategory": "christmas/christmas-storage/christmas-wreath-storage",
        },
        "christmas-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-wreaths/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-wreaths",
        },
        "christmas-wreaths-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/",
            "subcategory": "christmas/christmas-wreaths-garlands",
        },
        "christmas-yard-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/outdoor-christmas-decorations/christmas-yard-decorations/",
            "subcategory": "christmas/outdoor-christmas-decorations/christmas-yard-decorations",
        },
        "cinco-de-mayo": {
            "url": "https://www.michaels.com/shop/holidays-occasions/cinco-de-mayo/",
            "subcategory": "cinco-de-mayo",
        },
        "collectible-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/collectible-ornaments/",
            "subcategory": "christmas/christmas-ornaments/collectible-ornaments",
        },
        "conjuring-nightfall": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decor-collections/conjuring-nightfall/",
            "subcategory": "halloween/halloween-decor-collections/conjuring-nightfall",
        },
        "containers-vases": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/containers-vases/",
            "subcategory": "summer/summer-floral/containers-vases",
        },
        "day-of-the-dead": {
            "url": "https://www.michaels.com/shop/holidays-occasions/day-of-the-dead/",
            "subcategory": "day-of-the-dead",
        },
        "day-of-the-dead-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/day-of-the-dead/day-of-the-dead-decor/",
            "subcategory": "day-of-the-dead/day-of-the-dead-decor",
        },
        "decor-for-dad": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/decor-for-dad/",
            "subcategory": "fathers-day/decor-for-dad",
        },
        "decor-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-garlands/decor-garlands/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-garlands/decor-garlands",
        },
        "decorated-garland": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-garlands/decorated-garland/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-garlands/decorated-garland",
        },
        "decorated-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-wreaths/decorated-wreaths/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-wreaths/decorated-wreaths",
        },
        "diffusers-essential-oils": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-candles-fragrances/diffusers-essential-oils/",
            "subcategory": "fall/fall-decor-pieces/fall-candles-fragrances/diffusers-essential-oils",
        },
        "diffusers-fragrance": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/diffusers-fragrance/",
            "subcategory": "christmas/christmas-candles-fragrance/diffusers-fragrance",
        },
        "diy-christmas-cards": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/diy-christmas-cards/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/diy-christmas-cards",
        },
        "diy-christmas-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/diy-christmas-ornaments/",
            "subcategory": "christmas/christmas-crafts-diy/diy-christmas-ornaments",
        },
        "diy-craft-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/diy-craft-ornaments/",
            "subcategory": "christmas/christmas-ornaments/diy-craft-ornaments",
        },
        "diy-halloween-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/",
            "subcategory": "halloween/diy-halloween-crafts",
        },
        "diy-wood-ceramic-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/diy-wood-ceramic-crafts/",
            "subcategory": "halloween/diy-halloween-crafts/diy-wood-ceramic-crafts",
        },
        "easter-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-baking/",
            "subcategory": "easter/easter-baking",
        },
        "easter-basket-guide": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-baskets-stuffers/easter-basket-guide/",
            "subcategory": "easter/easter-baskets-stuffers/easter-basket-guide",
        },
        "easter-basket-stuffers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-baskets-stuffers/easter-basket-stuffers/",
            "subcategory": "easter/easter-baskets-stuffers/easter-basket-stuffers",
        },
        "easter-baskets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-baskets-stuffers/easter-baskets/",
            "subcategory": "easter/easter-baskets-stuffers/easter-baskets",
        },
        "easter-baskets-stuffers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-baskets-stuffers/",
            "subcategory": "easter/easter-baskets-stuffers",
        },
        "easter-candy": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-candy/",
            "subcategory": "easter/easter-candy",
        },
        "easter-craft-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-crafts-for-kids/easter-craft-kits/",
            "subcategory": "easter/easter-crafts-for-kids/easter-craft-kits",
        },
        "easter-craft-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-crafts-for-kids/easter-craft-supplies/",
            "subcategory": "easter/easter-crafts-for-kids/easter-craft-supplies",
        },
        "easter-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-crafts/",
            "subcategory": "easter/easter-crafts",
        },
        "easter-crafts-for-kids": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-crafts-for-kids/",
            "subcategory": "easter/easter-crafts-for-kids",
        },
        "easter-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/",
            "subcategory": "easter/easter-decorations",
        },
        "easter-decorative-baskets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/easter-decorative-baskets/",
            "subcategory": "easter/easter-decorations/easter-decorative-baskets",
        },
        "easter-egg-decorating": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-crafts-for-kids/easter-egg-decorating/",
            "subcategory": "easter/easter-crafts-for-kids/easter-egg-decorating",
        },
        "easter-eggs": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-baskets-stuffers/easter-eggs/",
            "subcategory": "easter/easter-baskets-stuffers/easter-eggs",
        },
        "easter-floral-containers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-floral-containers/",
            "subcategory": "easter/easter-floral-containers",
        },
        "easter-grass": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-baskets-stuffers/easter-grass/",
            "subcategory": "easter/easter-baskets-stuffers/easter-grass",
        },
        "easter-lighting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/easter-lighting/",
            "subcategory": "easter/easter-decorations/easter-lighting",
        },
        "easter-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-party-supplies/",
            "subcategory": "easter/easter-party-supplies",
        },
        "easter-pillows-throws": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/easter-pillows-throws/",
            "subcategory": "easter/easter-decorations/easter-pillows-throws",
        },
        "easter-ribbon-bows": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-ribbon-bows/",
            "subcategory": "easter/easter-ribbon-bows",
        },
        "easter-tabletop-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/easter-tabletop-decor/",
            "subcategory": "easter/easter-decorations/easter-tabletop-decor",
        },
        "easter-wall-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/easter-wall-decor/",
            "subcategory": "easter/easter-decorations/easter-wall-decor",
        },
        "easter-wood-ceramic-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-crafts/easter-wood-ceramic-crafts/",
            "subcategory": "easter/easter-crafts/easter-wood-ceramic-crafts",
        },
        "easter-wreaths-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/easter-wreaths-garlands/",
            "subcategory": "easter/easter-decorations/easter-wreaths-garlands",
        },
        "edible-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-baking/edible-decorations/",
            "subcategory": "christmas/christmas-party-baking/christmas-baking/edible-decorations",
        },
        "enchanted-romance": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decor-collections/enchanted-romance/",
            "subcategory": "halloween/halloween-decor-collections/enchanted-romance",
        },
        "entertainer": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/entertainer/",
            "subcategory": "fathers-day/entertainer",
        },
        "exclusive-collectibles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/lemax-christmas-village/exclusive-collectibles/",
            "subcategory": "christmas/lemax-christmas-village/exclusive-collectibles",
        },
        "exclusives": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/lemax-spooky-town-collection/exclusives/",
            "subcategory": "halloween/lemax-spooky-town-collection/exclusives",
        },
        "fall-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-party-baking/fall-baking/",
            "subcategory": "fall/fall-party-baking/fall-baking",
        },
        "fall-baskets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-baskets-containers/fall-baskets/",
            "subcategory": "fall/fall-decor-pieces/fall-baskets-containers/fall-baskets",
        },
        "fall-baskets-containers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-baskets-containers/",
            "subcategory": "fall/fall-decor-pieces/fall-baskets-containers",
        },
        "fall-bowl-filler": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-bowl-filler/",
            "subcategory": "fall/fall-floral/fall-bowl-filler",
        },
        "fall-bushes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-stems-bushes-picks/fall-bushes/",
            "subcategory": "fall/fall-floral/fall-stems-bushes-picks/fall-bushes",
        },
        "fall-candle-holders": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-candles-fragrances/fall-candle-holders/",
            "subcategory": "fall/fall-decor-pieces/fall-candles-fragrances/fall-candle-holders",
        },
        "fall-candles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-candles-fragrances/fall-candles/",
            "subcategory": "fall/fall-decor-pieces/fall-candles-fragrances/fall-candles",
        },
        "fall-candles-fragrances": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-candles-fragrances/",
            "subcategory": "fall/fall-decor-pieces/fall-candles-fragrances",
        },
        "fall-containers-vases": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-containers-vases/",
            "subcategory": "fall/fall-floral/fall-containers-vases",
        },
        "fall-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-crafting/",
            "subcategory": "fall/fall-crafting",
        },
        "fall-cross-stitch": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-crafting/fall-cross-stitch/",
            "subcategory": "fall/fall-crafting/fall-cross-stitch",
        },
        "fall-decor-collections": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-collections/",
            "subcategory": "fall/fall-decor-collections",
        },
        "fall-decor-pieces": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/",
            "subcategory": "fall/fall-decor-pieces",
        },
        "fall-decorative-boxes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-baskets-containers/fall-decorative-boxes/",
            "subcategory": "fall/fall-decor-pieces/fall-baskets-containers/fall-decorative-boxes",
        },
        "fall-diamond-art": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-crafting/fall-diamond-art/",
            "subcategory": "fall/fall-crafting/fall-diamond-art",
        },
        "fall-doormats": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-doormats/",
            "subcategory": "fall/fall-decor-pieces/fall-doormats",
        },
        "fall-entertaining": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-collections/fall-entertaining/",
            "subcategory": "fall/fall-decor-collections/fall-entertaining",
        },
        "fall-essentials": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-collections/fall-essentials/",
            "subcategory": "fall/fall-decor-collections/fall-essentials",
        },
        "fall-flags": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-outdoor-decor/fall-flags/",
            "subcategory": "fall/fall-outdoor-decor/fall-flags",
        },
        "fall-floral": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/",
            "subcategory": "fall/fall-floral",
        },
        "fall-floral-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-floral-accessories/",
            "subcategory": "fall/fall-floral/fall-floral-accessories",
        },
        "fall-floral-arrangements": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-floral-arrangements/",
            "subcategory": "fall/fall-floral/fall-floral-arrangements",
        },
        "fall-floral-stems": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-stems-bushes-picks/fall-floral-stems/",
            "subcategory": "fall/fall-floral/fall-stems-bushes-picks/fall-floral-stems",
        },
        "fall-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-garlands/",
            "subcategory": "fall/fall-floral/fall-garlands",
        },
        "fall-inflatables": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-outdoor-decor/fall-inflatables/",
            "subcategory": "fall/fall-outdoor-decor/fall-inflatables",
        },
        "fall-lighting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-candles-fragrances/fall-lighting/",
            "subcategory": "fall/fall-decor-pieces/fall-candles-fragrances/fall-lighting",
        },
        "fall-memorial-flowers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-memorial-flowers/",
            "subcategory": "fall/fall-floral/fall-memorial-flowers",
        },
        "fall-miniatures": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-crafting/fall-miniatures/",
            "subcategory": "fall/fall-crafting/fall-miniatures",
        },
        "fall-outdoor-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-outdoor-decor/",
            "subcategory": "fall/fall-outdoor-decor",
        },
        "fall-pampas-grass": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-pampas-grass/",
            "subcategory": "fall/fall-floral/fall-pampas-grass",
        },
        "fall-party-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-party-baking/",
            "subcategory": "fall/fall-party-baking",
        },
        "fall-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-party-baking/fall-party-supplies/",
            "subcategory": "fall/fall-party-baking/fall-party-supplies",
        },
        "fall-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-stems-bushes-picks/fall-picks/",
            "subcategory": "fall/fall-floral/fall-stems-bushes-picks/fall-picks",
        },
        "fall-pillows-blankets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-pillows-blankets/",
            "subcategory": "fall/fall-decor-pieces/fall-pillows-blankets",
        },
        "fall-porch-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-outdoor-decor/fall-porch-decor/",
            "subcategory": "fall/fall-outdoor-decor/fall-porch-decor",
        },
        "fall-potted-plants": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-trees-potted-plants/fall-potted-plants/",
            "subcategory": "fall/fall-floral/fall-trees-potted-plants/fall-potted-plants",
        },
        "fall-ribbon": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-ribbon/",
            "subcategory": "fall/fall-ribbon",
        },
        "fall-stem-bundles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-stem-bundles/",
            "subcategory": "fall/fall-floral/fall-stem-bundles",
        },
        "fall-stems-bushes-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-stems-bushes-picks/",
            "subcategory": "fall/fall-floral/fall-stems-bushes-picks",
        },
        "fall-tabletop-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-tabletop-decor/",
            "subcategory": "fall/fall-decor-pieces/fall-tabletop-decor",
        },
        "fall-trees": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-trees-potted-plants/fall-trees/",
            "subcategory": "fall/fall-floral/fall-trees-potted-plants/fall-trees",
        },
        "fall-trees-potted-plants": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-trees-potted-plants/",
            "subcategory": "fall/fall-floral/fall-trees-potted-plants",
        },
        "fall-wall-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-wall-decor/",
            "subcategory": "fall/fall-decor-pieces/fall-wall-decor",
        },
        "fall-wax-melts-scents": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/fall-candles-fragrances/fall-wax-melts-scents/",
            "subcategory": "fall/fall-decor-pieces/fall-candles-fragrances/fall-wax-melts-scents",
        },
        "fall-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-floral/fall-wreaths/",
            "subcategory": "fall/fall-floral/fall-wreaths",
        },
        "fall-yardstakes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-outdoor-decor/fall-yardstakes/",
            "subcategory": "fall/fall-outdoor-decor/fall-yardstakes",
        },
        "fathers-day": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/",
            "subcategory": "fathers-day",
        },
        "finial-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/finial-ornaments/",
            "subcategory": "christmas/christmas-ornaments/finial-ornaments",
        },
        "flags-bunting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/flags-bunting/",
            "subcategory": "red-white-blue/flags-bunting",
        },
        "flameless-led-candles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/flameless-led-candles/",
            "subcategory": "christmas/christmas-candles-fragrance/flameless-led-candles",
        },
        "floral-containers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/floral-containers/",
            "subcategory": "spring/spring-floral/floral-containers",
        },
        "floral-decor-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/floral-decor-gifts/",
            "subcategory": "mothers-day/floral-decor-gifts",
        },
        "foodie-dad": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/foodie-dad/",
            "subcategory": "fathers-day/foodie-dad",
        },
        "football-season-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/football-season-decor/",
            "subcategory": "thanksgiving/football-season-decor",
        },
        "front-door-christmas-floral-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/outdoor-christmas-decorations/front-door-christmas-floral-decor/",
            "subcategory": "christmas/outdoor-christmas-decorations/front-door-christmas-floral-decor",
        },
        "frosted-fairytale": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/frosted-fairytale/",
            "subcategory": "christmas/christmas-decor-collections/frosted-fairytale",
        },
        "galentines-day": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/galentines-day/",
            "subcategory": "valentines-day/galentines-day",
        },
        "garlands-with-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-garlands/garlands-with-lights/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-garlands/garlands-with-lights",
        },
        "gift-bags": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/gift-bags/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags/gift-bags",
        },
        "gifts-for-grandma": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/gifts-for-grandma/",
            "subcategory": "mothers-day/gifts-for-grandma",
        },
        "gifts-for-mom": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/gifts-for-mom/",
            "subcategory": "mothers-day/gifts-for-mom",
        },
        "gingerbread-forest": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/gingerbread-forest/",
            "subcategory": "christmas/christmas-decor-collections/gingerbread-forest",
        },
        "glass-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/glass-ornaments/",
            "subcategory": "christmas/christmas-ornaments/glass-ornaments",
        },
        "gracious-gathering": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-collections/gracious-gathering/",
            "subcategory": "fall/fall-decor-collections/gracious-gathering",
        },
        "grad-cap-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/crafting/grad-cap-supplies/",
            "subcategory": "graduation/crafting/grad-cap-supplies",
        },
        "graduation": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/",
            "subcategory": "graduation",
        },
        "graduation-paper": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/crafting/graduation-paper/",
            "subcategory": "graduation/crafting/graduation-paper",
        },
        "greenery-mats": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/greenery-mats/",
            "subcategory": "spring/spring-greenery/greenery-mats",
        },
        "hallowed-halls": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decor-collections/hallowed-halls/",
            "subcategory": "halloween/halloween-decor-collections/hallowed-halls",
        },
        "halloween-animatronics": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-animatronics/",
            "subcategory": "halloween/halloween-animatronics",
        },
        "halloween-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-baking-party/halloween-baking/",
            "subcategory": "halloween/halloween-baking-party/halloween-baking",
        },
        "halloween-baking-party": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-baking-party/",
            "subcategory": "halloween/halloween-baking-party",
        },
        "halloween-bushes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-stems-bushes-picks/halloween-bushes/",
            "subcategory": "halloween/halloween-floral/halloween-stems-bushes-picks/halloween-bushes",
        },
        "halloween-cafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-crafts-for-kids/halloween-cafts/",
            "subcategory": "halloween/halloween-crafts-for-kids/halloween-cafts",
        },
        "halloween-candles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-candles/",
            "subcategory": "halloween/halloween-decorations/halloween-candles",
        },
        "halloween-candy": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-candy/",
            "subcategory": "halloween/halloween-candy",
        },
        "halloween-canvas-painting-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/halloween-canvas-painting-kits/",
            "subcategory": "halloween/diy-halloween-crafts/halloween-canvas-painting-kits",
        },
        "halloween-costumes-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-costumes-accessories/",
            "subcategory": "halloween/halloween-costumes-accessories",
        },
        "halloween-crafts-for-kids": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-crafts-for-kids/",
            "subcategory": "halloween/halloween-crafts-for-kids",
        },
        "halloween-decor-collections": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decor-collections/",
            "subcategory": "halloween/halloween-decor-collections",
        },
        "halloween-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/",
            "subcategory": "halloween/halloween-decorations",
        },
        "halloween-diamond-art": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/halloween-diamond-art/",
            "subcategory": "halloween/diy-halloween-crafts/halloween-diamond-art",
        },
        "halloween-diorama-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/halloween-diorama-kits/",
            "subcategory": "halloween/diy-halloween-crafts/halloween-diorama-kits",
        },
        "halloween-doormats": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/outdoor-halloween-decorations/halloween-doormats/",
            "subcategory": "halloween/outdoor-halloween-decorations/halloween-doormats",
        },
        "halloween-fillers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-fillers/",
            "subcategory": "halloween/halloween-floral/halloween-fillers",
        },
        "halloween-flags": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/outdoor-halloween-decorations/halloween-flags/",
            "subcategory": "halloween/outdoor-halloween-decorations/halloween-flags",
        },
        "halloween-floral": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/",
            "subcategory": "halloween/halloween-floral",
        },
        "halloween-floral-arrangements": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-floral-arrangements/",
            "subcategory": "halloween/halloween-floral/halloween-floral-arrangements",
        },
        "halloween-floral-bundles-bouquets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-floral-bundles-bouquets/",
            "subcategory": "halloween/halloween-floral/halloween-floral-bundles-bouquets",
        },
        "halloween-garland": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-garland/",
            "subcategory": "halloween/halloween-decorations/halloween-garland",
        },
        "halloween-inflatables": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-inflatables/",
            "subcategory": "halloween/halloween-inflatables",
        },
        "halloween-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-lights/",
            "subcategory": "halloween/halloween-decorations/halloween-lights",
        },
        "halloween-miniatures": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/halloween-miniatures/",
            "subcategory": "halloween/diy-halloween-crafts/halloween-miniatures",
        },
        "halloween-needlework": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/halloween-needlework/",
            "subcategory": "halloween/diy-halloween-crafts/halloween-needlework",
        },
        "halloween-paint-by-number": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/halloween-paint-by-number/",
            "subcategory": "halloween/diy-halloween-crafts/halloween-paint-by-number",
        },
        "halloween-papercrafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/halloween-papercrafting/",
            "subcategory": "halloween/diy-halloween-crafts/halloween-papercrafting",
        },
        "halloween-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-baking-party/halloween-party-supplies/",
            "subcategory": "halloween/halloween-baking-party/halloween-party-supplies",
        },
        "halloween-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-stems-bushes-picks/halloween-picks/",
            "subcategory": "halloween/halloween-floral/halloween-stems-bushes-picks/halloween-picks",
        },
        "halloween-pillows-blankets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-pillows-blankets/",
            "subcategory": "halloween/halloween-decorations/halloween-pillows-blankets",
        },
        "halloween-porch-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/outdoor-halloween-decorations/halloween-porch-decor/",
            "subcategory": "halloween/outdoor-halloween-decorations/halloween-porch-decor",
        },
        "halloween-props": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-props/",
            "subcategory": "halloween/halloween-decorations/halloween-props",
        },
        "halloween-ribbon": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-ribbon/",
            "subcategory": "halloween/halloween-ribbon",
        },
        "halloween-statues": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/outdoor-halloween-decorations/halloween-statues/",
            "subcategory": "halloween/outdoor-halloween-decorations/halloween-statues",
        },
        "halloween-stems": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-stems-bushes-picks/halloween-stems/",
            "subcategory": "halloween/halloween-floral/halloween-stems-bushes-picks/halloween-stems",
        },
        "halloween-stems-bushes-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-stems-bushes-picks/",
            "subcategory": "halloween/halloween-floral/halloween-stems-bushes-picks",
        },
        "halloween-t-shirts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-t-shirts/",
            "subcategory": "halloween/halloween-t-shirts",
        },
        "halloween-tabletop-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-tabletop-decor/",
            "subcategory": "halloween/halloween-decorations/halloween-tabletop-decor",
        },
        "halloween-trees-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-trees-ornaments/",
            "subcategory": "halloween/halloween-decorations/halloween-trees-ornaments",
        },
        "halloween-vases-containers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-vases-containers/",
            "subcategory": "halloween/halloween-floral/halloween-vases-containers",
        },
        "halloween-wall-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-wall-decor/",
            "subcategory": "halloween/halloween-decorations/halloween-wall-decor",
        },
        "halloween-wreaths-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/halloween-wreaths-garlands/",
            "subcategory": "halloween/halloween-floral/halloween-wreaths-garlands",
        },
        "halloween-yardstakes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/outdoor-halloween-decorations/halloween-yardstakes/",
            "subcategory": "halloween/outdoor-halloween-decorations/halloween-yardstakes",
        },
        "hand-made-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/hand-made-gifts/",
            "subcategory": "mothers-day/hand-made-gifts",
        },
        "handmade-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/handmade-gifts/",
            "subcategory": "fathers-day/handmade-gifts",
        },
        "hanging-figurines": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/hanging-figurines/",
            "subcategory": "christmas/christmas-ornaments/hanging-figurines",
        },
        "hanukkah": {
            "url": "https://www.michaels.com/shop/holidays-occasions/hanukkah/",
            "subcategory": "hanukkah",
        },
        "hanukkah-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/hanukkah/hanukkah-decor/",
            "subcategory": "hanukkah/hanukkah-decor",
        },
        "heritage-hideaway": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-collections/heritage-hideaway/",
            "subcategory": "fall/fall-decor-collections/heritage-hideaway",
        },
        "hispanic-heritage-month": {
            "url": "https://www.michaels.com/shop/holidays-occasions/hispanic-heritage-month/",
            "subcategory": "hispanic-heritage-month",
        },
        "holiday-jewelry-making": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/holiday-jewelry-making/",
            "subcategory": "christmas/christmas-crafts-diy/holiday-jewelry-making",
        },
        "holiday-table-frames": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/holiday-frames/holiday-table-frames/",
            "subcategory": "christmas/holiday-frames/holiday-table-frames",
        },
        "holiday-tidings": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/holiday-tidings/",
            "subcategory": "christmas/christmas-decor-collections/holiday-tidings",
        },
        "holidays-occasions": {
            "url": "https://www.michaels.com/shop/holidays-occasions/",
            "subcategory": "holidays-occasions",
        },
        "holidays-occasions-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/lemax-spooky-town-collection/accessories/",
            "subcategory": "halloween/lemax-spooky-town-collection/accessories",
        },
        "holidays-occasions-accessories-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/lemax-christmas-village/accessories/",
            "subcategory": "christmas/lemax-christmas-village/accessories",
        },
        "holidays-occasions-area-rugs": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/rugs-doormats/area-rugs/",
            "subcategory": "summer/outdoor-living/rugs-doormats/area-rugs",
        },
        "holidays-occasions-art-gift-sets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/art-gift-sets/",
            "subcategory": "mothers-day/art-gift-sets",
        },
        "holidays-occasions-art-gift-sets-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/art-gift-sets/",
            "subcategory": "fathers-day/art-gift-sets",
        },
        "holidays-occasions-baskets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-baskets-storage/baskets/",
            "subcategory": "summer/summer-baskets-storage/baskets",
        },
        "holidays-occasions-black-history-month": {
            "url": "https://www.michaels.com/shop/holidays-occasions/black-history-month/",
            "subcategory": "black-history-month",
        },
        "holidays-occasions-blank-cards": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/diy-christmas-cards/blank-cards/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/diy-christmas-cards/blank-cards",
        },
        "holidays-occasions-bows": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ribbon-trimming/bows/",
            "subcategory": "christmas/christmas-ribbon-trimming/bows",
        },
        "holidays-occasions-bubbles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-toys-games/bubbles/",
            "subcategory": "summer/kids-summer-toys-games/bubbles",
        },
        "holidays-occasions-bushes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/spring-stems-bushes-picks/bushes/",
            "subcategory": "spring/spring-floral/spring-stems-bushes-picks/bushes",
        },
        "holidays-occasions-bushes-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/bushes/",
            "subcategory": "spring/spring-greenery/bushes",
        },
        "holidays-occasions-candle-holders": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-candles/candle-holders/",
            "subcategory": "halloween/halloween-decorations/halloween-candles/candle-holders",
        },
        "holidays-occasions-candle-holders-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/candles-fragrances/candle-holders/",
            "subcategory": "summer/summer-decor/candles-fragrances/candle-holders",
        },
        "holidays-occasions-candles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/candles/",
            "subcategory": "mothers-day/candles",
        },
        "holidays-occasions-candles-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/candles/",
            "subcategory": "christmas/christmas-candles-fragrance/candles",
        },
        "holidays-occasions-candles-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-candles/candles/",
            "subcategory": "halloween/halloween-decorations/halloween-candles/candles",
        },
        "holidays-occasions-candles-fragrances": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/candles-fragrances/",
            "subcategory": "summer/summer-decor/candles-fragrances",
        },
        "holidays-occasions-card-making": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/card-making/",
            "subcategory": "mothers-day/card-making",
        },
        "holidays-occasions-card-making-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/card-making/",
            "subcategory": "fathers-day/card-making",
        },
        "holidays-occasions-christmas": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/",
            "subcategory": "christmas",
        },
        "holidays-occasions-christmas-trees": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas-trees/",
            "subcategory": "christmas-trees",
        },
        "holidays-occasions-christmas-trees-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-trees/",
            "subcategory": "christmas/christmas-trees",
        },
        "holidays-occasions-craft-pumpkins": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/pumpkins/craft-pumpkins/",
            "subcategory": "fall/pumpkins/craft-pumpkins",
        },
        "holidays-occasions-craft-pumpkins-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/pumpkin-decor/craft-pumpkins/",
            "subcategory": "halloween/pumpkin-decor/craft-pumpkins",
        },
        "holidays-occasions-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/crafting/",
            "subcategory": "red-white-blue/crafting",
        },
        "holidays-occasions-crafting-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/crafting/",
            "subcategory": "st-patricks-day/crafting",
        },
        "holidays-occasions-crafting-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/crafting/",
            "subcategory": "graduation/crafting",
        },
        "holidays-occasions-crafting-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/crafting/",
            "subcategory": "pride/crafting",
        },
        "holidays-occasions-crafting-5": {
            "url": "https://www.michaels.com/shop/holidays-occasions/day-of-the-dead/crafting/",
            "subcategory": "day-of-the-dead/crafting",
        },
        "holidays-occasions-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/decor/",
            "subcategory": "red-white-blue/decor",
        },
        "holidays-occasions-decor-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mardi-gras/decor/",
            "subcategory": "mardi-gras/decor",
        },
        "holidays-occasions-decor-pumpkins": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/pumpkin-decor/decor-pumpkins/",
            "subcategory": "halloween/pumpkin-decor/decor-pumpkins",
        },
        "holidays-occasions-decor-pumpkins-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/pumpkins/decor-pumpkins/",
            "subcategory": "fall/pumpkins/decor-pumpkins",
        },
        "holidays-occasions-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/decorations/",
            "subcategory": "st-patricks-day/decorations",
        },
        "holidays-occasions-decorations-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/new-years-eve/decorations/",
            "subcategory": "new-years-eve/decorations",
        },
        "holidays-occasions-decorations-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/decorations/",
            "subcategory": "pride/decorations",
        },
        "holidays-occasions-decorative-boxes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-baskets-storage/decorative-boxes/",
            "subcategory": "summer/summer-baskets-storage/decorative-boxes",
        },
        "holidays-occasions-decorative-boxes-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-baskets-containers/decorative-boxes/",
            "subcategory": "spring/spring-baskets-containers/decorative-boxes",
        },
        "holidays-occasions-diamond-painting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-crafts/diamond-painting/",
            "subcategory": "easter/easter-crafts/diamond-painting",
        },
        "holidays-occasions-doormats": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-outdoor-decor/doormats/",
            "subcategory": "fall/fall-outdoor-decor/doormats",
        },
        "holidays-occasions-doormats-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-porch-yard-decor/doormats/",
            "subcategory": "spring/spring-porch-yard-decor/doormats",
        },
        "holidays-occasions-doormats-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/rugs-doormats/doormats/",
            "subcategory": "summer/outdoor-living/rugs-doormats/doormats",
        },
        "holidays-occasions-dried-floral": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/dried-floral/",
            "subcategory": "spring/spring-floral/dried-floral",
        },
        "holidays-occasions-easter": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/",
            "subcategory": "easter",
        },
        "holidays-occasions-fall": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/",
            "subcategory": "fall",
        },
        "holidays-occasions-figurines": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/lemax-christmas-village/figurines/",
            "subcategory": "christmas/lemax-christmas-village/figurines",
        },
        "holidays-occasions-figurines-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/lemax-spooky-town-collection/figurines/",
            "subcategory": "halloween/lemax-spooky-town-collection/figurines",
        },
        "holidays-occasions-floral": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/floral/",
            "subcategory": "red-white-blue/floral",
        },
        "holidays-occasions-floral-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/floral/",
            "subcategory": "st-patricks-day/floral",
        },
        "holidays-occasions-floral-arrangements": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/floral-arrangements/",
            "subcategory": "summer/summer-floral/floral-arrangements",
        },
        "holidays-occasions-floral-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/floral-supplies/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/floral-supplies",
        },
        "holidays-occasions-floral-supplies-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-floral/floral-supplies/",
            "subcategory": "halloween/halloween-floral/floral-supplies",
        },
        "holidays-occasions-frames": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/frames/",
            "subcategory": "graduation/frames",
        },
        "holidays-occasions-frames-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/frames/",
            "subcategory": "fathers-day/frames",
        },
        "holidays-occasions-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/garlands/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/garlands",
        },
        "holidays-occasions-garlands-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/garlands/",
            "subcategory": "spring/spring-wreaths-garlands/garlands",
        },
        "holidays-occasions-gift-boxes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/gift-boxes/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags/gift-boxes",
        },
        "holidays-occasions-gift-ribbon-bows": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/gift-ribbon-bows/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags/gift-ribbon-bows",
        },
        "holidays-occasions-greenery-arrangements": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/greenery-arrangements/",
            "subcategory": "spring/spring-greenery/greenery-arrangements",
        },
        "holidays-occasions-halloween": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/",
            "subcategory": "halloween",
        },
        "holidays-occasions-hay-bales": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/hay-bales/",
            "subcategory": "fall/fall-decor-pieces/hay-bales",
        },
        "holidays-occasions-hay-bales-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-outdoor-decor/hay-bales/",
            "subcategory": "fall/fall-outdoor-decor/hay-bales",
        },
        "holidays-occasions-holiday-frames": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/holiday-frames/",
            "subcategory": "christmas/holiday-frames",
        },
        "holidays-occasions-jar-candles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/jar-candles/",
            "subcategory": "christmas/christmas-candles-fragrance/jar-candles",
        },
        "holidays-occasions-jar-candles-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/candles-fragrances/jar-candles/",
            "subcategory": "summer/summer-decor/candles-fragrances/jar-candles",
        },
        "holidays-occasions-jewelry": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/jewelry/",
            "subcategory": "easter/jewelry",
        },
        "holidays-occasions-jewelry-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/jewelry/",
            "subcategory": "st-patricks-day/jewelry",
        },
        "holidays-occasions-jewelry-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/jewelry/",
            "subcategory": "mothers-day/jewelry",
        },
        "holidays-occasions-jewelry-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/jewelry/",
            "subcategory": "pride/jewelry",
        },
        "holidays-occasions-kids-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/kids-crafting/",
            "subcategory": "red-white-blue/kids-crafting",
        },
        "holidays-occasions-lanterns": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/candles-fragrances/lanterns/",
            "subcategory": "summer/summer-decor/candles-fragrances/lanterns",
        },
        "holidays-occasions-lanterns-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-candles/lanterns/",
            "subcategory": "halloween/halloween-decorations/halloween-candles/lanterns",
        },
        "holidays-occasions-lanterns-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-candles-fragrance/lanterns/",
            "subcategory": "christmas/christmas-candles-fragrance/lanterns",
        },
        "holidays-occasions-lanterns-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/lanterns/",
            "subcategory": "christmas/christmas-lights/lanterns",
        },
        "holidays-occasions-lemax-christmas-village": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/lemax-christmas-village/",
            "subcategory": "christmas/lemax-christmas-village",
        },
        "holidays-occasions-lighting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/decorations/lighting/",
            "subcategory": "st-patricks-day/decorations/lighting",
        },
        "holidays-occasions-memorial": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/memorial/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/memorial",
        },
        "holidays-occasions-miniature-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/miniature-kits/",
            "subcategory": "mothers-day/miniature-kits",
        },
        "holidays-occasions-outdoor-christmas-greenery": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/outdoor-christmas-greenery/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/outdoor-christmas-greenery",
        },
        "holidays-occasions-outdoor-christmas-greenery-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/outdoor-christmas-decorations/outdoor-christmas-greenery/",
            "subcategory": "christmas/outdoor-christmas-decorations/outdoor-christmas-greenery",
        },
        "holidays-occasions-outdoor-christmas-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/outdoor-christmas-decorations/outdoor-christmas-lights/",
            "subcategory": "christmas/outdoor-christmas-decorations/outdoor-christmas-lights",
        },
        "holidays-occasions-outdoor-christmas-lights-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/outdoor-christmas-lights/",
            "subcategory": "christmas/christmas-lights/outdoor-christmas-lights",
        },
        "holidays-occasions-outdoor-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-decor/outdoor-decor/",
            "subcategory": "thanksgiving/thanksgiving-decor/outdoor-decor",
        },
        "holidays-occasions-outdoor-decor-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/outdoor-decor/",
            "subcategory": "summer/outdoor-living/outdoor-decor",
        },
        "holidays-occasions-outdoor-furniture": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/outdoor-furniture/",
            "subcategory": "summer/outdoor-living/outdoor-furniture",
        },
        "holidays-occasions-party": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/party/",
            "subcategory": "red-white-blue/party",
        },
        "holidays-occasions-party-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/party/",
            "subcategory": "graduation/party",
        },
        "holidays-occasions-party-favors": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/party-favors/",
            "subcategory": "christmas/christmas-party-baking/party-favors",
        },
        "holidays-occasions-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/hanukkah/party-supplies/",
            "subcategory": "hanukkah/party-supplies",
        },
        "holidays-occasions-party-supplies-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/day-of-the-dead/party-supplies/",
            "subcategory": "day-of-the-dead/party-supplies",
        },
        "holidays-occasions-party-supplies-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/new-years-eve/party-supplies/",
            "subcategory": "new-years-eve/party-supplies",
        },
        "holidays-occasions-party-supplies-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-party/party-supplies/",
            "subcategory": "summer/summer-party/party-supplies",
        },
        "holidays-occasions-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/spring-stems-bushes-picks/picks/",
            "subcategory": "spring/spring-floral/spring-stems-bushes-picks/picks",
        },
        "holidays-occasions-picks-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/picks/",
            "subcategory": "spring/spring-greenery/picks",
        },
        "holidays-occasions-pillows-throws": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/decorations/pillows-throws/",
            "subcategory": "st-patricks-day/decorations/pillows-throws",
        },
        "holidays-occasions-pillows-throws-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-decor/pillows-throws/",
            "subcategory": "thanksgiving/thanksgiving-decor/pillows-throws",
        },
        "holidays-occasions-porch-signs": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-porch-yard-decor/porch-signs/",
            "subcategory": "spring/spring-porch-yard-decor/porch-signs",
        },
        "holidays-occasions-potted-plants": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/potted-plants/",
            "subcategory": "spring/spring-floral/potted-plants",
        },
        "holidays-occasions-potted-plants-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/potted-plants/",
            "subcategory": "summer/summer-floral/potted-plants",
        },
        "holidays-occasions-potted-plants-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/potted-plants/",
            "subcategory": "spring/spring-greenery/potted-plants",
        },
        "holidays-occasions-power-tools": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/power-tools/",
            "subcategory": "fathers-day/power-tools",
        },
        "holidays-occasions-ramadan": {
            "url": "https://www.michaels.com/shop/holidays-occasions/ramadan/",
            "subcategory": "ramadan",
        },
        "holidays-occasions-ribbon": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ribbon-trimming/ribbon/",
            "subcategory": "christmas/christmas-ribbon-trimming/ribbon",
        },
        "holidays-occasions-ribbon-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/ribbon/",
            "subcategory": "red-white-blue/ribbon",
        },
        "holidays-occasions-ribbon-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/ribbon/",
            "subcategory": "pride/ribbon",
        },
        "holidays-occasions-ribbon-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/ribbon/",
            "subcategory": "st-patricks-day/ribbon",
        },
        "holidays-occasions-sand-water-toys": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-toys-games/sand-water-toys/",
            "subcategory": "summer/kids-summer-toys-games/sand-water-toys",
        },
        "holidays-occasions-shadow-boxes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/shadow-boxes/",
            "subcategory": "fathers-day/shadow-boxes",
        },
        "holidays-occasions-specialty-ribbon": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ribbon-trimming/ribbon/specialty-ribbon/",
            "subcategory": "christmas/christmas-ribbon-trimming/ribbon/specialty-ribbon",
        },
        "holidays-occasions-st-patricks-day": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/",
            "subcategory": "st-patricks-day",
        },
        "holidays-occasions-statues": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-porch-yard-decor/statues/",
            "subcategory": "spring/spring-porch-yard-decor/statues",
        },
        "holidays-occasions-stepping-stone-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/stepping-stone-kits/",
            "subcategory": "mothers-day/stepping-stone-kits",
        },
        "holidays-occasions-stickers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/stickers/",
            "subcategory": "pride/stickers",
        },
        "holidays-occasions-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-baskets-containers/storage/",
            "subcategory": "spring/spring-baskets-containers/storage",
        },
        "holidays-occasions-string-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/string-lights/",
            "subcategory": "christmas/christmas-lights/string-lights",
        },
        "holidays-occasions-string-lights-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-lights/string-lights/",
            "subcategory": "halloween/halloween-decorations/halloween-lights/string-lights",
        },
        "holidays-occasions-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/supplies/",
            "subcategory": "spring/spring-floral/supplies",
        },
        "holidays-occasions-t-shirts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/t-shirts/",
            "subcategory": "pride/t-shirts",
        },
        "holidays-occasions-table-accents": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/lemax-spooky-town-collection/table-accents/",
            "subcategory": "halloween/lemax-spooky-town-collection/table-accents",
        },
        "holidays-occasions-table-accents-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/lemax-christmas-village/table-accents/",
            "subcategory": "christmas/lemax-christmas-village/table-accents",
        },
        "holidays-occasions-tabletop-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-collections/boho-coast/tabletop-decor/",
            "subcategory": "spring/spring-decor-collections/boho-coast/tabletop-decor",
        },
        "holidays-occasions-tabletop-decor-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-collections/home-work/tabletop-decor/",
            "subcategory": "spring/spring-decor-collections/home-work/tabletop-decor",
        },
        "holidays-occasions-tabletop-decor-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/decor/tabletop-decor/",
            "subcategory": "red-white-blue/decor/tabletop-decor",
        },
        "holidays-occasions-tabletop-decor-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-decor/tabletop-decor/",
            "subcategory": "thanksgiving/thanksgiving-decor/tabletop-decor",
        },
        "holidays-occasions-tabletop-decor-5": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/tabletop-decor/",
            "subcategory": "summer/summer-decor/tabletop-decor",
        },
        "holidays-occasions-tableware": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-party/tableware/",
            "subcategory": "summer/summer-party/tableware",
        },
        "holidays-occasions-tableware-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/tableware/",
            "subcategory": "pride/tableware",
        },
        "holidays-occasions-tags": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/tags/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags/tags",
        },
        "holidays-occasions-tech-crafting-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/tech-crafting-gifts/",
            "subcategory": "fathers-day/tech-crafting-gifts",
        },
        "holidays-occasions-tech-crafting-gifts-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/tech-crafting-gifts/",
            "subcategory": "mothers-day/tech-crafting-gifts",
        },
        "holidays-occasions-trees-floor-plants": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/trees-floor-plants/",
            "subcategory": "summer/summer-floral/trees-floor-plants",
        },
        "holidays-occasions-trim": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ribbon-trimming/ribbon/trim/",
            "subcategory": "christmas/christmas-ribbon-trimming/ribbon/trim",
        },
        "holidays-occasions-valentines-day": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/",
            "subcategory": "valentines-day",
        },
        "holidays-occasions-wall-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-decor/wall-decor/",
            "subcategory": "thanksgiving/thanksgiving-decor/wall-decor",
        },
        "holidays-occasions-wall-decor-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-floral-arrangements/wall-decor/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-floral-arrangements/wall-decor",
        },
        "holidays-occasions-wall-decor-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/wall-decor/",
            "subcategory": "summer/summer-decor/wall-decor",
        },
        "holidays-occasions-wall-decor-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/decor/wall-decor/",
            "subcategory": "red-white-blue/decor/wall-decor",
        },
        "holidays-occasions-wall-decor-5": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/decorations/wall-decor/",
            "subcategory": "st-patricks-day/decorations/wall-decor",
        },
        "holidays-occasions-wearables": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/wearables/",
            "subcategory": "st-patricks-day/wearables",
        },
        "holidays-occasions-wearables-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/day-of-the-dead/wearables/",
            "subcategory": "day-of-the-dead/wearables",
        },
        "holidays-occasions-wearables-3": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/wearables/",
            "subcategory": "red-white-blue/wearables",
        },
        "holidays-occasions-wearables-4": {
            "url": "https://www.michaels.com/shop/holidays-occasions/new-years-eve/wearables/",
            "subcategory": "new-years-eve/wearables",
        },
        "holidays-occasions-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/wreaths/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/wreaths",
        },
        "holidays-occasions-wreaths-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/wreaths/",
            "subcategory": "spring/spring-wreaths-garlands/wreaths",
        },
        "holidays-occasions-wreaths-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/wreaths-garlands/",
            "subcategory": "spring/spring-greenery/wreaths-garlands",
        },
        "holidays-occasions-wreaths-garlands-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/wreaths-garlands/",
            "subcategory": "halloween/wreaths-garlands",
        },
        "hooks-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/hooks-accessories/",
            "subcategory": "christmas/christmas-ornaments/hooks-accessories",
        },
        "icicle-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/icicle-lights/",
            "subcategory": "christmas/christmas-lights/icicle-lights",
        },
        "intentional-abundance": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-collections/intentional-abundance/",
            "subcategory": "fall/fall-decor-collections/intentional-abundance",
        },
        "jolly-jewels": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/jolly-jewels/",
            "subcategory": "christmas/christmas-decor-collections/jolly-jewels",
        },
        "kids-art": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/kids-christmas-crafting/kids-art/",
            "subcategory": "christmas/christmas-crafts-diy/kids-christmas-crafting/kids-art",
        },
        "kids-christmas-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/kids-christmas-crafting/",
            "subcategory": "christmas/christmas-crafts-diy/kids-christmas-crafting",
        },
        "kids-craft-kits-2": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/kids-christmas-crafting/kids-craft-kits/",
            "subcategory": "christmas/christmas-crafts-diy/kids-christmas-crafting/kids-craft-kits",
        },
        "kids-crafting-basics": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/kids-christmas-crafting/kids-crafting-basics/",
            "subcategory": "christmas/christmas-crafts-diy/kids-christmas-crafting/kids-crafting-basics",
        },
        "kids-fall-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-crafting/kids-fall-crafts/",
            "subcategory": "fall/fall-crafting/kids-fall-crafts",
        },
        "kids-spring-crafts-activities": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/kids-spring-crafts-activities/",
            "subcategory": "spring/kids-spring-crafts-activities",
        },
        "kids-summer-craft-activities": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-craft-activities/",
            "subcategory": "summer/kids-summer-craft-activities",
        },
        "kids-summer-craft-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-craft-activities/kids-summer-craft-kits/",
            "subcategory": "summer/kids-summer-craft-activities/kids-summer-craft-kits",
        },
        "kids-summer-jewelry": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-craft-activities/kids-summer-jewelry/",
            "subcategory": "summer/kids-summer-craft-activities/kids-summer-jewelry",
        },
        "kids-summer-toys-games": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-toys-games/",
            "subcategory": "summer/kids-summer-toys-games",
        },
        "kids-thanksgiving-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/kids-thanksgiving-crafts/",
            "subcategory": "thanksgiving/kids-thanksgiving-crafts",
        },
        "kitchen-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-baking/kitchen-accessories/",
            "subcategory": "christmas/christmas-party-baking/christmas-baking/kitchen-accessories",
        },
        "kwanzaa": {
            "url": "https://www.michaels.com/shop/holidays-occasions/kwanzaa/",
            "subcategory": "kwanzaa",
        },
        "lantern-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-lights/lantern-lights/",
            "subcategory": "halloween/halloween-decorations/halloween-lights/lantern-lights",
        },
        "leather-crafting-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/leather-crafting-gifts/",
            "subcategory": "fathers-day/leather-crafting-gifts",
        },
        "lemax-spooky-town-collection": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/lemax-spooky-town-collection/",
            "subcategory": "halloween/lemax-spooky-town-collection",
        },
        "light-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/light-accessories/",
            "subcategory": "christmas/christmas-lights/light-accessories",
        },
        "lighted-christmas-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-wreaths/lighted-christmas-wreaths/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-wreaths/lighted-christmas-wreaths",
        },
        "lighted-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/halloween-lights/lighted-decor/",
            "subcategory": "halloween/halloween-decorations/halloween-lights/lighted-decor",
        },
        "mardi-gras": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mardi-gras/",
            "subcategory": "mardi-gras",
        },
        "mardi-gras-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mardi-gras/mardi-gras-party-supplies/",
            "subcategory": "mardi-gras/mardi-gras-party-supplies",
        },
        "mini-crafting-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/mini-crafting-lights/",
            "subcategory": "christmas/christmas-lights/mini-crafting-lights",
        },
        "mini-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/wreaths/mini-wreaths/",
            "subcategory": "spring/spring-wreaths-garlands/wreaths/mini-wreaths",
        },
        "miniature-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/miniature-ornaments/",
            "subcategory": "christmas/christmas-ornaments/miniature-ornaments",
        },
        "mischief-magic": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decor-collections/mischief-magic/",
            "subcategory": "halloween/halloween-decor-collections/mischief-magic",
        },
        "model-making-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/model-making-gifts/",
            "subcategory": "fathers-day/model-making-gifts",
        },
        "moss-excelsior": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/moss-excelsior/",
            "subcategory": "spring/spring-greenery/moss-excelsior",
        },
        "mothers-day": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/",
            "subcategory": "mothers-day",
        },
        "net-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/net-lights/",
            "subcategory": "christmas/christmas-lights/net-lights",
        },
        "new-years-eve": {
            "url": "https://www.michaels.com/shop/holidays-occasions/new-years-eve/",
            "subcategory": "new-years-eve",
        },
        "next-chapter": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-collections/next-chapter/",
            "subcategory": "spring/spring-decor-collections/next-chapter",
        },
        "novelty-lights": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-lights/novelty-lights/",
            "subcategory": "christmas/christmas-lights/novelty-lights",
        },
        "ornament-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/ornament-storage/",
            "subcategory": "christmas/christmas-ornaments/ornament-storage",
        },
        "outdoor-christmas-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/outdoor-christmas-decorations/",
            "subcategory": "christmas/outdoor-christmas-decorations",
        },
        "outdoor-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/decorations/outdoor-decorations/",
            "subcategory": "st-patricks-day/decorations/outdoor-decorations",
        },
        "outdoor-easter-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/easter-decorations/outdoor-easter-decorations/",
            "subcategory": "easter/easter-decorations/outdoor-easter-decorations",
        },
        "outdoor-halloween-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/outdoor-halloween-decorations/",
            "subcategory": "halloween/outdoor-halloween-decorations",
        },
        "outdoor-living": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/",
            "subcategory": "summer/outdoor-living",
        },
        "outdoor-toys-games": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-toys-games/outdoor-toys-games/",
            "subcategory": "summer/kids-summer-toys-games/outdoor-toys-games",
        },
        "packaging": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-party-baking/christmas-baking/packaging/",
            "subcategory": "christmas/christmas-party-baking/christmas-baking/packaging",
        },
        "party-wear-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/party-wear-accessories/",
            "subcategory": "pride/party-wear-accessories",
        },
        "peeps": {
            "url": "https://www.michaels.com/shop/holidays-occasions/easter/peeps/",
            "subcategory": "easter/peeps",
        },
        "peppermint-lane": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/peppermint-lane/",
            "subcategory": "christmas/christmas-decor-collections/peppermint-lane",
        },
        "picture-frames-shadow-boxes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/picture-frames-shadow-boxes/",
            "subcategory": "mothers-day/picture-frames-shadow-boxes",
        },
        "pillows-rugs": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/pillows-rugs/",
            "subcategory": "summer/summer-decor/pillows-rugs",
        },
        "pillows-throws-table-linens": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/decor/pillows-throws-table-linens/",
            "subcategory": "red-white-blue/decor/pillows-throws-table-linens",
        },
        "pillows-throws-table-linens-runners": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-pieces/pillows-throws-table-linens-runners/",
            "subcategory": "spring/spring-decor-pieces/pillows-throws-table-linens-runners",
        },
        "pinecones-dried-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/pinecones-dried-decor/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/pinecones-dried-decor",
        },
        "pool-accessories": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/pool-accessories/",
            "subcategory": "summer/outdoor-living/pool-accessories",
        },
        "pool-floats": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/pool-floats/",
            "subcategory": "summer/outdoor-living/pool-floats",
        },
        "pools": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/pools/",
            "subcategory": "summer/outdoor-living/pools",
        },
        "porch-yard-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/decor/porch-yard-decor/",
            "subcategory": "red-white-blue/decor/porch-yard-decor",
        },
        "potted-poinsettias": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/potted-poinsettias/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/potted-poinsettias",
        },
        "pre-lit-tree-toppers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-tree-toppers/pre-lit-tree-toppers/",
            "subcategory": "christmas/christmas-decorations/christmas-tree-toppers/pre-lit-tree-toppers",
        },
        "pre-made-floral-arrangements": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/pre-made-floral-arrangements/",
            "subcategory": "spring/spring-floral/pre-made-floral-arrangements",
        },
        "pride": {
            "url": "https://www.michaels.com/shop/holidays-occasions/pride/",
            "subcategory": "pride",
        },
        "pumpkin-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/pumpkin-crafting/",
            "subcategory": "halloween/diy-halloween-crafts/pumpkin-crafting",
        },
        "pumpkin-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/pumpkin-decor/",
            "subcategory": "halloween/pumpkin-decor",
        },
        "pumpkin-decorating-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-crafts-for-kids/pumpkin-decorating-kits/",
            "subcategory": "halloween/halloween-crafts-for-kids/pumpkin-decorating-kits",
        },
        "pumpkins": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/pumpkins/",
            "subcategory": "fall/pumpkins",
        },
        "red-white-blue": {
            "url": "https://www.michaels.com/shop/holidays-occasions/red-white-blue/",
            "subcategory": "red-white-blue",
        },
        "reflected-romance": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-collections/reflected-romance/",
            "subcategory": "fall/fall-decor-collections/reflected-romance",
        },
        "roll-wrap": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/roll-wrap/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags/roll-wrap",
        },
        "rugs-doormats": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/rugs-doormats/",
            "subcategory": "summer/outdoor-living/rugs-doormats",
        },
        "shatterproof-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/shatterproof-ornaments/",
            "subcategory": "christmas/christmas-ornaments/shatterproof-ornaments",
        },
        "shop-all-christmas-trees": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas-trees/shop-all-christmas-trees/",
            "subcategory": "christmas-trees/shop-all-christmas-trees",
        },
        "shop-all-mothers-day-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/shop-all-mothers-day-gifts/",
            "subcategory": "mothers-day/shop-all-mothers-day-gifts",
        },
        "shred-tissue": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/shred-tissue/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags/shred-tissue",
        },
        "sidewalk-chalk": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/kids-summer-toys-games/sidewalk-chalk/",
            "subcategory": "summer/kids-summer-toys-games/sidewalk-chalk",
        },
        "silent-night": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decor-collections/silent-night/",
            "subcategory": "christmas/christmas-decor-collections/silent-night",
        },
        "skeletons": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decorations/skeletons/",
            "subcategory": "halloween/halloween-decorations/skeletons",
        },
        "spooky-buildings": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/lemax-spooky-town-collection/spooky-buildings/",
            "subcategory": "halloween/lemax-spooky-town-collection/spooky-buildings",
        },
        "sports-fan": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/sports-fan/",
            "subcategory": "fathers-day/sports-fan",
        },
        "spring": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/",
            "subcategory": "spring",
        },
        "spring-baskets": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-baskets-containers/spring-baskets/",
            "subcategory": "spring/spring-baskets-containers/spring-baskets",
        },
        "spring-baskets-containers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-baskets-containers/",
            "subcategory": "spring/spring-baskets-containers",
        },
        "spring-candle-holders": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-candles-fragrances/spring-candle-holders/",
            "subcategory": "spring/spring-candles-fragrances/spring-candle-holders",
        },
        "spring-candles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-candles-fragrances/spring-candles/",
            "subcategory": "spring/spring-candles-fragrances/spring-candles",
        },
        "spring-candles-fragrances": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-candles-fragrances/",
            "subcategory": "spring/spring-candles-fragrances",
        },
        "spring-canvas-painting-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-crafting/spring-canvas-painting-kits/",
            "subcategory": "spring/spring-crafting/spring-canvas-painting-kits",
        },
        "spring-celebrations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-celebrations/",
            "subcategory": "spring/spring-celebrations",
        },
        "spring-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-crafting/",
            "subcategory": "spring/spring-crafting",
        },
        "spring-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/kids-spring-crafts-activities/spring-crafts/",
            "subcategory": "spring/kids-spring-crafts-activities/spring-crafts",
        },
        "spring-decor-collections": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-collections/",
            "subcategory": "spring/spring-decor-collections",
        },
        "spring-decor-pieces": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-pieces/",
            "subcategory": "spring/spring-decor-pieces",
        },
        "spring-diamond-art": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-crafting/spring-diamond-art/",
            "subcategory": "spring/spring-crafting/spring-diamond-art",
        },
        "spring-fillers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-vases-containers-hangers/spring-fillers/",
            "subcategory": "spring/spring-vases-containers-hangers/spring-fillers",
        },
        "spring-floral": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/",
            "subcategory": "spring/spring-floral",
        },
        "spring-floral-front-porch": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-porch-yard-decor/spring-floral-front-porch/",
            "subcategory": "spring/spring-porch-yard-decor/spring-floral-front-porch",
        },
        "spring-floral-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/garlands/spring-floral-garlands/",
            "subcategory": "spring/spring-wreaths-garlands/garlands/spring-floral-garlands",
        },
        "spring-floral-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/wreaths/spring-floral-wreaths/",
            "subcategory": "spring/spring-wreaths-garlands/wreaths/spring-floral-wreaths",
        },
        "spring-greenery": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/",
            "subcategory": "spring/spring-greenery",
        },
        "spring-greenery-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/garlands/spring-greenery-garlands/",
            "subcategory": "spring/spring-wreaths-garlands/garlands/spring-greenery-garlands",
        },
        "spring-greenery-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/wreaths/spring-greenery-wreaths/",
            "subcategory": "spring/spring-wreaths-garlands/wreaths/spring-greenery-wreaths",
        },
        "spring-home-fragrance": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-candles-fragrances/spring-home-fragrance/",
            "subcategory": "spring/spring-candles-fragrances/spring-home-fragrance",
        },
        "spring-jar-candles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-candles-fragrances/spring-jar-candles/",
            "subcategory": "spring/spring-candles-fragrances/spring-jar-candles",
        },
        "spring-lanterns": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-candles-fragrances/spring-lanterns/",
            "subcategory": "spring/spring-candles-fragrances/spring-lanterns",
        },
        "spring-lighting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-pieces/spring-lighting/",
            "subcategory": "spring/spring-decor-pieces/spring-lighting",
        },
        "spring-memorial-flowers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/spring-memorial-flowers/",
            "subcategory": "spring/spring-floral/spring-memorial-flowers",
        },
        "spring-minis": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/spring-minis/",
            "subcategory": "spring/spring-floral/spring-minis",
        },
        "spring-needle-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-crafting/spring-needle-crafts/",
            "subcategory": "spring/spring-crafting/spring-needle-crafts",
        },
        "spring-papercrafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-crafting/spring-papercrafts/",
            "subcategory": "spring/spring-crafting/spring-papercrafts",
        },
        "spring-porch-yard-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-porch-yard-decor/",
            "subcategory": "spring/spring-porch-yard-decor",
        },
        "spring-ribbon": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-ribbon/",
            "subcategory": "spring/spring-ribbon",
        },
        "spring-stems-bushes-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/spring-stems-bushes-picks/",
            "subcategory": "spring/spring-floral/spring-stems-bushes-picks",
        },
        "spring-tabletop-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-pieces/spring-tabletop-decor/",
            "subcategory": "spring/spring-decor-pieces/spring-tabletop-decor",
        },
        "spring-toys-activities": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/kids-spring-crafts-activities/spring-toys-activities/",
            "subcategory": "spring/kids-spring-crafts-activities/spring-toys-activities",
        },
        "spring-trees-floor-plants": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-trees-floor-plants/",
            "subcategory": "spring/spring-trees-floor-plants",
        },
        "spring-vases-containers-hangers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-vases-containers-hangers/",
            "subcategory": "spring/spring-vases-containers-hangers",
        },
        "spring-wall-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-decor-pieces/spring-wall-decor/",
            "subcategory": "spring/spring-decor-pieces/spring-wall-decor",
        },
        "spring-wood-ceramic-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-crafting/spring-wood-ceramic-crafts/",
            "subcategory": "spring/spring-crafting/spring-wood-ceramic-crafts",
        },
        "spring-wreaths-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-wreaths-garlands/",
            "subcategory": "spring/spring-wreaths-garlands",
        },
        "st-patricks-day-baking-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/st-patricks-day-baking-supplies/",
            "subcategory": "st-patricks-day/st-patricks-day-baking-supplies",
        },
        "st-patricks-day-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/st-patricks-day-party-supplies/",
            "subcategory": "st-patricks-day/st-patricks-day-party-supplies",
        },
        "star-tree-toppers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-decorations/christmas-tree-toppers/star-tree-toppers/",
            "subcategory": "christmas/christmas-decorations/christmas-tree-toppers/star-tree-toppers",
        },
        "stem-bundles": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/stem-bundles/",
            "subcategory": "spring/spring-floral/stem-bundles",
        },
        "stems": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-floral/spring-stems-bushes-picks/stems/",
            "subcategory": "spring/spring-floral/spring-stems-bushes-picks/stems",
        },
        "stickers-embellishments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/graduation/crafting/stickers-embellishments/",
            "subcategory": "graduation/crafting/stickers-embellishments",
        },
        "stitchery-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/stitchery-gifts/",
            "subcategory": "mothers-day/stitchery-gifts",
        },
        "summer": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/",
            "subcategory": "summer",
        },
        "summer-apparel-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-crafting/summer-apparel-crafting/",
            "subcategory": "summer/summer-crafting/summer-apparel-crafting",
        },
        "summer-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-baking/",
            "subcategory": "summer/summer-baking",
        },
        "summer-baskets-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-baskets-storage/",
            "subcategory": "summer/summer-baskets-storage",
        },
        "summer-birds": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-birds/",
            "subcategory": "summer/summer-floral/summer-birds",
        },
        "summer-bushes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-stems-bushes-picks/summer-bushes/",
            "subcategory": "summer/summer-floral/summer-stems-bushes-picks/summer-bushes",
        },
        "summer-canvas-painting-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-crafting/summer-canvas-painting-kits/",
            "subcategory": "summer/summer-crafting/summer-canvas-painting-kits",
        },
        "summer-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-crafting/",
            "subcategory": "summer/summer-crafting",
        },
        "summer-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/",
            "subcategory": "summer/summer-decor",
        },
        "summer-decor-collections": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor-collections/",
            "subcategory": "summer/summer-decor-collections",
        },
        "summer-diamond-painting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-crafting/summer-diamond-painting/",
            "subcategory": "summer/summer-crafting/summer-diamond-painting",
        },
        "summer-floral": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/",
            "subcategory": "summer/summer-floral",
        },
        "summer-floral-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-wreaths-garlands/summer-garlands/summer-floral-garlands/",
            "subcategory": "summer/summer-wreaths-garlands/summer-garlands/summer-floral-garlands",
        },
        "summer-floral-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-floral-supplies/",
            "subcategory": "summer/summer-floral/summer-floral-supplies",
        },
        "summer-floral-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-wreaths-garlands/summer-wreaths/summer-floral-wreaths/",
            "subcategory": "summer/summer-wreaths-garlands/summer-wreaths/summer-floral-wreaths",
        },
        "summer-floral-wreaths-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-floral-wreaths-garlands/",
            "subcategory": "summer/summer-floral/summer-floral-wreaths-garlands",
        },
        "summer-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-wreaths-garlands/summer-garlands/",
            "subcategory": "summer/summer-wreaths-garlands/summer-garlands",
        },
        "summer-greenery-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-wreaths-garlands/summer-garlands/summer-greenery-garlands/",
            "subcategory": "summer/summer-wreaths-garlands/summer-garlands/summer-greenery-garlands",
        },
        "summer-greenery-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-wreaths-garlands/summer-wreaths/summer-greenery-wreaths/",
            "subcategory": "summer/summer-wreaths-garlands/summer-wreaths/summer-greenery-wreaths",
        },
        "summer-lighting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-decor/summer-lighting/",
            "subcategory": "summer/summer-decor/summer-lighting",
        },
        "summer-minis": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-minis/",
            "subcategory": "summer/summer-floral/summer-minis",
        },
        "summer-party": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-party/",
            "subcategory": "summer/summer-party",
        },
        "summer-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-stems-bushes-picks/summer-picks/",
            "subcategory": "summer/summer-floral/summer-stems-bushes-picks/summer-picks",
        },
        "summer-stems": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-stems-bushes-picks/summer-stems/",
            "subcategory": "summer/summer-floral/summer-stems-bushes-picks/summer-stems",
        },
        "summer-stems-bushes-picks": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-stems-bushes-picks/",
            "subcategory": "summer/summer-floral/summer-stems-bushes-picks",
        },
        "summer-unfinished-wood-ceramic-surfaces": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-crafting/summer-unfinished-wood-ceramic-surfaces/",
            "subcategory": "summer/summer-crafting/summer-unfinished-wood-ceramic-surfaces",
        },
        "summer-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-wreaths-garlands/summer-wreaths/",
            "subcategory": "summer/summer-wreaths-garlands/summer-wreaths",
        },
        "summer-wreaths-garlands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-wreaths-garlands/",
            "subcategory": "summer/summer-wreaths-garlands",
        },
        "swags-teardrops": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/swags-teardrops/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/swags-teardrops",
        },
        "table-linen-runners": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fall/fall-decor-pieces/table-linen-runners/",
            "subcategory": "fall/fall-decor-pieces/table-linen-runners",
        },
        "table-linens": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-decor/table-linens/",
            "subcategory": "thanksgiving/thanksgiving-decor/table-linens",
        },
        "tabletop": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-floral-arrangements-greenery/christmas-floral-arrangements/tabletop/",
            "subcategory": "christmas/christmas-floral-arrangements-greenery/christmas-floral-arrangements/tabletop",
        },
        "tabletop-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/st-patricks-day/decorations/tabletop-decorations/",
            "subcategory": "st-patricks-day/decorations/tabletop-decorations",
        },
        "tape-cutting-tools": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wrapping-paper-gift-bags/tape-cutting-tools/",
            "subcategory": "christmas/christmas-wrapping-paper-gift-bags/tape-cutting-tools",
        },
        "tech-apparel-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/tech-apparel-crafting/",
            "subcategory": "halloween/diy-halloween-crafts/tech-apparel-crafting",
        },
        "thanksgiving": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/",
            "subcategory": "thanksgiving",
        },
        "thanksgiving-cards": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-cards/",
            "subcategory": "thanksgiving/thanksgiving-cards",
        },
        "thanksgiving-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-decor/",
            "subcategory": "thanksgiving/thanksgiving-decor",
        },
        "thanksgiving-diys": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-diys/",
            "subcategory": "thanksgiving/thanksgiving-diys",
        },
        "thanksgiving-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-party-supplies/",
            "subcategory": "thanksgiving/thanksgiving-party-supplies",
        },
        "thanksgiving-ribbon": {
            "url": "https://www.michaels.com/shop/holidays-occasions/thanksgiving/thanksgiving-ribbon/",
            "subcategory": "thanksgiving/thanksgiving-ribbon",
        },
        "treat-making": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-party/treat-making/",
            "subcategory": "summer/summer-party/treat-making",
        },
        "trees-landscaping": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/lemax-christmas-village/trees-landscaping/",
            "subcategory": "christmas/lemax-christmas-village/trees-landscaping",
        },
        "tumblers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/tumblers/",
            "subcategory": "mothers-day/tumblers",
        },
        "umbrellas-stands": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/outdoor-living/umbrellas-stands/",
            "subcategory": "summer/outdoor-living/umbrellas-stands",
        },
        "undecorated-garland": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-garlands/undecorated-garland/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-garlands/undecorated-garland",
        },
        "undecorated-wreaths": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-wreaths/undecorated-wreaths/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-wreaths/undecorated-wreaths",
        },
        "valentines-baking": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-baking-party-supplies/valentines-baking/",
            "subcategory": "valentines-day/valentines-baking-party-supplies/valentines-baking",
        },
        "valentines-baking-party-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-baking-party-supplies/",
            "subcategory": "valentines-day/valentines-baking-party-supplies",
        },
        "valentines-cards-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-cards-crafting/",
            "subcategory": "valentines-day/valentines-cards-crafting",
        },
        "valentines-day-candy": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-candy/",
            "subcategory": "valentines-day/valentines-day-candy",
        },
        "valentines-day-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-decor/",
            "subcategory": "valentines-day/valentines-day-decor",
        },
        "valentines-day-diamond-painting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-diamond-painting/",
            "subcategory": "valentines-day/valentines-day-diamond-painting",
        },
        "valentines-day-lighting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-decor/valentines-day-lighting/",
            "subcategory": "valentines-day/valentines-day-decor/valentines-day-lighting",
        },
        "valentines-day-outdoor-decorations": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-decor/valentines-day-outdoor-decorations/",
            "subcategory": "valentines-day/valentines-day-decor/valentines-day-outdoor-decorations",
        },
        "valentines-day-pillows-throws": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-decor/valentines-day-pillows-throws/",
            "subcategory": "valentines-day/valentines-day-decor/valentines-day-pillows-throws",
        },
        "valentines-day-tabletop-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-decor/valentines-day-tabletop-decor/",
            "subcategory": "valentines-day/valentines-day-decor/valentines-day-tabletop-decor",
        },
        "valentines-day-wall-decor": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-day-decor/valentines-day-wall-decor/",
            "subcategory": "valentines-day/valentines-day-decor/valentines-day-wall-decor",
        },
        "valentines-floral": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-floral/",
            "subcategory": "valentines-day/valentines-floral",
        },
        "valentines-jewelry": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-jewelry/",
            "subcategory": "valentines-day/valentines-jewelry",
        },
        "valentines-kids-craft-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-kids-crafts/valentines-kids-craft-kits/",
            "subcategory": "valentines-day/valentines-kids-crafts/valentines-kids-craft-kits",
        },
        "valentines-kids-craft-supplies": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-kids-crafts/valentines-kids-craft-supplies/",
            "subcategory": "valentines-day/valentines-kids-crafts/valentines-kids-craft-supplies",
        },
        "valentines-kids-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-kids-crafts/",
            "subcategory": "valentines-day/valentines-kids-crafts",
        },
        "valentines-kids-impulse": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-kids-crafts/valentines-kids-impulse/",
            "subcategory": "valentines-day/valentines-kids-crafts/valentines-kids-impulse",
        },
        "valentines-paint-by-number-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-paint-by-number-kits/",
            "subcategory": "valentines-day/valentines-paint-by-number-kits",
        },
        "valentines-party-favors-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-party-favors-gifts/",
            "subcategory": "valentines-day/valentines-party-favors-gifts",
        },
        "valentines-party-packaging": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-baking-party-supplies/valentines-party-packaging/",
            "subcategory": "valentines-day/valentines-baking-party-supplies/valentines-party-packaging",
        },
        "valentines-ribbon": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-ribbon/",
            "subcategory": "valentines-day/valentines-ribbon",
        },
        "value-pack-paper": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/christmas-papercrafting/value-pack-paper/",
            "subcategory": "christmas/christmas-crafts-diy/christmas-papercrafting/value-pack-paper",
        },
        "vintage-spirits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/halloween-decor-collections/vintage-spirits/",
            "subcategory": "halloween/halloween-decor-collections/vintage-spirits",
        },
        "water-fountains": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/water-fountains/",
            "subcategory": "spring/water-fountains",
        },
        "water-resistant-bushes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/summer-stems-bushes-picks/summer-bushes/water-resistant-bushes/",
            "subcategory": "summer/summer-floral/summer-stems-bushes-picks/summer-bushes/water-resistant-bushes",
        },
        "wine-lover": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/wine-lover/",
            "subcategory": "mothers-day/wine-lover",
        },
        "wood-crafting-gifts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/fathers-day/wood-crafting-gifts/",
            "subcategory": "fathers-day/wood-crafting-gifts",
        },
        "wood-ornaments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-ornaments/wood-ornaments/",
            "subcategory": "christmas/christmas-ornaments/wood-ornaments",
        },
        "wreath-garland-making": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/wreath-garland-making/",
            "subcategory": "halloween/diy-halloween-crafts/wreath-garland-making",
        },
        "wreath-hangers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-wreaths/wreath-hangers/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-wreaths/wreath-hangers",
        },
        "wreath-making": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/wreath-making/",
            "subcategory": "christmas/christmas-crafts-diy/wreath-making",
        },
        "wreath-making-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-wreaths/wreath-making-kits/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-wreaths/wreath-making-kits",
        },
        "wreath-storage": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-wreaths-garlands/christmas-wreaths/wreath-storage/",
            "subcategory": "christmas/christmas-wreaths-garlands/christmas-wreaths/wreath-storage",
        },
        "xcanvas-painting-kits": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/xcanvas-painting-kits/",
            "subcategory": "christmas/christmas-crafts-diy/xcanvas-painting-kits",
        },
        "xcards-envelopes": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-cards-crafting/xcards-envelopes/",
            "subcategory": "valentines-day/valentines-cards-crafting/xcards-envelopes",
        },
        "xchinese-new-year": {
            "url": "https://www.michaels.com/shop/holidays-occasions/xchinese-new-year/",
            "subcategory": "xchinese-new-year",
        },
        "xdie-cuts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-cards-crafting/xdie-cuts/",
            "subcategory": "valentines-day/valentines-cards-crafting/xdie-cuts",
        },
        "xembellishments": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-cards-crafting/xembellishments/",
            "subcategory": "valentines-day/valentines-cards-crafting/xembellishments",
        },
        "xfiller": {
            "url": "https://www.michaels.com/shop/holidays-occasions/summer/summer-floral/xfiller/",
            "subcategory": "summer/summer-floral/xfiller",
        },
        "xpaint-by-number": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/xpaint-by-number/",
            "subcategory": "christmas/christmas-crafts-diy/xpaint-by-number",
        },
        "xstamps": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-cards-crafting/xstamps/",
            "subcategory": "valentines-day/valentines-cards-crafting/xstamps",
        },
        "xsucculents": {
            "url": "https://www.michaels.com/shop/holidays-occasions/spring/spring-greenery/xsucculents/",
            "subcategory": "spring/spring-greenery/xsucculents",
        },
        "xv-day-stickers": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-cards-crafting/xv-day-stickers/",
            "subcategory": "valentines-day/valentines-cards-crafting/xv-day-stickers",
        },
        "xwashi-tape": {
            "url": "https://www.michaels.com/shop/holidays-occasions/valentines-day/valentines-cards-crafting/xwashi-tape/",
            "subcategory": "valentines-day/valentines-cards-crafting/xwashi-tape",
        },
        "yarn-crafting": {
            "url": "https://www.michaels.com/shop/holidays-occasions/halloween/diy-halloween-crafts/yarn-crafting/",
            "subcategory": "halloween/diy-halloween-crafts/yarn-crafting",
        },
        "yarn-crafts": {
            "url": "https://www.michaels.com/shop/holidays-occasions/christmas/christmas-crafts-diy/yarn-crafts/",
            "subcategory": "christmas/christmas-crafts-diy/yarn-crafts",
        },
        "yarn-lover": {
            "url": "https://www.michaels.com/shop/holidays-occasions/mothers-day/yarn-lover/",
            "subcategory": "mothers-day/yarn-lover",
        },
    },
    "home-decor": {
        "accent-chairs": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/accent-chairs/",
            "subcategory": "accent-furniture/accent-chairs",
        },
        "accent-end-tables": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/accent-end-tables/",
            "subcategory": "accent-furniture/accent-end-tables",
        },
        "accent-furniture": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/",
            "subcategory": "accent-furniture",
        },
        "accent-pieces": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/accent-pieces/",
            "subcategory": "wall-decor-mirrors/accent-pieces",
        },
        "albums": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/albums/",
            "subcategory": "sports-fan-shop/albums",
        },
        "arbors-trellises": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/arbors-trellises/",
            "subcategory": "outdoor-decor/garden-decor/arbors-trellises",
        },
        "ashland": {
            "url": "https://www.michaels.com/shop/home-decor/ashland/",
            "subcategory": "ashland",
        },
        "bar-drinkware": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/",
            "subcategory": "kitchenware/bar-drinkware",
        },
        "bar-glasses": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/bar-glasses/",
            "subcategory": "kitchenware/bar-drinkware/bar-glasses",
        },
        "bar-tools-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/bar-tools-accessories/",
            "subcategory": "kitchenware/bar-drinkware/bar-tools-accessories",
        },
        "bath-body": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-body/",
            "subcategory": "bathware-accessories/bath-body",
        },
        "bath-salts": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-body/bath-salts/",
            "subcategory": "bathware-accessories/bath-body/bath-salts",
        },
        "bath-towels": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-towels/",
            "subcategory": "bathware-accessories/bath-towels",
        },
        "bathware-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/",
            "subcategory": "bathware-accessories",
        },
        "bed-pillows": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/bedding-essentials/bed-pillows/",
            "subcategory": "bedding/bedding-essentials/bed-pillows",
        },
        "bed-skirts": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/bed-skirts/",
            "subcategory": "bedding/bed-skirts",
        },
        "bedding": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/",
            "subcategory": "bedding",
        },
        "bedding-essentials": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/bedding-essentials/",
            "subcategory": "bedding/bedding-essentials",
        },
        "benches": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/ottomans-benches-poufs/benches/",
            "subcategory": "accent-furniture/ottomans-benches-poufs/benches",
        },
        "bird-baths-houses-feeders": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/bird-baths-houses-feeders/",
            "subcategory": "outdoor-decor/garden-decor/bird-baths-houses-feeders",
        },
        "blankets-throws": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/blankets-throws/",
            "subcategory": "bedding/blankets-throws",
        },
        "body-face-oils": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-body/body-face-oils/",
            "subcategory": "bathware-accessories/bath-body/body-face-oils",
        },
        "bookends": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/bookends/",
            "subcategory": "decorative-objects/bookends",
        },
        "bulbs": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/bulbs-accessories/bulbs/",
            "subcategory": "lighting/bulbs-accessories/bulbs",
        },
        "bulbs-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/bulbs-accessories/",
            "subcategory": "lighting/bulbs-accessories",
        },
        "cabinets": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/cabinets-chests-shelving/cabinets/",
            "subcategory": "accent-furniture/cabinets-chests-shelving/cabinets",
        },
        "cabinets-chests-shelving": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/cabinets-chests-shelving/",
            "subcategory": "accent-furniture/cabinets-chests-shelving",
        },
        "candle-lanterns": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/candle-lanterns/",
            "subcategory": "candles-fragrances/candle-lanterns",
        },
        "canvas-art": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/canvas-art/",
            "subcategory": "wall-decor-mirrors/canvas-art",
        },
        "carts-bar-carts": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/carts-bar-carts/",
            "subcategory": "accent-furniture/carts-bar-carts",
        },
        "ceiling-lights": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/ceiling-lights/",
            "subcategory": "lighting/ceiling-lights",
        },
        "cheese-charcuterie-boards": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/serveware/cheese-charcuterie-boards/",
            "subcategory": "kitchenware/serveware/cheese-charcuterie-boards",
        },
        "chests": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/cabinets-chests-shelving/chests/",
            "subcategory": "accent-furniture/cabinets-chests-shelving/chests",
        },
        "clocks": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/clocks/",
            "subcategory": "wall-decor-mirrors/clocks",
        },
        "cloth-napkins": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/table-linens-runners/cloth-napkins/",
            "subcategory": "kitchenware/table-linens-runners/cloth-napkins",
        },
        "coffee-mugs-tea-cups": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/coffee-mugs-tea-cups/",
            "subcategory": "kitchenware/bar-drinkware/coffee-mugs-tea-cups",
        },
        "comforters": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/comforters/",
            "subcategory": "bedding/comforters",
        },
        "condiment-snack-serveware": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/serveware/condiment-snack-serveware/",
            "subcategory": "kitchenware/serveware/condiment-snack-serveware",
        },
        "countertop-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/countertop-accessories/",
            "subcategory": "bathware-accessories/countertop-accessories",
        },
        "curtains-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/curtains-accessories/",
            "subcategory": "decorative-objects/curtains-accessories",
        },
        "decanters-carafes": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/decanters-carafes/",
            "subcategory": "kitchenware/bar-drinkware/decanters-carafes",
        },
        "decorative-objects": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/",
            "subcategory": "decorative-objects",
        },
        "decorative-vases-containers": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/decorative-vases-containers/",
            "subcategory": "decorative-objects/decorative-vases-containers",
        },
        "diffusers": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/diffusers/",
            "subcategory": "candles-fragrances/home-fragrance/diffusers",
        },
        "dining-furniture": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/dining-furniture/",
            "subcategory": "accent-furniture/dining-furniture",
        },
        "dinnerware-sets": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/tableware/dinnerware-sets/",
            "subcategory": "kitchenware/tableware/dinnerware-sets",
        },
        "display-cases-holders": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/display-cases-holders/",
            "subcategory": "sports-fan-shop/display-cases-holders",
        },
        "display-plate-easels": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/display-plate-easels/",
            "subcategory": "decorative-objects/display-plate-easels",
        },
        "drinking-glasses": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/drinking-glasses/",
            "subcategory": "kitchenware/bar-drinkware/drinking-glasses",
        },
        "duvet-covers": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/duvet-covers/",
            "subcategory": "bedding/duvet-covers",
        },
        "essential-oils": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/essential-oils/",
            "subcategory": "candles-fragrances/home-fragrance/essential-oils",
        },
        "fire-pits": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-furniture/fire-pits/",
            "subcategory": "outdoor-decor/outdoor-furniture/fire-pits",
        },
        "fireplaces-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/fireplaces-accessories/",
            "subcategory": "outdoor-decor/fireplaces-accessories",
        },
        "flameless-warmers": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/flameless-warmers/",
            "subcategory": "candles-fragrances/home-fragrance/flameless-warmers",
        },
        "flasks": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/flasks/",
            "subcategory": "kitchenware/bar-drinkware/flasks",
        },
        "flatware": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/tableware/flatware/",
            "subcategory": "kitchenware/tableware/flatware",
        },
        "floor-mats": {
            "url": "https://www.michaels.com/shop/home-decor/rugs-mats/floor-mats/",
            "subcategory": "rugs-mats/floor-mats",
        },
        "floor-runners": {
            "url": "https://www.michaels.com/shop/home-decor/rugs-mats/floor-runners/",
            "subcategory": "rugs-mats/floor-runners",
        },
        "floor-tiles": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/floor-tiles/",
            "subcategory": "decorative-objects/floor-tiles",
        },
        "fountains": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/fountains/",
            "subcategory": "decorative-objects/fountains",
        },
        "framed-art": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/framed-art/",
            "subcategory": "wall-decor-mirrors/framed-art",
        },
        "game-day-party-supplies": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/game-day-party-supplies/",
            "subcategory": "sports-fan-shop/game-day-party-supplies",
        },
        "garden-decor": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/",
            "subcategory": "outdoor-decor/garden-decor",
        },
        "garden-stools": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-furniture/garden-stools/",
            "subcategory": "outdoor-decor/outdoor-furniture/garden-stools",
        },
        "gardening-tools": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/home-gardening/gardening-tools/",
            "subcategory": "outdoor-decor/home-gardening/gardening-tools",
        },
        "hammocks-swings": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-furniture/hammocks-swings/",
            "subcategory": "outdoor-decor/outdoor-furniture/hammocks-swings",
        },
        "heated-blankets": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/heated-blankets/",
            "subcategory": "bedding/heated-blankets",
        },
        "home-decor": {
            "url": "https://www.michaels.com/shop/home-decor/",
            "subcategory": "home-decor",
        },
        "home-decor-aprons": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/aprons/",
            "subcategory": "kitchenware/aprons",
        },
        "home-decor-area-rugs": {
            "url": "https://www.michaels.com/shop/home-decor/rugs-mats/area-rugs/",
            "subcategory": "rugs-mats/area-rugs",
        },
        "home-decor-area-rugs-2": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-rugs/area-rugs/",
            "subcategory": "outdoor-decor/outdoor-rugs/area-rugs",
        },
        "home-decor-bath-mats": {
            "url": "https://www.michaels.com/shop/home-decor/rugs-mats/bath-mats/",
            "subcategory": "rugs-mats/bath-mats",
        },
        "home-decor-bath-mats-2": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-mats/",
            "subcategory": "bathware-accessories/bath-mats",
        },
        "home-decor-bathroom-storage": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bathroom-storage/",
            "subcategory": "bathware-accessories/bathroom-storage",
        },
        "home-decor-candle-holders": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/candle-holders/",
            "subcategory": "candles-fragrances/candle-holders",
        },
        "home-decor-candles-fragrances": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/",
            "subcategory": "candles-fragrances",
        },
        "home-decor-chargers": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/chargers/",
            "subcategory": "decorative-objects/chargers",
        },
        "home-decor-coasters": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/coasters/",
            "subcategory": "kitchenware/bar-drinkware/coasters",
        },
        "home-decor-doormats": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-rugs/doormats/",
            "subcategory": "outdoor-decor/outdoor-rugs/doormats",
        },
        "home-decor-doormats-2": {
            "url": "https://www.michaels.com/shop/home-decor/rugs-mats/doormats/",
            "subcategory": "rugs-mats/doormats",
        },
        "home-decor-flags": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/flags/",
            "subcategory": "outdoor-decor/flags",
        },
        "home-decor-floor-lamps": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/lamps/floor-lamps/",
            "subcategory": "lighting/lamps/floor-lamps",
        },
        "home-decor-floral-arrangements": {
            "url": "https://www.michaels.com/shop/home-decor/floral-arrangements/",
            "subcategory": "floral-arrangements",
        },
        "home-decor-frames": {
            "url": "https://www.michaels.com/shop/home-decor/frames/",
            "subcategory": "frames",
        },
        "home-decor-hooks": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/bulbs-accessories/hooks/",
            "subcategory": "lighting/bulbs-accessories/hooks",
        },
        "home-decor-hooks-knobs": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/hooks-knobs/",
            "subcategory": "wall-decor-mirrors/hooks-knobs",
        },
        "home-decor-hooks-knobs-2": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/hooks-knobs/",
            "subcategory": "decorative-objects/hooks-knobs",
        },
        "home-decor-kitchen-mats": {
            "url": "https://www.michaels.com/shop/home-decor/rugs-mats/kitchen-mats/",
            "subcategory": "rugs-mats/kitchen-mats",
        },
        "home-decor-kitchen-mats-2": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/kitchen-mats/",
            "subcategory": "kitchenware/kitchen-mats",
        },
        "home-decor-kitchen-storage": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/kitchen-storage/",
            "subcategory": "kitchenware/kitchen-storage",
        },
        "home-decor-lighting": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/",
            "subcategory": "lighting",
        },
        "home-decor-mirrors": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/mirrors/",
            "subcategory": "wall-decor-mirrors/mirrors",
        },
        "home-decor-outdoor-decor": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/",
            "subcategory": "outdoor-decor",
        },
        "home-decor-outdoor-furniture": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-furniture/",
            "subcategory": "outdoor-decor/outdoor-furniture",
        },
        "home-decor-pillows": {
            "url": "https://www.michaels.com/shop/home-decor/pillows-throws/pillows/",
            "subcategory": "pillows-throws/pillows",
        },
        "home-decor-pillows-throws": {
            "url": "https://www.michaels.com/shop/home-decor/ashland/pillows-throws/",
            "subcategory": "ashland/pillows-throws",
        },
        "home-decor-pillows-throws-2": {
            "url": "https://www.michaels.com/shop/home-decor/pillows-throws/",
            "subcategory": "pillows-throws",
        },
        "home-decor-plates": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/tableware/plates/",
            "subcategory": "kitchenware/tableware/plates",
        },
        "home-decor-porch-signs": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/porch-signs/",
            "subcategory": "outdoor-decor/porch-signs",
        },
        "home-decor-sets": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/sets/",
            "subcategory": "bedding/sets",
        },
        "home-decor-sets-2": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/countertop-accessories/sets/",
            "subcategory": "bathware-accessories/countertop-accessories/sets",
        },
        "home-decor-sheets": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/sheets/",
            "subcategory": "bedding/sheets",
        },
        "home-decor-shelving": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/cabinets-chests-shelving/shelving/",
            "subcategory": "accent-furniture/cabinets-chests-shelving/shelving",
        },
        "home-decor-statues": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/statues/",
            "subcategory": "outdoor-decor/garden-decor/statues",
        },
        "home-decor-stools": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/stools/",
            "subcategory": "accent-furniture/stools",
        },
        "home-decor-string-lights": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/string-lights/",
            "subcategory": "lighting/string-lights",
        },
        "home-decor-tabletop-decor": {
            "url": "https://www.michaels.com/shop/home-decor/ashland/tabletop-decor/",
            "subcategory": "ashland/tabletop-decor",
        },
        "home-decor-tableware": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/tableware/",
            "subcategory": "kitchenware/tableware",
        },
        "home-decor-trash-cans": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/trash-cans/",
            "subcategory": "bathware-accessories/trash-cans",
        },
        "home-decor-wall-decor": {
            "url": "https://www.michaels.com/shop/home-decor/ashland/wall-decor/",
            "subcategory": "ashland/wall-decor",
        },
        "home-decor-wallpaper": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/wallpaper/",
            "subcategory": "wall-decor-mirrors/wallpaper",
        },
        "home-fragrance": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/",
            "subcategory": "candles-fragrances/home-fragrance",
        },
        "home-gardening": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/home-gardening/",
            "subcategory": "outdoor-decor/home-gardening",
        },
        "incense": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/incense/",
            "subcategory": "candles-fragrances/home-fragrance/incense",
        },
        "indoor-gardening": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/home-gardening/indoor-gardening/",
            "subcategory": "outdoor-decor/home-gardening/indoor-gardening",
        },
        "inflatables": {
            "url": "https://www.michaels.com/shop/home-decor/inflatables/",
            "subcategory": "inflatables",
        },
        "kids-bedding": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/kids-bedding/",
            "subcategory": "bedding/kids-bedding",
        },
        "kids-decor": {
            "url": "https://www.michaels.com/shop/home-decor/kids-decor/",
            "subcategory": "kids-decor",
        },
        "kids-gifts": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/kids-gifts/",
            "subcategory": "sports-fan-shop/kids-gifts",
        },
        "kitchen-towels": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/kitchen-towels/",
            "subcategory": "kitchenware/kitchen-towels",
        },
        "kitchenware": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/",
            "subcategory": "kitchenware",
        },
        "lamp-shades": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/bulbs-accessories/lamp-shades/",
            "subcategory": "lighting/bulbs-accessories/lamp-shades",
        },
        "lamps": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/lamps/",
            "subcategory": "lighting/lamps",
        },
        "led-flameless-candles": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/led-flameless-candles/",
            "subcategory": "candles-fragrances/led-flameless-candles",
        },
        "led-lanterns": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/led-lanterns/",
            "subcategory": "lighting/led-lanterns",
        },
        "light-strips": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/novelty-lighting/light-strips/",
            "subcategory": "lighting/novelty-lighting/light-strips",
        },
        "lighted-signs": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/novelty-lighting/lighted-signs/",
            "subcategory": "lighting/novelty-lighting/lighted-signs",
        },
        "lighters-tools": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/lighters-tools/",
            "subcategory": "candles-fragrances/lighters-tools",
        },
        "loofahs-bath-sponges-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-body/loofahs-bath-sponges-accessories/",
            "subcategory": "bathware-accessories/bath-body/loofahs-bath-sponges-accessories",
        },
        "lotion": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-body/lotion/",
            "subcategory": "bathware-accessories/bath-body/lotion",
        },
        "media-centers": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/media-centers/",
            "subcategory": "accent-furniture/media-centers",
        },
        "mini-craft-lights": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/novelty-lighting/mini-craft-lights/",
            "subcategory": "lighting/novelty-lighting/mini-craft-lights",
        },
        "napkin-rings": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/serveware/napkin-rings/",
            "subcategory": "kitchenware/serveware/napkin-rings",
        },
        "night-lights": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/night-lights/",
            "subcategory": "lighting/night-lights",
        },
        "novelty-lighting": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/novelty-lighting/",
            "subcategory": "lighting/novelty-lighting",
        },
        "novelty-table-lamps": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/novelty-lighting/novelty-table-lamps/",
            "subcategory": "lighting/novelty-lighting/novelty-table-lamps",
        },
        "oil-oil-lamps": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/oil-oil-lamps/",
            "subcategory": "candles-fragrances/home-fragrance/oil-oil-lamps",
        },
        "ottomans": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/ottomans-benches-poufs/ottomans/",
            "subcategory": "accent-furniture/ottomans-benches-poufs/ottomans",
        },
        "ottomans-benches-poufs": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/ottomans-benches-poufs/",
            "subcategory": "accent-furniture/ottomans-benches-poufs",
        },
        "outdoor-chairs-patio-sets": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-furniture/outdoor-chairs-patio-sets/",
            "subcategory": "outdoor-decor/outdoor-furniture/outdoor-chairs-patio-sets",
        },
        "outdoor-fountains": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/outdoor-fountains/",
            "subcategory": "outdoor-decor/garden-decor/outdoor-fountains",
        },
        "outdoor-lanterns": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-lighting/outdoor-lanterns/",
            "subcategory": "outdoor-decor/outdoor-lighting/outdoor-lanterns",
        },
        "outdoor-lighting": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-lighting/",
            "subcategory": "outdoor-decor/outdoor-lighting",
        },
        "outdoor-rugs": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-rugs/",
            "subcategory": "outdoor-decor/outdoor-rugs",
        },
        "outdoor-string-lights": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-lighting/outdoor-string-lights/",
            "subcategory": "outdoor-decor/outdoor-lighting/outdoor-string-lights",
        },
        "outdoor-tables": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-furniture/outdoor-tables/",
            "subcategory": "outdoor-decor/outdoor-furniture/outdoor-tables",
        },
        "oven-mitts-pot-holders": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/oven-mitts-pot-holders/",
            "subcategory": "kitchenware/oven-mitts-pot-holders",
        },
        "party-lighting": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/novelty-lighting/party-lighting/",
            "subcategory": "lighting/novelty-lighting/party-lighting",
        },
        "pathway-lighting": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-lighting/pathway-lighting/",
            "subcategory": "outdoor-decor/outdoor-lighting/pathway-lighting",
        },
        "patio-umbrellas": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-furniture/patio-umbrellas/",
            "subcategory": "outdoor-decor/outdoor-furniture/patio-umbrellas",
        },
        "pillow-covers": {
            "url": "https://www.michaels.com/shop/home-decor/pillows-throws/pillow-covers/",
            "subcategory": "pillows-throws/pillow-covers",
        },
        "pillow-inserts": {
            "url": "https://www.michaels.com/shop/home-decor/pillows-throws/pillow-inserts/",
            "subcategory": "pillows-throws/pillow-inserts",
        },
        "pillowcases-shams": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/pillowcases-shams/",
            "subcategory": "bedding/pillowcases-shams",
        },
        "pitchers": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/tableware/pitchers/",
            "subcategory": "kitchenware/tableware/pitchers",
        },
        "placemats": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/table-linens-runners/placemats/",
            "subcategory": "kitchenware/table-linens-runners/placemats",
        },
        "plant-care": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/home-gardening/plant-care/",
            "subcategory": "outdoor-decor/home-gardening/plant-care",
        },
        "plant-seeds": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/home-gardening/plant-seeds/",
            "subcategory": "outdoor-decor/home-gardening/plant-seeds",
        },
        "potpourri-sachets": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/potpourri-sachets/",
            "subcategory": "candles-fragrances/home-fragrance/potpourri-sachets",
        },
        "pots-planters": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/pots-planters/",
            "subcategory": "outdoor-decor/pots-planters",
        },
        "poufs": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/ottomans-benches-poufs/poufs/",
            "subcategory": "accent-furniture/ottomans-benches-poufs/poufs",
        },
        "power-cords-strips": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/bulbs-accessories/power-cords-strips/",
            "subcategory": "lighting/bulbs-accessories/power-cords-strips",
        },
        "protectors-toppers": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/bedding-essentials/protectors-toppers/",
            "subcategory": "bedding/bedding-essentials/protectors-toppers",
        },
        "quilts-coverlets": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/quilts-coverlets/",
            "subcategory": "bedding/quilts-coverlets",
        },
        "room-dividers": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/room-dividers/",
            "subcategory": "accent-furniture/room-dividers",
        },
        "room-sprays": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/room-sprays/",
            "subcategory": "candles-fragrances/home-fragrance/room-sprays",
        },
        "rugs-mats": {
            "url": "https://www.michaels.com/shop/home-decor/rugs-mats/",
            "subcategory": "rugs-mats",
        },
        "sconces": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/sconces/",
            "subcategory": "lighting/sconces",
        },
        "seasonal-decor": {
            "url": "https://www.michaels.com/shop/home-decor/seasonal-decor/",
            "subcategory": "seasonal-decor",
        },
        "serveware": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/serveware/",
            "subcategory": "kitchenware/serveware",
        },
        "serving-bowls": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/serveware/serving-bowls/",
            "subcategory": "kitchenware/serveware/serving-bowls",
        },
        "serving-platters-trays": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/serveware/serving-platters-trays/",
            "subcategory": "kitchenware/serveware/serving-platters-trays",
        },
        "shelves": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/shelves/",
            "subcategory": "wall-decor-mirrors/shelves",
        },
        "shop-all-inflatables": {
            "url": "https://www.michaels.com/shop/home-decor/inflatables/shop-all-inflatables/",
            "subcategory": "inflatables/shop-all-inflatables",
        },
        "shower-curtain-liners": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/shower-curtains-accessories/shower-curtain-liners/",
            "subcategory": "bathware-accessories/shower-curtains-accessories/shower-curtain-liners",
        },
        "shower-curtain-rings-rods": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/shower-curtains-accessories/shower-curtain-rings-rods/",
            "subcategory": "bathware-accessories/shower-curtains-accessories/shower-curtain-rings-rods",
        },
        "shower-curtains": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/shower-curtains-accessories/shower-curtains/",
            "subcategory": "bathware-accessories/shower-curtains-accessories/shower-curtains",
        },
        "shower-curtains-accessories": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/shower-curtains-accessories/",
            "subcategory": "bathware-accessories/shower-curtains-accessories",
        },
        "shower-heads": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/shower-curtains-accessories/shower-heads/",
            "subcategory": "bathware-accessories/shower-curtains-accessories/shower-heads",
        },
        "signs": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/signs/",
            "subcategory": "wall-decor-mirrors/signs",
        },
        "soap": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/bath-body/soap/",
            "subcategory": "bathware-accessories/bath-body/soap",
        },
        "soap-dishes-dispensers": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/countertop-accessories/soap-dishes-dispensers/",
            "subcategory": "bathware-accessories/countertop-accessories/soap-dishes-dispensers",
        },
        "solar-lighting": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/outdoor-lighting/solar-lighting/",
            "subcategory": "outdoor-decor/outdoor-lighting/solar-lighting",
        },
        "sports-fan-shop": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/",
            "subcategory": "sports-fan-shop",
        },
        "stepping-stones-pavers": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/stepping-stones-pavers/",
            "subcategory": "outdoor-decor/garden-decor/stepping-stones-pavers",
        },
        "table-lamps": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/lamps/table-lamps/",
            "subcategory": "lighting/lamps/table-lamps",
        },
        "table-linens-runners": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/table-linens-runners/",
            "subcategory": "kitchenware/table-linens-runners",
        },
        "table-runners": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/table-linens-runners/table-runners/",
            "subcategory": "kitchenware/table-linens-runners/table-runners",
        },
        "tablecloths": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/table-linens-runners/tablecloths/",
            "subcategory": "kitchenware/table-linens-runners/tablecloths",
        },
        "tabletop-accents": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/tabletop-accents/",
            "subcategory": "decorative-objects/tabletop-accents",
        },
        "tabletop-clocks": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/tabletop-clocks/",
            "subcategory": "decorative-objects/tabletop-clocks",
        },
        "tailgating-supplies": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/tailgating-supplies/",
            "subcategory": "sports-fan-shop/tailgating-supplies",
        },
        "task-lighting": {
            "url": "https://www.michaels.com/shop/home-decor/lighting/lamps/task-lighting/",
            "subcategory": "lighting/lamps/task-lighting",
        },
        "team-crafts": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/team-crafts/",
            "subcategory": "sports-fan-shop/team-crafts",
        },
        "team-decor": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/team-decor/",
            "subcategory": "sports-fan-shop/team-decor",
        },
        "team-games": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/team-games/",
            "subcategory": "sports-fan-shop/team-games",
        },
        "team-outdoor-decor": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/team-outdoor-decor/",
            "subcategory": "sports-fan-shop/team-outdoor-decor",
        },
        "team-puzzles": {
            "url": "https://www.michaels.com/shop/home-decor/sports-fan-shop/team-puzzles/",
            "subcategory": "sports-fan-shop/team-puzzles",
        },
        "throws": {
            "url": "https://www.michaels.com/shop/home-decor/pillows-throws/throws/",
            "subcategory": "pillows-throws/throws",
        },
        "toilet-brushes": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/toilet-brushes/",
            "subcategory": "bathware-accessories/toilet-brushes",
        },
        "toilet-paper-holders": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/toilet-paper-holders/",
            "subcategory": "bathware-accessories/toilet-paper-holders",
        },
        "toothbrush-holders": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/countertop-accessories/toothbrush-holders/",
            "subcategory": "bathware-accessories/countertop-accessories/toothbrush-holders",
        },
        "towel-racks": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/towel-racks/",
            "subcategory": "bathware-accessories/towel-racks",
        },
        "travel-drinkware": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/travel-drinkware/",
            "subcategory": "kitchenware/bar-drinkware/travel-drinkware",
        },
        "trays": {
            "url": "https://www.michaels.com/shop/home-decor/decorative-objects/trays/",
            "subcategory": "decorative-objects/trays",
        },
        "tumblers-tumbler-holders": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/countertop-accessories/tumblers-tumbler-holders/",
            "subcategory": "bathware-accessories/countertop-accessories/tumblers-tumbler-holders",
        },
        "vanities": {
            "url": "https://www.michaels.com/shop/home-decor/accent-furniture/vanities/",
            "subcategory": "accent-furniture/vanities",
        },
        "vanity-mirrors": {
            "url": "https://www.michaels.com/shop/home-decor/bathware-accessories/vanity-mirrors/",
            "subcategory": "bathware-accessories/vanity-mirrors",
        },
        "wall-art": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/wall-art/",
            "subcategory": "wall-decor-mirrors/wall-art",
        },
        "wall-decor-mirrors": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/",
            "subcategory": "wall-decor-mirrors",
        },
        "wall-stickers": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/wall-stickers/",
            "subcategory": "wall-decor-mirrors/wall-stickers",
        },
        "wax-candles": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/wax-candles/",
            "subcategory": "candles-fragrances/wax-candles",
        },
        "wax-melts": {
            "url": "https://www.michaels.com/shop/home-decor/candles-fragrances/home-fragrance/wax-melts/",
            "subcategory": "candles-fragrances/home-fragrance/wax-melts",
        },
        "weighted-blankets": {
            "url": "https://www.michaels.com/shop/home-decor/bedding/weighted-blankets/",
            "subcategory": "bedding/weighted-blankets",
        },
        "wind-chimes": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/wind-chimes/",
            "subcategory": "outdoor-decor/wind-chimes",
        },
        "wine-glasses": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/wine-glasses/",
            "subcategory": "kitchenware/bar-drinkware/wine-glasses",
        },
        "wine-racks": {
            "url": "https://www.michaels.com/shop/home-decor/kitchenware/bar-drinkware/wine-racks/",
            "subcategory": "kitchenware/bar-drinkware/wine-racks",
        },
        "xprints": {
            "url": "https://www.michaels.com/shop/home-decor/wall-decor-mirrors/xprints/",
            "subcategory": "wall-decor-mirrors/xprints",
        },
        "yard-art": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/yard-art/",
            "subcategory": "outdoor-decor/garden-decor/yard-art",
        },
        "yard-stakes-flags": {
            "url": "https://www.michaels.com/shop/home-decor/outdoor-decor/garden-decor/yard-stakes-flags/",
            "subcategory": "outdoor-decor/garden-decor/yard-stakes-flags",
        },
    },
    "jonathan-adler": {
        "canvas-kits": {
            "url": "https://www.michaels.com/shop/jonathan-adler/crafts/canvas-kits/",
            "subcategory": "crafts/canvas-kits",
        },
        "casual-crafter": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decor-collections/casual-crafter/",
            "subcategory": "decor-collections/casual-crafter",
        },
        "crafts": {
            "url": "https://www.michaels.com/shop/jonathan-adler/crafts/",
            "subcategory": "crafts",
        },
        "decor-collections": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decor-collections/",
            "subcategory": "decor-collections",
        },
        "decorator-deluxe": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decor-collections/decorator-deluxe/",
            "subcategory": "decor-collections/decorator-deluxe",
        },
        "decorator-deluxe-black-white": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decor-collections/decorator-deluxe-black-white/",
            "subcategory": "decor-collections/decorator-deluxe-black-white",
        },
        "jonathan-adler": {
            "url": "https://www.michaels.com/shop/jonathan-adler/",
            "subcategory": "jonathan-adler",
        },
        "jonathan-adler-decorations": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decorations/",
            "subcategory": "decorations",
        },
        "jonathan-adler-diamond-painting": {
            "url": "https://www.michaels.com/shop/jonathan-adler/crafts/diamond-painting/",
            "subcategory": "crafts/diamond-painting",
        },
        "jonathan-adler-frames": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decorations/frames/",
            "subcategory": "decorations/frames",
        },
        "jonathan-adler-games": {
            "url": "https://www.michaels.com/shop/jonathan-adler/games/",
            "subcategory": "games",
        },
        "jonathan-adler-paint-by-number": {
            "url": "https://www.michaels.com/shop/jonathan-adler/crafts/paint-by-number/",
            "subcategory": "crafts/paint-by-number",
        },
        "jonathan-adler-party-supplies": {
            "url": "https://www.michaels.com/shop/jonathan-adler/party-supplies/",
            "subcategory": "party-supplies",
        },
        "jonathan-adler-pillows": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decorations/pillows/",
            "subcategory": "decorations/pillows",
        },
        "jonathan-adler-tabletop-decor": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decorations/tabletop-decor/",
            "subcategory": "decorations/tabletop-decor",
        },
        "jonathan-adler-wall-decor": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decorations/wall-decor/",
            "subcategory": "decorations/wall-decor",
        },
        "mod-maker": {
            "url": "https://www.michaels.com/shop/jonathan-adler/decor-collections/mod-maker/",
            "subcategory": "decor-collections/mod-maker",
        },
        "stitchery-crochet": {
            "url": "https://www.michaels.com/shop/jonathan-adler/crafts/stitchery-crochet/",
            "subcategory": "crafts/stitchery-crochet",
        },
        "unfinished-surfaces": {
            "url": "https://www.michaels.com/shop/jonathan-adler/crafts/unfinished-surfaces/",
            "subcategory": "crafts/unfinished-surfaces",
        },
    },
    "kids": {
        "3d": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/",
            "subcategory": "toys-games/puzzles/3d",
        },
        "3d-lunar-lantern": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/3d-lunar-lantern/",
            "subcategory": "kids-crafting/camp-creatology/3d-lunar-lantern",
        },
        "action": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/action/",
            "subcategory": "toys-games/games/board-games/action",
        },
        "active-play": {
            "url": "https://www.michaels.com/shop/kids/toys-games/active-play/",
            "subcategory": "toys-games/active-play",
        },
        "add-ins": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sensory-bins/diy-sensory-bins/add-ins/",
            "subcategory": "sensory-play/sensory-bins/diy-sensory-bins/add-ins",
        },
        "alphabet": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/stickers/alphabet/",
            "subcategory": "kids-crafting/embellishments/stickers/alphabet",
        },
        "alphabet-beads": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/beads/alphabet-beads/",
            "subcategory": "beads-jewelry/beads/alphabet-beads",
        },
        "animal": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/animal/",
            "subcategory": "toys-games/puzzles/3d/animal",
        },
        "animals-dinosaurs": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/wall-decor/wall-decals/animals-dinosaurs/",
            "subcategory": "furniture-decor/wall-decor/wall-decals/animals-dinosaurs",
        },
        "art-books": {
            "url": "https://www.michaels.com/shop/kids/books/art-books/",
            "subcategory": "books/art-books",
        },
        "artist": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/jigsaw/artist/",
            "subcategory": "toys-games/puzzles/jigsaw/artist",
        },
        "astronomy": {
            "url": "https://www.michaels.com/shop/kids/steam/earth-space/astronomy/",
            "subcategory": "steam/earth-space/astronomy",
        },
        "bath-body-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/bath-body-kits/",
            "subcategory": "activity-kits/bath-body-kits",
        },
        "beaded-holiday-decor": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/beaded-holiday-decor/",
            "subcategory": "kids-crafting/winter-workshop/beaded-holiday-decor",
        },
        "bins-tubes": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sensory-bins/diy-sensory-bins/bins-tubes/",
            "subcategory": "sensory-play/sensory-bins/diy-sensory-bins/bins-tubes",
        },
        "birds": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/birds/",
            "subcategory": "toys-games/figurines/birds",
        },
        "blind-packs": {
            "url": "https://www.michaels.com/shop/kids/toys-games/collectibles/blind-packs/",
            "subcategory": "toys-games/collectibles/blind-packs",
        },
        "block-sets": {
            "url": "https://www.michaels.com/shop/kids/building-toys/block-sets/",
            "subcategory": "building-toys/block-sets",
        },
        "board-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/",
            "subcategory": "toys-games/games/board-games",
        },
        "brainteasers": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/brainteasers/",
            "subcategory": "toys-games/puzzles/brainteasers",
        },
        "building-toys": {
            "url": "https://www.michaels.com/shop/kids/building-toys/",
            "subcategory": "building-toys",
        },
        "camp-creatology": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/",
            "subcategory": "kids-crafting/camp-creatology",
        },
        "card-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/card-games/",
            "subcategory": "toys-games/games/card-games",
        },
        "cars-trucks-trains": {
            "url": "https://www.michaels.com/shop/kids/toys-games/vehicles-trains-r-c/cars-trucks-trains/",
            "subcategory": "toys-games/vehicles-trains-r-c/cars-trucks-trains",
        },
        "ceramic-crafts": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-activities/ceramic-crafts/",
            "subcategory": "kids-crafting/craft-activities/ceramic-crafts",
        },
        "chairs-seating": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/kids-furniture/chairs-seating/",
            "subcategory": "furniture-decor/kids-furniture/chairs-seating",
        },
        "chalk": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/chalk-pastels/chalk/",
            "subcategory": "art-supplies/chalk-pastels/chalk",
        },
        "chalk-pastels": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/chalk-pastels/",
            "subcategory": "art-supplies/chalk-pastels",
        },
        "classic-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/classic-games/",
            "subcategory": "toys-games/games/board-games/classic-games",
        },
        "collectible-games-trading-cards": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/collectible-games-trading-cards/",
            "subcategory": "toys-games/games/collectible-games-trading-cards",
        },
        "collectibles": {
            "url": "https://www.michaels.com/shop/kids/toys-games/collectibles/",
            "subcategory": "toys-games/collectibles",
        },
        "color-in-activities": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/color-in-activities/",
            "subcategory": "art-supplies/drawing-coloring/color-in-activities",
        },
        "color-your-own": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-activities/color-your-own/",
            "subcategory": "kids-crafting/craft-activities/color-your-own",
        },
        "coloring-sets": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/coloring-sets/",
            "subcategory": "art-supplies/drawing-coloring/coloring-sets",
        },
        "colors-shapes-sorting": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/colors-shapes-sorting/",
            "subcategory": "toys-games/games/learning-games/colors-shapes-sorting",
        },
        "constellation-crafts": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/constellation-crafts/",
            "subcategory": "kids-crafting/camp-creatology/constellation-crafts",
        },
        "construction-sets": {
            "url": "https://www.michaels.com/shop/kids/building-toys/construction-sets/",
            "subcategory": "building-toys/construction-sets",
        },
        "cozy-crew-play-box": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/cozy-crew-play-box/",
            "subcategory": "kids-crafting/winter-workshop/cozy-crew-play-box",
        },
        "craft-bases": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/craft-bases/",
            "subcategory": "kids-crafting/craft-surfaces/craft-bases",
        },
        "craft-sticks": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/craft-sticks/",
            "subcategory": "kids-crafting/wood-crafts/craft-sticks",
        },
        "craft-supply-bundles": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-activities/craft-supply-bundles/",
            "subcategory": "kids-crafting/craft-activities/craft-supply-bundles",
        },
        "crafting-kits": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-activities/crafting-kits/",
            "subcategory": "kids-crafting/craft-activities/crafting-kits",
        },
        "crayola": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/crayola/",
            "subcategory": "art-supplies/crayola",
        },
        "creative-learning-kits": {
            "url": "https://www.michaels.com/shop/kids/steam/creative-learning-kits/",
            "subcategory": "steam/creative-learning-kits",
        },
        "creative-play": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/",
            "subcategory": "toys-games/creative-play",
        },
        "creatology": {
            "url": "https://www.michaels.com/shop/kids/creatology/",
            "subcategory": "creatology",
        },
        "customize-it": {
            "url": "https://www.michaels.com/shop/kids/slime/customize-it/",
            "subcategory": "slime/customize-it",
        },
        "dice-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/dice-games/",
            "subcategory": "toys-games/games/board-games/dice-games",
        },
        "diorama-figurines": {
            "url": "https://www.michaels.com/shop/kids/steam/school-project-supplies/diorama-figurines/",
            "subcategory": "steam/school-project-supplies/diorama-figurines",
        },
        "diy-sensory-bins": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sensory-bins/diy-sensory-bins/",
            "subcategory": "sensory-play/sensory-bins/diy-sensory-bins",
        },
        "dough": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/dough/",
            "subcategory": "sensory-play/dough",
        },
        "dowels": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/dowels/",
            "subcategory": "kids-crafting/wood-crafts/dowels",
        },
        "dress-up": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/dress-up/",
            "subcategory": "toys-games/creative-play/dress-up",
        },
        "earth-space": {
            "url": "https://www.michaels.com/shop/kids/steam/earth-space/",
            "subcategory": "steam/earth-space",
        },
        "easels-lap-desks": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/easels-lap-desks/",
            "subcategory": "art-supplies/easels-lap-desks",
        },
        "electronic-learning": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/electronic-learning/",
            "subcategory": "toys-games/games/learning-games/electronic-learning",
        },
        "engineering": {
            "url": "https://www.michaels.com/shop/kids/steam/engineering/",
            "subcategory": "steam/engineering",
        },
        "environmental-science": {
            "url": "https://www.michaels.com/shop/kids/steam/earth-space/environmental-science/",
            "subcategory": "steam/earth-space/environmental-science",
        },
        "fa-la-la-la-la-frames": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/fa-la-la-la-la-frames/",
            "subcategory": "kids-crafting/winter-workshop/fa-la-la-la-la-frames",
        },
        "face-paint": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/face-paint/",
            "subcategory": "toys-games/creative-play/face-paint",
        },
        "fashion-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/fashion-kits/",
            "subcategory": "activity-kits/fashion-kits",
        },
        "finger-paint": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint/finger-paint/",
            "subcategory": "art-supplies/painting/paint/finger-paint",
        },
        "floor-foam": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/floor-foam/",
            "subcategory": "toys-games/puzzles/floor-foam",
        },
        "foam-board": {
            "url": "https://www.michaels.com/shop/kids/steam/school-project-supplies/foam-board/",
            "subcategory": "steam/school-project-supplies/foam-board",
        },
        "frozen-friendly-pots": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/frozen-friendly-pots/",
            "subcategory": "kids-crafting/camp-creatology/frozen-friendly-pots",
        },
        "fun-fruity-patches": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/fun-fruity-patches/",
            "subcategory": "kids-crafting/camp-creatology/fun-fruity-patches",
        },
        "fur": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/fur/",
            "subcategory": "kids-crafting/craft-surfaces/fur",
        },
        "furniture": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/play-sets-play-food/furniture/",
            "subcategory": "toys-games/creative-play/play-sets-play-food/furniture",
        },
        "furniture-decor": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/",
            "subcategory": "furniture-decor",
        },
        "fuzzy-posters": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/fuzzy-posters/",
            "subcategory": "art-supplies/drawing-coloring/fuzzy-posters",
        },
        "gallon-paint": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint/gallon-paint/",
            "subcategory": "art-supplies/painting/paint/gallon-paint",
        },
        "gear-sets": {
            "url": "https://www.michaels.com/shop/kids/building-toys/gear-sets/",
            "subcategory": "building-toys/gear-sets",
        },
        "gem-crystal-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/gem-crystal-kits/",
            "subcategory": "activity-kits/gem-crystal-kits",
        },
        "geology": {
            "url": "https://www.michaels.com/shop/kids/steam/earth-space/geology/",
            "subcategory": "steam/earth-space/geology",
        },
        "gingerbread-puppet-pals": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/gingerbread-puppet-pals/",
            "subcategory": "kids-crafting/winter-workshop/gingerbread-puppet-pals",
        },
        "hand-stitched-card": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/hand-stitched-card/",
            "subcategory": "kids-crafting/winter-workshop/hand-stitched-card",
        },
        "hidden-object-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/hidden-object-games/",
            "subcategory": "toys-games/games/learning-games/hidden-object-games",
        },
        "historical": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/historical/",
            "subcategory": "toys-games/figurines/historical",
        },
        "holly-jolly-ornaments": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/holly-jolly-ornaments/",
            "subcategory": "kids-crafting/winter-workshop/holly-jolly-ornaments",
        },
        "ice-cream-wall-of-frames": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/ice-cream-wall-of-frames/",
            "subcategory": "kids-crafting/camp-creatology/ice-cream-wall-of-frames",
        },
        "ice-dream-pencil-cup": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/ice-dream-pencil-cup/",
            "subcategory": "kids-crafting/camp-creatology/ice-dream-pencil-cup",
        },
        "indoor-play": {
            "url": "https://www.michaels.com/shop/kids/toys-games/active-play/indoor-play/",
            "subcategory": "toys-games/active-play/indoor-play",
        },
        "jewelry-looms": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/jewelry-looms/",
            "subcategory": "beads-jewelry/jewelry-looms",
        },
        "jigsaw": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/jigsaw/",
            "subcategory": "toys-games/puzzles/jigsaw",
        },
        "journaling-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/journaling-kits/",
            "subcategory": "activity-kits/journaling-kits",
        },
        "journals-books": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/paper/journals-books/",
            "subcategory": "art-supplies/paper/journals-books",
        },
        "kids-accessories": {
            "url": "https://www.michaels.com/shop/kids/toys-games/dolls/accessories/",
            "subcategory": "toys-games/dolls/accessories",
        },
        "kids-accessories-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/jigsaw/accessories/",
            "subcategory": "toys-games/puzzles/jigsaw/accessories",
        },
        "kids-acrylic-paint": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint/acrylic-paint/",
            "subcategory": "art-supplies/painting/paint/acrylic-paint",
        },
        "kids-activity-books": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/activity-books/",
            "subcategory": "activity-kits/activity-books",
        },
        "kids-activity-books-2": {
            "url": "https://www.michaels.com/shop/kids/books/activity-books/",
            "subcategory": "books/activity-books",
        },
        "kids-activity-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/",
            "subcategory": "activity-kits",
        },
        "kids-art-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/art-kits/",
            "subcategory": "activity-kits/art-kits",
        },
        "kids-art-storage": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/art-storage/",
            "subcategory": "art-supplies/art-storage",
        },
        "kids-art-supplies": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/",
            "subcategory": "art-supplies",
        },
        "kids-art-technology": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/kids-art-technology/",
            "subcategory": "art-supplies/kids-art-technology",
        },
        "kids-bead-kits": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/perler-beads/bead-kits/",
            "subcategory": "beads-jewelry/perler-beads/bead-kits",
        },
        "kids-beads": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/beads/",
            "subcategory": "beads-jewelry/beads",
        },
        "kids-beads-2": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/perler-beads/beads/",
            "subcategory": "beads-jewelry/perler-beads/beads",
        },
        "kids-beads-jewelry-2": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/",
            "subcategory": "beads-jewelry",
        },
        "kids-bells": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/bells/",
            "subcategory": "kids-crafting/embellishments/bells",
        },
        "kids-books": {
            "url": "https://www.michaels.com/shop/kids/books/",
            "subcategory": "books",
        },
        "kids-brushes": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/brushes/",
            "subcategory": "art-supplies/painting/brushes",
        },
        "kids-canvas": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/canvas/",
            "subcategory": "art-supplies/painting/canvas",
        },
        "kids-charms": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/charms/",
            "subcategory": "beads-jewelry/charms",
        },
        "kids-chenille-stems": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/chenille-stems/",
            "subcategory": "kids-crafting/embellishments/chenille-stems",
        },
        "kids-clothespins": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/clothespins/",
            "subcategory": "kids-crafting/wood-crafts/clothespins",
        },
        "kids-colored-pencils": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/colored-pencils/",
            "subcategory": "art-supplies/drawing-coloring/colored-pencils",
        },
        "kids-coloring-books": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/coloring-books/",
            "subcategory": "art-supplies/drawing-coloring/coloring-books",
        },
        "kids-coloring-books-2": {
            "url": "https://www.michaels.com/shop/kids/books/coloring-books/",
            "subcategory": "books/coloring-books",
        },
        "kids-compounds": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sensory-bins/diy-sensory-bins/compounds/",
            "subcategory": "sensory-play/sensory-bins/diy-sensory-bins/compounds",
        },
        "kids-compounds-2": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/compounds/",
            "subcategory": "sensory-play/compounds",
        },
        "kids-construction-paper": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/construction-paper/",
            "subcategory": "kids-crafting/craft-surfaces/construction-paper",
        },
        "kids-construction-paper-2": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/paper/construction-paper/",
            "subcategory": "art-supplies/paper/construction-paper",
        },
        "kids-craft-activities": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-activities/",
            "subcategory": "kids-crafting/craft-activities",
        },
        "kids-craft-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/craft-kits/",
            "subcategory": "activity-kits/craft-kits",
        },
        "kids-craft-kits-3": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/craft-kits/",
            "subcategory": "kids-crafting/wood-crafts/craft-kits",
        },
        "kids-craft-supplies": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-supplies/",
            "subcategory": "kids-crafting/craft-supplies",
        },
        "kids-craft-surfaces": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/",
            "subcategory": "kids-crafting/craft-surfaces",
        },
        "kids-crafting-paper": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/paper/crafting-paper/",
            "subcategory": "art-supplies/paper/crafting-paper",
        },
        "kids-crayons": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/crayons/",
            "subcategory": "art-supplies/drawing-coloring/crayons",
        },
        "kids-disney": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/disney/",
            "subcategory": "toys-games/puzzles/3d/disney",
        },
        "kids-dollhouses": {
            "url": "https://www.michaels.com/shop/kids/toys-games/dolls/dollhouses/",
            "subcategory": "toys-games/dolls/dollhouses",
        },
        "kids-dolls": {
            "url": "https://www.michaels.com/shop/kids/toys-games/dolls/dolls/",
            "subcategory": "toys-games/dolls/dolls",
        },
        "kids-dolls-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/dolls/",
            "subcategory": "toys-games/dolls",
        },
        "kids-drawing-coloring": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/",
            "subcategory": "art-supplies/drawing-coloring",
        },
        "kids-dry-erase": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/dry-erase/",
            "subcategory": "art-supplies/drawing-coloring/dry-erase",
        },
        "kids-early-childhood": {
            "url": "https://www.michaels.com/shop/kids/toys-games/early-childhood/",
            "subcategory": "toys-games/early-childhood",
        },
        "kids-early-childhood-2": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/wall-decor/wall-decals/early-childhood/",
            "subcategory": "furniture-decor/wall-decor/wall-decals/early-childhood",
        },
        "kids-electronics": {
            "url": "https://www.michaels.com/shop/kids/toys-games/electronics/",
            "subcategory": "toys-games/electronics",
        },
        "kids-embellishments": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/",
            "subcategory": "kids-crafting/embellishments",
        },
        "kids-erasers": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/erasers/",
            "subcategory": "art-supplies/drawing-coloring/erasers",
        },
        "kids-feathers": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/feathers/",
            "subcategory": "kids-crafting/craft-surfaces/feathers",
        },
        "kids-felt": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/felt/",
            "subcategory": "kids-crafting/craft-surfaces/felt",
        },
        "kids-figurines": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/",
            "subcategory": "toys-games/figurines",
        },
        "kids-finished-jewelry": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/finished-jewelry/",
            "subcategory": "beads-jewelry/finished-jewelry",
        },
        "kids-foam": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/foam/",
            "subcategory": "kids-crafting/craft-surfaces/foam",
        },
        "kids-foam-2": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/stickers/foam/",
            "subcategory": "kids-crafting/embellishments/stickers/foam",
        },
        "kids-furniture": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/kids-furniture/",
            "subcategory": "furniture-decor/kids-furniture",
        },
        "kids-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/",
            "subcategory": "toys-games/games",
        },
        "kids-gems-rhinestones": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/gems-rhinestones/",
            "subcategory": "kids-crafting/embellishments/gems-rhinestones",
        },
        "kids-glitter": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/glitter/",
            "subcategory": "kids-crafting/embellishments/glitter",
        },
        "kids-glue-2": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-supplies/glue/",
            "subcategory": "kids-crafting/craft-supplies/glue",
        },
        "kids-googly-eyes": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/googly-eyes/",
            "subcategory": "kids-crafting/embellishments/googly-eyes",
        },
        "kids-harry-potter": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/harry-potter/",
            "subcategory": "toys-games/puzzles/3d/harry-potter",
        },
        "kids-hello-kitty": {
            "url": "https://www.michaels.com/shop/kids/toys-games/hello-kitty/",
            "subcategory": "toys-games/hello-kitty",
        },
        "kids-impulse": {
            "url": "https://www.michaels.com/shop/kids/toys-games/kids-impulse/",
            "subcategory": "toys-games/kids-impulse",
        },
        "kids-jewelry-kits": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/jewelry-kits/",
            "subcategory": "beads-jewelry/jewelry-kits",
        },
        "kids-jewelry-kits-2": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/jewelry-kits/",
            "subcategory": "activity-kits/jewelry-kits",
        },
        "kids-keychains": {
            "url": "https://www.michaels.com/shop/kids/toys-games/collectibles/keychains/",
            "subcategory": "toys-games/collectibles/keychains",
        },
        "kids-keychains-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/plush-toys/keychains/",
            "subcategory": "toys-games/plush-toys/keychains",
        },
        "kids-kids": {
            "url": "https://www.michaels.com/shop/kids/",
            "subcategory": "kids",
        },
        "kids-kids-crafting": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/",
            "subcategory": "kids-crafting",
        },
        "kids-kits-crafting": {
            "url": "https://www.michaels.com/shop/kids/toys-games/hello-kitty/kids-kits-crafting/",
            "subcategory": "toys-games/hello-kitty/kids-kits-crafting",
        },
        "kids-licensed": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/wall-decor/wall-decals/licensed/",
            "subcategory": "furniture-decor/wall-decor/wall-decals/licensed",
        },
        "kids-licensed-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/licensed/",
            "subcategory": "toys-games/puzzles/3d/licensed",
        },
        "kids-licensed-3": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/jigsaw/licensed/",
            "subcategory": "toys-games/puzzles/jigsaw/licensed",
        },
        "kids-life-science": {
            "url": "https://www.michaels.com/shop/kids/steam/life-science/",
            "subcategory": "steam/life-science",
        },
        "kids-locations": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/jigsaw/locations/",
            "subcategory": "toys-games/puzzles/jigsaw/locations",
        },
        "kids-locations-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/locations/",
            "subcategory": "toys-games/puzzles/3d/locations",
        },
        "kids-logic-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/logic-games/",
            "subcategory": "toys-games/games/logic-games",
        },
        "kids-logic-games-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/logic-games/",
            "subcategory": "toys-games/games/board-games/logic-games",
        },
        "kids-markers": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/markers/",
            "subcategory": "art-supplies/drawing-coloring/markers",
        },
        "kids-masks": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/masks/",
            "subcategory": "kids-crafting/craft-surfaces/masks",
        },
        "kids-misc": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/jigsaw/misc/",
            "subcategory": "toys-games/puzzles/jigsaw/misc",
        },
        "kids-misc-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/misc/",
            "subcategory": "toys-games/puzzles/3d/misc",
        },
        "kids-mixed-media-sets": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/mixed-media-sets/",
            "subcategory": "art-supplies/mixed-media-sets",
        },
        "kids-model-kits": {
            "url": "https://www.michaels.com/shop/kids/toys-games/vehicles-trains-r-c/model-kits/",
            "subcategory": "toys-games/vehicles-trains-r-c/model-kits",
        },
        "kids-music": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/music/",
            "subcategory": "toys-games/creative-play/music",
        },
        "kids-paint": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint/",
            "subcategory": "art-supplies/painting/paint",
        },
        "kids-paint-by-number": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint-by-number/",
            "subcategory": "art-supplies/painting/paint-by-number",
        },
        "kids-paper": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/paper/",
            "subcategory": "art-supplies/paper",
        },
        "kids-paper-pads": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/paper/paper-pads/",
            "subcategory": "art-supplies/paper/paper-pads",
        },
        "kids-paper-rolls": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/paper/paper-rolls/",
            "subcategory": "art-supplies/paper/paper-rolls",
        },
        "kids-party-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/party-games/",
            "subcategory": "toys-games/games/party-games",
        },
        "kids-pastels": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/chalk-pastels/pastels/",
            "subcategory": "art-supplies/chalk-pastels/pastels",
        },
        "kids-pencils": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/pencils/",
            "subcategory": "art-supplies/drawing-coloring/pencils",
        },
        "kids-pens": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/pens/",
            "subcategory": "art-supplies/drawing-coloring/pens",
        },
        "kids-reading-language-arts": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/reading-language-arts/",
            "subcategory": "toys-games/games/learning-games/reading-language-arts",
        },
        "kids-sand": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sand/",
            "subcategory": "sensory-play/sand",
        },
        "kids-sand-water-toys": {
            "url": "https://www.michaels.com/shop/kids/toys-games/active-play/sand-water-toys/",
            "subcategory": "toys-games/active-play/sand-water-toys",
        },
        "kids-school-supplies": {
            "url": "https://www.michaels.com/shop/kids/steam/school-project-supplies/school-supplies/",
            "subcategory": "steam/school-project-supplies/school-supplies",
        },
        "kids-science-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/science-kits/",
            "subcategory": "activity-kits/science-kits",
        },
        "kids-science-kits-2": {
            "url": "https://www.michaels.com/shop/kids/steam/science-kits/",
            "subcategory": "steam/science-kits",
        },
        "kids-scissors": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-supplies/scissors/",
            "subcategory": "kids-crafting/craft-supplies/scissors",
        },
        "kids-sequins": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/sequins/",
            "subcategory": "kids-crafting/embellishments/sequins",
        },
        "kids-shapes": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/foam/shapes/",
            "subcategory": "kids-crafting/craft-surfaces/foam/shapes",
        },
        "kids-sheets": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/foam/sheets/",
            "subcategory": "kids-crafting/craft-surfaces/foam/sheets",
        },
        "kids-slime": {
            "url": "https://www.michaels.com/shop/kids/slime/",
            "subcategory": "slime",
        },
        "kids-slime-2": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/slime/",
            "subcategory": "sensory-play/slime",
        },
        "kids-slime-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/slime-kits/",
            "subcategory": "activity-kits/slime-kits",
        },
        "kids-slime-kits-2": {
            "url": "https://www.michaels.com/shop/kids/slime/slime-kits/",
            "subcategory": "slime/slime-kits",
        },
        "kids-social-studies": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/social-studies/",
            "subcategory": "toys-games/games/learning-games/social-studies",
        },
        "kids-stamps-stamp-pads": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-supplies/stamps-stamp-pads/",
            "subcategory": "kids-crafting/craft-supplies/stamps-stamp-pads",
        },
        "kids-star-wars": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/star-wars/",
            "subcategory": "toys-games/puzzles/3d/star-wars",
        },
        "kids-sticker-books": {
            "url": "https://www.michaels.com/shop/kids/books/sticker-books/",
            "subcategory": "books/sticker-books",
        },
        "kids-sticker-books-2": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/stickers/sticker-books/",
            "subcategory": "kids-crafting/embellishments/stickers/sticker-books",
        },
        "kids-stickers": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/stickers/",
            "subcategory": "kids-crafting/embellishments/stickers",
        },
        "kids-stringing-materials": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/stringing-materials/",
            "subcategory": "beads-jewelry/stringing-materials",
        },
        "kids-tools": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/tools/",
            "subcategory": "sensory-play/tools",
        },
        "kids-wall-decor": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/wall-decor/",
            "subcategory": "furniture-decor/wall-decor",
        },
        "kids-wallpaper": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/wall-decor/wallpaper/",
            "subcategory": "furniture-decor/wall-decor/wallpaper",
        },
        "kids-wood": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/wood/",
            "subcategory": "toys-games/puzzles/wood",
        },
        "kids-wood-2": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/3d/wood/",
            "subcategory": "toys-games/puzzles/3d/wood",
        },
        "kids-wood-beads": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/beads/wood-beads/",
            "subcategory": "beads-jewelry/beads/wood-beads",
        },
        "kids-wood-crafts": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/",
            "subcategory": "kids-crafting/wood-crafts",
        },
        "kitchen-food": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/play-sets-play-food/kitchen-food/",
            "subcategory": "toys-games/creative-play/play-sets-play-food/kitchen-food",
        },
        "lacing": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/lacing/",
            "subcategory": "beads-jewelry/lacing",
        },
        "learning-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/",
            "subcategory": "toys-games/games/learning-games",
        },
        "lego": {
            "url": "https://www.michaels.com/shop/kids/building-toys/lego/",
            "subcategory": "building-toys/lego",
        },
        "licensed-kits": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/perler-beads/licensed-kits/",
            "subcategory": "beads-jewelry/perler-beads/licensed-kits",
        },
        "loose-leaf-paper": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/paper/loose-leaf-paper/",
            "subcategory": "art-supplies/paper/loose-leaf-paper",
        },
        "magic-tricks-sets": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/magic-tricks-sets/",
            "subcategory": "toys-games/games/magic-tricks-sets",
        },
        "magnetic-construction": {
            "url": "https://www.michaels.com/shop/kids/building-toys/magnetic-construction/",
            "subcategory": "building-toys/magnetic-construction",
        },
        "make-it": {
            "url": "https://www.michaels.com/shop/kids/slime/make-it/",
            "subcategory": "slime/make-it",
        },
        "mammals": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/mammals/",
            "subcategory": "toys-games/figurines/mammals",
        },
        "marble-runs": {
            "url": "https://www.michaels.com/shop/kids/building-toys/marble-runs/",
            "subcategory": "building-toys/marble-runs",
        },
        "math-counting": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/math-counting/",
            "subcategory": "toys-games/games/learning-games/math-counting",
        },
        "mathematics": {
            "url": "https://www.michaels.com/shop/kids/steam/mathematics/",
            "subcategory": "steam/mathematics",
        },
        "memory-matching": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/memory-matching/",
            "subcategory": "toys-games/games/learning-games/memory-matching",
        },
        "merry-masked-friends": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/merry-masked-friends/",
            "subcategory": "kids-crafting/winter-workshop/merry-masked-friends",
        },
        "mess-free-coloring": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/mess-free-coloring/",
            "subcategory": "art-supplies/drawing-coloring/mess-free-coloring",
        },
        "microscopes-telescopes": {
            "url": "https://www.michaels.com/shop/kids/steam/microscopes-telescopes/",
            "subcategory": "steam/microscopes-telescopes",
        },
        "minis": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/minis/",
            "subcategory": "toys-games/figurines/minis",
        },
        "misc-paint-mediums": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint/misc-paint-mediums/",
            "subcategory": "art-supplies/painting/paint/misc-paint-mediums",
        },
        "modeling-clay": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/modeling-clay/",
            "subcategory": "sensory-play/modeling-clay",
        },
        "moon-clay-painting": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/moon-clay-painting/",
            "subcategory": "kids-crafting/camp-creatology/moon-clay-painting",
        },
        "movie-tv-characters": {
            "url": "https://www.michaels.com/shop/kids/toys-games/collectibles/movie-tv-characters/",
            "subcategory": "toys-games/collectibles/movie-tv-characters",
        },
        "murder-mystery": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/party-games/murder-mystery/",
            "subcategory": "toys-games/games/party-games/murder-mystery",
        },
        "mythological": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/mythological/",
            "subcategory": "toys-games/figurines/mythological",
        },
        "novelty-beads": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/beads/novelty-beads/",
            "subcategory": "beads-jewelry/beads/novelty-beads",
        },
        "novelty-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/novelty-games/",
            "subcategory": "toys-games/games/board-games/novelty-games",
        },
        "outdoor-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/active-play/outdoor-play/outdoor-games/",
            "subcategory": "toys-games/active-play/outdoor-play/outdoor-games",
        },
        "outdoor-play": {
            "url": "https://www.michaels.com/shop/kids/toys-games/active-play/outdoor-play/",
            "subcategory": "toys-games/active-play/outdoor-play",
        },
        "paint-pans-pots": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint/paint-pans-pots/",
            "subcategory": "art-supplies/painting/paint/paint-pans-pots",
        },
        "paint-sets": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint-sets/",
            "subcategory": "art-supplies/painting/paint-sets",
        },
        "painted-wood-shapes": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/painted-wood-shapes/",
            "subcategory": "kids-crafting/wood-crafts/painted-wood-shapes",
        },
        "painting": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/",
            "subcategory": "art-supplies/painting",
        },
        "painting-supplies": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/painting-supplies/",
            "subcategory": "art-supplies/painting/painting-supplies",
        },
        "peg-boards": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/perler-beads/peg-boards/",
            "subcategory": "beads-jewelry/perler-beads/peg-boards",
        },
        "perler-beads": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/perler-beads/",
            "subcategory": "beads-jewelry/perler-beads",
        },
        "pets": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/pets/",
            "subcategory": "toys-games/figurines/pets",
        },
        "physics-chemistry": {
            "url": "https://www.michaels.com/shop/kids/steam/physics-chemistry/",
            "subcategory": "steam/physics-chemistry",
        },
        "play-sets-play-food": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/play-sets-play-food/",
            "subcategory": "toys-games/creative-play/play-sets-play-food",
        },
        "plush": {
            "url": "https://www.michaels.com/shop/kids/toys-games/plush-toys/plush/",
            "subcategory": "toys-games/plush-toys/plush",
        },
        "plush-toys": {
            "url": "https://www.michaels.com/shop/kids/toys-games/plush-toys/",
            "subcategory": "toys-games/plush-toys",
        },
        "poms-poms": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/poms-poms/",
            "subcategory": "kids-crafting/embellishments/poms-poms",
        },
        "pony-beads": {
            "url": "https://www.michaels.com/shop/kids/beads-jewelry/beads/pony-beads/",
            "subcategory": "beads-jewelry/beads/pony-beads",
        },
        "poster-board": {
            "url": "https://www.michaels.com/shop/kids/steam/school-project-supplies/poster-board/",
            "subcategory": "steam/school-project-supplies/poster-board",
        },
        "poster-making-supplies": {
            "url": "https://www.michaels.com/shop/kids/steam/school-project-supplies/poster-making-supplies/",
            "subcategory": "steam/school-project-supplies/poster-making-supplies",
        },
        "pre-made-sensory-bins": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sensory-bins/pre-made-sensory-bins/",
            "subcategory": "sensory-play/sensory-bins/pre-made-sensory-bins",
        },
        "prehistoric-animals": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/prehistoric-animals/",
            "subcategory": "toys-games/figurines/prehistoric-animals",
        },
        "premade-slime": {
            "url": "https://www.michaels.com/shop/kids/slime/premade-slime/",
            "subcategory": "slime/premade-slime",
        },
        "project-display-boards": {
            "url": "https://www.michaels.com/shop/kids/steam/school-project-supplies/project-display-boards/",
            "subcategory": "steam/school-project-supplies/project-display-boards",
        },
        "puppets": {
            "url": "https://www.michaels.com/shop/kids/toys-games/plush-toys/puppets/",
            "subcategory": "toys-games/plush-toys/puppets",
        },
        "puppets-puppet-theaters": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/puppets-puppet-theaters/",
            "subcategory": "toys-games/creative-play/puppets-puppet-theaters",
        },
        "puzzle-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/puzzle-games/",
            "subcategory": "toys-games/games/puzzle-games",
        },
        "puzzles": {
            "url": "https://www.michaels.com/shop/kids/toys-games/puzzles/",
            "subcategory": "toys-games/puzzles",
        },
        "r-c": {
            "url": "https://www.michaels.com/shop/kids/toys-games/vehicles-trains-r-c/r-c/",
            "subcategory": "toys-games/vehicles-trains-r-c/r-c",
        },
        "racetracks-play-sets": {
            "url": "https://www.michaels.com/shop/kids/toys-games/vehicles-trains-r-c/racetracks-play-sets/",
            "subcategory": "toys-games/vehicles-trains-r-c/racetracks-play-sets",
        },
        "reindeer-handprint-tee": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/reindeer-handprint-tee/",
            "subcategory": "kids-crafting/winter-workshop/reindeer-handprint-tee",
        },
        "reptiles-bugs": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/reptiles-bugs/",
            "subcategory": "toys-games/figurines/reptiles-bugs",
        },
        "riding-toys": {
            "url": "https://www.michaels.com/shop/kids/toys-games/active-play/outdoor-play/riding-toys/",
            "subcategory": "toys-games/active-play/outdoor-play/riding-toys",
        },
        "robots": {
            "url": "https://www.michaels.com/shop/kids/toys-games/vehicles-trains-r-c/robots/",
            "subcategory": "toys-games/vehicles-trains-r-c/robots",
        },
        "robots-technology": {
            "url": "https://www.michaels.com/shop/kids/steam/robots-technology/",
            "subcategory": "steam/robots-technology",
        },
        "rocket-ship-rolls": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/rocket-ship-rolls/",
            "subcategory": "kids-crafting/camp-creatology/rocket-ship-rolls",
        },
        "rocking-plush": {
            "url": "https://www.michaels.com/shop/kids/toys-games/plush-toys/rocking-plush/",
            "subcategory": "toys-games/plush-toys/rocking-plush",
        },
        "roll": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/stickers/roll/",
            "subcategory": "kids-crafting/embellishments/stickers/roll",
        },
        "scented-coloring": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/drawing-coloring/scented-coloring/",
            "subcategory": "art-supplies/drawing-coloring/scented-coloring",
        },
        "scented-dough": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/scented-dough/",
            "subcategory": "sensory-play/scented-dough",
        },
        "school-project-supplies": {
            "url": "https://www.michaels.com/shop/kids/steam/school-project-supplies/",
            "subcategory": "steam/school-project-supplies",
        },
        "sea-creatures": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/sea-creatures/",
            "subcategory": "toys-games/figurines/sea-creatures",
        },
        "seasonal-crafts": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-activities/seasonal-crafts/",
            "subcategory": "kids-crafting/craft-activities/seasonal-crafts",
        },
        "seasonal-slider-card": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/seasonal-slider-card/",
            "subcategory": "kids-crafting/winter-workshop/seasonal-slider-card",
        },
        "sensory-bins": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sensory-bins/",
            "subcategory": "sensory-play/sensory-bins",
        },
        "sensory-play": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/",
            "subcategory": "sensory-play",
        },
        "sets-kits": {
            "url": "https://www.michaels.com/shop/kids/sensory-play/sets-kits/",
            "subcategory": "sensory-play/sets-kits",
        },
        "sewing-weaving-kits": {
            "url": "https://www.michaels.com/shop/kids/activity-kits/sewing-weaving-kits/",
            "subcategory": "activity-kits/sewing-weaving-kits",
        },
        "shaped-embellishments": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/shaped-embellishments/",
            "subcategory": "kids-crafting/embellishments/shaped-embellishments",
        },
        "snowball-wall-of-frame": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/snowball-wall-of-frame/",
            "subcategory": "kids-crafting/winter-workshop/snowball-wall-of-frame",
        },
        "snowman-pinch-pot": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/snowman-pinch-pot/",
            "subcategory": "kids-crafting/winter-workshop/snowman-pinch-pot",
        },
        "soft-blocks": {
            "url": "https://www.michaels.com/shop/kids/building-toys/soft-blocks/",
            "subcategory": "building-toys/soft-blocks",
        },
        "steam": {
            "url": "https://www.michaels.com/shop/kids/steam/",
            "subcategory": "steam",
        },
        "steam-toys": {
            "url": "https://www.michaels.com/shop/kids/steam/steam-toys/",
            "subcategory": "steam/steam-toys",
        },
        "stem-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/learning-games/stem-games/",
            "subcategory": "toys-games/games/learning-games/stem-games",
        },
        "sticker-kits": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/stickers/sticker-kits/",
            "subcategory": "kids-crafting/embellishments/stickers/sticker-kits",
        },
        "sticker-sheets": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/embellishments/stickers/sticker-sheets/",
            "subcategory": "kids-crafting/embellishments/stickers/sticker-sheets",
        },
        "sticky-back": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-surfaces/foam/sticky-back/",
            "subcategory": "kids-crafting/craft-surfaces/foam/sticky-back",
        },
        "store-it": {
            "url": "https://www.michaels.com/shop/kids/slime/store-it/",
            "subcategory": "slime/store-it",
        },
        "story-books": {
            "url": "https://www.michaels.com/shop/kids/books/story-books/",
            "subcategory": "books/story-books",
        },
        "strategy-skill": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/strategy-skill/",
            "subcategory": "toys-games/games/board-games/strategy-skill",
        },
        "summer-foodie-banners": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/summer-foodie-banners/",
            "subcategory": "kids-crafting/camp-creatology/summer-foodie-banners",
        },
        "suncatchers": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/craft-activities/suncatchers/",
            "subcategory": "kids-crafting/craft-activities/suncatchers",
        },
        "tables-desks": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/kids-furniture/tables-desks/",
            "subcategory": "furniture-decor/kids-furniture/tables-desks",
        },
        "themed": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/play-sets-play-food/themed/",
            "subcategory": "toys-games/creative-play/play-sets-play-food/themed",
        },
        "toddler-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/toddler-games/",
            "subcategory": "toys-games/games/toddler-games",
        },
        "toy-storage": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/kids-furniture/toy-storage/",
            "subcategory": "furniture-decor/kids-furniture/toy-storage",
        },
        "toys-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/",
            "subcategory": "toys-games",
        },
        "trains": {
            "url": "https://www.michaels.com/shop/kids/toys-games/creative-play/play-sets-play-food/trains/",
            "subcategory": "toys-games/creative-play/play-sets-play-food/trains",
        },
        "travel-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/travel-games/",
            "subcategory": "toys-games/games/board-games/travel-games",
        },
        "trivia": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/trivia/",
            "subcategory": "toys-games/games/board-games/trivia",
        },
        "tunnels-tents": {
            "url": "https://www.michaels.com/shop/kids/toys-games/active-play/tunnels-tents/",
            "subcategory": "toys-games/active-play/tunnels-tents",
        },
        "unfinished-wood-shapes": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/unfinished-wood-shapes/",
            "subcategory": "kids-crafting/wood-crafts/unfinished-wood-shapes",
        },
        "unfinished-wood-toys": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/wood-crafts/unfinished-wood-toys/",
            "subcategory": "kids-crafting/wood-crafts/unfinished-wood-toys",
        },
        "vehicles-trains-r-c": {
            "url": "https://www.michaels.com/shop/kids/toys-games/vehicles-trains-r-c/",
            "subcategory": "toys-games/vehicles-trains-r-c",
        },
        "wall-decals": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/wall-decor/wall-decals/",
            "subcategory": "furniture-decor/wall-decor/wall-decals",
        },
        "wall-murals-borders": {
            "url": "https://www.michaels.com/shop/kids/furniture-decor/wall-decor/wall-murals-borders/",
            "subcategory": "furniture-decor/wall-decor/wall-murals-borders",
        },
        "washable-tempera-paint": {
            "url": "https://www.michaels.com/shop/kids/art-supplies/painting/paint/washable-tempera-paint/",
            "subcategory": "art-supplies/painting/paint/washable-tempera-paint",
        },
        "western": {
            "url": "https://www.michaels.com/shop/kids/toys-games/figurines/western/",
            "subcategory": "toys-games/figurines/western",
        },
        "winter-watercolor-keychains": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/winter-watercolor-keychains/",
            "subcategory": "kids-crafting/winter-workshop/winter-watercolor-keychains",
        },
        "winter-workshop": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/winter-workshop/",
            "subcategory": "kids-crafting/winter-workshop",
        },
        "wood-blocks": {
            "url": "https://www.michaels.com/shop/kids/building-toys/wood-blocks/",
            "subcategory": "building-toys/wood-blocks",
        },
        "wooden-space-pals": {
            "url": "https://www.michaels.com/shop/kids/kids-crafting/camp-creatology/wooden-space-pals/",
            "subcategory": "kids-crafting/camp-creatology/wooden-space-pals",
        },
        "word-games": {
            "url": "https://www.michaels.com/shop/kids/toys-games/games/board-games/word-games/",
            "subcategory": "toys-games/games/board-games/word-games",
        },
    },
    "lemax-christmas-village": {
        "lemax-christmas-village-lemax-christmas-village": {
            "url": "https://www.michaels.com/shop/lemax-christmas-village/",
            "subcategory": "lemax-christmas-village",
        },
    },
    "lemax-spooky-town": {
        "lemax-spooky-town": {
            "url": "https://www.michaels.com/shop/lemax-spooky-town/",
            "subcategory": "lemax-spooky-town",
        },
    },
    "makerplace-personalization-shop": {
        "makerplace-personalization-shop": {
            "url": "https://www.michaels.com/shop/makerplace-personalization-shop/",
            "subcategory": "makerplace-personalization-shop",
        },
    },
    "michaelspro-buy-in-bulk": {
        "albums-accessories": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/albums-accessories/",
            "subcategory": "bulk-scrapbooking-papercraft/albums-accessories",
        },
        "artist-paint-mediums": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/artist-paint-mediums/",
            "subcategory": "bulk-art-supplies-paint/artist-paint-mediums",
        },
        "basic": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-yarn/basic/",
            "subcategory": "bulk-yarn/basic",
        },
        "basswood": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/basswood/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/basswood",
        },
        "birch": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/birch/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/birch",
        },
        "bracelet-chain-rings": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-findings/bracelet-chain-rings/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-findings/bracelet-chain-rings",
        },
        "brushes-painting-accessories": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/brushes-painting-accessories/",
            "subcategory": "bulk-art-supplies-paint/brushes-painting-accessories",
        },
        "bulk-apparel-crafts": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-apparel-crafts/",
            "subcategory": "bulk-apparel-crafts",
        },
        "bulk-art-supplies-paint": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/",
            "subcategory": "bulk-art-supplies-paint",
        },
        "bulk-beads-jewelry-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/",
            "subcategory": "bulk-beads-jewelry-supplies",
        },
        "bulk-canvas": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-canvas/",
            "subcategory": "bulk-canvas",
        },
        "bulk-crafts-hobbies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/",
            "subcategory": "bulk-crafts-hobbies",
        },
        "bulk-decor": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-decor/",
            "subcategory": "bulk-decor",
        },
        "bulk-floral-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/",
            "subcategory": "bulk-floral-supplies",
        },
        "bulk-frames": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/",
            "subcategory": "bulk-frames",
        },
        "bulk-kids-crafting-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/",
            "subcategory": "bulk-kids-crafting-supplies",
        },
        "bulk-office-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/",
            "subcategory": "bulk-office-supplies",
        },
        "bulk-party-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-party-supplies/",
            "subcategory": "bulk-party-supplies",
        },
        "bulk-ribbon": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-ribbon/",
            "subcategory": "bulk-ribbon",
        },
        "bulk-scrapbooking-papercraft": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/",
            "subcategory": "bulk-scrapbooking-papercraft",
        },
        "bulk-sewing-notions": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-sewing-notions/",
            "subcategory": "bulk-sewing-notions",
        },
        "bulk-storage": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-storage/",
            "subcategory": "bulk-storage",
        },
        "bulk-tech-accessories": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-tech-accessories/",
            "subcategory": "bulk-tech-accessories",
        },
        "bulk-wedding-favors-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-wedding-favors-supplies/",
            "subcategory": "bulk-wedding-favors-supplies",
        },
        "bulk-yarn": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-yarn/",
            "subcategory": "bulk-yarn",
        },
        "caron-cake-shop": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-yarn/caron-cake-shop/",
            "subcategory": "bulk-yarn/caron-cake-shop",
        },
        "chains-connectors": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/beads-jewelry/chains-connectors/",
            "subcategory": "bulk-kids-crafting-supplies/beads-jewelry/chains-connectors",
        },
        "chalkboard": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/chalkboard/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/chalkboard",
        },
        "chenille-pipe-cleaners": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/chenille-pipe-cleaners/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/chenille-pipe-cleaners",
        },
        "clasp-toggles-closures": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-findings/clasp-toggles-closures/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-findings/clasp-toggles-closures",
        },
        "clay-compounds": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/clay-compounds/",
            "subcategory": "bulk-kids-crafting-supplies/clay-compounds",
        },
        "craft-sticks-clothespins": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/craft-sticks-clothespins/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/craft-sticks-clothespins",
        },
        "craft-surfaces-masks": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/craft-surfaces-masks/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/craft-surfaces-masks",
        },
        "crystal-gems": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/crystal-gems/",
            "subcategory": "bulk-beads-jewelry-supplies/crystal-gems",
        },
        "easels-picture-stands-plate-holders": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/easels-picture-stands-plate-holders/",
            "subcategory": "bulk-frames/easels-picture-stands-plate-holders",
        },
        "fashion-jewelry-kits": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/activity-kits/fashion-jewelry-kits/",
            "subcategory": "bulk-kids-crafting-supplies/activity-kits/fashion-jewelry-kits",
        },
        "feathers-bells": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/feathers-bells/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/feathers-bells",
        },
        "for-kids-baby": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-yarn/for-kids-baby/",
            "subcategory": "bulk-yarn/for-kids-baby",
        },
        "garlands-wreaths": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/garlands-wreaths/",
            "subcategory": "bulk-floral-supplies/garlands-wreaths",
        },
        "gift-wrap": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-party-supplies/gift-wrap/",
            "subcategory": "bulk-party-supplies/gift-wrap",
        },
        "jewelry-stringing-materials": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-stringing-materials/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-stringing-materials",
        },
        "kids-paint-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/art-supplies/kids-paint-supplies/",
            "subcategory": "bulk-kids-crafting-supplies/art-supplies/kids-paint-supplies",
        },
        "markers-pens": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/markers-pens/",
            "subcategory": "bulk-art-supplies-paint/markers-pens",
        },
        "michaelspro-buy-in-bulk": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/",
            "subcategory": "michaelspro-buy-in-bulk",
        },
        "michaelspro-buy-in-bulk-accessories": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-tech-accessories/accessories/",
            "subcategory": "bulk-tech-accessories/accessories",
        },
        "michaelspro-buy-in-bulk-activity-kits": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/activity-kits/",
            "subcategory": "bulk-kids-crafting-supplies/activity-kits",
        },
        "michaelspro-buy-in-bulk-adhesives": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/adhesives/",
            "subcategory": "bulk-crafts-hobbies/adhesives",
        },
        "michaelspro-buy-in-bulk-art-kits": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/activity-kits/art-kits/",
            "subcategory": "bulk-kids-crafting-supplies/activity-kits/art-kits",
        },
        "michaelspro-buy-in-bulk-art-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/art-supplies/",
            "subcategory": "bulk-kids-crafting-supplies/art-supplies",
        },
        "michaelspro-buy-in-bulk-basic-office-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/",
            "subcategory": "bulk-office-supplies/basic-office-supplies",
        },
        "michaelspro-buy-in-bulk-beads": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/beads-jewelry/beads/",
            "subcategory": "bulk-kids-crafting-supplies/beads-jewelry/beads",
        },
        "michaelspro-buy-in-bulk-beads-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/beads/",
            "subcategory": "bulk-beads-jewelry-supplies/beads",
        },
        "michaelspro-buy-in-bulk-beads-jewelry": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/beads-jewelry/",
            "subcategory": "bulk-kids-crafting-supplies/beads-jewelry",
        },
        "michaelspro-buy-in-bulk-birdhouses": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/birdhouses/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/birdhouses",
        },
        "michaelspro-buy-in-bulk-brads": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/brads/",
            "subcategory": "bulk-scrapbooking-papercraft/brads",
        },
        "michaelspro-buy-in-bulk-candle-holders": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-decor/candle-holders/",
            "subcategory": "bulk-decor/candle-holders",
        },
        "michaelspro-buy-in-bulk-candles": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-decor/candles/",
            "subcategory": "bulk-decor/candles",
        },
        "michaelspro-buy-in-bulk-card-making": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/card-making/",
            "subcategory": "bulk-scrapbooking-papercraft/card-making",
        },
        "michaelspro-buy-in-bulk-chargers": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-decor/chargers/",
            "subcategory": "bulk-decor/chargers",
        },
        "michaelspro-buy-in-bulk-charms": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/beads-jewelry/charms/",
            "subcategory": "bulk-kids-crafting-supplies/beads-jewelry/charms",
        },
        "michaelspro-buy-in-bulk-clothespins": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/clothespins/",
            "subcategory": "bulk-scrapbooking-papercraft/clothespins",
        },
        "michaelspro-buy-in-bulk-construction-paper": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/construction-paper/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/construction-paper",
        },
        "michaelspro-buy-in-bulk-craft-activities": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/craft-activities/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/craft-activities",
        },
        "michaelspro-buy-in-bulk-craft-paint": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/craft-paint/",
            "subcategory": "bulk-crafts-hobbies/craft-paint",
        },
        "michaelspro-buy-in-bulk-craft-paper": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/craft-paper/",
            "subcategory": "bulk-scrapbooking-papercraft/craft-paper",
        },
        "michaelspro-buy-in-bulk-craft-paper-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/craft-paper/craft-paper/",
            "subcategory": "bulk-scrapbooking-papercraft/craft-paper/craft-paper",
        },
        "michaelspro-buy-in-bulk-crates-boxes": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/crates-boxes/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/crates-boxes",
        },
        "michaelspro-buy-in-bulk-cutting-tools": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/cutting-tools/",
            "subcategory": "bulk-crafts-hobbies/cutting-tools",
        },
        "michaelspro-buy-in-bulk-drawing-coloring": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/art-supplies/drawing-coloring/",
            "subcategory": "bulk-kids-crafting-supplies/art-supplies/drawing-coloring",
        },
        "michaelspro-buy-in-bulk-drawing-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/drawing-supplies/",
            "subcategory": "bulk-art-supplies-paint/drawing-supplies",
        },
        "michaelspro-buy-in-bulk-drinkware": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/drinkware/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/drinkware",
        },
        "michaelspro-buy-in-bulk-earrings": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-findings/earrings/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-findings/earrings",
        },
        "michaelspro-buy-in-bulk-eye-head-pins": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-findings/eye-head-pins/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-findings/eye-head-pins",
        },
        "michaelspro-buy-in-bulk-felt": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/felt/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/felt",
        },
        "michaelspro-buy-in-bulk-fillers": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/fillers/",
            "subcategory": "bulk-floral-supplies/fillers",
        },
        "michaelspro-buy-in-bulk-foam": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/foam/",
            "subcategory": "bulk-floral-supplies/foam",
        },
        "michaelspro-buy-in-bulk-foam-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/foam/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/foam",
        },
        "michaelspro-buy-in-bulk-foam-fiber": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-sewing-notions/foam-fiber/",
            "subcategory": "bulk-sewing-notions/foam-fiber",
        },
        "michaelspro-buy-in-bulk-frame-mats": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/frame-mats/",
            "subcategory": "bulk-frames/frame-mats",
        },
        "michaelspro-buy-in-bulk-glitter": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/glitter/",
            "subcategory": "bulk-scrapbooking-papercraft/glitter",
        },
        "michaelspro-buy-in-bulk-glitter-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/glitter/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/glitter",
        },
        "michaelspro-buy-in-bulk-glue": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/glue/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/glue",
        },
        "michaelspro-buy-in-bulk-glue-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/adhesives/glue/",
            "subcategory": "bulk-crafts-hobbies/adhesives/glue",
        },
        "michaelspro-buy-in-bulk-hardware": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/hardware/",
            "subcategory": "bulk-frames/hardware",
        },
        "michaelspro-buy-in-bulk-ink": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/ink/",
            "subcategory": "bulk-scrapbooking-papercraft/ink",
        },
        "michaelspro-buy-in-bulk-jewelry-findings": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-findings/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-findings",
        },
        "michaelspro-buy-in-bulk-journals": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/journals/",
            "subcategory": "bulk-art-supplies-paint/journals",
        },
        "michaelspro-buy-in-bulk-jump-split-double-rings": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-findings/jump-split-double-rings/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-findings/jump-split-double-rings",
        },
        "michaelspro-buy-in-bulk-kids-art-storage": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/art-supplies/kids-art-storage/",
            "subcategory": "bulk-kids-crafting-supplies/art-supplies/kids-art-storage",
        },
        "michaelspro-buy-in-bulk-kids-crafting": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting",
        },
        "michaelspro-buy-in-bulk-leather-crafting": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/leather-crafting/",
            "subcategory": "bulk-crafts-hobbies/leather-crafting",
        },
        "michaelspro-buy-in-bulk-letters-numbers": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/letters-numbers/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/letters-numbers",
        },
        "michaelspro-buy-in-bulk-lighting": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-decor/lighting/",
            "subcategory": "bulk-decor/lighting",
        },
        "michaelspro-buy-in-bulk-markers": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/pens-pencils-markers/markers/",
            "subcategory": "bulk-office-supplies/basic-office-supplies/pens-pencils-markers/markers",
        },
        "michaelspro-buy-in-bulk-mason-jars": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/mason-jars/",
            "subcategory": "bulk-floral-supplies/mason-jars",
        },
        "michaelspro-buy-in-bulk-materials": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-tech-accessories/materials/",
            "subcategory": "bulk-tech-accessories/materials",
        },
        "michaelspro-buy-in-bulk-mediums": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/craft-paint/mediums/",
            "subcategory": "bulk-crafts-hobbies/craft-paint/mediums",
        },
        "michaelspro-buy-in-bulk-mini-frames": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/mini-frames/",
            "subcategory": "bulk-frames/mini-frames",
        },
        "michaelspro-buy-in-bulk-mixed-media-sets": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/art-supplies/mixed-media-sets/",
            "subcategory": "bulk-kids-crafting-supplies/art-supplies/mixed-media-sets",
        },
        "michaelspro-buy-in-bulk-paper": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/paper/",
            "subcategory": "bulk-office-supplies/basic-office-supplies/paper",
        },
        "michaelspro-buy-in-bulk-paper-pads": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/paper-pads/",
            "subcategory": "bulk-art-supplies-paint/paper-pads",
        },
        "michaelspro-buy-in-bulk-paper-pads-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/craft-paper/paper-pads/",
            "subcategory": "bulk-scrapbooking-papercraft/craft-paper/paper-pads",
        },
        "michaelspro-buy-in-bulk-pencils": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/pencils/",
            "subcategory": "bulk-art-supplies-paint/pencils",
        },
        "michaelspro-buy-in-bulk-pencils-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/pens-pencils-markers/pencils/",
            "subcategory": "bulk-office-supplies/basic-office-supplies/pens-pencils-markers/pencils",
        },
        "michaelspro-buy-in-bulk-pens": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/pens-pencils-markers/pens/",
            "subcategory": "bulk-office-supplies/basic-office-supplies/pens-pencils-markers/pens",
        },
        "michaelspro-buy-in-bulk-pens-pencils-markers": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/pens-pencils-markers/",
            "subcategory": "bulk-office-supplies/basic-office-supplies/pens-pencils-markers",
        },
        "michaelspro-buy-in-bulk-pom-poms": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/pom-poms/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/pom-poms",
        },
        "michaelspro-buy-in-bulk-poster-frames": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/poster-frames/",
            "subcategory": "bulk-frames/poster-frames",
        },
        "michaelspro-buy-in-bulk-project-tape": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/adhesives/project-tape/",
            "subcategory": "bulk-crafts-hobbies/adhesives/project-tape",
        },
        "michaelspro-buy-in-bulk-safety-bar-pins": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-beads-jewelry-supplies/jewelry-findings/safety-bar-pins/",
            "subcategory": "bulk-beads-jewelry-supplies/jewelry-findings/safety-bar-pins",
        },
        "michaelspro-buy-in-bulk-school-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/school-supplies/",
            "subcategory": "bulk-kids-crafting-supplies/school-supplies",
        },
        "michaelspro-buy-in-bulk-science-kits": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/activity-kits/science-kits/",
            "subcategory": "bulk-kids-crafting-supplies/activity-kits/science-kits",
        },
        "michaelspro-buy-in-bulk-sculpture-modeling": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/sculpture-modeling/",
            "subcategory": "bulk-art-supplies-paint/sculpture-modeling",
        },
        "michaelspro-buy-in-bulk-sequins": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/sequins/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/sequins",
        },
        "michaelspro-buy-in-bulk-shadow-boxes-display-cases": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/shadow-boxes-display-cases/",
            "subcategory": "bulk-frames/shadow-boxes-display-cases",
        },
        "michaelspro-buy-in-bulk-stickers": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/stickers/",
            "subcategory": "bulk-scrapbooking-papercraft/stickers",
        },
        "michaelspro-buy-in-bulk-sticky-notes": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/paper/sticky-notes/",
            "subcategory": "bulk-office-supplies/basic-office-supplies/paper/sticky-notes",
        },
        "michaelspro-buy-in-bulk-stringing-materials": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/beads-jewelry/stringing-materials/",
            "subcategory": "bulk-kids-crafting-supplies/beads-jewelry/stringing-materials",
        },
        "michaelspro-buy-in-bulk-surfaces": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces",
        },
        "michaelspro-buy-in-bulk-t-shirts": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-apparel-crafts/t-shirts/",
            "subcategory": "bulk-apparel-crafts/t-shirts",
        },
        "michaelspro-buy-in-bulk-tie-dye-fabric-dye": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-apparel-crafts/tie-dye-fabric-dye/",
            "subcategory": "bulk-apparel-crafts/tie-dye-fabric-dye",
        },
        "michaelspro-buy-in-bulk-uncut-matboard": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/frame-mats/uncut-matboard/",
            "subcategory": "bulk-frames/frame-mats/uncut-matboard",
        },
        "michaelspro-buy-in-bulk-unfinished-decor": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor",
        },
        "michaelspro-buy-in-bulk-unfinished-frames": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/unfinished-frames/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/unfinished-frames",
        },
        "michaelspro-buy-in-bulk-unfinished-frames-2": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-frames/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-frames",
        },
        "michaelspro-buy-in-bulk-vases-containers": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/vases-containers/",
            "subcategory": "bulk-floral-supplies/vases-containers",
        },
        "michaelspro-buy-in-bulk-wall-frames": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/wall-frames/",
            "subcategory": "bulk-frames/wall-frames",
        },
        "michaelspro-buy-in-bulk-wood-burning-carving": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/wood-burning-carving/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/wood-burning-carving",
        },
        "michaelspro-buy-in-bulk-wood-crafts": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/kids-crafting/wood-crafts/",
            "subcategory": "bulk-kids-crafting-supplies/kids-crafting/wood-crafts",
        },
        "michaelspro-buy-in-bulk-wood-hardboard-panels": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/wood-hardboard-panels/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/wood-hardboard-panels",
        },
        "michaelspro-buy-in-bulk-words-shapes": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/words-shapes/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/words-shapes",
        },
        "naturals": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/naturals/",
            "subcategory": "bulk-floral-supplies/naturals",
        },
        "other-embellishments": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/other-embellishments/",
            "subcategory": "bulk-scrapbooking-papercraft/other-embellishments",
        },
        "other-unfinished-decor": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/other-unfinished-decor/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/other-unfinished-decor",
        },
        "paint-pens-chalk-pens": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/craft-paint/paint-pens-chalk-pens/",
            "subcategory": "bulk-crafts-hobbies/craft-paint/paint-pens-chalk-pens",
        },
        "plaques": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/plaques/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/plaques",
        },
        "rhinestones": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/rhinestones/",
            "subcategory": "bulk-scrapbooking-papercraft/rhinestones",
        },
        "sand-slime": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-kids-crafting-supplies/clay-compounds/sand-slime/",
            "subcategory": "bulk-kids-crafting-supplies/clay-compounds/sand-slime",
        },
        "slate-ceramics": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/slate-ceramics/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/surfaces/slate-ceramics",
        },
        "social-stationery": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-scrapbooking-papercraft/craft-paper/social-stationery/",
            "subcategory": "bulk-scrapbooking-papercraft/craft-paper/social-stationery",
        },
        "staples-accessories": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-office-supplies/basic-office-supplies/staples-accessories/",
            "subcategory": "bulk-office-supplies/basic-office-supplies/staples-accessories",
        },
        "stems-bushes": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/stems-bushes/",
            "subcategory": "bulk-floral-supplies/stems-bushes",
        },
        "studio-presentation-supplies": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-art-supplies-paint/studio-presentation-supplies/",
            "subcategory": "bulk-art-supplies-paint/studio-presentation-supplies",
        },
        "supplies-accessories": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-floral-supplies/supplies-accessories/",
            "subcategory": "bulk-floral-supplies/supplies-accessories",
        },
        "surfaces-plaques": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/surfaces-plaques",
        },
        "tabletop-frames": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-frames/tabletop-frames/",
            "subcategory": "bulk-frames/tabletop-frames",
        },
        "tools-accessoires": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/tools-accessoires/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/tools-accessoires",
        },
        "turnings": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/turnings/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/turnings",
        },
        "unfinished-pallet-signs": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/unfinished-signs/unfinished-pallet-signs/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/unfinished-signs/unfinished-pallet-signs",
        },
        "unfinished-signs": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/unfinished-signs/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/unfinished-signs",
        },
        "wood-crafts-blank-surfaces": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces",
        },
        "wood-plaques": {
            "url": "https://www.michaels.com/shop/michaelspro-buy-in-bulk/bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/wood-plaques/",
            "subcategory": "bulk-crafts-hobbies/wood-crafts-blank-surfaces/unfinished-decor/wood-plaques",
        },
    },
    "office-supplies": {
        "badges-lanyards": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/badges-lanyards/",
            "subcategory": "office-supplies/badges-lanyards",
        },
        "batteries": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/batteries/",
            "subcategory": "electronics/batteries",
        },
        "binders": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/folders/binders/",
            "subcategory": "office-supplies/folders/binders",
        },
        "break-room-supplies": {
            "url": "https://www.michaels.com/shop/office-supplies/break-room-supplies/",
            "subcategory": "break-room-supplies",
        },
        "business-cards": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/business-cards/",
            "subcategory": "paper/business-cards",
        },
        "calendars-planners": {
            "url": "https://www.michaels.com/shop/office-supplies/calendars-planners/",
            "subcategory": "calendars-planners",
        },
        "cardstock": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/cardstock/",
            "subcategory": "paper/cardstock",
        },
        "carts": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/carts/",
            "subcategory": "furniture-storage/carts",
        },
        "chalkboards": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/chalkboards/",
            "subcategory": "whiteboards-corkboards/chalkboards",
        },
        "clipboards": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/clipboards/",
            "subcategory": "office-supplies/basic-office-supplies/clipboards",
        },
        "clips": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/clips/",
            "subcategory": "office-supplies/basic-office-supplies/clips",
        },
        "coffee-storage": {
            "url": "https://www.michaels.com/shop/office-supplies/break-room-supplies/coffee-storage/",
            "subcategory": "break-room-supplies/coffee-storage",
        },
        "computer-accessories": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/computer-accessories/",
            "subcategory": "electronics/computer-accessories",
        },
        "computer-paper": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/computer-paper/",
            "subcategory": "paper/computer-paper",
        },
        "contact-paper": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/contact-paper/",
            "subcategory": "office-supplies/basic-office-supplies/contact-paper",
        },
        "cork-boards": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/cork-boards/",
            "subcategory": "whiteboards-corkboards/cork-boards",
        },
        "correction-fluid-tape": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/correction-fluid-tape/",
            "subcategory": "pens-pencils-markers/correction-fluid-tape",
        },
        "desk-accessories": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/desk-accessories/",
            "subcategory": "office-supplies/desk-accessories",
        },
        "desk-calendars": {
            "url": "https://www.michaels.com/shop/office-supplies/calendars-planners/desk-calendars/",
            "subcategory": "calendars-planners/desk-calendars",
        },
        "drawing-instruments": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/drawing-instruments/",
            "subcategory": "office-supplies/basic-office-supplies/drawing-instruments",
        },
        "dry-erase-accessories": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/dry-erase-accessories/",
            "subcategory": "whiteboards-corkboards/dry-erase-accessories",
        },
        "dry-erase-markers": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/dry-erase-markers/",
            "subcategory": "whiteboards-corkboards/dry-erase-markers",
        },
        "fabric-bulletin-boards": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/fabric-bulletin-boards/",
            "subcategory": "whiteboards-corkboards/fabric-bulletin-boards",
        },
        "fasteners": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/fasteners/",
            "subcategory": "office-supplies/basic-office-supplies/fasteners",
        },
        "file-folders": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/folders/file-folders/",
            "subcategory": "office-supplies/folders/file-folders",
        },
        "file-storage": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/file-storage/",
            "subcategory": "furniture-storage/file-storage",
        },
        "filler-graph-paper": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/filler-graph-paper/",
            "subcategory": "paper/filler-graph-paper",
        },
        "furniture-storage": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/",
            "subcategory": "furniture-storage",
        },
        "headphones": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/headphones/",
            "subcategory": "electronics/headphones",
        },
        "index-cards": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/index-cards/",
            "subcategory": "paper/index-cards",
        },
        "keyboards": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/keyboards/",
            "subcategory": "electronics/keyboards",
        },
        "laminators-supplies": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/laminators-supplies/",
            "subcategory": "electronics/laminators-supplies",
        },
        "lap-desks": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/lap-desks/",
            "subcategory": "furniture-storage/lap-desks",
        },
        "mailers": {
            "url": "https://www.michaels.com/shop/office-supplies/packing-shipping/mailers/",
            "subcategory": "packing-shipping/mailers",
        },
        "mailing-labels": {
            "url": "https://www.michaels.com/shop/office-supplies/packing-shipping/mailing-labels/",
            "subcategory": "packing-shipping/mailing-labels",
        },
        "monitor-stands": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/monitor-stands/",
            "subcategory": "furniture-storage/monitor-stands",
        },
        "notebooks": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/notebooks/",
            "subcategory": "paper/notebooks",
        },
        "notepads": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/notepads/",
            "subcategory": "paper/notepads",
        },
        "office-chairs": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/office-chairs/",
            "subcategory": "furniture-storage/office-chairs",
        },
        "office-organization": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/office-storage/office-organization/",
            "subcategory": "furniture-storage/office-storage/office-organization",
        },
        "office-storage": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/office-storage/",
            "subcategory": "furniture-storage/office-storage",
        },
        "office-supplies-adhesives-magnets": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/adhesives-magnets/",
            "subcategory": "office-supplies/adhesives-magnets",
        },
        "office-supplies-basic-office-supplies": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/",
            "subcategory": "office-supplies/basic-office-supplies",
        },
        "office-supplies-boxes": {
            "url": "https://www.michaels.com/shop/office-supplies/packing-shipping/boxes/",
            "subcategory": "packing-shipping/boxes",
        },
        "office-supplies-calculators": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/calculators/",
            "subcategory": "electronics/calculators",
        },
        "office-supplies-desks": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/desks/",
            "subcategory": "furniture-storage/desks",
        },
        "office-supplies-desktop-storage": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/desktop-storage/",
            "subcategory": "furniture-storage/desktop-storage",
        },
        "office-supplies-dry-erase-boards": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/dry-erase-boards/",
            "subcategory": "whiteboards-corkboards/dry-erase-boards",
        },
        "office-supplies-easel-pads": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/easel-pads/",
            "subcategory": "paper/easel-pads",
        },
        "office-supplies-electronics": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/",
            "subcategory": "electronics",
        },
        "office-supplies-envelopes": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/envelopes/",
            "subcategory": "paper/envelopes",
        },
        "office-supplies-envelopes-2": {
            "url": "https://www.michaels.com/shop/office-supplies/packing-shipping/envelopes/",
            "subcategory": "packing-shipping/envelopes",
        },
        "office-supplies-erasers": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/erasers/",
            "subcategory": "pens-pencils-markers/erasers",
        },
        "office-supplies-folders": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/folders/folders/",
            "subcategory": "office-supplies/folders/folders",
        },
        "office-supplies-folders-2": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/folders/",
            "subcategory": "office-supplies/folders",
        },
        "office-supplies-highlighters": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/highlighters/",
            "subcategory": "pens-pencils-markers/highlighters",
        },
        "office-supplies-hooks": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/hooks/",
            "subcategory": "furniture-storage/hooks",
        },
        "office-supplies-label-makers": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/label-makers/",
            "subcategory": "electronics/label-makers",
        },
        "office-supplies-labels": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/labels/",
            "subcategory": "paper/labels",
        },
        "office-supplies-lamps-lighting": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/lamps-lighting/",
            "subcategory": "furniture-storage/lamps-lighting",
        },
        "office-supplies-markers": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/markers/",
            "subcategory": "pens-pencils-markers/markers",
        },
        "office-supplies-office-supplies": {
            "url": "https://www.michaels.com/shop/office-supplies/",
            "subcategory": "office-supplies",
        },
        "office-supplies-office-supplies-2": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/",
            "subcategory": "office-supplies",
        },
        "office-supplies-paper": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/",
            "subcategory": "paper",
        },
        "office-supplies-pencils": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/pencils/",
            "subcategory": "pens-pencils-markers/pencils",
        },
        "office-supplies-pens": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/pens/",
            "subcategory": "pens-pencils-markers/pens",
        },
        "office-supplies-pens-pencils-markers": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/",
            "subcategory": "pens-pencils-markers",
        },
        "office-supplies-planners": {
            "url": "https://www.michaels.com/shop/office-supplies/calendars-planners/planners/",
            "subcategory": "calendars-planners/planners",
        },
        "office-supplies-portfolios": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/portfolios/",
            "subcategory": "furniture-storage/portfolios",
        },
        "office-supplies-push-pins": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/push-pins/",
            "subcategory": "whiteboards-corkboards/push-pins",
        },
        "office-supplies-rulers": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/rulers/",
            "subcategory": "office-supplies/basic-office-supplies/rulers",
        },
        "office-supplies-scissors": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/scissors/",
            "subcategory": "office-supplies/basic-office-supplies/scissors",
        },
        "office-supplies-shelving": {
            "url": "https://www.michaels.com/shop/office-supplies/furniture-storage/shelving/",
            "subcategory": "furniture-storage/shelving",
        },
        "office-supplies-stamps-stamp-pads": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/stamps-stamp-pads/",
            "subcategory": "office-supplies/basic-office-supplies/stamps-stamp-pads",
        },
        "office-supplies-sticky-notes": {
            "url": "https://www.michaels.com/shop/office-supplies/paper/sticky-notes/",
            "subcategory": "paper/sticky-notes",
        },
        "packing-shipping": {
            "url": "https://www.michaels.com/shop/office-supplies/packing-shipping/",
            "subcategory": "packing-shipping",
        },
        "packing-supplies": {
            "url": "https://www.michaels.com/shop/office-supplies/packing-shipping/packing-supplies/",
            "subcategory": "packing-shipping/packing-supplies",
        },
        "paper-punches-cutters": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/paper-punches-cutters/",
            "subcategory": "office-supplies/basic-office-supplies/paper-punches-cutters",
        },
        "pencil-grips": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/pencil-grips/",
            "subcategory": "pens-pencils-markers/pencil-grips",
        },
        "pencil-sharpeners": {
            "url": "https://www.michaels.com/shop/office-supplies/pens-pencils-markers/pencil-sharpeners/",
            "subcategory": "pens-pencils-markers/pencil-sharpeners",
        },
        "rubber-bands": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/rubber-bands/",
            "subcategory": "office-supplies/basic-office-supplies/rubber-bands",
        },
        "sheet-protectors": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/sheet-protectors/",
            "subcategory": "office-supplies/basic-office-supplies/sheet-protectors",
        },
        "shredders": {
            "url": "https://www.michaels.com/shop/office-supplies/electronics/shredders/",
            "subcategory": "electronics/shredders",
        },
        "staplers-accessories": {
            "url": "https://www.michaels.com/shop/office-supplies/office-supplies/basic-office-supplies/staplers-accessories/",
            "subcategory": "office-supplies/basic-office-supplies/staplers-accessories",
        },
        "wall-calendars": {
            "url": "https://www.michaels.com/shop/office-supplies/calendars-planners/wall-calendars/",
            "subcategory": "calendars-planners/wall-calendars",
        },
        "whiteboards-corkboards": {
            "url": "https://www.michaels.com/shop/office-supplies/whiteboards-corkboards/",
            "subcategory": "whiteboards-corkboards",
        },
    },
    "paint": {
        "acrylic-craft-paint": {
            "url": "https://www.michaels.com/shop/paint/acrylic-craft-paint/",
            "subcategory": "acrylic-craft-paint",
        },
        "paint-paint": {
            "url": "https://www.michaels.com/shop/paint/",
            "subcategory": "paint",
        },
    },
    "papercraft": {
        "academic-year-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/academic-year-planners/",
            "subcategory": "planners/specialized-planners/academic-year-planners",
        },
        "adhesive-dots-squares": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/adhesives/adhesive-dots-squares/",
            "subcategory": "tools-adhesives/adhesives/adhesive-dots-squares",
        },
        "adhesive-sheets": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/adhesives/adhesive-sheets/",
            "subcategory": "tools-adhesives/adhesives/adhesive-sheets",
        },
        "albums-refills": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/",
            "subcategory": "albums-refills",
        },
        "animals-bugs": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/animals-bugs/",
            "subcategory": "stickers/animals-bugs",
        },
        "animals-insects": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/cling-stamps/animals-insects/",
            "subcategory": "stamps-embossing/cling-stamps/animals-insects",
        },
        "big-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/planner-books/big-planners/",
            "subcategory": "planners/the-happy-planner/planner-books/big-planners",
        },
        "binder-rings": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/companion-accessories/binder-rings/",
            "subcategory": "planners/the-happy-planner/companion-accessories/binder-rings",
        },
        "bling": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/bling/",
            "subcategory": "embellishments/bling",
        },
        "bling-pearls": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/bling-pearls/",
            "subcategory": "stickers/bling-pearls",
        },
        "book-binding": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/book-binding/",
            "subcategory": "tools-adhesives/book-binding",
        },
        "buttons-eyelets": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/buttons-eyelets/",
            "subcategory": "tools-adhesives/buttons-eyelets",
        },
        "card-kits": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/card-kits/",
            "subcategory": "card-making/card-kits",
        },
        "card-making-dies": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/card-making-dies/",
            "subcategory": "card-making/card-making-dies",
        },
        "cardstock-paper": {
            "url": "https://www.michaels.com/shop/papercraft/paper/cardstock-paper/",
            "subcategory": "paper/cardstock-paper",
        },
        "carpe-diem": {
            "url": "https://www.michaels.com/shop/papercraft/planners/collections/carpe-diem/",
            "subcategory": "planners/collections/carpe-diem",
        },
        "celebrations-food": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/celebrations-food/",
            "subcategory": "stickers/celebrations-food",
        },
        "certificate-paper": {
            "url": "https://www.michaels.com/shop/papercraft/paper/certificate-paper/",
            "subcategory": "paper/certificate-paper",
        },
        "character-stickers": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/character-stickers/",
            "subcategory": "stickers/character-stickers",
        },
        "chipboard-albums": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/chipboard-albums/",
            "subcategory": "albums-refills/chipboard-albums",
        },
        "classic-glitter": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/glitter/classic-glitter/",
            "subcategory": "embellishments/glitter/classic-glitter",
        },
        "classic-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/planner-books/classic-planners/",
            "subcategory": "planners/the-happy-planner/planner-books/classic-planners",
        },
        "cling-stamps": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/cling-stamps/",
            "subcategory": "stamps-embossing/cling-stamps",
        },
        "collections": {
            "url": "https://www.michaels.com/shop/papercraft/planners/collections/",
            "subcategory": "planners/collections",
        },
        "companion-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/companion-accessories/",
            "subcategory": "planners/the-happy-planner/companion-accessories",
        },
        "congratulations": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/greeting-cards/congratulations/",
            "subcategory": "card-making/greeting-cards/congratulations",
        },
        "craft-knives": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/craft-knives/",
            "subcategory": "tools-adhesives/craft-knives",
        },
        "crafting-albums": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/crafting-albums/",
            "subcategory": "albums-refills/crafting-albums",
        },
        "creative-journaling": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/creative-journaling/",
            "subcategory": "ink-mixed-media/creative-journaling",
        },
        "cutting-mats-crafting-surfaces": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/cutting-mats-crafting-surfaces/",
            "subcategory": "tools-adhesives/cutting-mats-crafting-surfaces",
        },
        "d-ring-albums": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/d-ring-albums/",
            "subcategory": "albums-refills/d-ring-albums",
        },
        "decoupage": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/adhesives/decoupage/",
            "subcategory": "tools-adhesives/adhesives/decoupage",
        },
        "die-cuts-ephemera": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/die-cuts-ephemera/",
            "subcategory": "embellishments/die-cuts-ephemera",
        },
        "die-cutting": {
            "url": "https://www.michaels.com/shop/papercraft/die-cutting/",
            "subcategory": "die-cutting",
        },
        "die-cutting-machines": {
            "url": "https://www.michaels.com/shop/papercraft/die-cutting/die-cutting-machines/",
            "subcategory": "die-cutting/die-cutting-machines",
        },
        "dies": {
            "url": "https://www.michaels.com/shop/papercraft/die-cutting/dies/",
            "subcategory": "die-cutting/dies",
        },
        "dreamplando": {
            "url": "https://www.michaels.com/shop/papercraft/planners/collections/dreamplando/",
            "subcategory": "planners/collections/dreamplando",
        },
        "dylusions": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/mixed-media-collections/dylusions/",
            "subcategory": "ink-mixed-media/mixed-media-collections/dylusions",
        },
        "embossing": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/embossing/",
            "subcategory": "stamps-embossing/embossing",
        },
        "embossing-folders": {
            "url": "https://www.michaels.com/shop/papercraft/die-cutting/embossing-folders/",
            "subcategory": "die-cutting/embossing-folders",
        },
        "embossing-machines": {
            "url": "https://www.michaels.com/shop/papercraft/die-cutting/embossing-machines/",
            "subcategory": "die-cutting/embossing-machines",
        },
        "embossing-powder": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/embossing/embossing-powder/",
            "subcategory": "stamps-embossing/embossing/embossing-powder",
        },
        "embossing-tools": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/embossing/embossing-tools/",
            "subcategory": "stamps-embossing/embossing/embossing-tools",
        },
        "envelope-seals": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/envelope-seals/",
            "subcategory": "card-making/envelope-seals",
        },
        "faith-self-improvement-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/faith-self-improvement-planners/",
            "subcategory": "planners/specialized-planners/faith-self-improvement-planners",
        },
        "family": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/family/",
            "subcategory": "stickers/family",
        },
        "fashion-trend": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/fashion-trend/",
            "subcategory": "stickers/fashion-trend",
        },
        "fitness-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/fitness-planners/",
            "subcategory": "planners/specialized-planners/fitness-planners",
        },
        "floral-greenery": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/cling-stamps/floral-greenery/",
            "subcategory": "stamps-embossing/cling-stamps/floral-greenery",
        },
        "flower-shop": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/flower-shop/",
            "subcategory": "embellishments/flower-shop",
        },
        "flowers-nature": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/flowers-nature/",
            "subcategory": "stickers/flowers-nature",
        },
        "foil-application": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/foil-application/",
            "subcategory": "stamps-embossing/foil-application",
        },
        "foil-sheets": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/foil-application/foil-sheets/",
            "subcategory": "stamps-embossing/foil-application/foil-sheets",
        },
        "gel-printing": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/gel-printing/",
            "subcategory": "stamps-embossing/gel-printing",
        },
        "glitter-gels-sprays": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/glitter/glitter-gels-sprays/",
            "subcategory": "embellishments/glitter/glitter-gels-sprays",
        },
        "glitter-sets": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/glitter/glitter-sets/",
            "subcategory": "embellishments/glitter/glitter-sets",
        },
        "greeting-cards": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/greeting-cards/",
            "subcategory": "card-making/greeting-cards",
        },
        "heidi-swapp-memory-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/collections/heidi-swapp-memory-planners/",
            "subcategory": "planners/collections/heidi-swapp-memory-planners",
        },
        "holiday": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/greeting-cards/holiday/",
            "subcategory": "card-making/greeting-cards/holiday",
        },
        "holidays": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/holidays/",
            "subcategory": "stickers/holidays",
        },
        "hot-foil-plates": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/foil-application/hot-foil-plates/",
            "subcategory": "stamps-embossing/foil-application/hot-foil-plates",
        },
        "hourly-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/hourly-planners/",
            "subcategory": "planners/specialized-planners/hourly-planners",
        },
        "ink-mixed-media": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/",
            "subcategory": "ink-mixed-media",
        },
        "ink-pad-reinkers": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/ink-pads/ink-pad-reinkers/",
            "subcategory": "stamps-embossing/ink-pads/ink-pad-reinkers",
        },
        "ink-pads": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/ink-pads/",
            "subcategory": "stamps-embossing/ink-pads",
        },
        "inking-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/inks-accessories/inking-accessories/",
            "subcategory": "ink-mixed-media/inks-accessories/inking-accessories",
        },
        "inks-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/inks-accessories/",
            "subcategory": "ink-mixed-media/inks-accessories",
        },
        "jane-davenport": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/mixed-media-collections/jane-davenport/",
            "subcategory": "ink-mixed-media/mixed-media-collections/jane-davenport",
        },
        "journals-notebooks": {
            "url": "https://www.michaels.com/shop/papercraft/planners/journals-notebooks/",
            "subcategory": "planners/journals-notebooks",
        },
        "laminating": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/laminating/",
            "subcategory": "tools-adhesives/laminating",
        },
        "machines": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/foil-application/machines/",
            "subcategory": "stamps-embossing/foil-application/machines",
        },
        "metal-embellishments": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/metal-embellishments/",
            "subcategory": "embellishments/metal-embellishments",
        },
        "milestones": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/milestones/",
            "subcategory": "stickers/milestones",
        },
        "miscellaneous-stamps": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/cling-stamps/miscellaneous-stamps/",
            "subcategory": "stamps-embossing/cling-stamps/miscellaneous-stamps",
        },
        "mixed-media-collections": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/mixed-media-collections/",
            "subcategory": "ink-mixed-media/mixed-media-collections",
        },
        "monthly-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/monthly-planners/",
            "subcategory": "planners/monthly-planners",
        },
        "nature": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/cling-stamps/nature/",
            "subcategory": "stamps-embossing/cling-stamps/nature",
        },
        "notebooks-journals": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/companion-accessories/notebooks-journals/",
            "subcategory": "planners/the-happy-planner/companion-accessories/notebooks-journals",
        },
        "occupations-hobbies": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/occupations-hobbies/",
            "subcategory": "stickers/occupations-hobbies",
        },
        "organization-labels": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/organization-labels/",
            "subcategory": "stickers/organization-labels",
        },
        "origami": {
            "url": "https://www.michaels.com/shop/papercraft/paper/origami/",
            "subcategory": "paper/origami",
        },
        "other-papercraft-tools": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/other-papercraft-tools/",
            "subcategory": "tools-adhesives/other-papercraft-tools",
        },
        "outdoor-activities": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/outdoor-activities/",
            "subcategory": "stickers/outdoor-activities",
        },
        "page-kits": {
            "url": "https://www.michaels.com/shop/papercraft/paper/page-kits/",
            "subcategory": "paper/page-kits",
        },
        "paint-mediums": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/paint-mediums/",
            "subcategory": "ink-mixed-media/paint-mediums",
        },
        "paper-collage": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/paper-collage/",
            "subcategory": "ink-mixed-media/paper-collage",
        },
        "paper-craft-kits": {
            "url": "https://www.michaels.com/shop/papercraft/paper-craft-kits/",
            "subcategory": "paper-craft-kits",
        },
        "paper-folders-shapers": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/paper-folders-shapers/",
            "subcategory": "tools-adhesives/paper-folders-shapers",
        },
        "paper-house": {
            "url": "https://www.michaels.com/shop/papercraft/planners/collections/paper-house/",
            "subcategory": "planners/collections/paper-house",
        },
        "paper-punches": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/paper-punches/",
            "subcategory": "tools-adhesives/paper-punches",
        },
        "paper-quillling": {
            "url": "https://www.michaels.com/shop/papercraft/paper/paper-quillling/",
            "subcategory": "paper/paper-quillling",
        },
        "papercraft": {
            "url": "https://www.michaels.com/shop/papercraft/",
            "subcategory": "papercraft",
        },
        "papercraft-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/foil-application/accessories/",
            "subcategory": "stamps-embossing/foil-application/accessories",
        },
        "papercraft-adhesives": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/adhesives/",
            "subcategory": "tools-adhesives/adhesives",
        },
        "papercraft-alcohol-ink": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/inks-accessories/alcohol-ink/",
            "subcategory": "ink-mixed-media/inks-accessories/alcohol-ink",
        },
        "papercraft-birthday": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/greeting-cards/birthday/",
            "subcategory": "card-making/greeting-cards/birthday",
        },
        "papercraft-blank-cards": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/blank-cards/",
            "subcategory": "card-making/blank-cards",
        },
        "papercraft-brads": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/brads/",
            "subcategory": "embellishments/brads",
        },
        "papercraft-brushes": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/brushes/",
            "subcategory": "tools-adhesives/brushes",
        },
        "papercraft-buttons": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/buttons/",
            "subcategory": "embellishments/buttons",
        },
        "papercraft-calendars": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/calendars/",
            "subcategory": "planners/the-happy-planner/calendars",
        },
        "papercraft-calendars-2": {
            "url": "https://www.michaels.com/shop/papercraft/planners/calendars/",
            "subcategory": "planners/calendars",
        },
        "papercraft-card-making": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/",
            "subcategory": "card-making",
        },
        "papercraft-clothespins": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/clothespins/",
            "subcategory": "embellishments/clothespins",
        },
        "papercraft-craft-storage": {
            "url": "https://www.michaels.com/shop/papercraft/craft-storage/",
            "subcategory": "craft-storage",
        },
        "papercraft-crafting-paper": {
            "url": "https://www.michaels.com/shop/papercraft/paper/crafting-paper/",
            "subcategory": "paper/crafting-paper",
        },
        "papercraft-cutting-machines": {
            "url": "https://www.michaels.com/shop/papercraft/cutting-machines/",
            "subcategory": "cutting-machines",
        },
        "papercraft-embellishments": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/",
            "subcategory": "embellishments",
        },
        "papercraft-envelopes": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/envelopes/",
            "subcategory": "card-making/envelopes",
        },
        "papercraft-glitter": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/glitter/",
            "subcategory": "embellishments/glitter",
        },
        "papercraft-glue": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/adhesives/glue/",
            "subcategory": "tools-adhesives/adhesives/glue",
        },
        "papercraft-invitations": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/invitations/",
            "subcategory": "card-making/invitations",
        },
        "papercraft-labels": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/labels/",
            "subcategory": "embellishments/labels",
        },
        "papercraft-letters-numbers": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/letters-numbers/",
            "subcategory": "stickers/letters-numbers",
        },
        "papercraft-measuring-tools": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/measuring-tools/",
            "subcategory": "tools-adhesives/measuring-tools",
        },
        "papercraft-paper": {
            "url": "https://www.michaels.com/shop/papercraft/paper/",
            "subcategory": "paper",
        },
        "papercraft-paper-mache": {
            "url": "https://www.michaels.com/shop/papercraft/paper/paper-mache/",
            "subcategory": "paper/paper-mache",
        },
        "papercraft-paper-trimmers": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/paper-trimmers/",
            "subcategory": "tools-adhesives/paper-trimmers",
        },
        "papercraft-patterns": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/washi-tape/patterns/",
            "subcategory": "embellishments/washi-tape/patterns",
        },
        "papercraft-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/",
            "subcategory": "planners",
        },
        "papercraft-scissors": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/scissors/",
            "subcategory": "tools-adhesives/scissors",
        },
        "papercraft-shapes": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/shapes/",
            "subcategory": "stickers/shapes",
        },
        "papercraft-solids": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/washi-tape/solids/",
            "subcategory": "embellishments/washi-tape/solids",
        },
        "papercraft-specialty": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/washi-tape/specialty/",
            "subcategory": "embellishments/washi-tape/specialty",
        },
        "papercraft-stencils": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/stencils/",
            "subcategory": "stamps-embossing/stencils",
        },
        "papercraft-stickers": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/companion-accessories/stickers/",
            "subcategory": "planners/the-happy-planner/companion-accessories/stickers",
        },
        "papercraft-stickers-2": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/",
            "subcategory": "stickers",
        },
        "papercraft-surfaces": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/inks-accessories/surfaces/",
            "subcategory": "ink-mixed-media/inks-accessories/surfaces",
        },
        "papercraft-tools-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/tools-accessories/",
            "subcategory": "card-making/tools-accessories",
        },
        "photo-albums": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/photo-albums/",
            "subcategory": "albums-refills/photo-albums",
        },
        "photo-frame-cards": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/photo-frame-cards/",
            "subcategory": "card-making/photo-frame-cards",
        },
        "pigment-powder": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/pigment-powder/",
            "subcategory": "embellishments/pigment-powder",
        },
        "planner-books": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/planner-books/",
            "subcategory": "planners/the-happy-planner/planner-books",
        },
        "punch-boards-templates": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/punch-boards-templates/",
            "subcategory": "tools-adhesives/punch-boards-templates",
        },
        "punches": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/companion-accessories/punches/",
            "subcategory": "planners/the-happy-planner/companion-accessories/punches",
        },
        "recipe-meal-planning": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/recipe-meal-planning/",
            "subcategory": "planners/specialized-planners/recipe-meal-planning",
        },
        "refills-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/refills-accessories/",
            "subcategory": "albums-refills/refills-accessories",
        },
        "rub-ons-transfers": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/rub-ons-transfers/",
            "subcategory": "stickers/rub-ons-transfers",
        },
        "runners": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/adhesives/runners/",
            "subcategory": "tools-adhesives/adhesives/runners",
        },
        "school": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/school/",
            "subcategory": "stickers/school",
        },
        "scrapbook-albums": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/scrapbook-albums/",
            "subcategory": "albums-refills/scrapbook-albums",
        },
        "scrapbook-kits": {
            "url": "https://www.michaels.com/shop/papercraft/albums-refills/scrapbook-kits/",
            "subcategory": "albums-refills/scrapbook-kits",
        },
        "scrapbook-paper-packs": {
            "url": "https://www.michaels.com/shop/papercraft/paper/scrapbook-paper-packs/",
            "subcategory": "paper/scrapbook-paper-packs",
        },
        "scrapbook-paper-sheets": {
            "url": "https://www.michaels.com/shop/papercraft/paper/scrapbook-paper-sheets/",
            "subcategory": "paper/scrapbook-paper-sheets",
        },
        "self-inking-stamps": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/self-inking-stamps/",
            "subcategory": "stamps-embossing/self-inking-stamps",
        },
        "sentiments-words": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/cling-stamps/sentiments-words/",
            "subcategory": "stamps-embossing/cling-stamps/sentiments-words",
        },
        "shaker-cards": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/shaker-cards/",
            "subcategory": "card-making/shaker-cards",
        },
        "shrink-film": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/shrink-film/",
            "subcategory": "tools-adhesives/shrink-film",
        },
        "specialized-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/",
            "subcategory": "planners/specialized-planners",
        },
        "specialty-glitter": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/glitter/specialty-glitter/",
            "subcategory": "embellishments/glitter/specialty-glitter",
        },
        "sports": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/sports/",
            "subcategory": "stickers/sports",
        },
        "spray-ink-pigment": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/inks-accessories/spray-ink-pigment/",
            "subcategory": "ink-mixed-media/inks-accessories/spray-ink-pigment",
        },
        "stamping-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/stamping-accessories/",
            "subcategory": "stamps-embossing/stamping-accessories",
        },
        "stamps-embossing": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/",
            "subcategory": "stamps-embossing",
        },
        "stationery": {
            "url": "https://www.michaels.com/shop/papercraft/paper/stationery/",
            "subcategory": "paper/stationery",
        },
        "stickers-accessories": {
            "url": "https://www.michaels.com/shop/papercraft/planners/stickers-accessories/",
            "subcategory": "planners/stickers-accessories",
        },
        "sympathy": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/greeting-cards/sympathy/",
            "subcategory": "card-making/greeting-cards/sympathy",
        },
        "tag-making": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/tag-making/",
            "subcategory": "card-making/tag-making",
        },
        "tape": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/adhesives/tape/",
            "subcategory": "tools-adhesives/adhesives/tape",
        },
        "teacher-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/teacher-planners/",
            "subcategory": "planners/specialized-planners/teacher-planners",
        },
        "thank-you": {
            "url": "https://www.michaels.com/shop/papercraft/card-making/greeting-cards/thank-you/",
            "subcategory": "card-making/greeting-cards/thank-you",
        },
        "the-happy-planner": {
            "url": "https://www.michaels.com/shop/papercraft/planners/the-happy-planner/",
            "subcategory": "planners/the-happy-planner",
        },
        "tim-holtz-distress": {
            "url": "https://www.michaels.com/shop/papercraft/ink-mixed-media/mixed-media-collections/tim-holtz-distress/",
            "subcategory": "ink-mixed-media/mixed-media-collections/tim-holtz-distress",
        },
        "tools-adhesives": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/",
            "subcategory": "tools-adhesives",
        },
        "tools-storage": {
            "url": "https://www.michaels.com/shop/papercraft/die-cutting/tools-storage/",
            "subcategory": "die-cutting/tools-storage",
        },
        "travel": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/travel/",
            "subcategory": "stickers/travel",
        },
        "trim-tassels": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/trim-tassels/",
            "subcategory": "embellishments/trim-tassels",
        },
        "twines": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/twines/",
            "subcategory": "embellishments/twines",
        },
        "vellum-paper": {
            "url": "https://www.michaels.com/shop/papercraft/paper/vellum-paper/",
            "subcategory": "paper/vellum-paper",
        },
        "washi-tape": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/washi-tape/",
            "subcategory": "embellishments/washi-tape",
        },
        "wedding-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/specialized-planners/wedding-planners/",
            "subcategory": "planners/specialized-planners/wedding-planners",
        },
        "weekly-planners": {
            "url": "https://www.michaels.com/shop/papercraft/planners/weekly-planners/",
            "subcategory": "planners/weekly-planners",
        },
        "wood-chipboard": {
            "url": "https://www.michaels.com/shop/papercraft/embellishments/wood-chipboard/",
            "subcategory": "embellishments/wood-chipboard",
        },
        "wood-rubber-stamps": {
            "url": "https://www.michaels.com/shop/papercraft/stamps-embossing/wood-rubber-stamps/",
            "subcategory": "stamps-embossing/wood-rubber-stamps",
        },
        "words-phrases": {
            "url": "https://www.michaels.com/shop/papercraft/stickers/words-phrases/",
            "subcategory": "stickers/words-phrases",
        },
        "xyron-sticker-making": {
            "url": "https://www.michaels.com/shop/papercraft/tools-adhesives/xyron-sticker-making/",
            "subcategory": "tools-adhesives/xyron-sticker-making",
        },
    },
    "party": {
        "100th-day-of-school": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/100th-day-of-school/",
            "subcategory": "holidays-special-occasions/100th-day-of-school",
        },
        "anniversary-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/anniversary-party/",
            "subcategory": "holidays-special-occasions/anniversary-party",
        },
        "baby-shower-gender-reveal": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/baby-shower-gender-reveal/",
            "subcategory": "holidays-special-occasions/baby-shower-gender-reveal",
        },
        "bachelorette-party-bridal-shower": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/bachelorette-party-bridal-shower/",
            "subcategory": "holidays-special-occasions/bachelorette-party-bridal-shower",
        },
        "balloon-accessories": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/balloon-accessories/",
            "subcategory": "balloons-accessories/balloon-accessories",
        },
        "balloon-banners-kits": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/balloon-banners-kits/",
            "subcategory": "balloons-accessories/balloon-banners-kits",
        },
        "balloon-tanks-pumps": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/balloon-tanks-pumps/",
            "subcategory": "balloons-accessories/balloon-tanks-pumps",
        },
        "balloon-weights": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/balloon-weights/",
            "subcategory": "balloons-accessories/balloon-weights",
        },
        "balloons-accessories": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/",
            "subcategory": "balloons-accessories",
        },
        "banners": {
            "url": "https://www.michaels.com/shop/party/party-decorations/banners/",
            "subcategory": "party-decorations/banners",
        },
        "baptism-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/baptism-party/",
            "subcategory": "holidays-special-occasions/religious-party/baptism-party",
        },
        "birthday-party": {
            "url": "https://www.michaels.com/shop/party/birthday-party/",
            "subcategory": "birthday-party",
        },
        "bowls": {
            "url": "https://www.michaels.com/shop/party/party-tableware/bowls/",
            "subcategory": "party-tableware/bowls",
        },
        "candles-cake-decorations": {
            "url": "https://www.michaels.com/shop/party/party-decorations/candles-cake-decorations/",
            "subcategory": "party-decorations/candles-cake-decorations",
        },
        "candy": {
            "url": "https://www.michaels.com/shop/party/candy-snacks/candy/",
            "subcategory": "candy-snacks/candy",
        },
        "candy-buffet-supplies": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/candy-buffet-supplies/",
            "subcategory": "entertaining-catering-supplies/candy-buffet-supplies",
        },
        "candy-snacks": {
            "url": "https://www.michaels.com/shop/party/candy-snacks/",
            "subcategory": "candy-snacks",
        },
        "ceiling-decorations": {
            "url": "https://www.michaels.com/shop/party/party-decorations/ceiling-decorations/",
            "subcategory": "party-decorations/ceiling-decorations",
        },
        "cocktail-beverage-napkins": {
            "url": "https://www.michaels.com/shop/party/party-tableware/napkins/cocktail-beverage-napkins/",
            "subcategory": "party-tableware/napkins/cocktail-beverage-napkins",
        },
        "confetti": {
            "url": "https://www.michaels.com/shop/party/party-decorations/confetti/",
            "subcategory": "party-decorations/confetti",
        },
        "confirmation-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/confirmation-party/",
            "subcategory": "holidays-special-occasions/religious-party/confirmation-party",
        },
        "coolers-ice-pails": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/coolers-ice-pails/",
            "subcategory": "entertaining-catering-supplies/coolers-ice-pails",
        },
        "cups": {
            "url": "https://www.michaels.com/shop/party/party-tableware/cups/",
            "subcategory": "party-tableware/cups",
        },
        "curling-ribbon": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/curling-ribbon/",
            "subcategory": "balloons-accessories/curling-ribbon",
        },
        "curtains-backdrops": {
            "url": "https://www.michaels.com/shop/party/party-decorations/curtains-backdrops/",
            "subcategory": "party-decorations/curtains-backdrops",
        },
        "cutlery": {
            "url": "https://www.michaels.com/shop/party/party-tableware/cutlery/",
            "subcategory": "party-tableware/cutlery",
        },
        "diwali-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/diwali-party/",
            "subcategory": "holidays-special-occasions/religious-party/diwali-party",
        },
        "doilies-placemats": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/doilies-placemats/",
            "subcategory": "entertaining-catering-supplies/doilies-placemats",
        },
        "drink-markers-coasters": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/drink-markers-coasters/",
            "subcategory": "entertaining-catering-supplies/drink-markers-coasters",
        },
        "entertaining-catering-supplies": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/",
            "subcategory": "entertaining-catering-supplies",
        },
        "favor-bags": {
            "url": "https://www.michaels.com/shop/party/party-favors-favor-containers/favor-bags/",
            "subcategory": "party-favors-favor-containers/favor-bags",
        },
        "favor-boxes": {
            "url": "https://www.michaels.com/shop/party/party-favors-favor-containers/favor-boxes/",
            "subcategory": "party-favors-favor-containers/favor-boxes",
        },
        "favor-buckets-pails": {
            "url": "https://www.michaels.com/shop/party/party-favors-favor-containers/favor-buckets-pails/",
            "subcategory": "party-favors-favor-containers/favor-buckets-pails",
        },
        "first-communion-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/first-communion-party/",
            "subcategory": "holidays-special-occasions/religious-party/first-communion-party",
        },
        "folding-tables-chairs": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/folding-tables-chairs/",
            "subcategory": "entertaining-catering-supplies/folding-tables-chairs",
        },
        "food-drink-labels": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/food-drink-labels/",
            "subcategory": "entertaining-catering-supplies/food-drink-labels",
        },
        "food-snack-containers": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/food-snack-containers/",
            "subcategory": "entertaining-catering-supplies/food-snack-containers",
        },
        "game-day-football-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/game-day-football-party/",
            "subcategory": "holidays-special-occasions/game-day-football-party",
        },
        "general-birthday-theme-parties": {
            "url": "https://www.michaels.com/shop/party/birthday-party/general-birthday-theme-parties/",
            "subcategory": "birthday-party/general-birthday-theme-parties",
        },
        "general-christian-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/general-christian-party/",
            "subcategory": "holidays-special-occasions/religious-party/general-christian-party",
        },
        "gift-bags-wine-bags": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/gift-bags-wine-bags/",
            "subcategory": "gift-packaging/gift-bags-wine-bags",
        },
        "gift-basket-packaging": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/gift-basket-packaging/",
            "subcategory": "gift-packaging/gift-basket-packaging",
        },
        "gift-packaging": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/",
            "subcategory": "gift-packaging",
        },
        "gift-packaging-accessories": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/gift-packaging-accessories/",
            "subcategory": "gift-packaging/gift-packaging-accessories",
        },
        "gift-tags": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/gift-tags/",
            "subcategory": "gift-packaging/gift-tags",
        },
        "glass-favor-containers": {
            "url": "https://www.michaels.com/shop/party/party-favors-favor-containers/glass-favor-containers/",
            "subcategory": "party-favors-favor-containers/glass-favor-containers",
        },
        "glasses-drinkware": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/glasses-drinkware/",
            "subcategory": "entertaining-catering-supplies/glasses-drinkware",
        },
        "graduation-balloon-bundles": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/graduation-balloon-bundles/",
            "subcategory": "balloons-accessories/graduation-balloon-bundles",
        },
        "guest-towels": {
            "url": "https://www.michaels.com/shop/party/party-tableware/napkins/guest-towels/",
            "subcategory": "party-tableware/napkins/guest-towels",
        },
        "holidays-special-occasions": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/",
            "subcategory": "holidays-special-occasions",
        },
        "kids-birthday-party": {
            "url": "https://www.michaels.com/shop/party/birthday-party/kids-birthday-party/",
            "subcategory": "birthday-party/kids-birthday-party",
        },
        "latex-balloons": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/latex-balloons/",
            "subcategory": "balloons-accessories/latex-balloons",
        },
        "luncheon-napkins": {
            "url": "https://www.michaels.com/shop/party/party-tableware/napkins/luncheon-napkins/",
            "subcategory": "party-tableware/napkins/luncheon-napkins",
        },
        "mylar-foil-balloons": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/mylar-foil-balloons/",
            "subcategory": "balloons-accessories/mylar-foil-balloons",
        },
        "napkins": {
            "url": "https://www.michaels.com/shop/party/party-tableware/napkins/",
            "subcategory": "party-tableware/napkins",
        },
        "paper-sacks-lunch-bags": {
            "url": "https://www.michaels.com/shop/party/party-favors-favor-containers/paper-sacks-lunch-bags/",
            "subcategory": "party-favors-favor-containers/paper-sacks-lunch-bags",
        },
        "party-chargers": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/chargers/",
            "subcategory": "entertaining-catering-supplies/chargers",
        },
        "party-decorations": {
            "url": "https://www.michaels.com/shop/party/party-decorations/",
            "subcategory": "party-decorations",
        },
        "party-favors-favor-containers": {
            "url": "https://www.michaels.com/shop/party/party-favors-favor-containers/",
            "subcategory": "party-favors-favor-containers",
        },
        "party-gift-boxes": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/gift-boxes/",
            "subcategory": "gift-packaging/gift-boxes",
        },
        "party-gift-ribbon-bows": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/gift-ribbon-bows/",
            "subcategory": "gift-packaging/gift-ribbon-bows",
        },
        "party-party": {
            "url": "https://www.michaels.com/shop/party/",
            "subcategory": "party",
        },
        "party-party-favors": {
            "url": "https://www.michaels.com/shop/party/party-favors-favor-containers/party-favors/",
            "subcategory": "party-favors-favor-containers/party-favors",
        },
        "party-party-games": {
            "url": "https://www.michaels.com/shop/party/party-games/",
            "subcategory": "party-games",
        },
        "party-plates": {
            "url": "https://www.michaels.com/shop/party/party-tableware/plates/",
            "subcategory": "party-tableware/plates",
        },
        "party-ramadan": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/ramadan/",
            "subcategory": "holidays-special-occasions/religious-party/ramadan",
        },
        "party-serveware": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/party-serveware/",
            "subcategory": "entertaining-catering-supplies/party-serveware",
        },
        "party-speakers-karaoke": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/party-speakers-karaoke/",
            "subcategory": "entertaining-catering-supplies/party-speakers-karaoke",
        },
        "party-straws": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/straws/",
            "subcategory": "entertaining-catering-supplies/straws",
        },
        "party-straws-2": {
            "url": "https://www.michaels.com/shop/party/party-tableware/straws/",
            "subcategory": "party-tableware/straws",
        },
        "party-tableware": {
            "url": "https://www.michaels.com/shop/party/party-tableware/",
            "subcategory": "party-tableware",
        },
        "party-tableware-sets": {
            "url": "https://www.michaels.com/shop/party/party-tableware/party-tableware-sets/",
            "subcategory": "party-tableware/party-tableware-sets",
        },
        "party-wearables": {
            "url": "https://www.michaels.com/shop/party/party-decorations/party-wearables/",
            "subcategory": "party-decorations/party-wearables",
        },
        "passover": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/passover/",
            "subcategory": "holidays-special-occasions/religious-party/passover",
        },
        "photo-booth-props": {
            "url": "https://www.michaels.com/shop/party/party-decorations/photo-booth-props/",
            "subcategory": "party-decorations/photo-booth-props",
        },
        "picks-skewers": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/picks-skewers/",
            "subcategory": "entertaining-catering-supplies/picks-skewers",
        },
        "pinatas": {
            "url": "https://www.michaels.com/shop/party/party-decorations/pinatas/",
            "subcategory": "party-decorations/pinatas",
        },
        "place-cards-holders": {
            "url": "https://www.michaels.com/shop/party/entertaining-catering-supplies/place-cards-holders/",
            "subcategory": "entertaining-catering-supplies/place-cards-holders",
        },
        "quinceanera": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/quinceanera/",
            "subcategory": "holidays-special-occasions/quinceanera",
        },
        "religious-party": {
            "url": "https://www.michaels.com/shop/party/holidays-special-occasions/religious-party/",
            "subcategory": "holidays-special-occasions/religious-party",
        },
        "serving-trays": {
            "url": "https://www.michaels.com/shop/party/party-tableware/serving-trays/",
            "subcategory": "party-tableware/serving-trays",
        },
        "snacks-beverages": {
            "url": "https://www.michaels.com/shop/party/candy-snacks/snacks-beverages/",
            "subcategory": "candy-snacks/snacks-beverages",
        },
        "streamers-garland": {
            "url": "https://www.michaels.com/shop/party/party-decorations/streamers-garland/",
            "subcategory": "party-decorations/streamers-garland",
        },
        "table-covers-skirts": {
            "url": "https://www.michaels.com/shop/party/party-tableware/table-covers-skirts/",
            "subcategory": "party-tableware/table-covers-skirts",
        },
        "table-decorations-centerpieces": {
            "url": "https://www.michaels.com/shop/party/party-decorations/table-decorations-centerpieces/",
            "subcategory": "party-decorations/table-decorations-centerpieces",
        },
        "tissue-paper-shredded-filler": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/tissue-paper-shredded-filler/",
            "subcategory": "gift-packaging/tissue-paper-shredded-filler",
        },
        "totali-ez-balloons-kit": {
            "url": "https://www.michaels.com/shop/party/balloons-accessories/totali-ez-balloons-kit/",
            "subcategory": "balloons-accessories/totali-ez-balloons-kit",
        },
        "wall-window-floor-decorations": {
            "url": "https://www.michaels.com/shop/party/party-decorations/wall-window-floor-decorations/",
            "subcategory": "party-decorations/wall-window-floor-decorations",
        },
        "wrapping-paper": {
            "url": "https://www.michaels.com/shop/party/gift-packaging/wrapping-paper/",
            "subcategory": "gift-packaging/wrapping-paper",
        },
        "yard-signs": {
            "url": "https://www.michaels.com/shop/party/party-decorations/yard-signs/",
            "subcategory": "party-decorations/yard-signs",
        },
    },
    "ribbon": {
        "basic-pattern-ribbon": {
            "url": "https://www.michaels.com/shop/ribbon/basic-pattern-ribbon/",
            "subcategory": "basic-pattern-ribbon",
        },
        "basic-ribbon": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/ribbon/basic-ribbon/",
            "subcategory": "texas-homecoming/ribbon/basic-ribbon",
        },
        "basic-solid-ribbon": {
            "url": "https://www.michaels.com/shop/ribbon/basic-solid-ribbon/",
            "subcategory": "basic-solid-ribbon",
        },
        "decorative-ribbon": {
            "url": "https://www.michaels.com/shop/ribbon/decorative-ribbon/",
            "subcategory": "decorative-ribbon",
        },
        "garland": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/garland/",
            "subcategory": "texas-homecoming/garland",
        },
        "homecoming-backers": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/homecoming-backers/",
            "subcategory": "texas-homecoming/homecoming-backers",
        },
        "homecoming-boas": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/homecoming-boas/",
            "subcategory": "texas-homecoming/homecoming-boas",
        },
        "homecoming-flower": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/homecoming-flower/",
            "subcategory": "texas-homecoming/homecoming-flower",
        },
        "homecoming-lights": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/homecoming-lights/",
            "subcategory": "texas-homecoming/homecoming-lights",
        },
        "light-up-homecoming-boa": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/homecoming-boas/light-up-homecoming-boa/",
            "subcategory": "texas-homecoming/homecoming-boas/light-up-homecoming-boa",
        },
        "mum-shape": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/mum-shape/",
            "subcategory": "texas-homecoming/mum-shape",
        },
        "pre-made-mums": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/pre-made-mums/",
            "subcategory": "texas-homecoming/pre-made-mums",
        },
        "premade-bows": {
            "url": "https://www.michaels.com/shop/ribbon/premade-bows/",
            "subcategory": "premade-bows",
        },
        "rhinestone-trim": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/ribbon/rhinestone-trim/",
            "subcategory": "texas-homecoming/ribbon/rhinestone-trim",
        },
        "ribbon-bows": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/ribbon/bows/",
            "subcategory": "texas-homecoming/ribbon/bows",
        },
        "ribbon-mesh": {
            "url": "https://www.michaels.com/shop/ribbon/mesh/",
            "subcategory": "mesh",
        },
        "ribbon-ribbon": {
            "url": "https://www.michaels.com/shop/ribbon/",
            "subcategory": "ribbon",
        },
        "ribbon-ribbon-2": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/ribbon/",
            "subcategory": "texas-homecoming/ribbon",
        },
        "ribbon-specialty-ribbon": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/ribbon/specialty-ribbon/",
            "subcategory": "texas-homecoming/ribbon/specialty-ribbon",
        },
        "ribbon-stickers": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/stickers/",
            "subcategory": "texas-homecoming/stickers",
        },
        "ribbon-supplies": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/supplies/",
            "subcategory": "texas-homecoming/supplies",
        },
        "ribbon-tools-accessories": {
            "url": "https://www.michaels.com/shop/ribbon/ribbon-tools-accessories/",
            "subcategory": "ribbon-tools-accessories",
        },
        "ribbon-trim": {
            "url": "https://www.michaels.com/shop/ribbon/trim/",
            "subcategory": "trim",
        },
        "ribbon-tulle-2": {
            "url": "https://www.michaels.com/shop/ribbon/tulle/",
            "subcategory": "tulle",
        },
        "stuffed-mascot": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/stuffed-mascot/",
            "subcategory": "texas-homecoming/stuffed-mascot",
        },
        "texas-homecoming": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/",
            "subcategory": "texas-homecoming",
        },
        "trinkets": {
            "url": "https://www.michaels.com/shop/ribbon/texas-homecoming/trinkets/",
            "subcategory": "texas-homecoming/trinkets",
        },
        "value-pack-ribbon": {
            "url": "https://www.michaels.com/shop/ribbon/value-pack-ribbon/",
            "subcategory": "value-pack-ribbon",
        },
    },
    "storage": {
        "bedroom-closet-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bedroom-closet-storage/",
            "subcategory": "home-storage-organization/bedroom-closet-storage",
        },
        "binders-storage-bags": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/binders-storage-bags/",
            "subcategory": "craft-storage/binders-storage-bags",
        },
        "cabinet-drawer-organizers": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/cabinet-drawer-organizers/",
            "subcategory": "home-storage-organization/kitchen-storage/cabinet-drawer-organizers",
        },
        "cabinets-shelving": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bathroom-storage/cabinets-shelving/",
            "subcategory": "home-storage-organization/bathroom-storage/cabinets-shelving",
        },
        "caddies": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bathroom-storage/caddies/",
            "subcategory": "home-storage-organization/bathroom-storage/caddies",
        },
        "canisters": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/canisters/",
            "subcategory": "home-storage-organization/kitchen-storage/canisters",
        },
        "cart-accessories": {
            "url": "https://www.michaels.com/shop/storage/storage-carts/cart-accessories/",
            "subcategory": "storage-carts/cart-accessories",
        },
        "closet-drawer-organizers": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bedroom-closet-storage/closet-drawer-organizers/",
            "subcategory": "home-storage-organization/bedroom-closet-storage/closet-drawer-organizers",
        },
        "clothes-racks-portable-closets": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bedroom-closet-storage/clothes-racks-portable-closets/",
            "subcategory": "home-storage-organization/bedroom-closet-storage/clothes-racks-portable-closets",
        },
        "countertop-organizers": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/countertop-organizers/",
            "subcategory": "home-storage-organization/kitchen-storage/countertop-organizers",
        },
        "craft-machine-vinyl-storage": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/craft-machine-vinyl-storage/",
            "subcategory": "craft-storage/craft-machine-vinyl-storage",
        },
        "craft-room-furniture": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/craft-room-furniture/",
            "subcategory": "craft-storage/craft-room-furniture",
        },
        "cubes-tower-tabletop": {
            "url": "https://www.michaels.com/shop/storage/modular-storage/cubes-tower-tabletop/",
            "subcategory": "modular-storage/cubes-tower-tabletop",
        },
        "dish-racks": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/dish-racks/",
            "subcategory": "home-storage-organization/kitchen-storage/dish-racks",
        },
        "drawer-organizers": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bathroom-storage/drawer-organizers/",
            "subcategory": "home-storage-organization/bathroom-storage/drawer-organizers",
        },
        "drawer-shelves": {
            "url": "https://www.michaels.com/shop/storage/modular-storage/drawer-shelves/",
            "subcategory": "modular-storage/drawer-shelves",
        },
        "drying-racks": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/laundry-room-storage/drying-racks/",
            "subcategory": "home-storage-organization/laundry-room-storage/drying-racks",
        },
        "food-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/food-storage/",
            "subcategory": "home-storage-organization/kitchen-storage/food-storage",
        },
        "garage-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/garage-storage/",
            "subcategory": "home-storage-organization/garage-storage",
        },
        "hampers": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/laundry-room-storage/hampers/",
            "subcategory": "home-storage-organization/laundry-room-storage/hampers",
        },
        "hangers": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bedroom-closet-storage/hangers/",
            "subcategory": "home-storage-organization/bedroom-closet-storage/hangers",
        },
        "holiday-christmas-storage": {
            "url": "https://www.michaels.com/shop/storage/holiday-christmas-storage/",
            "subcategory": "holiday-christmas-storage",
        },
        "home-storage-organization": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/",
            "subcategory": "home-storage-organization",
        },
        "ironing-boards": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/laundry-room-storage/ironing-boards/",
            "subcategory": "home-storage-organization/laundry-room-storage/ironing-boards",
        },
        "laundry-accessories": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/laundry-room-storage/laundry-accessories/",
            "subcategory": "home-storage-organization/laundry-room-storage/laundry-accessories",
        },
        "laundry-room-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/laundry-room-storage/",
            "subcategory": "home-storage-organization/laundry-room-storage",
        },
        "modular-storage": {
            "url": "https://www.michaels.com/shop/storage/modular-storage/",
            "subcategory": "modular-storage",
        },
        "modular-storage-accessories": {
            "url": "https://www.michaels.com/shop/storage/modular-storage/modular-storage-accessories/",
            "subcategory": "modular-storage/modular-storage-accessories",
        },
        "office-organization-storage": {
            "url": "https://www.michaels.com/shop/storage/office-organization-storage/",
            "subcategory": "office-organization-storage",
        },
        "paper-towel-holders": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/paper-towel-holders/",
            "subcategory": "home-storage-organization/kitchen-storage/paper-towel-holders",
        },
        "photo-storage": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/photo-storage/",
            "subcategory": "craft-storage/photo-storage",
        },
        "plastic-buckets-bins": {
            "url": "https://www.michaels.com/shop/storage/plastic-storage-bins-totes/plastic-buckets-bins/",
            "subcategory": "plastic-storage-bins-totes/plastic-buckets-bins",
        },
        "plastic-organizers": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/plastic-organizers/",
            "subcategory": "craft-storage/plastic-organizers",
        },
        "plastic-storage-bins-totes": {
            "url": "https://www.michaels.com/shop/storage/plastic-storage-bins-totes/",
            "subcategory": "plastic-storage-bins-totes",
        },
        "plastic-totes": {
            "url": "https://www.michaels.com/shop/storage/plastic-storage-bins-totes/plastic-totes/",
            "subcategory": "plastic-storage-bins-totes/plastic-totes",
        },
        "rolling-bags": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/rolling-bags/",
            "subcategory": "craft-storage/rolling-bags",
        },
        "rolling-storage-carts": {
            "url": "https://www.michaels.com/shop/storage/storage-carts/rolling-storage-carts/",
            "subcategory": "storage-carts/rolling-storage-carts",
        },
        "scrapbooking-storage": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/scrapbooking-storage/",
            "subcategory": "craft-storage/scrapbooking-storage",
        },
        "shoe-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/shoe-storage/",
            "subcategory": "home-storage-organization/shoe-storage",
        },
        "small-plastic-organizers": {
            "url": "https://www.michaels.com/shop/storage/plastic-storage-bins-totes/small-plastic-organizers/",
            "subcategory": "plastic-storage-bins-totes/small-plastic-organizers",
        },
        "soft-storage": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/soft-storage/",
            "subcategory": "craft-storage/soft-storage",
        },
        "step-stools": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/step-stools/",
            "subcategory": "home-storage-organization/step-stools",
        },
        "storage-art-storage": {
            "url": "https://www.michaels.com/shop/storage/art-storage/",
            "subcategory": "art-storage",
        },
        "storage-bags": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bedroom-closet-storage/storage-bags/",
            "subcategory": "home-storage-organization/bedroom-closet-storage/storage-bags",
        },
        "storage-baskets": {
            "url": "https://www.michaels.com/shop/storage/storage-baskets-boxes/baskets/",
            "subcategory": "storage-baskets-boxes/baskets",
        },
        "storage-baskets-boxes": {
            "url": "https://www.michaels.com/shop/storage/storage-baskets-boxes/",
            "subcategory": "storage-baskets-boxes",
        },
        "storage-bathroom-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bathroom-storage/",
            "subcategory": "home-storage-organization/bathroom-storage",
        },
        "storage-bead-jewelry-storage": {
            "url": "https://www.michaels.com/shop/storage/bead-jewelry-storage/",
            "subcategory": "bead-jewelry-storage",
        },
        "storage-bottles-jars": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/storage-bottles-jars/",
            "subcategory": "craft-storage/storage-bottles-jars",
        },
        "storage-carts": {
            "url": "https://www.michaels.com/shop/storage/storage-carts/",
            "subcategory": "storage-carts",
        },
        "storage-carts-drawer-units": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/carts-drawer-units/",
            "subcategory": "craft-storage/carts-drawer-units",
        },
        "storage-craft-storage": {
            "url": "https://www.michaels.com/shop/storage/craft-storage/",
            "subcategory": "craft-storage",
        },
        "storage-cubes": {
            "url": "https://www.michaels.com/shop/storage/storage-baskets-boxes/storage-cubes/",
            "subcategory": "storage-baskets-boxes/storage-cubes",
        },
        "storage-decorative-boxes": {
            "url": "https://www.michaels.com/shop/storage/storage-baskets-boxes/decorative-boxes/",
            "subcategory": "storage-baskets-boxes/decorative-boxes",
        },
        "storage-drawer-units": {
            "url": "https://www.michaels.com/shop/storage/plastic-storage-bins-totes/storage-drawer-units/",
            "subcategory": "plastic-storage-bins-totes/storage-drawer-units",
        },
        "storage-kids-art-storage": {
            "url": "https://www.michaels.com/shop/storage/kids-art-storage/",
            "subcategory": "kids-art-storage",
        },
        "storage-kitchen-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/",
            "subcategory": "home-storage-organization/kitchen-storage",
        },
        "storage-locked-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/locked-storage/",
            "subcategory": "home-storage-organization/locked-storage",
        },
        "storage-sewing-baskets-organization": {
            "url": "https://www.michaels.com/shop/storage/sewing-baskets-organization/",
            "subcategory": "sewing-baskets-organization",
        },
        "storage-storage": {
            "url": "https://www.michaels.com/shop/storage/",
            "subcategory": "storage",
        },
        "storage-trash-cans": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/bathroom-storage/trash-cans/",
            "subcategory": "home-storage-organization/bathroom-storage/trash-cans",
        },
        "storage-trash-cans-2": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/kitchen-storage/trash-cans/",
            "subcategory": "home-storage-organization/kitchen-storage/trash-cans",
        },
        "trash-bins": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/trash-bins/",
            "subcategory": "home-storage-organization/trash-bins",
        },
        "unfinished-boxes-crates": {
            "url": "https://www.michaels.com/shop/storage/storage-baskets-boxes/unfinished-boxes-crates/",
            "subcategory": "storage-baskets-boxes/unfinished-boxes-crates",
        },
        "vacuum-storage-bags": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/vacuum-storage-bags/",
            "subcategory": "home-storage-organization/vacuum-storage-bags",
        },
        "wall-mounted-storage": {
            "url": "https://www.michaels.com/shop/storage/home-storage-organization/wall-mounted-storage/",
            "subcategory": "home-storage-organization/wall-mounted-storage",
        },
        "yarn-storage": {
            "url": "https://www.michaels.com/shop/storage/yarn-storage/",
            "subcategory": "yarn-storage",
        },
    },
    "teacher-supplies": {
        "addition-subtraction": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/addition-subtraction/",
            "subcategory": "shop-by-class-subject/math/addition-subtraction",
        },
        "algebra": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/algebra/",
            "subcategory": "shop-by-class-subject/math/algebra",
        },
        "alphabet-number-lines": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/alphabet-number-lines/",
            "subcategory": "classroom-decorations/alphabet-number-lines",
        },
        "anatomy": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/anatomy/",
            "subcategory": "shop-by-class-subject/science/anatomy",
        },
        "animal-studies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/animal-studies/",
            "subcategory": "shop-by-class-subject/science/animal-studies",
        },
        "answer-buzzers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/game-parts/answer-buzzers/",
            "subcategory": "resources-management/game-parts/answer-buzzers",
        },
        "arts-crafts-supplies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/",
            "subcategory": "arts-crafts-supplies",
        },
        "awards": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/awards/",
            "subcategory": "awards-incentives/awards",
        },
        "awards-incentives": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/",
            "subcategory": "awards-incentives",
        },
        "back-to-school-accessories": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/back-to-school-accessories/",
            "subcategory": "awards-incentives/back-to-school-accessories",
        },
        "backpacks": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/backpacks/",
            "subcategory": "resources-management/backpacks",
        },
        "badges": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/badges/",
            "subcategory": "awards-incentives/badges",
        },
        "balls": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/balls/",
            "subcategory": "shop-by-class-subject/physical-education/balls",
        },
        "base-ten": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/base-ten/",
            "subcategory": "shop-by-class-subject/math/base-ten",
        },
        "basic-skills": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/basic-skills/",
            "subcategory": "shop-by-class-subject/basic-skills",
        },
        "bean-bags": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/game-parts/bean-bags/",
            "subcategory": "resources-management/game-parts/bean-bags",
        },
        "big-tree": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-sets/big-tree/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-sets/big-tree",
        },
        "bins-crates": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/bins-crates/",
            "subcategory": "classroom-organization/bins-crates",
        },
        "bookmarks": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/bookmarks/",
            "subcategory": "awards-incentives/bookmarks",
        },
        "bookshelves": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/bookshelves/",
            "subcategory": "classroom-organization/bookshelves",
        },
        "bouncy-balls": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/bouncy-balls/",
            "subcategory": "awards-incentives/bouncy-balls",
        },
        "bulletin-board-accents": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-accents/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-accents",
        },
        "bulletin-board-kraft-rolls": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/bulletin-board-kraft-rolls/",
            "subcategory": "arts-crafts-supplies/paper/bulletin-board-kraft-rolls",
        },
        "bulletin-board-letters": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-letters/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-letters",
        },
        "bulletin-board-paper": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-paper/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-paper",
        },
        "bulletin-board-sets": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-sets/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-sets",
        },
        "bulletin-board-supplies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/",
            "subcategory": "classroom-decorations/bulletin-board-supplies",
        },
        "bulletin-borders-trim": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-borders-trim/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-borders-trim",
        },
        "cds": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/music/cds/",
            "subcategory": "shop-by-class-subject/music/cds",
        },
        "certificates": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/certificates/",
            "subcategory": "awards-incentives/certificates",
        },
        "chair-storage": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/chair-storage/",
            "subcategory": "classroom-organization/chair-storage",
        },
        "chalkboard-accessories": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/chalkboard-accessories/",
            "subcategory": "resources-management/chalkboard-accessories",
        },
        "chart-tablets": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/chart-tablets/",
            "subcategory": "arts-crafts-supplies/paper/chart-tablets",
        },
        "charts": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/charts/",
            "subcategory": "classroom-decorations/charts",
        },
        "childrens-books": {
            "url": "https://www.michaels.com/shop/teacher-supplies/childrens-books/",
            "subcategory": "childrens-books",
        },
        "classroom-clean-up": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/classroom-clean-up/",
            "subcategory": "resources-management/classroom-clean-up",
        },
        "classroom-decorations": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/",
            "subcategory": "classroom-decorations",
        },
        "classroom-furniture": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/classroom-furniture/",
            "subcategory": "classroom-organization/classroom-furniture",
        },
        "classroom-management": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/classroom-management/",
            "subcategory": "resources-management/classroom-management",
        },
        "classroom-organization": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/",
            "subcategory": "classroom-organization",
        },
        "classroom-posters": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/classroom-posters/",
            "subcategory": "classroom-decorations/classroom-posters",
        },
        "clay-casting": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/clay-casting/",
            "subcategory": "arts-crafts-supplies/clay-casting",
        },
        "colors": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/basic-skills/colors/",
            "subcategory": "shop-by-class-subject/basic-skills/colors",
        },
        "community-culture": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/social-studies/community-culture/",
            "subcategory": "shop-by-class-subject/social-studies/community-culture",
        },
        "composition-notebooks": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/composition-notebooks/",
            "subcategory": "shop-by-class-subject/reading-language-arts/composition-notebooks",
        },
        "comprehension": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/comprehension/",
            "subcategory": "shop-by-class-subject/reading-language-arts/comprehension",
        },
        "cones": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/cones/",
            "subcategory": "shop-by-class-subject/physical-education/cones",
        },
        "counting": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/counting/",
            "subcategory": "shop-by-class-subject/math/counting",
        },
        "craft-sticks-wood-shapes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/craft-sticks-wood-shapes/",
            "subcategory": "arts-crafts-supplies/craft-supplies/craft-sticks-wood-shapes",
        },
        "craft-tape": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/craft-tape/",
            "subcategory": "arts-crafts-supplies/craft-supplies/craft-tape",
        },
        "critical-thinking": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/critical-thinking/",
            "subcategory": "shop-by-class-subject/reading-language-arts/critical-thinking",
        },
        "cross-curriculum-resources": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/cross-curriculum-resources/",
            "subcategory": "resources-management/cross-curriculum-resources",
        },
        "crowns": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/crowns/",
            "subcategory": "awards-incentives/crowns",
        },
        "dice-dominos": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/game-parts/dice-dominos/",
            "subcategory": "resources-management/game-parts/dice-dominos",
        },
        "dividers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/dividers/",
            "subcategory": "classroom-organization/dividers",
        },
        "door-decorations": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/door-decorations/",
            "subcategory": "classroom-decorations/door-decorations",
        },
        "early-education": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/shop-by-subject/early-education/",
            "subcategory": "classroom-decorations/shop-by-subject/early-education",
        },
        "early-learning": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/early-learning/",
            "subcategory": "resources-management/early-learning",
        },
        "early-learning-readers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/early-learning-readers/",
            "subcategory": "shop-by-class-subject/reading-language-arts/early-learning-readers",
        },
        "earth-science": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/earth-science/",
            "subcategory": "shop-by-class-subject/science/earth-science",
        },
        "emotions": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/basic-skills/emotions/",
            "subcategory": "shop-by-class-subject/basic-skills/emotions",
        },
        "environment": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/environment/",
            "subcategory": "shop-by-class-subject/science/environment",
        },
        "filing": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/filing/",
            "subcategory": "classroom-organization/filing",
        },
        "first-aid-safety": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/first-aid-safety/",
            "subcategory": "resources-management/first-aid-safety",
        },
        "flannel-boards": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/flannel-boards/",
            "subcategory": "resources-management/flannel-boards",
        },
        "floor-tape": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/floor-tape/",
            "subcategory": "shop-by-class-subject/physical-education/floor-tape",
        },
        "fractions-decimals": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/fractions-decimals/",
            "subcategory": "shop-by-class-subject/math/fractions-decimals",
        },
        "game-components": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/game-parts/game-components/",
            "subcategory": "resources-management/game-parts/game-components",
        },
        "game-parts": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/game-parts/",
            "subcategory": "resources-management/game-parts",
        },
        "geography": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/social-studies/geography/",
            "subcategory": "shop-by-class-subject/social-studies/geography",
        },
        "geometry": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/geometry/",
            "subcategory": "shop-by-class-subject/math/geometry",
        },
        "graders": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/graders/",
            "subcategory": "resources-management/graders",
        },
        "grammar-phonics": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/grammar-phonics/",
            "subcategory": "shop-by-class-subject/reading-language-arts/grammar-phonics",
        },
        "graphic-bulletin-borders": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-borders-trim/graphic-bulletin-borders/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-borders-trim/graphic-bulletin-borders",
        },
        "graphing": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/graphing/",
            "subcategory": "shop-by-class-subject/math/graphing",
        },
        "hall-passes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/hall-passes/",
            "subcategory": "resources-management/hall-passes",
        },
        "handwriting": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/handwriting/",
            "subcategory": "shop-by-class-subject/reading-language-arts/handwriting",
        },
        "handwriting-drawing-pads": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/handwriting-drawing-pads/",
            "subcategory": "arts-crafts-supplies/paper/handwriting-drawing-pads",
        },
        "handwriting-paper": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/paper/handwriting-paper/",
            "subcategory": "resources-management/paper/handwriting-paper",
        },
        "health-nutrition": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/health-nutrition/",
            "subcategory": "shop-by-class-subject/science/health-nutrition",
        },
        "history": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/social-studies/history/",
            "subcategory": "shop-by-class-subject/social-studies/history",
        },
        "incentive-charts": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/incentive-charts/",
            "subcategory": "awards-incentives/incentive-charts",
        },
        "indoor-awnings": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/indoor-awnings/",
            "subcategory": "classroom-decorations/indoor-awnings",
        },
        "indoor-outdoor-games": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/indoor-outdoor-games/",
            "subcategory": "shop-by-class-subject/physical-education/indoor-outdoor-games",
        },
        "instruments": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/music/instruments/",
            "subcategory": "shop-by-class-subject/music/instruments",
        },
        "jump-ropes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/jump-ropes/",
            "subcategory": "shop-by-class-subject/physical-education/jump-ropes",
        },
        "lab-equipment": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/lab-equipment/",
            "subcategory": "shop-by-class-subject/science/lab-equipment",
        },
        "letter-recognition": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/letter-recognition/",
            "subcategory": "shop-by-class-subject/reading-language-arts/letter-recognition",
        },
        "library-cards": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/library-cards/",
            "subcategory": "resources-management/library-cards",
        },
        "light-filters": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/light-filters/",
            "subcategory": "resources-management/light-filters",
        },
        "magnetic-bulletin-accents": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/magnetic-bulletin-accents/",
            "subcategory": "classroom-decorations/magnetic-bulletin-accents",
        },
        "magnetic-letters-numbers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/magnetic-letters-numbers/",
            "subcategory": "shop-by-class-subject/reading-language-arts/magnetic-letters-numbers",
        },
        "magnetism": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/magnetism/",
            "subcategory": "shop-by-class-subject/science/magnetism",
        },
        "mailboxes-paper-storage": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/mailboxes-paper-storage/",
            "subcategory": "classroom-organization/mailboxes-paper-storage",
        },
        "manipulatives": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/manipulatives/",
            "subcategory": "resources-management/manipulatives",
        },
        "maps-globes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/social-studies/maps-globes/",
            "subcategory": "shop-by-class-subject/social-studies/maps-globes",
        },
        "measurement": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/measurement/",
            "subcategory": "shop-by-class-subject/math/measurement",
        },
        "money": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/money/",
            "subcategory": "shop-by-class-subject/math/money",
        },
        "motor-skills": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/basic-skills/motor-skills/",
            "subcategory": "shop-by-class-subject/basic-skills/motor-skills",
        },
        "multiplication-division": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/multiplication-division/",
            "subcategory": "shop-by-class-subject/math/multiplication-division",
        },
        "name-plates-tags": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/name-plates-tags/",
            "subcategory": "resources-management/name-plates-tags",
        },
        "numeration": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/numeration/",
            "subcategory": "shop-by-class-subject/math/numeration",
        },
        "optics-light": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/optics-light/",
            "subcategory": "shop-by-class-subject/science/optics-light",
        },
        "organization": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/organization/",
            "subcategory": "resources-management/organization",
        },
        "paints-brushes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paints-brushes/",
            "subcategory": "arts-crafts-supplies/paints-brushes",
        },
        "parachutes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/parachutes/",
            "subcategory": "shop-by-class-subject/physical-education/parachutes",
        },
        "patterned-bulletin-borders": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-borders-trim/patterned-bulletin-borders/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-borders-trim/patterned-bulletin-borders",
        },
        "photo-props": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/photo-props/",
            "subcategory": "classroom-decorations/photo-props",
        },
        "physical-education": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/",
            "subcategory": "shop-by-class-subject/physical-education",
        },
        "place-value": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/place-value/",
            "subcategory": "shop-by-class-subject/math/place-value",
        },
        "plan-record-resources": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/plan-record-resources/",
            "subcategory": "resources-management/plan-record-resources",
        },
        "plastic-storage": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/plastic-storage/",
            "subcategory": "classroom-organization/plastic-storage",
        },
        "pocket-charts": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/pocket-charts/",
            "subcategory": "resources-management/pocket-charts",
        },
        "poetry": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/poetry/",
            "subcategory": "shop-by-class-subject/reading-language-arts/poetry",
        },
        "pointers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/pointers/",
            "subcategory": "resources-management/pointers",
        },
        "postcards": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/postcards/",
            "subcategory": "awards-incentives/postcards",
        },
        "progress-notices": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/progress-notices/",
            "subcategory": "resources-management/progress-notices",
        },
        "pumps": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/pumps/",
            "subcategory": "shop-by-class-subject/physical-education/pumps",
        },
        "reading-aids": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/reading-aids/",
            "subcategory": "shop-by-class-subject/reading-language-arts/reading-aids",
        },
        "reference-books": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/reference-books/",
            "subcategory": "shop-by-class-subject/reading-language-arts/reference-books",
        },
        "resources": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/music/resources/",
            "subcategory": "shop-by-class-subject/music/resources",
        },
        "resources-management": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/",
            "subcategory": "resources-management",
        },
        "rest-time": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/rest-time/",
            "subcategory": "resources-management/rest-time",
        },
        "robotics": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/robotics/",
            "subcategory": "shop-by-class-subject/science/robotics",
        },
        "seasonal-holiday": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-sets/seasonal-holiday/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-sets/seasonal-holiday",
        },
        "sentence-strips": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/sentence-strips/",
            "subcategory": "shop-by-class-subject/reading-language-arts/sentence-strips",
        },
        "shop-by-class-subject": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/",
            "subcategory": "shop-by-class-subject",
        },
        "shop-by-subject": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/shop-by-subject/",
            "subcategory": "classroom-decorations/shop-by-subject",
        },
        "sight-words-word-skills": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/sight-words-word-skills/",
            "subcategory": "shop-by-class-subject/reading-language-arts/sight-words-word-skills",
        },
        "simple-machines": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/simple-machines/",
            "subcategory": "shop-by-class-subject/science/simple-machines",
        },
        "solid-bulletin-borders": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-borders-trim/solid-bulletin-borders/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-borders-trim/solid-bulletin-borders",
        },
        "sorting": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/basic-skills/sorting/",
            "subcategory": "shop-by-class-subject/basic-skills/sorting",
        },
        "spelling": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/spelling/",
            "subcategory": "shop-by-class-subject/reading-language-arts/spelling",
        },
        "stamps-stencils": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/stamps-stencils/",
            "subcategory": "arts-crafts-supplies/craft-supplies/stamps-stencils",
        },
        "state-sets": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-sets/state-sets/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-sets/state-sets",
        },
        "states-capitals": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/social-studies/states-capitals/",
            "subcategory": "shop-by-class-subject/social-studies/states-capitals",
        },
        "study-activity-books": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/social-studies/study-activity-books/",
            "subcategory": "shop-by-class-subject/social-studies/study-activity-books",
        },
        "substitute-teachers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/substitute-teachers/",
            "subcategory": "resources-management/substitute-teachers",
        },
        "tangrams": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/tangrams/",
            "subcategory": "shop-by-class-subject/math/tangrams",
        },
        "teacher-supplies-art-storage": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/art-storage/",
            "subcategory": "classroom-organization/art-storage",
        },
        "teacher-supplies-bags": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/bags/",
            "subcategory": "shop-by-class-subject/physical-education/bags",
        },
        "teacher-supplies-bags-totes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/bags-totes/",
            "subcategory": "classroom-organization/bags-totes",
        },
        "teacher-supplies-bells": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/bells/",
            "subcategory": "arts-crafts-supplies/craft-supplies/bells",
        },
        "teacher-supplies-birthday": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-sets/birthday/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-sets/birthday",
        },
        "teacher-supplies-black-history-month": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/black-history-month/",
            "subcategory": "classroom-decorations/black-history-month",
        },
        "teacher-supplies-brushes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paints-brushes/brushes/",
            "subcategory": "arts-crafts-supplies/paints-brushes/brushes",
        },
        "teacher-supplies-calculators": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/calculators/",
            "subcategory": "shop-by-class-subject/math/calculators",
        },
        "teacher-supplies-calendars": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/bulletin-board-supplies/bulletin-board-sets/calendars/",
            "subcategory": "classroom-decorations/bulletin-board-supplies/bulletin-board-sets/calendars",
        },
        "teacher-supplies-canvas": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/canvas/",
            "subcategory": "arts-crafts-supplies/canvas",
        },
        "teacher-supplies-carts-drawer-units": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/carts-drawer-units/",
            "subcategory": "classroom-organization/carts-drawer-units",
        },
        "teacher-supplies-chenille-stems": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/chenille-stems/",
            "subcategory": "arts-crafts-supplies/craft-supplies/chenille-stems",
        },
        "teacher-supplies-colored-pencils": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/colored-pencils/",
            "subcategory": "arts-crafts-supplies/colored-pencils",
        },
        "teacher-supplies-construction-drawing-paper": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/construction-drawing-paper/",
            "subcategory": "arts-crafts-supplies/paper/construction-drawing-paper",
        },
        "teacher-supplies-construction-drawing-paper-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/paper/construction-drawing-paper/",
            "subcategory": "resources-management/paper/construction-drawing-paper",
        },
        "teacher-supplies-craft-activities": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/craft-activities/",
            "subcategory": "arts-crafts-supplies/craft-supplies/craft-activities",
        },
        "teacher-supplies-craft-supplies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/",
            "subcategory": "arts-crafts-supplies/craft-supplies",
        },
        "teacher-supplies-craft-surfaces": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/craft-surfaces/",
            "subcategory": "arts-crafts-supplies/craft-supplies/craft-surfaces",
        },
        "teacher-supplies-crayons": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/crayons/",
            "subcategory": "arts-crafts-supplies/crayons",
        },
        "teacher-supplies-curriculum-resources": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/curriculum-resources/",
            "subcategory": "shop-by-class-subject/math/curriculum-resources",
        },
        "teacher-supplies-curriculum-resources-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/curriculum-resources/",
            "subcategory": "shop-by-class-subject/reading-language-arts/curriculum-resources",
        },
        "teacher-supplies-curriculum-resources-3": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/curriculum-resources/",
            "subcategory": "shop-by-class-subject/science/curriculum-resources",
        },
        "teacher-supplies-decor": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/wall-tabletop-decorations/decor/",
            "subcategory": "classroom-decorations/wall-tabletop-decorations/decor",
        },
        "teacher-supplies-desktop-storage": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/desktop-storage/",
            "subcategory": "classroom-organization/desktop-storage",
        },
        "teacher-supplies-drawing-supplies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/drawing-supplies/",
            "subcategory": "arts-crafts-supplies/drawing-supplies",
        },
        "teacher-supplies-dry-erase": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/dry-erase/",
            "subcategory": "arts-crafts-supplies/paper/dry-erase",
        },
        "teacher-supplies-dry-erase-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/paper/dry-erase/",
            "subcategory": "resources-management/paper/dry-erase",
        },
        "teacher-supplies-dry-erase-boards": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/dry-erase-boards/",
            "subcategory": "resources-management/dry-erase-boards",
        },
        "teacher-supplies-easel-pads": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/paper/easel-pads/",
            "subcategory": "resources-management/paper/easel-pads",
        },
        "teacher-supplies-easel-pads-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/easel-pads/",
            "subcategory": "arts-crafts-supplies/paper/easel-pads",
        },
        "teacher-supplies-erasers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/erasers/",
            "subcategory": "arts-crafts-supplies/erasers",
        },
        "teacher-supplies-feathers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/feathers/",
            "subcategory": "arts-crafts-supplies/craft-supplies/feathers",
        },
        "teacher-supplies-felt": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/felt/",
            "subcategory": "arts-crafts-supplies/craft-supplies/felt",
        },
        "teacher-supplies-flags": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/flags/",
            "subcategory": "classroom-decorations/flags",
        },
        "teacher-supplies-foam": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/foam/",
            "subcategory": "arts-crafts-supplies/craft-supplies/foam",
        },
        "teacher-supplies-glitter": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/glitter/",
            "subcategory": "arts-crafts-supplies/craft-supplies/glitter",
        },
        "teacher-supplies-glue": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/glue/",
            "subcategory": "arts-crafts-supplies/glue",
        },
        "teacher-supplies-googly-eyes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/googly-eyes/",
            "subcategory": "arts-crafts-supplies/craft-supplies/googly-eyes",
        },
        "teacher-supplies-labels": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/labels/",
            "subcategory": "classroom-organization/labels",
        },
        "teacher-supplies-life-science": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/life-science/",
            "subcategory": "shop-by-class-subject/science/life-science",
        },
        "teacher-supplies-locked-storage": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/locked-storage/",
            "subcategory": "classroom-organization/locked-storage",
        },
        "teacher-supplies-markers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/markers/",
            "subcategory": "arts-crafts-supplies/markers",
        },
        "teacher-supplies-math": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/shop-by-subject/math/",
            "subcategory": "classroom-decorations/shop-by-subject/math",
        },
        "teacher-supplies-math-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/",
            "subcategory": "shop-by-class-subject/math",
        },
        "teacher-supplies-misc-paper": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/misc-paper/",
            "subcategory": "arts-crafts-supplies/paper/misc-paper",
        },
        "teacher-supplies-misc-paper-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/paper/misc-paper/",
            "subcategory": "resources-management/paper/misc-paper",
        },
        "teacher-supplies-music": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/music/",
            "subcategory": "shop-by-class-subject/music",
        },
        "teacher-supplies-novelty": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/novelty/",
            "subcategory": "awards-incentives/novelty",
        },
        "teacher-supplies-paint": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paints-brushes/paint/",
            "subcategory": "arts-crafts-supplies/paints-brushes/paint",
        },
        "teacher-supplies-paper": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/",
            "subcategory": "arts-crafts-supplies/paper",
        },
        "teacher-supplies-paper-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/paper/",
            "subcategory": "resources-management/paper",
        },
        "teacher-supplies-party-supplies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/wall-tabletop-decorations/party-supplies/",
            "subcategory": "classroom-decorations/wall-tabletop-decorations/party-supplies",
        },
        "teacher-supplies-patterns": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/basic-skills/patterns/",
            "subcategory": "shop-by-class-subject/basic-skills/patterns",
        },
        "teacher-supplies-pencils": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/pencils/",
            "subcategory": "awards-incentives/pencils",
        },
        "teacher-supplies-pom-poms": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/pom-poms/",
            "subcategory": "arts-crafts-supplies/craft-supplies/pom-poms",
        },
        "teacher-supplies-poster-tag-board": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/paper/poster-tag-board/",
            "subcategory": "arts-crafts-supplies/paper/poster-tag-board",
        },
        "teacher-supplies-poster-tag-board-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/paper/poster-tag-board/",
            "subcategory": "resources-management/paper/poster-tag-board",
        },
        "teacher-supplies-push-pins": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/push-pins/",
            "subcategory": "classroom-decorations/push-pins",
        },
        "teacher-supplies-reading-language-arts": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/",
            "subcategory": "shop-by-class-subject/reading-language-arts",
        },
        "teacher-supplies-reading-language-arts-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/shop-by-subject/reading-language-arts/",
            "subcategory": "classroom-decorations/shop-by-subject/reading-language-arts",
        },
        "teacher-supplies-science": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/",
            "subcategory": "shop-by-class-subject/science",
        },
        "teacher-supplies-science-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/shop-by-subject/science/",
            "subcategory": "classroom-decorations/shop-by-subject/science",
        },
        "teacher-supplies-scissors": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/scissors/",
            "subcategory": "arts-crafts-supplies/scissors",
        },
        "teacher-supplies-sequins": {
            "url": "https://www.michaels.com/shop/teacher-supplies/arts-crafts-supplies/craft-supplies/sequins/",
            "subcategory": "arts-crafts-supplies/craft-supplies/sequins",
        },
        "teacher-supplies-shapes": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/basic-skills/shapes/",
            "subcategory": "shop-by-class-subject/basic-skills/shapes",
        },
        "teacher-supplies-social-studies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/social-studies/",
            "subcategory": "shop-by-class-subject/social-studies",
        },
        "teacher-supplies-social-studies-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/shop-by-subject/social-studies/",
            "subcategory": "classroom-decorations/shop-by-subject/social-studies",
        },
        "teacher-supplies-stamps-stamp-pads": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/stamps-stamp-pads/",
            "subcategory": "awards-incentives/stamps-stamp-pads",
        },
        "teacher-supplies-stickers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/stickers/",
            "subcategory": "awards-incentives/stickers",
        },
        "teacher-supplies-stools": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-organization/stools/",
            "subcategory": "classroom-organization/stools",
        },
        "teacher-supplies-teacher-supplies": {
            "url": "https://www.michaels.com/shop/teacher-supplies/",
            "subcategory": "teacher-supplies",
        },
        "teacher-supplies-teacher-supplies-2": {
            "url": "https://www.michaels.com/shop/teacher-supplies/teacher-supplies/",
            "subcategory": "teacher-supplies",
        },
        "teacher-supplies-timers": {
            "url": "https://www.michaels.com/shop/teacher-supplies/resources-management/timers/",
            "subcategory": "resources-management/timers",
        },
        "test": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/test/",
            "subcategory": "shop-by-class-subject/math/test",
        },
        "time": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/time/",
            "subcategory": "shop-by-class-subject/math/time",
        },
        "unifix-cubes-cuisenaire-rods": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/unifix-cubes-cuisenaire-rods/",
            "subcategory": "shop-by-class-subject/math/unifix-cubes-cuisenaire-rods",
        },
        "vocabulary": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/vocabulary/",
            "subcategory": "shop-by-class-subject/reading-language-arts/vocabulary",
        },
        "wall-tabletop-decorations": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/wall-tabletop-decorations/",
            "subcategory": "classroom-decorations/wall-tabletop-decorations",
        },
        "weather": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/science/weather/",
            "subcategory": "shop-by-class-subject/science/weather",
        },
        "welcome-banners": {
            "url": "https://www.michaels.com/shop/teacher-supplies/classroom-decorations/welcome-banners/",
            "subcategory": "classroom-decorations/welcome-banners",
        },
        "whistles": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/physical-education/whistles/",
            "subcategory": "shop-by-class-subject/physical-education/whistles",
        },
        "word-problems": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/math/word-problems/",
            "subcategory": "shop-by-class-subject/math/word-problems",
        },
        "wristbands": {
            "url": "https://www.michaels.com/shop/teacher-supplies/awards-incentives/wristbands/",
            "subcategory": "awards-incentives/wristbands",
        },
        "writing": {
            "url": "https://www.michaels.com/shop/teacher-supplies/shop-by-class-subject/reading-language-arts/writing/",
            "subcategory": "shop-by-class-subject/reading-language-arts/writing",
        },
    },
    "wedding": {
        "aisle-runners": {
            "url": "https://www.michaels.com/shop/wedding/decor/ceremony-decor/aisle-runners/",
            "subcategory": "decor/ceremony-decor/aisle-runners",
        },
        "attendants": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/gifts/attendants/",
            "subcategory": "shop-by-event/bachelorette-party/gifts/attendants",
        },
        "bachelor-party": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelor-party/",
            "subcategory": "shop-by-event/bachelor-party",
        },
        "bachelorette-party": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/",
            "subcategory": "shop-by-event/bachelorette-party",
        },
        "banners-signs": {
            "url": "https://www.michaels.com/shop/wedding/decor/banners-signs/",
            "subcategory": "decor/banners-signs",
        },
        "bottle-openers": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/favors/bottle-openers/",
            "subcategory": "shop-by-event/bachelorette-party/favors/bottle-openers",
        },
        "bridal-accessories": {
            "url": "https://www.michaels.com/shop/wedding/bridal-accessories/",
            "subcategory": "bridal-accessories",
        },
        "bridal-bouquets": {
            "url": "https://www.michaels.com/shop/wedding/floral-bouquets/bridal-bouquets/",
            "subcategory": "floral-bouquets/bridal-bouquets",
        },
        "bridesmaids-gifts": {
            "url": "https://www.michaels.com/shop/wedding/gifts/wedding-attendant-gifts/bridesmaids-gifts/",
            "subcategory": "gifts/wedding-attendant-gifts/bridesmaids-gifts",
        },
        "cake-stands-servers-toppers": {
            "url": "https://www.michaels.com/shop/wedding/decor/cake-stands-servers-toppers/",
            "subcategory": "decor/cake-stands-servers-toppers",
        },
        "cake-toppers": {
            "url": "https://www.michaels.com/shop/wedding/decor/cake-stands-servers-toppers/cake-toppers/",
            "subcategory": "decor/cake-stands-servers-toppers/cake-toppers",
        },
        "candy-buffet": {
            "url": "https://www.michaels.com/shop/wedding/favors/candy-buffet/",
            "subcategory": "favors/candy-buffet",
        },
        "centerpieces": {
            "url": "https://www.michaels.com/shop/wedding/decor/centerpieces/",
            "subcategory": "decor/centerpieces",
        },
        "ceremony-decor": {
            "url": "https://www.michaels.com/shop/wedding/decor/ceremony-decor/",
            "subcategory": "decor/ceremony-decor",
        },
        "chalkboard-diy-surfaces": {
            "url": "https://www.michaels.com/shop/wedding/decor/chalkboard-diy-surfaces/",
            "subcategory": "decor/chalkboard-diy-surfaces",
        },
        "corsages-boutonnieres": {
            "url": "https://www.michaels.com/shop/wedding/floral-bouquets/corsages-boutonnieres/",
            "subcategory": "floral-bouquets/corsages-boutonnieres",
        },
        "decorative": {
            "url": "https://www.michaels.com/shop/wedding/decor/ribbon-tulle/decorative/",
            "subcategory": "decor/ribbon-tulle/decorative",
        },
        "decorative-accents": {
            "url": "https://www.michaels.com/shop/wedding/decor/decorative-accents/",
            "subcategory": "decor/decorative-accents",
        },
        "embellishments-stickers-tags": {
            "url": "https://www.michaels.com/shop/wedding/invitations/embellishments-stickers-tags/",
            "subcategory": "invitations/embellishments-stickers-tags",
        },
        "floral-bouquets": {
            "url": "https://www.michaels.com/shop/wedding/floral-bouquets/",
            "subcategory": "floral-bouquets",
        },
        "flower-girl-baskets": {
            "url": "https://www.michaels.com/shop/wedding/decor/ceremony-decor/flower-girl-baskets/",
            "subcategory": "decor/ceremony-decor/flower-girl-baskets",
        },
        "flower-girl-gifts": {
            "url": "https://www.michaels.com/shop/wedding/gifts/wedding-attendant-gifts/flower-girl-gifts/",
            "subcategory": "gifts/wedding-attendant-gifts/flower-girl-gifts",
        },
        "flower-petal-packs": {
            "url": "https://www.michaels.com/shop/wedding/floral-bouquets/flower-petal-packs/",
            "subcategory": "floral-bouquets/flower-petal-packs",
        },
        "for-the-bride": {
            "url": "https://www.michaels.com/shop/wedding/gifts/for-the-bride/",
            "subcategory": "gifts/for-the-bride",
        },
        "for-the-couple": {
            "url": "https://www.michaels.com/shop/wedding/gifts/for-the-couple/",
            "subcategory": "gifts/for-the-couple",
        },
        "for-the-groom": {
            "url": "https://www.michaels.com/shop/wedding/gifts/for-the-groom/",
            "subcategory": "gifts/for-the-groom",
        },
        "groomsmen-gifts": {
            "url": "https://www.michaels.com/shop/wedding/gifts/wedding-attendant-gifts/groomsmen-gifts/",
            "subcategory": "gifts/wedding-attendant-gifts/groomsmen-gifts",
        },
        "guest-books-pens": {
            "url": "https://www.michaels.com/shop/wedding/decor/guest-books-pens/",
            "subcategory": "decor/guest-books-pens",
        },
        "hair-ribbons": {
            "url": "https://www.michaels.com/shop/wedding/decor/ribbon-tulle/hair-ribbons/",
            "subcategory": "decor/ribbon-tulle/hair-ribbons",
        },
        "invitations-programs": {
            "url": "https://www.michaels.com/shop/wedding/invitations/invitations-programs/",
            "subcategory": "invitations/invitations-programs",
        },
        "lighted-branches": {
            "url": "https://www.michaels.com/shop/wedding/decor/lighting-candles/lighted-branches/",
            "subcategory": "decor/lighting-candles/lighted-branches",
        },
        "lighting-candles": {
            "url": "https://www.michaels.com/shop/wedding/decor/lighting-candles/",
            "subcategory": "decor/lighting-candles",
        },
        "makerplace-personalized-wedding": {
            "url": "https://www.michaels.com/shop/wedding/makerplace-personalized-wedding/",
            "subcategory": "makerplace-personalized-wedding",
        },
        "parents-grandparents": {
            "url": "https://www.michaels.com/shop/wedding/gifts/parents-grandparents/",
            "subcategory": "gifts/parents-grandparents",
        },
        "party-accessories": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/party-accessories/",
            "subcategory": "shop-by-event/bachelorette-party/party-accessories",
        },
        "ribbon-tulle": {
            "url": "https://www.michaels.com/shop/wedding/decor/ribbon-tulle/",
            "subcategory": "decor/ribbon-tulle",
        },
        "ring-bearer-gifts": {
            "url": "https://www.michaels.com/shop/wedding/gifts/wedding-attendant-gifts/ring-bearer-gifts/",
            "subcategory": "gifts/wedding-attendant-gifts/ring-bearer-gifts",
        },
        "ring-bearer-pillows": {
            "url": "https://www.michaels.com/shop/wedding/decor/ceremony-decor/ring-bearer-pillows/",
            "subcategory": "decor/ceremony-decor/ring-bearer-pillows",
        },
        "servers": {
            "url": "https://www.michaels.com/shop/wedding/decor/cake-stands-servers-toppers/servers/",
            "subcategory": "decor/cake-stands-servers-toppers/servers",
        },
        "submersible-lights": {
            "url": "https://www.michaels.com/shop/wedding/decor/lighting-candles/submersible-lights/",
            "subcategory": "decor/lighting-candles/submersible-lights",
        },
        "table-covers-runners": {
            "url": "https://www.michaels.com/shop/wedding/decor/tableware-drinkware/table-covers-runners/",
            "subcategory": "decor/tableware-drinkware/table-covers-runners",
        },
        "table-numbers-place-cards-holders": {
            "url": "https://www.michaels.com/shop/wedding/decor/table-numbers-place-cards-holders/",
            "subcategory": "decor/table-numbers-place-cards-holders",
        },
        "tableware-drinkware": {
            "url": "https://www.michaels.com/shop/wedding/decor/tableware-drinkware/",
            "subcategory": "decor/tableware-drinkware",
        },
        "thank-you-cards": {
            "url": "https://www.michaels.com/shop/wedding/invitations/thank-you-cards/",
            "subcategory": "invitations/thank-you-cards",
        },
        "toasting-glasses": {
            "url": "https://www.michaels.com/shop/wedding/decor/tableware-drinkware/toasting-glasses/",
            "subcategory": "decor/tableware-drinkware/toasting-glasses",
        },
        "unity-sand-ceremony": {
            "url": "https://www.michaels.com/shop/wedding/decor/ceremony-decor/unity-sand-ceremony/",
            "subcategory": "decor/ceremony-decor/unity-sand-ceremony",
        },
        "wedding": {
            "url": "https://www.michaels.com/shop/wedding/",
            "subcategory": "wedding",
        },
        "wedding-accessories": {
            "url": "https://www.michaels.com/shop/wedding/decor/ribbon-tulle/accessories/",
            "subcategory": "decor/ribbon-tulle/accessories",
        },
        "wedding-attendant-gifts": {
            "url": "https://www.michaels.com/shop/wedding/gifts/wedding-attendant-gifts/",
            "subcategory": "gifts/wedding-attendant-gifts",
        },
        "wedding-bags-boxes-containers": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/favors/bags-boxes-containers/",
            "subcategory": "shop-by-event/bachelorette-party/favors/bags-boxes-containers",
        },
        "wedding-bags-boxes-containers-2": {
            "url": "https://www.michaels.com/shop/wedding/favors/bags-boxes-containers/",
            "subcategory": "favors/bags-boxes-containers",
        },
        "wedding-bubbles": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/favors/bubbles/",
            "subcategory": "shop-by-event/bachelorette-party/favors/bubbles",
        },
        "wedding-cake-stands": {
            "url": "https://www.michaels.com/shop/wedding/decor/cake-stands-servers-toppers/cake-stands/",
            "subcategory": "decor/cake-stands-servers-toppers/cake-stands",
        },
        "wedding-candle-holders": {
            "url": "https://www.michaels.com/shop/wedding/decor/lighting-candles/candle-holders/",
            "subcategory": "decor/lighting-candles/candle-holders",
        },
        "wedding-candles": {
            "url": "https://www.michaels.com/shop/wedding/decor/lighting-candles/candles/",
            "subcategory": "decor/lighting-candles/candles",
        },
        "wedding-card-envelope-holders": {
            "url": "https://www.michaels.com/shop/wedding/decor/wedding-card-envelope-holders/",
            "subcategory": "decor/wedding-card-envelope-holders",
        },
        "wedding-chargers": {
            "url": "https://www.michaels.com/shop/wedding/decor/chargers/",
            "subcategory": "decor/chargers",
        },
        "wedding-decor": {
            "url": "https://www.michaels.com/shop/wedding/decor/",
            "subcategory": "decor",
        },
        "wedding-drinkware": {
            "url": "https://www.michaels.com/shop/wedding/decor/tableware-drinkware/drinkware/",
            "subcategory": "decor/tableware-drinkware/drinkware",
        },
        "wedding-embellishments": {
            "url": "https://www.michaels.com/shop/wedding/invitations/embellishments-stickers-tags/embellishments/",
            "subcategory": "invitations/embellishments-stickers-tags/embellishments",
        },
        "wedding-favors": {
            "url": "https://www.michaels.com/shop/wedding/favors/favors/",
            "subcategory": "favors/favors",
        },
        "wedding-favors-2": {
            "url": "https://www.michaels.com/shop/wedding/favors/",
            "subcategory": "favors",
        },
        "wedding-favors-3": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/favors/",
            "subcategory": "shop-by-event/bachelorette-party/favors",
        },
        "wedding-gifts": {
            "url": "https://www.michaels.com/shop/wedding/gifts/",
            "subcategory": "gifts",
        },
        "wedding-gifts-2": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/gifts/",
            "subcategory": "shop-by-event/bachelorette-party/gifts",
        },
        "wedding-glass-jars": {
            "url": "https://www.michaels.com/shop/wedding/favors/glass-jars/",
            "subcategory": "favors/glass-jars",
        },
        "wedding-glass-jars-2": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/bachelorette-party/favors/glass-jars/",
            "subcategory": "shop-by-event/bachelorette-party/favors/glass-jars",
        },
        "wedding-invitations": {
            "url": "https://www.michaels.com/shop/wedding/invitations/",
            "subcategory": "invitations",
        },
        "wedding-lanterns": {
            "url": "https://www.michaels.com/shop/wedding/decor/lighting-candles/lanterns/",
            "subcategory": "decor/lighting-candles/lanterns",
        },
        "wedding-mesh": {
            "url": "https://www.michaels.com/shop/wedding/decor/ribbon-tulle/mesh/",
            "subcategory": "decor/ribbon-tulle/mesh",
        },
        "wedding-paper": {
            "url": "https://www.michaels.com/shop/wedding/invitations/paper/",
            "subcategory": "invitations/paper",
        },
        "wedding-shower": {
            "url": "https://www.michaels.com/shop/wedding/shop-by-event/wedding-shower/",
            "subcategory": "shop-by-event/wedding-shower",
        },
        "wedding-stickers": {
            "url": "https://www.michaels.com/shop/wedding/invitations/embellishments-stickers-tags/stickers/",
            "subcategory": "invitations/embellishments-stickers-tags/stickers",
        },
        "wedding-string-lights": {
            "url": "https://www.michaels.com/shop/wedding/decor/lighting-candles/string-lights/",
            "subcategory": "decor/lighting-candles/string-lights",
        },
        "wedding-tableware": {
            "url": "https://www.michaels.com/shop/wedding/decor/tableware-drinkware/tableware/",
            "subcategory": "decor/tableware-drinkware/tableware",
        },
        "wedding-tags": {
            "url": "https://www.michaels.com/shop/wedding/invitations/embellishments-stickers-tags/tags/",
            "subcategory": "invitations/embellishments-stickers-tags/tags",
        },
        "wedding-trim": {
            "url": "https://www.michaels.com/shop/wedding/decor/ribbon-tulle/trim/",
            "subcategory": "decor/ribbon-tulle/trim",
        },
        "wedding-tulle": {
            "url": "https://www.michaels.com/shop/wedding/tulle/",
            "subcategory": "tulle",
        },
        "wedding-tulle-2": {
            "url": "https://www.michaels.com/shop/wedding/decor/ribbon-tulle/tulle/",
            "subcategory": "decor/ribbon-tulle/tulle",
        },
        "wedding-vases-containers": {
            "url": "https://www.michaels.com/shop/wedding/floral-bouquets/vases-containers/",
            "subcategory": "floral-bouquets/vases-containers",
        },
    },
    "yarn-needlework": {
        "baby-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/baby-yarn/",
            "subcategory": "shop-all-yarn/baby-yarn",
        },
        "basic-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/basic-yarn/",
            "subcategory": "shop-all-yarn/basic-yarn",
        },
        "beadwork": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/beadwork/",
            "subcategory": "needlework-fiber-arts/beadwork",
        },
        "bernat-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/bernat-yarn/",
            "subcategory": "featured-yarn-brands/bernat-yarn",
        },
        "big-twist-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/big-twist-yarn/",
            "subcategory": "featured-yarn-brands/big-twist-yarn",
        },
        "cable-needles": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-needles/cable-needles/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-needles/cable-needles",
        },
        "canvas-tools": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/needlepoint/canvas-tools/",
            "subcategory": "needlework-fiber-arts/needlepoint/canvas-tools",
        },
        "caron-cakes": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/caron-cakes-shop/caron-cakes/",
            "subcategory": "shop-all-yarn/caron-cakes-shop/caron-cakes",
        },
        "caron-cakes-birthday": {
            "url": "https://www.michaels.com/shop/yarn-needlework/caron-cakes-birthday/",
            "subcategory": "caron-cakes-birthday",
        },
        "caron-cakes-shop": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/caron-cakes-shop/",
            "subcategory": "shop-all-yarn/caron-cakes-shop",
        },
        "caron-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/caron-yarn/",
            "subcategory": "featured-yarn-brands/caron-yarn",
        },
        "circular-needles": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-needles/circular-needles/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-needles/circular-needles",
        },
        "cloth-canvas": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/cloth-canvas/",
            "subcategory": "needlework-fiber-arts/cloth-canvas",
        },
        "crochet-accessories": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/crochet-supplies/crochet-accessories/",
            "subcategory": "knitting-crochet/crochet-supplies/crochet-accessories",
        },
        "crochet-books-learning-guides": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/crochet-supplies/crochet-books-learning-guides/",
            "subcategory": "knitting-crochet/crochet-supplies/crochet-books-learning-guides",
        },
        "crochet-hooks": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/crochet-supplies/crochet-hooks/",
            "subcategory": "knitting-crochet/crochet-supplies/crochet-hooks",
        },
        "crochet-kits": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/crochet-kits/",
            "subcategory": "knitting-crochet/crochet-kits",
        },
        "crochet-supplies": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/crochet-supplies/",
            "subcategory": "knitting-crochet/crochet-supplies",
        },
        "crochet-thread": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/crochet-supplies/crochet-thread/",
            "subcategory": "knitting-crochet/crochet-supplies/crochet-thread",
        },
        "cross-stitch": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/cross-stitch-embroidery/cross-stitch/",
            "subcategory": "needlework-fiber-arts/cross-stitch-embroidery/cross-stitch",
        },
        "cross-stitch-embroidery": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/cross-stitch-embroidery/",
            "subcategory": "needlework-fiber-arts/cross-stitch-embroidery",
        },
        "dmc": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/dmc/",
            "subcategory": "needlework-fiber-arts/dmc",
        },
        "double-pointed-needles": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-needles/double-pointed-needles/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-needles/double-pointed-needles",
        },
        "embroidery": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/cross-stitch-embroidery/embroidery/",
            "subcategory": "needlework-fiber-arts/cross-stitch-embroidery/embroidery",
        },
        "featured-yarn-brands": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/",
            "subcategory": "featured-yarn-brands",
        },
        "felting": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/felting/",
            "subcategory": "needlework-fiber-arts/felting",
        },
        "floss": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/floss/",
            "subcategory": "needlework-fiber-arts/floss",
        },
        "floss-packs": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/floss-packs/",
            "subcategory": "needlework-fiber-arts/floss-packs",
        },
        "home-decor-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/home-decor-yarn/",
            "subcategory": "shop-all-yarn/home-decor-yarn",
        },
        "knitting-accessories": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-accessories/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-accessories",
        },
        "knitting-books-learning-guides": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-books-learning-guides/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-books-learning-guides",
        },
        "knitting-looms": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-looms/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-looms",
        },
        "knitting-needles": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-needles/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-needles",
        },
        "knitting-supplies": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/",
            "subcategory": "knitting-crochet/knitting-supplies",
        },
        "latch-hook": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/latch-hook/",
            "subcategory": "needlework-fiber-arts/latch-hook",
        },
        "limited-time-caron-cakes": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/caron-cakes-shop/limited-time-caron-cakes/",
            "subcategory": "shop-all-yarn/caron-cakes-shop/limited-time-caron-cakes",
        },
        "limited-time-loops-threads": {
            "url": "https://www.michaels.com/shop/yarn-needlework/loops-threads/limited-time-loops-threads/",
            "subcategory": "loops-threads/limited-time-loops-threads",
        },
        "lion-brand-multi-packs": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/lion-brand-yarn/lion-brand-multi-packs/",
            "subcategory": "featured-yarn-brands/lion-brand-yarn/lion-brand-multi-packs",
        },
        "lion-brand-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/lion-brand-yarn/",
            "subcategory": "featured-yarn-brands/lion-brand-yarn",
        },
        "loops-threads-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/loops-threads-yarn/",
            "subcategory": "featured-yarn-brands/loops-threads-yarn",
        },
        "more-lion-brand-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/lion-brand-yarn/more-lion-brand-yarn/",
            "subcategory": "featured-yarn-brands/lion-brand-yarn/more-lion-brand-yarn",
        },
        "natural-sustainable-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/natural-sustainable-yarn/",
            "subcategory": "shop-all-yarn/natural-sustainable-yarn",
        },
        "needle-cases": {
            "url": "https://www.michaels.com/shop/yarn-needlework/storage-organization/needle-cases/",
            "subcategory": "storage-organization/needle-cases",
        },
        "needlepoint": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/needlepoint/",
            "subcategory": "needlework-fiber-arts/needlepoint",
        },
        "needlepoint-kits": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/needlepoint/needlepoint-kits/",
            "subcategory": "needlework-fiber-arts/needlepoint/needlepoint-kits",
        },
        "needlework-accessories": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/needlework-accessories/",
            "subcategory": "needlework-fiber-arts/needlework-accessories",
        },
        "needlework-fiber-arts": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/",
            "subcategory": "needlework-fiber-arts",
        },
        "punch-needle": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/punch-needle/",
            "subcategory": "needlework-fiber-arts/punch-needle",
        },
        "red-heart-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/red-heart-yarn/",
            "subcategory": "featured-yarn-brands/red-heart-yarn",
        },
        "rug-tufting": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/rug-tufting/",
            "subcategory": "needlework-fiber-arts/rug-tufting",
        },
        "rug-tufting-essential-tools": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/rug-tufting/rug-tufting-essential-tools/",
            "subcategory": "needlework-fiber-arts/rug-tufting/rug-tufting-essential-tools",
        },
        "rug-tufting-materials": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/rug-tufting/rug-tufting-materials/",
            "subcategory": "needlework-fiber-arts/rug-tufting/rug-tufting-materials",
        },
        "shop-all-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/",
            "subcategory": "shop-all-yarn",
        },
        "stitch-counters": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/stitch-counters/",
            "subcategory": "knitting-crochet/stitch-counters",
        },
        "stitch-holders": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/stitch-holders/",
            "subcategory": "knitting-crochet/stitch-holders",
        },
        "stitch-markers": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/stitch-markers/",
            "subcategory": "knitting-crochet/stitch-markers",
        },
        "stitchery-kits": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/dmc/stitchery-kits/",
            "subcategory": "needlework-fiber-arts/dmc/stitchery-kits",
        },
        "storage-organization": {
            "url": "https://www.michaels.com/shop/yarn-needlework/storage-organization/",
            "subcategory": "storage-organization",
        },
        "straight-needles": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-needles/straight-needles/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-needles/straight-needles",
        },
        "string-art-wood-cross-stitch": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/string-art-wood-cross-stitch/",
            "subcategory": "needlework-fiber-arts/string-art-wood-cross-stitch",
        },
        "value-yarn": {
            "url": "https://www.michaels.com/shop/yarn-needlework/shop-all-yarn/value-yarn/",
            "subcategory": "shop-all-yarn/value-yarn",
        },
        "weaving": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/weaving/",
            "subcategory": "needlework-fiber-arts/weaving",
        },
        "wool-ease-collections": {
            "url": "https://www.michaels.com/shop/yarn-needlework/featured-yarn-brands/lion-brand-yarn/wool-ease-collections/",
            "subcategory": "featured-yarn-brands/lion-brand-yarn/wool-ease-collections",
        },
        "yarn-bowls-dispensers": {
            "url": "https://www.michaels.com/shop/yarn-needlework/storage-organization/yarn-bowls-dispensers/",
            "subcategory": "storage-organization/yarn-bowls-dispensers",
        },
        "yarn-needlework": {
            "url": "https://www.michaels.com/shop/yarn-needlework/",
            "subcategory": "yarn-needlework",
        },
        "yarn-needlework-bags": {
            "url": "https://www.michaels.com/shop/yarn-needlework/storage-organization/bags/",
            "subcategory": "storage-organization/bags",
        },
        "yarn-needlework-baskets": {
            "url": "https://www.michaels.com/shop/yarn-needlework/storage-organization/baskets/",
            "subcategory": "storage-organization/baskets",
        },
        "yarn-needlework-darning-yarn-needles": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/crochet-supplies/darning-yarn-needles/",
            "subcategory": "knitting-crochet/crochet-supplies/darning-yarn-needles",
        },
        "yarn-needlework-darning-yarn-needles-2": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/knitting-supplies/knitting-needles/darning-yarn-needles/",
            "subcategory": "knitting-crochet/knitting-supplies/knitting-needles/darning-yarn-needles",
        },
        "yarn-needlework-hoops-frames": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/hoops-frames/",
            "subcategory": "needlework-fiber-arts/hoops-frames",
        },
        "yarn-needlework-knitting-crochet": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/",
            "subcategory": "knitting-crochet",
        },
        "yarn-needlework-lace": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/lace/",
            "subcategory": "needlework-fiber-arts/lace",
        },
        "yarn-needlework-loops-threads": {
            "url": "https://www.michaels.com/shop/yarn-needlework/loops-threads/",
            "subcategory": "loops-threads",
        },
        "yarn-needlework-macrame": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/macrame/",
            "subcategory": "needlework-fiber-arts/macrame",
        },
        "yarn-needlework-needles": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/cross-stitch-embroidery/needles/",
            "subcategory": "needlework-fiber-arts/cross-stitch-embroidery/needles",
        },
        "yarn-needlework-scissors": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/scissors/",
            "subcategory": "knitting-crochet/scissors",
        },
        "yarn-needlework-tools": {
            "url": "https://www.michaels.com/shop/yarn-needlework/needlework-fiber-arts/cross-stitch-embroidery/tools/",
            "subcategory": "needlework-fiber-arts/cross-stitch-embroidery/tools",
        },
        "yarn-winders-machines": {
            "url": "https://www.michaels.com/shop/yarn-needlework/knitting-crochet/yarn-winders-machines/",
            "subcategory": "knitting-crochet/yarn-winders-machines",
        },
    },
}


def category_index(categories: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """``category`` slug -> inventory entry, for ``-a category=<slug>`` lookup."""
    return {entry["category"]: entry for entry in categories}


def resolve_category(
    categories: list[dict[str, str]],
    *,
    category: str | None = None,
    category_url: str | None = None,
    url: str | None = None,
) -> dict[str, str] | None:
    """Resolve the CLI args to one inventory entry, or ``None`` when unscoped.

    Resolution order is url > category_url > category, matching
    :meth:`BaseListingSpider.resolve_target_url`. A URL is matched on its
    normalized ``/shop/`` path so a trailing slash, an absolute URL and a bare
    path all hit the same entry.
    """
    if category:
        index = category_index(categories)
        entry = index.get(category)
        if entry is not None:
            return entry
        # Fall back to a URL-shaped category arg so `-a category=/shop/...` works.
        if "/" in category:
            return resolve_category(
                categories, category_url=category
            )
        return None

    target = category_url or url
    if not target:
        return None
    wanted = category_path_parts(target)
    if not wanted:
        return None
    for entry in categories:
        if category_path_parts(entry["url"]) == wanted:
            return entry
    return None


def available_categories(categories: list[dict[str, str]], limit: int = 10) -> list[Any]:
    """A short, deterministic sample of category slugs for error messages."""
    return [entry["category"] for entry in categories[:limit]]