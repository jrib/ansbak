#!/usr/bin/env python
"""
format ansible output for humans and more
"""


import re
import sys
import collections


HEADER_success = re.compile('(?P<hostname>\S*) \| (?P<return_msg>\S*) \| rc=(?P<return_code>\S*) >>')
HEADER_failure = re.compile('(?P<hostname>\S*) \| (?P<return_msg>\S*) => {')


def main():
    results = collections.defaultdict(list)

    host = ''
    out = ''
    return_msg = ''
    rc = ''

    for line in sys.stdin:
        match_host = HEADER_success.match(line)
        if match_host:
            # new host
            # save output of previous host if any
            if host:
                key = (return_msg, rc, out)
                value = host
                results[key].append(value)
            # now set these values for the new host
            (host, return_msg, rc) = match_host.groups()
            out = ''
        else:
            match_fail = HEADER_failure.match(line)
            if match_fail:
                # new failed host
                # save output of previous host if any
                if host:
                    key = (return_msg, rc, out)
                    value = host
                    results[key].append(value)
                # now set these values for the new host
                (host, return_msg) = match_fail.groups()
                out = ''
            else:
                out += line

    # save output of last host
    if host:
        key = (return_msg, rc, out)
        value = host
        results[key].append(value)

    for (return_msg, rc, out), hostgroup in results.items():
        print('{hostgroup} | {return_msg} | rc={rc} >>'.format(
            hostgroup=','.join(hostgroup),
            return_msg=return_msg,
            rc=rc))
        print(out)


if __name__ == '__main__':
    main()
