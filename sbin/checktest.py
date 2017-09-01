#!/usr/bin/env python
"""
This script checks the "sanity" of test output data

Copyright 2017, University Corporation for Atmospheric Research
See the LICENSE.rst file for details
"""

from argparse import ArgumentParser, ArgumentTypeError
from itertools import permutations
from netCDF4 import Dataset
from os.path import isfile, join

#===================================================================================================
# Argument Parser
#===================================================================================================
__PARSER__ = ArgumentParser(description='Check time-series files generated by PyReshaper testing')
__PARSER__.add_argument('-d', '--dimensions', metavar='SIZE[,SIZE[,SIZE[...]]]',
                        help='Size of dimensions to be written to files')
__PARSER__.add_argument('-n', '--numslices', metavar='NUMBER', default=100, type=int,
                        help='Number of time-slice files to write')
__PARSER__.add_argument('-o', '--outputdir', metavar='DIR', default='slices',
                        help='Directory where time-slice files should be written')
__PARSER__.add_argument('-p', '--prefix', metavar='PREFIX', default='slice.',
                        help='String prefix to all time-slice files generated')
__PARSER__.add_argument('-s', '--serial', default=False, action='store_true',
                        help='Whether to run the data generation in serial')
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
    args.dimensions = dimensions
    
    if args.variables is None:
        dims = sorted(args.dimensions)
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
                vdims = tuple(d for d in vtype[1:] if d in args.dimensions)
                for i in range(vnum):
                    vname = 'v{}'.format(n)
                    variables[vname] = vdims
                    n += 1
        except:
            raise ArgumentTypeError('Variables must be specified as a '
                                    'comma-separated list of integers')
    args.variables = variables     
        
    return args


#===================================================================================================
# main
#===================================================================================================
def main(argv=None):
    args = cli(argv)
    
    numslices = args.numslices
    dimensions = args.dimensions
    dimensions['0'] *= numslices
    variables = args.variables
    outdir = args.outputdir

    for vname in variables:
        fname = join(outdir, '{}{}.nc'.format(args.prefix, vname))
        if not isfile(fname):
            raise RuntimeError('Output file {} missing'.format(fname))
        
        with Dataset(fname) as fobj:
                
            for dname in variables[vname]:
                if dname not in fobj.dimensions:
                    raise RuntimeError('Dimension {} missing from file {}'.format(dname, fname))
                if len(fobj.dimensions[dname]) != dimensions[dname]:
                    raise RuntimeError('Dimension {} has size {} but expected {} in file {}'.format(dname, len(fobj.dimensions[dname]), dimensions[dname], fname))
                if dname not in fobj.variables:
                    raise RuntimeError('Coordinate variable {} missing in file {}'.format(dname, fname))
                if fobj.variables[dname].dimensions != (dname,):
                    raise RuntimeError('Coordinate variable {} has dimensions {} but expected {} in file {}'.format(dname, fobj.variables[dname].dimensions, (dname,), fname))

            if vname not in fobj.variables:
                raise RuntimeError('Variable {} missing in file {}'.format(dname, fname))
            if fobj.variables[vname].dimensions != variables[vname]:
                raise RuntimeError('Variable {} has dimensions {} but expected {} in file {}'.format(vname, fobj.variables[vname].dimensions, variables[vname], fname))


#===================================================================================================
# Command-line Operation
#===================================================================================================
if __name__ == '__main__':
    main()
