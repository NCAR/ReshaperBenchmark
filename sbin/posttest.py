#!/usr/bin/env python
"""
This script runs "post-test" analysis to display timing and throughput numbers

Copyright 2017, University Corporation for Atmospheric Research
See the LICENSE.rst file for details
"""

from argparse import ArgumentParser
from readlogs import read_logfile

#===================================================================================================
# Argument Parser
#===================================================================================================
__PARSER__ = ArgumentParser(description='Post-process a PyReshaper logfile for timing and throughput information')
__PARSER__.add_argument('logfile', metavar='LOGFILE',
                        help='Name of PyReshaper logfile to post-process')


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
    logdb = read_logfile(args.logfile)
    time = logdb['time[sec]']['complete conversion process']
    volume = logdb['volume[MB]']['requested data']
    thruput = volume / time
    print '  Processed {} MB in {} sec ({} MB/sec).'.format(volume, time, thruput)


#===================================================================================================
# Command-line Operation
#===================================================================================================
if __name__ == '__main__':
    main()
