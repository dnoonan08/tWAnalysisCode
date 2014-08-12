#!/usr/bin/env python                                                                                                                  

from ROOT import *

def separation(S, B):
    separation = 0

    if S.GetNbinsX() != B.GetNbinsX() or S.GetNbinsX() <= 0:
        print "Problem with bins"
        return -1

    if S.GetXaxis().GetXmin() != B.GetXaxis().GetXmin() or S.GetXaxis().GetXmax() != B.GetXaxis().GetXmax() or S.GetXaxis().GetXmax() <- S.GetXaxis().GetXmin():
        print "Problem"
        return -1

    nstep  = S.GetNbinsX()
    intBin = (S.GetXaxis().GetXmax() - S.GetXaxis().GetXmin())/nstep
    nS     = float(S.GetSumOfWeights()*intBin)
    nB     = float(B.GetSumOfWeights()*intBin)

    if nS > 0 and nB > 0 :
        for i in range(nstep):
            s = S.GetBinContent(i)/nS
            b = B.GetBinContent(i)/nB

            if (s+b) > 0:
                separation += 0.5*(s-b)*(s-b)/(s+b)
        separation *= intBin
    else:
        print "No entries in histogram"
        return -1
    
    return separation
