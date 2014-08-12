#! /usr/bin/env python

import os,sys

from ROOT import *

directory = 'Test/Rmeasurement_AdaBoostDefault_NewTests_35Bins_Rcut_'
rootFileName = 'inputFileTheta_Rmeasurement_AdaBoostDefault_NewTests_35Bins_Rcut_'

EfficiencyBase = 0.

file = TFile(directory+'0.0/'+rootFileName+'0.0.root')

EfficiencyBase += TH1F(file.Get("emu1j1tT__twdr")).Integral()
EfficiencyBase += TH1F(file.Get("emu1j1tTbar__tbarwdr")).Integral()
EfficiencyBase += TH1F(file.Get("mumu1j1tT__twdr")).Integral()
EfficiencyBase += TH1F(file.Get("mumu1j1tTbar__tbarwdr")).Integral()
EfficiencyBase += TH1F(file.Get("ee1j1tT__twdr")).Integral()
EfficiencyBase += TH1F(file.Get("ee1j1tTbar__tbarwdr")).Integral()

print EfficiencyBase

efficiencies = list()
purities = list()
errorUp = list()
errorDown = list()
Rval = list()
error = list()
Theoryerror = list()

Cut=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.65,0.66,0.67,0.68,0.69,0.7,0.8]

for i in Cut:
    print i
    name = "%s%s/%s%s.root" % (directory, str(i), rootFileName, str(i))
    print name
    file = TFile(name)

    CountRight = 0
    CountWrong = 0
    CountRight += TH1F(file.Get("emu1j1tT__twdr")).Integral()
    CountRight += TH1F(file.Get("emu1j1tTbar__tbarwdr")).Integral()
    CountRight += TH1F(file.Get("mumu1j1tT__twdr")).Integral()
    CountRight += TH1F(file.Get("mumu1j1tTbar__tbarwdr")).Integral()
    CountRight += TH1F(file.Get("ee1j1tT__twdr")).Integral()
    CountRight += TH1F(file.Get("ee1j1tTbar__tbarwdr")).Integral()

    CountWrong += TH1F(file.Get("emu1j1tTbar__twdr")).Integral()
    CountWrong += TH1F(file.Get("emu1j1tT__tbarwdr")).Integral()
    CountWrong += TH1F(file.Get("mumu1j1tTbar__twdr")).Integral()
    CountWrong += TH1F(file.Get("mumu1j1tT__tbarwdr")).Integral()
    CountWrong += TH1F(file.Get("ee1j1tTbar__twdr")).Integral()
    CountWrong += TH1F(file.Get("ee1j1tT__tbarwdr")).Integral()

    print CountRight, CountWrong
    efficiencies.append(CountRight / EfficiencyBase)
    purities.append(CountRight / (CountRight+CountWrong))

    condorFile = open("%s%s/condor_output/condor_NewThetaRunTheta_0.out" % (directory, str(i)))

    UseThis = False
    for line in condorFile:
        if 'Ratio value' in line:
            UseThis = True
        if 'TW signal' in line:
            UseThis = False
        if 'TbarW signal' in line:
            UseThis = False
        if UseThis and 'total fit (interval)' in line:
            temp= line.split(":")[-1].split('(')[-1].split(')')[0].split('--')
            error.append((float(temp[1])-float(temp[0]))/2)
#            error.append(abs(max(float(temp[1]),float(temp[0]))-1))
        if UseThis and '--> total additional uncertaitnty' in line:
            Theoryerror.append(float(line.split()[-1]))

#         if UseThis and 'central fit :' in line:
#             R_value=line.split(':')[-1][:-1].split()
#     errorUp.append(float(R_value[1]))
#     errorUp.append(float(R_value[1]))
#     errorDown.append(float(R_value[2]))
    

print "Cut\tEff\tPur\tError\tTheoryErr"
for i in range(len(Cut)):
    
    print "%s\t%.3f\t%.3f\t%.4f\t%.4f\t%.4f" % (str(Cut[i]),efficiencies[i],purities[i],error[i],Theoryerror[i], sqrt(error[i]**2 + Theoryerror[i]**2))
#    print "%s\t%.3f\t%.3f\t%.4f\t%.3f\t%.3f" % (str(Cut[i]),efficiencies[i],purities[i],Rval[i],errorUp[i],errorDown[i])
    
