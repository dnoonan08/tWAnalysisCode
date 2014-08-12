#ifndef __SINGLETOP_PUP_DUMPER_H__
#define __SINGLETOP_PUP_DUMPER_H__

/* \Class SingleTopSystematicsDumper
 *
 * \Authors A. Orso M. Iorio
 * 
 * Produces systematics histograms out of a standard Single Top n-tuple 
 * \ version $Id: SingleTopPileUpDumper.h,v 1.1 2011/07/03 20:01:52 oiorio Exp $
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
#include "FWCore/Framework/interface/EventSetup.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "JetMETCorrections/JetVertexAssociation/interface/JetVertexMain.h"
#include "DataFormats/HepMCCandidate/interface/PdfInfo.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"




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
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

//--------------------ROOT includes
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH2.h"

//lorentzVector
#include "DataFormats/Math/interface/LorentzVector.h"

//B Tag reading from DB
#include "RecoBTag/Records/interface/BTagPerformanceRecord.h"
#include "CondFormats/PhysicsToolsObjects/interface/BinningPointByMap.h"
#include "RecoBTag/PerformanceDB/interface/BtagPerformance.h"

using namespace std;
using namespace edm;
using namespace reco;



class SingleTopPileUpDumper : public edm::EDAnalyzer {
 public:
  explicit SingleTopPileUpDumper(const edm::ParameterSet&);
  //  ~SingleTopPileUpDumper();
  
  
 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  //void  EventInfo();

  // Handles

  edm::InputTag pileUpInfo_;
  edm::Handle<std::vector< PileupSummaryInfo > >  pileUpInfo;
  string channel;
  TH1F *hPileUp;  
 
};

#endif
