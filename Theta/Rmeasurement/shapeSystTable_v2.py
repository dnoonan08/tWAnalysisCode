#! /usr/bin/env python

import os, sys
import math
channels = ['','_emu','_mumu','_ee','_emu_ee','_emu_mumu','_ee_mumu']

ChanNames = ['emu/mumu/ee combination',
             'emu channel',
             'mumu channel',
             'ee channel',
             'emu/ee combination',
             'emu/mumu combination',
             'ee/mumu combination']

chanNum = 0

if len(sys.argv) == 2:
    chanNum = int(sys.argv[1])

print
print 'Results for ' + ChanNames[chanNum]
print

verbose = False

sortBy = 1

showSort = True


uncertainties = { 'JER':[0,0,0,'JER'],
                  'Q2':[0,0,0,'$Q^2$ scale'],
                  'JES':[0,0,0,'JES'],
                  'PU':[0,0,0,'Event pile up'],
                  'UnclusteredMET':[0,0,0,'\MET modeling'],
                  'DRDS':[0,0,0,'tW DR/DS scheme'],
                  'lepSF':[0,0,0,'Lepton identification'],
                  '(statistical)':[0,0,0,'Statistical'],
                  'LES':[0,0,0,'Lepton energy scale'],
                  'ttxs':[0,0,0,'\\ttbar cross section'],
                  'lumi':[0,0,0,'Luminosity'],
                  'PDF':[0,0,0,'PDF'],
                  'TopMass':[0,0,0,'Top quark mass'],
                  'Matching':[0,0,0,'ME/PS matching thresholds'],
                  'BtagSF':[0,0,0,'B-tagging data/MC scale factor'],
                  'ZjetSF':[0,0,0,'Z+jet data/MC scale factor'],
                  'TopPt':[0,0,0,'Top Pt Reweighting'],
                  'SpinCorr':[0,0,0,'\\ttbar Spin Correlations'], 
                  'beta':[0,0,0,'beta for other signal'], 
                 }

totalUnc = [0.,0.,0.]
crossSec = [0,0,0]
quadtotalUnc = [0.,0.,0.]

isTop = False
isAntiTop = False
isRvalue = False

condorOutLines = open("condor_output/condor_NewThetaRunTheta_"+str(chanNum)+".out",'r').readlines()

    
if len(condorOutLines) == 0:
    print "Not Finished"
else:
    for line in condorOutLines:
        if 'TW signal' in line:
            isTop = True
            isAntiTop = False
            isRvalue = False            
            errorIndex = 0
        if 'TbarW signal' in line:
            isTop = False
            isAntiTop = True
            isRvalue = False            
            errorIndex = 1
        if 'Ratio value' in line:
            isTop = False
            isAntiTop = False
            isRvalue = True
            errorIndex = 2
        if 'uncertainty due to' in line:
            syst = line.split()[3][:-1]
            if 'beta_' in syst:
                syst = 'beta'
            uncertainties[syst][errorIndex] = float(line.split()[-1])
        if 'shifts (plus/minus/absolute max.)' in line:
            uncertainties[line.split()[0]][errorIndex] = float(line.split(',')[-1])
        if 'central fit :' in line:
            totalUnc[errorIndex] = max(float(line.split()[-1]),float(line.split()[-2]))
            crossSec[errorIndex] = float(line.split()[-3])

uncList = list()
for i in uncertainties:
    uncList.append(uncertainties[i])

uncerts0 = sorted(uncList, key=lambda x: x[0], reverse=True)
uncerts1 = sorted(uncList, key=lambda x: x[1], reverse=True)
uncerts2 = sorted(uncList, key=lambda x: x[2], reverse=True)

for u in uncerts1:
    quadtotalUnc[0] += pow(u[0],2)
    quadtotalUnc[1] += pow(u[1],2)
    quadtotalUnc[2] += pow(u[2],2)

quadtotalUnc[0] = math.sqrt(quadtotalUnc[0])
quadtotalUnc[1] = math.sqrt(quadtotalUnc[1])
quadtotalUnc[2] = math.sqrt(quadtotalUnc[2])

print
print
print
print '\\begin{table*}'
print '  \\begin{center}'
print '    \caption {Systematic uncertainties extracted by fixing sources one at a time and measuring difference in cross section uncertainty.}'
print '    \label{tab:BDTSystShape}'
print '    \\begin{tabular}{| l | c | c |}'
print '    \hline'
print '                         & tW & & tbarW & & R \\\\'
print '  Systematic Uncertainty & $\Delta \sigma$ (pb) & $\\frac{\Delta \sigma}{\sigma}$ & $\Delta \sigma$ (pb) & $\\frac{\Delta \sigma}{\sigma}$ & $\Delta R$ \\\\'
print '    \hline'
# for i in uncertainties:
#     unc = uncertainties[i]
for unc in uncerts2:
    print '    %s & %.2f & %.0f%s & %.2f & %.0f%s & %.2f \\\\' % (unc[3], unc[0], unc[0]/crossSec[0]*100., '\%', unc[1], unc[1]/crossSec[1]*100., '\%', unc[2])
#    print ' ',unc[2],'&',unc[1]*22.2,'&',unc[1],'\\\\'
print '    \hline'
#print '    Total & %.2f & %.0f%s \\\\' % (totalUnc[1], totalUnc[1]/crossSec[1]*100., '\%')
print '    Total & %.2f & %.0f%s & %.2f & %.0f%s & %.2f \\\\' % (quadtotalUnc[0], quadtotalUnc[0]/crossSec[0]*100., '\%', quadtotalUnc[1], quadtotalUnc[1]/crossSec[1]*100., '\%', quadtotalUnc[2])
#print '    Total &',totalUnc[1]*22.2,'&',totalUnc[1],'\\\\'
print '    \hline'
print '    \end{tabular}'
print '  \end{center}'
print '\end{table*}'

