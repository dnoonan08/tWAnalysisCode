#ifndef _Top_Producer_h
#define _Top_Producer_h



/**
 *\Class TopProducer
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: TopProducer.h,v 1.7 2010/09/07 14:32:43 oiorio Exp $
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

  class TopProducer : public edm::EDProducer {

    public:

      explicit TopProducer(const edm::ParameterSet & iConfig);
      ~TopProducer();
      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
    //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
    private:
    std::vector<math::XYZTLorentzVector> Nu4Momentum(const reco::Candidate & Lepton,const reco::Candidate & MET);
    
    edm::InputTag electronsSrc_,muonsSrc_,jetsSrc_,METsSrc_;
    
    bool useNegativeDeltaSolutions_,usePositiveDeltaSolutions_,usePzMinusSolutions_,usePzPlusSolutions_,usePzAbsValMinimumSolutions_,useMetForNegativeSolutions_,usePxMinusSolutions_,usePxPlusSolutions_;   

 



   //std::vector<std::string> triggernames;
      
  };
//}


#endif
