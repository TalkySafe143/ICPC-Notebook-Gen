from pylatex import Package
from pylatex.base_classes import Environment
class Multicols(Environment):
    packages = [Package("multicol")]
    content_separator = "\n"
