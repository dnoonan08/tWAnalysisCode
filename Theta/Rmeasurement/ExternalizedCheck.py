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


uncertainties = { 'Q2':[0,0,0,0,'$Q^2$ scale'],
                  'DRDS':[0,0,0,0,'tW DR/DS scheme'],
#                  'PDF':[0,0,0,0,'PDF'],
                  'TopMass':[0,0,0,0,'Top quark mass'],
                  'Matching':[0,0,0,0,'ME/PS matching thresholds'],
                  }

totalUnc = [0.,0.,0.,0.]
OtherUnc = [0.,0.,0.,0.]

for i in range(4):
    TheoryFixed = False

    condorOutLines = open("condor_output/condor_NewThetaRunTheta_"+str(i)+".out",'r').readlines()
    
    if len(condorOutLines) == 0:
        print "Not Finished"
    else:
        for line in condorOutLines:
            if "uncertainties not fitted:  [" in line:
                TheoryFixed = True
            if 'quadratically added uncertainty' in line:
                if TheoryFixed:
                    totalUnc[i] = float(line.split(':')[-1].split()[0])
                    OtherUnc[i] = float(line.split(':')[-1].split()[0])
            if TheoryFixed:
                if 'shifts (plus/minus/absolute max.)' in line:
                    uncertainties[line.split()[0]][i] = float(line.split(',')[-1])/22.2
                if 'total additional uncertaitnty from fixed parameters:' in line:
                    percUnc = float(line.split()[-1])/22.2
                    totalUnc[i] = math.sqrt(totalUnc[i]*totalUnc[i] + percUnc*percUnc)
    
    
uncList = list()
for i in uncertainties:
    uncList.append(uncertainties[i])

uncerts1 = sorted(uncList, key=lambda x: x[0], reverse=True)


# print 'Theory Included'
# print
# print
# print '\\begin{table*}'
# print '\\begin{center}'
# print '  \caption {Systematic uncertainties extracted by fixing sources one at a time and measuring difference in cross section uncertainty.}'
# print '  \label{tab:BDTSystShape}'
# print '  \\begin{tabular}{| l | c | c |}'
# print '  \hline'
# print '  Systematic Uncertainty & $\Delta \sigma$ (pb) & $\\frac{\Delta \sigma}{\sigma}$ \\\\'
# print '  \hline'
# # for i in uncertainties:
# #     unc = uncertainties[i]
# for unc in uncerts1:
#     print ' ',unc[2],'&',unc[0]*22.2,'&',unc[0],'\\\\'
# print '  \hline'
# print '  Total &',totalUnc[0]*22.2,'&',totalUnc[0],'\\\\'
# print '  \hline'
# print '  \end{tabular}'
# print '\end{center}'
# print '\end{table*}'

print
print
print 'Theory Externalized'
print
print
print '\\begin{table*}'
print '  \\begin{center}'
print '    \caption {Systematic uncertainties extracted by fixing sources one at a time and measuring difference in cross section uncertainty.}'
print '    \label{tab:BDTSystShape}'
print '    \\begin{tabular}{| l | c | c | c | c |}'
print '    \hline'
print '    Systematic Uncertainty & $e\mu/\mu\mu/ee$ & $e\mu$ & $\mu\mu$ & $ee$ \\\\'
print '    \hline'
for unc in uncerts1:
    print '    %s & %.2f & %.2f & %.2f & %.2f \\\\' % (unc[4], unc[0]*22.2, unc[1]*22.2, unc[2]*22.2, unc[3]*22.2)
print '    Other & %.2f & %.2f & %.2f & %.2f \\\\' % (OtherUnc[0]*22.2,OtherUnc[1]*22.2,OtherUnc[2]*22.2,OtherUnc[3]*22.2)
print '    \hline'
print '    Total & %.2f & %.2f & %.2f & %.2f \\\\' % (totalUnc[0]*22.2,totalUnc[1]*22.2,totalUnc[2]*22.2,totalUnc[3]*22.2)
print '    \hline'
print '    \end{tabular}'
print '  \end{center}'
print '\end{table*}'

