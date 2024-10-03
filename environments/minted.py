from pylatex.base_classes import Environment
from pylatex import Package

class Minted(Environment):
    packages=[Package('minted')]
    content_separator="\n"
