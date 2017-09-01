"""
Read PyReshaper log files
"""

from collections import OrderedDict
from datetime import datetime

import numpy as np

#===============================================================================
# Print a dictionary

def print_dict(d, lvl=0):
    for k,v in d.iteritems():
        if isinstance(v, dict):
            print '{0}{1}:'.format('   '*lvl, k)
            print_dict(v, lvl=lvl+1)
        else:
            print '{0}{1}:  {2}'.format('   '*lvl, k, v)

#===============================================================================
# Function for finding most recent timestamp from dense string

def most_recent_timestamp(timestamps):
    dtstamps = map(lambda ts: datetime.strptime(ts, "%Y%m%d%H%M%S"),
                   timestamps)
    return max(dtstamps).strftime("%Y%m%d%H%M%S")

#===============================================================================
# Function for reading log files

def read_logfile(logfile):
    database = OrderedDict()
    
    flog = open(logfile)
    loglines = [line.strip() for line in flog.readlines()]
    flog.close()
    
    database['backend'] = 'unknown'
    database['compression'] = 'unknown'
    database['count'] = OrderedDict()
    for logline in loglines:
        if 'NetCDF I/O Backend' in logline:
            database['backend'] = logline.strip().split()[-1]
        elif 'NetCDF Compression' in logline:
            database['compression'] = logline.strip().split()[-1]
        elif 'Time-Invariant Metadata:' in logline:
            v_str = logline.strip().split('[')[-1].split(']')[0]
            v_list = [v.strip().split("'")[1] for v in v_str.split(',')]
            database['count']['time-inv-meta'] = len(v_list)
        elif 'Time-Variant Metadata:' in logline:
            v_str = logline.strip().split('[')[-1].split(']')[0]
            v_list = [v.strip().split("'")[1] for v in v_str.split(',')]
            database['count']['time-var-meta'] = len(v_list)
        elif 'Time-Series Variables:' in logline:
            v_str = logline.strip().split('[')[-1].split(']')[0]
            v_list = [v.strip().split("'")[1] for v in v_str.split(',')]
            database['count']['time-ser-vars'] = len(v_list)
        elif logline == 'TIMING DATA:':
            break

    strt_idx = loglines.index('TIMING DATA:') + 2
    end_idx = loglines.index('-'*50, strt_idx)
    timing_lines = loglines[strt_idx : end_idx]
    timing_data = OrderedDict((n.strip().lower(), float(t)) for n,t in
                              map(lambda s: s.split(':'), timing_lines))
    database['time[s]'] = timing_data
    
    strt_idx = loglines.index('BYTE COUNTS (MB):') + 2
    end_idx = loglines.index('-'*50, strt_idx)
    volume_lines = loglines[strt_idx : end_idx]
    volume_data = OrderedDict((n.strip().lower(), float(t)) for n,t in
                              map(lambda s: s.split(':'), volume_lines))
    database['volume[MB]'] = volume_data
    
    return database

#===============================================================================
# Compute the rank (max depth) of a nested dictionary

def get_dict_rank(d, depth=0):
    if isinstance(d, dict):
        return max(get_dict_rank(v, depth=depth+1) for v in d.itervalues())
    else:
        return depth

#===============================================================================
# Get the axes/dimension names from a nested dictionary

def fill_dict_names(d, names, depth=0, rank=None, union=False):
    if rank is None:
        rank = get_dict_rank(d)
    if isinstance(d, dict):
        if depth < rank-1:
            nset = list(k for (k,v) in d.iteritems()
                        if isinstance(v, dict))
        elif depth == rank-1:
            nset = list(k for (k,v) in d.iteritems()
                        if isinstance(v, (int, float)))
        if depth == len(names):
            names.append(nset)
        elif union:
            for n in nset:
                if n not in names[depth]:
                    names[depth].append(n)
        else:
            for n in names[depth]:
                if n not in nset:
                    names[depth].remove(n)
        if depth < rank-1:
            for v in d.itervalues():
                if isinstance(v, dict):
                    fill_dict_names(v, names, depth=depth+1,
                                    rank=rank, union=union)

#===============================================================================
# Check if data indicated by a list of keys exists in a nested dictionary

def keylist_in_data(d, keylist):
    if len(keylist) > 0:
        key = keylist[0]
        if key in d:
            return keylist_in_data(d[key], keylist[1:])
        else:
            return False
    else:
        return True

#===============================================================================
# Retrieve the data from a nested dictionary given a list of keys

def data_by_keylist(d, keylist):
    if len(keylist) > 0:
        return data_by_keylist(d[keylist[0]], keylist[1:])
    else:
        return d

#===============================================================================
# Compute a list of keys/names from a multi-dimensional array index

def keylist_by_index(dim_names, idx):
    return [dim_names[i][j] for i,j in enumerate(idx)]

#===============================================================================
# Compute data array from a data dictionary

def dict_to_array(data_dict, union=False, max_depth=None):

    rank = get_dict_rank(data_dict)
    if max_depth is not None and max_depth < rank:
        rank = max_depth

    dim_names = []
    fill_dict_names(data_dict, dim_names, union=union, rank=rank)

    dshape = tuple(len(n) for n in dim_names)
    data_array = np.zeros(dshape, dtype=np.float64)
    data_iter = np.nditer(data_array, flags=['multi_index'])
    while not data_iter.finished:
        keylist = keylist_by_index(dim_names, data_iter.multi_index)
        if keylist_in_data(data_dict, keylist):
            data_array[data_iter.multi_index] = data_by_keylist(data_dict, keylist)
        data_iter.iternext()

    return data_array, dim_names
