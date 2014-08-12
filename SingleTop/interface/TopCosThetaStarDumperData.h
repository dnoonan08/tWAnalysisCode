#ifndef _Top_CosThetaStarDumperData_h
#define _Top_CosThetaStarDumperData_h



/**
 *\Class TopCosThetaStarDumperData
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: TopCosThetaStarDumperData.h,v 1.1 2010/12/10 14:14:30 oiorio Exp $
 *
 *
*/



#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "FWCore/ServiceRegistry/interface/Service.h" 


#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "FWCore/ParameterSet/interface/InputTag.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/PatCandidates/interface/UserData.h"
#include "PhysicsTools/PatAlgos/interface/PATUserDataHelper.h"


#include "DataFormats/PatCandidates/interface/Lepton.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"

#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"

//#include "TLorentzVector.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"


//class JetFlavourIdentifier;


//namespace pat {

  class TopCosThetaStarDumperData : public edm::EDProducer {

    public:

      explicit TopCosThetaStarDumperData(const edm::ParameterSet & iConfig);
      ~TopCosThetaStarDumperData();
      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
    //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
    private:
    
    edm::InputTag topsSrc_,jetsSrc_,tChanSrc_;
    
  };
//}


#endif
