import os
from pylatex import Document, Package, UnsafeCommand
from pylatex.base_classes import Arguments, Options
from pylatex.utils import NoEscape

from commands.algorithm import Algorithm
from commands.directory import Directory
from environments.landscape import Landscape
from environments.minted import Minted
from environments.multicols import Multicols
from ignore import getAllGitIgnores

class LatexParser:
    def __init__(self) -> None:
        self.doc = Document(
            default_filepath=os.path.join(os.getcwd(), "dist/out"),
            documentclass="report",
            document_options="letterpaper, 15pt"
        )
        self.doc.packages.append(Package('multicol'))
        self.doc.packages.append(Package('blindtext'))
        self.doc.packages.append(Package('listings'))
        self.doc.packages.append(Package('xcolor'))
        self.doc.packages.append(Package('minted'))
        self.doc.packages.append(Package('pdflscape'))
        self.doc.packages.append(Package('geometry', NoEscape(r"a4paper, total={7.5in, 11.3in}")))
        self.doc.append(NoEscape(r"""
            \usemintedstyle{bw}
            \lstset { %
                language=C++,
                basicstyle=\scriptsize\ttfamily,
                commentstyle=\normalfont\itshape
            }
            \newcommand{\directory}[1]{
                {
                \Huge \centering
                \textbf{#1}\\
                \vspace{0cm}
                }
            }
            \newcommand{\algorithm}[2]{
                \section*{#1}
                #2
            }
            \newminted[cpp]{c}{breaklines}
            """))

    def init(self):
        with self.doc.create(Landscape()):
            self.doc.append(
                NoEscape(
                    r"""\begin{titlepage}
                        \begin{center}
                            \vspace*{1cm}

                            \Huge
                            \textbf{Notebook}

                            \vspace{0.5cm}
                            \LARGE
                            Competitive programming notebook

                            \vspace{1.5cm}

                            \textbf{UnratedPUJ}

                            \vfill

                            Collection of algorithms and implementations\\
                            for ICPC competitions

                            \vspace{0.8cm}

                            \Large
                            Pontificia Universidad Javeriana\\
                            Colombia\\
                            Bogotá

                        \end{center}
                    \end{titlepage}
                    \large
                    \setlength{\columnseprule}{0.5pt}
                    """
                )
            )
            with self.doc.create(Multicols(arguments="2")):
                self.parseFiles(os.getcwd(), getAllGitIgnores())

    def parseFiles(self, startpath : str, vis):
        for root, dirs, files in os.walk(startpath):
            good = True
            for d in root.split("/"):
                if vis[d]:
                    good = False
                    break
            if not good or os.path.basename(root) == os.path.basename(os.getcwd()):
                continue

            self.doc.append(Directory(arguments=Arguments(os.path.basename(root))))
            for f in files:
                if f == ".gitignore" or vis[f] or f == "README.md":
                    continue
                desc, code = self.getFileInfo(os.path.join(root, f))
                self.doc.append(Algorithm(arguments=Arguments(f.split(".")[0], NoEscape(desc))))
                with self.doc.create(Minted(options=Options("breaklines"), arguments=Arguments("c"))):
                    self.doc.append(NoEscape(code))

    def getFileInfo(self, path: str):
        code = ""
        desc = ""
        with open(path, "r") as file:
            content = file.read().split("*/")
            if len(content) > 1:
                ignoreV = content[0].split("---")
                desc = ignoreV[0].split("/*")[1]
            code = content[-1].strip()
        return (desc, code)
    def dump(self):
        self.doc.generate_tex()
