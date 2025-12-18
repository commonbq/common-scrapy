# Common Scrapy Templates

An open, well-maintained collection of Scrapy templates for harvesting structured product data from major retailers. Each template encodes the HTTP request, pagination strategy, and response extraction rules needed for a specific storefront so you can stay focused on downstream data processing.

## Project layout

- `common/spiders/common_spider.py` – single parameterized spider that loads retailer-specific templates and converts API responses into normalized items.
- `common/templates/` – each retailer lives in its own folder (for example, `common/templates/<retailer>/`) with three files:
  - `request.json` – captured HTTP request, headers, query/body params, and pagination strategy.
  - `sample.json` – a trimmed API response saved from the network inspector so you can reason about the payload without re-running the crawl.
  - `extract.json` – schema describing what to copy out of the payload (see “Iterating on extraction”).
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
   - Inspect `common/templates/<name>/` for existing retailer folders.
   - Duplicate a folder to bootstrap a new retailer and update `request.json` with headers, query parameters, and pagination details.
   - Keep `sample.json` roughly in sync with the responses you see in DevTools so you can iterate locally on extraction logic.

## Running a crawl

```bash
scrapy crawl common -a name=<retailer_products>
```

Arguments:
- `name` – JSON filename (without extension) in `common/templates/`.

The spider will issue the configured request, follow pagination, and yield structured records defined in `extract.json`.

### Iterating on extraction

- Reference `sample.json` to understand the payload shape without replaying the crawl.
- Update `extract.json` to control which fields land in the final item. Set `$list` to the array that contains products, `$include` for top-level metadata to copy onto every record, and `$item` for nested lookups inside each product.
- Save the file and re-run the spider to confirm you get the expected output.

## Adding new retailer templates

1. Capture a representative network request (e.g., via DevTools) and save the HAR snippet into `common/templates/<retailer>/request.json`.
2. Grab a sample JSON response (copy/paste the network preview) and drop it into `common/templates/<retailer>/sample.json`. Update it as the API evolves.
3. Populate `extract.json` with `$list`, `$include`, and `$item` sections so the spider knows which fields to emit.
4. Run the spider with `scrapy crawl common -a name=<retailer>` to verify it paginates and emits data.

## Contributing

Issues and pull requests that add or improve retailer templates, pagination logic, or extraction helpers are welcome. Please keep templates well-commented, anonymize sensitive identifiers, and include notes on any authentication or proxy requirements to keep the collection healthy for the community.
