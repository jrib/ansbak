#!/usr/bin/env python
"""
format ansible output for humans and more
"""


import re
import sys
import collections


HEADER = re.compile(r'(?P<hostname>\S*) \| (?P<return_msg>\S*) (?P<return_code>\| rc=\S* >>|=> {)')

def main(lines):
    results = collections.defaultdict(list)

    host = ''
    out = ''
    return_msg = ''
    rc = ''

    def sort_hostgroups(k):
        (key, hostgroups) = k
        return hostgroups

    def sort_return_msg(k):
        (key, hostgroups) = k
        (return_msg, rc, out) = key
        return return_msg

    for line in lines:
        m = HEADER.match(line)
        if m:
            # New host:
            # save output of previous host if any

            if host:
                key = (return_msg, rc, out)
                value = host

                # The key is the bits that might be common
                # between hosts, then we maintain a list of
                # hosts that match that key
                results[key].append(value)

            # Now set these values for the new host, so they can be
            # saved next time around
            (host, return_msg, rc) = m.groups()
            out = ''
        else:
            out += line

    # Save output of last host since we didn't capture it on the way
    # out
    if host:
        key = (return_msg, rc, out)
        value = host

        results[key].append(value)

    # Go back through the list of hostgroups, and sort each host entry
    # within each hostgroup (and convert list to string).  Don't worry
    # about the ANSI colour codes that might appear in front of each
    # host if you forced ansible colour output - they all sort the
    # same regardless
    for (return_msg, rc, out), hostgroup in results.items():
        key = (return_msg, rc, out)
        results[key] = ','.join(sorted(results[key]))

    # Sort each grouped output based on reverse status first (so
    # "UNREACHABLE!" comes out before "CHANGED"), then (already sorted
    # and comma-separated) hostgroup, second
    for i, ((return_msg, rc, out), hostgroup) in enumerate(sorted(sorted(results.items(), key=sort_hostgroups), key=sort_return_msg, reverse=True)):
        if i != 0:
            print('--------------------')

        print('{hostgroup} | {return_msg} {rc}'.format(
            hostgroup=hostgroup,
            return_msg=return_msg,
            rc=rc))
        print(out)


if __name__ == '__main__':
    main(sys.stdin)
