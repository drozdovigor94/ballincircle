# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import ballincircle

bp = ballincircle.ballpath(-0.5,0.5,1,1)

fig = plt.figure()
ax = fig.add_subplot(111)
circ = plt.Circle((0, 0), radius=1, edgecolor='k', facecolor='None', lw = 1)
ax.add_patch(circ)
ax.set_xlim(-1.25,1.25)
ax.set_ylim(-1.25,1.25)
ax.set_aspect('equal')

for i in range(4):
    xvals, yvals = next(bp)
    ax.plot(xvals, yvals)
