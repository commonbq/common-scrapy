"""Command line interface for running the Common spider.

Behavior:
- If the given identifier matches a purpose-built spider (e.g. `amazon_listing`),
  run that spider.
- Otherwise, treat it as a template name and run the parameterized `common` spider.
"""

from __future__ import annotations

import os
import pkgutil
import inspect
from pathlib import Path

import click
import scrapy
from scrapy.cmdline import execute

from common.spiders.common_spider import CommonSpider

# Ensure Scrapy loads the project's settings when invoked as a standalone script.
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "common.settings")


@click.group()
def cli() -> None:
    """Entrypoint for the common scrapy utilities."""


def _purpose_built_spider_names() -> set[str]:
    """Discover purpose-built spiders under ``common.spiders``.

    Convention: any module ending with ``_spider`` (excluding ``common_spider``)
    may define one or more ``scrapy.Spider`` subclasses.
    """

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
            # Don't fail CLI discovery if an optional spider module errors.
            continue

        for _, obj in inspect.getmembers(m, inspect.isclass):
            if not issubclass(obj, scrapy.Spider):
                continue
            spider_name = getattr(obj, "name", None)
            if isinstance(spider_name, str) and spider_name and spider_name != CommonSpider.name:
                names.add(spider_name)

    return names


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("template")
@click.argument("scrapy_args", nargs=-1, type=click.UNPROCESSED)
def crawl(template: str, scrapy_args: tuple[str, ...]) -> None:
    """Run a crawl.

    If ``template`` matches a purpose-built spider name, run that spider.
    Otherwise, run the parameterized ``common`` spider with ``-a name=<template>``.
    """

    purpose_built = _purpose_built_spider_names()

    if template in purpose_built:
        argv = ["scrapy", "crawl", template, *scrapy_args]
    else:
        argv = [
            "scrapy",
            "crawl",
            CommonSpider.name,
            "-a",
            f"name={template}",
            *scrapy_args,
        ]

    execute(argv)


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
