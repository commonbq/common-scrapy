# Add `gymshark_listing` spider — Gymshark (UK/global DTC apparel), top 20 collections, Next.js SSR product cards + Algolia `ssrQuery` hydration and `?page=N` pagination

## Goal

Add a `gymshark_listing` spider for **Gymshark** (`https://www.gymshark.com`), one of the UK's largest direct-to-consumer fitness-apparel brands (global shipping, tens of millions of monthly visits). Gymshark is **not represented** under `common/spiders/` and there is **no Gymshark issue** in this repository (verified: no `gymshark*` file anywhere under the tree and no matching issue).

Follow the conventions of the existing listing spiders and subclass `BaseListingSpider` (list category URLs, yield listing items per category, use the shared ScrapeOps proxy + retry/parse helpers).

## Target site

- **Site:** `https://www.gymshark.com`
- **Platform:** **Next.js** (headless Shopify storefront, `__NEXT_DATA__` present) with an **Algolia**-backed product search. Products for page 1 are **server-rendered into plain HTML** (`article[role="listitem"]`, `data-testid="plp-productCard-<id>-select"`), **and** the same page exposes the structured product list in the Next.js hydration blob at `props.pageProps.ssrQuery` (`hits[]`, `nbHits`, `nbPages`, `page`, `hitsPerPage`). **No JS execution is required** to read a listing page: parse either the SSR HTML grid or the `ssrQuery.hits` JSON.
- **Proxy:** ScrapeOps, plain datacenter endpoint (`country=us`) — returned `200` for the home page, the collection sitemap and every collection page fetched (1,018/1,018 with no failures). **No bot challenge observed.** Collection pages are large (~1.9–2.1 MB uncompressed) and arrive populated. (TLS verification must be disabled for the ScrapeOps MITM tunnel, as with the other spiders.)
- **robots.txt:** standard `User-agent: *`; disallows `/cart`, `/checkout`, `/account*`, `/search*` and the `/api/*` write paths. The `/collections/*` PLPs used here are **allowed**.
- **Traffic:** evergreen global apparel catalogue; the master `all-products` collection alone returns **2,471** products and the brand runs frequent collections across men's/women's apparel, `t-shirts-tops`, `bottoms`, `shorts`, `hoodies-jackets`, `sports-bras`, `leggings`, `tracksuits`, accessories, etc.

## 1. Categories dict

Category inventory was harvested from the **Shopify collections sitemap** (`https://www.gymshark.com/sitemap_collections_1.xml`) — the authoritative, complete collection tree — yielding **1,018 `/collections/...` URLs**.

Each of the **1,018** collection URLs was then fetched through the ScrapeOps proxy and the product count parsed from the Next.js hydration (`props.pageProps.ssrQuery.nbHits`, cross-checked against the rendered `Viewing 1 - 60 of <N> products` text). **635** collections carried a non-zero count; **383** are empty/placeholder (marketing, discount-code, navigation-only) collections and were dropped.

**Top 20 real product-listing collections**, ranked by measured product count (promotional/discount-code collections — `sale*`, `outlet*`, `cyber*`, `*-off`, `winback-codes`, `20extra`, `build-your-wishlist`, `klarna-*`, etc. — are excluded from the ranking):

