#ifndef __SINGLETOP_SYST_DUMPER_H__
#define __SINGLETOP_SYST_DUMPER_H__

/* \Class SingleTopSystematicsDumper
 *
 * \Authors A. Orso M. Iorio
 * 
 * Produces systematics histograms out of a standard Single Top n-tuple 
 * \ version $Id: SingleTopSystematicsDumper.h,v 1.3 2011/04/23 22:59:19 oiorio Exp $
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



class SingleTopSystematicsDumper : public edm::EDAnalyzer {
 public:
  explicit SingleTopSystematicsDumper(const edm::ParameterSet&);
  //  ~SingleTopSystematicsDumper();
  
  
 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  //void  EventInfo();

  math::XYZTLorentzVector top4Momentum(float leptonPx, float leptonPy, float leptonPz,float leptonE, float jetPx, float jetPy, float jetPz,float jetE, float metPx, float metPy);

  math::XYZTLorentzVector top4Momentum(math::XYZTLorentzVector lepton, math::XYZTLorentzVector jet, float metPx, float metPy);
  std::vector<math::XYZTLorentzVector> NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy );


  float cosThetaLJ(math::XYZTLorentzVector lepton, math::XYZTLorentzVector jet, math::XYZTLorentzVector top);

  double BScaleFactor(string algo,string syst_name); 
  double MisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr);
  double jetUncertainty(double eta, double ptCorr, int flavor);
  
  string rootFileName;

  std::vector<std::string> systematics,rate_systematics;

  edm::ParameterSet channelInfo;
  std::string channel;
  double crossSection,originalEvents,finalLumi,MTWCut; 
  edm::Event*   iEvent;
  
  double loosePtCut ;
  //  std::vector<float> leptonsPt,leptonsPhi,leptonsPz,leptonsEta,jetsPt,jetsPx,jetsPy,jetsPz,jetsEta,jetEnergy,jetsBTagAlgo,jetsAntiBTagAlgo,METPt,METPhi;
  
  //InputTags
  edm::InputTag leptonsPx_,leptonsPy_,leptonsPz_,leptonsEnergy_,leptonsCharge_,jetsPx_,jetsPy_,jetsPz_,jetsEnergy_,jetsBTagAlgo_,jetsCorrTotal_,jetsAntiBTagAlgo_,METPt_,METPhi_,jetsFlavour_,UnclMETPx_,UnclMETPy_;

  // Handles
  edm::Handle<std::vector<float> > leptonsPx,
   leptonsPy,
   leptonsPz,
   leptonsEnergy,
   leptonsCharge,
   jetsPz,
   jetsPx,
   jetsPy,
   jetsEnergy,
   jetsBTagAlgo,
   jetsAntiBTagAlgo,
   jetsFlavour,
   jetsCorrTotal,
   METPhi,
   METPt;
  
  edm::Handle< double > UnclMETPx,UnclMETPy;


  //Part for BTagging payloads
  edm::ESHandle<BtagPerformance> perfHP;
  edm::ESHandle<BtagPerformance> perfHE;

  //Part for JEC and JES
  string JEC_PATH;
  edm::FileInPath fip;
  JetCorrectionUncertainty *jecUnc;
  double JES_SW, JES_b_cut, JES_b_overCut;

  //Vectors definition  
  
  std::vector<math::XYZTLorentzVector> leptons;
  std::vector<math::XYZTLorentzVector> jets;
  std::vector<math::XYZTLorentzVector> loosejets;
  std::vector<math::XYZTLorentzVector> bjets;
  std::vector<math::XYZTLorentzVector> antibjets;
  
  //Base histograms 
  map<string, TH1F*> CosThetaLJ;
  map<string, TH1F*> ForwardJetEta;
  map<string, TH1F*> MTW;
  map<string, TH1F*> TopMass;
  
  map<string, TH1F*> CosThetaLJWSample;
  map<string, TH1F*> ForwardJetEtaWSample;
  map<string, TH1F*> MTWWSample;
  map<string, TH1F*> TopMassWSample;

  //Part for Asymmetry

  map<string, TH1F*> CosThetaLJPlus;
  map<string, TH1F*> ForwardJetEtaPlus;
  map<string, TH1F*> MTWPlus;
  map<string, TH1F*> TopMassPlus;
  
  map<string, TH1F*> CosThetaLJWSamplePlus;
  map<string, TH1F*> ForwardJetEtaWSamplePlus;
  map<string, TH1F*> MTWWSamplePlus;
  map<string, TH1F*> TopMassWSamplePlus;

  map<string, TH1F*> CosThetaLJMinus;
  map<string, TH1F*> ForwardJetEtaMinus;
  map<string, TH1F*> MTWMinus;
  map<string, TH1F*> TopMassMinus;

  map<string, TH1F*> CosThetaLJWSampleMinus;
  map<string, TH1F*> ForwardJetEtaWSampleMinus;
  map<string, TH1F*> MTWWSampleMinus;
  map<string, TH1F*> TopMassWSampleMinus;

 
};

#endif
