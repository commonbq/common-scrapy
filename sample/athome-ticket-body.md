# Add `athome_listing` spider — At Home (US home décor & furniture superstore), top 20 categories, Salesforce Commerce Cloud (SFRA) server-rendered product grid + `Search-UpdateGrid` AJAX pagination

## Goal

Add an `athome_listing` spider for **At Home** (`https://www.athome.com`), a high-traffic US home-furnishings and décor retailer (228 open US stores; furniture, rugs, lighting, wall art, kitchen & dining, bed & bath, outdoor, seasonal). At Home is **not represented** under `common/spiders/` and there is **no At Home issue** in this repository (verified: no `athome*` file anywhere under the tree and no matching issue).

Follow the conventions of the existing listing spiders and subclass `BaseListingSpider` (list category URLs, yield listing items per category, use the shared ScrapeOps proxy + retry/parse helpers).

## Target site

- **Site:** `https://www.athome.com`
- **Platform:** **Salesforce Commerce Cloud / Demandware (SFRA Storefront Reference Architecture)**. Evidence: `…/on/demandware.store/Sites-athome-sfra-Site/default/…` controller URLs, `demandware.static` asset host, `Search-UpdateGrid` grid controller.
- **How products load:** the category **product grid is server-rendered into the initial HTML response** (`<div class="product-tile">` cards, no JS required). **Additional pages load via an AJAX XHR** to the SFRA grid controller `Search-UpdateGrid` which returns an **HTML fragment** (not JSON). There is **no `__NEXT_DATA__`/`__NUXT__` state-hydration blob** and no client-side JSON API needed.
- **Proxy:** ScrapeOps, plain datacenter endpoint (`country=us`). Home page, sitemaps and every category page/market-fragment fetched returned `200`. **No bot challenge observed.** (TLS verification must be disabled for the ScrapeOps MITM tunnel, as with the other spiders.)
- **robots.txt:** `User-agent: *` disallows `/*Size=*`, refinement params (`prefn*/prefv*`), `/*srule=*`, `*/search/*`, cart/checkout/account paths and various promo/utility paths; it `Allow`s `/llms.txt`. The **`/<category>/` PLPs used here are allowed**.
- **Traffic:** evergreen US home/décor/seasonal catalogue; department-level CLPs link to hundreds of leaf product-listing categories, with individual leaf categories carrying up to ~3,500 products.

## 1. Categories dict

Category inventory was harvested two ways and cross-checked:

1. the **homepage mega-nav** (`?nav=top_nav` anchors) — **459** category/navigation URLs; and
2. the SFRA **sitemap** (`https://www.athome.com/sitemap_1.xml`, ~1,285 URLs including editorial content) plus `sitemap-refinements-1.xml` (colour/style refinements, excluded).

The full **459-entry name → URL category dict** is attached as `sample/athome_category_dict.json`.

**Note on taxonomy depth:** SFRA department pages (e.g. `/furniture/`, `/rugs/`, `/home-decor/`, `/kitchen-dining/`, `/bed-bath/`, `/outdoor-furniture-decor/`, `/lighting/`, `/storage-organization/`, `/wall-decor/`) are **Category Landing Pages (CLPs)** — they render category/sub-category tiles, not a product grid (`"productCount":0`, zero `.product-tile`). The **product-listing categories are the leaf categories**, which expose a server-rendered grid and a `data-product-count` attribute.

**Top 20 product-listing categories**, ranked by measured product count (`data-product-count` on each PLP):

