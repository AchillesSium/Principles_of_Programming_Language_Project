#!/usr/bin/env python3


from ply import yacc
import sys, lexesPractice # previous phase example snippet code

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexesPractice.tokens

# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce 
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
def p_program(p):
    '''program : function_or_variable_definition statement_list'''
    p[0] = p[1]
    print( 'program' )

def p_function_or_variable_definition(p):
    '''function_or_variable_definition : empty
                                       | variable_definition
                                       | function_definition
                                       | subroutine_definition
                                       | function_or_variable_definition variable_definition'''

def p_variable_definition(p):

    '''variable_definition : scalar_definition
                           | range_definition
                           | sheet_definition'''

def p_different_variable_definition(p):
    '''different_variable_definition : variable_definition
                                     | different_variable_definition variable_definition'''

def p_function_definition(p):
    '''function_definition : FUNCTION get_func_ident LSQUARE formal_arg RSQUARE RETURN scalar_or_range IS different_variable_definition statement_list END'''


def p_get_func_ident(p):
    '''get_func_ident : FUNC_IDENT'''
    print('function_definition(',p[1],')')

def p_subroutine_definition(p):
    '''subroutine_definition : SUBROUTINE get_subroutine_ident LSQUARE formal_arg RSQUARE IS different_variable_definition statement_list END'''

def p_get_subroutine_ident(p):
    '''get_subroutine_ident : FUNC_IDENT'''
    print('subroutine_definition(',p[1],')')

def p_scalar_or_range(p):
    '''scalar_or_range : SCALAR
                       | RANGE'''


def p_empty(p):

    '''empty : '''


def p_formals(p):

    '''formals : formal_arg comma_arguments'''

    print('formals')

def p_formal_arg(p):
    '''formal_arg : IDENT COLON SCALAR
                  | RANGE_IDENT COLON RANGE
                  | SHEET_IDENT COLON SHEET'''



def p_comma_arguments(p):
    '''comma_arguments : comma_argument
                       | comma_arguments comma_argument  '''



def p_comma_argument(p):
    '''comma_argument : COMMA formal_arg  '''


def p_sheet_definition(p):


    '''sheet_definition : SHEET get_sheet_ident new_sheet_init'''

    # print('sheet_definition')

def p_get_sheet_ident(p):
    '''get_sheet_ident : SHEET_IDENT'''
    print('variable_definition(', p[1], ':sheet', ')')

def p_new_sheet_init(p):


    '''new_sheet_init : sheet_init
                      | empty '''

    # print('new_sheet_init')


def p_sheet_init(p):
    '''sheet_init : EQ sheet_init_list
                  | EQ INT_LITERAL MULT INT_LITERAL
                  | EQ INT_LITERAL MULT INT_LITERAL subroutine_definition'''



def p_sheet_init_list(p):

    '''sheet_init_list : LCURLY differentsheetrow RCURLY'''




def p_differentsheetrow(p):

    '''differentsheetrow : sheet_row
                         | differentsheetrow sheet_row '''



def p_sheet_row(p):

    '''sheet_row : simple_expr
                 | sheet_row COMMA simple_expr'''




def p_range_definition(p):

    '''range_definition : RANGE get_range_ident another_equalrange'''


def p_get_range_ident(p):
    '''get_range_ident : RANGE_IDENT'''
    print('variable_definition(', p[1],':range', ')')

def p_another_equalrange(p):

    '''another_equalrange : EQ range_expr
                          | empty'''


def p_scalar_definition(p):

    '''scalar_definition : SCALAR get_ident another_equalscalar'''


def p_get_ident(p):
    '''get_ident : IDENT'''
    print('variable_definition(',p[1], ':scalar',')')

def p_another_equalscalar(p):

    '''another_equalscalar : EQ scalar_expr
                           | empty'''

    # print('another_equalscalar(',p[1],')')


def p_statement_list(p):

    '''statement_list : differentstatements'''

def p_differentstatements(p):

    '''differentstatements : statement
                           | differentstatements statement'''


def p_statement(p):

    '''statement : print_sheet
                 | print_range
                 | print_scalar
                 | ifscalar
                 | whilescalar
                 | forrangelist
                 | returnstatement
                 | assignment
                 | subroutine_call'''

def p_print_sheet(p):

   '''print_sheet : PRINT_SHEET  infostrings SHEET_IDENT'''
   print('statement( print_sheet )')

def p_infostrings(p):

   '''infostrings : INFO_STRING
                  | empty'''


def p_print_range(p):

   '''print_range : PRINT_RANGE infostrings range_expr'''

   print('statement( print_range )')

def p_print_scalar(p):

   '''print_scalar : PRINT_SCALAR infostrings scalar_expr
                   | PRINT_SCALAR infostrings IDENT'''

   print('statement( print_scalar )')

def p_ifscalar(p):

    '''ifscalar : IF scalar_expr THEN statement_list elsescalar ENDIF'''

    print('statement( if )')

