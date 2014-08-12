#! /usr/bin/env python

from os import listdir

from ROOT import TH1,TFile
from math import sqrt

def getStatUnc(channels, regions, samples, texString = False):
    """
    Takes in the root file that is the input to theta for the tW analysis, and the name of the histogram you want the statistical uncertainty for

    The last 3 arguments (channels, regions, samples) are lists used to get the histogram name (channelregion__sample)

    Returns the statistical uncertainty in that histogram as a 3 dimensional list, stats[sample][region][channel]
    if texString is True, the list is returned as as a string with '\pm' inserted before had (to be inserted in tex table)
    """

    fileList = listdir('.')

    for rootFileName in fileList:
        if '.root' and 'inputFileTheta' in rootFileName:
            fileName = rootFileName
            print fileName
            file = TFile(rootFileName, 'r')

    print file

#    stats  = {}
    stats = list()


    for s in range(len(samples)):
        stats.append(list())
        for r in range(len(regions)):
            stats[s].append(list())
            for c in range(len(channels)):
                stats[s][r].append(list())
                
                histoName = channels[c]+regions[r]+'__'+samples[s]
                print histoName
                hist = file.Get(histoName)
                print hist
                statUncSquared = 0.
                for bin in range(hist.GetNbinsX()):
                    statUncSquared += pow(hist.GetBinError(bin+1),2)
                
                if texString:
                    stats[s][r][c] = '$ \pm %.2f $' %(sqrt(statUncSquared)/hist.Integral())
                else:
                    stats[s][r][c].append(sqrt(statUncSquared)/hist.Integral())
            stats[s][r].append(list())
#                stats[histoName] = sqrt(statUncSquared)/hist.Integral()


    return stats
