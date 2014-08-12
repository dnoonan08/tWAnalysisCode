#! /usr/bin/env python

import os,sys

useTheoryFixed = True

verbose = False

for arg in sys.argv[1:]:
    if '-notheory' in arg:
        useTheoryFixed = False
    if '-v' in arg:
        verbose = True

channels = ['','_emu','_mumu','_ee','_emu_ee','_emu_mumu','_ee_mumu']

Directories=['.']

sortBy = 1

showSort = True

fullList = list()

maxSigList = list()

crossSecList = list()
#crossSecListTheoryFixed = list()
crossSecListUp = list()
#crossSecListTheoryFixedUp = list()
crossSecListDown = list()
#crossSecListTheoryFixedDown = list()

for chanNum in range(len(channels)):
    chan = channels[chanNum]
    expectedSignificance=0.
    if chan == '':
        if verbose:
            print "emu/mumu/ee"
    else:
        if verbose:
            print chan[1:]

    if not os.path.exists("condor_output/condor_NewThetaRunTheta_"+str(chanNum)+".out"):
        if verbose:
            print '-'

        crossSecList.append(-5.)
        crossSecListUp.append(-5.)
        crossSecListDown.append(-5.)

    condorOutLines = open("condor_output/condor_NewThetaRunTheta_"+str(chanNum)+".out",'r').readlines()

    if len(condorOutLines) == 0:
        crossSecList.append(-10.)
        crossSecListUp.append(-10.)
        crossSecListDown.append(-10.)
        if verbose:
            print 'Not Finished'
        continue
    for line in condorOutLines:
        if line.startswith('central fit'):
            crossSection=line.split(':')[-1][:-1]

    if len(crossSection.split()) > 0:            
        crossSecList.append(round(float(crossSection.split()[0]),2))
        crossSecListUp.append(round(float(crossSection.split()[1]),2))
        crossSecListDown.append(round(float(crossSection.split()[2]),2))
    else:
        crossSecList.append(-1.)
        crossSecListUp.append(-1.)
        crossSecListDown.append(-1.)

print '\\begin{table*}'
print '\\begin{center}'
print '  \caption{Results of the fit of the BDT discriminant, split into individual channels.}'
print '  \label{tab:resultsSplitChannels}'
print '  \\begin{tabular}{| l | c |}'
print '  \hline'
print '  Channel & \\tWt (pb) \\\\'
print '  \hline'
print '  $e\mu/\mu\mu/ee$ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (crossSecList[0], crossSecListUp[0], crossSecListDown[0])
print '  \hline'
print '  $e\mu$           & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (crossSecList[1], crossSecListUp[1], crossSecListDown[1])
print '  $\mu\mu$         & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (crossSecList[2], crossSecListUp[2], crossSecListDown[2])
print '  $ee$             & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (crossSecList[3], crossSecListUp[3], crossSecListDown[3])
print '  \hline'
print '  $e\mu/ee$        & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (crossSecList[4], crossSecListUp[4], crossSecListDown[4])
print '  $e\mu/\mu\mu$    & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (crossSecList[5], crossSecListUp[5], crossSecListDown[5])
print '  $ee/\mu\mu$      & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (crossSecList[6], crossSecListUp[6], crossSecListDown[6])
print '  \hline'
print '  \end{tabular}'
print '\end{center}'
print '\end{table*}'
