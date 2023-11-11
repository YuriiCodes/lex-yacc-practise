import json

from yacc_parser import parser, variables, ASTNode


class ASTEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ASTNode):
            return o.to_dict()
        return json.JSONEncoder.default(self, o)


def main():
    while True:
        try:
            s = input('Enter a statement or expression: ')
        except EOFError:
            break
        if not s:
            continue
        ast = parser.parse(s)
        if ast:
            result = ast.evaluate()
            ast_json = json.dumps(ast, indent=2, cls=ASTEncoder)
            print("AST JSON:", ast_json)
            print("Result:", result)
        else:
            print("No valid input provided.")


if __name__ == '__main__':
    main()
