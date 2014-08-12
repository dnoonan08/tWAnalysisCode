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

observedList = list()
#observedListTheoryFixed = list()
observedListUp = list()
#observedListTheoryFixedUp = list()
observedListDown = list()
#observedListTheoryFixedDown = list()

expectedList = list()
#expectedListTheoryFixed = list()
expectedListUp = list()
#expectedListTheoryFixedUp = list()
expectedListDown = list()
#expectedListTheoryFixedDown = list()

for chanNum in range(len(channels)):

    startedTheoryFixed = False

    maxSig = 0.
    
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
        observedList.append(-5.)
        observedListUp.append(-5.)
        observedListDown.append(-5.)
        expectedList.append(-5.)
        expectedListUp.append(-5.)
        expectedListDown.append(-5.)
        continue
    
    condorOutLines = open("condor_output/condor_NewThetaRunTheta_"+str(chanNum)+".out",'r').readlines()

    if len(condorOutLines) == 0:
        crossSecList.append(-10.)
        crossSecListUp.append(-10.)
        crossSecListDown.append(-10.)
        observedList.append(-10.)
        observedListUp.append(-10.)
        observedListDown.append(-10.)
        expectedList.append(-10.)
        expectedListUp.append(-10.)
        expectedListDown.append(-10.)
        if verbose:
            print 'Not Finished'
        continue
    for line in condorOutLines:
#         if "error while trying to execute " in line:
#             ex

        if "uncertainties not fitted:  [" in line:
            startedTheoryFixed = True

        if not useTheoryFixed:
            if not startedTheoryFixed:
                if line.startswith('expected'):
                    expectedSignificance=line.split(':')[-1][:-1]
                if line.startswith('observed'):
                    observedSignificance=line.split(':')[-1][:-1]
                if line.startswith('central fit'):
                    crossSection=line.split(':')[-1][:-1]
                if line.startswith('    observed_significance =') and '>~ ' in line:
                    maxSig = line.split('>~ ')[-1][:5]
                if line.startswith('    expected significance ') and '>~ ' in line:
                    maxSig = line.split('>~ ')[-1][:5]                    
        elif startedTheoryFixed:
            if line.startswith('expected'):
                expectedSignificance=line.split(':')[-1][:-1]
            if line.startswith('observed'):
                observedSignificance=line.split(':')[-1][:-1]
            if line.startswith('central fit'):
                crossSection=line.split(':')[-1][:-1]
            if line.startswith('    observed_significance =') and '>~ ' in line:
                maxSig = line.split('>~ ')[-1][:5]
            if line.startswith('    expected significance ') and '>~ ' in line:
                maxSig = line.split('>~ ')[-1][:5]

    if expectedSignificance == 0.0:
        crossSecList.append(-8.)
        crossSecListUp.append(-8.)
        crossSecListDown.append(-8.)
        observedList.append(-8.)
        observedListUp.append(-8.)
        observedListDown.append(-8.)
        expectedList.append(-8.)
        expectedListUp.append(-8.)
        expectedListDown.append(-8.)
    else:
        if len(crossSection.split()) > 0:            
            crossSecList.append(round(float(crossSection.split()[0]),2))
            crossSecListUp.append(round(float(crossSection.split()[1]),2))
            crossSecListDown.append(round(float(crossSection.split()[2]),2))
        else:
            crossSecList.append(-1.)
            crossSecListUp.append(-1.)
            crossSecListDown.append(-1.)

        if len(observedSignificance.split()) > 0:
            if 'inf' in observedSignificance.split()[0]:
                observedList.append(str(round(float(observedSignificance.split()[0]),2))+'(\geq'+str(round(float(maxSig),2))+")")
            else:
                observedList.append(round(float(observedSignificance.split()[0]),2))
            observedListUp.append(round(float(observedSignificance.split()[2]),2))
            observedListDown.append(round(float(observedSignificance.split()[2]),2))
        else:
            observedList.append(-5.)
            observedListUp.append(-5.)
            observedListDown.append(-5.)

        if len(expectedSignificance.split()) > 0:
            if 'inf' in expectedSignificance.split()[0]:
                expectedList.append(str(round(float(expectedSignificance.split()[0]),2))+'(\geq'+str(round(float(maxSig),2))+")")
#                expectedList.append('>~'+str(round(float(maxSig),2)))
            else:
                expectedList.append(round(float(expectedSignificance.split()[0]),2))
            expectedListDown.append(round(float(expectedSignificance.split('(')[-1].split()[0])-float(expectedSignificance.split()[0]),2))
            expectedListUp.append(round(float(expectedSignificance.split()[7])-float(expectedSignificance.split()[0]),2))
        else:
            expectedList.append(-5.)
            expectedListUp.append(-5.)
            expectedListDown.append(-5.)
            
    if verbose:
        print expectedSignificance


    





print '\\begin{table*}'
print '\\begin{center}'
print '  \caption{Results of the fit of the BDT discriminant, split into individual channels.}'
print '  \label{tab:resultsSplitChannels}'
print '  \\begin{tabular}{| l | c | c | c |}'
print '  \hline'
print '  Channel & Observed Significance & Expected & Cross Section (pb) \\\\'
print '  \hline'
print '  $e\mu/\mu\mu/ee$ & $ %s $ & $ %s^{%+.2f}_{%+.2f} $ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (observedList[0], expectedList[0], expectedListUp[0], expectedListDown[0], crossSecList[0], crossSecListUp[0], crossSecListDown[0])
print '  \hline'
print '  $e\mu$ & $ %s $ & $ %s^{%+.2f}_{%+.2f} $ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (observedList[1], expectedList[1], expectedListUp[1], expectedListDown[1], crossSecList[1], crossSecListUp[1], crossSecListDown[1])
print '  $\mu\mu$ & $ %s $ & $ %s^{%+.2f}_{%+.2f} $ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (observedList[2], expectedList[2], expectedListUp[2], expectedListDown[2], crossSecList[2], crossSecListUp[2], crossSecListDown[2])
print '  $ee$ & $ %s $ & $ %s^{%+.2f}_{%+.2f} $ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (observedList[3], expectedList[3], expectedListUp[3], expectedListDown[3], crossSecList[3], crossSecListUp[3], crossSecListDown[3])
print '  \hline'
print '  $e\mu/ee$ & $ %s $ & $ %s^{%+.2f}_{%+.2f} $ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (observedList[4], expectedList[4], expectedListUp[4], expectedListDown[4], crossSecList[4], crossSecListUp[4], crossSecListDown[4])
print '  $e\mu/\mu\mu$ & $ %s $ & $ %s^{%+.2f}_{%+.2f} $ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (observedList[5], expectedList[5], expectedListUp[5], expectedListDown[5], crossSecList[5], crossSecListUp[5], crossSecListDown[5])
print '  $ee/\mu\mu$ & $ %s $ & $ %s^{%+.2f}_{%+.2f} $ & $ %.1f^{%+.1f}_{%+.1f} $ \\\\' % (observedList[6], expectedList[6], expectedListUp[6], expectedListDown[6], crossSecList[6], crossSecListUp[6], crossSecListDown[6])
print '  \hline'
print '  \end{tabular}'
print '\end{center}'
print '\end{table*}'

print
print
print
