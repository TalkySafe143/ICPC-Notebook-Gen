from pylatex import Package
from pylatex.base_classes import Environment
class Landscape(Environment):
    packages = [Package("pdflscape")]
    content_separator = "\n"
