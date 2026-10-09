# Add `toolstation_listing` spider — Toolstation (UK), top 20 categories, Nuxt 3 SSR product grid + `?page=N` pagination

## Goal

Add a `toolstation_listing` spider for **Toolstation** (`https://www.toolstation.com`), one of the UK's largest trade/DIY retailers (Travis Perkins group; nationwide branch network, tens of millions of monthly visits). Toolstation is **not represented** under `common/spiders/` and there is **no Toolstation issue** in this repository (verified: no `toolstation*` file anywhere under the tree, no `toolstation` reference, and no matching issue).

Follow the conventions of the existing listing spiders and subclass `BaseListingSpider` (list category URLs, yield listing items per category, use the shared ScrapeOps proxy + retry/parse helpers).

## Target site

- **Site:** `https://www.toolstation.com`
- **Platform:** **Nuxt 3** (Vue) SSR. The hydration blob `window.__NUXT__` exists but contains **only runtime config** (`{public:{apiBaseUrl, region:"uk", domain, currency:"GBP", ...}}`) — **no product data**. **Products for page 1 are server-rendered directly into plain HTML** (`data-testid="product-card"`), so no JS execution, no XHR replay and no hydration parsing is required to read a listing page.
- **Proxy:** ScrapeOps, plain datacenter endpoint (`country=us`) — returned `200` for the home page and all category pages. **No bot-challenge observed.** Pages are ~300–660 KB and arrive populated. (TLS verification must be disabled for the ScrapeOps MITM tunnel, as with the other spiders.)
- **Robots:** `robots.txt` allows the category tree for `User-agent: *`; it only disallows `/trolley`, `/checkout`, `/auth/silent-login`, `/search?*`, `/products?*`, `/campaign/` and unparameterised facet URLs. Category PLPs and `?page=N` are **allowed**.
- **Traffic:** large evergreen trade catalogue across tools, power tools, screws & fixings, plumbing, electrical, heating, bathrooms & kitchens, construction, ironmongery, workwear & safety, landscaping, adhesives/sealants, automotive, cleaning.

## 1. Categories dict

Category inventory was harvested from the **`departments.xml` sitemap** (`https://www.toolstation.com/sitemap/departments.xml`) — the authoritative, complete category tree — yielding **1,013 `/.../c<id>` category URLs** (the homepage mega-menu exposes the same tree, 313 of them, as a subset).

Each of the **1,013** category URLs was then fetched through the ScrapeOps proxy and the **`(N products)`** result-count header parsed to rank them. **908** pages carried a count; the other 105 are non-listing hub/landing pages (no product marker).

**Top 20 real product-listing categories**, ranked by measured product count (excludes the promotional `deals/*` and `sale-clearance/*` collections, whose largest member `deals/offers/c1460` measured 2,428):

| # | Category | Products | URL |
|---|----------|---------:|-----|
| 1 | Kitchen Cabinets | 1771 | https://www.toolstation.com/kitchens/kitchen-cabinets/c1468 |
| 2 | Flat Pack Kitchen Units | 1376 | https://www.toolstation.com/kitchens/flat-pack-kitchen-units/c1500 |
| 3 | Joinery | 1325 | https://www.toolstation.com/construction-insulation/joinery/c1478 |
| 4 | Shower Enclosures | 1000 | https://www.toolstation.com/bathrooms/shower-enclosures/c1089 |
| 5 | Cutting Blades | 859 | https://www.toolstation.com/power-tool-accessories/cutting-blades/c715 |
| 6 | Drill Bits | 853 | https://www.toolstation.com/power-tool-accessories/drill-bits/c713 |
| 7 | Switches & Sockets | 794 | https://www.toolstation.com/electrical-supplies-accessories/switches-sockets/c660 |
| 8 | Screws | 758 | https://www.toolstation.com/screws-fixings/screws/c728 |
| 9 | Boiler Spares | 680 | https://www.toolstation.com/central-heating-supplies/boiler-spares/c1562 |
| 10 | Cable Management | 621 | https://www.toolstation.com/electrical-supplies-accessories/cable-management/c207 |
| 11 | Workwear | 609 | https://www.toolstation.com/workwear-safety/workwear/c794 |
| 12 | Designer Radiators | 601 | https://www.toolstation.com/central-heating-supplies/designer-radiators/c769 |
| 13 | Doors | 520 | https://www.toolstation.com/construction-insulation/doors/c1463 |
| 14 | Outdoor Buildings | 518 | https://www.toolstation.com/landscaping/outdoor-buildings/c692 |
| 15 | Door Locks & Security | 509 | https://www.toolstation.com/ironmongery/door-locks-security/c680 |
| 16 | Safety Footwear | 496 | https://www.toolstation.com/workwear-safety/safety-footwear/c737 |
| 17 | Door Handles & Knobs | 494 | https://www.toolstation.com/ironmongery/door-handles-knobs/c678 |
| 18 | Sheds | 488 | https://www.toolstation.com/landscaping/sheds/c781 |
| 19 | Bathroom Fittings | 475 | https://www.toolstation.com/bathrooms/bathroom-fittings/c1090 |
| 20 | Push Fit Fittings | 474 | https://www.toolstation.com/plumbing/push-fit-fittings/c968 |

