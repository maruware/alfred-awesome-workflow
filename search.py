#!/usr/bin/python
# encoding: utf-8

import sys
import re

from workflow import Workflow

import urllib2

def get_awesome_md():
    url = 'https://raw.githubusercontent.com/sindresorhus/awesome/master/readme.md'
    res = urllib2.urlopen(url)
    text = res.read()
    return text

def main(wf):
    args = wf.args
    query = args[0]


    awesome_md = wf.cached_data('awesome_md', get_awesome_md, max_age=180)
    lines = awesome_md.splitlines()
    pattern = re.compile('- \[(.+)\]\((.+)\)')
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if not m:
            continue

        name = m.group(1).decode('utf-8')
        url = m.group(2).decode('utf-8')

        if url.find(u'https://') < 0:
            continue

        name_l = name.lower()
        query_l = query.lower()

        if name_l.find(query_l) > -1:
            wf.add_item(name, url, arg=url, uid=unicode(i), valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    sys.exit(wf.run(main))