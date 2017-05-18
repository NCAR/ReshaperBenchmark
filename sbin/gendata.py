#!/usr/bin/env python
"""
This script generates data for benchmarking tests

Copyright 2017, University Corporation for Atmospheric Research
See the LICENSE.rst file for details
"""

from argparse import ArgumentParser, ArgumentTypeError
from itertools import permutations
from netCDF4 import Dataset
from numpy import arange
from numpy.random import random_sample
from os.path import isdir, isfile, join
from os import makedirs
from asaptools import simplecomm
from time import time

#===================================================================================================
# Argument Parser
#===================================================================================================
__PARSER__ = ArgumentParser(description='Generate time-slice files for PyReshaper testing')
__PARSER__.add_argument('-c', '--chunk', metavar='DIM,SIZE', 
                        help='Dimension number and size of chunks to write')
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
    
    if args.chunk is None:
        chunk = ('3', 1)
    else:
        try:
            dim, size = args.chunk.split(',')
            chunk = (dim, int(size))
        except:
            raise ArgumentTypeError('Chunking must be set with a comma-separated '
                                    'dimension number and integer size')  
    args.chunk = chunk          
        
    return args


#===================================================================================================
# main
#===================================================================================================
def main(argv=None):
    args = cli(argv)
    
    dimensions = args.dimensions
    variables = args.variables
    numslices = args.numslices
    outdir = args.outputdir
    chunk = args.chunk
    
    scomm = simplecomm.create_comm(serial=args.serial)
    header = '[{}/{}]'.format(scomm.get_rank(), scomm.get_size())
    if scomm.is_manager():
        print 'Creating time-slice files in output directory: {}'.format(outdir)
        print 'MPI Environment Size: {}'.format(scomm.get_size())
        print
        if not isdir(outdir):
            makedirs(outdir)
    scomm.sync()
        
    myslices = scomm.partition(range(numslices), involved=True)

    tstart = time()
    for nslice in myslices:
        fname = join(outdir, '{}{}.nc'.format(args.prefix, nslice))
        if isfile(fname):
            print '{}: Overwriting file: {}'.format(header, fname)
        else:
            print '{}: Creating file: {}'.format(header, fname)

        with Dataset(fname, 'w', keepweakref=True) as fobj:
            fobj.setncattr('file', fname)
            fobj.setncattr('slice', str(nslice))
            
            for dname in dimensions:
                if dname == '0':
                    fobj.createDimension(dname)
                else:
                    fobj.createDimension(dname, dimensions[dname])

            for dname in dimensions:
                vobj = fobj.createVariable(dname, 'd', (dname,))
                vobj.setncattr('units', '1')
                vobj.setncattr('comment', 'Coordinate {}'.format(dname))
                dlen = dimensions[dname]
                if dname == '0':
                    vobj[:] = arange(nslice*dlen, (nslice+1)*dlen, dtype='d')
                else:
                    vobj[:] = arange(dlen, dtype='d')
            fobj.sync()
                
            vobjs = {}    
            for vname in variables:
                vdims = variables[vname]
                vtype = 'f' if len(vdims) > 1 else 'd'
                vobj = fobj.createVariable(vname, vtype, vdims)
                vobj.setncattr('units', '1')
                vobj.setncattr('comment', 'Variable {}'.format(vname))
                vobjs[vname] = vobj
            fobj.sync()

            for vname in vobjs:
                vobj = vobjs[vname]
                ndims = len(vobj.dimensions)
                if ndims == 0:
                    vobj[:] = 1.0
                elif ndims == 1:
                    vobj[:] = arange(dimensions[vobj.dimensions[0]], dtype='d')
                else:
                    cname = chunk[0]
                    if cname in vobj.dimensions:
                        cdlen = dimensions[cname]
                        csize = chunk[1]
                    else:
                        cdlen = 1
                        csize = 1

                    nchnks = cdlen / csize + int(cdlen % csize > 0)
                    for n in xrange(nchnks):
                        istart = n*csize
                        iend = cdlen if n == nchnks-1 else (n+1)*csize
                        slc = tuple(slice(istart,iend) if d == cname else slice(None)
                                    for d in vobj.dimensions)
                        shp = tuple(csize if d == cname else dimensions[d]
                                    for d in vobj.dimensions)
                        vobj[slc] = random_sample(shp)
                fobj.sync()

    tend = time()
    
    runtime = scomm.allreduce(tend - tstart, op='max')

    if scomm.is_manager():
        print
        print 'Maximum Process Runtime: {} seconds'.format(runtime)


#===================================================================================================
# Command-line Operation
#===================================================================================================
if __name__ == '__main__':
    main()
