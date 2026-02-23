"""Command line interface for running purpose-built spiders only."""

from __future__ import annotations

import inspect
import os
import pkgutil

import click
import scrapy
from scrapy.cmdline import execute

# Ensure Scrapy loads the project's settings when invoked as a standalone script.
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "common.settings")


@click.group()
def cli() -> None:
    """Entrypoint for the common scrapy utilities."""


def _purpose_built_spider_names() -> set[str]:
    """Discover purpose-built spiders under ``common.spiders``."""

    import common.spiders as spiders_pkg

    names: set[str] = set()

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
                names.add(spider_name)

    return names


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("spider")
@click.argument("scrapy_args", nargs=-1, type=click.UNPROCESSED)
def crawl(spider: str, scrapy_args: tuple[str, ...]) -> None:
    """Run only a purpose-built spider by name."""

    purpose_built = _purpose_built_spider_names()

    if spider not in purpose_built:
        available = ", ".join(sorted(purpose_built))
        raise click.ClickException(
            f"Unknown spider '{spider}'. Only purpose-built spiders are supported. "
            f"Available: {available}"
        )

    execute(["scrapy", "crawl", spider, *scrapy_args])


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
