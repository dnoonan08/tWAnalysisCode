#! /usr/bin/env python

#pulls the rate systematics from the tables in the index.html outputs from theta

import os
from math import sqrt

from getStatUnc import *

RateSysts = dict()
RateLevel = dict()

condorOutLines = open("analysisJochenSyst8TeVRunTheta/index.html",'r').readlines()

region = -1
mode = -1

systList = list()

regionList = ['1j1t','2j1t','2j2t']
#regionList = ['1j1t','2j1t','2j2t','2plusjets1plustag','3plusjets1plustag','2j0t']

dictMade = False
if len(condorOutLines) == 0:
    print "Not Finished"
else:
    for line in condorOutLines:
        if '<h2>Observable ' in line:
            for i in range(len(regionList)):
                if regionList[i] in line:
                    region = i
#             if regionList[0] in line:
#                 region = 0
#             elif regionList[1] in line:
#                 region = 1
#             elif regionList[2] in line:
#                 region = 2

            if 'emu' in line:
                mode = 0
            elif 'mumu' in line:
                mode = 1
            elif 'ee' in line:
                mode = 2
#            print region, mode
        if not dictMade and '<tr><th>process / nuisance parameter</th><th>' in line:
            for s in line.split('</th><th>')[1:]:
                systList.append(s.split()[0])
                tempList = list()
                for i in range(len(regionList)):
                    tempList.append([0,0,0,0])
#                print tempList
                RateSysts[s.split()[0]] = list()
                RateLevel[s.split()[0]] = list()
                
                RateSysts[s.split()[0]].append(tempList[:])
                RateSysts[s.split()[0]].append(tempList[:])
                RateSysts[s.split()[0]].append(tempList[:])

                RateLevel[s.split()[0]].append(tempList[:])
                RateLevel[s.split()[0]].append(tempList[:])
                RateLevel[s.split()[0]].append(tempList[:])
#                 RateSysts[s.split()[0]] = [[[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
#                 RateLevel[s.split()[0]] = [[[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0]],[[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
            dictMade = True

        if '<tr><td>other</td><td><sup>' in line:
#            print mode,region
            vals = line.split('</td><td>')[1:]
            vals[-1] = vals[-1].split('</td></tr>')[0]
            for v in range(len(vals)):                
                value = vals[v]
                if '---' in value:
                    RateSysts[systList[v]][2][region][mode] = '-'
                    RateLevel[systList[v]][2][region][mode] = 0.
                if '</sup><sub>' in value:
                    up = value.split('</sup><sub>')[0].split('<sup>')[-1]
                    down = value.split('</sup><sub>')[-1].split('</sub>')[0]
                    if '(s)' in value:                    
                        RateSysts[systList[v]][2][region][mode] = '$^{'+up+'}_{'+down+'}$'
                        RateLevel[systList[v]][2][region][mode] = max(float(up),float(down))
                    if '(r)' in value:
                        rate = (abs(float(up)) + abs(float(down)))/2.
                        RateSysts[systList[v]][2][region][mode] = '$\pm'+str(rate)+'$'
                        RateLevel[systList[v]][2][region][mode] = float(rate)


        if '<tr><td>tt</td><td><sup>' in line:
#            print mode,region
            vals = line.split('</td><td>')[1:]
            vals[-1] = vals[-1].split('</td></tr>')[0]
            for v in range(len(vals)):
                value = vals[v]
                if '---' in value:
                    RateSysts[systList[v]][1][region][mode] = '-'
                    RateLevel[systList[v]][1][region][mode] = 0.
                if '</sup><sub>' in value:
                    up = value.split('</sup><sub>')[0].split('<sup>')[-1]
                    down = value.split('</sup><sub>')[-1].split('</sub>')[0]
                    if '(s)' in value:                    
                        RateSysts[systList[v]][1][region][mode] = '$^{'+up+'}_{'+down+'}$'
                        RateLevel[systList[v]][1][region][mode] = max(float(up),float(down))
                    if '(r)' in value:
                        rate = (abs(float(up)) + abs(float(down)))/2.
                        RateSysts[systList[v]][1][region][mode] = '$\pm'+str(rate)+'$'
                        RateLevel[systList[v]][1][region][mode] = float(rate)
            
        if '<tr><td>twdr</td><td><sup>' in line:
