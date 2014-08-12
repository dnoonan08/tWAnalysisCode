#ifndef _Top_B_Jet_Producer_h
#define _Top_B_Jet_Producer_h



/**
 *\Class TopProducer
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: SingleTopBJetsProducer.h,v 1.1 2010/10/20 15:25:51 oiorio Exp $
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

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"



//#include "TLorentzVector.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"


//class JetFlavourIdentifier;


//namespace pat {

  class SingleTopBJetsProducer : public edm::EDProducer {

    public:

      explicit SingleTopBJetsProducer(const edm::ParameterSet & iConfig);
      ~SingleTopBJetsProducer();
      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
    //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
    private:
    //    typedef StringCutObjectSelector<pat::Jet> Selector;
    
    edm::InputTag src_;
    bool veto_;
    double bThreshold_;
    //    std::string cut_;
    //typedef pat::helper::OverlapTest OverlapTest;
    //boost::ptr_vector<OverlapTest> overlaps;
    



   //std::vector<std::string> triggernames;
      
  };
//}


#endif
