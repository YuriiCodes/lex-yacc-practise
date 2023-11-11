import ply.yacc as yacc
from lex import tokens

variables = {}


class ASTNode:
    def to_json(self):
        raise NotImplementedError("Subclasses should implement this!")

    def to_dict(self):
        raise NotImplementedError("Subclasses should implement this!")

    pass


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def to_json(self):
        return {"type": "BinOp", "op": self.op, "left": self.left.to_json(), "right": self.right.to_json()}

    def to_dict(self):
        return {"type": "BinOp", "op": self.op, "left": self.left.to_dict(), "right": self.right.to_dict()}

    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        if self.op == '+':
            return left_val + right_val
        elif self.op == '-':
            return left_val - right_val
        elif self.op == '*':
            return left_val * right_val
        elif self.op == '/':
            return left_val / right_val
        elif self.op == '^':
            return left_val ** right_val
        elif self.op == 'mod':
            return left_val % right_val


class Num(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def evaluate(self):
        return self.value

    def to_json(self):
        return {"type": "Num", "value": self.value}

    def to_dict(self):
        return {"type": "Num", "value": self.value}


class Var(ASTNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def evaluate(self):
        # Here you need to fetch the value of the variable from a stored location
        return variables.get(self.name, 0)  # Assuming 'variables' is your variable storage

    def to_json(self):
        return {"type": "Var", "name": self.name}

    def to_dict(self):
        return {"type": "Var", "name": self.name}


class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name} = {self.value}"

    def evaluate(self):
        # Assign the value to the variable in your variable storage
        variables[self.name] = self.value.evaluate()
        return variables[self.name]


def to_dict(self):
    return {"type": "Assign", "name": self.name, "value": self.value.to_dict()}


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EXPONENT'),
    ('right', 'UMINUS'),
)


def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]


def p_statement_assign(p):
    'statement : IDENTIFIER EQUALS expression'
    p[0] = Assign(Var(p[1]), p[3])


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression EXPONENT expression'''
    p[0] = BinOp(p[1], p[2], p[3])


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = BinOp(Num(0), "-", p[2])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = Num(p[1])


def p_expression_var(p):
    "expression : IDENTIFIER"
    p[0] = Var(p[1])


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()
