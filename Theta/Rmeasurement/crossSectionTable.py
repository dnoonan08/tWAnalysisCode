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
#channels = ['','_emu','_mumu','_ee']

Directories=['.']

sortBy = 1

showSort = True

fullList = list()

maxSigList = list()

T_crossSecList = list()
T_crossSecListUp = list()
T_crossSecListDown = list()

Tbar_crossSecList = list()
Tbar_crossSecListUp = list()
Tbar_crossSecListDown = list()

R_valueList = list()
R_valueListUp = list()
R_valueListDown = list()

for chanNum in range(len(channels)):
    T_crossSection = ''
    Tbar_crossSection = ''
    R_value = ''

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

        T_crossSecList.append(-5.)
        T_crossSecListUp.append(-5.)
        T_crossSecListDown.append(-5.)
        Tbar_crossSecList.append(-5.)
        Tbar_crossSecListUp.append(-5.)
        Tbar_crossSecListDown.append(-5.)
        R_valueList.append(-5.)
        R_valueListUp.append(-5.)
        R_valueListDown.append(-5.)

    condorOutLines = open("condor_output/condor_NewThetaRunTheta_"+str(chanNum)+".out",'r').readlines()

    if len(condorOutLines) == 0:
        T_crossSecList.append(-10.)
        T_crossSecListUp.append(-10.)
        T_crossSecListDown.append(-10.)
        Tbar_crossSecList.append(-10.)
        Tbar_crossSecListUp.append(-10.)
        Tbar_crossSecListDown.append(-10.)
        R_valueList.append(-10.)
        R_valueListUp.append(-10.)
        R_valueListDown.append(-10.)
        if verbose:
            print 'Not Finished'
        continue

    isTop = False
    isAntiTop = False
    isRvalue = False
    for line in condorOutLines:
        if line.startswith('central fit :'):
            if isTop:
                T_crossSection=line.split(':')[-1][:-1]
            if isAntiTop:
                Tbar_crossSection=line.split(':')[-1][:-1]
            if isRvalue:
                R_value=line.split(':')[-1][:-1]
        if 'TW signal' in line:
            isTop = True
            isAntiTop = False
            isRvalue = False
        if 'TbarW signal' in line:
            isTop = False
            isAntiTop = True
            isRvalue = False
        if 'Ratio value' in line:
            isTop = False
            isAntiTop = False
            isRvalue = True

    if len(T_crossSection.split()) > 0 and len(Tbar_crossSection.split()) > 0:            
        T_crossSecList.append(round(float(T_crossSection.split()[0]),2))
        T_crossSecListUp.append(round(float(T_crossSection.split()[1]),2))
        T_crossSecListDown.append(round(float(T_crossSection.split()[2]),2))
        Tbar_crossSecList.append(round(float(Tbar_crossSection.split()[0]),2))
        Tbar_crossSecListUp.append(round(float(Tbar_crossSection.split()[1]),2))
        Tbar_crossSecListDown.append(round(float(Tbar_crossSection.split()[2]),2))
        R_valueList.append(round(float(R_value.split()[0]),2))
        R_valueListUp.append(round(float(R_value.split()[1]),2))
        R_valueListDown.append(round(float(R_value.split()[2]),2))
    else:
        T_crossSecList.append(-1.)
        T_crossSecListUp.append(-1.)
        T_crossSecListDown.append(-1.)
        Tbar_crossSecList.append(-1.)
        Tbar_crossSecListUp.append(-1.)
        Tbar_crossSecListDown.append(-1.)
        R_valueList.append(-1.)
        R_valueListUp.append(-1.)
        R_valueListDown.append(-1.)

print '\\begin{table*}'
print '\\begin{center}'
print '  \caption{Results of the fit of the BDT discriminant, split into individual channels.}'
print '  \label{tab:resultsSplitChannels}'
print '  \\begin{tabular}{ l  c c }'
print '  \hline'
print '  \hline'
print '  Channel & \\tWt (pb) & \\tWtbar (pb) & Ratio ($t/\bar{t})$\\\\'
print '  \hline'
print '  $e\mu/\mu\mu/ee$ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.2f^{%+.2f}_{%+.2f} $ \\\\' % (T_crossSecList[0], T_crossSecListUp[0], T_crossSecListDown[0], Tbar_crossSecList[0], Tbar_crossSecListUp[0], Tbar_crossSecListDown[0], R_valueList[0], R_valueListUp[0], R_valueListDown[0])
print '  \hline' 
print '  $e\mu$           & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.2f^{%+.2f}_{%+.2f} $ \\\\' % (T_crossSecList[1], T_crossSecListUp[1], T_crossSecListDown[1], Tbar_crossSecList[1], Tbar_crossSecListUp[1], Tbar_crossSecListDown[1], R_valueList[1], R_valueListUp[1], R_valueListDown[1])
print '  $\mu\mu$         & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.2f^{%+.2f}_{%+.2f} $ \\\\' % (T_crossSecList[2], T_crossSecListUp[2], T_crossSecListDown[2], Tbar_crossSecList[2], Tbar_crossSecListUp[2], Tbar_crossSecListDown[2], R_valueList[2], R_valueListUp[2], R_valueListDown[2])
print '  $ee$             & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.2f^{%+.2f}_{%+.2f} $ \\\\' % (T_crossSecList[3], T_crossSecListUp[3], T_crossSecListDown[3], Tbar_crossSecList[3], Tbar_crossSecListUp[3], Tbar_crossSecListDown[3], R_valueList[3], R_valueListUp[3], R_valueListDown[3])
print '  \hline'  
print '  $e\mu/ee$        & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.2f^{%+.2f}_{%+.2f} $ \\\\' % (T_crossSecList[4], T_crossSecListUp[4], T_crossSecListDown[4], Tbar_crossSecList[4], Tbar_crossSecListUp[4], Tbar_crossSecListDown[4], R_valueList[4], R_valueListUp[4], R_valueListDown[4])
print '  $e\mu/\mu\mu$    & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.2f^{%+.2f}_{%+.2f} $ \\\\' % (T_crossSecList[5], T_crossSecListUp[5], T_crossSecListDown[5], Tbar_crossSecList[5], Tbar_crossSecListUp[5], Tbar_crossSecListDown[5], R_valueList[5], R_valueListUp[5], R_valueListDown[5])
print '  $ee/\mu\mu$      & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.1f^{%+.1f}_{%+.1f} $ & $ %.2f^{%+.2f}_{%+.2f} $ \\\\' % (T_crossSecList[6], T_crossSecListUp[6], T_crossSecListDown[6], Tbar_crossSecList[6], Tbar_crossSecListUp[6], Tbar_crossSecListDown[6], R_valueList[6], R_valueListUp[6], R_valueListDown[6])
print '  \hline'
print '  \end{tabular}'
print '\end{center}'
print '\end{table*}'
