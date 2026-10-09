# Add `hsn_listing` spider — HSN (hsn.com, US shopping network), top 20 categories, server-rendered product grid + `?page=N&skip=&take=60&view=all` pagination

## Goal

Add an `hsn_listing` spider for **HSN** (`https://www.hsn.com`), the high-traffic US
televised/online shopping retailer (QVC Group). HSN carries fashion, beauty, jewelry,
home, kitchen, electronics, health, crafts and more. HSN is **not represented** under
`common/spiders/` and there is **no HSN issue** in this repository (verified: no
`hsn*` file anywhere under the tree and no matching issue).

Follow the conventions of the existing listing spiders and subclass
`BaseListingSpider` (list category URLs, yield listing items per category, use the
shared ScrapeOps proxy + retry/parse helpers).

## Target site

- **Site:** `https://www.hsn.com`
- **Platform:** classic **server-rendered** storefront (no Next.js/Nuxt). Evidence:
  the homepage and PLPs contain **no `__NEXT_DATA__`, `__NUXT__` or
  `window.__INITIAL_STATE__`** blob; the product grid is emitted directly into the
  HTML response. Analytics/merch tooling is **Constructor.io** (`data-cnstrc-*`
  attributes) plus Adobe suite (`BOOMR`, `akam/`) and `data-datalayer-udo` JSON.
- **How products load:** the category **product grid is server-rendered into the
  initial HTML** — `<li class="item product-item module violated">` cards with
  `itemscope itemtype="https://schema.org/Product"`, `data-product-id`, `data-product-url`,
  `<meta itemprop="sku">`, `class="product-name"` and price markup. **No JS execution is
  required.** Pagination is **URL query-string driven and server-rendered**:
  `?page=N&skip=<N*60>&take=60&view=all` (the PLP emits `rel="next"` and `?page=` links).
- **Per-card structured data:** every card embeds a URL-encoded JSON blob in
  `data-datalayer-udo="…"` with `product_id`, `product_sku`, `product_brand`,
  `product_name`, `product_sale_price`, `product_original_price`,
  `product_shipping_handling`, `categories` (full breadcrumb with ids),
  `product_primary_category_id/name`, `product_rating_average/count`, `product_item_flag`,
  `is_onair_today`. This is the cheapest, most reliable extraction path (parse the
  attribute, `html.unescape`, `json.loads`) and does not depend on CSS class churn.
- **Proxy:** ScrapeOps, plain datacenter endpoint (`country=us`). Homepage, robots.txt
  and every category page fetched returned `200`. **No bot challenge observed.** TLS
  verification must be disabled for the ScrapeOps MITM tunnel, as with the other spiders.
- **robots.txt:** `User-agent: *` disallows `/account`, `/profile`, `/checkout`, `/com`,
  `/cust`, `/myaccount`, `/search`, `/search-more-products`, **`/show-more-products/`**,
  `/smgen.aspx`, `/bonusbuy/PromotionProducts/` and two individual product URLs; it
  advertises `Sitemap: https://www.hsn.com/sitemap`. The **`/shop/…` PLPs and
  `?page=` pagination used here are allowed**; the disallowed `/show-more-products/`
  XHR must **not** be used (see below).
- **Traffic:** evergreen US shopping catalogue; 11 top-level departments plus hundreds of
  leaf category pages and brand pages.

## 1. Categories dict

Category inventory was harvested from the **homepage mega-menu + primary navigation**
(`<nav id="primary-navigation">`), then every `/shop/<slug>/<code>` anchor was
deduplicated into a **443-entry name → URL category dict** (departments, subcategories,
brand/shop pages and editorial collections), attached as
`sample/hsn_category_dict.json`.

**Top 20 categories** (11 top-level departments + 9 highest-value subcategories),
attached as `sample/hsn_top20_categories.json`:

