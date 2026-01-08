"""Command line interface for running the Common spider."""

from __future__ import annotations

import os
from pathlib import Path

import click
from scrapy.cmdline import execute

from common.spiders.common_spider import CommonSpider

# Ensure Scrapy loads the project's settings when invoked as a standalone script.
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "common.settings")


@click.group()
def cli() -> None:
    """Entrypoint for the common scrapy utilities."""


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("template")
@click.argument("scrapy_args", nargs=-1, type=click.UNPROCESSED)
def crawl(template: str, scrapy_args: tuple[str, ...]) -> None:
    """Run the "common" spider for the given template identifier."""
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
