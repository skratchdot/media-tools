# -*- coding: utf-8 -*-

import argparse
from lib.collection_utils import *
from lib.io_utils import *
from lib.math_utils import *
from lib.text_utils import *
import os
from pprint import pprint
from string import Formatter
from string import Template
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="tmp/metadata.csv", help="Input metdata csv")
parser.add_argument('-sf', dest="SAMPLE_FILE", default="tmp/sampledata.csv", help="Input sampledata csv")
parser.add_argument('-tmpl', dest="TEMPLATE", default="${title}", help="Template for printing")
parser.add_argument('-sort', dest="SORT_BY", default="ntext", help="Either text for lastWord")
a = parser.parse_args()
aa = vars(a)
aa["TEMPLATE"] = a.TEMPLATE.strip()

_, meta = readCsv(a.INPUT_FILE)
_, samples = readCsv(a.SAMPLE_FILE)

# filter out meta that isn't in sampledata
ufilenames = set([s["filename"] for s in samples])
meta = [d for d in meta if d["filename"] in ufilenames]

keys = [ele[1] for ele in Formatter().parse(a.TEMPLATE) if ele[1]]
tmpl = Template(a.TEMPLATE)
lines = []
for d in meta:
    fvalues = dict([(key, d[key]) for key in keys])
    text = tmpl.substitute(fvalues)
    if len(text) > 0:
        lastWord = text.split()[-1]
        ntext = normalizeText(text)
        line = {
            "text": text,
            "ntext": ntext,
            "lastWord": lastWord
        }
        if a.SORT_BY not in line and a.SORT_BY in fvalues:
            line[a.SORT_BY] = fvalues[a.SORT_BY]
        lines.append(line)

# make unique based on text, then sort
lines = list({line["text"]:line for line in lines}.values())
lines = sorted(lines, key=lambda l: l[a.SORT_BY])

print("%s results" % len(lines))
print("===")
for line in lines:
    print(line["text"])
print("===")