| # | Category | Level | URL |
|---|----------|-------|-----|
| 1 | Fashion | L1 | https://www.hsn.com/shop/fashion/fa |
| 2 | Home | L1 | https://www.hsn.com/shop/home/ho |
| 3 | Electronics | L1 | https://www.hsn.com/shop/electronics/ec |
| 4 | Beauty | L1 | https://www.hsn.com/shop/beauty/bs |
| 5 | Jewelry | L1 | https://www.hsn.com/shop/jewelry/j |
| 6 | Kitchen & Food | L1 | https://www.hsn.com/shop/kitchen-and-food/qc |
| 7 | Health & Fitness | L1 | https://www.hsn.com/shop/health-and-fitness/hf |
| 8 | Crafts & Sewing | L1 | https://www.hsn.com/shop/crafts-and-sewing/ct |
| 9 | Shoes | L1 | https://www.hsn.com/shop/shoes/fa0045 |
| 10 | Men's | L1 | https://www.hsn.com/shop/mens/mn |
| 11 | Fan Shop | L1 | https://www.hsn.com/shop/fan-shop/sp |
| 12 | Dresses | L2 | https://www.hsn.com/shop/dresses/fa0283 |
| 13 | Women's Tops | L2 | https://www.hsn.com/shop/womens-tops/fa0053 |
| 14 | Women's Jeans | L2 | https://www.hsn.com/shop/womens-jeans/fa0173 |
| 15 | Intimates | L2 | https://www.hsn.com/shop/intimates/fa0031 |
| 16 | Handbags & Wallets | L2 | https://www.hsn.com/shop/handbags-and-wallets/fa0402 |
| 17 | Home Appliances | L2 | https://www.hsn.com/shop/home-appliances/ho0209 |
| 18 | Storage & Organization | L2 | https://www.hsn.com/shop/storage-and-organization/ho0299 |
| 19 | Vacuums & Floor Care | L2 | https://www.hsn.com/shop/vacuums-and-floor-care/ho0441 |
| 20 | Luggage & Travel | L2 | https://www.hsn.com/shop/luggage-and-travel/ho0235 |

`categories` should use `[{"category": name, "url": url}, …]` per `BaseListingSpider`.

## 2. Product-loading investigation (first category: Electronics `/shop/electronics/ec`)

Verified live through the ScrapeOps proxy:

- **Server-rendered grid.** `GET https://www.hsn.com/shop/electronics/ec` → `200`,
  `1,447,173` bytes, **60** `data-datalayer-udo` product blobs = **60 unique
  `product_id`s** across `.item.product-item` cards. No hydration blob.
- **SSR pagination works.** `GET …/shop/electronics/ec?page=2&skip=60&take=60&view=all`
  → `200`, another **60** products; only **12** ids overlap with page 1 (the 12 are
  pinned `Customer Pick` items) ⇒ ~48 net-new products per page, confirming true
  server-side pagination. The page-1 HTML advertises `?page=1..29` links
  (`…?page=29&skip=1680&take=49&view=all`) plus `<link rel="next">`.
- **Loading mechanism = SSR HTML + query-string pagination** — *not* AJAX XHR, *not*
  Next/Nuxt hydration. A `/show-more-products/` endpooint exists (robots-disallowed) and
  should be avoided; the `?page/N` link path is the supported, allowed crawl route.
- **Parsing recommendation:** prefer the `data-datalayer-udo` JSON per card
  (`html.unescape` → `json.loads`) for name/brand/prices/rating/category breadcrumb,
  and read `data-product-url` / `data-product-id` / `itemprop="sku"` from the card for
  the canonical product URL and ids.

## 3. Attachments (in `sample/`)

- `sample/hsn_category_dict.json` — full **443-entry** name → URL category dict.
- `sample/hsn_top20_categories.json` — the **top 20** categories above.
- `sample/hsn-electronics-listing-sample.html` — trimmed Electronics PLP capture
  (2 server-rendered `.item.product-item` cards incl. `data-datalayer-udo`
  + the server-rendered pagination block).
- `sample/hsn-electronics-products-sample.json` — first **5** decoded per-card product
  objects (from `data-datalayer-udo`), showing the available fields.

_(Full raw page-1 capture was 1.4 MB; only representative slices are committed.)_

## 4. Implementation notes

- Name: `hsn_listing`; `allowed_domains = ["hsn.com", "www.hsn.com"]`;
  `categories` from `common/spiders/hsn_categories.py` (generate the dict from
  `sample/hsn_category_dict.json`).
- Request each category at `…?take=60&view=all` and follow `?page=N` up to `max_pages`;
  stop when a page returns no `.item.product-item`.
- Yield item fields consistent with other listing spiders: `item_id` (product_id),
  `sku`, `title`, `brand`, `url`, `price`, `original_price`, `currency` (USD),
  `shipping_handling`, `rating`, `rating_count`, `primary_category_id`,
  `primary_category`, `category_path`, `item_flag`, `is_onair_today`, `image`,
  `category`, `page`, `position`, `source`, `raw`, `timestamp`.
- `CONCURRENT_REQUESTS_PER_DOMAIN = 1`, modest `DOWNLOAD_DELAY`; ScrapeOps datacenter
  proxy with TLS verification disabled.

## 5. Acceptance

- `scrapy crawl hsn_listing -a category="Electronics" -a max_pages=3` yields ≥120
  products with non-empty `item_id`, `title`, `price`, `url`.
- All 20 categories in the dict resolve to a PLP that returns `.item.product-item`
  cards on page 1.
