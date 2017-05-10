#!/usr/bin/env python
"""
This script generates data for benchmarking tests

Copyright 2017, University Corporation for Atmospheric Research
See the LICENSE.rst file for details
"""

from argparse import ArgumentParser, ArgumentTypeError
from itertools import permutations


#===================================================================================================
# Argument Parser
#===================================================================================================
__PARSER__ = ArgumentParser(description='Generate time-slice files for PyReshaper testing')
__PARSER__.add_argument('-d', '--dimensions', metavar='SIZE[,SIZE[,SIZE[...]]]',
                        help='Size of dimensions to be written to files')
__PARSER__.add_argument('-v', '--variables', action='append', metavar='NUM[,DIM[,DIM[...]]]',
                        help='Number of variables of a given dimensionality')


#===================================================================================================
# Commond-Line Interface
#===================================================================================================
def cli(argv=None):
    args = __PARSER__.parse_args(argv)
    
    if args.dimensions is None:
        dimensions = {'0': 10, '1': 1000}
    elif args.dimensions == '':
        raise ArgumentTypeError('Dimensions must be specified as a '
                                'comma-separated list of integers')
    else:
        try:
            dimensions = {str(i):int(s) for i,s in enumerate(args.dimensions.split(','))}
        except:
            raise ArgumentTypeError('Dimensions must be specified as a '
                                    'comma-separated list of integers')
    
    if args.variables is None:
        dims = sorted(dimensions)
        variables = {}
        n = 0
        for i in range(len(dims)):
            for vdims in permutations(dims, i+1):
                vname = 'v{}'.format(n)
                variables[vname] = tuple(vdims)
                n += 1
    elif args.variables == '':
        raise ArgumentTypeError('Variables must be specified as a '
                                'comma-separated list of integers')
    else:
        try:
            n = 0
            variables = {}
            for varg in args.variables:
                vtype = varg.split(',')
                vnum = int(vtype[0])
                vdims = tuple(d for d in vtype[1:] if d in dimensions)
                for i in range(vnum):
                    vname = 'v{}'.format(n)
                    variables[vname] = vdims
                    n += 1
        except:
            raise ArgumentTypeError('Variables must be specified as a '
                                    'comma-separated list of integers')
        
    return dimensions, variables


#===================================================================================================
# main
#===================================================================================================
def main(argv=None):
    dimensions, variables = cli(argv)
    
    print dimensions
    print variables


#===================================================================================================
# Command-line Operation
#===================================================================================================
if __name__ == '__main__':
    main()
