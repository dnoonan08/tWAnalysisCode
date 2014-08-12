#! /usr/bin/env python
#A script to set up, from basic templates files a directory to submit Theta jobs broken down by channel(s)
import os,subprocess,sys

doQ2ShapeFix = False
do9Nuisance = False
do3Nuisance = False
Q2TwoSigma = False
NoTopMass = False

#The two options for test statistic are deltanll (for likelihood ratio) or derll (for derivative of likelihood)
#testStatistic = 'deltanll'
testStatistic = 'derll'

fullSubmissions = 1000
emuSubmissions = 75
twoChanSubmissions = 100
otherSubmissions = 5

nToys = 1000000

# fullSubmissions = 100
# emuSubmissions = 25
# twoChanSubmissions = 25
# otherSubmissions = 5

# nToys = 500000

fullSubmissions = 4000
emuSubmissions = 200
twoChanSubmissions = 0
otherSubmissions = 0

nToys = 1000000


use2j1t = True
use2j2t = True

mleOnly = False
NotExternalized = False

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if 'Q2ShapeFix' in arg:
            doQ2ShapeFix = True
        if 'do9Nuisance' in arg:
            do9Nuisance = True
        if 'do3Nuisance' in arg:
            do3Nuisance = True
        if 'Q2TwoSigma' in arg:
            Q2TwoSigma = True
        if 'no2j1t' in arg:
            use2j1t = False
        if 'no2j2t' in arg:
            use2j2t = False
        if 'NoTopMass' in arg:
            NoTopMass = True
        if 'mleOnly' in arg:
            mleOnly = True
            fullSubmissions = 0
            emuSubmissions = 0
            twoChanSubmissions = 0
            otherSubmissions = 0            
            nToys = 100
        if 'CrossSectionOnly' in arg:
            mleOnly = True
            fullSubmissions = 0
            emuSubmissions = 0
            twoChanSubmissions = 0
            otherSubmissions = 0            
            nToys = 100
        elif 'NotExternalized' in arg:
            NotExternalized = True
        if 'deltanll' in arg:
            testStatistic = 'deltanll'


#Get current working directory
currentDir=os.getcwd()

#Templates dir:
templatesDir=(currentDir+'/../../copy_Gabriele_SampleThetaCondorScripts')




#Fix the condor executable script first Theta.sh:

#First get the file from template directory:
print "Taking the template NewTheta.sh from %s/NewTheta.sh"%templatesDir
cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,'NewTheta.sh'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput

cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,'NewThetaRunTheta.sh'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput

cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,'NewThetaRunTheta.condor'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput


#Then get the analysis.py of the fittinganalysis.py file template and "clone" it for all the subchannels combinations:
pythonCfg='analysisJochenSyst8TeV.py' #Using Jochen's latest significance and profile likelihood analysis with the tweak of using 4.4% lumi and 6% ttbar x-sect errors (and not other rate uncertainties)

print "Copying the theta configuration template file %s from %s/%s"%(pythonCfg,templatesDir,pythonCfg)
cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,pythonCfg),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput

#Now given the theta python configuration file (that will use all the channels in the model)  generate the alternative configurations
#to look into the single and pairs of channels:
pythonCfgOriginalLines=open(pythonCfg,'r').readlines()
ChannelsList=['ee/emu/mumu',
              'ee',
              'emu',
              'mumu',
              'emu_ee',
              'emu_mumu',
              'ee_mumu'
              ]

#ChannelsLines='setmodel.add("CHAN")\nsetmodel.add("CHAN2j1t")\nsetmodel.add("CHAN2j2t")\nmodel.restrict_to_observables(setmodel)\n'

rootFile=[rootfile for rootfile in os.listdir('.') if rootfile.endswith('.root')][0]

print rootFile

