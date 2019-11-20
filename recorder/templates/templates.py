import os

import attr
from jinja2 import Environment, FileSystemLoader, select_autoescape

_TEMPLATES_PATH = os.path.dirname(os.path.abspath(__file__))
_TEMPLATES = Environment(
    loader=FileSystemLoader(_TEMPLATES_PATH), autoescape=select_autoescape(["html"]),
)


class InvalidTemplateIdentifier(Exception):
    pass


@attr.attrs
class _Template:
    identifier = attr.attrib()
    name = attr.attrib()
    renderer = attr.attrib()

    @property
    def _html(self):
        return _TEMPLATES.get_template(f"{self.identifier}.html")

    def render(self, *args, **kwargs):
        return self._html.render(*args, **kwargs)


_all = []

_by_identifier = {t.identifier: t for t in _all}

ALL = [t for t in _all]

IDENTIFIERS = _by_identifier.keys()


def from_identifier(identifier):
    if identifier in IDENTIFIERS:
        return _by_identifier[identifier]
    raise InvalidTemplateIdentifier(identifier)
