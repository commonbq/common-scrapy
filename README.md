# Common Scrapy Templates

An open, well-maintained collection of Scrapy templates for harvesting structured product data from major retailers. Each template encodes the HTTP request, pagination strategy, and response extraction rules needed for a specific storefront so you can stay focused on downstream data processing.

## Installation

```bash
pip install common-scrapy
```

## CLI usage

`pip install common-scrapy` adds a `common-scrapy` console script so you can work with the packaged spider without cloning the repo.

### Use your own proxy

Set the `PROXY` environment variable inline with the command to force all HTTP requests through your proxy of choice. Any syntax Scrapy supports will work, for example:

```bash
PROXY=http://user:pass@host:1234 common-scrapy crawl kohls_products
```

If you need to switch proxies between runs, just update the `PROXY=` prefix before invoking `common-scrapy` again.

### List available templates

```bash
common-scrapy list
```

### Run a crawl

```bash
common-scrapy crawl <template> [additional Scrapy args]
```

Examples:

- `common-scrapy crawl kohls_products -s LOG_LEVEL=INFO`
- `common-scrapy crawl sephora_products -o sephora.csv`

The command wires Scrapy's `common` spider to the template you choose, so any flags you normally pass to `scrapy crawl` still work (for example, output feeds, settings overrides, or depth limits).

## Available templates

- `kohls_products` – product listing crawl for Kohl's seasonal catalog endpoints.
- `sephora_products` – product listing crawl for Sephora category APIs.

## Contributing

Issues and pull requests that add or improve retailer templates, pagination logic, or extraction helpers are welcome. Please keep templates well-commented, anonymize sensitive identifiers, and include notes on any authentication or proxy requirements to keep the collection healthy for the community.

### Project layout

- `common/spiders/common_spider.py` – single parameterized spider that loads retailer-specific templates and converts API responses into normalized items.
- `common/templates/` – each retailer lives in its own folder (for example, `common/templates/<retailer>/`) with three files:
  - `request.json` – captured HTTP request, headers, query/body params, and pagination strategy.
  - `sample.json` – a trimmed API response saved from the network inspector so you can reason about the payload without re-running the crawl.
  - `extract.json` – schema describing what to copy out of the payload (see “Iterating on extraction”).
- `common/settings/` – shared Scrapy configuration; reads environment variables via `.env`.
- `scrapy.cfg` – entry point for the `scrapy` CLI.

### Iterating on extraction

- Reference `sample.json` to understand the payload shape without replaying the crawl.
- Update `extract.json` to control which fields land in the final item. Set `$list` to the array that contains products, `$include` for top-level metadata to copy onto every record, and `$item` for nested lookups inside each product.
- Save the file and re-run the spider to confirm you get the expected output.

### Adding new retailer templates

1. Capture a representative network request (e.g., via DevTools) and save the HAR snippet into `common/templates/<retailer>/request.json`.
2. Grab a sample JSON response (copy/paste the network preview) and drop it into `common/templates/<retailer>/sample.json`. Update it as the API evolves.
3. Populate `extract.json` with `$list`, `$include`, and `$item` sections so the spider knows which fields to emit.
4. Run the spider with `scrapy crawl common -a name=<retailer>` to verify it paginates and emits data.
