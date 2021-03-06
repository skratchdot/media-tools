# -*- coding: utf-8 -*-

import argparse
import collections
import inspect
import json
import math
from matplotlib import pyplot as plt
import numpy as np
import os
from pprint import pprint
import sys
import time

# add parent directory to sys path to import relative modules
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)

from lib.io_utils import *
from lib.collection_utils import *
from lib.processing_utils import *
from loclib import *

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="tmp/loc/lc_pd_audio.csv", help="File generated by collect_metadata.py")
parser.add_argument('-pages', dest="INPUT_PAGES_FILES", default="output/loc/pd_audio/page_*.json", help="File pattern for json files downloaded from download_query.py")
parser.add_argument('-filter', dest="FILTER", default="", help="Filter string")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/lc_bd_audio_subset.csv", help="Output .csv file")
parser.add_argument('-probe', dest="PROBE", action="store_true", help="Just print details?")
a = parser.parse_args()

files, fieldNames, itemLookup, itemCount = getLocItemData(a)
fileCount = len(files)

if a.PROBE:
    sys.exit()

# Make sure output dirs exist
makeDirectories(a.OUTPUT_FILE)
writeCsv(a.OUTPUT_FILE, files, headings=fieldNames)