| # | Category | Products | URL |
|---|----------|---------:|-----|
| 1 | Christmas | 3475 | https://www.athome.com/christmas/ |
| 2 | Gift Ideas | 1931 | https://www.athome.com/gift-ideas/ |
| 3 | Artificial Flowers & Greenery | 1198 | https://www.athome.com/artificial-flowers-greenery/ |
| 4 | Outdoor Décor | 948 | https://www.athome.com/outdoor-decor/ |
| 5 | Halloween | 789 | https://www.athome.com/halloween/ |
| 6 | Vases | 736 | https://www.athome.com/vases/ |
| 7 | Area Rugs | 686 | https://www.athome.com/area-rugs/ |
| 8 | Outdoor Pots & Planters | 655 | https://www.athome.com/outdoor-pots-planters/ |
| 9 | Framed Art | 622 | https://www.athome.com/framed-art/ |
| 10 | Storage Baskets | 566 | https://www.athome.com/storage-baskets/ |
| 11 | Kitchen Storage | 544 | https://www.athome.com/kitchen-storage/ |
| 12 | Drinkware | 540 | https://www.athome.com/drinkware-glassware/ |
| 13 | Throw Pillows | 477 | https://www.athome.com/toss-pillows/ |
| 14 | Canvas Art | 460 | https://www.athome.com/canvas-art/ |
| 15 | Lamps | 326 | https://www.athome.com/lamps/ |
| 16 | Sculptures & Figurines | 322 | https://www.athome.com/sculptures-figurines/ |
| 17 | Bath Towels & Washcloths | 314 | https://www.athome.com/bath-towels-washcloths/ |
| 18 | Bed Sheets & Pillowcases | 272 | https://www.athome.com/bed-sheets-pillowcases/ |
| 19 | Bathroom Rugs & Bath Mats | 233 | https://www.athome.com/bathroom-rugs-mats/ |
| 20 | Scented Candles | 225 | https://www.athome.com/scented-candles/ |

(Seasonal collections rank at the top in October; they are first-class categories with real product grids. The ranked top 20 is attached as `sample/athome_top20_categories.json`.)

## 2. Product-listing investigation — first category (`/christmas/`)

Fetched: `GET https://www.athome.com/christmas/` → `200` (~0.6 MB HTML). It contains a full product listing (`data-product-count="3475"`, 24 server-rendered `.product-tile` cards on page 1).

**How products are loaded — server-rendered HTML (SFRA) + AJAX HTML-fragment pagination.** Verified against the candidate mechanisms:

- **Not `__NEXT_DATA__`/`__NUXT__`/`window.__*` hydration:** no such state blob exists; the SFRA page is plain SSR HTML.
- **Products ARE in the initial response.** The grid is emitted server-side as `<div class="product-tile">` cards (each wraps a `.product-image` link, title, rating and `.product-pricing`).
- **Pagination is an AJAX XHR returning an HTML fragment.** The SFRA grid controller is used:

  ```
  GET https://www.athome.com/on/demandware.store/Sites-athome-sfra-Site/default/Search-UpdateGrid
        ?cgid=christmas&start=<offset>&sz=<pageSize>
  ```

  Confirmed: `start=0&sz=24` and `start=24&sz=24` each returned `200` with a `text/html` fragment containing **24 different `<div class="product-tile">` cards** (different `data-pid`s). The page-1 category HTML references the same controller with `start=12&sz=12`. Paginate `start = 0, pageSize, 2*pageSize, …` up to `data-product-count`, where **`cgid` = the category URL slug** (e.g. `/area-rugs/` → `cgid=area-rugs`).

- **Not JSON-LD `ItemList`:** the PLP emits `BreadcrumbList`/`CollectionPage` JSON-LD only; products are not in `application/ld+json`.

**Product card markup (server-rendered; identical in the PLP and in the `Search-UpdateGrid` fragment):**