The **full 1,013-entry `url -> {name, id, path, products}` dict** is attached as `sample/toolstation_category_dict.json`; the ranked top 20 as `sample/toolstation_top20_categories.json`.

## 2. Product-listing investigation — first category (`Kitchen Cabinets`)

Fetched: `GET https://www.toolstation.com/kitchens/kitchen-cabinets/c1468` → `200` (~656 KB HTML). It contains a full product listing (`1,771 products`).

**How products are loaded — server-rendered HTML (Nuxt 3 SSR).** Verified against the three candidate mechanisms:

- **Not XHR/AJAX:** the 48 product cards are present in the initial response with no client fetch needed.
- **Not `__NEXT_DATA__`/`__NUXT__` hydration:** `window.__NUXT__` is present but is **config-only** (4 KB) and does **not** contain the product `id` (checked: `66358` absent) nor a `products` array. Products are **not** in state hydration.
- **Not JSON-LD `ItemList`:** the only `application/ld+json` block is a `BreadcrumbList`; there is no `ItemList`.

The server renders the grid as plain Vue SSR markup:

```html
<div class="... products--grid__card" data-testid="product-card" data-v-a17035f1>
  <a href="/curved-bath-screen/p66358" data-testid="product-card-image-link"> … </a>
  <a href="/curved-bath-screen/p66358#reviews" data-testid="product-card-reviews"
     data-product-id="66358" title="Highlife / Curved Bath Screen"> ( 254 ) </a>
  <p class="text-size-2 mb-1 text-blue">Product code: 66358</p>
  <a href="/curved-bath-screen/p66358"><p class="font-semibold text-blue …">Curve…</p></a>
  … price / add-to-trolley (data-testid="add-to-trolley-delivery-button") …
</div>
```

**Useful stable hooks** (Tailwind classes are not stable; prefer these):

- Product card: `data-testid="product-card"` (48 per page).
- Product image link / name link: `data-testid="product-card-image-link"`, `data-testid="plp-product-main-image"`.
- Product URL: `href="<slug>/p<id>"` (e.g. `/curved-bath-screen/p66358`); numeric id also in `data-product-id` on the reviews link, and the visible **`Product code: <id>`** line.
- Reviews count: `data-testid="product-card-reviews"` → `( 254 )`.
- Stock / purchase buttons: `data-testid="add-to-trolley-delivery-button"` and `add-to-trolley-collection-button` (presence ⇒ purchasable online / collectable).
- Result count header: the literal text `(<N> products)` in the grid header.
- Brand: a brand `<img alt="<Brand>">` at the top of each card.

- **Pagination:** **query-string based** — `https://www.toolstation.com/kitchens/kitchen-cabinets/c1468?page=2` … up to `?page=37` (1771 / 48 ≈ 37). Links are rendered as `data-testid="show-page-number"` and `data-testid="show-next-link"`. `?page=2` was confirmed to return a **different** 48-product page (HTTP 200). This differs from Argos-style `/opt/page:N/`; use `?page=N`.

## 3. Attached evidence (repo)

- `sample/toolstation_category_dict.json` — full **1,013-entry** dict from the `departments.xml` sitemap: `url -> {name, id, path, products}`.
- `sample/toolstation_top20_categories.json` — ranked top 20 (`name`, `url`, `id`, `products`, `department`, `path`).
- `sample/toolstation-kitchen-cabinets-listing-sample.html` — trimmed real listing HTML for the first category: `<head>` excerpt, `(1,771 products)` header, one server-rendered `product-card`, the `?page=N` pagination control, and the `window.__NUXT__` tail (showing it is config-only).
- `sample/toolstation-product-card-sample.html` — the server-rendered product-card markup slice with `/<slug>/p<id>` links.

## 4. Suggested implementation

- `class ToolstationListingSpider(BaseListingSpider)` with `name = "toolstation_listing"`.
- Start URLs from the top-20 `CATEGORIES` map (allow a `category` spider argument to run one PLP).
- Parse the rendered HTML grid: select `[data-testid="product-card"]`; for each card read the name/URL link (`[data-testid="product-card-image-link"]` / `href^="/"` ending `/p<id>`), extract `id` from the id link or the `Product code: <id>` text, brand from the brand `img[alt]`, price from the card price node, reviews from `[data-testid="product-card-reviews"]`, and stock flags from the `add-to-trolley-*` buttons.
- Read the total from the `(<N> products)` header; paginate `?page=2..ceil(N/48)` (48 items/page) via `data-testid="show-next-link"`, capping at the parsed total.
- Emit the standard item fields: `item_id` (`p<id>`), `title`, `url` (`https://www.toolstation.com<path>`), `brand`, `price`, `currency` (`GBP`), `rating`, `reviews`, `in_stock`, `image` (`cdn.toolstation.com` / `cdn.aws.toolstation.com`), `category`.
- Use the shared ScrapeOps proxy settings and existing retry/parse helpers (TLS verify off for the proxy tunnel).
- Add `tests/test_toolstation_listing_spider.py` covering product-card extraction, `p<id>` derivation, price parsing, and `?page=N` pagination derivation.
