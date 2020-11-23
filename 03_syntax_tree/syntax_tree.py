#!/usr/bin/env python3

from ply import yacc
import lexesPractice # previous phase example snippet code

import tree_print # syntax tree pretty-printer

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexesPractice.tokens

# Simple class to store syntax tree nodes, by default only contains the type of the node as string
# (more stuff will be added in BNF actions)
class ASTnode:
  def __init__(self, typestr):
    self.nodetype = typestr

# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
# any funcion starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors

def p_program1(p):
    '''program : function_or_variable_definition'''
    p[0] = ASTnode('program')
    p[0].children_funcs_vars = [p[1]]
    p[0].children_stmt_list = []

def p_program2(p):
    '''program : program function_or_variable_definition'''
    p[0] = p[1]
    p[0].children_funcs_vars.append(p[2])

def p_program3(p):
    '''program : program forrangelist'''
    p[0] = p[1]
    p[0].children_stmt_list = [p[2]]

def p_program4(p):
    '''program : program print_sheet'''
    p[0] = p[1]
    p[0].children_stmt_list.append(p[2])

def p_program5(p):
    '''program : program print_scalar'''
    p[0] = p[1]
    p[0].children_stmt_list.append(p[2])

def p_program6(p):
    '''program : program statement'''
    p[0] = p[1]
    p[0].children_stmt_list.append(p[2])

def p_program7(p):
    '''program : program subroutine_call'''
    p[0] = p[1]
    p[0].children_stmt_list.append(p[2])

def p_function_or_variable_definition1(p):
    '''function_or_variable_definition : variable_definition'''
    p[0] = p[1]

def p_function_or_variable_definition2(p):
    '''function_or_variable_definition : function_definition'''
    p[0] = p[1]

def p_function_or_variable_definition3(p):
    '''function_or_variable_definition : subroutine_definition'''
    p[0] = p[1]

def p_subroutine_definition1(p):
    '''subroutine_definition : SUBROUTINE get_func_ident LSQUARE'''
    p[0] = ASTnode('subroutine-def')
    p[0].child_name = p[2]
    p[0].children_formals = []
    p[0].children_vars = []
    p[0].children_stmts = []

def p_subroutine_definition2(p):
    '''subroutine_definition : subroutine_definition formal_arg'''
    p[0] = p[1]
    p[0].children_formals.append(p[2])

def p_subroutine_definition3(p):
    '''subroutine_definition : subroutine_definition RSQUARE IS'''
    p[0] = p[1]

def p_subroutine_definition4(p):
    '''subroutine_definition : subroutine_definition variable_definition'''
    p[0] = p[1]
    p[0].children_vars.append(p[2])

def p_subroutine_definition5(p):
    '''subroutine_definition : subroutine_definition statement'''
    p[0] = p[1]
    p[0].children_stmts.append(p[2])

def p_subroutine_definition6(p):
    '''subroutine_definition : subroutine_definition END'''
    p[0] = p[1]

def p_function_definition1(p):
    '''function_definition : FUNCTION get_func_ident LSQUARE'''
    p[0] = ASTnode('function_definition')
    p[0].child_name = p[2]
    p[0].children_formals = []
    p[0].child_rettype = None
    p[0].children_vars = []
    p[0].children_stmts = []

def p_function_definition2(p):
    '''function_definition : function_definition formal_arg'''
    p[0] = p[1]
    p[0].children_formals.append(p[2])

def p_function_definition3(p):
    '''function_definition : function_definition RSQUARE RETURN scalar_or_range IS'''
    p[0] = p[1]
    p[0].child_rettype = p[4]

def p_function_definition4(p):
    '''function_definition : function_definition variable_definition'''
    p[0].children_vars.append(p[2])
    p[0] = p[1]

def p_function_definition5(p):
    '''function_definition : function_definition statement'''
    p[0] = p[1]
    p[0].children_stmts.append(p[2])

def p_function_definition6(p):
    '''function_definition : function_definition END'''
    p[0] = p[1]

def p_get_func_ident(p):
    '''get_func_ident : FUNC_IDENT'''
    p[0] = ASTnode('FUNC_IDENT')
    p[0].value = p[1]

def p_formal_arg1(p):
    '''formal_arg : get_ident COLON SCALAR
                  | RANGE_IDENT COLON RANGE
                  | get_sheet_ident COLON SHEET'''
    p[0] = ASTnode('formal_arg')
    p[0].child_name = p[1]

def p_formal_arg(p):
    '''formal_arg : formal_arg COMMA'''
    p[0] = p[1]

