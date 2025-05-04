from sub_parsers.block import BlockParser
from utils.classes import Parser


class FooterParser:
    def __init__(self, parser: Parser, source_file: str):
        self.source_file = source_file
        self.method = parser.consume(source_file, "N_FUNC")
        assert self.method.value == "footer"
        parser.consume(source_file, "LPAREN")
        parser.consume(source_file, "RPAREN")
        parser.consume(source_file, "LBRACE")
        self.code = BlockParser(parser, source_file).html()

    def html(self):
        return self.code

    def __repr__(self):
        return f"<h{self.level}>{self.value.value}</h{self.level}>"
