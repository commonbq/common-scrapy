"""Command line interface for running the Common spider."""

from __future__ import annotations

import os
from pathlib import Path

import click
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from common.spiders.common_spider import CommonSpider

# Ensure Scrapy loads the project's settings when invoked as a standalone script.
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "common.settings")


@click.group()
def cli() -> None:
    """Entrypoint for the common scrapy utilities."""


@cli.command()
@click.argument("retailer_products")
def crawl(retailer_products: str) -> None:
    """Run the "common" spider for the given retailer products identifier."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(CommonSpider, name=retailer_products)
    process.start()


@cli.command(name="list")
def list_templates() -> None:
    """List available templates under ``common/templates``."""
    templates_dir = Path(__file__).resolve().parent.parent / "common" / "templates"
    if not templates_dir.is_dir():
        raise click.ClickException("Templates directory not found.")

    templates = sorted(entry.name for entry in templates_dir.iterdir() if entry.is_dir())
    if not templates:
        click.echo("No templates found.")
        return

    for template in templates:
        click.echo(template)

def main() -> None:
    """CLI entry point used by ``python -m`` and console scripts."""
    cli(prog_name="common-scrapy")


if __name__ == "__main__":
    main()