def p_elsescalar(p):

    '''elsescalar : ELSE statement_list
                  | ELSE IF scalar_expr THEN statement_list ENDIF
                  | empty'''
#
# def p_else_if_scalar(p):
#     '''else_if_scalar : '''

def p_whilescalar(p):

    '''whilescalar : WHILE scalar_expr DO statement_list DONE'''
    print('statement( while )')

def p_forrangelist(p):

    '''forrangelist : FOR range_list DO statement_list DONE
                    | FOR many_range_expr DO statement_list DONE'''
    print('statement( for )')

def p_many_range_expr(p):
    '''many_range_expr : range_expr
                       | COMMA range_expr
                       | COMMA IDENT'''

def p_returnstatement(p):

    '''returnstatement : RETURN scalarrangesexpr
                       | RETURN IDENT'''
    print('statement( return )')


def p_scalarrangesexpr(p):

    '''scalarrangesexpr : scalar_expr
                        | range_expr'''


def p_range_list(p):

    '''range_list : range_expr commarangesexpr
                  | range_expr commarangesexpr commarangesexpr'''



def p_commarangesexpr(p):

    '''commarangesexpr : empty
                       | COMMA range_expr
                       | COMMA IDENT'''



def p_arguments(p):

    '''arguments : arg_expr commaargumentexpr
                 | arg_expr'''

def p_commaargumentexpr(p):

    '''commaargumentexpr : COMMA arg_expr'''
    print('commaargumentexpr')


def p_arg_expr(p):

    '''arg_expr : scalar_expr
                | range_expr
                | SHEET_IDENT'''


def p_subroutine_call(p):
    '''subroutine_call : subroutine_call_print LSQUARE arguments RSQUARE'''

def p_subroutine_call_print(p):
    '''subroutine_call_print : FUNC_IDENT'''
    print('subroutine_call(',p[1],')')

def p_assignment(p):

    '''assignment : assign_variable_name ASSIGN scalar_expr
                  | assign_variable_name ASSIGN simple_expr
                  | cell_ref ASSIGN function_call
                  | cell_ref ASSIGN scalar_expr
                  | RANGE_IDENT ASSIGN range_expr
                  | SHEET_IDENT ASSIGN SHEET_IDENT'''


def p_assign_variable_name(p):
    '''assign_variable_name : IDENT'''
    print('assignment(', p[1], ')')


def p_function_call(p):
    '''function_call : function_call_print LSQUARE arguments RSQUARE'''

def p_function_call_print(p):
    '''function_call_print : FUNC_IDENT'''
    print('function_call(',p[1],')')

def p__exprrange(p):

    '''range_expr : RANGE_IDENT
                  | RANGE cell_ref DOTDOT cell_ref
                  | range_expr LSQUARE INT_LITERAL COMMA INT_LITERAL RSQUARE'''


def p_cell_ref(p):

    '''cell_ref : SHEET_IDENT SQUOTE COORDINATE_IDENT
                | DOLLAR colonrange_indent'''



def p_colonrange_indent(p):

    '''colonrange_indent : COLON RANGE_IDENT
                         | empty'''



def p_scalar_expr(p):

    '''scalar_expr : simple_expr
                   | scalar_expr differentexpr IDENT
                   | scalar_expr differentexpr simple_expr'''
    print('scalar_expr')

def p_differentexpr(p):

    '''differentexpr : multipleexpr'''


def p_multipleexpr(p):

    '''multipleexpr : EQ
                    | NOTEQ
                    | LT
                    | LTEQ
                    | GT
                    | GTEQ'''



def p_simple_expr(p):

    '''simple_expr : term
                   | IDENT plusminusexprs
                   | atom
                   | simple_expr plusminusexprs term'''



def p_plusminusexprs(p):

    '''plusminusexprs : plusminusexp DOLLAR
                      | plusminusexp term'''



def p_plusminusexp(p):

    '''plusminusexp : PLUS
                    | MINUS'''



def p_term(p):

    '''term : factor
            | term multdivexprs factor'''
    print('term')


def p_multdivexprs(p):

    '''multdivexprs : MULT
                    | DIV'''
    print('multdivexprs')


def p_factor(p):

    '''factor : only_minus atom'''
    print('factor')

def p_only_minus(p):

    '''only_minus : MINUS
                  | empty'''



def p_atom(p):
    '''atom : decimal_sep
            | another_atom'''


def p_another_atom(p):
    '''another_atom : IDENT
                    | cell_ref
                    | NUMBER_SIGN range_expr
                    | LPAREN scalar_expr RPAREN'''
    if p[1] == None:
        print('atom')
    else:
        print('atom(',p[1],')')


def p_decimal_sep(p):
    '''decimal_sep : DECIMAL_LITERAL'''
    print('atom(',p[1],')')

# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print( 'syntax error @', p )
    raise SystemExit

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        # identify who wrote this
        print( 'Nothing' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexesPractice.lexer, debug=True)
        if result is None:
            print( 'syntax OK' )

