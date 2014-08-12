#!/usr/bin/env python
import os, sys
import glob
import subprocess

#Script to take the edmtuple output from a crab job (given by a directory name as an argument)
#and put them into a cfg file to make the systematics nTuples for that sample
#Two arguments needed, directory of crab output and the channel name

#ex:
# mergeAndRun.py tW_Synch T_tWChannel

channelName = ""
directory = ""
rootFileName = ""

appendVersion = ""

currentFileVersion = "v9"

okChannelNames = ['TChannel',
                  'TbarChannel',
                  'TWChannel',
                  'TbarWChannel',
                  'SChannel',
                  'SbarChannel',
                  'TTBar',
                  'ZJets',
                  'ZJetsLowMass',
                  'WJets',
                  'WW',
                  'WZ',
                  'ZZ',
                  'Data',
                  'TWChannelDilepton',
                  'TbarWChannelDilepton',
                  'TTBarDilepton',                  
                  'TestSample',
                  'TWChannel_DS',
                  'TbarWChannel_DS',
                  'TWChannel_Q2Up',
                  'TWChannel_Q2Down',
                  'TbarWChannel_Q2Up',
                  'TbarWChannel_Q2Down',
                  'TWChannel_TopMassUp',
                  'TWChannel_TopMassDown',
                  'TbarWChannel_TopMassUp',
                  'TbarWChannel_TopMassDown',
                  'TTBar_Q2Up',
                  'TTBar_Q2Down',
                  'TTBar_MatchingUp',
                  'TTBar_MatchingDown',
                  'TTBar_TopMassUp',
                  'TTBar_TopMassDown',                
                  'TTBarSpin',
                  'TTBarPowheg',
                  'TTBarNew',
                  'TTBar_Q2Up_New',
                  'TTBar_Q2Down_New',
                  'TTBar_MatchingUp_New',
                  'TTBar_MatchingDown_New1',
                  'TTBar_MatchingDown_New2',
                  'TTBar_MatchingDown_New',
                  'TTBar_TopMassUp_New',
                  'TTBar_TopMassDown_New',
                  ]


dataChannels = ['MuEG',
                'DoubleMu',
                'DoubleElectron']

# dataRuns = ['Run2012A-13Jul2012',
#             'Run2012A-recover-06Aug2012',
#             'Run2012B-13Jul2012',
#             'Run2012C-24Aug2012',
#             'Run2012C-PromptReco']

dataRuns = ['Run2012A-22Jan2013',
            'Run2012B-22Jan2013',
            'Run2012C-22Jan2013',
            'Run2012D-22Jan2013',
            ]


#storeUser = "/home/t3-ku/dnoonan/storeUser/tW_8TeV/"
storeUser = "/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/user/dnoonan/tW_8TeV/"    

ProcessNumber = -1
OutOf = -1

isData = False
goodOptions = False
isSyst = False

Dirs = list()
doMulti = False

if sys.argv[5] == 'Multi':
    doMulti = True
    print "Using Systematics"
    if sys.argv[2] in okChannelNames:
        channelName = sys.argv[2]
        rootFileName = sys.argv[2]
        goodOptions = True
        isSyst = True
    else:
        print "Invalid channel name: " + sys.argv[2]
        print okChannelNames
        exit()
    ProcessNumber = int(sys.argv[3])
    OutOf = int(sys.argv[4])
    for i in range(6,len(sys.argv)):  
        print sys.argv[i]
        directory=storeUser+"Systs/"+sys.argv[i]
        if not os.path.exists(directory):
            print "Directory specified ("+directory+") does not exist"
            exit()                      
        else:
            Dirs.append(directory)
elif len(sys.argv) == 7:
    if sys.argv[2] == 'Data':
        if sys.argv[3] in dataChannels:
            if sys.argv[4] in dataRuns:
                channelName = sys.argv[2]
                rootFileName = sys.argv[3] + "_" + sys.argv[4]
                directory=storeUser + "Data/" + sys.argv[1]
                if not os.path.exists(directory):
                    print "Directory specified ("+directory+") does not exist"
                    exit()                
                isData = True
                goodOptions = True
                ProcessNumber = int(sys.argv[5])
                OutOf = int(sys.argv[6])
            else:
                print "Must specify one of the following runs:"
                print dataRuns
                exit()
        else:
            print "Must specify one of the following channels for data:"
            print dataChannels
            exit()                             
elif not isData and len(sys.argv) == 5:
    directory=storeUser+"MC/"+sys.argv[1]
    if not os.path.exists(directory):
        print "Directory specified ("+directory+") does not exist"
        exit()
                      
    if sys.argv[2] in okChannelNames:
        channelName = sys.argv[2]
        rootFileName = sys.argv[2]
        goodOptions = True
    else:
        print "Invalid channel name: " + sys.argv[2]
        exit()
    ProcessNumber = int(sys.argv[3])
    OutOf = int(sys.argv[4])