#            print mode,region
            vals = line.split('</td><td>')[1:]
            vals[-1] = vals[-1].split('</td></tr>')[0]
            for v in range(len(vals)):
                value = vals[v]
                if '---' in value:
                    RateSysts[systList[v]][0][region][mode] = '-'
                    RateLevel[systList[v]][0][region][mode] = 0.
                if '</sup><sub>' in value:
                    up = value.split('</sup><sub>')[0].split('<sup>')[-1]
                    down = value.split('</sup><sub>')[-1].split('</sub>')[0]
                    if '(s)' in value:                    
                        RateSysts[systList[v]][0][region][mode] = '$^{'+up+'}_{'+down+'}$'
                        RateLevel[systList[v]][0][region][mode] = max(float(up),float(down))
                    if '(r)' in value:
                        rate = (abs(float(up)) + abs(float(down)))/2.
                        RateSysts[systList[v]][0][region][mode] = '$\pm'+str(rate)+'$'
                        RateLevel[systList[v]][0][region][mode] = float(rate)

#print RateSysts            

#RateSysts['Sim Stats'] = getStatUnc(['emu','mumu','ee'],['1j1t','2j1t','2j2t'],['twdr','tt','other'], texString = True)
RateSysts['Sim Stats'] = getStatUnc(['emu','mumu','ee'],regionList,['twdr','tt','other'], texString = True)


#print RateSysts['Sim Stats']


for region in range(len(regionList)):
    for sample in range(3):
#        for syst in systList:
        for syst in RateSysts:
            emu = RateSysts[syst][sample][region][0]
            mumu = RateSysts[syst][sample][region][1]
            ee = RateSysts[syst][sample][region][2]
#            print syst, emu, mumu, ee
            if emu ==  ee and emu == mumu:
                RateSysts[syst][sample][region][3] = str(emu)
            else:
                RateSysts[syst][sample][region][3] = str(ee) + '/' + str(emu) + '/' + str(mumu)
                

