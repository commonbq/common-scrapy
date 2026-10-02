
### williams_sonoma_listing

| Status | Data | Proxy | Anti-bot | Items | Categories | Sample Item (truncated) |
|---|---|---|---|---|---|---|
| Active | api | none detected (ScrapeOps proxy) | Akamai (not an issue for API) | 100 (1 page, proxy) | ~3500 (`williams_sonoma_categories.py` runtime API) | `{"category":"cookware-sets","item_id":"greenpan-reserve-pro-ceramic-nonstick-10-piece-cookware-set","title":"GreenPan™ Reserve Pro Ceramic Nonstick 10-Piece Cookware Set","price":399.95,"currency":"USD","image_url":"https://assets.wsimgs.com/wsimgs/rk/images/dp/wcm/202631/0164/img2c.jpg","flags":["freeShip","more_colors"],"raw":{"id":"greenpan-reserve-pro-ceramic-nonstick-10-piece-cookware-set", ...}}` |

This spider extracts product listings from the Williams-Sonoma (US) storefront
(`williams-sonoma.com`) via its Constructor.io browse API. The category taxonomy
is pulled from a first-party JSON API (`/api/catalog/v1/category/categorytree/...`)
on every run, so category changes on the site are reflected immediately without
spider updates. Product data itself is sourced from the Constructor.io
`/browse/group_id/{group_id}` endpoint.

No HTML parsing or rendered browser is used: the category pages are JavaScript
shells that load products dynamically. The spider reads the
Constructor.io API key from `window.__INITIAL_STATE__` on a sample category
page once per run and then uses it to query the browse endpoint directly.

- **Accepts categories by name, URL, or `--all-categories`**:
  - `common-scrapy crawl williams_sonoma_listing -a category=cookware-sets -a max_pages=1 -O ws.jsonl`
  - `common-scrapy crawl williams_sonoma_listing -a category_url='https://www.williams-sonoma.com/shop/cookware/cookware-sets/' -a max_pages=1 -O ws.jsonl`
  - `common-scrapy crawl williams_sonoma_listing -a all_categories=true -a max_pages=1 -O ws-full.jsonl`
- **Fixture tests** are run against `sample/williams-sonoma-category-tree.json`,
  `sample/williams-sonoma-browse-items.json`, and
  `sample/williams-sonoma-context.html`. All fixtures are trimmed to remove
  secrets and keep file size small.
- **`FEED_EXPORT_FIELDS`**:
```json
[
  "category",
  "category_name",
  "parent_category",
  "item_id",
  "title",
  "url",
  "brand",
  "sku",
  "price",
  "regular_price",
  "price_min",
  "price_max",
  "regular_price_min",
  "regular_price_max",
  "sale_price_min",
  "sale_price_max",
  "discount_percent",
  "price_type",
  "currency",
  "image_url",
  "image_alt",
  "alt_images_count",
  "swatches_count",
  "flags",
  "pip_type",
  "quick_buy",
  "description",
  "short_description",
  "product_details",
  "group_ids",
  "page",
  "category_url",
  "source",
  "raw"
]
```