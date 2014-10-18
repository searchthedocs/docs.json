# -*- coding: utf-8 -*-

import json
import logging
import requests

from pyquery import PyQuery

log = logging.getLogger(__name__)

"""
base_url = 'https://developer.mozilla.org'

url = "https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5"
json_url = url + "$json"
raw_url = url + "?raw"

json_obj = requests.get(json_url).json()
raw_html = requests.get(raw_url).content

canonical = {
    "title": json_obj['title'],
    "slug": json_obj['slug'],
    "url": base_url + json_obj['url'],
    "language": json_obj['locale'],
    "tags": json_obj['tags'],
    "translations": [],
    "content": raw_html,
}
for t in json_obj['translations']:
    canonical['translations'].append({t['locale']: base_url + t['url']})

print json.dumps(canonical, indent=4)
"""


def recurse_while_none(element):
    if element.text is None:
        return recurse_while_none(element.getchildren()[0])
    else:
        return element.text


url = "https://media.readthedocs.org/json/docs/latest/faq.fjson"
url = "http://docs.readthedocs.org/en/latest/faq.html"

data = requests.get(url).json()
headers = []
sections = []
content = ''
title = ''
body_content = ''
if 'current_page_name' in data:
    path = data['current_page_name']
else:
    log.error('Unable to index file due to no name %s' % url)
if 'toc' in data:
    for element in PyQuery(data['toc'])('a'):
        headers.append(recurse_while_none(element))
    if None in headers:
        log.error('Unable to index file headers for: %s' % url)
if 'body' in data:
    body = PyQuery(data['body'])
    body_content = body.text().replace(u'¶', '')
    # Section stuff from inside the body
    section_list = body('.section > h2')
    for num in range(len(section_list)):
        div = section_list.eq(num).parent()
        header = section_list.eq(num)
        title = header.text().replace(u'¶', '').strip()
        section_id = div.attr('id')
        content = div.html()
        sections.append({
            'id': section_id,
            'title': title,
            'content': content,
        })
        log.debug("(Search Index) Section [%s:%s]: %s" % (
            section_id, title, content))

else:
    log.error('Unable to index content for: %s' % url)
if 'title' in data:
    title = data['title']
    if title.startswith('<'):
        title = PyQuery(data['title']).text()
else:
    log.error('Unable to index title for: %s' % url)

canonical = {
    "title": title,
    "slug": path,
    "url": url,
    "language": "en",
    "tags": None,
    "translations": None,
    "content": body_content,
}

print json.dumps(canonical, indent=4)
