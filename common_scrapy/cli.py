"""Command line interface for running purpose-built spiders only."""

from __future__ import annotations

import inspect
import os
import pkgutil
from collections.abc import Mapping

import click
import scrapy
from scrapy.cmdline import execute

# Ensure Scrapy loads the project's settings when invoked as a standalone script.
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "common.settings")


@click.group()
def cli() -> None:
    """Entrypoint for the common scrapy utilities."""


def _purpose_built_spiders() -> dict[str, type[scrapy.Spider]]:
    """Discover purpose-built spiders under ``common.spiders``."""

    import common.spiders as spiders_pkg

    spiders: dict[str, type[scrapy.Spider]] = {}

    for mod in pkgutil.iter_modules(spiders_pkg.__path__, prefix=f"{spiders_pkg.__name__}."):
        module_name = mod.name
        if module_name.endswith("common_spider"):
            continue
        if not module_name.endswith("_spider"):
            continue

        try:
            m = __import__(module_name, fromlist=["*"])
        except Exception:
            continue

        for _, obj in inspect.getmembers(m, inspect.isclass):
            if not issubclass(obj, scrapy.Spider):
                continue
            spider_name = getattr(obj, "name", None)
            if isinstance(spider_name, str) and spider_name:
                spiders[spider_name] = obj

    return spiders


def _purpose_built_spider_names() -> set[str]:
    return set(_purpose_built_spiders().keys())


def _available_categories(spider_cls: type[scrapy.Spider]) -> list[str]:
    categories = getattr(spider_cls, "categories", None)
    if not isinstance(categories, list):
        return []

    names: list[str] = []
    for entry in categories:
        if isinstance(entry, Mapping):
            category_name = entry.get("category")
            if isinstance(category_name, str) and category_name:
                names.append(category_name)

    return sorted(set(names))


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("spider")
@click.option("--category", help="Category shortcut for listing spiders.")
@click.argument("scrapy_args", nargs=-1, type=click.UNPROCESSED)
def crawl(spider: str, category: str | None, scrapy_args: tuple[str, ...]) -> None:
    """Run only a purpose-built spider by name."""

    purpose_built = _purpose_built_spiders()

    if spider not in purpose_built:
        available = ", ".join(sorted(purpose_built))
        raise click.ClickException(
            f"Unknown spider '{spider}'. Only purpose-built spiders are supported. "
            f"Available: {available}"
        )

    spider_cls = purpose_built[spider]
    available_categories = _available_categories(spider_cls)
    has_category_in_scrapy_args = any(arg.startswith("category=") for arg in scrapy_args)

    if available_categories and not category and not has_category_in_scrapy_args:
        raise click.ClickException(
            f"Spider '{spider}' requires --category=<category>. "
            f"Available categories: {', '.join(available_categories)}"
        )

    extra_args = list(scrapy_args)
    if category and not has_category_in_scrapy_args:
        extra_args = ["-a", f"category={category}", *extra_args]

    execute(["scrapy", "crawl", spider, *extra_args])


@cli.command(name="list")
def list_spiders() -> None:
    """List all available purpose-built spiders in this project."""
    spiders = sorted(_purpose_built_spider_names())

    if not spiders:
        click.echo("No spiders found.")
        return

    for spider in spiders:
        click.echo(spider)


def main() -> None:
    """CLI entry point used by ``python -m`` and console scripts."""
    cli(prog_name="common-scrapy")


if __name__ == "__main__":
    main()
