# -*- coding: utf-8 -*-

import argparse
import inspect
from matplotlib import pyplot as plt
import numpy as np
import os
from pprint import pprint
import sys

# add parent directory to sys path to import relative modules
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)

from lib.math_utils import *
from lib.io_utils import *

parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="projects/global_lives/data/ia_globallives_subset.csv", help="Input video csv file")
parser.add_argument('-single', dest="SINGLE", action="store_true", help="Display single line?")
a = parser.parse_args()

headings, rows = readCsv(a.INPUT_FILE)
collections = {}
labels = []
for i, r in enumerate(rows):
    dur = r["end"] - r["start"]
    start = r["start"] / 3600.0
    dur = dur / 3600.0
    collection = r["collection"]
    if collection in collections:
        collections[collection].append((start, dur))
    else:
        collections[collection] = [(start, dur)]
        labels.append(collection)

fig, ax = plt.subplots(figsize=(6,3))
colors = iter(plt.cm.prism(np.linspace(0,1,len(labels))))
for i, label in enumerate(labels):
    data = collections[label]
    color = next(colors)
    h = 0.8 if a.SINGLE else 0.8 / len(data)
    if a.SINGLE:
        ax.broken_barh(data, (i-0.4,h), color=color)
    else:
        for j, d in enumerate(data):
            ax.broken_barh([d], (i-0.4+h*j,h), color=color)

ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels)
ax.set_xlabel("time [hour]")
plt.tight_layout()
plt.show()