#Make numerous copies of the analysisJochenSyst8TeV.py script, where each copy will run 200k toys for the background only hypothesis
for channel in ChannelsList:
    if channel == 'ee/emu/mumu': maxSubmissions = fullSubmissions
    elif channel == 'emu': maxSubmissions = emuSubmissions
    elif channel == 'emu_ee' or channel == 'emu_mumu' or channel == 'ee_mumu': maxSubmissions = twoChanSubmissions
    else: maxSubmissions = otherSubmissions
    for i in range(maxSubmissions):
        if channel == 'ee/emu/mumu':
            pythonCfgNew=open(pythonCfg.replace('.py','_'+str(i+1)+'_'+str(maxSubmissions)+'.py'),'w')
        else:
            pythonCfgNew=open(pythonCfg.replace('.py','_'+channel+'_'+str(i+1)+'_'+str(maxSubmissions)+'.py'),'w')
        for line in pythonCfgOriginalLines:
            if 'ROOTFILEINPUT' in line:
                print "Will automatically set all theta cfgs to use the root file found in this directory:"
#                 rootFile=[rootfile for rootfile in os.listdir('.') if rootfile.endswith('.root')][0]
                print "%s"%rootFile
                newline=line.replace('ROOTFILEINPUT',rootFile)
                
            elif line.startswith('model = get_model('):
                newline=line+'setmodel = set([])\n'
                if channel !='ee/emu/mumu': #For all channel combination, but the All Channel one:
                    if '_' not in channel: #IndividualChannels
                        newline=newline+"\n#Channel %s ONLY:\n"%channel
                        #G.Benelli Jan 2013
                        #Need to add 1j1t to the signal region model name!!!!
#                         newline=newline+'setmodel.add("%s1j1t")\nsetmodel.add("%s2j1t")\nsetmodel.add("%s2j2t")\nmodel.restrict_to_observables(setmodel)\n'%(channel,channel,channel)
                        newline=newline+'setmodel.add("%s1j1t")\n'%(channel)
                        if use2j1t:
                            newline=newline+'setmodel.add("%s2j1t")\n'%(channel)
                        if use2j2t:
                            newline=newline+'setmodel.add("%s2j2t")\n'%(channel)
                        newline=newline+'model.restrict_to_observables(setmodel)\n'
                    else:
                        newline=newline+"\n#Channels %s %s ONLY:\n"%tuple(channel.split('_'))
                        for chan in channel.split('_'):
                            #G.Benelli Jan 2013
                            #Need to add 1j1t to the signal region model name!!!!
#                            newline=newline+'setmodel.add("%s1j1t")\nsetmodel.add("%s2j1t")\nsetmodel.add("%s2j2t")\n'%(chan,chan,chan)
                            newline=newline+'setmodel.add("%s1j1t")\n'%(chan)
                            if use2j1t:
                                newline=newline+'setmodel.add("%s2j1t")\n'%(chan)
                            if use2j2t:
                                newline=newline+'setmodel.add("%s2j2t")\n'%(chan)
                        newline=newline+'model.restrict_to_observables(setmodel)\n'
                elif not use2j1t or not use2j2t:
                    for chan in ['emu','mumu','ee']:
                        newline=newline+'setmodel.add("%s1j1t")\n'%(chan)
                        if use2j1t:
                            newline=newline+'setmodel.add("%s2j1t")\n'%(chan)
                        if use2j2t:
                            newline=newline+'setmodel.add("%s2j2t")\n'%(chan)
                    newline=newline+'model.restrict_to_observables(setmodel)\n'                    
            elif 'NUMBEROFRUNS' in line:
                newline = line.replace('NUMBEROFRUNS',str(maxSubmissions)).replace('TOYSPERRUN',str(nToys)).replace('TESTSTAT',testStatistic)
            elif 'TOYSPERRUN' in line:
                newline = line.replace('TOYSPERRUN',str(nToys))
            elif 'CURRENTRUN' in line:
                newline = line.replace('CURRENTRUN',str(i))
            elif doQ2ShapeFix and 'Q2ShapeFixed=' in line:
                newline = line.replace('=False','=True')
            elif do3Nuisance and 'Nuisance3par=' in line:
                newline = line.replace('=False','=True')
            elif do9Nuisance and 'Nuisance9par=' in line:
                newline = line.replace('=False','=True')
            elif Q2TwoSigma and 'Q2TwoSigma=' in line:
                newline = line.replace('=False','=True')
            elif '_NoDRDS' in rootFile and 'for fix_uncertainties in ' in line:
                newline = line.replace(", 'DRDS',",",")
            elif '_NoMatching' in rootFile and 'for fix_uncertainties in ' in line:
                newline = line.replace(", 'Matching',",",")
            elif '_NoQ2' in rootFile and 'for fix_uncertainties in ' in line:
                newline = line.replace(", 'Q2',",",")
            elif '_NoTopMass' in rootFile and 'for fix_uncertainties in ' in line:
                newline = line.replace(", 'TopMass',",",")
            elif NoTopMass and 'useTopMass = True' in line:
                newline = line.replace('= True','= False')
            elif '_NoTopMass' in rootFile and 'useTopMass = True' in line:
                newline = line.replace('= True','= False')
            elif NoTopMass and 'for fix_uncertainties in ' in line:
                newline = line.replace(", 'TopMass',",",")
            elif NotExternalized and 'for fix_uncertainties in ' in line:
                newline = line.replace("['DRDS', 'Matching', 'Q2', 'TopMass', 'TopPt']","None")
            else:
                newline=line
            pythonCfgNew.write(newline)



