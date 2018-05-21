# -*- coding: utf-8 -*-

import numpy as np
from sympy import symbols, roots, diff, poly, lambdify

def ballpath(xinit=0, yinit=0, vxinit=1, vyinit=1):
    x0val = xinit
    y0val = yinit
    v0xval = vxinit
    v0yval = vyinit
    
    # create symbolic exprs for ball path and intersection polynomial
    x0, y0, v0x, v0y, t = symbols('x0 y0 v0x v0y t')
    xt = x0 + v0x*t
    yt = y0 + v0y*t - (1/2)*9.8*(t**2)
    pgen = poly(xt**2 + yt**2 - 1, t)
    
    # create actual functions from symbolic exprs
    xtf = lambdify((t, x0, v0x), xt)
    ytf = lambdify((t, y0, v0y), yt)
    vytf = lambdify((t, v0y), diff(yt, t))
    
    while True:
        # subst current conditions into intersect poly
        p = pgen.subs({x0:x0val, y0:y0val, v0x:v0xval, v0y:v0yval})
        
        # solve for t
        rts = roots(p, t)
        rts = np.array([complex(r) for r in rts.keys()])
        tcol = np.min(rts[np.logical_and(rts > 0, np.imag(rts) == 0)]).real
        
        # find intersect point and speed at the moment
        xcol = xtf(tcol, x0val, v0xval)
        ycol = ytf(tcol, y0val, v0yval)
        vxcol = v0xval
        vycol = vytf(tcol, v0yval)
        vcol = np.array([[vxcol], [vycol]])
        
        # calculate speed vector after bounce
        alpha = np.arctan2(ycol, xcol) - np.arctan2(vycol, vxcol)
        R = np.array([[np.cos(2*alpha), -np.sin(2*alpha)], \
                      [np.sin(2*alpha),  np.cos(2*alpha)]])
        newv0 = R @ -vcol
        tvals = np.linspace(0, tcol, 100)
        xvals = xtf(tvals, x0val, v0xval)
        yvals = ytf(tvals, y0val, v0yval)
        
        yield (xvals.tolist(), yvals.tolist())
        
        x0val = xcol
        y0val = ycol
        v0xval = newv0[0].item()
        v0yval = newv0[1].item()
        
        