| # | Category | Products | URL |
|---|----------|---------:|-----|
| 1 | All Products | 2472 | https://www.gymshark.com/collections/all-products |
| 2 | Steven Kelly | 2472 | https://www.gymshark.com/collections/steven-kelly |
| 3 | All Products (Women) | 1528 | https://www.gymshark.com/collections/all-products/womens |
| 4 | Conditioning | 1218 | https://www.gymshark.com/collections/conditioning |
| 5 | All Products (Men) | 1123 | https://www.gymshark.com/collections/all-products/mens |
| 6 | Steven Kelly (Men) | 1123 | https://www.gymshark.com/collections/steven-kelly/mens |
| 7 | Matching Sets | 1118 | https://www.gymshark.com/collections/matching-sets |
| 8 | Matching Sets (Women) | 1004 | https://www.gymshark.com/collections/matching-sets/womens |
| 9 | T-Shirts & Tops | 825 | https://www.gymshark.com/collections/t-shirts-tops |
| 10 | All Tops | 825 | https://www.gymshark.com/collections/all-tops |
| 11 | Conditioning (Women) | 789 | https://www.gymshark.com/collections/conditioning/womens |
| 12 | Running | 712 | https://www.gymshark.com/collections/running |
| 13 | Airport Outfits | 666 | https://www.gymshark.com/collections/airport-outfits |
| 14 | Travel Outfits | 666 | https://www.gymshark.com/collections/travel-outfits |
| 15 | Black Staples | 652 | https://www.gymshark.com/collections/black-staples |
| 16 | Slounge | 573 | https://www.gymshark.com/collections/slounge |
| 17 | Power Down | 573 | https://www.gymshark.com/collections/power-down |
| 18 | Reset | 573 | https://www.gymshark.com/collections/reset |
| 19 | Rest Day | 573 | https://www.gymshark.com/collections/rest-day |
| 20 | Functional Fitness | 570 | https://www.gymshark.com/collections/functional-fitness |

The **full 1,018-entry `url -> {name, handle, path, gender, products}` dict** is attached as `sample/gymshark_category_dict.json`; the ranked top 20 as `sample/gymshark_top20_categories.json`.

## 2. Product-listing investigation — first category (`All Products`)

Fetched: `GET https://www.gymshark.com/collections/all-products` → `200` (~1.87 MB HTML). It contains a full product listing (`2,471 products`).

**How products are loaded — server-rendered HTML + Next.js SSR hydration (`__NEXT_DATA__`).** Verified against the candidate mechanisms:

- **Not a standalone AJAX call on first paint:** the 60 product cards are present in the initial response with no client fetch needed.
- **Next.js `__NEXT_DATA__` hydration IS present and carries the grid data.** `props.pageProps.ssrQuery` is an Algolia-style response containing `hits` (60 items, each with `handle`, `title`, `price`, `compareAtPrice`, `colour`, `gender`, `inStock`, `discountPercentage`, `featuredMedia`, `rating`, `labels`, …), plus `nbHits` (**2,471**), `nbPages` (17 — capped, see pagination note), `hitsPerPage` (60) and `page` (0). Products can be read straight from `ssrQuery.hits` — no JS execution needed.
- **The grid is also server-rendered as plain HTML.** The same 60 products appear as `article[role="listitem"]` cards inside `div[data-product-grid="true"]`; the human-readable count is rendered as `Viewing 1 - 60 of 2471 products`.
- **Not JSON-LD `ItemList`:** there is no `application/ld+json` `ItemList` on the page (only Shopify/Organization meta).

**Product card markup (SSR HTML):**

```html
<article class="product-card_product-card__1T7k9"
         data-testid="plp-productCard-6806409347274-select" aria-label="product" role="listitem">
  <div class="product-card_card-wrapper__eXXBl" role="group">
    <a title="Power T-Shirt" aria-label="Power T-Shirt"
       href="https://www.gymshark.com/products/gymshark-power-t-shirt-ss-tops-black-aw25-3">
      <img alt="Power T-Shirt" data-product-image-index="1" data-nimg="fill"
           srcSet="https://cdn.shopify.com/s/files/1/0156/6146/files/…-32x.jpg?v=1762443934 32w, … ">
    </a>
    <h4 class="product-card_product-title__CVoTa"
        data-testid="plp-productTitle-6806927933642-read">Power T-Shirt</h4>
    <span class="product-price_product-price__K0usY"
          data-testid="plp-totalValue-6806927933642-read">
      <span class="sr-only">Regular Price: </span>$36</span>
  </div>
</article>
```

**Useful stable hooks** (hashed CSS-Module class suffixes are not stable; prefer the `data-testid` attributes):

