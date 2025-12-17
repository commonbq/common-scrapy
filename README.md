# Common Scrapy Templates

An open, well-maintained collection of Scrapy templates for harvesting structured product data from major retailers. Each template encodes the HTTP request, pagination strategy, and response extraction rules needed for a specific storefront so you can stay focused on downstream data processing.

## Project layout

- `common/spiders/common_spider.py` – single parameterized spider that loads retailer-specific templates and converts API responses into normalized items.
- `common/templates/` – JSON blueprints (for example, `kohls_products.json`) describing request payloads, pagination, and extraction rules.
- `common/settings/` – shared Scrapy configuration; reads environment variables via `.env`.
- `scrapy.cfg` – entry point for the `scrapy` CLI.

## Getting started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or: pipenv install
   ```
2. **Configure environment**
   - Copy `.env.example` to `.env` if available, then set retailer-specific credentials.
   - Optionally set `COMMON_SCRAPY_PROXY` to route traffic through your proxy provider.
3. **Choose a template**
   - Inspect `common/templates/*.json` for existing retailers.
   - Add new JSON files to capture headers, query parameters, pagination (`page` or `offset`), and `$extract` rules.

## Running a crawl

```bash
scrapy crawl common -a name=kohls_products -a template_name=kohls_products
```

Arguments:
- `name` – logical spider name shown in logs.
- `template_name` – JSON filename (without extension) in `common/templates/`.

The spider will issue the configured request, follow pagination, and yield structured records defined in the template’s `$extract` block.

## Adding new retailer templates

1. Capture a representative network request (e.g., via DevTools) and save it under `common/templates/<retailer>.json`.
2. Populate:
   - `request.url`, `method`, headers, and `queryDict` or body payload.
   - `request.pagination` describing how to advance (`page` vs `offset`).
   - `response.$extract` with `$list` pointing to the iterable path and `$include` entries describing any per-item fields to hydrate.
3. Run the spider with `scrapy crawl common -a template_name=<retailer>` to verify it paginates and emits data.

## Contributing

Issues and pull requests that add or improve retailer templates, pagination logic, or extraction helpers are welcome. Please keep templates well-commented, anonymize sensitive identifiers, and include notes on any authentication or proxy requirements to keep the collection healthy for the community.
