/*
*\Author:  O.Iorio
*
*
*
*\version  $Id: SingleTopPileUpDumper.cc,v 1.2 2011/07/04 00:56:22 oiorio Exp $ 
*/
// This analyzer dumps the histograms for all systematics listed in the cfg file 
//
//
//

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopPileUpDumper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Common/interface/TriggerNames.h"
//#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
//#include "FWCore/Framework/interface/TriggerNames.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include <Math/VectorUtil.h>
//#include "CommonTools/CandUtils/interface/Booster.h"
#include <sstream> //libreria per usare stringstream

#include "DataFormats/Math/interface/deltaR.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"

SingleTopPileUpDumper::SingleTopPileUpDumper(const edm::ParameterSet& iConfig)
{
  channel = iConfig.getParameter<std::string >("channel"); 
  
  Service<TFileService> fs;
  hPileUp = fs->make<TH1F>(("PileUp"+channel).c_str(),("PileUp"+channel).c_str(),51,-0.5,50.5);
}

void SingleTopPileUpDumper::analyze(const Event& iEvent, const EventSetup& iSetup)
{

  iEvent.getByLabel(edm::InputTag("addPileupInfo"), pileUpInfo);
  
  // cout << " test pupinfo size " << pileUpInfo->size()<< endl;
  
  std::vector<PileupSummaryInfo>::const_iterator PVI;
  
  int npv = -1;
  for(PVI = pileUpInfo->begin(); PVI != pileUpInfo->end(); ++PVI) {
    int BX = PVI->getBunchCrossing();
    
    if(BX == 0) { 
      npv = PVI->getPU_NumInteractions();
      continue;
    }
  }
 

  hPileUp->Fill(npv);
  //  iEvent.getByLabel(pileUpInfo_,pileUpInfo);
  //to retrieve the value of scale factor and its error
}

//EndJob filling rate systematics trees
void SingleTopPileUpDumper::endJob(){
  
}


//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopPileUpDumper);