- Product card: `article[role="listitem"]` with `data-testid="plp-productCard-<productId>-select"`; all cards live in `div[data-product-grid="true"]`.
- Product URL: `a[href^="https://www.gymshark.com/products/"]` → `/products/<handle>`; product id = `plp-productCard-<id>-select`.
- Title: `[data-testid^="plp-productTitle-"]`.
- Price: `[data-testid^="plp-totalValue-"]` (currency `$`/USD; `sb-only` "Regular Price:" prefix).
- Colour: `[data-testid^="plp-productColour-"]`.
- Ratings: `[data-testid="star-rating"]` (52/60 cards rated).
- Badges: `[data-testid^="plp-productTag-"]` (`-promotion-`, `-new-`).
- Result-count header: the literal text `Viewing 1 - 60 of <N> products` (`[data-testid="plp-paginationText-read"]`).
- Structured alternative (recommended): `__NEXT_DATA__.props.pageProps.ssrQuery.hits[]` + `.nbHits` / `.nbPages` / `.hitsPerPage`.

- **Pagination:** **query-string based** — `…/collections/<handle>?page=N`, 60 items per page, where the window is `offset = N * 60` (default = page 0 → `1 - 60`). Confirmed against the master collection:
  - `?page=1` → `Viewing 60 - 120 of 1123 products` (different 60 products, HTTP 200)
  - `?page=2` → `Viewing 120 - 180 of 1123 products`
  - `?page=3` → `Viewing 180 - 240 of 1123 products`
  Paginate `page = 1 .. ceil(nbHits/60)-1`. Note: `ssrQuery.nbPages` is present but appears capped (reported `17` for both 1,123- and 2,471-product collections while `hitsPerPage` is 60), so **derive the last page from `nbHits`**, not from `nbPages`.

## 3. Attached evidence (repo)

- `sample/gymshark_category_dict.json` — full **1,018-entry** dict from the collections sitemap: `url -> {name, handle, path, gender, products}`.
- `sample/gymshark_top20_categories.json` — ranked top 20 (`rank`, `name`, `url`, `handle`, `path`, `gender`, `products`).
- `sample/gymshark-listing-sample.html` — trimmed real listing HTML for the first category (`/collections/all-products`): `<head>` excerpt, one server-rendered product card, the `Load more`/pagination control, and the `__NEXT_DATA__` head + `ssrQuery.nbHits`.
- `sample/gymshark-product-card-sample.html` — the server-rendered product-card markup slice with the `/products/<handle>` link, price and title testids.

## 4. Suggested implementation

- `class GymsharkListingSpider(BaseListingSpider)` with `name = "gymshark_listing"`.
- Start URLs from the top-20 `CATEGORIES` map (allow a `category` spider argument to run one collection).
- Preferred extraction: parse `__NEXT_DATA__` (`json.loads` of `#__NEXT_DATA__`) → `props.pageProps.ssrQuery.hits` for structured fields; fall back to the SSR HTML grid (`article[role="listitem"]`) for robustness.
- Read the total from `ssrQuery.nbHits` (fallback: parse `Viewing 1 - 60 of <N> products`); paginate `?page=1..ceil(N/60)-1` (60 items/page) using the shared retry helper.
- Emit the standard item fields: `item_id` (product id from `plp-productCard-<id>-select` / `hits[].id`), `title`, `url` (`https://www.gymshark.com/products/<handle>`), `brand` (constant `Gymshark`), `price`, `compare_at_price`, `currency` (`USD`), `colour`, `gender`, `rating`, `labels`/badges, `in_stock`, `image` (`cdn.shopify.com` / `featuredMedia`), `category`.
- Use the shared ScrapeOps proxy settings and existing retry/parse helpers (TLS verify off for the proxy tunnel).
- Add `tests/test_gymshark_listing_spider.py` covering `__NEXT_DATA__`/`ssrQuery.hits` extraction, `plp-productCard-<id>` parsing, price parsing, and `?page=N` pagination derivation (offset = N*60).
