#! /usr/bin/env python

import os,subprocess,time,sys

rootFiles=[rootfile for rootfile in os.listdir('rootFileDir') if rootfile.endswith('.root')]

startDir=os.getcwd()

extraName = ''
extraArgs = ''

getName = False
if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        if 'Q2ShapeFix' in arg:
            extraName += 'Q2ShapeFix'
            extraArgs += ' ' + arg
        elif 'do9Nuisance' in arg:
            extraName += 'Extra9NuisancePar'
            extraArgs += ' ' + arg
        elif 'do3Nuisance' in arg:
            extraName += 'Extra3NuisancePar'
            extraArgs += ' ' + arg
        elif 'Q2TwoSigma' in arg:
            extraName += 'Q2TwoSigma'
            extraArgs += ' ' + arg
        elif 'no2j1t' in arg:
            extraName += 'no2j1t'
            extraArgs += ' ' + arg
        elif 'no2j2t' in arg:
            extraName += 'no2j2t'
            extraArgs += ' ' + arg
        elif 'NoTopMass' in arg:
            extraArgs += ' ' + arg
        elif 'mleOnly' in arg:
            extraName += 'mleOnly'
            extraArgs += ' ' + arg
        elif 'CrossSectionOnly' in arg:
            extraName += 'CrossSectionOnly'
            extraArgs += ' ' + arg
        elif '-n' in arg:
            extraName += sys.argv[i+1]
            getName = True
        elif 'externalizedOnly' in arg:
            extraArgs += ' ' + arg
        elif 'externalizedOld' in arg:
            extraArgs += ' ' + arg
        elif 'NotExternalized' in arg:
            extraArgs += ' ' + arg
        elif getName:
            getName = False
        elif 'deltanll' in arg or 'deltaNLL' in arg:
            extraArgs += ' deltanll'
            extraName += '_DeltaNLL'
        else:
            print 'Unknown argument value ('+arg+')'
            sys.exit(0)

for file in rootFiles:

    os.chdir(startDir)

    directory = file.split('inputFileTheta_')[-1].split('.root')[0]
    directory = directory + extraName
    print directory

    mkdirOutput=subprocess.Popen('mkdir Test/%s'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/condor_output'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_emu'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_mumu'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_ee'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_emu_mumu'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_emu_ee'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_ee_mumu'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput



    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta/cache'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_emu/cache'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_mumu/cache'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_ee/cache'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_emu_mumu/cache'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_emu_ee/cache'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput

    mkdirOutput=subprocess.Popen('mkdir Test/%s/analysisJochenSyst8TeVRunTheta_ee_mumu/cache'%directory,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print mkdirOutput


    cpRootOutput=subprocess.Popen('cp rootFileDir/%s Test/%s/.'%(file,directory),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    print cpRootOutput

    os.chdir(startDir+'/Test/'+directory)

    print os.getcwd()

    subprocess.call([startDir+'/copy_Gabriele_SampleThetaCondorScripts/NewSetDistributiveCondorFiles8TeV.py', extraArgs])


    os.chdir(startDir)
    
    print os.getcwd()
