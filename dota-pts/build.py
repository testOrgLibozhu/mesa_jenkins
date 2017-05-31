#!/usr/bin/python

import sys
import os.path as path
sys.path.append(path.join(path.dirname(path.abspath(sys.argv[0])), ".."))
import build_support as bs

# 500 - intro
# 600 - pause
# 1540 - 2nd pause
# 1750 - menu
# 2100 unpause
# 2240 spiderweb
# 2310 - big spider
# 2450 - explosion
# 2493 - end
# 8:30 run time

bs.build(bs.ApiTracePerf("dota_pts.json"))
