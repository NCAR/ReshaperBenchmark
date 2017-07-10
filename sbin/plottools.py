"""
General Plotting Tools
"""

from readlogs import dict_to_array
from matplotlib import pyplot as plt
from itertools import cycle

import numpy as np


#===============================================================================
# Standardized plot title format

def make_title(textlist, pretext='', posttext=''):
    titleroot = ' v '.join(textlist)
    titlelist = []
    if len(pretext) > 0:
        titlelist.append(pretext)
    titlelist.append(titleroot)
    if len(posttext) > 0:
        titlelist.append(posttext)
    return ' '.join(titlelist)

#===============================================================================
# Standardized plot filename format

def make_filename(textlist, pretext='', posttext=''):
    titleroot = '_v_'.join(textlist)
    titlelist = []
    if len(pretext) > 0:
        titlelist.append(pretext)
    titlelist.append(titleroot)
    if len(posttext) > 0:
        titlelist.append(posttext)
    return '{0}.pdf'.format('_'.join(titlelist))

#===============================================================================
# Stacked Bar Graph

def grouped_stacked_bar_graph(data_dict, max_width=0.8, pretitle='', 
                              title='', label='', union=False):

    data, dim_names = dict_to_array(data_dict, union=union)
    stack_names, group_names, categories = dim_names
    num_stacks, num_groups, num_categories = data.shape
    
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.725, 0.8])
    x_orig = np.arange(num_groups, dtype='d') + 0.25
    x_left = x_orig.copy()
    stack_width = max_width / num_stacks
    x_cntr = x_left.copy() + 0.5*stack_width
    for i in xrange(num_stacks):
        ic = cycle(['g', 'b', 'c', 'y', 'm', 'r', 'white'])
        y_base = np.zeros(num_groups, dtype='d')
        for j in xrange(num_categories):
            y_vals = data[i, :, j]
            if i == 0:
                ax.bar(x_left, y_vals, stack_width, bottom=y_base,
                       color=ic.next(), label=categories[j])
            else:
                ax.bar(x_left, y_vals, stack_width, bottom=y_base,
                       color=ic.next())
            y_base += y_vals
        for x,y in zip(x_cntr, y_base):
            ax.text(x, y, stack_names[i], fontsize=8,
                    verticalalignment='bottom', horizontalalignment='center')
        x_cntr += stack_width
        x_left += stack_width

    ax.set_ylabel(label)
    ax.set_title(make_title(stack_names, pretitle, title))
    ax.set_xticks(x_orig + 0.5*max_width)
    ax.set_xticklabels(group_names, rotation=15, ha='right')
    ax.set_xlim(0, max(x_left) + 0.25)
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), borderaxespad=0.3,
              prop={'size': 12})
    fig.savefig(make_filename(stack_names, pretitle, title))

#===============================================================================
# Nested Bar Graph

def grouped_nested_bar_graph(data_dict, max_width=0.8, pretitle='', 
                             title='', label='', union=False):

    data, dim_names = dict_to_array(data_dict, union=union)
    stack_names, group_names, categories = dim_names
    num_stacks, num_groups, num_categories = data.shape
    colors = ['g', 'b', 'c', 'y', 'm', 'r', 'white']
    y_min0 = np.min(data)
    y_max0 = np.max(data)
    
    fig = plt.figure()
    ax = fig.add_axes([0.11, 0.1, 0.675, 0.8])
    x_orig = np.arange(num_groups, dtype='d') + 0.25
    stack_width0 = max_width / num_stacks
    for i_x in xrange(num_groups):
        x_val = x_orig[i_x]
        x_cntr = x_val + 0.5*stack_width0
        for i_s in xrange(num_stacks):
            stack_width = stack_width0
            stack_dwidth = stack_width / (4*num_categories)
            x_val = x_orig[i_x] + i_s*stack_width0
            y_max = 0.0
            y_vals = [i for i in enumerate(data[i_s, i_x, :])]
            y_vals.sort(key=lambda x: x[1])
            y_vals.reverse()
            cat_indices = zip(*y_vals)[0]
            for i_c in cat_indices:
                y_val = data[i_s, i_x, i_c]
                if i_x == 0 and i_s == 0:
                    ax.bar(x_val, y_val, stack_width, color=colors[i_c],
                           label=categories[i_c])
                else:
                    ax.bar(x_val, y_val, stack_width, color=colors[i_c])
                stack_width = stack_width - 2*stack_dwidth
                x_val += stack_dwidth
                if y_val > y_max:
                    y_max = y_val
            ax.text(x_cntr, y_max, stack_names[i_s], fontsize=8,
                    verticalalignment='bottom', horizontalalignment='center')
            x_cntr += stack_width0

    ax.set_ylabel(label)
    ax.set_title(make_title(stack_names, pretitle, title))
    ax.set_xticks(x_orig + 0.5*max_width)
    ax.set_xticklabels(group_names, rotation=15, ha='right')
    ax.set_xlim(0, max(x_orig) + num_stacks*stack_width0 + 0.25)
    ax.set_ylim(0.5*y_min0, 2*y_max0)
    ax.set_yscale('log')
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), borderaxespad=0.3,
              prop={'size': 12})
    fig.savefig(make_filename(stack_names, pretitle, title))

#===============================================================================
# Nested Bar Graph

def grouped_bar_graph(data_dict, max_width=0.8, pretitle='', 
                      title='', label='', union=False):

    data, dim_names = dict_to_array(data_dict, union=union)
    stack_names, group_names = dim_names
    num_stacks, num_groups = data.shape
    colors = ['g', 'b', 'c', 'y', 'm', 'r', 'white']
    #y_min0 = np.min(data)
    #y_max0 = np.max(data)
    
    fig = plt.figure()
    ax = fig.add_axes([0.11, 0.1, 0.675, 0.8])
    x_orig = np.arange(num_groups, dtype='d') + 0.25
    stack_width0 = max_width / num_stacks
    for i_x in xrange(num_groups):
        x_val = x_orig[i_x]
        for i_s in xrange(num_stacks):
            x_val = x_orig[i_x] + i_s*stack_width0
            y_val = data[i_s, i_x]
            if i_x == 0:
                ax.bar(x_val, y_val, stack_width0, color=colors[i_s],
                       label=stack_names[i_s])
            else:
                ax.bar(x_val, y_val, stack_width0, color=colors[i_s])
            x_val += stack_width0

    ax.set_ylabel(label)
    ax.set_title(make_title(stack_names, pretitle, title))
    ax.set_xticks(x_orig + 0.5*max_width)
    ax.set_xticklabels(group_names, rotation=15, ha='right')
    ax.set_xlim(0, max(x_orig) + num_stacks*stack_width0 + 0.25)
    #ax.set_ylim(0.5*y_min0, 2*y_max0)
    #ax.set_yscale('log')
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0), borderaxespad=0.3,
              prop={'size': 12})
    fig.savefig(make_filename(stack_names, pretitle, title))
