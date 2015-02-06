#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: smartsort.py

import re

# using regex in verbose mode for readability/maintainability
p1_regex = re.compile(  # (e.g. '#10-24', '#0000-160')
    r"""
    ^             # beginning of string
    \#            # the pound symbol (must be escaped in re.VERBOSE mode)
    [0-9]{1,4}    # first integer (1-4 digits)
    -             # separator
    [0-9]{0,3}    # second integer (0-3 digits)
    $             # end of string
    """,
    re.UNICODE | re.VERBOSE)


p2_regex = re.compile(  # (e.g. '1/2"-13', '5/16"-24')
    r"""
    ^             # beginning of string
    [0-9]{1,2}    # numerator
    /             # fraction separator
    [0-9]{1,2}"   # denominator
    -             # separator
    [0-9]{1,2}    # integer (1-2 digits)
    $             # end of string
    """,
    re.UNICODE | re.VERBOSE)


p3_regex = re.compile(  # (e.g. 'M.5-0.125', 'M6-1')
    r"""
    ^             # beginning of string
    M             # M (metric size)
    \d*\.?\d*     # first float number
    -             # separator
    \d*\.?\d*     # second float number
    $             # end of string
    """,
    re.UNICODE | re.VERBOSE)


def p1_sort_key(i):
    """
    Sort function for pattern 1 (e.g. '#10-24', '#0000-160')
    Sort by first int, then second int.
    """
    a, b = i.split('-')
    a = int(a.lstrip('#'))
    b = int(b)
    return (a, b)


def p2_sort_key(i):
    """
    Sort function for pattern 2 (e.g. '1/2"-13', '5/16"-24')
    Sort first by fraction, then the second integer.
    """
    a, b = i.split('-')
    a1, a2 = a.split('/')
    a2 = a2.rstrip('"')
    a1 = int(a1)
    a2 = int(a2)
    a = 1.0 * a1 / a2
    b = int(b)
    return (a, b)


def p3_sort_key(i):
    """
    Sort function for pattern 3 (e.g. 'M1.1-0.25', 'M6-1')
    Sort by the first float, then second float.
    """
    i = i.lstrip('M')
    a, b = i.split('-')
    a = float(a)
    b = float(b)
    return (a, b)


def smart_sort(input_list):
    """
    Smart Sort the input list. Returns a
    dictionary with two lists, keyed by 'matched' and 'unmatched'.
    """

    # temporary variables used for a smart sort
    p1_list = []
    p2_list = []
    p3_list = []
    unmatched_list = []

    # put each value in the appropriate list
    for item in input_list:
        if re.match(p1_regex, item):
            p1_list.append(item)
        elif re.match(p2_regex, item):
            p2_list.append(item)
        elif re.match(p3_regex, item):
            p3_list.append(item)
        else:
            unmatched_list.append(item)

    # sort each pattern/list
    patterns_and_keys = [(p1_list, p1_sort_key), (p2_list, p2_sort_key),
                         (p3_list, p3_sort_key)]

    # prepare sorted lists to be returned
    matched_list = []
    for p, k in patterns_and_keys:
        if p:  # only process a pattern if its list is not empty
            p.sort(key=k)
            matched_list.extend(p)

    if unmatched_list:
        # there were some unmatched values; default sort them
        unmatched_list.sort(key=None)

    return_dict = {}
    return_dict['matched'] = matched_list
    return_dict['unmatched'] = unmatched_list

    return return_dict


test_data_string = """#00-120
#00-90
#00-80
#1-20
#10-16
1/4"-20
3/8"-16
5/16"-18
1/2"-12
M.5-0.125
M.6-0.15
M1.1-.5
M10-1.5
M2.5-0.45
1 invalid data
2 should appear
3 at the end"""
