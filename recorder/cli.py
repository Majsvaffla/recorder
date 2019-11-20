from pathlib import Path

import click
import yaml
from bs4 import BeautifulSoup

from .html.renderers import ProtokollRenderer
from .markdown import ParserWithoutBody
from .templates import templates


def validate_template(ctx, param, value):
    if value in templates.IDENTIFIERS:
        return value
    raise click.BadParameter(f"'{value}' is an unknown template.")


@click.command()
@click.argument("source", type=click.File("r"))
@click.argument("template", type=click.STRING, callback=validate_template)
@click.option(
    "--context",
    type=click.File("r"),
    default=None,
    help="Path to a YAML file providing values to variables in the template.",
)
@click.option(
    "--stylesheet",
    type=click.Path(readable=True),
    default=None,
    help="Path to a CSS file that will be applied to the HTML.",
)
@click.option(
    "--output",
    type=click.Path(writable=True),
    default="output.pdf",
    help="Path to the output PDF file.",
)
def cli(source, template, context, stylesheet, output):
    document_template = templates.from_identifier(template)

    markdown = source.read()
    markdown_to_html = ParserWithoutBody(renderer=document_template.renderer())
    content = markdown_to_html(markdown)

    template_context = yaml.safe_load(context.read()) if context else {}

    html = document_template.render(
        **template_context,
        agenda_items_html=content.format(meeting_id=template_context.get("meeting_id")),
    )

    print(BeautifulSoup(html, "html.parser").prettify())
