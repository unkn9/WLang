from utils.classes import Parser


class HeadingParser:
    def __init__(self, parser: Parser, source_file: str):
        self.source_file = source_file
        self.method = parser.consume(source_file, "N_FUNC")
        assert self.method.value in (
            "heading1",
            "heading2",
            "heading3",
            "heading4",
            "heading5",
            "heading6",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        )
        self.level = self.method.value[-1]
        parser.consume(source_file, "LPAREN")
        self.value = parser.consume(source_file, "STRING", "RPAREN")
        if self.value.type == "STRING":
            parser.consume(source_file, "RPAREN")
        else:
            self.value.value = ""
        parser.consume(source_file, "SEMICOLON")

    def html(self):
        return f"<h{self.level}>{self.value.value}</h{self.level}>"

    def __repr__(self):
        return f"<h{self.level}>{self.value.value}</h{self.level}>"
