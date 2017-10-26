#!/usr/bin/env python

from readlogs import print_dict, read_logfile, most_recent_timestamp
from glob import glob
from os.path import split as ossplit
from collections import OrderedDict
from sys import exit

import argparse

parser = argparse.ArgumentParser(description=('Tabulate PyReshaper Logs (timing, rates, etc.)'))
parser.add_argument('-a', '--average', default=False, action='store_true', dest='use_average',
                    help=('Whether to average over different'))
parser.add_argument('-p', '--pattern', action='append', dest='patterns', metavar='PATTERN', default=[], 
                    help=('A pattern and optional name to give to each '
                          'group of logs.  Name and pattern should be comma-'
                          'separated, with the name coming first.'))
parser.add_argument('-t', '--title', default='', type=str, dest='title', metavar='TITLE',
                    help=('The title to use for both the timing and rate '
                          'plots.  This is pre-pended to the automatically '
                          'generated title.  It does not replace it.'))
parser.add_argument('-u', '--union', default=False, action='store_true', dest='use_union',
                    help=('Plot all data (union) versus only common elements'))
args = parser.parse_args()

named_logs = OrderedDict()
if len(args.patterns) > 0:
    for i, p in enumerate(args.patterns):
        patternids = p.split(',')
        if len(patternids) == 1:
            named_logs[patternids[0]] = glob(patternids[0])
        elif len(patternids) == 2:
            named_logs[patternids[0]] = glob(patternids[1])
        else:
            raise ValueError('Unrecognized pattern identifier: {0!r}'.format(p))
else:
    parser.print_help()
    print
    exit(0)

#===============================================================================
# Gather and print data found in logs:

database = OrderedDict()
for name, logfiles in named_logs.iteritems():
    database[name] = OrderedDict()
    for logfile in logfiles:
        toolname, testname, runname, hostname, timestamp, extension = ossplit(logfile)[1].split('.')
        if toolname != 'reshaper':
            continue
        if testname not in database[name]:
            database[name][testname] = OrderedDict()
        database[name][testname][timestamp] = read_logfile(logfile)
        database[name][testname][timestamp]['hostname'] = hostname

print
print_dict(database)

#===============================================================================
# Gather timing and rate data into a reduced dictionary

time_db = OrderedDict()
time_ids = {'Input': ('open input files', 'close input files', 'read time-invariant metadata',
                      'read time-variant metadata', 'read time-series variables'),
            'Output': ('open output files', 'close output files', 'write time-invariant metadata',
                      'write time-variant metadata', 'write time-series variables'),
            'Other': ()}
rate_db = OrderedDict()
for set_name, set_data in database.iteritems():
    for test_name, test_data in set_data.iteritems():
        
        # Average datasets across timestamps, or find most recent dataset
        if args.use_average:
            timestamp = test_data.keys()[0]
            volume = test_data[timestamp]['volume[MB]']['requested data']
            vcount = 1
            tdict = test_data[timestamp]['time[sec]']
            tcounts = dict((k,1) for k in tdict.keys())
            for timestamp in test_data.keys()[1:]:
                for tkey, tval in test_data[timestamp]['time[sec]'].iteritems():
                    if tkey in tdict:
                        tdict[tkey] += tval
                        tcounts[tkey] += 1
                    else:
                        tdict[tkey] = tval
                        tcounts[tkey] = 1
                volume += test_data[timestamp]['volume[MB]']['requested data']
                vcount += 1
            for tkey, tval in tdict.iteritems():
                tdict[tkey] = float(tval) / tcounts[tkey]
            volume = volume / vcount
        else:
            timestamp = most_recent_timestamp(test_data.keys())
            volume = test_data[timestamp]['volume[MB]']['requested data']
            tdict = test_data[timestamp]['time[sec]']
        
        # Reduce the time data to specific categories
        tdict_reduced = OrderedDict((c,0.0) for c in time_ids)
        total_time = tdict['complete conversion process']
        start_index = tdict.keys().index('complete conversion process') + 1
        for tkey in tdict.keys()[start_index:]:
            tvalue = tdict[tkey]
            for tid in tdict_reduced:
                if tkey in time_ids[tid]:
                    tdict_reduced[tid] += tvalue
                    break
                elif tid == time_ids[-1]:
                    tdict_reduced[tid] += tvalue
        
        # Scale time data by fractions of total time
        sum_time = sum(tdict_reduced.values())
        sfact = total_time / sum_time
        for tkey in tdict_reduced:
            tdict_reduced[tkey] *= sfact

        # Save the time data by set name and test name
        if set_name not in time_db:
            time_db[set_name] = OrderedDict()
        time_db[set_name][test_name] = tdict_reduced
        
        # Compute the rate information
        if set_name not in rate_db:
            rate_db[set_name] = OrderedDict()
        rate_db[set_name][test_name] = OrderedDict()
        rate_db[set_name][test_name]['Input'] = volume / tdict_reduced['Input']
        rate_db[set_name][test_name]['Output'] = volume / tdict_reduced['Output']
        rate_db[set_name][test_name]['Combined'] = volume / total_time

print
print 'TIMES:'
print_dict(time_db)
print
print 'RATES:'
print_dict(rate_db)

#===============================================================================
# Compute the relative time data
if len(time_db) > 1:
    speedup_db = OrderedDict()
    set_name0 = time_db.keys()[0]
    set_data0 = time_db[set_name0]
    for set_name, set_data in time_db.items()[1:]:
        set_name1 = '{0}:{1}'.format(set_name, set_name0)
        for test_name, test_data in set_data.iteritems():
            if test_name in set_data0:
                if set_name1 not in speedup_db:
                    speedup_db[set_name1] = OrderedDict()
                if test_name not in speedup_db[set_name1]:
                    speedup_db[set_name1][test_name] = OrderedDict()
                value = sum(test_data.values())
                value0 = sum(set_data0[test_name].values())
                speedup_db[set_name1][test_name] = value0 / value 
    
    print
    print 'SPEEDUP:'
    print_dict(speedup_db)