def p_scalar_or_range(p):
    '''scalar_or_range : SCALAR
                       | RANGE'''
    p[0] = ASTnode('rettype')
    p[0].value = p[1]

def p_different_variable_definition1(p):
    '''different_variable_definition : variable_definition'''
    p[0] = p[1]

def p_different_variable_definition2(p):
    '''different_variable_definition : different_variable_definition variable_definition'''
    p[0] = p[2]

def p_variable_definition1(p):
    '''variable_definition : sheet_definition
                           | range_definition'''
    p[0] = p[1]

def p_variable_definition2(p):
    '''variable_definition : scalar_definition'''
    p[0] = p[1]

def p_scalar_definition1(p):
    '''scalar_definition : SCALAR get_ident another_equalscalar'''
    p[0] = ASTnode('scalar_definition')
    p[0].child_name = p[2]
    p[0].child_init = p[3]

def p_scalar_definition2(p):
    '''scalar_definition : SCALAR get_ident empty'''
    p[0] = ASTnode('scalar_definition')
    p[0].child_name = p[2]
    p[0].child_init = None

def p_get_ident(p):
    '''get_ident : IDENT'''
    p[0] = ASTnode('IDENT')
    p[0].value = p[1]

def p_another_equalscalar(p):
    '''another_equalscalar : EQ scalar_expr'''
    p[0] = p[2]

def p_scalar_expr1(p):
    '''scalar_expr : simple_expr'''
    p[0] = p[1]

def p_scalar_expr2(p):
    '''scalar_expr : new_scalar_expr'''
    p[0] = p[1]

def p_scalar_expr3(p):
    '''scalar_expr : scalar_expr PLUS new_scalar_expr'''
    p[0] = ASTnode('oper ' + p[2])
    p[0].child_left = p[1]
    p[0].child_right = p[3]

def p_scalar_expr4(p):
    '''scalar_expr : new_scalar_expr empty'''
    p[0] = p[1]

def p_new_scalar_expr1(p):
    '''new_scalar_expr : LPAREN simple_expr MULT simple_expr RPAREN'''
    p[0] = ASTnode('oper ' + p[3])
    p[0].child_left = p[2]
    p[0].child_right = p[4]

def p_new_scalar_expr2(p):
    '''new_scalar_expr : LPAREN simple_expr PLUS simple_expr RPAREN'''
    p[0] = ASTnode('oper ' + p[3])
    p[0].child_left = p[2]
    p[0].child_right = p[4]

def p_sheet_definition(p):
    '''sheet_definition : SHEET get_sheet_ident new_sheet_init'''
    p[0] = ASTnode('sheet_definition')
    p[0].child_name = p[2]
    p[0].child_init = p[3]

def p_get_sheet_ident(p):
    '''get_sheet_ident : SHEET_IDENT'''
    p[0] = ASTnode('SHEET_IDENT')
    p[0].value = p[1]

def p_new_sheet_init(p):
    '''new_sheet_init : sheet_init
                      | empty '''
    p[0] = p[1]

def p_sheet_init(p):
    '''sheet_init : EQ sheet_init_list'''
    p[0] = p[2]

def p_sheet_init_list1(p):
    '''sheet_init_list : INT_LITERAL MULT INT_LITERAL'''
    p[0] = ASTnode('sheet_init_size')
    p[0].value = p[1]

def p_sheet_init_list2(p):
    '''sheet_init_list : LCURLY differentsheetrow RCURLY'''
    p[0] = p[2]

def p_differentsheetrow1(p):
    '''differentsheetrow : sheet_row'''
    p[0] = ASTnode('sheet_init_list')
    p[0].children_rows = [p[1]]

def p_differentsheetrow2(p):
    '''differentsheetrow : differentsheetrow sheet_row'''
    p[0] = ASTnode('sheet_init_list')
    p[0] = p[1]
    p[0].children_rows.append(p[2])

def p_sheet_row1(p):
    '''sheet_row : simple_expr'''
    p[0] = ASTnode('col_init_list')
    p[0].children_cols = [p[1]]

def p_sheet_row2(p):
    '''sheet_row : sheet_row COMMA simple_expr'''
    p[0] = ASTnode('col_init_list')
    p[0] = p[1]
    p[0].children_cols.append(p[3])

def p_simple_expr1(p):
    '''simple_expr : atom'''
    p[0] = p[1]

def p_simple_expr3(p):
    '''simple_expr : simple_expr PLUS simple_expr'''
    p[0] = ASTnode('oper ' + p[2])
    p[0].child_left = p[1]
    p[0].child_right = p[3]

