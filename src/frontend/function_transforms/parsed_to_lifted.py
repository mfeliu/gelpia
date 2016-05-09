#!/usr/bin/env python3

from lexed_to_parsed import *

import sys

    
# constants used in the expression
GLOBAL_CONSTANTS_LIST = list()
GLOBAL_INPUTS_LIST = list()

# read only list of supported ops
# base lists are taken from parser
binops = prefix_binary_functions + ['+', '-', '*', '/', 'ipow']
uniops = prefix_unary_functions + ['Neg']

def make_constant(exp):
    ''' Given a constant expression places it in the global const list
    and mutates it to represent that it is a constant '''
    # If the constant value is already in the list, don't recreate it
    try:
        i = GLOBAL_CONSTANTS_LIST.index(exp)
    except ValueError:
        i = len(GLOBAL_CONSTANTS_LIST)
        GLOBAL_CONSTANTS_LIST.append(exp[:])
    exp[0] = 'Const'
    exp[1] = i
    del exp[2:]


def lift_constants(exp):
    ''' Given an expression, recursively lifts constants from the expression,
    coalescing neighboring constants. Mutates the expression and returns True
    if the expression was completely constant '''
    if exp[0] == 'Input':
        if exp[1] not in GLOBAL_INPUTS_LIST:
            GLOBAL_INPUTS_LIST.append(exp[1])
        return False
    if exp[0] == 'Variable':
        return False
    if exp[0] in ['Interval', 'Float', 'Integer']:
        return True
    if exp[0] == 'Return':
        if lift_constants(exp[1]):
            make_constant(exp[1])
        return False
    if exp[0] == 'Assign':
        if lift_constants(exp[2]):
            make_constant(exp[2])
        lift_constants(exp[3])
        return False
    if exp[0] in binops:
        first = lift_constants(exp[1])
        second = lift_constants(exp[2])
        if first and second:
            return True
        if first:
            make_constant(exp[1])
        if second:
            make_constant(exp[2])
        return False
    if exp[0] in uniops:
        return lift_constants(exp[1])

    print("Error constant lifting '{}'".format(exp))
    sys.exit(-1)


def runmain():
    ''' Wrapper to allow constant lifter to run with direct
    command line input '''
    try:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            data = f.read()
    except IndexError:
        sys.stdout.write('Reading from standard input (type EOF to end):\n')
        data = sys.stdin.read()

    exp = parser.parse(data)
    lift_constants(exp)

    print(exp)
    print()
    print(list(enumerate(GLOBAL_INPUTS_LIST)))
    print()
    print(list(enumerate(GLOBAL_CONSTANTS_LIST)))



# On call run as a util, taking in text and printing the constant lifted version
if __name__ == "__main__":
    runmain()