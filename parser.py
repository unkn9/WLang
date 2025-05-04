from sub_parsers.footer import FooterParser
from sub_parsers.head import HeadParser
from sub_parsers.main import MainParser
from utils.classes import Parser
from utils.a import base
from os import mkdir
from os.path import isdir


def parse(parser: Parser, source_file: str):
    head_ast = []
    body_ast = []
    footer_ast = []
    head = False
    main = False
    footer = False

    while parser.current_token(source_file):
        if parser.current_token(source_file).type == "N_FUNC":
            if parser.current_token(source_file).value == "head":
                if head:
                    raise Exception("Error: head function is already declared!")
                head = True
                head_ast.append(HeadParser(parser, source_file).html())
                continue

            if parser.current_token(source_file).value == "main":
                if main:
                    raise Exception("Error: main function is already declared!")
                main = True
                body_ast.append(MainParser(parser, source_file).html())
                continue
            
            if parser.current_token(source_file).value == "footer":
                if footer:
                    raise Exception("Error: footer function is already declared!")
                footer = True
                footer_ast.append(FooterParser(parser, source_file).html())
                continue
            
        raise Exception(f"Unregistered token: '{parser.current_token(source_file).value}' of type {parser.current_token(source_file).type}") 

    if not isdir("out"): mkdir("out")
    with open("out/" + source_file.rsplit('.', 1)[0] + ".html", 'w') as f:
        code = base.replace('[lang]', parser.language).replace("[head]", '\n'.join(head_ast)).replace("[body]", '\n'.join(body_ast)).replace("[footer]", f"""<footer>
{'\n'.join(footer_ast)}
</footer>""" if footer_ast else "")
        f.write(f"{code}\n<!-- Made with <3 using WLang -->")