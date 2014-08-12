#ifndef __SINGLETOP_SYST_TREES_DUMPER_H__
#define __SINGLETOP_SYST_TREES_DUMPER_H__

/* \Class SingleTopSystematicsDumper
 *
 * \Authors A. Orso M. Iorio
 *
 * Produces systematics histograms out of a standard Single Top n-tuple
 * \ version $Id: SingleTopSystematicsTreesDumper_tW.h,v 1.1.2.5 2013/07/05 17:54:19 dnoonan Exp $
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
//#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

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

#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

#include "ReWeighting.h"
//#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h"
//#include "TopQuarkAnalysis/SingleTop/interface/Lumi3DReWeighting.h"


using namespace std;
using namespace edm;
using namespace reco;


class SingleTopSystematicsTreesDumper_tW : public edm::EDAnalyzer
{
public:
    explicit SingleTopSystematicsTreesDumper_tW(const edm::ParameterSet &);
    //  ~SingleTopSystematicsTreesDumper_tW();


private:
    virtual void analyze(const edm::Event &, const edm::EventSetup &);
    virtual void endJob();
    void initBranchVars();

    //void  EventInfo();

    //Find functions descriptions in .cc

    //Kinematic functions:
    math::PtEtaPhiELorentzVector top4Momentum(float leptonPx, float leptonPy, float leptonPz, float leptonE, float jetPx, float jetPy, float jetPz, float jetE, float metPx, float metPy);
    math::PtEtaPhiELorentzVector top4Momentum(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy);
    math::XYZTLorentzVector NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy );
    float cosThetaLJ(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top);
    float cosTheta_eta_bl(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top);

    double topMtw(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy);

  float muonHLTEff(float etaMu,string period);

    //B-weight generating functions
    double BScaleFactor(string algo, string syst_name);
    double MisTagScaleFactor(string algo, string syst_name, double sf, double eff, double sferr);
    double AntiBScaleFactor(string algo, string syst_name);
    double AntiMisTagScaleFactor(string algo, string syst_name, double sf, double eff, double sferr);
    double resolSF(double eta, string syst);
    double pileUpSF(string syst, string run);
    double pileUpSFNew();
    double bTagSF(int B);
    double bTagSF(int B, string syst);

    double EventAntiScaleFactor(string algo, string syst_name );
    double EventScaleFactor(string algo, string syst_name );
    double SFMap(string);   double SFErrMap(string);   double EFFMap(string); double EFFMap(string, string);  double EFFErrMap(string);

    void InitializeEventScaleFactorMap();
    void InitializeTurnOnReWeight(string SFFile);
    double EventScaleFactorMap(string, string);

    //Jet uncertainty as a function of eta pt and jet flavour
    double jetUncertainty(double eta, double ptCorr, int flavour);

    double jetUncertaintyNew(double eta, double ptCorr, string systematics);


    //  int nsrc;// = 16;
    //  std::vector<JetCorrectionUncertainty*> vsrc(16);



    bool flavourFilter(string c, int nb, int nc, int nl);
    int eventFlavour(string c, int nb, int nc, int nl);


    //Weight and probabilities for TurnOn curves
    double turnOnWeight (std::vector<double> probs, int njets_req);
    double turnOnReWeight (double preWeight, double pt, double tchpt);
    double jetprob(double pt, double tchp);
    double jetprob(double pt, double tchp, double eta, string syst);
    double jetprobold(double pt, double tchp, double eta, string syst);
    double jetprobpt(double pt);
    double jetprobbtag(double tchp);

    double BTagSFNew(double pt, string algo);
    double MisTagSFNew(double pt, double eta, string algo);

    double BTagSFErrNew(double pt, string algo);
    double MisTagSFErrNewUp(double pt, double eta, string algo);
    double MisTagSFErrNewDown(double pt, double eta, string algo);
    double EFFMapNew(double btag, string algo);

    double turnOnProbs (string syst, int njets_req);
    void pushJetProbs (double pt, double btag, double eta);
    void resetWeightsDoubles();


    //Define vector of required systematics to loop on
    std::vector<std::string> systematics, rate_systematics;


    //Define parameterSet to change from channel to channel
    edm::ParameterSet channelInfo;
    std::string channel;
    double crossSection, originalEvents, finalLumiA, finalLumiB, finalLumiC, finalLumiD, MTWCut, RelIsoCut;
    edm::Event   *iEvent;

    //  std::vector<float> leptonsPt,leptonsPhi,leptonsPz,leptonsEta,jetsPt,jetsPx,jetsPy,jetsPz,jetsEta,jetEnergy,jetsBTagAlgo,jetsAntiBTagAlgo,METPt,METPhi;

    //InputTags
    edm::InputTag muonsPt_,
        muonsPhi_,
        muonsEta_,
        muonsEnergy_,
        muonsCharge_,
        muonsDB_,
        muonsDZ_,
        muonsDXY_,
        muonsRelIso_,
        muonsDeltaCorrectedRelIso_,
        muonsRhoCorrectedRelIso_,
        muonsChargedHadronIso_,
        muonsPUChargedHadronIso_,
        muonsNeutralHadronIso_,
        muonsPhotonIso_,
        muonsSumChargedHadronPtR03_,
        muonsSumChargedParticlePtR03_,
        muonsSumNeutralHadronEtR03_,
        muonsSumPhotonEtR03_,
        muonsSumNeutralHadronEtHighThresholdR03_,
        muonsSumPhotonEtHighThresholdR03_,
        muonsSumPUPtR03_,
        muonsSumChargedHadronPtR04_,
        muonsSumChargedParticlePtR04_,
        muonsSumNeutralHadronEtR04_,
        muonsSumPhotonEtR04_,
        muonsSumNeutralHadronEtHighThresholdR04_,
        muonsSumPhotonEtHighThresholdR04_,
        muonsSumPUPtR04_,

        muonsGenPDGId_,
        muonsHasBParent_,
        muonsHasTParent_,
        muonsHasZParent_,
        muonsHasWParent_,
        muonsHasHParent_,

        electronsPt_,
        electronsPhi_,
        electronsEta_,
        electronsEnergy_,
        electronsCharge_,
        electronsDB_,
        electronsDZ_,
        electronsDXY_,
        electronsMVAID_,
        electronsMVAIDNonTrig_,
        electronsRelIso_,
        electronsDeltaCorrectedRelIso_,
        electronsRhoCorrectedRelIso_,
        electronsEleId70cIso_,
        electronsEleId80cIso_,
        electronsEleId90cIso_,
        electronsEleId95cIso_,
        electronsTrackerExpectedInnerHits_,
        electronsSuperClusterEta_,
        electronsECALPt_,
        electronsChargedHadronIso_,
        electronsPUChargedHadronIso_,
        electronsNeutralHadronIso_,
        electronsPhotonIso_,
        electronsPassConversionVeto_,

        electronsGenPDGId_,
        electronsHasBParent_,
        electronsHasTParent_,
        electronsHasZParent_,
        electronsHasWParent_,
        electronsHasHParent_,

        vertexX_,
        vertexY_,
        vertexZ_,
        vertexrho_,
        vertexchi_,
        vertexNDOF_,
        vertexIsFake_,

        jetsPt_,
        jetsEta_,
        jetsPhi_,
        jetsEnergy_,
        jetsCSV_,
        jetsTCHP_,
        jetsRMS_,
        jetsNumDaughters_,
        jetsCHEmEn_,
        jetsCHHadEn_,
        jetsCHMult_,
        jetsNeuEmEn_,
        jetsNeuHadEn_,
        jetsNeuMult_,
        jetsPUChargedDiscr_,
        jetsPUChargedWP_,
        jetsPUFullDiscr_,
        jetsPUFullWP_,
        jetsBeta_,
        jetsBetaStar_,
        jetsFlavour_,
        jetsDZ_,
        genjetsPt_,
        genjetsEta_,

        genPartPt_,
        genPartPdgId_,

        jetsGenPDGId_,
        jetsHasBParent_,
        jetsHasTParent_,
        jetsHasZParent_,
        jetsHasWParent_,
        jetsHasHParent_,


        ktJetsForIsoRho_,

        METPt_,
        METPhi_,
        UnclMETPx_,
        UnclMETPy_,

        n0_,
        np1_,
        nm1_,
        x1_,
        x2_,
        id1_,
        id2_,
        scalePDF_ ;



    // Handles
    edm::Handle<std::vector<float> > muonsPt,
        muonsPhi,
        muonsEta,
        muonsEnergy,
        muonsCharge,
        muonsDeltaCorrectedRelIso,
        muonsRhoCorrectedRelIso,
        muonsRelIso,
        muonsDB,
        muonsDZ,
        muonsDXY,
        muonsChargedHadronIso,
        muonsPUChargedHadronIso,
        muonsNeutralHadronIso,
        muonsPhotonIso,
        muonsSumChargedHadronPtR03,
        muonsSumChargedParticlePtR03,
        muonsSumNeutralHadronEtR03,
        muonsSumPhotonEtR03,
        muonsSumNeutralHadronEtHighThresholdR03,
        muonsSumPhotonEtHighThresholdR03,
        muonsSumPUPtR03,
        muonsSumChargedHadronPtR04,
        muonsSumChargedParticlePtR04,
        muonsSumNeutralHadronEtR04,
        muonsSumPhotonEtR04,
        muonsSumNeutralHadronEtHighThresholdR04,
        muonsSumPhotonEtHighThresholdR04,
        muonsSumPUPtR04,

        muonsGenPDGId,
        muonsHasBParent,
        muonsHasTParent,
        muonsHasZParent,
        muonsHasWParent,
        muonsHasHParent,      

        electronsPt,
        electronsPhi,
        electronsEta,
        electronsEnergy,
        electronsCharge,
        electronsDeltaCorrectedRelIso,
        electronsRhoCorrectedRelIso,
        electronsRelIso,
        electronsDB,
        electronsDZ,
        electronsDXY,
        electronsMVAID,
        electronsMVAIDNonTrig,
        electronsEleId70cIso,
        electronsEleId80cIso,
        electronsEleId90cIso,
        electronsEleId95cIso,
        electronsTrackerExpectedInnerHits,
        electronsSuperClusterEta,
        electronsECALPt,
        electronsChargedHadronIso,
        electronsPUChargedHadronIso,
        electronsNeutralHadronIso,
        electronsPhotonIso,
        electronsPassConversionVeto,
      
        electronsGenPDGId,
        electronsHasBParent,
        electronsHasTParent,
        electronsHasZParent,
        electronsHasWParent,
        electronsHasHParent,

        jetsPt,
        jetsEta,
        jetsPhi,
        jetsEnergy,
        jetsCSV,
        jetsTCHP,
        jetsRMS,
        jetsNumDaughters,
        jetsCHEmEn,
        jetsCHHadEn,
        jetsCHMult,
        jetsNeuEmEn,
        jetsNeuHadEn,
        jetsNeuMult,
        jetsPUChargedDiscr,
        jetsPUChargedWP,
        jetsPUFullDiscr,
        jetsPUFullWP,
        jetsBeta,
        jetsBetaStar,
        jetsFlavour,
        jetsDZ,

        jetsGenPDGId,
        jetsHasBParent,
        jetsHasTParent,
        jetsHasZParent,
        jetsHasWParent,
        jetsHasHParent,

        METPhi,
        METPt,

        vertexX,
        vertexY,
        vertexZ,
        vertexrho,
        vertexchi,
        
        genPartPt,
        genPartPdgId;

    edm::Handle<std::vector<int> > vertexNDOF;

    edm::Handle<std::vector<bool> > vertexIsFake;

    edm::Handle<std::vector<double> > genjetsPt,
      genjetsEta; 
    
    edm::Handle<double> UnclMETPx,
      UnclMETPy, ktJetsForIsoRho;

    edm::Handle<int > n0, nm1, np1;

    int npv;

    int passingPreselection, passingLepton, passingMuonVeto, passingLeptonVeto, passingJets, passingBJets, passingMET;


    int nVertices, nGoodVertices;

    edm::Handle< float > x1h, x2h, scalePDFh;
    edm::Handle< int > id1h, id2h;

    //Part for BTagging payloads
    edm::ESHandle<BtagPerformance> perfMHP;
    edm::ESHandle<BtagPerformance> perfMHPM;
    edm::ESHandle<BtagPerformance> perfMHE;
    edm::ESHandle<BtagPerformance> perfBHP;
    edm::ESHandle<BtagPerformance> perfBHPM;
    edm::ESHandle<BtagPerformance> perfBHE;


    //Part for JEC and JES
    //Part for JEC and JES
    string JEC_PATH;
    //  JetResolution *ptResol;
    edm::FileInPath fip;
    JetCorrectionUncertainty *jecUnc;

    JetCorrectionUncertainty *jecUnc__;

    JetCorrectionUncertainty *jecUncCorrelationGroupInSitu;
    JetCorrectionUncertainty *jecUncCorrelationGroupFlavor;
    JetCorrectionUncertainty *jecUncCorrelationGroupIntercalibration;
    JetCorrectionUncertainty *jecUncCorrelationGroupUncorrelated;

    double JES_SW, JES_b_cut, JES_b_overCut;



    //4-momenta vectors definition
    /*  std::vector<math::PtEtaPhiELorentzVector>
      jets,
      loosejets,
      bjets,
      antibjets;*/
    math::PtEtaPhiELorentzVector leptons[3],
         qcdLeptons[3],
         jets[10],
         jetsNoSyst[10],
         bjets[10],
         antibjets[10];
    int flavours[10];

    float  pdf_weights_alternate_set_1, pdf_weights_alternate_set_2;
    //  float recorrection_weights[7][7];
    //  float pt_bin_extremes[8];
    //  float tchpt_bin_extremes[8];

    TH2D histoSFs;

    math::PtEtaPhiELorentzVector leptonPFour;

    //Definition of trees

    map<string, TTree *> trees;


    enum Bin
    {
        ZeroT = 0,
        OneT = 1,
        TwoT = 2,
        ZeroT_QCD = 3,
        OneT_QCD = 4,
        TwoT_QCD = 5
    };


    //Other variables definitions
    double bTagThreshold, maxPtCut;
    size_t bScanSteps;


    bool doQCD_, doPDF_, takeBTagSFFromDB_;
    //To be changed in 1 tree, now we keep
    //because we have no time to change and debug
    map<string, TTree *> treesScan[10];
    map<string, TTree *> treesScanQCD[10];
    //Vectors of b-weights
    vector< double > b_weight_tag_algo1,
    b_weight_tag_algo2,
    b_weight_antitag_algo1,
    b_weight_antitag_algo2,
    b_discriminator_value_tag_algo1,
    b_discriminator_value_antitag_algo2;

    //Variables to use as trees references

    //Variables to use as trees references

    std::vector<double> _muonPt_;
    std::vector<double> _muonEta_;
    std::vector<double> _muonPhi_;
    std::vector<double> _muonEnergy_;
    std::vector<double> _muonCharge_;
    std::vector<double> _muonRelIso_;
    std::vector<double> _muonRhoCorrectedRelIso_;
    std::vector<double> _muonDeltaCorrectedRelIso_;
    std::vector<double> _muonPVDz_;
    std::vector<double> _muonPVDxy_;
    std::vector<double> _muonDB_;
    std::vector<double> _muonChargedHadronIso_;
    std::vector<double> _muonPUChargedHadronIso_;
    std::vector<double> _muonNeutralHadronIso_;
    std::vector<double> _muonPhotonIso_;
    std::vector<double> _muonSumChargedHadronPtR03_;
    std::vector<double> _muonSumChargedParticlePtR03_;
    std::vector<double> _muonSumNeutralHadronEtR03_;
    std::vector<double> _muonSumPhotonEtR03_;
    std::vector<double> _muonSumNeutralHadronEtHighThresholdR03_;
    std::vector<double> _muonSumPhotonEtHighThresholdR03_;
    std::vector<double> _muonSumPUPtR03_;
    std::vector<double> _muonSumChargedHadronPtR04_;
    std::vector<double> _muonSumChargedParticlePtR04_;
    std::vector<double> _muonSumNeutralHadronEtR04_;
    std::vector<double> _muonSumPhotonEtR04_;
    std::vector<double> _muonSumNeutralHadronEtHighThresholdR04_;
    std::vector<double> _muonSumPhotonEtHighThresholdR04_;
    std::vector<double> _muonSumPUPtR04_;
    std::vector<double> _muonGenPDGId_;
    std::vector<double> _muonHasBParent_;
    std::vector<double> _muonHasTParent_;
    std::vector<double> _muonHasZParent_;
    std::vector<double> _muonHasWParent_;
    std::vector<double> _muonHasHParent_;

    std::vector<double> _electronPt_;
    std::vector<double> _electronEta_;
    std::vector<double> _electronPhi_;
    std::vector<double> _electronEnergy_;
    std::vector<double> _electronCharge_;
    std::vector<double> _electronRelIso_;
    std::vector<double> _electronRhoCorrectedRelIso_;
    std::vector<double> _electronDeltaCorrectedRelIso_;
    std::vector<double> _electronPVDz_;
    std::vector<double> _electronPVDxy_;
    std::vector<double> _electronDB_;
    std::vector<double> _electronMVAID_;
    std::vector<double> _electronMVAIDNonTrig_;
    std::vector<double> _electronEleId70cIso_;
    std::vector<double> _electronEleId80cIso_;
    std::vector<double> _electronEleId90cIso_;
    std::vector<double> _electronEleId95cIso_;
    std::vector<double> _electronTrackerExpectedInnerHits_;
    std::vector<double> _electronSuperClusterEta_;
    std::vector<double> _electronECALPt_;
    std::vector<double> _electronChargedHadronIso_;
    std::vector<double> _electronPUChargedHadronIso_;
    std::vector<double> _electronNeutralHadronIso_;
    std::vector<double> _electronPhotonIso_;
    std::vector<double> _electronPassConversionVeto_;
    
    std::vector<double> _electronGenPDGId_;
    std::vector<double> _electronHasBParent_;
    std::vector<double> _electronHasTParent_;
    std::vector<double> _electronHasZParent_;
    std::vector<double> _electronHasWParent_;
    std::vector<double> _electronHasHParent_;

    std::vector<double> _jetPt_;
    std::vector<double> _jetEta_;
    std::vector<double> _jetPhi_;
    std::vector<double> _jetEnergy_;
    std::vector<double> _jetNumDaughters_;
    std::vector<double> _jetCHEmEn_;
    std::vector<double> _jetCHHadEn_;
    std::vector<double> _jetCHMult_;
    std::vector<double> _jetNeuEmEn_;
    std::vector<double> _jetNeuHadEn_;
    std::vector<double> _jetNeuMult_;
    std::vector<double> _jetCSV_;
    std::vector<double> _jetTCHP_;
    std::vector<double> _jetRMS_;
    std::vector<double> _jetPUChargedDiscr_;
    std::vector<double> _jetPUChargedWP_;
    std::vector<double> _jetPUFullDiscr_;
    std::vector<double> _jetPUFullWP_;
    std::vector<double> _jetBeta_;
    std::vector<double> _jetBetaStar_;
    std::vector<double> _jetFlavour_;
    std::vector<double> _jetDZ_;

    std::vector<double> _jetGenPDGId_;
    std::vector<double> _jetHasBParent_;
    std::vector<double> _jetHasTParent_;
    std::vector<double> _jetHasZParent_;
    std::vector<double> _jetHasWParent_;
    std::vector<double> _jetHasHParent_;

    std::vector<double> _genjetPt_;
    std::vector<double> _genjetEta_;
    std::vector<double> _jetUncorrPt_;

    double _ktJetsForIsoRho_;

    double _MetPhi_;
    double _MetPt_;
    double _UncorrMetPt_;
    double _UnclMETPx_;
    double _UnclMETPy_;

    double _vertexX_;
    double _vertexY_;
    double _vertexZ_;
    double _vertexrho_;
    double _vertexchi_;
    int _vertexNDOF_;
    bool _vertexIsFake_;

    int _runNum_;
    int _lumiNum_;
    int _eventNum_;
    double _weight_;
    double _weightA_;
    double _weightB_;
    double _weightC_;
    double _weightD_;
    double _PUWeight_;
    double _PUWeightA_;
    double _PUWeightB_;
    double _PUWeightC_;
    double _PUWeightD_;
    double _PUWeightNew_;
    double _TopPtweight_;
    double _scalePDF_;
    double _PDF_x1_;
    double _PDF_x2_;
    int _PDF_id1_;
    int _PDF_id2_;
    std::vector<double> _PDF_weights_;



  
    double etaTree, etaTree2, cosTree, cosBLTree, topMassTree, totalWeightTree, weightTree, mtwMassTree, lowBTagTree, highBTagTree, maxPtTree, minPtTree, topMassLowBTagTree, topMassBestTopTree, topMassMeas, bWeightTree, PUWeightTree, turnOnWeightTree, limuWeightTree, turnOnReWeightTree, miscWeightTree, lepEff, lepEffB, topMtwTree, HT ;
    double PUWeightTreeNew;

    //Weights for systematics
    double bWeightTreeBTagUp,
           bWeightTreeMisTagUp,
           bWeightTreeBTagDown,
           bWeightTreeMisTagDown,
           PUWeightTreePUUp,
           PUWeightTreePUDown,
           turnOnWeightTreeJetTrig1Up,
           turnOnWeightTreeJetTrig2Up,
           turnOnWeightTreeJetTrig3Up,
           turnOnWeightTreeJetTrig1Down,
           turnOnWeightTreeJetTrig2Down,
           turnOnWeightTreeJetTrig3Down,
           turnOnWeightTreeBTagTrig1Up,
           turnOnWeightTreeBTagTrig2Up,
           turnOnWeightTreeBTagTrig3Up,
           turnOnWeightTreeBTagTrig1Down,
           turnOnWeightTreeBTagTrig2Down,
           turnOnWeightTreeBTagTrig3Down;

  int nJ, nJNoPU, nJCentral, nJCentralNoPU, nJForward, nJForwardNoPU, nTCHPT, nCSVT, nCSVM;
    double w1TCHPT, w2TCHPT, w1CSVT, w2CSVT, w1CSVM, w2CSVM;

    int runTree, eventTree, lumiTree, chargeTree, electronID, bJetFlavourTree, fJetFlavourTree, eventFlavourTree, puZero, firstJetFlavourTree, secondJetFlavourTree, thirdJetFlavourTree;

  double lepPt, lepEta, lepPhi, lepRelIso, lepDeltaCorrectedRelIso, lepRhoCorrectedRelIso, fJetPhi, fJetPt, fJetEta, fJetE, bJetPt, bJetEta, bJetPhi, bJetE, metPt, metPhi, topPt, topPhi, topEta, topE, totalEnergy, totalMomentum, fJetBTag, bJetBTag, vtxZ, fJetPUID, fJetPUWP, bJetPUID, bJetPUWP, firstJetPt, firstJetEta, firstJetPhi, firstJetE, secondJetPt, secondJetEta, secondJetPhi, secondJetE, thirdJetPt, thirdJetEta, thirdJetPhi, thirdJetE,fJetBeta,fJetDZ,fJetRMS,bJetBeta,bJetDZ,bJetRMS;


    //Not used anymore:
    double loosePtCut, resolScale ;
    bool doPU_, doTurnOn_, doResol_ , doGen_;

    edm::LumiReWeighting LumiWeights_, LumiWeightsUp_, LumiWeightsDown_;
    edm::LumiReWeighting LumiWeightsA_, LumiWeightsB_, LumiWeightsC_, LumiWeightsD_;
    edm::LumiReWeighting LumiWeightsAUp_, LumiWeightsBUp_, LumiWeightsCUp_, LumiWeightsDUp_;
    edm::LumiReWeighting LumiWeightsADown_, LumiWeightsBDown_, LumiWeightsCDown_, LumiWeightsDDown_;
    std::string mcPUFile_, dataPUFile_, puHistoName_;

    edm::ReWeighting NewPUWeights_;
    std::string PUFileNew_;

    std::vector<double> jetprobs,
        jetprobs_j1up,
        jetprobs_j2up,
        jetprobs_j3up,
        jetprobs_b1up,
        jetprobs_b2up,
        jetprobs_b3up,
        jetprobs_j1down,
        jetprobs_j2down,
        jetprobs_j3down,
        jetprobs_b1down,
        jetprobs_b2down,
        jetprobs_b3down ;

    double leptonRelIsoQCDCutUpper, leptonRelIsoQCDCutLower;
    bool gotLeptons, gotJets, gotMets, gotLooseLeptons, gotPU, gotQCDLeptons, gotPV;

  int nb, nc, nudsg, ntchpt_tags, ncsvm_tags, ncsvt_tags,ncsvl_tags,
        nbNoSyst, ncNoSyst, nudsgNoSyst,
        ntchpt_antitags, ntchpm_tags, ntchel_tags, ntche_antitags, ntight_tags;

    string algo_;

    double TCHPM_LMisTagUp,  TCHPM_BBTagUp, TCHPM_CBTagUp, TCHPM_LMisTagDown, TCHPM_BBTagDown, TCHPM_CBTagDown;
    double TCHPM_LAntiMisTagUp,  TCHPM_BAntiBTagUp, TCHPM_CAntiBTagUp, TCHPM_LAntiMisTagDown, TCHPM_BAntiBTagDown, TCHPM_CAntiBTagDown;
    double TCHPM_C,  TCHPM_B, TCHPM_L;
    double TCHPM_CAnti,  TCHPM_BAnti, TCHPM_LAnti;

    double TCHPT_LMisTagUp,  TCHPT_BBTagUp, TCHPT_CBTagUp, TCHPT_LMisTagDown, TCHPT_BBTagDown, TCHPT_CBTagDown;
    double TCHPT_LAntiMisTagUp,  TCHPT_BAntiBTagUp, TCHPT_CAntiBTagUp, TCHPT_LAntiMisTagDown, TCHPT_BAntiBTagDown, TCHPT_CAntiBTagDown;
    double TCHPT_C,  TCHPT_B, TCHPT_L;
    double TCHPT_CAnti,  TCHPT_BAnti, TCHPT_LAnti;


    double TCHEL_LMisTagUp,  TCHEL_BBTagUp, TCHEL_CBTagUp, TCHEL_LMisTagDown, TCHEL_BBTagDown, TCHEL_CBTagDown;
    double TCHEL_LAntiMisTagUp,  TCHEL_BAntiBTagUp, TCHEL_CAntiBTagUp, TCHEL_LAntiMisTagDown, TCHEL_BAntiBTagDown, TCHEL_CAntiBTagDown;
    double TCHEL_C,  TCHEL_B, TCHEL_L;
    double TCHEL_CAnti,  TCHEL_BAnti, TCHEL_LAnti;

    double facBTagErr;

    class BTagWeight
    {
    public:
        struct JetInfo
        {
            JetInfo(float mceff, float datasf) : eff(mceff), sf(datasf) {}
            float eff;
            float sf;
        };
        BTagWeight():
            minTags(0), maxTags(0)
        {
            ;
        }
        BTagWeight(int jmin, int jmax) :
            maxTags(jmax), minTags(jmin) {}

      bool filter(int t);
      float weight(vector<JetInfo> jets, int tags);
      float weightWithVeto(vector<JetInfo> jetsTags, int tags, vector<JetInfo> jetsVetoes, int vetoes);
    private:
        int maxTags;
        int minTags;
    };

    vector<BTagWeight::JetInfo> jsfshpt, jsfshel,
           jsfshpt_b_tag_up, jsfshel_b_tag_up,
           jsfshpt_mis_tag_up, jsfshel_mis_tag_up,
           jsfshpt_b_tag_down, jsfshel_b_tag_down,
           jsfshpt_mis_tag_down, jsfshel_mis_tag_down,
           jsfshptNoSyst, jsfshelNoSyst; // bjs,cjs,ljs;


    vector<BTagWeight::JetInfo> jsfscsvt, jsfscsvm,
           jsfscsvt_b_tag_up, jsfscsvm_b_tag_up,
           jsfscsvt_mis_tag_up, jsfscsvm_mis_tag_up,
           jsfscsvt_b_tag_down, jsfscsvm_b_tag_down,
           jsfscsvt_mis_tag_down, jsfscsvm_mis_tag_down,
           jsfscsvtNoSyst, jsfscsvmNoSyst; // bjs,cjs,ljs;



    BTagWeight b_tchpt_0_tags,
               b_tchpt_1_tag,
               b_tchpt_2_tags;

    BTagWeight b_csvm_0_tags,
               b_csvm_1_tag,
               b_csvm_2_tags;

    BTagWeight b_csvt_0_tags,
               b_csvt_1_tag,
               b_csvt_2_tags;

    double b_weight_tchpt_0_tags,
           b_weight_tchpt_1_tag,
           b_weight_tchpt_2_tags;

    double b_weight_csvm_0_tags,
           b_weight_csvm_1_tag,
           b_weight_csvm_2_tags;

    double b_weight_csvt_0_tags,
           b_weight_csvt_1_tag,
           b_weight_csvt_2_tags;

    float x1, x2, Q2, scalePDF;
    int id1, id2;

  bool isFirstEvent, doReCorrection_, doLooseBJetVeto_;

    vector<JetCorrectorParameters > *vParData;
    FactorizedJetCorrector *JetCorrectorData;
    vector<JetCorrectorParameters > vParMC;
    FactorizedJetCorrector *JetCorrectorMC;
};

#endif
