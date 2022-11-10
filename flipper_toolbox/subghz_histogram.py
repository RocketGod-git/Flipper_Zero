#!/usr/bin/env python3
"""
    Peter Shipley github.com/evilpete

    Script to read Flipper SubGhz RAW File and plot 0 & 1 segment lengths using pyplot

    From pkg https://github.com/evilpete/flipper_toolbox

    Based heavily on jinscho's gist :
        https://gist.github.com/jinschoi/8396f25a4cb7ac7986a7d881026ae950
"""

import re
import sys
from statistics import mean, median_high
import pandas as pd
import matplotlib.pyplot as plt

# LIMIT = 1000      # this number is arbitrary
LIMIT = None      # If None, limit will be calculated from the median

_debug = 0

filename = sys.argv[1]

psegs = []
nsegs = []
with open(filename, 'r', encoding="utf-8") as fd:
    header = fd.readline().strip()
    if header != 'Filetype: Flipper SubGhz RAW File':
        print(f"Error: {filename} is not a 'Flipper SubGhz RAW File' sample file'")
        sys.exit(1)

    for line in fd:
        m = re.match(r'RAW_Data:\s*([-0-9 ]+)\s*$', line)
        if m:
            nsegs.extend(abs(int(seg)) for seg in m[1].split(r' ') if int(seg) < 0)
            psegs.extend(abs(int(seg)) for seg in m[1].split(r' ') if int(seg) > 0)

if _debug:
    print("nseg :", min(nsegs), mean(nsegs), max(nsegs))
    print("pseg :", min(psegs), mean(psegs), max(psegs))


limit = LIMIT
if limit is None:
    data_median = max(median_high(nsegs), median_high(psegs))
    limit = 4 * data_median
    print(f"Limit = median * 4 = {data_median} * 4 = {limit}")
    # max_dat = max(nsegs + psegs)
    # print("max =", max_dat)


pseries = pd.Series(data=psegs)
nseries = pd.Series(data=nsegs)

pseries = pseries[pseries < limit]
nseries = nseries[nseries < limit]

df = pd.DataFrame(pseries, columns=['pos'])
df['neg'] = nseries

ax = df.plot.hist(bins=int(limit / 4),
                  log=False,
                  alpha=0.5, figsize=(6, 3),
                  title='Histogram of segment length')

ax.set(xlabel='milliseconds')

ax.grid(True, which='major', axis='y')

plt.show()