print '\\begin{table*}'
print '\\begin{center}'
print '\caption{Rate impact of all considered systematic uncertainty sources in the 1j1t signal region, values as a percentage.  Estimates for each of the three channels, unless specified as separate values for each channel ($ee$/$e\mu$/$\mu\mu$).  If two numbers are listed for a single uncertainty, the upper number is the effect on the rate when the systematic uncertainty source is scaled up and the lower is for when it is scaled down.  Entries with a single value indicate that the systematic is symmetric between the scaled up and scaled down effects.}'
print '\label{tab:BDTSystRates1j1t}'
print '\\begin{tabular}{| l | c | c | c |}'
print '\hline'
print '&&&\\[-2ex]'
print 'Systematic Uncertainty & tW & \\ttbar & Other \\\\'
print '(ee/$e\mu$/$\mu\mu$) & (\%) & (\%) & (\%) \\\\'
print '\hline'
print '&&&\\[-2ex]'
print 'Luminosity                     & '+RateSysts['lumi'][0][0][3]           +' & '+RateSysts['lumi'][1][0][3]           +' & '+RateSysts['lumi'][2][0][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Lepton identification          & '+RateSysts['lepSF'][0][0][3]          +' & '+RateSysts['lepSF'][1][0][3]          +' & '+RateSysts['lepSF'][2][0][3]          +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'JER                            & '+RateSysts['JER'][0][0][3]            +' & '+RateSysts['JER'][1][0][3]            +' & '+RateSysts['JER'][2][0][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'JES                            & '+RateSysts['JES'][0][0][3]            +' & '+RateSysts['JES'][1][0][3]            +' & '+RateSysts['JES'][2][0][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Lepton Energy Scale            & '+RateSysts['LES'][0][0][3]            +' & '+RateSysts['LES'][1][0][3]            +' & '+RateSysts['LES'][2][0][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'MET modeling                   & '+RateSysts['UnclusteredMET'][0][0][3] +' & '+RateSysts['UnclusteredMET'][1][0][3] +' & '+RateSysts['UnclusteredMET'][2][0][3] +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Event pile up                  & '+RateSysts['PU'][0][0][3]             +' & '+RateSysts['PU'][1][0][3]             +' & '+RateSysts['PU'][2][0][3]             +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'B-tagging data/MC scale factor & '+RateSysts['BtagSF'][0][0][3]         +' & '+RateSysts['BtagSF'][1][0][3]         +' & '+RateSysts['BtagSF'][2][0][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print '$Q^2$ scale                    & '+RateSysts['Q2'][0][0][3]             +' & '+RateSysts['Q2'][1][0][3]             +' & '+RateSysts['Q2'][2][0][3]             +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'ME/PS matching thresholds      & '+RateSysts['Matching'][0][0][3]       +' & '+RateSysts['Matching'][1][0][3]       +' & '+RateSysts['Matching'][2][0][3]       +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'tW DR/DS scheme                & '+RateSysts['DRDS'][0][0][3]           +' & '+RateSysts['DRDS'][1][0][3]           +' & '+RateSysts['DRDS'][2][0][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Top quark mass                 & '+RateSysts['TopMass'][0][0][3]        +' & '+RateSysts['TopMass'][1][0][3]        +' & '+RateSysts['TopMass'][2][0][3]        +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print '\\ttbar cross-section          & '+RateSysts['ttxs'][0][0][3]           +' & '+RateSysts['ttxs'][1][0][3]           +' & '+RateSysts['ttxs'][2][0][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'PDF                            & '+RateSysts['PDF'][0][0][3]            +' & '+RateSysts['PDF'][1][0][3]            +' & '+RateSysts['PDF'][2][0][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Z+jet MET scale factor         & '+RateSysts['ZjetSF'][0][0][3]         +' & '+RateSysts['ZjetSF'][1][0][3]         +' & '+RateSysts['ZjetSF'][2][0][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Simulations Statistics         & '+RateSysts['Sim Stats'][0][0][3]         +' & '+RateSysts['Sim Stats'][1][0][3]         +' & '+RateSysts['Sim Stats'][2][0][3]         +' \\\\ [0.5ex]'
print '\hline'
print '\end{tabular}'
print '\end{center}'
print '\end{table*}'

print
print
print
print
print



print '\\begin{table*}'
print '\\begin{center}'
print '\caption{Rate impact of all considered systematic uncertainty sources in the 2j1t control region, values as a percentage.  Estimates for each of the three channels, unless specified as separate values for each channel ($ee$/$e\mu$/$\mu\mu$).  If two numbers are listed for a single uncertainty, the upper number is the effect on the rate when the systematic uncertainty source is scaled up and the lower is for when it is scaled down.  Entries with a single value indicate that the systematic is symmetric between the scaled up and scaled down effects.}'
print '\label{tab:BDTSystRates2j1t}'
print '\\begin{tabular}{| l | c | c | c |}'
print '\hline'
print '&&&\\[-2ex]'
print 'Systematic Uncertainty & tW & \\ttbar & Other \\\\'
print '(ee/$e\mu$/$\mu\mu$) & (\%) & (\%) & (\%) \\\\'
print '\hline'
print '&&&\\[-2ex]'
print 'Luminosity                     & '+RateSysts['lumi'][0][1][3]           +' & '+RateSysts['lumi'][1][1][3]           +' & '+RateSysts['lumi'][2][1][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Lepton identification          & '+RateSysts['lepSF'][0][1][3]          +' & '+RateSysts['lepSF'][1][1][3]          +' & '+RateSysts['lepSF'][2][1][3]          +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'JER                            & '+RateSysts['JER'][0][1][3]            +' & '+RateSysts['JER'][1][1][3]            +' & '+RateSysts['JER'][2][1][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'JES                            & '+RateSysts['JES'][0][1][3]            +' & '+RateSysts['JES'][1][1][3]            +' & '+RateSysts['JES'][2][1][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Lepton Energy Scale            & '+RateSysts['LES'][0][1][3]            +' & '+RateSysts['LES'][1][1][3]            +' & '+RateSysts['LES'][2][1][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'MET modeling                   & '+RateSysts['UnclusteredMET'][0][1][3] +' & '+RateSysts['UnclusteredMET'][1][1][3] +' & '+RateSysts['UnclusteredMET'][2][1][3] +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Event pile up                  & '+RateSysts['PU'][0][1][3]             +' & '+RateSysts['PU'][1][1][3]             +' & '+RateSysts['PU'][2][1][3]             +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'B-tagging data/MC scale factor & '+RateSysts['BtagSF'][0][1][3]         +' & '+RateSysts['BtagSF'][1][1][3]         +' & '+RateSysts['BtagSF'][2][1][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print '$Q^2$ scale                    & '+RateSysts['Q2'][0][1][3]             +' & '+RateSysts['Q2'][1][1][3]             +' & '+RateSysts['Q2'][2][1][3]             +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'ME/PS matching thresholds      & '+RateSysts['Matching'][0][1][3]       +' & '+RateSysts['Matching'][1][1][3]       +' & '+RateSysts['Matching'][2][1][3]       +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'tW DR/DS scheme                & '+RateSysts['DRDS'][0][1][3]           +' & '+RateSysts['DRDS'][1][1][3]           +' & '+RateSysts['DRDS'][2][1][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Top quark mass                 & '+RateSysts['TopMass'][0][1][3]        +' & '+RateSysts['TopMass'][1][1][3]        +' & '+RateSysts['TopMass'][2][1][3]        +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print '\\ttbar cross-section           & '+RateSysts['ttxs'][0][1][3]           +' & '+RateSysts['ttxs'][1][1][3]           +' & '+RateSysts['ttxs'][2][1][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'PDF                            & '+RateSysts['PDF'][0][1][3]            +' & '+RateSysts['PDF'][1][1][3]            +' & '+RateSysts['PDF'][2][1][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Z+jet MET scale factor         & '+RateSysts['ZjetSF'][0][1][3]         +' & '+RateSysts['ZjetSF'][1][1][3]         +' & '+RateSysts['ZjetSF'][2][1][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Spin Correlation               & '+RateSysts['SpinCorr'][0][1][3]         +' & '+RateSysts['SpinCorr'][1][1][3]         +' & '+RateSysts['SpinCorr'][2][1][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Top \pt Reweighting            & '+RateSysts['TopPt'][0][1][3]         +' & '+RateSysts['TopPt'][1][1][3]         +' & '+RateSysts['TopPt'][2][1][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Simulations Statistics         & '+RateSysts['Sim Stats'][0][1][3]         +' & '+RateSysts['Sim Stats'][1][1][3]         +' & '+RateSysts['Sim Stats'][2][1][3]         +' \\\\'
print '\hline'
print '\end{tabular}'
print '\end{center}'
print '\end{table*}'

print
print
print
print
print

print '\\begin{table*}'
print '\\begin{center}'
print '\caption{Rate impact of all considered systematic uncertainty sources in the 2j2t control region, values as a percentage.  Estimates for each of the three channels, unless specified as separate values for each channel ($ee$/$e\mu$/$\mu\mu$).  If two numbers are listed for a single uncertainty, the upper number is the effect on the rate when the systematic uncertainty source is scaled up and the lower is for when it is scaled down.  Entries with a single value indicate that the systematic is symmetric between the scaled up and scaled down effects.}'
print '\label{tab:BDTSystRates2j2t}'
print '\\begin{tabular}{| l | c | c | c |}'
print '\hline'
print '&&&\\[-2ex]'
print 'Systematic Uncertainty & tW & \\ttbar & Other \\\\'
print '(ee/$e\mu$/$\mu\mu$) & (\%) & (\%) & (\%) \\\\'
print '\hline'
print '&&&\\[-2ex]'
print 'Luminosity                     & '+RateSysts['lumi'][0][2][3]           +' & '+RateSysts['lumi'][1][2][3]           +' & '+RateSysts['lumi'][2][2][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Lepton identification          & '+RateSysts['lepSF'][0][2][3]          +' & '+RateSysts['lepSF'][1][2][3]          +' & '+RateSysts['lepSF'][2][2][3]          +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'JER                            & '+RateSysts['JER'][0][2][3]            +' & '+RateSysts['JER'][1][2][3]            +' & '+RateSysts['JER'][2][2][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'JES                            & '+RateSysts['JES'][0][2][3]            +' & '+RateSysts['JES'][1][2][3]            +' & '+RateSysts['JES'][2][2][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Lepton Energy Scale            & '+RateSysts['LES'][0][2][3]            +' & '+RateSysts['LES'][1][2][3]            +' & '+RateSysts['LES'][2][2][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'MET modeling                   & '+RateSysts['UnclusteredMET'][0][2][3] +' & '+RateSysts['UnclusteredMET'][1][2][3] +' & '+RateSysts['UnclusteredMET'][2][2][3] +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Event pile up                  & '+RateSysts['PU'][0][2][3]             +' & '+RateSysts['PU'][1][2][3]             +' & '+RateSysts['PU'][2][2][3]             +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'B-tagging data/MC scale factor & '+RateSysts['BtagSF'][0][2][3]         +' & '+RateSysts['BtagSF'][1][2][3]         +' & '+RateSysts['BtagSF'][2][2][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print '$Q^2$ scale                    & '+RateSysts['Q2'][0][2][3]             +' & '+RateSysts['Q2'][1][2][3]             +' & '+RateSysts['Q2'][2][2][3]             +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'ME/PS matching thresholds      & '+RateSysts['Matching'][0][2][3]       +' & '+RateSysts['Matching'][1][2][3]       +' & '+RateSysts['Matching'][2][2][3]       +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'tW DR/DS scheme                & '+RateSysts['DRDS'][0][2][3]           +' & '+RateSysts['DRDS'][1][2][3]           +' & '+RateSysts['DRDS'][2][2][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Top quark mass                 & '+RateSysts['TopMass'][0][2][3]        +' & '+RateSysts['TopMass'][1][2][3]        +' & '+RateSysts['TopMass'][2][2][3]        +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print '\\ttbar cross-section           & '+RateSysts['ttxs'][0][2][3]           +' & '+RateSysts['ttxs'][1][2][3]           +' & '+RateSysts['ttxs'][2][2][3]           +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'PDF                            & '+RateSysts['PDF'][0][2][3]            +' & '+RateSysts['PDF'][1][2][3]            +' & '+RateSysts['PDF'][2][2][3]            +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Z+jet MET scale factor         & '+RateSysts['ZjetSF'][0][2][3]         +' & '+RateSysts['ZjetSF'][1][2][3]         +' & '+RateSysts['ZjetSF'][2][2][3]         +' \\\\ [0.5ex] \hline &&& \\\\ [-2ex]'
print 'Simulations Statistics         & '+RateSysts['Sim Stats'][0][2][3]         +' & '+RateSysts['Sim Stats'][1][2][3]         +' & '+RateSysts['Sim Stats'][2][2][3]         +' \\\\ [0.5ex] '
print '\hline'
print '\end{tabular}'
print '\end{center}'
print '\end{table*}'

tempList = list()
for i in range(len(regionList)):
    tempList.append(0)

# rateSystLevels = [[[0,0,0],[0,0,0],[0,0,0]],
#                   [[0,0,0],[0,0,0],[0,0,0]],
#                   [[0,0,0],[0,0,0],[0,0,0]]]

rateSystLevels = [[tempList[:],tempList[:],tempList[:]],
                  [tempList[:],tempList[:],tempList[:]],
                  [tempList[:],tempList[:],tempList[:]]]



for chan in range(3):
    for reg in range(len(regionList)):
        for s in RateSysts:
            if 'Sim S' in s:
                continue
            if 'TopMass' in s:
                modRate = 1.
            else:
                modRate = 1.
            rateSystLevels[0][chan][reg] += pow((RateLevel[s][0][reg][chan]/100.)/modRate,2)
            rateSystLevels[1][chan][reg] += pow((RateLevel[s][1][reg][chan]/100.)/modRate,2)
            rateSystLevels[2][chan][reg] += pow((RateLevel[s][2][reg][chan]/100.)/modRate,2)

        rateSystLevels[0][chan][reg] = sqrt(rateSystLevels[0][chan][reg])
        rateSystLevels[1][chan][reg] = sqrt(rateSystLevels[1][chan][reg])
        rateSystLevels[2][chan][reg] = sqrt(rateSystLevels[2][chan][reg])

#print rateSystLevels
print RateLevel['JER'][0]

# print
# print
# print 'ERROR LISTS'
# print
# print
# print 'tWErrors = [[',rateSystLevels[0][0][0],',',rateSystLevels[0][0][1],',',rateSystLevels[0][0][2],'],'
# print '            [',rateSystLevels[0][1][0],',',rateSystLevels[0][1][1],',',rateSystLevels[0][1][2],'],'
# print '            [',rateSystLevels[0][2][0],',',rateSystLevels[0][2][1],',',rateSystLevels[0][2][2],']]'
# print
# print 'ttErrors = [[',rateSystLevels[1][0][0],',',rateSystLevels[1][0][1],',',rateSystLevels[1][0][2],'],'
# print '            [',rateSystLevels[1][1][0],',',rateSystLevels[1][1][1],',',rateSystLevels[1][1][2],'],'
# print '            [',rateSystLevels[1][2][0],',',rateSystLevels[1][2][1],',',rateSystLevels[1][2][2],']]'
# print
# print 'otherErrors = [[',rateSystLevels[2][0][0],',',rateSystLevels[2][0][1],',',rateSystLevels[2][0][2],'],'
# print '               [',rateSystLevels[2][1][0],',',rateSystLevels[2][1][1],',',rateSystLevels[2][1][2],'],'
# print '               [',rateSystLevels[2][2][0],',',rateSystLevels[2][2][1],',',rateSystLevels[2][2][2],']]'

# print
# print
# print



print 'tWErrors = {"'
for i in range(len(regionList)):
    print '            "'+regionList[i]+'":[',rateSystLevels[0][0][i],',',rateSystLevels[0][1][i],',',rateSystLevels[0][2][i],'],'
print '            }'
print
print 'ttErrors = {"'
for i in range(len(regionList)):
    print '            "'+regionList[i]+'":[',rateSystLevels[1][0][i],',',rateSystLevels[1][1][i],',',rateSystLevels[1][2][i],'],'
print '            }'
print
print 'otherErrors = {"'
for i in range(len(regionList)):
    print '            "'+regionList[i]+'":[',rateSystLevels[2][0][i],',',rateSystLevels[2][1][i],',',rateSystLevels[2][2][i],'],'
print '            }'
print

# print 'tWErrors = {"'+regionList[0]+'":[',rateSystLevels[0][0][0],',',rateSystLevels[0][1][0],',',rateSystLevels[0][2][0],'],'
# print '            "'+regionList[1]+'":[',rateSystLevels[0][0][1],',',rateSystLevels[0][1][1],',',rateSystLevels[0][2][1],'],'
# print '            "'+regionList[2]+'":[',rateSystLevels[0][0][2],',',rateSystLevels[0][1][2],',',rateSystLevels[0][2][2],'],'
# print '            }'
# print
# print 'ttErrors = {"'+regionList[0]+'":[',rateSystLevels[1][0][0],',',rateSystLevels[1][1][0],',',rateSystLevels[1][2][0],'],'
# print '            "'+regionList[1]+'":[',rateSystLevels[1][0][1],',',rateSystLevels[1][1][1],',',rateSystLevels[1][2][1],'],'
# print '            "'+regionList[2]+'":[',rateSystLevels[1][0][2],',',rateSystLevels[1][1][2],',',rateSystLevels[1][2][2],'],'
# print '            }'
# print
# print 'otherErrors = {"'+regionList[0]+'":[',rateSystLevels[2][0][0],',',rateSystLevels[2][1][0],',',rateSystLevels[2][2][0],'],'
# print '               "'+regionList[1]+'":[',rateSystLevels[2][0][1],',',rateSystLevels[2][1][1],',',rateSystLevels[2][2][1],'],'
# print '               "'+regionList[2]+'":[',rateSystLevels[2][0][2],',',rateSystLevels[2][1][2],',',rateSystLevels[2][2][2],'],'
# print '               }'
# print
