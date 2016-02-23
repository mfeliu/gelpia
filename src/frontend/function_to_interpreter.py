#!/usr/bin/env python3

from function_utils import *
import sys as SYS
import random as R
import subprocess

ops_interpreter = {
    '+'      : '+',
    '-'      : '-',
    '*'      : '*',
    '/'      : '/',
    'pow'    : 'p',
}

funcs_interpreter = {
#    'abs' ommitted due to special handling in rewrite_interpreter
    'cos'    : 'cos',
    'exp'    : 'exp',
    'log'    : 'log',
    'Neg'    : 'neg',
    'sin'    : 'sin',
    'tan'    : 'tan',
}

INT_VARIABLES = None

def rewrite_interpreter(exp):
    if exp[0] == 'Input':
        return "i{} ".format(INT_VARIABLES[exp[1]])
    if exp[0] == 'Bound':
        return rewrite_interpreter(GLOBAL_NAMES[exp[1]])
    if exp[0] == 'Const':
        return "c{} ".format(exp[1])
    if exp[0] in ['Return']:
        return rewrite_interpreter(exp[1])
    if exp[0] == 'Assign':
        return rewrite_interpreter(exp[3])
    if exp[0] in ops_interpreter:
        return "{} {} o{}".format(rewrite_interpreter(exp[1]),
                                 rewrite_interpreter(exp[2]),
                                 ops_interpreter[exp[0]])
    if exp[0] in funcs_interpreter:
        return "{} f{}".format(rewrite_interpreter(exp[1]),
                              funcs_interpreter[exp[0]])
    if exp[0] == 'abs':
        return "{} fabs".format(rewrite_interpreter(exp[1]))
    if exp[0] == 'sqrt':
        return "{} fsqrt".format(rewrite_interpreter(exp[1]))
    if exp[0] == "ipow":
        c = GOBAL_CONSTANTS_LIST[exp[2][1]][1]
        return "{} p{}".format(rewrite_interpreter(exp[1]), c)
    print("Error rewriting_interpreter '{}'".format(exp))
    SYS.exit(-1)


def rewrite_int(exp, variables):
    global INT_VARIABLES
    INT_VARIABLES = variables
    return rewrite_interpreter(exp)

    
def runmain():
    ''' Wrapper to allow interpreter rewriter to run with direct
    command line input '''
    try:
        filename = SYS.argv[1]
        f = open(filename)
        data = f.read()
        f.close()
    except IndexError:
        SYS.stdout.write('Reading from standard input (type EOF to end):\n')
        data = SYS.stdin.read()

    exp = parser.parse(data)
    lift_constants(exp)
    consts = ["{} : {}".format(i, c) for i, c in
              enumerate(GLOBAL_CONSTANTS_LIST)]
    print("consts: [{}]".format('\n '.join(consts)))
    print("globals: ", GLOBAL_NAMES)
    print("expression: ", exp)
    print("intrepter_code: ", rewrite_interpreter(exp))
    
if __name__ == '__main__':
    runmain()