```html
<div class="product-tile">
  <div class="QVWishlistwrapper">
    <button class="update-wishlist-product btn ghost sm icon-only on-plp-page touchable"
            aria-label="Add to Wishlist" role="switch" aria-checked="false" aria-pressed="false">…</button>
  </div>
  <a href="/b500-xander-ivory-tan-area-rug-5x7/124225653.html" class="product-image"
     aria-label="(B500) Xander Ivory &amp; Tan Area Rug, 5x7, 4.8 out of 5 stars, ">
    <div class="image-container">
      <img src="https://static.athome.com/images/w_200,h_200,c_pad,f_auto,fl_lossy,q_auto/p/124225653/b500-xander-ivory-tan-area-rug-5x7.jpg"
           srcset="… 2x" loading="lazy" class="tile-image" alt="(B500) Xander Ivory &amp; Tan Area Rug, 5x7" />
    </div>
  </a>
  <div class="tile-body">
    <div class="badge-container badge-list"></div>
    <a href="/b500-xander-ivory-tan-area-rug-5x7/124225653.html#reviews-info" title="…">
      <div class="rating" style="--star-rating: 4.8;" aria-label="4.8 out of 5 stars">
        <span class="rating-stars"><span class="rating-stars-active"></span></span>
        <span class="rating-number">4.8</span><span class="rating-count">(85)</span>
      </div>
    </a>
    <a href="/b500-xander-ivory-tan-area-rug-5x7/124225653.html"
       class="pt-desc-link product-image product-id-124225653" aria-label="…">
      <h3 class="pdp-link pt-name">(B500) Xander Ivory &amp; Tan Area Rug, 5x7</h3>
    </a>
    <a href="/b500-xander-ivory-tan-area-rug-5x7/124225653.html"
       class="pt-desc-link product-image product-id-124225653">
      <div class="more-options-container"><span class="product-moreoptions">More sizes available</span></div>
      <div class="product-pricing is-PLP" data-price-type="regular">
        <div class="Pricing" data-isclearance="false" data-cache-timestamp="2026-10-08 22:00:12 GMT">
          <div class="fancy price"><span>$</span><span>99</span><sub>.</sub><sup>99</sup></div>
        </div>
      </div>
    </a>
  </div>
</div>
```

**Useful stable hooks:**

- Product card root: `div.product-tile` (grid wrapper: `.js-producttiles`).
- Product URL + id: `a.product-image[href]` / `a.pt-desc-link.product-id-<pid>` → `/<slug>/<pid>.html`; product id also on `data-pid="<pid>"` and `data-master-pid="M<masterPid>"` (variant/master grouping).
- Title: `h3.pdp-link.pt-name`.
- Price: `.product-pricing .fancy.price` (digits split across `span/sub/sup`; `data-isclearance` flags clearance).
- Rating: `div.rating` (`aria-label="<x> out of 5 stars"`, `.rating-number`, `.rating-count`).
- Image: `img.tile-image[src]` (At Home Cloudinary-style `static.athome.com/images/…`).
- Product count: `[data-product-count="<N>"]` on the PLP.
- Pagination: `Search-UpdateGrid?cgid=<slug>&start=<offset>&sz=<pageSize>` (HTML fragment of `.product-tile`).

## 3. Attached evidence (repo)

- `sample/athome_category_dict.json` — full **459-entry** name → URL category dict (slug-keyed) from the homepage nav.
- `sample/athome_top20_categories.json` — ranked top 20 (`rank`, `name`, `url`, `products`).
- `sample/athome-christmas-listing-sample.html` — trimmed real listing HTML for the first category (`/christmas/`): `<head>` excerpt, `data-product-count="3475"`, one server-rendered product card.
- `sample/athome-search-updategrid-xhr-sample.html` — real `Search-UpdateGrid` XHR response fragment (one `.product-tile`), showing pagination returns an HTML fragment, not a full page/JSON.
- `sample/athome-product-card-sample.html` — the isolated `.product-tile` markup slice with link, title, rating and price hooks.

## 4. Suggested implementation

- `class AthomeListingSpider(BaseListingSpider)` with `name = "athome_listing"`.
- Start URLs from the top-20 `CATEGORIES` map (allow a `category` spider argument to run one category).
- Extraction: parse the PLP's server-rendered `div.product-tile` cards for page 1; for subsequent pages call the SFRA grid controller `…/Search-UpdateGrid?cgid=<slug>&start=<offset>&sz=<pageSize>` and parse the same `.product-tile` fragment — loop `start += pageSize` until `start >= data-product-count` (read the count once from the PLP).
- Use the shared ScrapeOps proxy (TLS verification disabled) and the existing retry/parse helpers; `cgid` is the URL slug (strip leading slash).
