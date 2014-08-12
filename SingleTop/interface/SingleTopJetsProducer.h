#ifndef _Top_Jet_Producer_h
#define _Top_Jet_Producer_h



/**
 *\Class TopProducer
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: SingleTopJetsProducer.h,v 1.2.12.3 2012/08/15 09:36:37 oiorio Exp $
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

#include "CMGTools/External/interface/PileupJetIdentifier.h"

//class JetFlavourIdentifier;


//namespace pat {

  class SingleTopJetsProducer : public edm::EDProducer {

    public:

      explicit SingleTopJetsProducer(const edm::ParameterSet & iConfig);
      ~SingleTopJetsProducer();
      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
    //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
    private:
  

  
    edm::InputTag src_,PUFullDiscriminant_,PUFullID_,PUChargedDiscriminant_,PUChargedID_,PUIDVariables_,electronsSrc_;
    std::string cut_;
      
    typedef StringCutObjectSelector<pat::Jet> Selector;

    bool removeOverlap_;

    edm::Handle<std::vector<pat::Jet> > jets;
    edm::Handle<edm::View<pat::Jet> > vjets;
    edm::Handle<std::vector<pat::Electron> > electrons;

    edm::Handle<edm::ValueMap<StoredPileupJetIdentifier> > puIDVariables;

    edm::Handle<edm::ValueMap<float> > puFullJetIdMVA;
    edm::Handle<edm::ValueMap<int> > puFullJetIdFlag;
    edm::Handle<edm::ValueMap<float> > puChargedJetIdMVA;
    edm::Handle<edm::ValueMap<int> > puChargedJetIdFlag;
  };
//}


#endif