def p_simple_expr4(p):
    '''simple_expr : simple_expr MULT atom'''
    p[0] = ASTnode('oper ' + p[2])
    p[0].child_left = p[1]
    p[0].child_right = p[3]

def p_atom1(p):
    '''atom : decimal_sep'''
    p[0] = p[1]

def p_atom2(p):
    '''atom : scalar_ref'''
    p[0] = p[1]

def p_atom3(p):
    '''atom : cell_ref'''
    p[0] = p[1]

def p_decimal_sep(p):
    '''decimal_sep : DECIMAL_LITERAL'''
    p[0] = ASTnode('decimal_number')
    p[0].value = p[1]

def p_statement(p):
    '''statement : forrangelist
                 | ifscalar
                 | assignment
                 | returnstatement
                 | cell_assign'''
    p[0] = p[1]

def p_returnstatement1(p):
    '''returnstatement : RETURN scalar_ranges_expr'''
    p[0] = ASTnode('return')
    p[0].child_expr = p[2]

def p_returnstatement2(p):
    '''returnstatement : RETURN IDENT'''
    p[0] = ASTnode('return')
    p[0].child_expr = p[2]

def p_scalar_ranges_expr(p):
    '''scalar_ranges_expr : scalar_expr
                          | range_expr'''
    p[0] = p[1]

def p_assignment1(p):
    '''assignment : scalar_ref ASSIGN loopvar'''
    p[0] = ASTnode('scalar_assign')
    p[0].child_var = p[1]
    p[0].child_expr = p[3]

def p_assignment2(p):
    '''assignment : scalar_ref ASSIGN simple_expr'''
    p[0] = ASTnode('scalar_assign')
    p[0].child_var = p[1]
    p[0].child_expr = p[3]

def p_ifscalar1(p):
    '''ifscalar : IF if_condition THEN statement elsescalar ENDIF'''
    p[0] = ASTnode('if_stmt')
    p[0].child_condition = p[2]
    p[0].children_then_stmts = [p[4]]
    p[0].children_else_stmts = [p[5]]

def p_ifscalar2(p):
    '''ifscalar : IF if_condition THEN statement ENDIF'''
    p[0] = ASTnode('if_stmt')
    p[0].children_condition = [p[2]]
    p[0].children_then_stmts = [p[4]]
    p[0].children_else_stmts = []

def p_if_condition1(p):
    '''if_condition : loopvar LT scalar_ref'''
    p[0] = ASTnode('oper ' + p[2])
    p[0].child_left = p[1]
    p[0].child_right = p[3]

def p_if_condition2(p):
    '''if_condition : loopvar GT scalar_ref'''
    p[0] = ASTnode('oper ' + p[2])
    p[0].child_left = p[1]
    p[0].child_right = p[3]

def p_elsescalar(p):
    '''elsescalar : ELSE ifscalar'''
    p[0] = p[2]

# '''forrangelist : FOR range_list DO statement_list DONE
#                     | FOR many_range_expr DO statement_list DONE'''

def p_forrangelist1(p):
    '''forrangelist : FOR'''
    p[0] = ASTnode('for_stmt')
    p[0].children_ranges = []
    p[0].children_stmts = []

def p_forrangelist2(p):
    '''forrangelist : forrangelist range_list
                    | forrangelist many_range_expr'''
    p[0] = p[1]
    p[0].children_ranges.append(p[2])

def p_forrangelist3(p):
    '''forrangelist : forrangelist DO'''
    p[0] = p[1]

def p_forrangelist4(p):
    '''forrangelist : forrangelist statement'''
    p[0] = p[1]
    p[0].children_stmts.append(p[2])

def p_forrangelist5(p):
    '''forrangelist : forrangelist DONE'''
    p[0] = p[1]

def p_scalar_ref(p):
    '''scalar_ref : get_ident'''
    p[0] = ASTnode('scalar_ref')
    p[0].child_name = p[1]

def p_loopvar(p):
    '''loopvar : DOLLAR'''
    p[0] = ASTnode('loopvar')
    p[0].child_range_selector = None

def p_cell_assign(p):
    '''cell_assign : loopvar ASSIGN scalar_ref'''
    p[0] = ASTnode('cell_assign')
    p[0].child_cell = p[1]
    p[0].child_expr = p[3]

def p_print_scalar1(p):
   '''print_scalar : PRINT_SCALAR infostrings scalar_ref'''
   p[0] = ASTnode('print_scalar')
   p[0].child_infostr = p[2]
   p[0].child_expr = p[3]

def p_print_scalar2(p):
   '''print_scalar : PRINT_SCALAR infostrings atom'''
   p[0] = ASTnode('print_scalar')
   p[0].child_infostr = p[2]
   p[0].child_expr = p[3]

