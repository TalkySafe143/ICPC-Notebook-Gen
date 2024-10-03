from latex_parser import LatexParser

if "__main__" == __name__:
    parser = LatexParser()
    parser.init()
    parser.dump()
    print("Compile dist/out.tex with --shell-escape option")
