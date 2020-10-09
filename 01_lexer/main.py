import sys, ply.lex

#Reserved words

# sheet, scalar, range, do, done, is, while, for, if, then, else, endif,
# function, subroutine, return, end, print_sheet, print_scalar, print_range
reserved = {'sheet' : 'SHEET',
            'scalar' : 'SCALAR',
            'range' : 'RANGE',
            'do' : 'DO',
            'done' : 'DONE',
            'is' : 'IS',
            'while' : 'WHILE',
            'for' : 'FOR',
            'if' : 'IF',
            'then' : 'THEN',
            'else' : 'ELSE',
            'endif' : 'ENDIF',
            'function' : 'FUNCTION',
            'subroutine' : 'SUBROUTINE',
            'return' : 'RETURN',
            'end' : 'END',
            'print_sheet' : 'PRINT_SHEET',
            'print_scalar' : 'PRINT_SCALAR',
            'print_range' : 'PRINT_RANGE'
            }
# List of token names.   This is always required
tokens = [
    'WHITESPACE',
    'COMMENT',
    'INFO_STRING',
    'INT_LITERAL',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'LCURLY',
    'RCURLY',
    'COMMA',
    'DOTDOT',
    'SQUOTE',
    'COLON',
    'DOLLAR',
    'NUMBER_SIGN',
    'EQ',
    'NOTEQ',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ',
    'sheet',
    'scalar',
    'range',
    'do',
    'done',
    'is',
    'while',
    'for',
    'if',
    'then',
    'else',
    'endif',
    'function',
    'subroutine',
    'return',
    'end',
    'print_sheet',
    'print_scalar',
    'print_range',
    'IDENT',
    'COORDINATE_IDENT',
    'FUNC_IDENT',
    'RANGE_IDENT',
    'SHEET_IDENT',
    'DECIMAL_LITERAL',
    'ID',
]

tokens = tokens + list(reserved.values())

def t_COMMENT(t):
    r'\.\.\..*\.\.\.'
    pass

# Regular expression rules for simple tokens
def t_WHITESPACE(t):
    r'\s'
    pass

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'\:='
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'\{'
t_RCURLY =r'\}'
t_COMMA = r'\,'
t_DOTDOT = r'\.\.'
t_SQUOTE = r"\'"
t_COLON = r'\:'
t_DOLLAR = r'\$'
t_NUMBER_SIGN = r'\#'
t_EQ = r'\='
t_NOTEQ = r'\!='
t_LTEQ = r'<='
t_LT = r'\<'
t_GTEQ = r'\>='
t_GT = r'\>'

# A regular expression rule with some action code

def t_INFO_STRING(t):
    r'!.*!'
    st = str(t.value)
    st = st.replace("!", "")
    t.value = st
    return t

def t_COORDINATE_IDENT(t):
    r'[A-Z]{1,2}[0-9]{1,3}'
    t.type = reserved.get(t.value, 'COORDINATE_IDENT')  # Check for reserved words
    return t

def t_IDENT(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENT')  # Check for reserved words
    return t

def t_RANGE_IDENT(t):
    r'[_][a-z_0-9]*'
    return t

def t_FUNC_IDENT(t):
    r'[A-Z][a-z_0-9]+'
    t.type = reserved.get(t.value, 'FUNC_IDENT')  # Check for reserved words
    return t

def t_SHEET_IDENT(t):
    r'[A-Z]+'
    t.type = reserved.get(t.value, 'SHEET_IDENT')  # Check for reserved words
    return t

def t_DECIMAL_LITERAL(t):
    r'[-]?[0-9]+[.][0-9]'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Decimal value invalid", t.value)
        t.value = 0.0
    return t

def t_INT_LITERAL(t):
    r'[-]?[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Int value invalid", t.value)
        t.value = 0
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = ply.lex.lex()

# if this module/file is the first one started (the main module)
# then run:
if __name__ == '__main__':
    import argparse, codecs
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')

    ns = parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print('nothing new')
    elif ns.file is None:
        # user didn't provide input filename
        print('nothing new2')
        parser.print_help()
    else:
        # using codecs to make sure we process unicode
        with codecs.open('animals.ss', 'r', encoding='utf-8' ) as INFILE:
            # blindly read all to memory (what if that is a 42Gb file?)
            data = INFILE.read()

        lexer.input( data )

        while True:
            token = lexer.token()
            if token is None:
                break
            print( token )