elif not isData and len(sys.argv) == 6:
    if sys.argv[1] == 'Syst':
        print "Using Systematics"
        print sys.argv[2]
        directory=storeUser+"Systs/"+sys.argv[2]
        if not os.path.exists(directory):
            print "Directory specified ("+directory+") does not exist"
            exit()                      
        if sys.argv[3] in okChannelNames:
            channelName = sys.argv[3]
            rootFileName = sys.argv[3]
            goodOptions = True
            isSyst = True
        else:
            print "Invalid channel name: " + sys.argv[3]
            print okChannelNames
            exit()
        ProcessNumber = int(sys.argv[4])
        OutOf = int(sys.argv[5])
if not goodOptions:
    print "You need 2 argumyents (directory and channel name). Something like:"
    print "mergeAndRun.py tW_Synch T_tWChannel"
    print "Or for data, 4 arguments must be specified (directory, data as channel name, and ) ! Something like:"
    print "mergeAndRun.py MuEG_Run2012B-13Jul2012-v1_v1 Data MuEG Run2012B-13Jul2012"
    print "Or for Systematics, 4 arguments must be specified (directory, data as channel name, and ) ! Something like:"
    print "mergeAndRun.py Syst TTBar_MatchingUp"    
    exit()

if ProcessNumber > OutOf:
    print "Asking for job", ProcessNumber, "out of only", OutOf,"jobs, please select a number in range of jobs"
    exit()
if ProcessNumber < 1:
    print "Asking for a job number below 1, please select a new job number"
    exit()



edmFileListFull = list()

def iterNumber(f):
    return int(f.split('/')[-1].split('_')[2])

for directory in Dirs:
    edmFileListStart = list()
    edmFileListStart = glob.glob(directory+"/edm*root")
    edmFileListStart.sort()


    maxJobNum = -1

    for i in range(len(edmFileListStart)):
        file_i = edmFileListStart[i].split('/')[-1]
        jobNum = file_i.split('_')[1]
        if int(jobNum) > maxJobNum:
            maxJobNum = int(jobNum)

    print maxJobNum


    for job in range(1,maxJobNum+1):
        jobFileList = list()    
        for i in range(len(edmFileListStart)):
            file_i = edmFileListStart[i].split('/')[-1]
            jobNum = file_i.split('_')[1]
            if job == int(jobNum):
                jobFileList.append(edmFileListStart[i])
        jobFileList.sort(key=iterNumber)

        if len(jobFileList) > 0:
            edmFileListFull.append(jobFileList[-1])

if OutOf > len(edmFileListFull):
    print "More jobs than files; requesting",OutOf,"jobs from only", len(edmFileListFull),"files"
    print "Please select fewer than",len(edmFileListFull),"jobs"
    exit()
# for file in edmFileListFull:
#     print file

edmFileList = list()
if OutOf == 1:
    edmFileList = edmFileListFull[:]
else:
    total = len(edmFileListFull)
    perJob = int((total*1.)/(OutOf*1.))
    print OutOf, "jobs from",total,"files gives",perJob,"files per job"
    if ProcessNumber == OutOf:
        StartJob = (ProcessNumber-1)*perJob
        edmFileList = edmFileListFull[StartJob:]
    else:
        StartJob = (ProcessNumber-1)*perJob
        EndJob = (ProcessNumber)*perJob
        edmFileList = edmFileListFull[StartJob:EndJob]

for file in edmFileList:
    print file

import time
time.sleep(10)
TemplateCfg=open('SingleTopSystematicsWithTrigger_tW_TEMPLATE_cfg.py','r')
TemplateCfgLines=TemplateCfg.readlines()
TemplateCfg.close()

processCount = '_'+str(ProcessNumber)+'_'+str(OutOf)

NewCfg=open('SingleTopSystematicsWithTrigger_tW_'+rootFileName+processCount+'_cfg.py','w')

for cfgLine in TemplateCfgLines:
    if 'INSERTFILENAME' in cfgLine:
        newline = ''
        for file in edmFileList:
            newline = newline+cfgLine.replace('INSERTFILENAME',file)
    elif 'REPLACECHANNELNAME' in cfgLine:        
        newline = cfgLine.replace('REPLACECHANNELNAME',channelName)
    elif 'REPLACEROOTFILENAME' in cfgLine:        
        newline = cfgLine.replace('REPLACEROOTFILENAME',rootFileName +processCount+ appendVersion)
    elif channelName == 'Data' and 'MC_instruction = True' in cfgLine:
        newline = cfgLine.replace('True','False')
    elif channelName == 'Data' and 'channel_instruction = ' in cfgLine:
        newline = cfgLine.replace('allmc','data')
    elif isSyst and 'channel_instruction = ' in cfgLine:
        newline = cfgLine.replace('allmc','systSample')
    else:
        newline = cfgLine

    NewCfg.write(newline)

NewCfg.close()

command = 'cmsRun SingleTopSystematicsWithTrigger_tW_'+rootFileName+processCount+'_cfg.py'
print command
os.system(command)

if not os.path.exists(storeUser+"Ntuples/"+currentFileVersion):
    command = "mkdir "+storeUser+"Ntuples/"+currentFileVersion
    print command
    os.system(command)

command = "mv output/ntuple_SysTrees_"+rootFileName+processCount+".root "+storeUser+"Ntuples/"+currentFileVersion+"/."
print command
os.system(command)

command = 'mv SingleTopSystematicsWithTrigger_tW_'+rootFileName+processCount+'_cfg.py OldNtupleCfgs/.'
print command
os.system(command)
