#!/usr/bin/env python
"""
This script generates data for benchmarking tests

Copyright 2017, University Corporation for Atmospheric Research
See the LICENSE.rst file for details
"""

from argparse import ArgumentParser, ArgumentTypeError

#===================================================================================================
# commalist
#===================================================================================================
def commalist(arg):
    try:
        name, size_str = arg.split(',')
        size = int(size_str)
    except:
        raise ArgumentTypeError("Dimensions must be formatted as 'NAME,SIZE'")
    return name, size


#===================================================================================================
# Argument Parser
#===================================================================================================
__PARSER__ = ArgumentParser(description='Generate time-slice files for PyReshaper testing')
__PARSER__.add_argument('-d', '--dimensions', type=commalist, metavar='SIZE[,SIZE[,SIZE[...]]]',
                        default=[10,100,100,100], help='Size of dimensions')
__PARSER__.add_argument('-v', '--variables', type=commalist, metavar='SIZE[,SIZE[,SIZE[...]]]',
                        default=[5,10,15,20], help='Number of variables of each dimension size')


#===================================================================================================
# Commond-Line Interface
#===================================================================================================
def cli(argv=None):
    return __PARSER__.parse_args(argv)


#===================================================================================================
# main
#===================================================================================================
def main(argv=None):
    args = cli(argv)


#===================================================================================================
# Command-line Operation
#===================================================================================================
if __name__ == '__main__':
    main()