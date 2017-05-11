#!/usr/bin/env python
#===============================================================================
# Run a PyReshaper Benchmark Test
#===============================================================================

from glob import glob
from os import environ, getcwd
from os.path import join as joinpath, basename
from time import strftime
from sys import path

print 'Path:'
for p in path:
    print '   {}'.format(p)

TESTNAME = basename(getcwd())

RUNNAME  = environ['RUNNAME']
DEFLATE  = environ['DEFLATE']
HOSTNAME = environ['HOSTNAME']

from pyreshaper.specification import Specifier
from pyreshaper.reshaper import Reshaper

testspec = Specifier(infiles=glob(joinpath('input', '*.nc')),
                     ncfmt='netcdf4',
                     compression=int(DEFLATE),
                     prefix=joinpath('output', '{}.'.format(TESTNAME)),
                     suffix='.nc',
                     backend='netCDF4')
testspec.validate()

specname = '.'.join([TESTNAME, RUNNAME, HOSTNAME, strftime("%Y%m%d%H%M%S"), 's2s'])
testspec.write(specname)

reshaper = Reshaper(testspec, verbosity=5, wmode='o')
reshaper.convert()
reshaper.print_diagnostics()
