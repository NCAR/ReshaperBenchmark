#!/usr/bin/env python
"""
This script runs the PyReshaper in a given test directory

Copyright 2017, University Corporation for Atmospheric Research
See the LICENSE.rst file for details
"""

from argparse import ArgumentParser
from glob import glob
from os.path import join as joinpath
from time import strftime
from sys import path
from asaptools import simplecomm
from pyreshaper.specification import Specifier
from pyreshaper.reshaper import Reshaper


#===================================================================================================
# Argument Parser
#===================================================================================================
__PARSER__ = ArgumentParser(description='Run a PyReshaper test')
__PARSER__.add_argument('--hostname', metavar='HOSTNAME', default='hostname',
                        help='Name of the host machine')
__PARSER__.add_argument('--runname', metavar='RUNNAME', default='runname',
                        help='Name of the run')
__PARSER__.add_argument('--testname', metavar='TESTNAME', default='testname',
                        help='Name of the test')
__PARSER__.add_argument('-d', '--deflate', metavar='DEFLATE', type=int, default=0,
                        help='Deflate value to use in PyReshaper run')
__PARSER__.add_argument('-o', '--outputdir', metavar='DIR', default='output',
                        help='Directory from where time-slice files should be read')
__PARSER__.add_argument('-i', '--inputdir', metavar='DIR', default='input',
                        help='Directory to where time-series files should be written')
__PARSER__.add_argument('-p', '--prefix', metavar='PREFIX', default='series.',
                        help='String prefix to all time-series files generated')
__PARSER__.add_argument('-s', '--suffix', metavar='SUFFIX', default='.nc',
                        help='String suffix to all time-series files generated')


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

    scomm = simplecomm.create_comm(serial=False)

    TESTNAME = args.testname    
    RUNNAME  = args.runname
    HOSTNAME = args.hostname
    DEFLATE  = args.deflate
    INDIR = args.inputdir
    OUTDIR = args.outputdir
    PREFIX = args.prefix
    SUFFIX = args.suffix
    
    testspec = Specifier(infiles=glob(joinpath(INDIR, '*.nc')),
                         ncfmt='netcdf4',
                         compression=DEFLATE,
                         prefix=joinpath(OUTDIR, PREFIX),
                         suffix=SUFFIX,
                         backend='netCDF4',
                         meta1d=True)
    testspec.validate()
    
    specname = '.'.join([TESTNAME, RUNNAME, HOSTNAME, strftime("%Y%m%d%H%M%S"), 's2s'])
    testspec.write(specname)
    
    reshaper = Reshaper(testspec, verbosity=5, wmode='o', simplecomm=scomm)
    reshaper.convert()
    reshaper.print_diagnostics()


#===================================================================================================
# Command-line Operation
#===================================================================================================
if __name__ == '__main__':
    main()
