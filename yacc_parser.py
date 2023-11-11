import math

import ply.yacc as yacc
from lex import tokens

# Indirect Usage: In PLY, the tokens variable from the lex file is used indirectly by the Yacc module
# to ensure that the tokens defined in the lexer match up with those used in the parser. This linkage
# is crucial for the lexer and parser to work together correctly. However, this use is not in the form
# of direct function calls or variable accesses that static analysis tools typically detect.

# Parsing rules
# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'UMINUS'),  # Unary minus operator
    ('left', 'EXPONENT'),
    ('right', 'SQRT'),
    ('left', 'MOD'),
)

start = 'statement'

# Dictionary to store variable values
variables = {}


# Define a rule for statements which could be either assignments or expressions
def p_statement(p):
    '''
    statement : assignment
              | expression
    '''
    p[0] = p[1]


def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression'
    variables[p[1]] = p[3]
    p[0] = p[3]


# Grammar rules and actions
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_exponent(p):
    'expression : expression EXPONENT expression'
    p[0] = p[1] ** p[3]


def p_expression_mod(p):
    'expression : expression MOD expression'
    p[0] = p[1] % p[3]


def p_expression_sqrt(p):
    'expression : SQRT LPAREN expression RPAREN'
    p[0] = math.sqrt(p[3])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# New rule for variable
def p_expression_var(p):
    'expression : IDENTIFIER'
    try:
        p[0] = variables[p[1]]
    except LookupError:
        print(f"Undefined name '{p[1]}'")
        p[0] = 0


# Build the parser
parser = yacc.yacc()