def p_print_scalar3(p):
   '''print_scalar : PRINT_SCALAR infostrings simple_expr'''
   p[0] = ASTnode('print_scalar')
   p[0].child_infostr = p[2]
   p[0].child_expr = p[3]

def p_print_scalar4(p):
   '''print_scalar : PRINT_SCALAR infostrings function_call'''
   p[0] = ASTnode('print_scalar')
   p[0].child_infostr = p[2]
   p[0].child_expr = p[3]

def p_print_sheet(p):
   '''print_sheet : PRINT_SHEET infostrings sheet_ref'''
   p[0] = ASTnode('print_sheet')
   p[0].child_infostr = p[2]
   p[0].child_expr = p[3]

def p_sheet_ref(p):
    '''sheet_ref : get_sheet_ident'''
    p[0] = ASTnode('sheet_ref')
    p[0].child_name = p[1]

def p_infostrings1(p):
   '''infostrings : INFO_STRING'''
   p[0] = ASTnode('infostring')
   p[0].value = p[1]

def p_infostrings2(p):
   '''infostrings : empty'''
   p[0] = p[1]

def p_many_range_expr(p):
    '''many_range_expr : range_expr
                       | COMMA range_expr
                       | COMMA IDENT'''
    p[0] = p[1]

def p_range_list1(p):
    '''range_list : range_expr commarangesexpr'''
    p[0] = p[1]

def p_range_list2(p):
    '''range_list : range_expr commarangesexpr commarangesexpr'''
    p[0] = p[1]

def p_commarangesexpr1(p):
    '''commarangesexpr : COMMA IDENT'''
    p[0] = p[2]

def p_commarangesexpr2(p):
    '''commarangesexpr : COMMA range_expr'''
    p[0] = p[2]

def p_commarangesexpr3(p):
    '''commarangesexpr : empty'''
    p[0] = p[1]

def p_range_expr1(p):
    '''range_expr : RANGE cell_ref DOTDOT cell_ref'''
    p[0] = ASTnode('range')
    p[0].child_coord1 = p[2]
    p[0].child_coord2 = p[4]

def p_range_expr2(p):
    '''range_expr : range_ref'''
    p[0] = p[1]

def p_cell_ref(p):
    '''cell_ref : get_sheet_ident SQUOTE get_coordinate_ident'''
    p[0] = ASTnode('cell_ref')
    p[0].child_name = p[1]
    p[0].child_coord = p[3]

def p_get_coordinate_ident(p):
    '''get_coordinate_ident : COORDINATE_IDENT'''
    p[0] = ASTnode('coord')
    p[0].value = p[1]

def p_function_call(p):
    '''function_call : get_func_ident LSQUARE arguments RSQUARE'''
    p[0] = ASTnode('function_call')
    p[0].child_name = p[1]
    p[0].children_args = [p[3]]

def p_arguments(p):
    '''arguments : arg_expr comma_argument_expr
                 | arg_expr'''
    p[0] = p[1]

def p_comma_argument_expr(p):
    '''comma_argument_expr : COMMA arg_expr'''
    p[0] = p[1]

def p_arg_expr(p):
    '''arg_expr : scalar_expr
                | range_expr
                | sheet_ref'''
    p[0] = p[1]

def p_range_definition(p):
    '''range_definition : RANGE get_range_ident another_equalrange'''
    p[0] = ASTnode('range_definition')
    p[0].child_name = p[2]
    p[0].child_init = p[3]

def p_another_equalrange(p):
    '''another_equalrange : EQ range_expr'''
    p[0] = p[2]

def p_range_ref(p):
    '''range_ref : get_range_ident'''
    p[0] = ASTnode('range_ref')
    p[0].child_name = p[1]

def p_get_range_ident(p):
    '''get_range_ident : RANGE_IDENT'''
    p[0] = ASTnode('RANGE_IDENT')
    p[0].value = p[1]

def p_subroutine_call(p):
    '''subroutine_call : get_func_ident LSQUARE arguments RSQUARE'''
    p[0] = ASTnode('subroutine_call')
    p[0].child_name = p[1]
    p[0].children_args = [p[3]]

def p_empty(p):
    '''empty : '''

# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print( 'syntax error @', p )
    raise SystemExit

parser = yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()

    outformat="unicode"
    if ns.treetype:
      outformat = ns.treetype

    if ns.who == True:
        # identify who wrote this
        print( '88888 Ahto Simakuutio' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexesPractice.lexer, debug=False)
        # Pretty print the resulting tree
        tree_print.treeprint(result, outformat)
