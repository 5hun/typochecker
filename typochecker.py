#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import argparse
import glob

def is_typo(s1, s2, ud):
    ls1 = len(s1)
    ls2 = len(s2)
    mat = list([0]*(ls2+1) for i in range(ls1+1))
    for i in range(ls1+1):
        mat[i][0] = i
    for i in range(ls2+1):
        mat[0][i] = i
    for d in range(2, ls1+ls2+1):
        mind = d
        for i,j in ((i,d-i) for i in range(1, min(d, ls1)+1)
                    if d-i >= 1 and d-i <= ls2):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1
            mat[i][j] = min(mat[i-1][j] + 1,
                            mat[i][j-1] + 1,
                            mat[i-1][j-1] + cost)
            mind = min(mat[i][j], mind)
        if mind >= ud:
            return(False)
    return(mat[ls1][ls2] > 0)


def collect_typos(tokens, ud):
    ret = []
    for i in range(len(tokens)):
        tmp = [tokens[j] for j in range(i+1, len(tokens))
               if is_typo(tokens[i], tokens[j], ud)]
        if len(tmp) > 0:
            ret.append([tokens[i]] + tmp)
    return(ret)

def print_typos(typos):
    for lyst in typos:
        for x in lyst:
            print(x),
        print

def collect_tokenset(tokenre, filelist, minl):
    comp = re.compile(tokenre)
    ret = set([])
    for fn in filelist:
        with open(fn, 'r') as fin:
            ret |= set(tok for tok in comp.findall(fin.read())
                       if len(tok) >= minl)
    return(tuple(ret))

def main(tokenre, filelist, ud, minlen):
    tokens = collect_tokenset(tokenre, filelist, minlen)
    typos = collect_typos(tokens, ud)
    print_typos(typos)

def glob_argfiles(lyst):
    ret = set([])
    for s in lyst:
        ret |= set(glob.glob(s))
    return(ret)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check typos between tokens')
    parser.add_argument('-d', default=2, type=int, action='store',
                        help='if the edit distance between two tokens is less than D, it is regarded as typo (default: %(default)d)')
    parser.add_argument('-re', '-regexp', default='[A-Za-z_][A-Za-z0-9_]*', action='store',
                        help='regular expression (of Python) pattern for tokens (default: "%(default)s")')
    parser.add_argument('-l', '-minlen', default=1, type=int, action='store',
                        help='the minimum length of the target tokens')
    parser.add_argument('file', nargs='+', type=str,
                        help='file to check')
    args = parser.parse_args()
    main(args.re, glob_argfiles(args.file), args.d, minlen=args.l)
