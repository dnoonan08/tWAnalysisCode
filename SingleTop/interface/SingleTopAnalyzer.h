#ifndef __SINGLETOPANALYZER_H__
#define __SINGLETOPANALYZER_H__

/* \Class SingleTopAnalyzer
 *
 * \Authors M.Merola, A. Orso M. Iorio
 * 
 * \ version $Id: SingleTopAnalyzer.h,v 1.3 2010/03/18 11:34:07 oiorio Exp $
 */


//----------------- system include files
#include <memory>
#include <iostream>
#include <list>
#include <string>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>

//----------------- cmssw includes

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "JetMETCorrections/JetVertexAssociation/interface/JetVertexMain.h"
#include "DataFormats/HepMCCandidate/interface/PdfInfo.h"

//--------------------TQAF includes
/*
#include "AnalysisDataFormats/TopObjects/interface/TopObject.h"
#include "AnalysisDataFormats/TopObjects/interface/TopLepton.h"
#include "AnalysisDataFormats/TopObjects/interface/TopJet.h"
#include "AnalysisDataFormats/TopObjects/interface/TopMET.h"
#include "AnalysisDataFormats/TopObjects/interface/TopElectron.h"
#include "AnalysisDataFormats/TopObjects/interface/TopMuon.h"
*/

//--------------------PAT includes
#include "DataFormats/PatCandidates/interface/Particle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


//--------------------ROOT includes
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH2.h"



using namespace std;
using namespace edm;
using namespace reco;



class SingleTopAnalyzer : public edm::EDAnalyzer {
 public:
  explicit SingleTopAnalyzer(const edm::ParameterSet&);
  //  ~SingleTopAnalyzer();
  
  
 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  //void  EventInfo();

  string rootFileName;
  
  edm::Event*   iEvent;
  
  InputTag      electronProducer;
  InputTag      muonProducer;  
  InputTag      jetProducer;
  InputTag      metProducer;
  InputTag      topProducer;

  InputTag      MCLeptonProducer;  
  InputTag      MCJetProducer;
  InputTag      MCNeutrinoProducer;
  InputTag      MCBQuarkProducer;
  InputTag      MCLightQuarkProducer;

  bool isMCSingleTop;

  InputTag      bJetProducer,nonBJetProducer,forwardJetProducer;
  //  InputTag      trackProducer;  
  //  InputTag      EventType;
  //  InputTag      AnaType;
  

  //Data Histos
  TH1F *h_nJets;
  TH1F *h_nLeptTop;
  TH1F *h_nLept;

  TH1F *h_lepPt;
  TH1F *h_eleRelIso;
  TH1F *h_muRelIso;
  TH1F *h_jetsEta;
  TH1F *h_jetsPt;
  TH1F *h_nBTag;
  TH1F *h_bTagValueInsideEta;
  TH1F *h_nFwdJets;

  TH1F *h_thetaDiff;

  TH1F *h_wTransverseMass;
  
  //MC Histos
  TH1F *h_MCwTransverseMass;
  TH1F *h_MCLeptonPt;

  TH1F *h_MCBQuarkEta;
  TH1F *h_MCBQuarkPt;
  TH1F *h_bJetsEta;

  TH1F *h_MCLightQuarkPt;
  TH1F *h_MCLightQuarkEta;

  TH2F *h_nLepVsNBtag;
};

#endif
