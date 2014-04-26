#!/usr/bin/python
#
# The top 100 name list is copied from
# http://www.babycenter.com/top-baby-names-2013, this code takes boy's
# name as example, it's same principle for girl's name.
#
# Usage:
#  python baby_name_trend.py

import sys

def GenerateNameRankFromFile(year, name_map):
    try:
        fn = 'boy/%d.txt' % year
        fp = open(fn)
    except IOError:
        print 'Can not open file: [%s]' % fn
        return

    idx = 1
    for line in fp.readlines():
        if line.find(' ') == -1:
            name = line.strip()
        else:
            name = line.split(' ')[-1].strip()
        if name not in name_map:
            name_map[name] = {}
        name_map[name][year] = idx
        idx += 1


def EvalName(year_rank_map):
    """Not implemented yet..."""
    return True


def GenTrend(year_rank_map):
    year_keys = year_rank_map.keys()
    year_keys.sort()
    prev = -1
    ret = []
    for year in year_keys:
        curr = year_rank_map[year]
        if prev != -1:
            if curr < prev:  # smaller is higher
                ret.append('/')
            elif curr == prev:
                ret.append('-')
            else:
                ret.append('\\')
        prev = curr

    return ''.join(ret)


def GenRank(year_rank_map):
    year_keys = year_rank_map.keys()
    year_keys.sort()
    prev = -1
    ret = []
    for year in year_keys:
        ret.append(' %3d (%d) ' % (year_rank_map[year], year))

    return ''.join(ret)


def main(args):
    name_years = range(2004, 2014)
    name_map = {}
    for year in name_years:
        GenerateNameRankFromFile(year, name_map)

    for name in name_map:
        for year in name_years:
            if year not in name_map[name]:
                name_map[name][year] = 200

    name_list = []
    for name in name_map:
        year_rank_map = name_map[name]
        if not EvalName(year_rank_map):
            continue
        rank_str = GenRank(year_rank_map)
        trend_str = GenTrend(year_rank_map)
        final_rank = year_rank_map[name_years[-1]]
        name_metadata = '%12s :  %s  %s' % (name, trend_str, rank_str)

        name_list.append((name_metadata, final_rank))

    name_list = sorted(name_list, key=lambda elem: elem[1])

    for elem in name_list:
        print '%3d  %s' % (elem[1], elem[0])


if __name__ == '__main__':
    main(sys.argv)
