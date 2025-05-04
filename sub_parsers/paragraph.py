from utils.classes import Parser


class ParagraphParser:
    def __init__(self, parser: Parser, source_file: str):
        self.source_file = source_file
        self.method = parser.consume(source_file, "N_FUNC")
        assert self.method.value in ("paragraph", "p")
        parser.consume(source_file, "LPAREN")
        self.value = parser.consume(source_file, "STRING", "RPAREN")
        if self.value.type == "STRING":
            parser.consume(source_file, "RPAREN")
        else:
            self.value.value = ''
        parser.consume(source_file, "SEMICOLON")
    
    def html(self):
        return f"<p>{self.value.value}</p>"
        
    def __repr__(self):
        return f"<p>{self.value.value}</p>"