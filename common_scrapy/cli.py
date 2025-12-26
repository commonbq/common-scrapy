"""Command line interface for running the Common spider."""

from __future__ import annotations

import os

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


def main() -> None:
    """CLI entry point used by ``python -m`` and console scripts."""
    cli(prog_name="common-scrapy")
