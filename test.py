# -*- coding: utf-8 -*-

__author__ = 'mayns'


def substr(a, b):
    if a == b:
        return True
    if len(a) < len(b):
        return False
    s = True
    ss = b
    for i in xrange(len(a)):
        print 'a[i]', a[i]
        for j in xrange(len(ss)):
            print 'ss[j]', ss[j]
            if a[i] == ss[j]:
                ss = ss[j+1:]
                s = True
                break
            else:
                s = False
                break
    return s

print substr('alice in wonderland lewis caroll', 'alice')