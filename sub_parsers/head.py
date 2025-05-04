from sub_parsers.head_block import HeadBlockParser
from utils.classes import Parser


class HeadParser:
    def __init__(self, parser: Parser, source_file: str):
        self.source_file = source_file
        self.method = parser.consume(source_file, "N_FUNC")
        assert self.method.value == "head"
        parser.consume(source_file, "LPAREN")
        parser.consume(source_file, "RPAREN")
        parser.consume(source_file, "LBRACE")

        self.code = HeadBlockParser(parser, source_file).html()

    def html(self):
        return self.code

    def __repr__(self):
        return ""