#File for combining all the toys using the "discover" method
pythonRunThetaCfg='analysisJochenSyst8TeVRunTheta.py' #Template for file that collects all the previously run background only toys and runs the "discovery" method

print "Copying the theta configuration template file %s from %s/%s"%(pythonRunThetaCfg,templatesDir,pythonRunThetaCfg)
cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,pythonRunThetaCfg),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput

#Now given the theta python configuration file (that will use all the channels in the model)  generate the alternative configurations
#to look into the single and pairs of channels:
pythonRunThetaCfgOriginalLines=open(pythonRunThetaCfg,'r').readlines()


for channel in ChannelsList:
    if channel == 'ee/emu/mumu': maxSubmissions = fullSubmissions
    elif channel == 'emu': maxSubmissions = emuSubmissions
    elif channel == 'emu_ee' or channel == 'emu_mumu' or channel == 'ee_mumu': maxSubmissions = twoChanSubmissions
    else: maxSubmissions = otherSubmissions

    if channel == 'ee/emu/mumu':
        pythonRunThetaCfgNew=open(pythonRunThetaCfg,'w')
    else:
        pythonRunThetaCfgNew=open(pythonRunThetaCfg.replace('.py','_'+channel+'.py'),'w')
    for line in pythonRunThetaCfgOriginalLines:
        if 'ROOTFILEINPUT' in line:
            print "Will automatically set all theta cfgs to use the root file found in this directory:"
