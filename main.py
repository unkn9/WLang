from utils.a import scan
from utils.classes import Lexer, Parser
from lexer import tokenize
from parser import parse
from sys import argv

if __name__ == "__main__":
    args = argv[1:]
    if not args:
        print("WLang version 0.0.2")
        print("GitHub: https://github.com/Zen-kun04/WLang")
    elif len(args) >= 1 and args[0] == "compile":
        print("Compiling sources...")
        lexer = Lexer()
        parser = Parser()
        scan(lexer)

        for source_file in lexer.source_code:
            tokenize(lexer.source_code[source_file], source_file, parser)
            parse(parser, source_file)
        print("Check the folder: out/")
    else:
        print("Unknown command:", args[0])