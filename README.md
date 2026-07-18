# Common Scrapy Retailer Spiders

Scrapy spiders for four supported retailers:

- `ulta_listing`
- `sephora_listing`
- `nordstrom_listing`
- `macys_listing`

> This repository is actively maintained by **OpenClaw AI Agents** (with human oversight).

## Installation

```bash
pip install common-scrapy
```

## CLI usage

`pip install common-scrapy` adds a `common-scrapy` console script so you can run the packaged spiders without cloning the repo.

### Proxy configuration

```bash
PROXY=http://user:pass@host:1234 common-scrapy crawl ulta_listing --category hair -a max_pages=1
```

All spiders honor `PROXY` via project-wide middleware.

### List available spiders

```bash
common-scrapy list
```

### Run a crawl

```bash
common-scrapy crawl <spider> [--category <category>] [additional Scrapy args]
```

`--category` is required for these listing spiders. If omitted, the CLI prints available categories for that spider.

Examples:

- `common-scrapy crawl ulta_listing --category hair -a max_pages=1 -O ulta.jsonl`
- `common-scrapy crawl sephora_listing --category makeup -a max_pages=1 -O sephora.jsonl`
- `common-scrapy crawl nordstrom_listing --category women -a max_pages=1 -O nordstrom.jsonl`
- `common-scrapy crawl macys_listing --category fragrance -a max_pages=1 -O macys.jsonl`

## Supported spiders

| Spider | Status | Method | Description | Categories |
|---|---|---|---|---|
| `ulta_listing` | Active | api + html | Ulta category listing spider with GraphQL default and HTML fallback. | `makeup`, `skin-care`, `hair`, `fragrance`, `body-care` |
| `sephora_listing` | Active | api | Sephora listing spider via catalog category API. | `makeup`, `skincare`, `gifts`, `fragrance` |
| `nordstrom_listing` | Experimental | bootstrap + html | Nordstrom listing spider using embedded hydration data. | `women`, `men`, `kids`, `beauty`, `home`, `designer`, `sale` |
| `macys_listing` | Active | api | Macy's listing spider via `/xapi/discover/v1/page`. | `fragrance`, `skin-care`, `makeup`, `hair-care` |

## Sample output

### ulta_listing

```json
{
  "item_id": "2565096",
  "sku_id": "2565096",
  "title": "3 sizes Hydrate Shampoo for Dry Hair $12.00 - $90.00 Add to bag",
  "url": "https://www.ulta.com/p/hydrate-shampoo-dry-hair-pimprod2017791?sku=2565096",
  "image_url": "https://media.ultainc.com/i/ulta/2565096?w=200&$ProductCardNeutralBGLight$&h=200&fmt=auto",
  "source": "ulta_direct_html"
}
```

Run examples:

- `common-scrapy crawl ulta_listing --category hair -a max_pages=1 -O ulta.jsonl`
- `common-scrapy crawl ulta_listing --category hair -a mode=html -a max_pages=1 -O ulta_html.jsonl`

### sephora_listing

```json
{
  "item_id": "P517483",
  "title": "Pocket Blush Buildable Hydrating Cream Blush",
  "url": "https://www.sephora.com/product/pocket-blush-P517483?skuId=2895845",
  "brand": "rhode",
  "rating": 4.0598,
  "reviews_count": 1153,
  "source": "sephora_catalog_api"
}
```

Run example:

`common-scrapy crawl sephora_listing --category makeup -a max_pages=1 -O sephora.jsonl`

### nordstrom_listing

```json
{
  "category": "women",
  "product_id": 3865966,
  "name": "Pure Luxe Underwire T-Shirt Bra",
  "brand": "Natori",
  "price": 29.6,
  "url": "https://www.nordstrom.com/s/natori-pure-luxe-underwire-t-shirt-bra/3865966",
  "image": "https://n.nordstrommedia.com/it/0777d4b6-d7ef-4809-84a5-36fe4da01aff.jpeg",
  "rating": 4.5,
  "reviews_count": 1715
}
```

Run example:

`common-scrapy crawl nordstrom_listing --category women -a max_pages=1 -O nordstrom.jsonl`

### macys_listing

```json
{
  "item_id": "25092672",
  "title": "Floral Stickers Laptop, 74 Pcs, Stickers for Water Bottles,",
  "brand": "Mr. Pen",
  "price": 6.99,
  "price_text": "$6.99",
  "url": "https://www.macys.com/shop/product/floral-stickers-laptop-74-pcs-stickers-for-water-bottles?ID=25092672",
  "image_url": "7/optimized/34925717_fpx.tif",
  "source": "macys_xapi_discover_v1_page"
}
```

Run example:

`common-scrapy crawl macys_listing --category fragrance -a max_pages=1 -O macys.jsonl`

## Repository layout

- `common/spiders/` - retailer spiders and shared spider helpers
- `common_scrapy/cli.py` - CLI entrypoint for listing and running supported spiders
- `dags/` - DAG wrappers for the supported listing spiders