#             rootFile=[rootfile for rootfile in os.listdir('.') if rootfile.endswith('.root')][0]
            print "%s"%rootFile
            newline=line.replace('ROOTFILEINPUT',rootFile)                
        elif line.startswith('model = get_model('):
            newline=line+'setmodel = set([])\n'
            if channel !='ee/emu/mumu': #For all channel combination, but the All Channel one:
                if '_' not in channel: #IndividualChannels
                    newline=newline+"\n#Channel %s ONLY:\n"%channel
                    #G.Benelli Jan 2013
                    #Need to add 1j1t to the signal region model name!!!!
                    #                         newline=newline+'setmodel.add("%s1j1t")\nsetmodel.add("%s2j1t")\nsetmodel.add("%s2j2t")\nmodel.restrict_to_observables(setmodel)\n'%(channel,channel,channel)
                    newline=newline+'setmodel.add("%s1j1t")\n'%(channel)
                    if use2j1t:
                        newline=newline+'setmodel.add("%s2j1t")\n'%(channel)
                    if use2j2t:
                        newline=newline+'setmodel.add("%s2j2t")\n'%(channel)
                    newline=newline+'model.restrict_to_observables(setmodel)\n'
                else:
                    newline=newline+"\n#Channels %s %s ONLY:\n"%tuple(channel.split('_'))
                    for chan in channel.split('_'):
                        #G.Benelli Jan 2013
                        #Need to add 1j1t to the signal region model name!!!!
                        #                            newline=newline+'setmodel.add("%s1j1t")\nsetmodel.add("%s2j1t")\nsetmodel.add("%s2j2t")\n'%(chan,chan,chan)
                        newline=newline+'setmodel.add("%s1j1t")\n'%(chan)
                        if use2j1t:
                            newline=newline+'setmodel.add("%s2j1t")\n'%(chan)
                        if use2j2t:
                            newline=newline+'setmodel.add("%s2j2t")\n'%(chan)
                    newline=newline+'model.restrict_to_observables(setmodel)\n'
            elif not use2j1t or not use2j2t:
                for chan in ['emu','mumu','ee']:
                    newline=newline+'setmodel.add("%s1j1t")\n'%(chan)
                    if use2j1t:
                        newline=newline+'setmodel.add("%s2j1t")\n'%(chan)
                    if use2j2t:
                        newline=newline+'setmodel.add("%s2j2t")\n'%(chan)
                newline=newline+'model.restrict_to_observables(setmodel)\n'                    
        elif 'NUMBEROFRUNS' in line:
            newline = line.replace('NUMBEROFRUNS',str(maxSubmissions)).replace('TOYSPERRUN',str(nToys)).replace('TESTSTAT',testStatistic)
        elif 'TOYSPERRUN' in line:
            newline = line.replace('TOYSPERRUN',str(nToys))
        elif doQ2ShapeFix and 'Q2ShapeFixed=' in line:
            newline = line.replace('=False','=True')
        elif do3Nuisance and 'Nuisance3par=' in line:
            newline = line.replace('=False','=True')
        elif do9Nuisance and 'Nuisance9par=' in line:
            newline = line.replace('=False','=True')
        elif Q2TwoSigma and 'Q2TwoSigma=' in line:
            newline = line.replace('=False','=True')        
        elif mleOnly and 'do_significance =' in line:
            newline = line.replace('= True','= False')
        elif '_NoDRDS' in rootFile and 'for fix_uncertainties in ' in line:
            newline = line.replace(", 'DRDS',",",")
        elif '_NoMatching' in rootFile and 'for fix_uncertainties in ' in line:
            newline = line.replace(", 'Matching',",",")
        elif '_NoQ2' in rootFile and 'for fix_uncertainties in ' in line:
            newline = line.replace(", 'Q2',",",")
        elif '_NoTopMass' in rootFile and 'for fix_uncertainties in ' in line:
            newline = line.replace(", 'TopMass',",",")
        elif NoTopMass and 'useTopMass = True' in line:
            newline = line.replace('= True','= False')
        elif '_NoTopMass' in rootFile and 'useTopMass = True' in line:
            newline = line.replace('= True','= False')
        elif NoTopMass and 'for fix_uncertainties in ' in line:
            newline = line.replace(", 'TopMass',",",")
        elif NotExternalized and 'for fix_uncertainties in ' in line:
            newline = line.replace("['DRDS', 'Matching', 'Q2', 'TopMass', 'TopPt']","None")
        else:
            newline=line
        pythonRunThetaCfgNew.write(newline)



#Finally get and edit the Theta.condor file (and make one for each channel):
condorCfg='NewTheta.condor'
print "Copying the condor configuration template file %s from %s/%s"%(condorCfg,templatesDir,condorCfg)
cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,condorCfg),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput
condorCfgOriginalLines=open(condorCfg,'r').readlines()
for channel in ChannelsList:
    if channel == 'ee/emu/mumu': maxSubmissions = fullSubmissions
    elif channel == 'emu': maxSubmissions = emuSubmissions
    elif channel == 'emu_ee' or channel == 'emu_mumu' or channel == 'ee_mumu': maxSubmissions = twoChanSubmissions
    else: maxSubmissions = otherSubmissions
    if channel == 'ee/emu/mumu':
        condorCfgNew=open(condorCfg,'w') #For all three channels the pythong cfg stays the same name as the template!
    else:
        condorCfgNew=open(condorCfg.replace('.condor','_'+channel+'.condor'),'w')
    for line in condorCfgOriginalLines:
        if 'CURRENTDIR/NewTHETACHAN' in line:
            if channel=='ee/emu/mumu':
                newline=line.replace('THETACHAN','Theta').replace('CURRENTDIR',currentDir)
            else:
                newline=line.replace('THETACHAN','Theta_%s'%channel).replace('CURRENTDIR',currentDir)
        elif 'CURRENTDIR' in line:
            newline=line.replace('CURRENTDIR',currentDir)
        elif 'THETACHAN' in line:
            if channel=='ee/emu/mumu':
                newline=line.replace('THETACHAN','Theta')
            else:
                newline=line.replace('THETACHAN','Theta_%s'%channel)
        elif 'MAXSUBMISSIONS' in line:
