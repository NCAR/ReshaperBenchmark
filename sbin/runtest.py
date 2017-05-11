#!/usr/bin/env python
#===============================================================================
# Run a PyReshaper Benchmark Test
#===============================================================================

from glob import glob
from pyreshaper.specification import Specifier
from pyreshaper.reshaper import Reshaper
from os import environ, getcwd
from os.path import join as joinpath, basename
from time import strftime
import sys
sys.path.append(getcwd())

TESTNAME = basename(getcwd())

RUNNAME     = environ['RUNNAME']
DEFLATE     = environ['DEFLATE']
HOSTNAME    = environ['HOSTNAME']
INPUTDIR    = environ['INPUTDIR']
OUTPUTDIR   = environ['OUTPUTDIR']
NCIOBACKEND = environ['NCIOBACKEND']

testinit = __import__('testinit')

infiles = []
for pattern in testinit.INFILES:
    infiles.extend(glob(joinpath(INPUTDIR, testinit.INAME, pattern)))

testspec = Specifier(infiles=infiles,
                     ncfmt='netcdf4',
                     compression=int(DEFLATE),
                     prefix=joinpath(OUTPUTDIR, TESTNAME, testinit.PREFIX),
                     suffix=testinit.SUFFIX,
                     metadata=testinit.METADATA,
                     backend=NCIOBACKEND)
testspec.validate()

TIMESTAMP = strftime("%Y%m%d%H%M%S")
SPECNAME = TESTNAME.replace('-', '.', 1)
specname = '.'.join([SPECNAME, RUNNAME, HOSTNAME, TIMESTAMP, 'spec'])
testspec.write(specname)

reshaper = Reshaper(testspec, verbosity=5, wmode='o')
reshaper.convert()
reshaper.print_diagnostics()