#            newline=line.replace('MAXSUBMISSIONS',str(maxSubmissions+1)) #for when also doing the SplusB
            newline=line.replace('MAXSUBMISSIONS',str(maxSubmissions))
        else:
            newline=line
        condorCfgNew.write(newline)


condorSh='NewTheta.sh'
print "Copying the condor configuration template file %s from %s/%s"%(condorSh,templatesDir,condorSh)
cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,condorSh),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput
condorShOriginalLines=open(condorSh,'r').readlines()
for channel in ChannelsList:
    if channel == 'ee/emu/mumu': maxSubmissions = fullSubmissions
    elif channel == 'emu': maxSubmissions = emuSubmissions
    elif channel == 'emu_ee' or channel == 'emu_mumu' or channel == 'ee_mumu': maxSubmissions = twoChanSubmissions
    else: maxSubmissions = otherSubmissions
    if channel == 'ee/emu/mumu':
        condorShNew=open(condorSh,'w') #For all three channels the pythong cfg stays the same name as the template!
        chan = ''
    else:
        condorShNew=open(condorSh.replace('.sh','_'+channel+'.sh'),'w')
        chan = '_'+channel
    for line in condorShOriginalLines:
        if 'CURRENTDIR' in line:
            newline=line.replace('CURRENTDIR',currentDir)
        elif 'ITERATION' in line:
            newline=''
            for i in range(maxSubmissions):
                newline+=line.replace('ITERATION',str(i)).replace('CHANNEL',chan).replace('ITER-PLUS-1',str(i+1)).replace('MAXSUBMISSION',str(maxSubmissions))
        elif 'EXTRA' in line:
            newline=line.replace('EXTRA',str(maxSubmissions)).replace('CHANNEL',chan)
        else:
            newline=line
        condorShNew.write(newline)



#Finally get and edit the Theta.condor file (and make one for each channel):
condorCfg='NewThetaRunTheta.condor'
print "Copying the condor configuration template file %s from %s/%s"%(condorCfg,templatesDir,condorCfg)
cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,condorCfg),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput
condorCfgOriginalLines=open(condorCfg,'r').readlines()
condorCfgNew=open(condorCfg,'w') #For all three channels the pythong cfg stays the same name as the template!
for line in condorCfgOriginalLines:
    if 'CURRENTDIR' in line:
        newline=line.replace('CURRENTDIR',currentDir)
    else:
        newline=line
    condorCfgNew.write(newline)


condorSh='NewThetaRunTheta.sh'
print "Copying the condor configuration template file %s from %s/%s"%(condorSh,templatesDir,condorSh)
cmdOutput=subprocess.Popen('cp -pR %s/%s .'%(templatesDir,condorSh),shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
print cmdOutput
condorShOriginalLines=open(condorSh,'r').readlines()

condorShNew=open(condorSh,'w') #For all three channels the pythong cfg stays the same name as the template!

for line in condorShOriginalLines:
    if 'CURRENTDIR' in line:
        newline=line.replace('CURRENTDIR',currentDir)
    else:
        newline=line
    condorShNew.write(newline)



#Create a simple shell script to copy all job outputs over to the directories needed for the RunTheta scripts (so it doesn't try to remake them)

copyFile=open('copyAll.sh','w')

for channel in ChannelsList:
    if channel == 'ee/emu/mumu': maxSubmissions = fullSubmissions
    elif channel == 'emu': maxSubmissions = emuSubmissions
    elif channel == 'emu_ee' or channel == 'emu_mumu' or channel == 'ee_mumu': maxSubmissions = twoChanSubmissions
    else: maxSubmissions = otherSubmissions
    if channel == 'ee/emu/mumu':
        chan = ''
    else:
        chan = '_'+channel

    line = ' \n'
    copyFile.write(line)

    line = '#'+channel+' \n'
    copyFile.write(line)

    for i in range(maxSubmissions):
        line = 'mv analysisJochenSyst8TeV'+chan+'_'+str(i+1)+'_'+str(maxSubmissions)+'/cache/* analysisJochenSyst8TeVRunTheta'+chan+'/cache/.'+' \n'
        copyFile.write(line)
#    line = 'mv analysisJochenSyst8TeV_SplusB'+chan+'/cache/* analysisJochenSyst8TeVRunTheta'+chan+'/cache/.'+' \n'
#    copyFile.write(line)
