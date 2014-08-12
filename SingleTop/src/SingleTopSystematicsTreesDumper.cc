/*
*\Author:  O.Iorio
*
*
*
*\version  $Id: SingleTopSystematicsTreesDumper.cc,v 1.12.2.18.2.15 2012/08/23 13:37:22 atiko Exp $
*/
// This analyzer dumps the histograms for all systematics listed in the cfg file
//
//
//

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopSystematicsTreesDumper.h"
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
//#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"

#include "../interface/ReWeighting.h"

namespace LHAPDF
{
void initPDFSet(int nset, const std::string &filename, int member = 0);
int numberPDF(int nset);
void usePDFMember(int nset, int member);
double xfx(int nset, double x, double Q, int fl);
double getXmin(int nset, int member);
double getXmax(int nset, int member);
double getQ2min(int nset, int member);
double getQ2max(int nset, int member);
void extrapolate(bool extrapolate = true);
}

SingleTopSystematicsTreesDumper::SingleTopSystematicsTreesDumper(const edm::ParameterSet &iConfig)
{
    //MCLightQuarkProducer   = iConfig.getParameter<InputTag>("MCLightQuarkProducer");
    systematics = iConfig.getUntrackedParameter<std::vector<std::string> >("systematics");
    rate_systematics = iConfig.getUntrackedParameter<std::vector<std::string> >("rateSystematics");
    //Channel information

    channelInfo = iConfig.getParameter<edm::ParameterSet>("channelInfo");
    //Cross section, name and number of events
    channel = channelInfo.getUntrackedParameter<string>("channel");
    crossSection = channelInfo.getUntrackedParameter<double>("crossSection");
    originalEvents = channelInfo.getUntrackedParameter<double>("originalEvents");
    finalLumi = channelInfo.getUntrackedParameter<double>("finalLumi");
    MTWCut = channelInfo.getUntrackedParameter<double>("MTWCut", 50);


    RelIsoCut = channelInfo.getUntrackedParameter<double>("RelIsoCut", 0.1);
    loosePtCut = channelInfo.getUntrackedParameter<double>("loosePtCut", 40);

    maxPtCut = iConfig.getUntrackedParameter<double>("maxPtCut", 40);

    //tight leptons
    leptonsFlavour_ =  iConfig.getUntrackedParameter< std::string >("leptonsFlavour");



    //  dataPUFile_ =  iConfig.getUntrackedParameter< std::string >("dataPUFile","pileUpDistr.root");
    //  mcPUFile_ =  iConfig.getUntrackedParameter< std::string >("mcPUFile","pileupdistr_TChannel.root");

    leptonsPt_ =  iConfig.getParameter< edm::InputTag >("leptonsPt");
    leptonsPhi_ =  iConfig.getParameter< edm::InputTag >("leptonsPhi");
    leptonsEta_ =  iConfig.getParameter< edm::InputTag >("leptonsEta");
    leptonsEnergy_ =  iConfig.getParameter< edm::InputTag >("leptonsEnergy");
    leptonsCharge_ =  iConfig.getParameter< edm::InputTag >("leptonsCharge");

    leptonsDeltaCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("leptonsDeltaCorrectedRelIso");
    leptonsRhoCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("leptonsRhoCorrectedRelIso");

    leptonsDB_ =  iConfig.getParameter< edm::InputTag >("leptonsDB");
    leptonsDZ_ =  iConfig.getParameter< edm::InputTag >("leptonsDZ");
    leptonsID_ =  iConfig.getParameter< edm::InputTag >("leptonsID");
    leptonsMVAID_ =  iConfig.getParameter< edm::InputTag >("leptonsMVAID");

    //qcd leptons

    qcdLeptonsPt_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsPt");
    qcdLeptonsPhi_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsPhi");
    qcdLeptonsEta_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsEta");
    qcdLeptonsEnergy_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsEnergy");
    qcdLeptonsCharge_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsCharge");

    qcdLeptonsDeltaCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsDeltaCorrectedRelIso");
    qcdLeptonsRhoCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsRhoCorrectedRelIso");

    qcdLeptonsDB_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsDB");
    qcdLeptonsID_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsID");

    leptonsFlavour_ =  iConfig.getUntrackedParameter< std::string >("leptonsFlavour");

    looseMuonsDeltaCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("looseMuonsDeltaCorrectedRelIso");
    looseMuonsRhoCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("looseMuonsRhoCorrectedRelIso");

    looseElectronsDeltaCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("looseElectronsDeltaCorrectedRelIso");
    looseElectronsRhoCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("looseElectronsRhoCorrectedRelIso");

    //Jets

    jetsEta_ =  iConfig.getParameter< edm::InputTag >("jetsEta");
    jetsPt_ =  iConfig.getParameter< edm::InputTag >("jetsPt");
    jetsPhi_ =  iConfig.getParameter< edm::InputTag >("jetsPhi");
    jetsEnergy_ =  iConfig.getParameter< edm::InputTag >("jetsEnergy");

    jetsBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsBTagAlgo");
    jetsAntiBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsAntiBTagAlgo");

    jetsPileUpID_ =  iConfig.getParameter< edm::InputTag >("jetsPileUpDiscr");
    jetsPileUpWP_ =  iConfig.getParameter< edm::InputTag >("jetsPileUpWP");

    jetsBeta_ =  iConfig.getParameter< edm::InputTag >("jetsBeta");
    jetsDZ_ =  iConfig.getParameter< edm::InputTag >("jetsDZ");
    jetsRMS_ =  iConfig.getParameter< edm::InputTag >("jetsRMS");

    jetsFlavour_ =  iConfig.getParameter< edm::InputTag >("jetsFlavour");

    //  genJetsPt_  = iConfig.getParameter< edm::InputTag >("genJetsPt");
    //genJetsEta_  = iConfig.getParameter< edm::InputTag >("genJetsEta");//FIXMEEE

    genJetsPt_  = iConfig.getParameter< edm::InputTag >("genJetsPt");
    genJetsEta_  = iConfig.getParameter< edm::InputTag >("genJetsEta");//FIXMEEE


    METPhi_ =  iConfig.getParameter< edm::InputTag >("METPhi");
    METPt_ =  iConfig.getParameter< edm::InputTag >("METPt");

    //  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
    //  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
    UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
    UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");


    jetsCorrTotal_ =  iConfig.getParameter< edm::InputTag >("jetsCorrTotal");

    doBScan_  =  iConfig.getUntrackedParameter< bool >("doBScan", false);
    doQCD_  =  iConfig.getUntrackedParameter< bool >("doQCD", true);

    doPDF_  =  iConfig.getUntrackedParameter< bool >("doPDF", true);

    //Q2 part
    x1_ = iConfig.getParameter<edm::InputTag>("x1") ;
    x2_ = iConfig.getParameter<edm::InputTag>("x2") ;

    id1_ = iConfig.getParameter<edm::InputTag>("id1") ;
    id2_ = iConfig.getParameter<edm::InputTag>("id2") ;

    scalePDF_ = iConfig.getParameter<edm::InputTag>("scalePDF") ;

    //Pile Up Part
    np1_ = iConfig.getParameter< edm::InputTag >("nVerticesPlus");//,"PileUpSync");
    nm1_ = iConfig.getParameter< edm::InputTag >("nVerticesMinus");//,"PileUpSync");
    n0_ = iConfig.getParameter< edm::InputTag >("nVertices");//,"PileUpSync");
    
    vertexZ_ = iConfig.getParameter< edm::InputTag >("vertexZ");//,"PileUpSync");

    doPU_ = iConfig.getUntrackedParameter< bool >("doPU", false);
    doResol_ = iConfig.getUntrackedParameter< bool >("doResol", false);
    doTurnOn_ = iConfig.getUntrackedParameter< bool >("doTurnOn", true);

    doReCorrection_ = iConfig.getUntrackedParameter< bool >("doReCorrection", false);
    dataPUFile_ =  channelInfo.getUntrackedParameter< std::string >("Season", "SummerMean11");
    
    PUFileNew_ =  channelInfo.getUntrackedParameter< std::string >("PUFileNew", "pileUpDistrNewWJets");
    
    takeBTagSFFromDB_ = iConfig.getUntrackedParameter< bool >("takeBTagSFFromDB", true);

    doJetTrees_ = iConfig.getUntrackedParameter< bool >("doJetTrees", true);

    algo_ = iConfig.getUntrackedParameter< std::string >("algo", "CSVT");
    doLooseBJetVeto_ = iConfig.getUntrackedParameter< bool >("doLooseBJetVeto", false);

    string season = "Summer11";
    season = dataPUFile_;
    //  TString season = "Fall11";
    string distr = "pileUpDistr" + season + ".root";
    if (doPU_)
    {
        //    //cout << " before lumIweightse "<<endl;
        LumiWeights_ = edm::LumiReWeighting(distr,
                                            "pileUpData.root",
                                            std::string("pileup"),
                                            std::string("pileup"));
        LumiWeightsUp_ = edm::LumiReWeighting(distr,
                                              "pileUpDataUp.root",
                                              std::string("pileup"),
                                              std::string("pileup"));
        LumiWeightsDown_ = edm::LumiReWeighting(distr,
                                                "pileUpDataDown.root",
                                                std::string("pileup"),
                                                std::string("pileup"));
        //    LumiWeightsUp_.weight3D_init(1.080);
        //LumiWeightsDown_.weight3D_init(0.961);
        //    LumiWeights_.weight3D_init(1.044);
        //LumiWeights_.weight3D_init(1.000);

        //    //cout << " built lumiWeights "<<endl;
        
        NewPUWeights_ = edm::ReWeighting(PUFileNew_+".root",
            PUFileNew_+"Data.root",
            std::string("c1"),
            std::string("c1"));
    }
    
    


    Service<TFileService> fs;


    bTagThreshold = 3.41;
    facBTagErr = 1.5;

    systematics.insert(systematics.begin(), "noSyst");

    //  for(size_t i = 0; i < systematics.size();++i){
    //  if(systematics.at(i)=="")
    //}

    std::vector<std::string> all_syst = systematics;


    TFileDirectory SingleTopSystematics = fs->mkdir( "systematics_histograms" );
    TFileDirectory SingleTopTrees = fs->mkdir( "systematics_trees" );


    for (size_t i = 0; i < rate_systematics.size(); ++i)
    {
      all_syst.push_back(rate_systematics.at(i));
    }


    for (size_t i = 0; i < all_syst.size(); ++i)
    {


        string syst = all_syst[i];

        if (doJetTrees_)
        {
            string treenameJets = (channel + "_NJets_" + syst);
            treesNJets[syst] = new TTree(treenameJets.c_str(), treenameJets.c_str());


            //Create INT branches first
            treesNJets[syst]->Branch("charge", &chargeTree);
            treesNJets[syst]->Branch("runid", &runTree);
            treesNJets[syst]->Branch("lumiid", &lumiTree);
            treesNJets[syst]->Branch("eventid", &eventTree);
            treesNJets[syst]->Branch("weight", &weightTree);
            treesNJets[syst]->Branch("eventFlavour", &eventFlavourTree);
            treesNJets[syst]->Branch("nJ", &nJ);
            treesNJets[syst]->Branch("nJNoPU", &nJNoPU);
            treesNJets[syst]->Branch("nJCentral", &nJCentral);
            treesNJets[syst]->Branch("nJCentralNoPU", &nJCentralNoPU);
            treesNJets[syst]->Branch("nJForward", &nJForward);
            treesNJets[syst]->Branch("nJForwardNoPU", &nJForwardNoPU);
            treesNJets[syst]->Branch("nVertices", &nVertices);
            treesNJets[syst]->Branch("nGoodVertices", &npv);
            treesNJets[syst]->Branch("nTCHPT", &ntchpt_tags);
            treesNJets[syst]->Branch("nCSVT", &ncsvt_tags);
            treesNJets[syst]->Branch("nCSVL", &ncsvm_tags);
            treesNJets[syst]->Branch("secondJetFlavour", &secondJetFlavourTree);
            treesNJets[syst]->Branch("firstJetFlavour", &firstJetFlavourTree);
            treesNJets[syst]->Branch("thirdJetFlavour", &thirdJetFlavourTree);

            //Now create DOUBLE branches
            treesNJets[syst]->Branch("w1TCHPT", &w1TCHPT);
            treesNJets[syst]->Branch("w2TCHPT", &w2TCHPT);
            treesNJets[syst]->Branch("w1CSVT", &w1CSVT);
            treesNJets[syst]->Branch("w2CSVT", &w2CSVT);
            treesNJets[syst]->Branch("w1CSVL", &w1CSVM);
            treesNJets[syst]->Branch("w2CSVL", &w2CSVM);
            treesNJets[syst]->Branch("bWeight",&bWeightTree);
            treesNJets[syst]->Branch("PUWeight", &PUWeightTree);
            treesNJets[syst]->Branch("PUWeightNew", &PUWeightTreeNew);
            treesNJets[syst]->Branch("turnOnWeight", &turnOnWeightTree);
            treesNJets[syst]->Branch("turnOnReWeight", &turnOnReWeightTree);
            treesNJets[syst]->Branch("leptonPt", &lepPt);
            treesNJets[syst]->Branch("leptonEta", &lepEta);
            treesNJets[syst]->Branch("leptonPhi", &lepPhi);
            treesNJets[syst]->Branch("leptonDeltaCorrectedRelIso", &lepDeltaCorrectedRelIso);
            treesNJets[syst]->Branch("leptonRhoCorrectedRelIso", &lepRhoCorrectedRelIso);
            treesNJets[syst]->Branch("leptonEff", &lepEff);
            treesNJets[syst]->Branch("leptonEffB", &lepEffB);
            treesNJets[syst]->Branch("mtwMass", &mtwMassTree);
            treesNJets[syst]->Branch("metPt", &metPt);
            treesNJets[syst]->Branch("HT", &HT);
            treesNJets[syst]->Branch("firstJetPt", &firstJetPt);
            treesNJets[syst]->Branch("firstJetEta", &firstJetEta);
            treesNJets[syst]->Branch("firstJetPhi", &firstJetPhi);
            treesNJets[syst]->Branch("firstJetE", &firstJetE);
            treesNJets[syst]->Branch("thirdJetPt", &thirdJetPt);
            treesNJets[syst]->Branch("thirdJetEta", &thirdJetEta);
            treesNJets[syst]->Branch("thirdJetPhi", &thirdJetPhi);
            treesNJets[syst]->Branch("thirdJetE", &thirdJetE);
            treesNJets[syst]->Branch("secondJetPt", &secondJetPt);
            treesNJets[syst]->Branch("secondJetEta", &secondJetEta);
            treesNJets[syst]->Branch("secondJetPhi", &secondJetPhi);
            treesNJets[syst]->Branch("secondJetE", &secondJetE);
            treesNJets[syst]->Branch("bJetPt", &bJetPt);
            treesNJets[syst]->Branch("fJetPt", &fJetPt);
            treesNJets[syst]->Branch("fJetEta", &fJetEta);
            treesNJets[syst]->Branch("bJetEta", &bJetEta);
            treesNJets[syst]->Branch("fJetPUID", &fJetPUID);
            treesNJets[syst]->Branch("fJetPUWP", &fJetPUWP);
            //58 lines
            treesNJets[syst]->Branch("fJetBeta", &fJetBeta);
            treesNJets[syst]->Branch("fJetDZ", &fJetDZ);
            treesNJets[syst]->Branch("fJetRMS", &fJetRMS);

            treesNJets[syst]->Branch("bJetBeta", &bJetBeta);
            treesNJets[syst]->Branch("bJetDZ", &bJetDZ);
            treesNJets[syst]->Branch("bJetRMS", &bJetRMS);
            
        }

        for (int bj = 0; bj <= 5; ++bj)
        {

            stringstream tags;
            int ntagss = bj;
            if (ntagss > 2 )
	      {

                ntagss = ntagss - 3;
                tags << ntagss;
                tags <<  "T_QCD";
	      }
            else
	      {
                tags << ntagss << "T";
	      }
           //2J1T

            string treename = (channel + "_2J_" + tags.str() + "_" + syst);

            //if(bj==0 )treename = (channel+"_"+syst+"WSample");
            //      if(bj==3 )treename = (channel+"_"+syst+"WSampleQCD");

            //      if(bj==1 )treename = (channel+"_"+syst);
            //      if(bj==4 )treename = (channel+"_"+syst+"QCD");

            trees2J[bj][syst] = new TTree(treename.c_str(), treename.c_str());

            //quantities for the analysis

            trees2J[bj][syst]->Branch("eta", &etaTree);
            trees2J[bj][syst]->Branch("costhetalj", &cosTree);
            trees2J[bj][syst]->Branch("costhetalbl", &cosBLTree);
            trees2J[bj][syst]->Branch("mtwMass", &mtwMassTree);

            trees2J[bj][syst]->Branch("charge", &chargeTree);
            trees2J[bj][syst]->Branch("runid", &runTree);
            trees2J[bj][syst]->Branch("lumiid", &lumiTree);
            trees2J[bj][syst]->Branch("eventid", &eventTree);
            trees2J[bj][syst]->Branch("weight", &weightTree);
            //trees2J[bj][syst]->Branch("weightTmp",&weightTree);

            trees2J[bj][syst]->Branch("totalWeight", &totalWeightTree);

            trees2J[bj][syst]->Branch("bWeight", &bWeightTree);

            //Systematics b weights
            trees2J[bj][syst]->Branch("bWeightBTagUp", &bWeightTreeBTagUp);
            trees2J[bj][syst]->Branch("bWeightBTagDown", &bWeightTreeBTagDown);

            trees2J[bj][syst]->Branch("bWeightMisTagUp", &bWeightTreeMisTagUp);
            trees2J[bj][syst]->Branch("bWeightMisTagDown", &bWeightTreeMisTagDown);

            //Systematics pile up weights
            trees2J[bj][syst]->Branch("PUWeight", &PUWeightTree);

            trees2J[bj][syst]->Branch("PUWeightPUUp", &PUWeightTreePUUp);
            trees2J[bj][syst]->Branch("PUWeightPUDown", &PUWeightTreePUDown);

            trees2J[bj][syst]->Branch("PUWeightNew", &PUWeightTreeNew);

            //Systematics turn on weights
            trees2J[bj][syst]->Branch("turnOnWeight", &turnOnWeightTree);
            //trees2J[bj][syst]->Branch("turnOnWeightPt",&turnOnPtWeightTree);
            //trees2J[bj][syst]->Branch("turnOnWeightBTag",&turnOnBTagWeightTree);
            trees2J[bj][syst]->Branch("turnOnReWeight", &turnOnReWeightTree);

            trees2J[bj][syst]->Branch("turnOnWeightJetTrig1Up", &turnOnWeightTreeJetTrig1Up);
            trees2J[bj][syst]->Branch("turnOnWeightJetTrig1Down", &turnOnWeightTreeJetTrig1Down);

            trees2J[bj][syst]->Branch("turnOnWeightJetTrig2Up", &turnOnWeightTreeJetTrig2Up);
            trees2J[bj][syst]->Branch("turnOnWeightJetTrig2Down", &turnOnWeightTreeJetTrig2Down);

            trees2J[bj][syst]->Branch("turnOnWeightJetTrig3Up", &turnOnWeightTreeJetTrig3Up);
            trees2J[bj][syst]->Branch("turnOnWeightJetTrig3Down", &turnOnWeightTreeJetTrig3Down);

            trees2J[bj][syst]->Branch("turnOnWeightBTagTrig1Up", &turnOnWeightTreeBTagTrig1Up);
            trees2J[bj][syst]->Branch("turnOnWeightBTagTrig1Down", &turnOnWeightTreeBTagTrig1Down);

            trees2J[bj][syst]->Branch("turnOnWeightBTagTrig2Up", &turnOnWeightTreeBTagTrig2Up);
            trees2J[bj][syst]->Branch("turnOnWeightBTagTrig2Down", &turnOnWeightTreeBTagTrig2Down);

            trees2J[bj][syst]->Branch("turnOnWeightBTagTrig3Up", &turnOnWeightTreeBTagTrig3Up);
            trees2J[bj][syst]->Branch("turnOnWeightBTagTrig3Down", &turnOnWeightTreeBTagTrig3Down);


            //other observables
            trees2J[bj][syst]->Branch("leptonPt", &lepPt);
            trees2J[bj][syst]->Branch("leptonEta", &lepEta);
            trees2J[bj][syst]->Branch("leptonPhi", &lepPhi);
            trees2J[bj][syst]->Branch("leptonDeltaCorrectedRelIso", &lepDeltaCorrectedRelIso);
            trees2J[bj][syst]->Branch("leptonRhoCorrectedRelIso", &lepRhoCorrectedRelIso);

            trees2J[bj][syst]->Branch("leptonEff", &lepEff);
            trees2J[bj][syst]->Branch("leptonEffB", &lepEffB);

            trees2J[bj][syst]->Branch("fJetPt", &fJetPt);
            trees2J[bj][syst]->Branch("fJetE", &fJetE);
            trees2J[bj][syst]->Branch("fJetEta", &fJetEta);
            trees2J[bj][syst]->Branch("fJetPhi", &fJetPhi);
            trees2J[bj][syst]->Branch("fJetBtag", &fJetBTag);
            trees2J[bj][syst]->Branch("fJetFlavour", &fJetFlavourTree);
            trees2J[bj][syst]->Branch("fJetPUID", &fJetPUID);
            trees2J[bj][syst]->Branch("fJetPUWP", &fJetPUWP);

            trees2J[bj][syst]->Branch("fJetBeta", &fJetBeta);
            trees2J[bj][syst]->Branch("fJetDZ", &fJetDZ);
            trees2J[bj][syst]->Branch("fJetRMS", &fJetRMS);

            trees2J[bj][syst]->Branch("bJetBeta", &bJetBeta);
            trees2J[bj][syst]->Branch("bJetDZ", &bJetDZ);
            trees2J[bj][syst]->Branch("bJetRMS", &bJetRMS);

            trees2J[bj][syst]->Branch("bJetPt", &bJetPt);
            trees2J[bj][syst]->Branch("bJetE", &bJetE);
            trees2J[bj][syst]->Branch("bJetEta", &bJetEta);
            trees2J[bj][syst]->Branch("bJetPhi", &bJetPhi);
            trees2J[bj][syst]->Branch("bJetBtag", &bJetBTag);
            trees2J[bj][syst]->Branch("bJetFlavour", &bJetFlavourTree);
            trees2J[bj][syst]->Branch("bJetPUID", &bJetPUID);
            trees2J[bj][syst]->Branch("bJetPUWP", &bJetPUWP);

            trees2J[bj][syst]->Branch("firstJetPt", &firstJetPt);
            trees2J[bj][syst]->Branch("firstJetEta", &firstJetEta);
            trees2J[bj][syst]->Branch("firstJetPhi", &firstJetPhi);
            trees2J[bj][syst]->Branch("firstJetE", &firstJetE);
            trees2J[bj][syst]->Branch("firstJetFlavour", &firstJetFlavourTree);

            trees2J[bj][syst]->Branch("secondJetPt", &secondJetPt);
            trees2J[bj][syst]->Branch("secondJetEta", &secondJetEta);
            trees2J[bj][syst]->Branch("secondJetPhi", &secondJetPhi);
            trees2J[bj][syst]->Branch("secondJetE", &secondJetE);
            trees2J[bj][syst]->Branch("secondJetFlavour", &secondJetFlavourTree);



            trees2J[bj][syst]->Branch("eventFlavour", &eventFlavourTree);

            trees2J[bj][syst]->Branch("metPt", &metPt);
            trees2J[bj][syst]->Branch("metPhi", &metPhi);

            trees2J[bj][syst]->Branch("HT", &HT);

            trees2J[bj][syst]->Branch("topMass", &topMassTree);
            trees2J[bj][syst]->Branch("topMtw", &topMtwTree);

            trees2J[bj][syst]->Branch("topPt", &topPt);
            trees2J[bj][syst]->Branch("topPhi", &topPhi);
            trees2J[bj][syst]->Branch("topEta", &topEta);
            trees2J[bj][syst]->Branch("topE", &topE);

            trees2J[bj][syst]->Branch("ID", &electronID);
            trees2J[bj][syst]->Branch("nVertices", &nVertices);
            trees2J[bj][syst]->Branch("nGoodVertices", &npv);

            //      trees2J[bj][syst]->Branch("nVerticesReco",&nVerticesReco);

            trees2J[bj][syst]->Branch("totalEnergy", &totalEnergy);
            trees2J[bj][syst]->Branch("totalMomentum", &totalMomentum);

            trees2J[bj][syst]->Branch("lowBTag", &lowBTagTree);
            trees2J[bj][syst]->Branch("highBTag", &highBTagTree);

            for (int p = 1; p <= 52; ++p)
            {
                stringstream w_n;
                w_n << p;
                trees2J[bj][syst]->Branch(("PDFWeight" + w_n.str()).c_str(), &pdf_weights[p - 1]);
            }
            trees2J[bj][syst]->Branch("PDFWeight_Alternate_Set_1", &pdf_weights_alternate_set_1);
            trees2J[bj][syst]->Branch("PDFWeight_Alternate_Set_2", &pdf_weights_alternate_set_2);

            treename = (channel + "_3J_" + tags.str() + "_" + syst);
            //      if(bj==2 )treename = (channel+"_"+syst+"3J2T");
            //if(bj==5 )treename = (channel+"_"+syst+"ESBQCD");
            trees3J[bj][syst] = new TTree(treename.c_str(), treename.c_str());

            //basic quantities

            trees3J[bj][syst]->Branch("eta", &etaTree);
            trees3J[bj][syst]->Branch("costhetalj", &cosTree);
            trees3J[bj][syst]->Branch("costhetalbl", &cosBLTree);
            trees3J[bj][syst]->Branch("topMass", &topMassTree);

            trees3J[bj][syst]->Branch("topMtw", &topMtwTree);

            trees3J[bj][syst]->Branch("HT", &HT);

            trees3J[bj][syst]->Branch("mtwMass", &mtwMassTree);

            trees3J[bj][syst]->Branch("charge", &chargeTree);
            trees3J[bj][syst]->Branch("runid", &runTree);
            trees3J[bj][syst]->Branch("lumiid", &lumiTree);
            trees3J[bj][syst]->Branch("eventid", &eventTree);
            trees3J[bj][syst]->Branch("weight", &weightTree);
            //trees2J[bj][syst]->Branch("weightTmp",&weightTree);

            trees3J[bj][syst]->Branch("totalWeight", &totalWeightTree);

            //Extra info

            trees3J[bj][syst]->Branch("leptonPt", &lepPt);
            trees3J[bj][syst]->Branch("leptonEta", &lepEta);
            trees3J[bj][syst]->Branch("leptonPhi", &lepPhi);

            trees3J[bj][syst]->Branch("leptonDeltaCorrectedRelIso", &lepDeltaCorrectedRelIso);
            trees3J[bj][syst]->Branch("leptonRhoCorrectedRelIso", &lepRhoCorrectedRelIso);

            trees3J[bj][syst]->Branch("leptonEff", &lepEff);
            trees3J[bj][syst]->Branch("leptonEffB", &lepEffB);

            trees3J[bj][syst]->Branch("fJetPt", &fJetPt);
            trees3J[bj][syst]->Branch("fJetE", &fJetE);
            trees3J[bj][syst]->Branch("fJetEta", &fJetEta);
            trees3J[bj][syst]->Branch("fJetPhi", &fJetPhi);
            trees3J[bj][syst]->Branch("fJetBtag", &fJetBTag);
            trees3J[bj][syst]->Branch("fJetFlavour", &fJetFlavourTree);
            trees3J[bj][syst]->Branch("fJetPUID", &fJetPUID);
            trees3J[bj][syst]->Branch("fJetPUWP", &fJetPUWP);

            trees3J[bj][syst]->Branch("fJetBeta", &fJetBeta);
            trees3J[bj][syst]->Branch("fJetDZ", &fJetDZ);
            trees3J[bj][syst]->Branch("fJetRMS", &fJetRMS);

            trees3J[bj][syst]->Branch("bJetBeta", &bJetBeta);
            trees3J[bj][syst]->Branch("bJetDZ", &bJetDZ);
            trees3J[bj][syst]->Branch("bJetRMS", &bJetRMS);

            trees3J[bj][syst]->Branch("bJetPt", &bJetPt);
            trees3J[bj][syst]->Branch("bJetE", &bJetE);
            trees3J[bj][syst]->Branch("bJetEta", &bJetEta);
            trees3J[bj][syst]->Branch("bJetPhi", &bJetPhi);
            trees3J[bj][syst]->Branch("bJetBtag", &bJetBTag);
            trees3J[bj][syst]->Branch("bJetFlavour", &bJetFlavourTree);
            trees3J[bj][syst]->Branch("bJetPUID", &bJetPUID);
            trees3J[bj][syst]->Branch("bJetPUWP", &bJetPUWP);


            trees3J[bj][syst]->Branch("firstJetPt", &firstJetPt);
            trees3J[bj][syst]->Branch("firstJetEta", &firstJetEta);
            trees3J[bj][syst]->Branch("firstJetPhi", &firstJetPhi);
            trees3J[bj][syst]->Branch("firstJetE", &firstJetE);
            trees3J[bj][syst]->Branch("firstJetFlavour", &firstJetFlavourTree);

            trees3J[bj][syst]->Branch("secondJetPt", &secondJetPt);
            trees3J[bj][syst]->Branch("secondJetEta", &secondJetEta);
            trees3J[bj][syst]->Branch("secondJetPhi", &secondJetPhi);
            trees3J[bj][syst]->Branch("secondJetE", &secondJetE);
            trees3J[bj][syst]->Branch("secondJetFlavour", &secondJetFlavourTree);

            trees3J[bj][syst]->Branch("thirdJetPt", &thirdJetPt);
            trees3J[bj][syst]->Branch("thirdJetEta", &thirdJetEta);
            trees3J[bj][syst]->Branch("thirdJetPhi", &thirdJetPhi);
            trees3J[bj][syst]->Branch("thirdJetE", &thirdJetE);
            trees3J[bj][syst]->Branch("thirdJetFlavour", &thirdJetFlavourTree);




            trees3J[bj][syst]->Branch("eventFlavour", &eventFlavourTree);


            trees3J[bj][syst]->Branch("metPt", &metPt);
            trees3J[bj][syst]->Branch("metPhi", &metPhi);

            trees3J[bj][syst]->Branch("topPt", &topPt);
            trees3J[bj][syst]->Branch("topPhi", &topPhi);
            trees3J[bj][syst]->Branch("topEta", &topEta);
            trees3J[bj][syst]->Branch("topE", &topE);

            trees3J[bj][syst]->Branch("ID", &electronID);
            trees3J[bj][syst]->Branch("nVertices", &nVertices);
            trees3J[bj][syst]->Branch("nGoodVertices", &npv);


            trees3J[bj][syst]->Branch("totalEnergy", &totalEnergy);
            trees3J[bj][syst]->Branch("totalMomentum", &totalMomentum);

            trees3J[bj][syst]->Branch("lowBTag", &lowBTagTree);
            trees3J[bj][syst]->Branch("highBTag", &highBTagTree);


            //Systematics b weights

            trees3J[bj][syst]->Branch("bWeight", &bWeightTree);

            trees3J[bj][syst]->Branch("bWeightBTagUp", &bWeightTreeBTagUp);
            trees3J[bj][syst]->Branch("bWeightBTagDown", &bWeightTreeBTagDown);

            trees3J[bj][syst]->Branch("bWeightMisTagUp", &bWeightTreeMisTagUp);
            trees3J[bj][syst]->Branch("bWeightMisTagDown", &bWeightTreeMisTagDown);

            //Systematics pile up weights
            trees3J[bj][syst]->Branch("PUWeight", &PUWeightTree);

            trees3J[bj][syst]->Branch("PUWeightPUUp", &PUWeightTreePUUp);
            trees3J[bj][syst]->Branch("PUWeightPUDown", &PUWeightTreePUDown);
            
            trees3J[bj][syst]->Branch("PUWeightNew", &PUWeightTreeNew);

            //Systematics turn on weights
            trees3J[bj][syst]->Branch("turnOnWeight", &turnOnWeightTree);
            trees3J[bj][syst]->Branch("turnOnReWeight", &turnOnReWeightTree);

            trees3J[bj][syst]->Branch("turnOnWeightJetTrig1Up", &turnOnWeightTreeJetTrig1Up);
            trees3J[bj][syst]->Branch("turnOnWeightJetTrig1Down", &turnOnWeightTreeJetTrig1Down);

            trees3J[bj][syst]->Branch("turnOnWeightJetTrig2Up", &turnOnWeightTreeJetTrig2Up);
            trees3J[bj][syst]->Branch("turnOnWeightJetTrig2Down", &turnOnWeightTreeJetTrig2Down);

            trees3J[bj][syst]->Branch("turnOnWeightJetTrig3Up", &turnOnWeightTreeJetTrig3Up);
            trees3J[bj][syst]->Branch("turnOnWeightJetTrig3Down", &turnOnWeightTreeJetTrig3Down);


            trees3J[bj][syst]->Branch("turnOnWeightBTagTrig1Up", &turnOnWeightTreeBTagTrig1Up);
            trees3J[bj][syst]->Branch("turnOnWeightBTagTrig1Down", &turnOnWeightTreeBTagTrig1Down);

            trees3J[bj][syst]->Branch("turnOnWeightBTagTrig2Up", &turnOnWeightTreeBTagTrig2Up);
            trees3J[bj][syst]->Branch("turnOnWeightBTagTrig2Down", &turnOnWeightTreeBTagTrig2Down);

            trees3J[bj][syst]->Branch("turnOnWeightBTagTrig3Up", &turnOnWeightTreeBTagTrig3Up);
            trees3J[bj][syst]->Branch("turnOnWeightBTagTrig3Down", &turnOnWeightTreeBTagTrig3Down);

            for (int p = 1; p <= 52; ++p)
            {
                stringstream w_n;
                w_n << p;
                trees3J[bj][syst]->Branch(("PDFWeight" + w_n.str()).c_str(), &pdf_weights[p - 1]);
            }

            trees2J[bj][syst]->Branch("PDFWeight_Alternate_Set_1", &pdf_weights_alternate_set_1);
            trees2J[bj][syst]->Branch("PDFWeight_Alternate_Set_2", &pdf_weights_alternate_set_2);

        }

    }

    passingLepton = 0;
    passingMuonVeto = 0;
    passingLeptonVeto = 0;
    passingJets = 0;
    passingBJets = 0;
    passingMET = 0;

    //TCHPT
    b_tchpt_0_tags = BTagWeight(0, 0);
    b_tchpt_1_tag = BTagWeight(1, 1);
    b_tchpt_2_tags = BTagWeight(2, 2);
    //CSVT
    b_csvt_0_tags = BTagWeight(0, 0);
    b_csvt_1_tag = BTagWeight(1, 1);
    b_csvt_2_tags = BTagWeight(2, 2);
    //CSVM
    b_csvm_0_tags = BTagWeight(0, 0);
    b_csvm_1_tag = BTagWeight(1, 1);
    b_csvm_2_tags = BTagWeight(2, 2);




    //  JEC_PATH = "CondFormats/JetMETObjects/data/";
    //  JEC_PATH = "./JECs/";
    //  fip = edm::FileInPath(JEC_PATH+"Spring10_Uncertainty_AK5PF.txt");
    //fip = edm::FileInPath(JEC_PATH+"GR_R_42_V19_AK5PF_Uncertainty.txt");
    //jecUnc = new JetCorrectionUncertainty(fip.fullPath());

    JEC_PATH = "./";

    //jecUnc  = new JetCorrectionUncertainty(JEC_PATH+"GR_R_42_V19_AK5PF_Uncertainty.txt");
    //  jecUnc  = new JetCorrectionUncertainty(JEC_PATH+"JEC11_V12_AK5PF_UncertaintySources.txt");
    //    jecUnc  = new JetCorrectionUncertainty(*(new JetCorrectorParameters("JEC11_V12_AK5PF_UncertaintySources.txt", "Total")));
    jecUnc  = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Summer12_V2_DATA_AK5PF_UncertaintySources.txt", "Total")));
    JES_SW = 0.015;
    JES_b_cut = 0.02;
    JES_b_overCut = 0.03;


    //JetResolution part
    string fileResolName = "Spring10_PtResolution_AK5PF.txt";
    bool  doGaussianResol = false;
    //  ptResol = new JetResolution(fileResolName, doGaussianResol);

    leptonRelIsoQCDCutUpper = 0.9, leptonRelIsoQCDCutLower = 0.2;


    topMassMeas = 172.9;
    //  doReCorrection_= false;
    if (doReCorrection_) //FIXME CURRENTLY NOT WORKING!!!
    {
        /*cout << "jec 1" << endl;
        JetCorrectorParameters *ResJetParData = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L2L3Residual.txt");
        cout << "jec 1A" << endl;
        JetCorrectorParameters *L3JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L3Absolute.txt");
        JetCorrectorParameters *L2JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L2Relative.txt");
        JetCorrectorParameters *L1JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L1FastJet.txt");
        cout << "jec 1B" << endl;
        vParData->push_back(*L1JetParData);
        cout << "jec 1C" << endl;
        vParData->push_back(*L2JetParData);
        vParData->push_back(*L3JetParData);
        vParData->push_back(*ResJetParData);
         */

        //cout << "jec 2" << endl;
        // JetCorrectorParameters *L3JetParMC = new JetCorrectorParameters(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L3Absolute.txt");
        //JetCorrectorParameters *L2JetParMC = new JetCorrectorParameters(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L2Relative.txt");

        //  JetCorrectorParameters L1JetParMC(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L1FastJet.txt");
        //cout << "jec 3" << endl;
        //  vector<JetCorrectorParameters > vParTmp;

        //  vParMC.push_back(L1JetParMC);
        //vParTmp.push_back(L1JetParMC);
        //   vParMC->push_back(*L2JetParMC)

        //   vParMC->push_back(*L3JetParMC);

        //cout << "jec 4" << endl;

        //   JetCorrectorData = new FactorizedJetCorrector(*vParData);
        //   JetCorrectorMC  = new FactorizedJetCorrector( vParTmp);
    }
    InitializeEventScaleFactorMap();
    InitializeTurnOnReWeight("CentralJet30BTagIP_2ndSF_mu.root");
    //   LHAPDF::initPDFSet(1, "cteq66.LHgrid");
    LHAPDF::initPDFSet(1, "CT10.LHgrid");
    LHAPDF::initPDFSet(2, "MSTW2008nlo68cl.LHgrid");
    LHAPDF::initPDFSet(3, "MSTW2008nlo68cl.LHgrid");
    //   LHAPDF::initPDFSet(3, "NNPDF21_100.LHgrid");



    //  //cout<< "I work for now but I do nothing. But again, if you gotta do nothing, you better do it right. To prove my good will I will provide you with somse numbers later."<<endl;
    isFirstEvent = true;
}

void SingleTopSystematicsTreesDumper::initBranchVars()
{
#define INT_NAN 9999
#define FLOAT_NAN 9999.0
#define DOUBLE_NAN 9999.0

    //ints
    chargeTree = INT_NAN;
    runTree = INT_NAN;
    lumiTree = INT_NAN;
    eventTree = INT_NAN;
    eventFlavourTree = INT_NAN;
    firstJetFlavourTree = INT_NAN;
    secondJetFlavourTree = INT_NAN;
    thirdJetFlavourTree = INT_NAN;
    nJ = INT_NAN;
    nJNoPU = INT_NAN;
    nJCentral = INT_NAN;
    nJCentralNoPU = INT_NAN;
    nJForward = INT_NAN;
    nJForwardNoPU = INT_NAN;
    nVertices = INT_NAN;
    npv = INT_NAN;
    ntchpt_tags = INT_NAN;
    ncsvt_tags = INT_NAN;
    ncsvm_tags = INT_NAN;

    //doubles
    weightTree = DOUBLE_NAN;
    w1TCHPT = DOUBLE_NAN;
    w2TCHPT = DOUBLE_NAN;
    w1CSVT = DOUBLE_NAN;
    w2CSVT = DOUBLE_NAN;
    w1CSVM = DOUBLE_NAN;
    w2CSVM = DOUBLE_NAN;
    PUWeightTree = DOUBLE_NAN;
    PUWeightTreeNew = DOUBLE_NAN;
    turnOnWeightTree = DOUBLE_NAN;
    turnOnReWeightTree = DOUBLE_NAN;
    lepPt = DOUBLE_NAN;
    lepEta = DOUBLE_NAN;
    lepPhi = DOUBLE_NAN;
    lepDeltaCorrectedRelIso = DOUBLE_NAN;
    lepRhoCorrectedRelIso = DOUBLE_NAN;
    lepEff = DOUBLE_NAN;
    mtwMassTree = DOUBLE_NAN;
    metPt = DOUBLE_NAN;
    firstJetPt = DOUBLE_NAN;
    firstJetEta = DOUBLE_NAN;
    firstJetPhi = DOUBLE_NAN;
    firstJetE = DOUBLE_NAN;
    secondJetPt = DOUBLE_NAN;
    secondJetEta = DOUBLE_NAN;
    secondJetPhi = DOUBLE_NAN;
    secondJetE = DOUBLE_NAN;
    thirdJetPt = DOUBLE_NAN;
    thirdJetEta = DOUBLE_NAN;
    thirdJetPhi = DOUBLE_NAN;
    thirdJetE = DOUBLE_NAN;
    bJetPt = DOUBLE_NAN;
    fJetPt = DOUBLE_NAN;
    bJetEta = DOUBLE_NAN;
    fJetEta = DOUBLE_NAN;
    fJetPUID = DOUBLE_NAN;
    fJetPUWP = DOUBLE_NAN;
    //58 lines

    etaTree = DOUBLE_NAN;
    cosTree = DOUBLE_NAN;
    cosBLTree = DOUBLE_NAN;
    mtwMassTree = DOUBLE_NAN;

    chargeTree = INT_NAN;
    runTree = INT_NAN;
    lumiTree = INT_NAN;
    eventTree = INT_NAN;

    weightTree = DOUBLE_NAN;

    fJetFlavourTree = INT_NAN;
    bJetFlavourTree = INT_NAN;
    eventFlavourTree = INT_NAN;
    nVertices = INT_NAN;
    npv = INT_NAN;
    firstJetFlavourTree = INT_NAN;
    secondJetFlavourTree = INT_NAN;
    thirdJetFlavourTree = INT_NAN;

    bWeightTreeBTagUp = DOUBLE_NAN;
    bWeightTreeBTagDown = DOUBLE_NAN;
    bWeightTreeMisTagUp = DOUBLE_NAN;
    bWeightTreeMisTagDown = DOUBLE_NAN;
    PUWeightTree = DOUBLE_NAN;
    PUWeightTreePUUp = DOUBLE_NAN;
    PUWeightTreePUDown = DOUBLE_NAN;
    turnOnWeightTree = DOUBLE_NAN;
    turnOnReWeightTree = DOUBLE_NAN;
    turnOnWeightTreeJetTrig1Up = DOUBLE_NAN;
    turnOnWeightTreeJetTrig1Down = DOUBLE_NAN;
    turnOnWeightTreeJetTrig2Up = DOUBLE_NAN;
    turnOnWeightTreeJetTrig2Down = DOUBLE_NAN;
    turnOnWeightTreeJetTrig3Up = DOUBLE_NAN;
    turnOnWeightTreeJetTrig3Down = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig1Up = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig1Down = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig2Up = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig2Down = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig3Up = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig3Down = DOUBLE_NAN;
    lepPt = DOUBLE_NAN;
    lepEta = DOUBLE_NAN;
    lepPhi = DOUBLE_NAN;
    lepDeltaCorrectedRelIso = DOUBLE_NAN;
    lepRhoCorrectedRelIso = DOUBLE_NAN;
    lepEff = DOUBLE_NAN;
    lepEffB = DOUBLE_NAN;
    fJetPt = DOUBLE_NAN;
    fJetE = DOUBLE_NAN;
    fJetEta = DOUBLE_NAN;
    fJetPhi = DOUBLE_NAN;
    fJetBTag = DOUBLE_NAN;
    fJetPUID = DOUBLE_NAN;
    fJetPUWP = DOUBLE_NAN;
    bJetPt = DOUBLE_NAN;
    bJetE = DOUBLE_NAN;
    bJetEta = DOUBLE_NAN;
    bJetPhi = DOUBLE_NAN;
    bJetBTag = DOUBLE_NAN;
    bJetPUID = DOUBLE_NAN;
    bJetPUWP = DOUBLE_NAN;
    firstJetPt = DOUBLE_NAN;
    firstJetEta = DOUBLE_NAN;
    firstJetPhi = DOUBLE_NAN;
    firstJetE = DOUBLE_NAN;
    secondJetPt = DOUBLE_NAN;
    secondJetEta = DOUBLE_NAN;
    secondJetPhi = DOUBLE_NAN;
    secondJetE = DOUBLE_NAN;
    thirdJetPt = DOUBLE_NAN;
    thirdJetEta = DOUBLE_NAN;
    thirdJetPhi = DOUBLE_NAN;
    thirdJetE = DOUBLE_NAN;
    metPt = DOUBLE_NAN;
    metPhi = DOUBLE_NAN;
    topMassTree = DOUBLE_NAN;
    topMtwTree = DOUBLE_NAN;
    topPt = DOUBLE_NAN;
    topPhi = DOUBLE_NAN;
    topEta = DOUBLE_NAN;
    topE = DOUBLE_NAN;
    electronID = DOUBLE_NAN;
    totalEnergy = DOUBLE_NAN;
    totalMomentum = DOUBLE_NAN;
    lowBTagTree = DOUBLE_NAN;
    highBTagTree = DOUBLE_NAN;

    pdf_weights_alternate_set_1 = FLOAT_NAN;
    pdf_weights_alternate_set_2 = FLOAT_NAN;

    for (int i = 0; i < 52; i++)
    {
        pdf_weights[i] = FLOAT_NAN;
    }

}

void SingleTopSystematicsTreesDumper::analyze(const Event &iEvent, const EventSetup &iSetup)
{

  //  if()
  //

    initBranchVars();

    //cout <<" test 1 "<<endl;
    iEvent.getByLabel(jetsEta_, jetsEta);
    iEvent.getByLabel(jetsPt_, jetsPt);
    //  if(jetsPt->size() < 2)return;
    if (jetsPt->size() > 25 && channel != "Data")return; //Crazy events with huge jet multiplicity in mc
    iEvent.getByLabel(jetsPhi_, jetsPhi);

    if (isFirstEvent && takeBTagSFFromDB_)
    {
        //cout <<  "isfirst " << endl;
        iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT", perfMHP);
        iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPM", perfMHPM);
        iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL", perfMHE);

        iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPM", perfBHPM);
        iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPT", perfBHP);
        iSetup.get<BTagPerformanceRecord>().get("BTAGTCHEL", perfBHE);
        isFirstEvent = false;
    }
    //  iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
    // iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);

    //  //cout << "test 0 "<<endl;

    gotLeptons = 0;
    gotPV = 0;
    gotQCDLeptons = 0;
    gotLooseLeptons = 0;
    gotJets = 0;
    gotMets = 0;
    gotPU = 0;

    //cout <<" test 2 "<<endl;

    jsfshpt.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfshpt_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfshpt_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfshpt_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfshpt_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvt.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvt_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvt_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvt_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvt_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvm.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvm_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvm_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvm_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvm_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();


    //No second tagger: uncomment it to add one

    //  jsfshel.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();





    iEvent.getByLabel(METPhi_, METPhi);
    iEvent.getByLabel(METPt_, METPt);
    iEvent.getByLabel(leptonsDeltaCorrectedRelIso_, leptonsDeltaCorrectedRelIso);

    double PUWeight = 1;
    double PUWeightNoSyst = 1;
    double bWeightNoSyst = 1;
    double turnOnWeightValueNoSyst = 1;
    double turnOnReWeightTreeNoSyst = 1;

    double PUWeightNew = 1;
    double PUWeightNewNoSyst = 1;

    BinningPointByMap measurePoint;

    float metPx = 0;
    float metPy = 0;

    metPx = METPt->at(0) * cos(METPhi->at(0));
    metPy = METPt->at(0) * sin(METPhi->at(0));

    float metPxTmp = metPx;
    float metPyTmp = metPy;

    size_t nLeptons = 0;//leptonsPt->size();
    size_t nQCDLeptons = 0;//leptonsPt->size();
    size_t nJets = 0;
    size_t nJetsNoPU = 0;
    size_t nJetsCentralNoPU = 0;
    size_t nJetsCentral = 0;
    size_t nJetsForwardNoPU = 0;
    size_t nJetsForward = 0;
    size_t nJetsNoSyst = 0;
    size_t nBJets = 0;
    size_t nLooseBJets = 0;
    //  size_t nAntiBJets = 0;


    double WeightLumi = finalLumi * crossSection / originalEvents;
    double Weight = 1;
    double MTWValue = 0;
    double MTWValueQCD = 0;
    double RelIsoQCDCut = 0.1;

    float ptCut = 40;

    double myWeight = 1.;

    bool didLeptonLoop = false;
    bool passesLeptonStep = false;
    bool isQCD = false;


    bool didJetLoop = false;

    if (channel == "Data")WeightLumi = 1;

    int secondPtPosition = -1;
    int thirdPtPosition = -1;

    double secondPt = -1;
    double thirdPt = -1;

    int lowBTagTreePositionNoSyst = -1;
    int highBTagTreePositionNoSyst = -1;
    int maxPtTreePositionNoSyst = -1;
    int minPtTreePositionNoSyst = -1;

    for (size_t s = 0; s < systematics.size(); ++s)
    {
        string syst_name =  systematics.at(s);
        string syst = syst_name;

        nLeptons = 0;
        nQCDLeptons = 0;
        nJets = 0;
        nJetsNoPU = 0;
        nJetsCentral = 0;
        nJetsCentralNoPU = 0;
        nJetsForward = 0;
        nJetsForwardNoPU = 0;
        //    nBJets =0;
        //cout <<" syst " << syst << endl;
        //    nAntiBJets =0;

        //Here the weight of the event is the weight
        //to normalize the sample to the luminosity
        //required in the cfg
        Weight = WeightLumi;
        //    Weight *= PUWeight;

	HT = 0;

        bool is_btag_relevant = ((syst_name == "noSyst" || syst_name == "BTagUp" || syst_name == "BTagDown"
                                  || syst_name == "MisTagUp" || syst_name == "MisTagDown"
                                  || syst_name == "JESUp" || syst_name == "JESDown"
                                  || syst_name == "JERUp" || syst_name == "JERDown"
                                 ) && channel != "Data"
                                );


        //Setup for systematics

        //This is done according to old b-tagging prescriptions

        //Here we have vectors of weights
        //to be associated with the
        //b-jets selection in the sample according to algorythm X:
        //a b-tag requirement implies a b_weight_tag_algoX,
        //a b-veto requirement implies a b_weight_antitag_algoX

        //TCHPT
        b_weight_tchpt_1_tag = 1;
        b_weight_tchpt_0_tags = 1;
        b_weight_tchpt_2_tags = 1;
        //CSVT
        b_weight_csvm_1_tag = 1;
        b_weight_csvm_0_tags = 1;
        b_weight_csvm_2_tags = 1;
        //CSVT
        b_weight_csvt_1_tag = 1;
        b_weight_csvt_0_tags = 1;
        b_weight_csvt_2_tags = 1;

        nb = 0;
        nc = 0;
        nudsg = 0;


        //Clear the vector of objects to be used in the selection

        //Define - initialize some variables
        MTWValue = 0;


        //position of lowest and highest b-tag used to chose the top candidate
        int lowBTagTreePosition = -1;
        lowBTagTree = 99999;

        int highBTagTreePosition = -1;
        highBTagTree = -9999;


        int maxPtTreePosition = -1;
        maxPtTree = -99999;

        int minPtTreePosition = -1;
        minPtTree = 99999;

        secondPt = -1;
        thirdPt = -1;
        secondPtPosition = -1;
        thirdPtPosition = -1;

        //Taking the unclustered met previously evaluated
        //and already present in the n-tuples
        //This is used for syst up and down

        if (syst_name == "UnclusteredMETUp")
        {
            iEvent.getByLabel(UnclMETPx_, UnclMETPx);
            iEvent.getByLabel(UnclMETPy_, UnclMETPy);
            metPx += (*UnclMETPx) * 0.1;
            metPy += (*UnclMETPy) * 0.1;
        }
        if (syst_name == "UnclusteredMETDown")
        {
            iEvent.getByLabel(UnclMETPx_, UnclMETPx);
            iEvent.getByLabel(UnclMETPy_, UnclMETPy);
            metPx -= (*UnclMETPx) * 0.1;
            metPy -= (*UnclMETPy) * 0.1;
        }


        //Define - initialize some variables
        float eta;
        float ptCorr;
        int flavour;
        double unc = 0;

        //Loops to apply systematics on jets-leptons


        //cout << " before leptons "<<endl;

        //Lepton loop
        if (!didLeptonLoop)
        {
            for (size_t i = 0; i < leptonsDeltaCorrectedRelIso->size(); ++i)
            {

                if (leptonsFlavour_ == "muon")
                {
                    float leptonRelIsoDeltaCorr = leptonsDeltaCorrectedRelIso->at(i);
                    lepDeltaCorrectedRelIso = leptonRelIsoDeltaCorr;
                    if (leptonRelIsoDeltaCorr > RelIsoCut)continue;
                }

                if (leptonsFlavour_ == "electron")
                {
                    iEvent.getByLabel(leptonsRhoCorrectedRelIso_, leptonsRhoCorrectedRelIso);
                    float leptonRelIsoRhoCorr = leptonsRhoCorrectedRelIso->at(i);
                    lepRhoCorrectedRelIso = leptonRelIsoRhoCorr;
                    if (leptonRelIsoRhoCorr > RelIsoCut)continue;
                }

                float leptonPt = 0.;

                //  if(leptonsFlavour_ == "muon" ) {
                iEvent.getByLabel(leptonsPt_, leptonsPt);
                leptonPt = leptonsPt->at(i);
                if ( leptonPt < 26.) continue;
                //  }
                //Apply isolation cut
                if (!gotLeptons)
                {

                    if (leptonsFlavour_ == "muon")
                    {
                        iEvent.getByLabel(leptonsRhoCorrectedRelIso_, leptonsRhoCorrectedRelIso);
                        lepRhoCorrectedRelIso = leptonsRhoCorrectedRelIso->at(i);
                    }



                    //    if(leptonsFlavour_ == "electron"){
                    //  iEvent.getByLabel(leptonsPt_,leptonsPt);
                    //  leptonPt = leptonsPt->at(i);
                    // }

                    iEvent.getByLabel(leptonsEta_, leptonsEta);
                    iEvent.getByLabel(leptonsPhi_, leptonsPhi);
                    iEvent.getByLabel(leptonsEnergy_, leptonsEnergy);
                    iEvent.getByLabel(leptonsCharge_, leptonsCharge);
                    iEvent.getByLabel(leptonsID_, leptonsID);
                    iEvent.getByLabel(leptonsDB_, leptonsDB);
                    gotLeptons = true;
                }
                //if electron apply ID cuts
                if (leptonsFlavour_ == "electron"  )
                {
                    if (leptonsID->size() == 0)cout << "warning requiring ele id of collection which has no entries! Check the leptonsFlavour parameter " << endl;

                    float leptonRelIsoRhoCorr = leptonsRhoCorrectedRelIso->at(i);
                    lepRhoCorrectedRelIso = leptonRelIsoRhoCorr;
                    //if(leptonRelIsoRhoCorr>RelIsoCut)continue;

                    iEvent.getByLabel(leptonsMVAID_, leptonsMVAID);

                    float leptonID = leptonsID->at(i);
                    float leptonMVAID = leptonsMVAID->at(i);

                    if (leptonMVAID < 0 )continue;
                    //Legenda for eleId : 0 fail, 1 ID only, 2 iso Only, 3 ID iso only, 4 conv rej, 5 conv rej and ID, 6 conv rej and iso, 7 all
                    //Require Full ID selection

                    //if ((leptonID != 7) && leptonID != 5)continue;
                    electronID = leptonID;
                    //This is to require conv rejection and ID but do not make requests on iso from id
                    //  if (!(leptonID==5 || leptonID ==7))continue;
                }
                if (leptonsFlavour_ == "muon"  )
                {
                    iEvent.getByLabel(leptonsDZ_, leptonsDZ);
                    if ( leptonsDZ->at(i) > 0.1) continue;
                }
                float leptonDB = leptonsDB->at(i);
                if ( fabs(leptonDB) > 0.02) continue;

                float leptonPhi = leptonsPhi->at(i);
                float leptonEta = leptonsEta->at(i);
                float leptonE = leptonsEnergy->at(i);
                //Build the lepton 4-momentum
                ++nLeptons;

                leptons[nLeptons - 1] = math::PtEtaPhiELorentzVector(leptonPt, leptonEta, leptonPhi, leptonE);
                //  Leptons.push_back(math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE));
                if (nLeptons >= 3) break;

                //  cout<< " lepton number " << nLeptons << " pt "<< leptonPt << " eta " << fabs(leptonEta)<< endl;
            }

            bool passesLeptons = (nLeptons == 1);
            bool passesOneLepton = (nLeptons == 1);
            if (passesLeptons)
            {
                if (passesLeptons && syst == "noSyst")++passingLepton;

                iEvent.getByLabel(looseMuonsDeltaCorrectedRelIso_, looseMuonsDeltaCorrectedRelIso);
                if (passesLeptons && syst == "noSyst" && looseMuonsDeltaCorrectedRelIso->size() == 1)++passingMuonVeto;
                iEvent.getByLabel(looseElectronsDeltaCorrectedRelIso_, looseElectronsDeltaCorrectedRelIso);
                bool passesLooseLeptons = (looseMuonsDeltaCorrectedRelIso->size() + looseElectronsDeltaCorrectedRelIso->size()) == 1;
                passesLeptons = passesLeptons && passesLooseLeptons;
            }
            if (passesLeptons && syst == "noSyst")++passingLeptonVeto;

            isQCD = (!passesLeptons);
            //      isQCD = (!passesOneLepton);

            //Loop for the qcd leptons
            if (doQCD_ && isQCD)
            {
                iEvent.getByLabel(looseMuonsDeltaCorrectedRelIso_, looseMuonsDeltaCorrectedRelIso);
                iEvent.getByLabel(looseElectronsDeltaCorrectedRelIso_, looseElectronsDeltaCorrectedRelIso);
                
                bool hasLooseElectrons = looseElectronsDeltaCorrectedRelIso->size() != 0;
                bool hasLooseMuons =  looseMuonsDeltaCorrectedRelIso->size() != 0;

                if (hasLooseElectrons or hasLooseMuons) continue;
            
                iEvent.getByLabel(qcdLeptonsDeltaCorrectedRelIso_, qcdLeptonsDeltaCorrectedRelIso);
        		iEvent.getByLabel(qcdLeptonsRhoCorrectedRelIso_, qcdLeptonsRhoCorrectedRelIso);

                for (size_t i = 0; i < qcdLeptonsDeltaCorrectedRelIso->size(); ++i)
                {

		  float leptonPt = 0.;
		  
		  //  if(leptonsFlavour_ == "muon" ) {
                    iEvent.getByLabel(qcdLeptonsPt_, qcdLeptonsPt);
                    leptonPt = qcdLeptonsPt->at(i);
                    if ( leptonPt < 26.) continue;


                    float leptonRelIso = qcdLeptonsDeltaCorrectedRelIso->at(i);
		    //		    cout << "qcd lep " << i << "rel iso "<<leptonRelIso<<endl;

		    		    
        		    float leptonQCDRelIso = leptonRelIso;
                            //Use an anti-isolation requirement

        		    lepDeltaCorrectedRelIso = leptonRelIso;
        		    lepRhoCorrectedRelIso = qcdLeptonsRhoCorrectedRelIso->at(i) ;

                    if (leptonsFlavour_ == "muon")
                    {
                        if ( leptonQCDRelIso > leptonRelIsoQCDCutUpper )continue;
                        if ( leptonQCDRelIso < leptonRelIsoQCDCutLower )continue;
			
                        if (!gotQCDLeptons)
                        {
                            iEvent.getByLabel(qcdLeptonsEta_, qcdLeptonsEta);
                            //iEvent.getByLabel(qcdLeptonsPt_,qcdLeptonsPt);
                            iEvent.getByLabel(qcdLeptonsPhi_, qcdLeptonsPhi);
                            iEvent.getByLabel(qcdLeptonsEnergy_, qcdLeptonsEnergy);
                            iEvent.getByLabel(qcdLeptonsCharge_, qcdLeptonsCharge);
                            iEvent.getByLabel(qcdLeptonsID_, qcdLeptonsID);


                            iEvent.getByLabel(qcdLeptonsDB_, qcdLeptonsDB);
                            gotQCDLeptons = true;

			    //			    cout << " qcd lep "<< endl;
                        }
                    }

                    if (leptonsFlavour_ == "electron"  )
                    {
                        bool QCDCondition = false;
                        iEvent.getByLabel(qcdLeptonsID_, qcdLeptonsID);
                        iEvent.getByLabel(qcdLeptonsDB_, qcdLeptonsDB);
                        float leptonID = qcdLeptonsID->at(i);
                        float beamspot  = abs(qcdLeptonsDB->at(i));
                        bool isid = (leptonID ==  1 || leptonID == 3 || leptonID == 5 || leptonID == 7);
                        //Legenda for eleId : 0 fail, 1 ID only, 2 iso Only, 3 ID iso only, 4 conv rej, 5 conv rej and ID, 6 conv rej and iso, 7 all
                        QCDCondition = (!(leptonRelIso < 0.1) && !(beamspot < 0.02))  || (!(leptonRelIso < 0.1) && !isid) || (!isid && !(beamspot < 0.02));
                        electronID = leptonID;



                        if (!QCDCondition) continue;
                        if (!gotQCDLeptons)
                        {
                            iEvent.getByLabel(qcdLeptonsEta_, qcdLeptonsEta);
                            iEvent.getByLabel(qcdLeptonsPhi_, qcdLeptonsPhi);
                            iEvent.getByLabel(qcdLeptonsEnergy_, qcdLeptonsEnergy);
                            iEvent.getByLabel(qcdLeptonsCharge_, qcdLeptonsCharge);
                            gotQCDLeptons = true;
                        }
                    }
		    
                    lepRelIso = leptonRelIso;

                    float qcdLeptonPt = qcdLeptonsPt->at(i);
                    float qcdLeptonPhi = qcdLeptonsPhi->at(i);
                    float qcdLeptonEta = qcdLeptonsEta->at(i);
                    float qcdLeptonE = qcdLeptonsEnergy->at(i);
                    //Create the lepton
                    ++nQCDLeptons;

                    qcdLeptons[nQCDLeptons - 1] = math::PtEtaPhiELorentzVector(qcdLeptonPt, qcdLeptonEta, qcdLeptonPhi, qcdLeptonE);
                    //   leptonsQCD.push_back(math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE));
                    if (nQCDLeptons == 3) break;

                }
            }
            didLeptonLoop = true;
	    
	    isQCD = (nQCDLeptons == 1 && !passesLeptons);
	    
            passesLeptonStep = (passesLeptons || isQCD);
	    //cout << " nqcd lep "<<nQCDLeptons<< " passes leptons? " <<passesLeptons<<endl;
	}
        if (!passesLeptonStep)continue;

        if (!gotPV)
        {
            iEvent.getByLabel(vertexZ_, vertexZ);
            npv = vertexZ->size();
        }

        //Clear the vector of btags //NOT USED NOW
        //    b_weight_tag_algo1.clear();
        //    b_weight_tag_algo2.clear();
        //    b_weight_antitag_algo1.clear();
        //    b_weight_antitag_algo2.clear();
        //        b_discriminator_value_tag_algo1.clear();
        //    b_discriminator_value_antitag_algo2.clear();

        ntchpt_tags = 0;
        ncsvl_tags = 0;
        ncsvt_tags = 0;
        ncsvm_tags = 0;

        ntight_tags = 0;

        jsfshpt.clear();//  bjs.clear();cjs.clear();ljs.clear();
        jsfscsvt.clear();//  bjs.clear();cjs.clear();ljs.clear();
        jsfscsvm.clear();//  bjs.clear();cjs.clear();ljs.clear();
        //    jsfshel.clear();//  bjs.clear();cjs.clear();ljs.clear();

        //Clear the vectors of non-leptons
        //    jets.clear();
        //    bjets.clear();
        //    antibjets.clear();



        //  cout << " test 1 "<<endl;

        //cout << " before met "<<endl;

        bool hasTurnOnWeight = false;
        double turnOnWeightValue = 1;
        turnOnReWeightTree = 1;
        turnOnWeightTreeJetTrig1Up = 1;
        turnOnWeightTreeJetTrig1Down = 1;
        turnOnWeightTreeJetTrig2Up = 1;
        turnOnWeightTreeJetTrig2Down = 1;
        turnOnWeightTreeJetTrig3Up = 1;
        turnOnWeightTreeJetTrig3Down = 1;

        turnOnWeightTreeBTagTrig1Up = 1;
        turnOnWeightTreeBTagTrig1Down = 1;
        turnOnWeightTreeBTagTrig2Up = 1;
        turnOnWeightTreeBTagTrig2Down = 1;
        turnOnWeightTreeBTagTrig3Up = 1;
        turnOnWeightTreeBTagTrig3Down = 1;

        bWeightTree = 1;
        bWeightTreeBTagUp = 1;
        bWeightTreeMisTagUp = 1;
        bWeightTreeBTagDown = 1;
        bWeightTreeMisTagDown = 1;


        if (!gotMets)
        {
            iEvent.getByLabel(METPhi_, METPhi);
            iEvent.getByLabel(METPt_, METPt);

            metPx = METPt->at(0) * cos(METPhi->at(0));
            metPy = METPt->at(0) * sin(METPhi->at(0));

            metPxTmp = metPx;
            metPyTmp = metPy;

            metPhi = METPhi->at(0);


            gotMets = true;
        }

        metPx = metPxTmp;
        metPy = metPyTmp;


        if (syst_name == "UnclusteredMETUp")
        {
            iEvent.getByLabel(UnclMETPx_, UnclMETPx);
            iEvent.getByLabel(UnclMETPy_, UnclMETPy);
            metPx += (*UnclMETPx) * 0.1;
            metPy += (*UnclMETPy) * 0.1;
        }
        if (syst_name == "UnclusteredMETDown")
        {
            iEvent.getByLabel(UnclMETPx_, UnclMETPx);
            iEvent.getByLabel(UnclMETPy_, UnclMETPy);
            metPx -= (*UnclMETPx) * 0.1;
            metPy -= (*UnclMETPy) * 0.1;
        }


        //    cout << " before jets "<<endl;

        if (!gotJets)
        {
            iEvent.getByLabel(jetsEta_, jetsEta);
            iEvent.getByLabel(jetsPhi_, jetsPhi);

            iEvent.getByLabel(jetsEnergy_, jetsEnergy);
            iEvent.getByLabel(jetsBTagAlgo_, jetsBTagAlgo);
            iEvent.getByLabel(jetsAntiBTagAlgo_, jetsAntiBTagAlgo);

            iEvent.getByLabel(jetsPileUpID_, jetsPileUpID);
            iEvent.getByLabel(jetsPileUpWP_, jetsPileUpWP);

            iEvent.getByLabel(jetsBeta_, jetsBeta);
            iEvent.getByLabel(jetsDZ_, jetsDZ);
            iEvent.getByLabel(jetsRMS_, jetsRMS);

            iEvent.getByLabel(jetsFlavour_, jetsFlavour);
            iEvent.getByLabel(jetsCorrTotal_, jetsCorrTotal);
            if (doResol_)iEvent.getByLabel(genJetsPt_, genJetsPt);

            /*      if(channel != "Data"){
            iEvent.getByLabel(x1_,x1h);
            iEvent.getByLabel(x2_,x2h);

            x1 = *x1h;
            x2 = *x2h;
            }
            Q2 = x1 * x2 * 7000*7000;
            */
            gotJets = true;
        }

        if (syst == "noSyst"
                || syst == "JESUp" || syst == "JESDown"
                || syst == "JERUp" || syst == "JERDown"
                || syst == "BTagUp" || syst == "BTagDown"
                || syst == "MisTagUp" || syst == "MisTagDown"
           )
        {
            for (size_t i = 0; i < jetsPt->size(); ++i)
            {

                eta = jetsEta->at(i);
                if (fabs(eta ) > 4.5)continue;
                ptCorr = jetsPt->at(i);
                flavour = jetsFlavour->at(i);
                double energyCorr = jetsEnergy->at(i);



                //      float geneta =genJetsEta->at(i);
                float genpt = -1.;
                if (doResol_)genpt = genJetsPt->at(i);
                float rndm = 0.1;

                //If systematics JES up/down we need to change the pt of the jet
                //consider if it passes the threshold or not

                if (doResol_ && genpt > 0.0)
                {
                    resolScale = resolSF(fabs(eta), syst_name);
                    double smear = std::max((double)(0.0), (double)(ptCorr + (ptCorr - genpt) * resolScale) / ptCorr);
                    energyCorr = energyCorr * smear;
                    ptCorr = ptCorr * smear;
                }

                /*      if(doReCorrection_){
                  ptCorr = ptCorr/jetsCorrTotal->at(i);
                  JetCorrectorMC->setJetPt(ptCorr);
                  JetCorrectorMC->setJetEta(eta);
                  double JECorr = JetCorrectorMC->getCorrection();
                ptCorr = ptCorr*JECorr;
                energyCorr = energyCorr/jetsCorrTotal->at(i)*JECorr;
                //  JetCorrectorMC.setJetPt(ptCorr);
                //JetCorrectorMC.setJetEta(eta);
                //ptCorr = ptCorr*JetCorrectorMC.getCorrection();
                }*/

                if (syst_name == "JESUp")
                {
                    unc = jetUncertainty( eta,  ptCorr, flavour);
		    //		    cout << syst << "  "<< unc << endl; 
                    ptCorr = ptCorr * (1 + unc);
                    energyCorr = energyCorr * (1 + unc);
                    metPx -= (jetsPt->at(i) * cos(jetsPhi->at(i))) * unc;
                    metPy -= (jetsPt->at(i) * sin(jetsPhi->at(i))) * unc;
                }
                if (syst_name == "JESDown")
                {
                    unc = jetUncertainty( eta,  ptCorr, flavour);
                    ptCorr = ptCorr * (1 - unc);
                    energyCorr = energyCorr * (1 - unc);
                    metPx -= -(jetsPt->at(i) * cos(jetsPhi->at(i))) * unc;
                    metPy -= -(jetsPt->at(i) * sin(jetsPhi->at(i))) * unc;
                }


		HT+= (math::PtEtaPhiELorentzVector(ptCorr, jetsEta->at(i), jetsPhi->at(i), energyCorr)).Et();

                //Pt cut
                bool passesPtCut = ptCorr > ptCut;
                if (passesPtCut)
                {
                    ++nJets;
                    if ( fabs(eta) < 2.5)++nJetsCentral;
                    else ++nJetsForward;
                    if ( jetsPileUpWP->at(i) > 2.5)
                    {
                        ++nJetsNoPU;
                        if ( fabs(eta) < 2.5)++nJetsCentralNoPU;
                        else ++nJetsForwardNoPU;
                    }
                    jets[nJets - 1] = math::PtEtaPhiELorentzVector(ptCorr, jetsEta->at(i), jetsPhi->at(i), energyCorr);
                    flavours[nJets - 1] = flavour;
                    if (syst == "noSyst")
                    {
                        ++nJetsNoSyst;
                        jetsNoSyst[nJets - 1] = jets[nJets - 1];
			//			cout <<" jet no syst "<< nJets-1<<" pt "  <<jetsNoSyst[nJets-1].pt()<<endl;

		    }
		}

                //b tag thresholds

                double valueTCHPT = jetsBTagAlgo->at(i);
                double valueCSV = jetsAntiBTagAlgo->at(i);

                bool passesTCHPT = jetsBTagAlgo->at(i) > 3.41; //TCHPT Working point
                bool passesCSVT = jetsAntiBTagAlgo->at(i) > 0.898; //TCHPT Working point

		bool passesCSVM = jetsAntiBTagAlgo->at(i)>0.244;//ACTUALLY IT IS LOOSE WORKING POINT

		//		bool passesCSVM = jetsAntiBTagAlgo->at(i) > 0.679;

                double valueChosenAlgo = valueCSV;
                if (algo_ == "TCHPT")valueChosenAlgo = valueTCHPT;

                if (!passesPtCut) continue;




                //max pt position:
                int pos = nJets - 1;
                //cout << " pos " << pos << " j pt " << ptCorr << endl;
                if (ptCorr > maxPtTree)
                {
                    maxPtTreePosition = nJets - 1;
                    maxPtTree = ptCorr;
                    firstJetFlavourTree = flavour;
                    //cout << " first jet pos " << maxPtTreePosition  << " pt "<< maxPtTree <<endl ;
                }


                //min pt position:
                if (ptCorr < minPtTree)
                {
                    minPtTreePosition = nJets - 1;
                    minPtTree = ptCorr;
                }


                //Passes firs algorythm (b tag requirement in the case of t-channel standard selection)

                double etaMin =  min(fabs(eta), (float)2.3999);
                double ptMin =  min(ptCorr, (float)239.9); //min(jets.back().pt(),998.0);
                measurePoint.insert(BinningVariables::JetAbsEta, etaMin);
                measurePoint.insert(BinningVariables::JetEt, ptMin);
                //Apply different SFs if it is b,c or light jet
                if (abs(flavour) == 4)
                {
                    ++nc;
                    if (is_btag_relevant )
                    {
                        double hptSF = 1;
                        double hptSFErr = 0;

                        double csvtSF = 1;
                        double csvtSFErr = 0;

                        double csvmSF = 1;
                        double csvmSFErr = 0;

                        double hpteff = EFFMap("TCHPT_C");
                        double csvteff = EFFMap("CSVT_C", channel);
                        double csvmeff = EFFMap("CSVL_C", channel);

                        //double hpteff = EFFMapNew(valueAlgo1,"TCHP_C");
                        //double heleff = EFFMapNew(valueAlgo2,"TCHE_C");

                        if (abs(eta) > 2.6)
                        {
                            hpteff = 0;
                            csvteff = 0;
                            csvmeff = 0;
                        }

                        if (  takeBTagSFFromDB_)
                        {
                            hptSF = (perfBHP->getResult(PerformanceResult::BTAGBEFFCORR, measurePoint));
                            hptSFErr = fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR, measurePoint));
                        }
                        else
                        {
                            hptSF = BTagSFNew(ptCorr, "TCHPT");
                            csvtSF = BTagSFNew(ptCorr, "CSVT");
                            csvmSF = BTagSFNew(ptCorr, "CSVL");

                            hptSFErr = BTagSFErrNew(ptCorr, "TCHPT") * facBTagErr;
                            csvtSFErr = BTagSFErrNew(ptCorr, "CSVT") * facBTagErr;
                            csvmSFErr = BTagSFErrNew(ptCorr, "CSVL") * facBTagErr;

                            //hptSFErr = BTagSFErrNew(ptCorr,"TCHPT");
                            //      csvtSF = BTagSFErrNew(ptCorr,"TCHPT");
                            //      csvmSF = BTagSFErrNew(ptCorr,"TCHPT");
                        }

                        jsfshpt.push_back(BTagWeight::JetInfo(hpteff, hptSF));
                        jsfshpt_mis_tag_up.push_back(BTagWeight::JetInfo(hpteff, hptSF));
                        jsfshpt_mis_tag_down.push_back(BTagWeight::JetInfo(hpteff, hptSF));

                        jsfscsvt.push_back(BTagWeight::JetInfo(csvteff, csvtSF));
                        jsfscsvt_mis_tag_up.push_back(BTagWeight::JetInfo(csvteff, csvtSF));
                        jsfscsvt_mis_tag_down.push_back(BTagWeight::JetInfo(csvteff, csvtSF));

                        jsfscsvm.push_back(BTagWeight::JetInfo(csvmeff, csvmSF));
                        jsfscsvm_mis_tag_up.push_back(BTagWeight::JetInfo(csvmeff, csvmSF));
                        jsfscsvm_mis_tag_down.push_back(BTagWeight::JetInfo(csvmeff, csvmSF));


                        if (syst == "noSyst")
                        {
                            jsfshpt_b_tag_up.push_back(BTagWeight::JetInfo(hpteff, hptSF + 2 * hptSFErr));
                            jsfshpt_b_tag_down.push_back(BTagWeight::JetInfo(hpteff, hptSF - 2 * hptSFErr));

                            jsfscsvt_b_tag_up.push_back(BTagWeight::JetInfo(csvteff, csvtSF + 2 * csvtSFErr));
                            jsfscsvt_b_tag_down.push_back(BTagWeight::JetInfo(csvteff, csvtSF - 2 * csvtSFErr));

                            jsfscsvm_b_tag_up.push_back(BTagWeight::JetInfo(csvmeff, csvmSF + 2 * csvmSFErr));
                            jsfscsvm_b_tag_down.push_back(BTagWeight::JetInfo(csvmeff, csvmSF - 2 * csvmSFErr));

                        }
                    }
                }
                else if (abs(flavour) == 5)
                {
                    ++nb;
                    if (is_btag_relevant )
                    {
                        double hptSF = 1;
                        double hptSFErr = 0;
                        double csvtSF = 1;
                        double csvtSFErr = 0;
                        double csvmSF = 1;
                        double csvmSFErr = 0;

                        double hpteff = EFFMap("TCHPT_B");
                        double csvteff = EFFMap("CSVT_B", channel);
                        double csvmeff = EFFMap("CSVL_B", channel);

                        //double hpteff = EFFMapNew(valueAlgo1,"TCHP_C");
                        //double heleff = EFFMapNew(valueAlgo2,"TCHE_C");

                        if (abs(eta) > 2.6)
                        {
                            hpteff = 0;
                            csvteff = 0;
                            csvmeff = 0;
                        }

                        if (  takeBTagSFFromDB_)
                        {
                            hptSF = (perfBHP->getResult(PerformanceResult::BTAGBEFFCORR, measurePoint));
                            hptSFErr = fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR, measurePoint));
                        }
                        else
                        {
                            hptSF = BTagSFNew(ptCorr, "TCHPT");
                            csvtSF = BTagSFNew(ptCorr, "CSVT");
                            csvmSF = BTagSFNew(ptCorr, "CSVL");

                            hptSFErr = BTagSFErrNew(ptCorr, "TCHPT") * facBTagErr;
                            csvtSFErr = BTagSFErrNew(ptCorr, "CSVT") * facBTagErr;
                            csvmSFErr = BTagSFErrNew(ptCorr, "CSVL") * facBTagErr;

                        }

                        jsfshpt.push_back(BTagWeight::JetInfo(hpteff, hptSF));
                        jsfshpt_mis_tag_up.push_back(BTagWeight::JetInfo(hpteff, hptSF));
                        jsfshpt_mis_tag_down.push_back(BTagWeight::JetInfo(hpteff, hptSF));

                        jsfscsvt.push_back(BTagWeight::JetInfo(csvteff, csvtSF));
                        jsfscsvt_mis_tag_up.push_back(BTagWeight::JetInfo(csvteff, csvtSF));
                        jsfscsvt_mis_tag_down.push_back(BTagWeight::JetInfo(csvteff, csvtSF));

                        jsfscsvm.push_back(BTagWeight::JetInfo(csvmeff, csvmSF));
                        jsfscsvm_mis_tag_up.push_back(BTagWeight::JetInfo(csvmeff, csvmSF));
                        jsfscsvm_mis_tag_down.push_back(BTagWeight::JetInfo(csvmeff, csvmSF));


                        if (syst == "noSyst")
                        {
                            jsfshpt_b_tag_up.push_back(BTagWeight::JetInfo(hpteff, hptSF + hptSFErr));
                            jsfshpt_b_tag_down.push_back(BTagWeight::JetInfo(hpteff, hptSF - hptSFErr));

                            jsfscsvt_b_tag_up.push_back(BTagWeight::JetInfo(csvteff, csvtSF + csvtSFErr));
                            jsfscsvt_b_tag_down.push_back(BTagWeight::JetInfo(csvteff, csvtSF - csvtSFErr));

                            jsfscsvm_b_tag_up.push_back(BTagWeight::JetInfo(csvmeff, csvmSF + csvmSFErr));
                            jsfscsvm_b_tag_down.push_back(BTagWeight::JetInfo(csvmeff, csvmSF - csvmSFErr));

                        }
                    }

                }
                else
                {
                    if (is_btag_relevant )
                    {
                        double hptSF = 1;
                        double hptSFErrUp = 0;
                        double hptSFErrDown = 0;

                        double csvtSF = 1;
                        double csvtSFErrUp = 0;
                        double csvtSFErrDown = 0;

                        double csvmSF = 1;
                        double csvmSFErrUp = 0;
                        double csvmSFErrDown = 0;

                        double hpteff = EFFMap("TCHPT_L");
                        double csvteff = EFFMap("CSVT_L", channel);
                        double csvmeff = EFFMap("CSVL_L", channel);


                        if (abs(eta) > 2.6)
                        {
                            hpteff = 0;
                            csvteff = 0;
                            csvmeff = 0;
                        }

                        if (  takeBTagSFFromDB_)
                        {
                            hpteff = (perfMHP->getResult(PerformanceResult::BTAGLEFF, measurePoint));
                            hptSF = (perfMHP->getResult(PerformanceResult::BTAGLEFFCORR, measurePoint));

                        }
                        else
                        {
                            //      hpteff = EFFMapNew(valueAlgo1,"TCHP_L");
                            //      heleff = EFFMapNew(valueAlgo2,"TCHE_L");

			  hptSF = MisTagSFNew(ptCorr, eta, "TCHPT");
			  hptSFErrUp = MisTagSFErrNewUp(ptCorr, eta, "TCHPT")* facBTagErr;
			  hptSFErrDown = MisTagSFErrNewDown(ptCorr, eta, "TCHPT")* facBTagErr;

			  csvmSF = MisTagSFNew(ptCorr, eta, "CSVL");
			  csvmSFErrUp = MisTagSFErrNewUp(ptCorr, eta, "CSVL");
			  csvmSFErrDown = MisTagSFErrNewDown(ptCorr, eta, "CSVL");
			  
			  csvtSF = MisTagSFNew(ptCorr, eta, "CSVT");
			  csvtSFErrUp = MisTagSFErrNewUp(ptCorr, eta, "CSVT")* facBTagErr;
			  csvtSFErrDown = MisTagSFErrNewDown(ptCorr, eta, "CSVT")* facBTagErr;
                        }

                        jsfshpt.push_back(BTagWeight::JetInfo(hpteff, hptSF));
                        jsfshpt_b_tag_up.push_back(BTagWeight::JetInfo(hpteff, hptSF));
                        jsfshpt_b_tag_down.push_back(BTagWeight::JetInfo(hpteff, hptSF));

                        jsfscsvt.push_back(BTagWeight::JetInfo(csvteff, hptSF));
                        jsfscsvt_b_tag_up.push_back(BTagWeight::JetInfo(csvteff, hptSF));
                        jsfscsvt_b_tag_down.push_back(BTagWeight::JetInfo(csvteff, hptSF));

                        jsfscsvm.push_back(BTagWeight::JetInfo(csvmeff, hptSF));
                        jsfscsvm_b_tag_up.push_back(BTagWeight::JetInfo(csvmeff, hptSF));
                        jsfscsvm_b_tag_down.push_back(BTagWeight::JetInfo(csvmeff, hptSF));

                        if (syst == "noSyst")
                        {
                            jsfshpt_mis_tag_up.push_back(BTagWeight::JetInfo(hpteff, hptSFErrUp));
                            jsfshpt_mis_tag_down.push_back(BTagWeight::JetInfo(hpteff, hptSFErrDown));

                            jsfscsvt_mis_tag_up.push_back(BTagWeight::JetInfo(csvteff, csvtSFErrUp));
                            jsfscsvt_mis_tag_down.push_back(BTagWeight::JetInfo(csvteff, csvtSFErrDown));

                            jsfscsvm_mis_tag_up.push_back(BTagWeight::JetInfo(csvmeff, csvmSFErrUp));
                            jsfscsvm_mis_tag_down.push_back(BTagWeight::JetInfo(csvmeff, csvmSFErrDown));

                        }
                    }
                    ++nudsg;
                }

                if (is_btag_relevant) measurePoint.reset();

                //  if(passesMediumBTag){
                //    ++ntchpm_tags;
                //  }
                if (passesCSVT)
                {
                    ++ncsvt_tags;
                }
                if (passesCSVM)
                {
                    ++ncsvm_tags;
                }
                if (passesTCHPT)
                {
                    //Add to b-jet collection
                    ++ntchpt_tags;
                }

                bool passesAlgo = passesCSVT;
		if(passesCSVM) ++ncsvl_tags;
                if (algo_ == "TCHPT" ) passesAlgo = passesTCHPT;
                if (passesAlgo)
                {
                    if (syst == "noSyst" )  ++nBJets;
                    bjets[nBJets - 1] = jets[nJets - 1];
                }

                //Condition to find the highest/lowest b-tag
                //according to algo 1 (tchp)
                //cout << " i "<< i <<" jets size "<< nJets << " btag  "<< valueAlgo1<<endl;
                if (valueChosenAlgo > highBTagTree)
                {
                    highBTagTree = valueChosenAlgo;
                    highBTagTreePosition = nJets - 1;
                    bJetFlavourTree = jetsFlavour->at(i);
                    bJetPUID = jetsPileUpID->at(i);
                    bJetPUWP = jetsPileUpWP->at(i);

                    bJetBeta = jetsBeta->at(i);
                    bJetDZ = jetsDZ->at(i);
                    bJetRMS = jetsRMS->at(i);

                }
                if (valueChosenAlgo < lowBTagTree)
                {
                    lowBTagTree = valueChosenAlgo;
                    lowBTagTreePosition = nJets - 1;
                    fJetFlavourTree = jetsFlavour->at(i);
                    fJetPUID = jetsPileUpID->at(i);
                    fJetPUWP = jetsPileUpWP->at(i);

                    fJetBeta = jetsBeta->at(i);
                    fJetDZ = jetsDZ->at(i);
                    fJetRMS = jetsRMS->at(i);
                }
                if (nJets >= 10 )break;
            }
        }

        if (syst == "noSyst")
        {
	  highBTagTreePositionNoSyst = highBTagTreePosition;
	  lowBTagTreePositionNoSyst = lowBTagTreePosition;
            maxPtTreePositionNoSyst = maxPtTreePosition;
            minPtTreePositionNoSyst = minPtTreePosition;
            nbNoSyst = nb;
            ncNoSyst = nc;
            nudsgNoSyst = nudsg;
            jsfshptNoSyst = jsfshpt;
            //      jsfshelNoSyst = jsfshel;
        }
        if (!(syst == "noSyst"
                || syst == "JESUp" || syst == "JESDown"
                || syst == "JERUp" || syst == "JERDown"
                || syst == "BTagUp" || syst == "BTagDown"
                || syst == "MisTagUp" || syst == "MisTagDown" ))
        {
            nJets = nJetsNoSyst;

            ncsvt_tags = nBJets;
            if (algo_ == "TCHPT" ) ntchpt_tags = nBJets;

            ntchel_tags = nLooseBJets;
            nb = nbNoSyst;
            nc = ncNoSyst;
            nudsg = nudsgNoSyst;
            for (size_t a = 0; a < nJetsNoSyst; ++a)
            {
                jets[a] = jetsNoSyst[a];
		//		cout <<" jet no syst "<< a <<" pt "  <<jets[a].pt()<<endl;
            }
            highBTagTreePosition = highBTagTreePositionNoSyst;
            lowBTagTreePosition = lowBTagTreePositionNoSyst;
            maxPtTreePosition = maxPtTreePositionNoSyst;
            minPtTreePosition = minPtTreePositionNoSyst;
            jsfshpt = jsfshptNoSyst;
            //jsfshel = jsfshelNoSyst;

        }

        /*
            //cout <<" syst "<< syst<< " njets "<< nJets << " nJetsNoSyst " << nJetsNoSyst << " nBJets "<< ntchpt_tags<<
        " nBJetsNoSyst "<< nBJets<< " nb "<< nb << " nbNoSyst "<<nbNoSyst<< " lowBPos " <<lowBTagTreePosition << " lowBNoSyst " <<
        lowBTagTreePositionNoSyst<<endl;
        */

        if (!isQCD && leptonsFlavour_ == "mon")
        {
            for (size_t l = 0; l < nLeptons; ++l)
            {
                for (size_t j = 0; j < nJets; ++j)
                {
                    if ( deltaR( leptons[l], jets[j]) < 0.3 )
                    {
                        ;
                        --passingLepton;
                        passesLeptonStep = false;
                    }
                }
            }
        }
        if (passesLeptonStep == false)continue;

        eventFlavourTree = eventFlavour(channel, nb, nc, nudsg);
        //if( !flavourFilter(channel,nb,nc,nudsg) ) continue;


        /////////
        ///End of the standard lepton-jet loop
        /////////

        if (doPU_)
        {
            if (!gotPU )
            {
                //  //cout << " before npv "<<endl;
                //iEvent.getByLabel(nm1_,nm1);
                iEvent.getByLabel(n0_, n0);
                //iEvent.getByLabel(np1_,np1);
                nVertices = *n0;
                
                gotPU = true;
            }

        }
        else(nVertices = -1);

        if (doPU_)
        {
            if (syst == "noSyst")
            {
                PUWeightNoSyst = pileUpSF(syst); PUWeight = PUWeightNoSyst;
                PUWeightTreePUUp = pileUpSF("PUUp");
                PUWeightTreePUDown = pileUpSF("PUDown");
                //    cout<< "n0 " << nVertices <<   " weight = "<< PUWeightNoSyst<< " cross-check "  <<endl;
                
                PUWeightNewNoSyst = pileUpSFNew(); PUWeightNew = PUWeightNewNoSyst;
            }
            else {
               PUWeight = PUWeightNoSyst;
               PUWeightNew = PUWeightNewNoSyst;
            }
        }
        else {
            PUWeight = 1;
            PUWeightNew = 1;
        }
        PUWeightTree = PUWeight;
        weightTree = Weight;

        PUWeightTreeNew = PUWeightNew;
        //Jet trees:

        if (isQCD)
        {
            leptonPFour = qcdLeptons[0];
            chargeTree = qcdLeptonsCharge->at(0) ;
            //  cout << " b is "<< B << " lepton  charge "<< chargeTree<<  endl;
        }
        else
        {
            leptonPFour = leptons[0];
            chargeTree = leptonsCharge->at(0) ;
        }

        metPt = sqrt(metPx * metPx + metPy * metPy);
        MTWValue =  sqrt((leptonPFour.pt() + metPt) * (leptonPFour.pt() + metPt)  - (leptonPFour.px() + metPx) * (leptonPFour.px() + metPx) - (leptonPFour.py() + metPy) * (leptonPFour.py() + metPy));
        mtwMassTree = MTWValue;

        bool passesMet = false;


        runTree = iEvent.eventAuxiliary().run();
        lumiTree = iEvent.eventAuxiliary().luminosityBlock();
        eventTree = iEvent.eventAuxiliary().event();

	//	cout << " syst " << syst << endl;

        for (size_t J_ = 0; J_ < nJets; ++J_ )
        {
            double ptCorr = jets[J_].pt();
            if (ptCorr > secondPt &&  ptCorr < maxPtTree)
            {
                secondPt = ptCorr;
                secondPtPosition = J_ ;
                secondJetFlavourTree = flavours[J_];
		//      cout << " second jet pos " <<secondPtPosition << " pt "<<secondPt <<endl ;
            }
        }

        for (size_t J_ = 0; J_ < nJets; ++J_ )
        {
            double ptCorr = jets[J_].pt();
            if (ptCorr > thirdPt &&  ptCorr < secondPt)
            {
                thirdPt = ptCorr;
                thirdPtPosition = J_;
                thirdJetFlavourTree = flavours[J_];
		// cout << " third jet pos " << thirdPtPosition << " pt "<< thirdPt <<endl ;
            }
        }

	//        if (thirdPt > secondPt ) cout << "  sanity check: Pt3 > Pt2 at event" << eventTree << " njets "<< nJets <<endl;
        //if (secondPt > maxPtTree ) cout << "  sanity check: Pt2 > Pt1 at event" << eventTree <<" njets "<< nJets <<endl;
        //if (thirdPt > maxPtTree ) cout << "  sanity check: Pt3 > Pt1 at event" << eventTree << " njets "<< nJets <<endl;


        if (nJets > 0)
        {

            firstJetPt = jets[maxPtTreePosition].pt();
            firstJetE = jets[maxPtTreePosition].energy();
            firstJetEta = jets[maxPtTreePosition].eta();
            firstJetPhi = jets[maxPtTreePosition].phi();



            if (nJets > 1)
            {

                secondJetPt = jets[secondPtPosition].pt();
                secondJetE = jets[secondPtPosition].energy();
                secondJetEta = jets[secondPtPosition].eta();
                secondJetPhi = jets[secondPtPosition].phi();

            }

            if (nJets > 2)
            {
                thirdJetPt = jets[thirdPtPosition].pt();
                thirdJetE = jets[thirdPtPosition].energy();
                thirdJetEta = jets[thirdPtPosition].eta();
                thirdJetPhi = jets[thirdPtPosition].phi();

                //    cout << " first jet pt "<< firstJetPt <<endl ;
                //cout << "second jet pt "<<secondPt <<endl ;
                //cout << " third jet pt "<< thirdPt <<endl ;
            }
        }
        else
        {
            firstJetFlavourTree = 0;
            secondJetFlavourTree = 0;
            thirdJetFlavourTree = 0;

            firstJetPt = 0;
            firstJetE = 0;
            firstJetEta = -99;
            firstJetPhi = -99;

            secondJetPt = 0;
            secondJetE = 0;
            secondJetEta = -99;
            secondJetPhi = -99;

            thirdJetPt = 0;
            thirdJetE = 0;
            thirdJetEta = -99;
            thirdJetPhi = -99;


        }




        if (doJetTrees_ && !isQCD)
        {
            if (syst == "noSyst")
            {
                jetprobs.clear();
                for (size_t i = 0; i < jetsEta->size(); ++i)
                {
                    double eta = jetsEta->at(i);
                    double btag = jetsBTagAlgo->at(i);
                    double pt = jetsPt->at(i);
                    if (fabs(eta) > 2.6) jetprobs.push_back(0.);
                    jetprobs.push_back(jetprob(pt, btag, eta, syst));
                }

                if (leptonsFlavour_ == "muon" )lepEff = muonHLTEff(leptons[0].eta(),"Mu2012A");
                if (leptonsFlavour_ == "muon" )lepEffB = muonHLTEff(leptons[0].eta(),"Mu2012B");
                if (leptonsFlavour_ == "electron" )lepEff = 1;

                lepPt = leptons[0].pt();

                turnOnWeightValue = turnOnProbs("noSyst", 1);
                w1TCHPT = b_tchpt_1_tag.weight(jsfshpt, ntchpt_tags);
                w2TCHPT = b_tchpt_2_tags.weight(jsfshpt, ntchpt_tags);
                w1CSVT = b_csvt_1_tag.weight(jsfscsvt, ncsvt_tags);
                w2CSVT = b_csvt_2_tags.weight(jsfscsvt, ncsvt_tags);
                w1CSVM = b_csvm_1_tag.weight(jsfscsvt, ncsvm_tags);
                w2CSVM = b_csvm_2_tags.weight(jsfscsvt, ncsvm_tags);

                nJ = nJets;
                nJNoPU = nJetsNoPU;

                nJCentralNoPU = nJetsCentralNoPU;
                nJCentral = nJetsCentral;

                nJForwardNoPU = nJetsForwardNoPU;
                nJForward = nJetsForward;

                //  if(nJ > 2) cout << " nJ>3 check "<<  nJets << " third pt "<< thirdPt<<endl;

                treesNJets[syst]->Fill();
            }

        }
        
        ntight_tags = ncsvt_tags;
        if (algo_ == "TCHPT")ntight_tags = ntchpt_tags;
        if ( nJets < 2 )continue;
        if (nJets > 3)continue;

        //    if( maxPtTree< maxPtCut )continue;

        //LEGENDA
        //    0T = 0;
        //    1T = 1;
        //    2T = 2;
        //    0T_QCD=3;
        //    1T_QCD=4;
        //    2T_QCD=5;

        if (nJets == 2 || nJets == 3)
        {

            int B;
            if (ntight_tags == 0) B = 0 ;
            else if (ntight_tags == 1)B = 1;
            else if (ntight_tags == 2)B = 2;
            else continue;



            if (isQCD)
            {
                B += 3;
                //leptonPFour = qcdLeptons[0];
                //  chargeTree = qcdLeptonsCharge->at(0) ;
                //cout << " b is " << B << " lepton  charge " << chargeTree <<  endl;
            }
            //      else {
            //  leptonPFour = leptons[0];
            //chargeTree = leptonsCharge->at(0) ;
            //      }

            if ( syst == "noSyst" && nJets == 2 && B < 3)
            {
                ++passingJets;
            }

            if ( (B == 0 || B == 3 ) && (ntchpt_tags != 0  || lowBTagTreePosition < 0 || lowBTagTreePosition == highBTagTreePosition) ) continue; //Sample A condition, ok for now
	    
	    if(doLooseBJetVeto_)if(nJets==2 && (B == 1 || B==4))if( ncsvl_tags != 1 )continue;


            if (syst == "noSyst")
            {
                bWeightNoSyst = bTagSF(B);  bWeightTree = bWeightNoSyst;
                bWeightTreeBTagUp = bTagSF(B, "BTagUp");
                bWeightTreeBTagDown = bTagSF(B, "BTagDown");
                bWeightTreeMisTagUp = bTagSF(B, "MisTagUp");
                bWeightTreeMisTagDown = bTagSF(B, "MisTagDown");

                /*
                  vetoTree = vetoSF(B);
                  vetoTreeBTagUp = vetoSF(B,"BTagUp");
                  vetoTreeBTagDown = vetoSF(B,"BTagDown");
                  vetoTreeMisTagUp = vetoSF(B,"MisTagUp");
                  vetoTreeMisTagDown = vetoSF(B,"MisTagDown");
                */
            }
            else if (syst == "JESUp" || syst == "JESDown" ||
                     syst == "JERUp" || syst == "JERDown" ||
                     syst == "BTagUp" || syst == "BTagDown" ||
                     syst == "MisTagUp" || syst == "MisTagDown" ) bWeightTree = bTagSF(B);
            else bWeightTree = bWeightNoSyst;

            //cout << " before npv "<<endl;


            //cout << " before turnon loop"<<endl;


            if ( //leptonsFlavour_ == "electron" &&
                doTurnOn_)
            {
                if (syst == "noSyst" && (B == 1 || B == 4))
                {
                    jetprobs.clear();
                    jetprobs_j1up.clear();
                    jetprobs_j2up.clear();
                    jetprobs_j3up.clear();
                    jetprobs_b1up.clear();
                    jetprobs_b2up.clear();
                    jetprobs_b3up.clear();
                    jetprobs_j1down.clear();
                    jetprobs_j2down.clear();
                    jetprobs_j3down.clear();
                    jetprobs_b1down.clear();
                    jetprobs_b2down.clear();
                    jetprobs_b3down.clear();
                    for (size_t i = 0; i < jetsEta->size(); ++i)
                    {
                        double eta = jetsEta->at(i);
                        double btag = jetsBTagAlgo->at(i);
                        double pt = jetsPt->at(i);

                        pushJetProbs(pt, btag, eta);
                    }
                    //cout << "right before turn on "<< endl;
                    turnOnWeightValue = turnOnProbs("noSyst", 1);
                    turnOnWeightTreeJetTrig1Up = turnOnProbs("JetTrig1Up", 1);
                    turnOnWeightTreeJetTrig1Down = turnOnProbs("JetTrig1Down", 1);
                    turnOnWeightTreeJetTrig2Up = turnOnProbs("JetTrig2Up", 1);
                    turnOnWeightTreeJetTrig2Down = turnOnProbs("JetTrig2Down", 1);
                    turnOnWeightTreeJetTrig3Up = turnOnProbs("JetTrig3Up", 1);
                    turnOnWeightTreeJetTrig3Down = turnOnProbs("JetTrig3Down", 1);

                    turnOnWeightTreeBTagTrig1Up = turnOnProbs("BTagTrig1Up", 1);
                    turnOnWeightTreeBTagTrig1Down = turnOnProbs("BTagTrig1Down", 1);
                    turnOnWeightTreeBTagTrig2Up = turnOnProbs("BTagTrig2Up", 1);
                    turnOnWeightTreeBTagTrig2Down = turnOnProbs("BTagTrig2Down", 1);
                    turnOnWeightTreeBTagTrig3Up = turnOnProbs("BTagTrig3Up", 1);
                    turnOnWeightTreeBTagTrig3Down = turnOnProbs("BTagTrig3Down", 1);
                    //    turnOnWeightValue = turnOnWeight(jetprobs,1);
                    if (syst == "noSyst") turnOnWeightValueNoSyst = turnOnWeightValue;
                    if (syst == "noSyst") turnOnReWeightTreeNoSyst = turnOnReWeight(turnOnWeightValue, jets[highBTagTreePosition].pt(), highBTagTree);
                    //cout <<  " test right after loop " << endl;
                }
                else
                {

                    jetprobs.clear();

                    for (size_t i = 0; i < jetsEta->size(); ++i)
                    {
                        double eta = jetsEta->at(i);
                        double btag = jetsBTagAlgo->at(i);
                        double pt = jetsPt->at(i);
                        if (fabs(eta) > 2.6) jetprobs.push_back(0.);
                        jetprobs.push_back(jetprob(pt, btag, eta, syst));
                    }

                    turnOnWeightValue = turnOnWeight(jetprobs, 1);
                    turnOnWeightTreeJetTrig1Up = turnOnWeightValue;
                    turnOnWeightTreeJetTrig1Down = turnOnWeightValue;
                    turnOnWeightTreeJetTrig2Up = turnOnWeightValue;
                    turnOnWeightTreeJetTrig2Down = turnOnWeightValue;
                    turnOnWeightTreeJetTrig3Up = turnOnWeightValue;
                    turnOnWeightTreeJetTrig3Down = turnOnWeightValue;

                    turnOnWeightTreeBTagTrig1Up = turnOnWeightValue;
                    turnOnWeightTreeBTagTrig1Down = turnOnWeightValue;
                    turnOnWeightTreeBTagTrig2Up = turnOnWeightValue;
                    turnOnWeightTreeBTagTrig2Down = turnOnWeightValue;
                    turnOnWeightTreeBTagTrig3Up = turnOnWeightValue;
                    turnOnWeightTreeBTagTrig3Down = turnOnWeightValue;
                }

                //  //cout << "jetprobs @syst: " << syst << " test 3" <<endl;
                ////cout << " njets "<< nJets << " high b-tag " <<highBTagTree<< " high b-tag tree position" << highBTagTreePosition<<endl;

                turnOnReWeightTree =  turnOnReWeightTreeNoSyst;

                ////cout << "jet "<< jets[highBTagTreePosition].pt()<< " weight value "<< turnOnWeightValue <<endl;
                //cout << "test after loop "<<endl;

            }
            if (leptonsFlavour_ == "none" && doTurnOn_)
            {
                jetprobs.clear();
                for (size_t i = 0; i < jetsEta->size(); ++i)
                {
                    double eta = jetsEta->at(i);
                    double btag = jetsBTagAlgo->at(i);
                    double pt = jetsPt->at(i);
                    if (fabs(eta) > 2.6) jetprobs.push_back(0.);
                    jetprobs.push_back(jetprobbtag(btag));
                }
                turnOnWeightValue = turnOnWeight(jetprobs, 1);
            }

            ////cout << " before pdf "<<endl;

            if (syst == "noSyst" && doPDF_ )
            {

                if (channel != "Data")
                {
                    iEvent.getByLabel(x1_, x1h);
                    iEvent.getByLabel(x2_, x2h);

                    iEvent.getByLabel(scalePDF_, scalePDFh);
                    iEvent.getByLabel(id1_, id1h);
                    iEvent.getByLabel(id2_, id2h);

                    x1 = *x1h;
                    x2 = *x2h;

                    scalePDF = *scalePDFh;

                    id1 = *id1h;
                    id2 = *id2h;

                    //Q2 = x1 * x2 * 7000*7000;
                    LHAPDF::usePDFMember(1, 0);
                    double xpdf1 = LHAPDF::xfx(1, x1, scalePDF, id1);
                    double xpdf2 = LHAPDF::xfx(1, x2, scalePDF, id2);
                    double w0 = xpdf1 * xpdf2;
                    for (int p = 1; p <= 52; ++p)
                    {
                        LHAPDF::usePDFMember(1, p);
                        double xpdf1_new = LHAPDF::xfx(1, x1, scalePDF, id1);
                        double xpdf2_new = LHAPDF::xfx(1, x2, scalePDF, id2);
                        double pweight = xpdf1_new * xpdf2_new / w0;
                        pdf_weights[p - 1] = pweight;
                    }
                    LHAPDF::usePDFMember(2, 0);
                    double xpdf1_new = LHAPDF::xfx(2, x1, scalePDF, id1);
                    double xpdf2_new = LHAPDF::xfx(2, x2, scalePDF, id2);
                    pdf_weights_alternate_set_1 = xpdf1_new * xpdf2_new / w0;
                    xpdf1_new = LHAPDF::xfx(3, x1, scalePDF, id1);
                    xpdf2_new = LHAPDF::xfx(3, x2, scalePDF, id2);
                    pdf_weights_alternate_set_2 = xpdf1_new * xpdf2_new / w0;
                    //    pdf_weights_alternate_set_1 =pweight1;
                    //    pdf_weights_alternate_set_2 =pweight2;

                }
            }
            turnOnWeightTree = turnOnWeightValue;

            ////cout << " before mtw "<<endl;

            if ( syst == "noSyst" && nJets == 2)
            {
                //  ++passingJets;

                if (leptonsFlavour_ == "muon" && MTWValue > 40 && B < 3 )
                {
                    ++passingMET;
                    passesMet = true;
                }
                if (leptonsFlavour_ == "electron" && metPt > 35 && B < 3)
                {
                    ++passingMET;
                    passesMet = true;
                }


                if ( B == 1 && passesMet)
                    ++passingBJets;
            }

            math::PtEtaPhiELorentzVector top = top4Momentum(leptonPFour, jets[highBTagTreePosition], metPx, metPy);
            float fCosThetaLJ =  cosThetaLJ(leptonPFour, jets[lowBTagTreePosition], top);
            cosBLTree =  cosTheta_eta_bl(leptonPFour, jets[lowBTagTreePosition], top);


            etaTree = fabs(jets[lowBTagTreePosition].eta());
            cosTree = fCosThetaLJ;
            topMassTree = top.mass();

            topMtwTree = topMtw(leptonPFour, jets[highBTagTreePosition], metPx, metPy);


            lepPt = leptonPFour.pt();
            lepEta = leptonPFour.eta();
            lepPhi = leptonPFour.phi();

	    if (leptonsFlavour_ == "muon" )lepEff = muonHLTEff(lepEta,"Mu2012A");
	    if (leptonsFlavour_ == "muon" )lepEffB = muonHLTEff(lepEta,"Mu2012B");

	    if (leptonsFlavour_ == "electron" )lepEff = 1;



            bJetPt = jets[highBTagTreePosition].pt();
            bJetE = jets[highBTagTreePosition].energy();
            bJetEta = jets[highBTagTreePosition].eta();
            bJetPhi = jets[highBTagTreePosition].phi();

            fJetPt = jets[lowBTagTreePosition].pt();
            fJetE = jets[lowBTagTreePosition].energy();
            fJetEta = jets[lowBTagTreePosition].eta();
            fJetPhi = jets[lowBTagTreePosition].phi();

            totalWeightTree = bWeightTree * turnOnWeightValue * PUWeight * Weight;

            etaTree = fabs(jets[lowBTagTreePosition].eta());
            etaTree2 = fabs(jets[highBTagTreePosition].eta());
            cosTree = fCosThetaLJ;

            topEta = top.eta();
            topPhi = top.phi();
            topPt = top.pt();


            if (nJets == 2)
            {
	      //cout << " B is "<< B<< " syst is "<<syst_name <<endl;
                //  //cout<< " tree name "<< trees2J[B][syst_name]->GetName() <<endl;
                trees2J[B][syst_name]->Fill();
            }
            if (nJets == 3)
            {
	      //cout << " B is "<< B<< " syst is "<<syst_name <<endl;
                //  cout << " tree name "<< trees3J[B][syst_name]->GetName() <<endl;
                trees3J[B][syst_name]->Fill();
            }
        }
        //W Sample



    }
}

//CosThetalj given top quark, lepton and light jet
float SingleTopSystematicsTreesDumper::cosThetaLJ(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top)
{

    math::PtEtaPhiELorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton, top.BoostToCM());
    math::PtEtaPhiELorentzVector boostedJet = ROOT::Math::VectorUtil::boost(jet, top.BoostToCM());

    return  ROOT::Math::VectorUtil::CosTheta(boostedJet.Vect(), boostedLepton.Vect());

}

//CosTheta-lepton-beam-line, implementation by Joosep Pata
float SingleTopSystematicsTreesDumper::cosTheta_eta_bl(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top)
{

    double eta = jet.eta();
    double z;
    if (eta > 0)
    {
        z = 1.0;
    }
    else
    {
        z = -1.0;
    }
    math::XYZTLorentzVector beamLine = math::XYZTLorentzVector(0.0, 0.0, z, 1.0);
    math::PtEtaPhiELorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton, top.BoostToCM());
    math::XYZTLorentzVector boostedBeamLine = ROOT::Math::VectorUtil::boost(beamLine, top.BoostToCM());

    return ROOT::Math::VectorUtil::CosTheta(boostedBeamLine.Vect(), boostedLepton.Vect());

}


double SingleTopSystematicsTreesDumper::topMtw(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy)
{
    math::PtEtaPhiELorentzVector lb = lepton + jet;
    double mlb2 = lb.mass() * lb.mass();
    double etlb = sqrt(mlb2 + lb.pt() * lb.pt());
    double metPT = sqrt(metPx * metPx + metPy * metPy);

    return sqrt( mlb2 + 2 * ( etlb * metPT - lb.px() * metPx - lb.py() * metPy ) );
}

//top quark 4-momentum given lepton, met and b-jet
math::PtEtaPhiELorentzVector SingleTopSystematicsTreesDumper::top4Momentum(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy)
{
    return top4Momentum(lepton.px(), lepton.py(), lepton.pz(), lepton.energy(), jet.px(), jet.py(), jet.pz(), jet.energy(), metPx, metPy);
}

//top quark 4-momentum original function given the necessary parameters
math::PtEtaPhiELorentzVector SingleTopSystematicsTreesDumper::top4Momentum(float leptonPx, float leptonPy, float leptonPz, float leptonE, float jetPx, float jetPy, float jetPz, float jetE, float metPx, float metPy)
{
    float lepton_Pt = sqrt( (leptonPx * leptonPx) +  (leptonPy * leptonPy) );

    math::XYZTLorentzVector neutrino = NuMomentum(leptonPx, leptonPy, leptonPz, lepton_Pt, leptonE, metPx, metPy); //.at(0);;

    math::XYZTLorentzVector lep(leptonPx, leptonPy, leptonPz, leptonE);
    math::XYZTLorentzVector jet(jetPx, jetPy, jetPz, jetE);

    math::XYZTLorentzVector top = lep + jet + neutrino;
    return math::PtEtaPhiELorentzVector(top.pt(), top.eta(), top.phi(), top.E());
}

//top neutrino 4-momentum function given the parameters
//In brief:
//Works for top->1l+1neutrino+1bjet
//Assuming all met comes from neutrino
/////What it does:
//w boson mass put to pdg value
//obtained neutrino pz from kinematics
//We get a second order equation
/////In case of two positive Delta solutions:
//we choose solution with minimum |pz|
/////In case of two negative Delta solutions:
//in such case: mtw > mw
//To solve this: put mtw = mw
//Solve the equations
//In this way we must
//drop the constraints px_Nu = MET_x and py_Nu = MET_y
//Solve this by chosing the px_Nu and py_Nu that
//minimize the distance from the MET in the px-py plane
//Such minimization can be done analytically with derivatives
//and much patience. Here we exploit such analytical minimization
/////
//More detailed inline description: work in progress!
math::XYZTLorentzVector SingleTopSystematicsTreesDumper::NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy )
{

    double  mW = 80.399;

    math::XYZTLorentzVector result;

    //  double Wmt = sqrt(pow(Lepton.et()+MET.pt(),2) - pow(Lepton.px()+metPx,2) - pow(leptonPy+metPy,2) );

    double MisET2 = (metPx * metPx + metPy * metPy);
    double mu = (mW * mW) / 2 + metPx * leptonPx + metPy * leptonPy;
    double a  = (mu * leptonPz) / (leptonE * leptonE - leptonPz * leptonPz);
    double a2 = TMath::Power(a, 2);
    double b  = (TMath::Power(leptonE, 2.) * (MisET2) - TMath::Power(mu, 2.)) / (TMath::Power(leptonE, 2) - TMath::Power(leptonPz, 2));
    double pz1(0), pz2(0), pznu(0);
    int nNuSol(0);

    math::XYZTLorentzVector p4nu_rec;
    math::XYZTLorentzVector p4W_rec;
    math::XYZTLorentzVector p4b_rec;
    math::XYZTLorentzVector p4Top_rec;
    math::XYZTLorentzVector p4lep_rec;

    p4lep_rec.SetPxPyPzE(leptonPx, leptonPy, leptonPz, leptonE);

    math::XYZTLorentzVector p40_rec(0, 0, 0, 0);

    if (a2 - b > 0 )
    {
        //if(!usePositiveDeltaSolutions_)
        //  {
        //  result.push_back(p40_rec);
        //  return result;
        //  }
        double root = sqrt(a2 - b);
        pz1 = a + root;
        pz2 = a - root;
        nNuSol = 2;

        //    if(usePzPlusSolutions_)pznu = pz1;
        //    if(usePzMinusSolutions_)pznu = pz2;
        //if(usePzAbsValMinimumSolutions_){
        pznu = pz1;
        if (fabs(pz1) > fabs(pz2)) pznu = pz2;
        //}


        double Enu = sqrt(MisET2 + pznu * pznu);

        p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu);

        //    result =.push_back(p4nu_rec);
        result = p4nu_rec;

    }
    else
    {

        // if(!useNegativeDeltaSolutions_){
        //result.push_back(p40_rec);
        //  return result;
        //    }
        //    double xprime = sqrt(mW;


        double ptlep = leptonPt, pxlep = leptonPx, pylep = leptonPy, metpx = metPx, metpy = metPy;

        double EquationA = 1;
        double EquationB = -3 * pylep * mW / (ptlep);
        double EquationC = mW * mW * (2 * pylep * pylep) / (ptlep * ptlep) + mW * mW - 4 * pxlep * pxlep * pxlep * metpx / (ptlep * ptlep) - 4 * pxlep * pxlep * pylep * metpy / (ptlep * ptlep);
        double EquationD = 4 * pxlep * pxlep * mW * metpy / (ptlep) - pylep * mW * mW * mW / ptlep;

        std::vector<long double> solutions = EquationSolve<long double>((long double)EquationA, (long double)EquationB, (long double)EquationC, (long double)EquationD);

        std::vector<long double> solutions2 = EquationSolve<long double>((long double)EquationA, -(long double)EquationB, (long double)EquationC, -(long double)EquationD);


        double deltaMin = 14000 * 14000;
        double zeroValue = -mW * mW / (4 * pxlep);
        double minPx = 0;
        double minPy = 0;

        //    std::cout<<"a "<<EquationA << " b " << EquationB  <<" c "<< EquationC <<" d "<< EquationD << std::endl;

        //  if(usePxMinusSolutions_){
        for ( int i = 0; i < (int)solutions.size(); ++i)
        {
            if (solutions[i] < 0 ) continue;
            double p_x = (solutions[i] * solutions[i] - mW * mW) / (4 * pxlep);
            double p_y = ( mW * mW * pylep + 2 * pxlep * pylep * p_x - mW * ptlep * solutions[i]) / (2 * pxlep * pxlep);
            double Delta2 = (p_x - metpx) * (p_x - metpx) + (p_y - metpy) * (p_y - metpy);

            //      std:://cout<<"intermediate solution1 met x "<<metpx << " min px " << p_x  <<" met y "<<metpy <<" min py "<< p_y << std::endl;

            if (Delta2 < deltaMin && Delta2 > 0)
            {
                deltaMin = Delta2;
                minPx = p_x;
                minPy = p_y;
            }
            //     std:://cout<<"solution1 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl;
        }

        //    }

        //if(usePxPlusSolutions_){
        for ( int i = 0; i < (int)solutions2.size(); ++i)
        {
            if (solutions2[i] < 0 ) continue;
            double p_x = (solutions2[i] * solutions2[i] - mW * mW) / (4 * pxlep);
            double p_y = ( mW * mW * pylep + 2 * pxlep * pylep * p_x + mW * ptlep * solutions2[i]) / (2 * pxlep * pxlep);
            double Delta2 = (p_x - metpx) * (p_x - metpx) + (p_y - metpy) * (p_y - metpy);
            //  std:://cout<<"intermediate solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl;
            if (Delta2 < deltaMin && Delta2 > 0)
            {
                deltaMin = Delta2;
                minPx = p_x;
                minPy = p_y;
            }
            //  std:://cout<<"solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl;
        }
        //}

        double pyZeroValue = ( mW * mW * pxlep + 2 * pxlep * pylep * zeroValue);
        double delta2ZeroValue = (zeroValue - metpx) * (zeroValue - metpx) + (pyZeroValue - metpy) * (pyZeroValue - metpy);

        if (deltaMin == 14000 * 14000)return result;
        //    else std:://cout << " test " << std::endl;

        if (delta2ZeroValue < deltaMin)
        {
            deltaMin = delta2ZeroValue;
            minPx = zeroValue;
            minPy = pyZeroValue;
        }

        //    std:://cout<<" MtW2 from min py and min px "<< sqrt((minPy*minPy+minPx*minPx))*ptlep*2 -2*(pxlep*minPx + pylep*minPy)  <<std::endl;
        ///    ////Y part

        double mu_Minimum = (mW * mW) / 2 + minPx * pxlep + minPy * pylep;
        double a_Minimum  = (mu_Minimum * leptonPz) / (leptonE * leptonE - leptonPz * leptonPz);
        pznu = a_Minimum;

        //if(!useMetForNegativeSolutions_){
        double Enu = sqrt(minPx * minPx + minPy * minPy + pznu * pznu);
        p4nu_rec.SetPxPyPzE(minPx, minPy, pznu , Enu);

        //    }
        //    else{
        //      pznu = a;
        //      double Enu = sqrt(metpx*metpx+metpy*metpy + pznu*pznu);
        //      p4nu_rec.SetPxPyPzE(metpx, metpy, pznu , Enu);
        //    }

        //      result.push_back(p4nu_rec);
        result = p4nu_rec;
    }
    return result;
}

//JES uncertainty as a function of pt, eta and jet flavour
double SingleTopSystematicsTreesDumper::jetUncertainty(double eta, double ptCorr, int flavour)
{
    jecUnc->setJetEta(eta);
    jecUnc->setJetPt(ptCorr);
    double JetCorrection = jecUnc->getUncertainty(true); // In principle, boolean controls if uncertainty on +ve or -ve side is returned (asymmetric errors) but not yet implemented.
    bool cut = ptCorr > 50 && ptCorr < 200 && fabs(eta) < 2.0;
    // JES_SW = 0.015;
    //  double JES_PU=0.75*0.8*2.2/ptCorr;
    double JES_PU = 0.; //We are using pfNoPU must understand what value to put there
    double JES_b = 0;
    if (abs(flavour) == 5)
    {
        if (cut) JES_b = JES_b_cut;
        else JES_b = JES_b_overCut;
    }
    //    float JESUncertaintyTmp = sqrt(JESUncertainty*JESUncertainty + JetCorrection*JetCorrection);
    return sqrt(JES_b * JES_b + JES_PU * JES_PU + JES_SW * JES_SW + JetCorrection * JetCorrection);
    return JetCorrection;
}

float SingleTopSystematicsTreesDumper::muonHLTEff(float eta, string period)
{
    float eff = 0.87;

    /*    if(period == "Mu2012A"){
    if (eta < -1.1 && eta > -2.1) eff = 0.81;
    if (eta > -1.1 && eta < -0.9) eff = 0.835;
    if (eta > -0.9 && eta < -0.0) eff = 0.919;
    if (eta > 0.0 && eta < 0.9) eff = 0.921;
    if (eta > 0.9 && eta < 1.1) eff = 0.83;
    if (eta > 1.1 && eta < 2.1) eff = 0.815;
    }


    if(period == "Mu2012B"){
    if (eta < -1.1 && eta > -2.1) eff = 0.81;
    if (eta > -1.1 && eta < -0.9) eff = 0.841;
    if (eta > -0.9 && eta < -0.0) eff = 0.938;
    if (eta > 0.0 && eta < 0.9) eff = 0.940;
    if (eta > 0.9 && eta < 1.1) eff = 0.84;
    if (eta > 1.1 && eta < 2.1) eff = 0.821;
    }OLD
    */


    if(period == "Mu2012A"){
      if (eta < -1.2 && eta > -2.1) eff = 0.8083;
      if (eta > -1.2 && eta < -0.9) eff = 0.8339;
      if (eta > -0.9 && eta < -0.0) eff = 0.9151;
      if (eta > 0.0 && eta < 0.9) eff = 0.9151;
      if (eta > 0.9 && eta < 1.2) eff = 0.8339;
      if (eta > 1.2 && eta < 2.1) eff = 0.8083;
    }
    
    
    if(period == "Mu2012B"){
      if (eta < -1.2 && eta > -2.1) eff = 0.8047;
      if (eta > -1.2 && eta < -0.9) eff = 0.8394;
      if (eta > -0.9 && eta < -0.0) eff = 0.9326;
      if (eta > 0.0 && eta < 0.9) eff = 0.9326;
      if (eta > 0.9 && eta < 1.2) eff = 0.8394;
      if (eta > 1.2 && eta < 2.1) eff = 0.8047;
    }
    
    return eff;
}

//EndJob filling rate systematics trees
void SingleTopSystematicsTreesDumper::endJob()
{

    //part for rate systematics

    cout << endl << passingLepton << " | " << passingMuonVeto << " | " << passingLeptonVeto << " | "  << passingJets << " | " << passingMET << " | " << passingBJets << endl << endl;

    //  resetWeightsDoubles();
    /*  for(size_t i = 0; i < rate_systematics.size();++i){
      string syst = rate_systematics[i];
      string treename = (channel+"_"+syst);

      cout<< " endjob"  << syst<< " 0 "<<endl;
      int bj =0;
      trees2J[bj][syst]->CopyAddresses(trees2J[bj]["noSyst"]);


          cout<< " endjob"  << syst<< " 1 "<<endl;


      //modify the weight by a constant factor
      double tmpWeight = 0;
      double weightSF = 1.;

      TBranch * b = trees2J[bj]["noSyst"]->GetBranch("weight");
      int entries = b->GetEntries();
      b->SetAddress(&tmpWeight);


      cout<< " endjob"  << syst<< " 2 "<<endl;

      trees2J[bj][syst]->GetBranch("weight")->Reset();
      trees2J[bj][syst]->GetBranch("weight")->SetAddress(&tmpWeight);


      cout<< " endjob"  << syst<< " 3 "<<endl;

      for(int t =0; t < entries ; ++t){
        b->GetEntry(t);
        tmpWeight*=weightSF;
        trees2J[bj][syst]->GetBranch("weight")->Fill();

      }



      b->SetAddress(&weightTree);
      trees2J[bj][syst]->GetBranch("weight")->SetAddress(&weightTree);



      //    cout<< " syst "<< syst<< " weights entries "<<  entries <<endl;

    }*/
}

//B-C weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper::BTagSFNew(double pt, string algo)
{
    if (algo == "CSVM")return 0.6981 * ((1. + (0.414063 * pt)) / (1. + (0.300155 * pt)));
    if (algo == "CSVT")return 0.901615 * ((1. + (0.552628 * pt)) / (1. + (0.547195 * pt)));
    if (algo == "TCHPT")return 0.895596 * ((1. + (9.43219e-05 * pt)) / (1. + (-4.63927e-05 * pt)));
    if (algo == "CSVL") return 1.02658 * ((1. + (0.0195388 * pt)) / (1. + (0.0209145 * pt)));


    return 1;
}


double SingleTopSystematicsTreesDumper::BTagSFErrNew(double pt, string algo)
{
    if (algo == "TCHPT")
    {
        if (pt > 30 && pt < 40)return 0.0543376;
        if (pt > 40 && pt < 50)return 0.0534339;
        if (pt > 50 && pt < 60)return 0.0266156;
        if (pt > 60 && pt < 70)return 0.0271337;
        if (pt > 70 && pt < 80)return 0.0276364;
        if (pt > 80 && pt < 100)return 0.0308838;
        if (pt > 100 && pt < 120)return 0.0381656;
        if (pt > 120 && pt < 160)return 0.0336979;
        if (pt > 160 && pt < 210)return 0.0336773;
        if (pt > 210 && pt < 260)return 0.0347688;
        if (pt > 260 && pt < 320)return 0.0376865;
        if (pt > 320 && pt < 400)return 0.0556052;
        if (pt > 400 && pt < 500)return 0.0598105;
        if (pt > 500 && pt < 670)return 0.0861122;
    }
    if (algo == "TCHEL")
    {
        if (pt > 30 && pt < 40)return 0.0244956;
        if (pt > 40 && pt < 50)return 0.0237293;
        if (pt > 50 && pt < 60)return 0.0180131;
        if (pt > 60 && pt < 70)return 0.0182411;
        if (pt > 70 && pt < 80)return 0.0184592;
        if (pt > 80 && pt < 100)return 0.0106444;
        if (pt > 100 && pt < 120)return 0.0110736;
        if (pt > 120 && pt < 160)return 0.0106296;
        if (pt > 160 && pt < 210)return 0.0175259;
        if (pt > 210 && pt < 260)return 0.0161566;
        if (pt > 260 && pt < 320)return 0.0158973;
        if (pt > 320 && pt < 400)return 0.0186782;
        if (pt > 400 && pt < 500)return 0.0371113;
        if (pt > 500 && pt < 670)return 0.0289788;
    }
    if (algo == "CSVM")
    {
        if (pt > 30 && pt < 40)return 0.0295675;
        if (pt > 40 && pt < 50)return 0.0295095;
        if (pt > 50 && pt < 60)return 0.0210867;
        if (pt > 60 && pt < 70)return 0.0219349;
        if (pt > 70 && pt < 80)return 0.0227033;
        if (pt > 80 && pt < 100)return 0.0204062;
        if (pt > 100 && pt < 120)return 0.0185857;
        if (pt > 120 && pt < 160)return 0.0256242;
        if (pt > 160 && pt < 210)return 0.0383341;
        if (pt > 210 && pt < 260)return 0.0409675;
        if (pt > 260 && pt < 320)return 0.0420284;
        if (pt > 320 && pt < 400)return 0.0541299;
        if (pt > 400 && pt < 500)return 0.0578761;
        if (pt > 500 && pt < 670)return 0.0655432;
    }

    if (algo == "CSVT")
    {
        if (pt > 30 && pt < 40)return 0.0364717;
        if (pt > 40 && pt < 50)return 0.0362281;
        if (pt > 50 && pt < 60)return 0.0232876;
        if (pt > 60 && pt < 70)return 0.0249618;
        if (pt > 70 && pt < 80)return 0.0261482;
        if (pt > 80 && pt < 100)return 0.0290466;
        if (pt > 100 && pt < 120)return 0.0300033;
        if (pt > 120 && pt < 160)return 0.0453252;
        if (pt > 160 && pt < 210)return 0.0685143;
        if (pt > 210 && pt < 260)return 0.0653621;
        if (pt > 260 && pt < 320)return 0.0712586;
        if (pt > 320 && pt < 400)return 0.0945892;
        if (pt > 400 && pt < 500)return 0.0777011;
        if (pt > 500 && pt < 670)return 0.0866563;
    }
















    if (algo == "CSVL")
    {
        if (pt > 30 && pt < 40)return     0.0188743;
        if (pt > 40 && pt < 50)return     0.0161816;
        if (pt > 50 && pt < 60)return     0.0139824;
        if (pt > 60 && pt < 70)return     0.0152644;
        if (pt > 70 && pt < 80)return     0.0161226;
        if (pt > 80 && pt < 100)return     0.0157396;
        if (pt > 100 && pt < 120)return     0.0161619;
        if (pt > 120 && pt < 160)return     0.0168747;
        if (pt > 160 && pt < 210)return     0.0257175;
        if (pt > 210 && pt < 260)return     0.026424;
        if (pt > 260 && pt < 320)return     0.0264928;
        if (pt > 320 && pt < 400)return     0.0315127;
        if (pt > 400 && pt < 500)return     0.030734;
        if (pt > 500 && pt < 670)return     0.0438259 ;
    }


    return 0;

}

double SingleTopSystematicsTreesDumper::MisTagSFNew(double pt, double eta, string algo)
{
    if (algo == "TCHPT")return ((1.20711 + (0.000681067 * pt)) + (-1.57062e-06 * (pt * pt))) + (2.83138e-10 * (pt * (pt * pt))) * (1.08376 + -0.000666189 * pt + 1.01272e-06 * pt * pt);
    if (algo == "CSVM")return ((1.20711 + (0.000681067 * pt)) + (-1.57062e-06 * (pt * pt))) + (2.83138e-10 * (pt * (pt * pt))) * (1.10422 + -0.000523856 * pt + 1.14251e-06 * pt * pt);
    if (algo == "CSVT") return (1.10649 * ((1 + (-9.00297e-05 * pt)) + (2.32185e-07 * (pt * pt)))) + (-4.04925e-10 * (pt * (pt * (pt / (1 + (-0.00051036 * pt)))))) * (1.19275 + -0.00191042 * pt + 2.92205e-06 * pt * pt);

    if (algo == "CSVL")return ((1.0344 + (0.000962994 * pt)) + (-3.65392e-06 * (pt * pt))) + (3.23525e-09 * (pt * (pt * pt))) * (0.979396 + 0.000205898 * pt + 2.49868e-07 * pt * pt);

    return 0;
}

double SingleTopSystematicsTreesDumper::MisTagSFErrNewUp(double pt, double eta, string algo)
{
    double x = pt;

    if (algo == "TCHPT")return ((1.38002 + (0.000933875 * pt)) + (-2.59821e-06 * (pt * pt))) + (1.18434e-09 * (pt * (pt * pt)));
    if (algo == "TCHEL")return (1.19751 * ((1 + (-0.000114197 * pt)) + (3.08558e-07 * (pt * pt)))) + (-5.27598e-10 * (pt * (pt * (pt / (1 + (-0.000422372 * pt)))))) ;

    if (algo == "CSVT") return ((0.997077 + (0.00473953 * x)) + (-1.34985e-05 * (x * x))) + (1.0032e-08 * (x * (x * x)));
    if (algo == "CSVL")return ((1.11272 + (0.00110104 * x)) + (-4.11956e-06 * (x * x))) + (3.65263e-09 * (x * (x * x)));

    return 0;
}

double SingleTopSystematicsTreesDumper::MisTagSFErrNewDown(double pt, double eta, string algo)
{
    double x = pt;
    if (algo == "TCHPT")return ((1.03418 + (0.000428273 * pt)) + (-5.43024e-07 * (pt * pt))) + (-6.18061e-10 * (pt * (pt * pt)));
    if (algo == "TCHEL")return (1.01541 * ((1 + (-6.04627e-05 * pt)) + (1.38195e-07 * (pt * pt)))) + (-2.83043e-10 * (pt * (pt * (pt / (1 + (-0.000633609 * pt))))));

    if (algo == "CSVT") return ((0.899715 + (0.00102278 * x)) + (-2.46335e-06 * (x * x))) + (9.71143e-10 * (x * (x * x)));
    if (algo == "CSVL")return ((0.956023 + (0.000825106 * x)) + (-3.18828e-06 * (x * x))) + (2.81787e-09 * (x * (x * x)));

    return 0;
}


double SingleTopSystematicsTreesDumper::EFFMapNew(double btag, string algo)
{
    if (algo == "TCHP_B")return 1.26119661124e-05 * btag * btag * btag * btag +  -0.000683198597977 * btag * btag * btag +  0.0145106168149 * btag * btag +  -0.159575511553 * btag +  0.887707865272;
    if (algo == "TCHP_C")
    {
        if (btag < 0.54) return 0.451288118581 * exp(-0.0213290505241 * btag * btag * btag + 0.356020789904 * btag * btag + -2.20158883207 * btag + 1.84838018633 );
        else return 0.99;
    }
    if (algo == "TCHP_L")return (-0.00101 + (4.70405e-05 * btag)) + (8.3338e-09 * (btag * btag));

    if (algo == "TCHE_B")return 3.90732786802e-06 * btag * btag * btag * btag +  -0.000239934437355 * btag * btag * btag +  0.00664986827287 * btag * btag +  -0.112578996016 * btag +  1.00775721404;
    if (algo == "TCHE_C")
    {
        if (btag > 0.46 ) return 0.343760640168 * exp(-0.00315525164823 * btag * btag * btag + 0.0805427315196 * btag * btag + -0.867625139194 * btag + 1.44815935164 );
        else return 0.99;//EFFMap("TCHEL_C");
    }

    if (algo == "TCHE_L")return(((-0.0276197 + (0.00291907 * btag)) + (-7.51594e-06 * (btag * btag))) + (9.82128e-09 * (btag * (btag * btag)))) + (-5.33759e-12 * (btag * (btag * (btag * btag))));
    return 1;
}

double SingleTopSystematicsTreesDumper::BScaleFactor(string algo, string syst_name)
{

    double bcentral = 0.9;
    double berr = 0.15 * bcentral;
    double cerr = 0.3 * bcentral;
    double tcheeff = 0.7;

    if (syst_name == "BTagUp")
    {
        if (algo == "TCHP_B")
        {
            return bcentral + berr;
        }
        if (algo == "TCHP_C")
        {
            return bcentral + cerr;
        }

        if (algo == "TCHE_B")
        {
            return bcentral + berr;
        }

        if (algo == "TCHE_C")
        {
            return bcentral + cerr;
        }

    }

    if (syst_name == "BTagDown")
    {
        if (algo == "TCHP_B")
        {
            return bcentral - berr;
        }
        if (algo == "TCHP_C")
        {
            return bcentral - cerr;
        }

        if (algo == "TCHE_B")
        {
            return bcentral - berr;
        }
        if (algo == "TCHE_C")
        {
            return bcentral - berr;
        }
    }

    if (algo == "TCHP_B")
    {
        return bcentral;
    }
    if (algo == "TCHP_C")
    {
        return bcentral;
    }
    if (algo == "TCHE_B")
    {
        return bcentral;
    }
    if (algo == "TCHE_C")
    {
        return bcentral;
    }

    return 0.9;
}

//Mistag weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper::MisTagScaleFactor(string algo, string syst_name, double sf, double eff, double sferr)
{
    double mistagcentral = sf;
    double mistagerr = sferr;
    double tcheeff = eff;


    if (syst_name == "MisTagUp")
    {
        if (algo == "TCHP_L")
        {
            return mistagcentral + mistagerr;
        }
        if (algo == "TCHE_L")
        {
            return mistagcentral + mistagerr;
        }

    }

    if (syst_name == "MisTagDown")
    {
        if (algo == "TCHP_L")
        {
            return mistagcentral - mistagerr;
        }
        if (algo == "TCHE_L")
        {
            return mistagcentral - mistagerr;
        }
    }

    if (algo == "TCHP_L")
    {
        return mistagcentral;
    }
    if (algo == "TCHE_L")
    {
        return mistagcentral;
    }

    return 0.9;


}



//B-C veto weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper::AntiBScaleFactor(string algo, string syst_name)
{

    double bcentral = 0.9;
    double berr = 0.15 * bcentral;
    double cerr = 0.3 * bcentral;
    double tcheeff = 0.7;
    double tchpeff = 0.26;

    if (syst_name == "BTagUp")
    {
        if (algo == "TCHP_B")
        {
            return (1 - tchpeff * (bcentral + berr)) / (1 - tchpeff);
        }
        if (algo == "TCHP_C")
        {
            return (1 - tchpeff * (bcentral + cerr)) / (1 - tchpeff);
        }

        if (algo == "TCHE_B")
        {
            return (1 - tcheeff * (bcentral + berr)) / (1 - tcheeff);
        }

        if (algo == "TCHE_C")
        {
            return (1 - tcheeff * (bcentral + cerr)) / (1 - tcheeff);
        }
    }

    if (syst_name == "BTagDown")
    {
        if (algo == "TCHP_B")
        {
            return (1 - tchpeff * (bcentral - berr)) / (1 - tchpeff);
        }
        if (algo == "TCHP_C")
        {
            return (1 - tchpeff * (bcentral - cerr)) / (1 - tchpeff);
        }

        if (algo == "TCHE_B")
        {
            return (1 - tcheeff * (bcentral - berr)) / (1 - tcheeff);
        }
        if (algo == "TCHE_C")
        {
            return (1 - tcheeff * (bcentral - cerr)) / (1 - tcheeff);
        }
    }

    if (algo == "TCHP_B")
    {
        return (1 - tchpeff * (bcentral)) / (1 - tchpeff);
    }
    if (algo == "TCHP_C")
    {
        return (1 - tchpeff * (bcentral)) / (1 - tchpeff);
    }
    if (algo == "TCHE_B")
    {
        return (1 - tcheeff * (bcentral)) / (1 - tcheeff);
    }
    if (algo == "TCHE_C")
    {
        return (1 - tcheeff * (bcentral)) / (1 - tcheeff);
    }

    return 0.9;
}

void SingleTopSystematicsTreesDumper::InitializeEventScaleFactorMap()
{

    TCHPT_B = EventScaleFactor("TCHPT_B", "noSyst");
    TCHPT_C = EventScaleFactor("TCHPT_C", "noSyst");
    TCHPT_L = EventScaleFactor("TCHPT_L", "noSyst");


    TCHPT_BBTagUp = EventScaleFactor("TCHPT_B", "BTagUp");
    TCHPT_BBTagDown = EventScaleFactor("TCHPT_B", "BTagDown");
    TCHPT_CBTagUp = EventScaleFactor("TCHPT_C", "BTagUp");
    TCHPT_CBTagDown = EventScaleFactor("TCHPT_C", "BTagDown");
    TCHPT_LMisTagUp = EventScaleFactor("TCHPT_L", "MisTagUp");
    TCHPT_LMisTagDown = EventScaleFactor("TCHPT_L", "MisTagDown");


    TCHPT_BAnti = EventAntiScaleFactor("TCHPT_B", "noSyst");
    TCHPT_CAnti = EventAntiScaleFactor("TCHPT_C", "noSyst");
    TCHPT_LAnti = EventAntiScaleFactor("TCHPT_L", "noSyst");

    TCHPT_BAntiBTagUp = EventAntiScaleFactor("TCHPT_B", "BTagUp");
    TCHPT_BAntiBTagDown = EventAntiScaleFactor("TCHPT_B", "BTagDown");
    TCHPT_CAntiBTagUp = EventAntiScaleFactor("TCHPT_C", "BTagUp");
    TCHPT_CAntiBTagDown = EventAntiScaleFactor("TCHPT_C", "BTagDown");
    TCHPT_LAntiMisTagUp = EventAntiScaleFactor("TCHPT_L", "MisTagUp");
    TCHPT_LAntiMisTagDown = EventAntiScaleFactor("TCHPT_L", "MisTagDown");


    //  TCHP_LAntiMisTagDown = EventAntiScaleFactor("TCHP_L","MisTagDown");

    TCHPM_B = EventScaleFactor("TCHPM_B", "noSyst");
    TCHPM_C = EventScaleFactor("TCHPM_C", "noSyst");
    TCHPM_L = EventScaleFactor("TCHPM_L", "noSyst");


    TCHPM_BBTagUp = EventScaleFactor("TCHPM_B", "BTagUp");
    TCHPM_BBTagDown = EventScaleFactor("TCHPM_B", "BTagDown");
    TCHPM_CBTagUp = EventScaleFactor("TCHPM_C", "BTagUp");
    TCHPM_CBTagDown = EventScaleFactor("TCHPM_C", "BTagDown");
    TCHPM_LMisTagUp = EventScaleFactor("TCHPM_L", "MisTagUp");
    TCHPM_LMisTagDown = EventScaleFactor("TCHPM_L", "MisTagDown");


    TCHPM_BAnti = EventAntiScaleFactor("TCHPM_B", "noSyst");
    TCHPM_CAnti = EventAntiScaleFactor("TCHPM_C", "noSyst");
    TCHPM_LAnti = EventAntiScaleFactor("TCHPM_L", "noSyst");

    TCHPM_BAntiBTagUp = EventAntiScaleFactor("TCHPM_B", "BTagUp");
    TCHPM_BAntiBTagDown = EventAntiScaleFactor("TCHPM_B", "BTagDown");
    TCHPM_CAntiBTagUp = EventAntiScaleFactor("TCHPM_C", "BTagUp");
    TCHPM_CAntiBTagDown = EventAntiScaleFactor("TCHPM_C", "BTagDown");
    TCHPM_LAntiMisTagUp = EventAntiScaleFactor("TCHPM_L", "MisTagUp");
    TCHPM_LAntiMisTagDown = EventAntiScaleFactor("TCHPM_L", "MisTagDown");

    /////

    TCHEL_B = EventScaleFactor("TCHEL_B", "noSyst");
    TCHEL_C = EventScaleFactor("TCHEL_C", "noSyst");
    TCHEL_L = EventScaleFactor("TCHEL_L", "noSyst");

    TCHEL_BBTagUp = EventScaleFactor("TCHEL_B", "BTagUp");
    TCHEL_BBTagDown = EventScaleFactor("TCHEL_B", "BTagDown");
    TCHEL_CBTagUp = EventScaleFactor("TCHEL_C", "BTagUp");
    TCHEL_CBTagDown = EventScaleFactor("TCHEL_C", "BTagDown");
    TCHEL_LMisTagUp = EventScaleFactor("TCHEL_L", "MisTagUp");
    TCHEL_LMisTagDown = EventScaleFactor("TCHEL_L", "MisTagDown");

    TCHEL_BAnti = EventAntiScaleFactor("TCHEL_B", "noSyst");
    TCHEL_CAnti = EventAntiScaleFactor("TCHEL_C", "noSyst");
    TCHEL_LAnti = EventAntiScaleFactor("TCHEL_L", "noSyst");

    TCHEL_BAntiBTagUp = EventAntiScaleFactor("TCHEL_B", "BTagUp");
    TCHEL_BAntiBTagDown = EventAntiScaleFactor("TCHEL_B", "BTagDown");
    TCHEL_CAntiBTagUp = EventAntiScaleFactor("TCHEL_C", "BTagUp");
    TCHEL_CAntiBTagDown = EventAntiScaleFactor("TCHEL_C", "BTagDown");
    TCHEL_LAntiMisTagUp = EventAntiScaleFactor("TCHEL_L", "MisTagUp");
    TCHEL_LAntiMisTagDown = EventAntiScaleFactor("TCHEL_L", "MisTagDown");
}

double SingleTopSystematicsTreesDumper::SFMap(string algo )
{
    if (algo == "TCHPT_B")return 0.89;
    if (algo == "TCHPT_C")return 0.89;
    if (algo == "TCHPT_L")return 1.17;

    if (algo == "TCHPM_B")return 0.91;
    if (algo == "TCHPM_C")return 0.91;
    if (algo == "TCHPM_L")return 0.91;

    if (algo == "TCHEL_B")return 0.95;
    if (algo == "TCHEL_C")return 0.95;
    if (algo == "TCHEL_L")return 1.11;


    return 0.9;
}

double SingleTopSystematicsTreesDumper::SFErrMap(string algo )
{
    if (algo == "TCHPT_B")return 0.092;
    if (algo == "TCHPT_C")return 0.092;
    if (algo == "TCHPT_L")return 0.18;

    if (algo == "TCHPM_B")return 0.10;
    if (algo == "TCHPM_C")return 0.10;
    if (algo == "TCHPM_L")return 0.11;

    if (algo == "TCHEL_B")return 0.10;
    if (algo == "TCHEL_C")return 0.10;
    if (algo == "TCHEL_L")return 0.11;

    return 0.1;
}

double SingleTopSystematicsTreesDumper::EFFMap(string algo )
{
    if (algo == "TCHPT_B")return 0.365 * 1.;
    if (algo == "TCHPT_C")return 0.0365;
    if (algo == "TCHPT_L")return 0.0017;

    if (algo == "CSVT_B")return 0.5;
    if (algo == "CSVT_C")return 0.05;
    if (algo == "CSVT_L")return 0.003;

    if (algo == "CSVM_B")return 0.365;
    if (algo == "CSVM_C")return 0.0365;
    if (algo == "CSVM_L")return 0.0017;

    if (algo == "CSVL_B")return 0.8;
    if (algo == "CSVL_C")return 0.36;
    if (algo == "CSVL_L")return 0.2;

    return 0.36;
}

double SingleTopSystematicsTreesDumper::EFFMap(string algo, string channel )
{

    if (channel == "TChannel" || channel == "TbarChannel" || channel == "SChannel" || channel == "SbarChannel" || channel == "TWChannel" || channel == "TbarWChannel")
    {
        if (algo == "CSVT_B")return 0.54;
        if (algo == "CSVT_C")return 0.037;
        if (algo == "CSVT_L")return 0.002;

        if (algo == "CSVL_B")return 0.84;
        if (algo == "CSVL_C")return 0.33;
        if (algo == "CSVL_L")return 0.2;

    }

    if (channel == "TTBar")
    {
        if (algo == "CSVT_B")return 0.66;
        if (algo == "CSVT_C")return 0.052;
        if (algo == "CSVT_L")return 0.047;

        if (algo == "CSVL_B")return 0.92;
        if (algo == "CSVL_C")return 0.44;
        if (algo == "CSVL_L")return 0.3;



    }

    if (channel == "WJets")
    {
        if (algo == "CSVT_B")return 0.31;
        if (algo == "CSVT_C")return 0.046;
        if (algo == "CSVT_L")return 0.0015;

        if (algo == "CSVL_B")return 0.63;
        if (algo == "CSVL_C")return 0.40;
        if (algo == "CSVL_L")return 0.14;


    }

    if (channel == "ZJets")
    {

        if (algo == "CSVT_B")return 0.41;
        if (algo == "CSVT_C")return 0.047;
        if (algo == "CSVT_L")return 0.002;

        if (algo == "CSVL_B")return 0.76;
        if (algo == "CSVL_C")return 0.41;
        if (algo == "CSVL_L")return 0.2;


    }



    return EFFMap(algo);

}

double SingleTopSystematicsTreesDumper::EFFErrMap(string algo )
{
    if (algo == "TCHPT_B")return 0.05;
    if (algo == "TCHPT_C")return 0.05;
    if (algo == "TCHPT_L")return 0.0004;

    if (algo == "TCHEL_B")return 0.05;
    if (algo == "TCHEL_C")return 0.05;
    if (algo == "TCHEL_L")return 0.03;

    if (algo == "TCHEL_B")return 0.05;
    if (algo == "TCHEL_C")return 0.05;
    if (algo == "TCHEL_L")return 0.004;

    return 0.05;
}
double SingleTopSystematicsTreesDumper::EventScaleFactor(string algo, string syst_name) //,double sf, double eff, double sferr){
{

    //  double mistagcentral = sf;
    //double mistagerr = sferr;
    //double tcheeff = eff;

    double mistagcentral = SFMap(algo);
    double mistagerr = SFErrMap(algo);
    double tcheeff = EFFMap(algo);


    if (syst_name == "MisTagUp" || syst_name == "BTagUp")
    {
        return mistagcentral + mistagerr;
    }

    if (syst_name == "MisTagDown" || syst_name == "BTagDown")
    {
        return mistagcentral - mistagerr;
    }

    return mistagcentral;
}

//EventAntiScaleFactor

double SingleTopSystematicsTreesDumper::EventAntiScaleFactor(string algo, string syst_name )
{
    //,double sf, double eff, double sferr){


    //double mistagcentral = sf;
    //double mistagerr = sferr;
    //double tcheeff = eff;

    double mistagcentral = SFMap(algo);
    double mistagerr = SFErrMap(algo);
    double tcheeff = EFFMap(algo);


    if (syst_name == "MisTagUp" || syst_name == "BTagUp")
    {
        return (1 - tcheeff) / (1 - tcheeff / (mistagcentral + mistagerr));
    }

    if (syst_name == "MisTagDown" || syst_name == "BTagDown")
    {
        return (1 - tcheeff) / (1 - tcheeff / (mistagcentral - mistagerr));

    }

    return (1 - tcheeff) / (1 - tcheeff / (mistagcentral));

}


//MisTag veto weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper::AntiMisTagScaleFactor(string algo, string syst_name, double sf, double eff, double sferr)
{
    double mistagcentral = sf;
    double mistagerr = sferr;
    double tcheeff = eff;
    double tchpeff = eff;

    if (syst_name == "MisTagUp")
    {
        if (algo == "TCHP_L")
        {
            return (1 - tchpeff) / (1 - tchpeff / (mistagcentral + mistagerr));
        }
        if (algo == "TCHE_L")
        {
            return (1 - tcheeff) / (1 - tcheeff / (mistagcentral + mistagerr));
        }

    }

    if (syst_name == "MisTagDown")
    {
        if (algo == "TCHP_L")
        {
            return (1 - tchpeff) / (1 - tchpeff / (mistagcentral - mistagerr));
        }
        if (algo == "TCHE_L")
        {
            return (1 - tcheeff) / (1 - tcheeff / (mistagcentral - mistagerr));
        }
    }

    if (algo == "TCHP_L")
    {
        return (1 - tchpeff) / (1 - tchpeff / (mistagcentral));
    }
    if (algo == "TCHE_L")
    {
        return (1 - tcheeff) / (1 - tcheeff / (mistagcentral));
    }

    return 0.9;


}


double SingleTopSystematicsTreesDumper::turnOnWeight (std::vector<double> probabilities, int njets_req = 1)
{
    double prob = 0;
    for (unsigned int i = 0; i < pow(2, probabilities.size()); ++i)
    {
        //at least njets_req objects for trigger required
        int ntrigobj = 0;
        for (unsigned int j = 0; j < probabilities.size(); ++j)
        {
            if ((int)(i / pow(2, j)) % 2) ntrigobj++;
        }
        if (ntrigobj < njets_req) continue;
        double newprob = 1;
        for (unsigned int j = 0; j < probabilities.size(); ++j)
        {
            if ((int)(i / pow(2, j)) % 2) newprob *= probabilities[j];
            else newprob *= 1 - probabilities[j];
        }
        prob += newprob;
    }
    return prob;
}


int SingleTopSystematicsTreesDumper::eventFlavour(string ch, int nb, int nc, int nl)
{
    if (ch !=  "WJets" && ch != "ZJets") return 0;
    else
    {
        if ( flavourFilter("WJets_wlight", nb, nc, nl) ) return 1;
        if ( flavourFilter("WJets_wcc", nb, nc, nl) ) return 2;
        if ( flavourFilter("WJets_wbb", nb, nc, nl) ) return 3;
    }
    return 0;
}

bool SingleTopSystematicsTreesDumper::flavourFilter(string ch, int nb, int nc, int nl)
{

    if (ch == "WJets_wbb" || ch == "ZJets_wbb") return (nb > 0 );
    if (ch == "WJets_wcc" || ch == "ZJets_wcc") return (nb == 0 && nc > 0);
    if (ch == "WJets_wlight" || ch == "ZJets_wlight") return (nb == 0 && nc == 0);

    return true;
}

/*double SingleTopSystematicsTreesDumper::jetprob(double pt, double btag){
  double prob=0.993*(exp(-51.0*exp(-0.160*pt)));
  prob*=0.902*exp((-5.995*exp(-0.604*btag)));
  return prob;
  }*/

double SingleTopSystematicsTreesDumper::jetprob(double pt, double btag)
{
    double prob = 0.982 * exp(-30.6 * exp(-0.151 * pt)); //PT turnOn
    prob *= 0.844 * exp((-6.72 * exp(-0.720 * btag))); //BTag turnOn
    return prob;
}


double SingleTopSystematicsTreesDumper::jetprobpt(double pt)
{
    double prob = 0.982 * exp(-30.6 * exp(-0.151 * pt)); //PT turnOn
    return prob;
}

double SingleTopSystematicsTreesDumper::jetprobbtag(double btag)
{
    double prob = 0.844 * exp((-6.72 * exp(-0.720 * btag))); //BTag turnOn
    return prob;
}

double SingleTopSystematicsTreesDumper::turnOnProbs(string syst, int n)
{
    if (syst == "JetTrig1Up")
    {
        return turnOnWeight(jetprobs_j1up, 1)
               ;
    }
    else if (syst == "JetTrig2Up")
    {
        return turnOnWeight(jetprobs_j2up, 1)
               ;
    }
    else if (syst == "JetTrig3Up")
    {
        return turnOnWeight(jetprobs_j3up, 1)
               ;
    }

    if (syst == "JetTrig1Down")
    {
        return turnOnWeight(jetprobs_j1down, 1)
               ;
    }
    else if (syst == "JetTrig2Down")
    {
        return turnOnWeight(jetprobs_j2down, 1)
               ;
    }
    else if (syst == "JetTrig3Down")
    {
        return turnOnWeight(jetprobs_j3down, 1)
               ;
    }

    if (syst == "BTagTrig1Up")
    {
        return turnOnWeight(jetprobs_b1up, 1)
               ;
    }
    else if (syst == "BTagTrig2Up")
    {
        return turnOnWeight(jetprobs_b2up, 1)
               ;
    }
    else if (syst == "BTagTrig3Up")
    {
        return turnOnWeight(jetprobs_b3up, 1)
               ;
    }

    if (syst == "BTagTrig1Down")
    {
        return turnOnWeight(jetprobs_b1down, 1)
               ;
    }
    else if (syst == "BTagTrig2Down")
    {
        return turnOnWeight(jetprobs_b2down, 1)
               ;
    }
    else if (syst == "BTagTrig3Down")
    {
        return turnOnWeight(jetprobs_b3down, 1)
               ;
    }

    return turnOnWeight(jetprobs, 1);


}

void SingleTopSystematicsTreesDumper::pushJetProbs(double pt, double btag, double eta)
{

    jetprobs.push_back(jetprob(pt, btag, eta, "noSyst"));

    jetprobs_j1up.push_back(jetprob(pt, btag, eta, "JetTrig1Up"));
    jetprobs_j1down.push_back(jetprob(pt, btag, eta, "JetTrig1Down"));

    jetprobs_j2up.push_back(jetprob(pt, btag, eta, "JetTrig2Up"));
    jetprobs_j2down.push_back(jetprob(pt, btag, eta, "JetTrig2Down"));

    jetprobs_j3up.push_back(jetprob(pt, btag, eta, "JetTrig3Up"));
    jetprobs_j3down.push_back(jetprob(pt, btag, eta, "JetTrig3Down"));


    jetprobs_b1up.push_back(jetprob(pt, btag, eta, "BTagTrig1Up"));
    jetprobs_b1down.push_back(jetprob(pt, btag, eta, "BTagTrig1Down"));

    jetprobs_b2up.push_back(jetprob(pt, btag, eta, "BTagTrig2Up"));
    jetprobs_b2down.push_back(jetprob(pt, btag, eta, "BTagTrig2Down"));

    jetprobs_b3up.push_back(jetprob(pt, btag, eta, "BTagTrig3Up"));
    jetprobs_b3down.push_back(jetprob(pt, btag, eta, "BTagTrig3Down"));




}

void SingleTopSystematicsTreesDumper::InitializeTurnOnReWeight(string rootFile = "CentralJet30BTagIP_2ndSF_mu.root")
{

    TFile f("CentralJet30BTagIP_2ndSF_mu.root");
    TH2D *histSF = dynamic_cast<TH2D *>(f.Get("ScaleFactor"));

    histoSFs = *histSF;
    f.Close();
    //  cout << " histo random test bin " <<histoSFs.FindFixBin(61,6.5)<< " content "<<histoSFs.GetBinContent(histoSFs.FindFixBin(61,6.5)) << endl;
    //  for
    //  recorrection_weights[7][7];

    //  float pt_bin_extremes[8];
    //float tchpt_bin_extremes[8];

    ;
}

double SingleTopSystematicsTreesDumper::turnOnReWeight (double preWeight, double pt, double tchpt)
{
  //    cout << "reweight pt" <<  pt << " tchpt " << tchpt << endl;
  //  cout << " bin " << histoSFs.FindFixBin(pt, tchpt) << " sf ";
  //    cout << histoSFs.GetBinContent(histoSFs.FindFixBin(pt, tchpt)) << endl;
    double a = histoSFs.GetBinContent(histoSFs.FindFixBin(pt, tchpt));
    return a;
    //  return 1;//preWeight;
}


double SingleTopSystematicsTreesDumper::jetprob(double pt, double btag, double eta, string syst)
{
    double prob = 1.;
    if (fabs(eta) > 2.6) return 0.;

    double a = 0, b = 1, c = 1;

    if (syst == "BTagTrig1Up")
    {
        if (btag < -10.)
        {
            a = 0.0142;
            b = -27.7;
            c = -0.128;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0735;
            b = -4.24;
            c = -0.0615;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0196;
            b = -7.71;
            c = -0.0647;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -16.3;
            c = -0.0933;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.071;
            b = -50.;
            c = -0.138;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.255;
            b = -109.4;
            c = -0.172;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.39;
            b = -112.;
            c = -0.168;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.534;
            b = -113.;
            c = -0.166;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.647;
            b = -69.3;
            c = -0.15;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.734;
            b = -107;
            c = -0.164;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.816;
            b = -102;
            c = -0.162;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.868;
            b = -96.2;
            c = -0.158;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.878;
            b = -111;
            c = -0.165;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.893;
            b = -83.9;
            c = -0.156;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -59.6;
            c = -0.141;
        };
    }

    else if (syst == "BTagTrig1Down")
    {
        if (btag < -10.)
        {
            a = 0.0138;
            b = -45.4;
            c = -0.146;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.065;
            b = -14.6;
            c = -0.104;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.019;
            b = -9.33;
            c = -0.0719;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.0266;
            b = -20.7;
            c = -0.0102;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0706;
            b = -65.1;
            c = -0.147;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.253;
            b = -192.;
            c = -0.191;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.387;
            b = -192.;
            c = -0.186;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.529;
            b = -188.;
            c = -0.183;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.642;
            b = -106.;
            c = -0.164;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.73;
            b = -161.;
            c = -0.179;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.813;
            b = -129.;
            c = -0.17;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.865;
            b = -123.;
            c = -0.166;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.881;
            b = -151.;
            c = -0.176;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.891;
            b = -103.;
            c = -0.162;
        };
        if (btag > 10.0 )
        {
            a = 0.885;
            b = -70.6;
            c = -0.146;
        };
    }
    else if (syst == "BTagTrig2Up")
    {
        if (btag < -10.)
        {
            a = 0.0141;
            b = -36.5;
            c = -0.136;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0727;
            b = -9.42;
            c = -0.0797;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0195;
            b = -8.52;
            c = -0.0677;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -18.5;
            c = -0.0969;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.071;
            b = -57.5;
            c = -0.142;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.256;
            b = -150.;
            c = -0.181;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.392;
            b = -152.;
            c = -0.176;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.536;
            b = -151.;
            c = -0.174;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.649;
            b = -87.5;
            c = -0.156;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.737;
            b = -134.0;
            c = -0.171;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.818;
            b = -115.;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.869;
            b = -110.;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.883;
            b = -131.;
            c = -0.171;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.894;
            b = -93.4;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.887;
            b = -65.1;
            c = -0.144;
        };

    }
    else if (syst == "BTagTrig2Down")
    {
        if (btag < -10.)
        {
            a = 0.0138;
            b = -36.5;
            c = -0.138;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0658;
            b = -9.42;
            c = -0.0859;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0191;
            b = -8.52;
            c = -0.0689;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.0267;
            b = -18.5;
            c = -0.098;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0706;
            b = -57.5;
            c = -0.144;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.252;
            b = -150;
            c = -0.182;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.384;
            b = -152.;
            c = -0.177;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.527;
            b = -151.;
            c = -0.175;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.639;
            b = -87.5;
            c = -0.157;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.727;
            b = -134.0;
            c = -0.172;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.812;
            b = -115.;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.863;
            b = -110.;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.877;
            b = -131.;
            c = -0.170;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.89;
            b = -93.4;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.884;
            b = -65.1;
            c = -0.144;
        };

    }
    else if (syst == "BTagTrig3Up")
    {
        if (btag < -10.)
        {
            a = 0.0139;
            b = -36.5;
            c = -0.137;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0702;
            b = -9.42;
            c = -0.0839;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0192;
            b = -8.52;
            c = -0.0683;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.0267;
            b = -18.5;
            c = -0.0974;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0705;
            b = -57.5;
            c = -0.143;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.254;
            b = -150.;
            c = -0.183;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.388;
            b = -152.;
            c = -0.178;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.531;
            b = -151.;
            c = -0.175;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.644;
            b = -87.5;
            c = -0.158;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.732;
            b = -134.0;
            c = -0.172;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.815;
            b = -115.;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.866;
            b = -110.;
            c = -0.163;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.880;
            b = -131.;
            c = -0.171;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.892;
            b = -93.4;
            c = -0.160;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -65.1;
            c = -0.144;
        };
    }
    else if (syst == "BTagTrig3Down")
    {
        if (btag < -10.)
        {
            a = 0.0141;
            b = -36.5;
            c = -0.137;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0683;
            b = -9.42;
            c = -0.0817;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0194;
            b = -8.52;
            c = -0.0684;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -18.5;
            c = -0.0975;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0711;
            b = -57.5;
            c = -0.143;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.253;
            b = -150.;
            c = -0.18;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.388;
            b = -152.;
            c = -0.176;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.531;
            b = -151.;
            c = -0.174;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.644;
            b = -87.5;
            c = -0.156;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.732;
            b = -134.0;
            c = -0.171;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.815;
            b = -115.;
            c = -0.165;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.866;
            b = -110.;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.880;
            b = -131.;
            c = -0.170;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.892;
            b = -93.4;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -65.11;
            c = -0.143;
        };

    }
    else
    {
        if (btag < -10.)
        {
            a = 0.014;
            b = -36.55;
            c = -0.137;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.069;
            b = -9.42;
            c = -0.083;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.019;
            b = -8.52;
            c = -0.068;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -18.51;
            c = -0.097;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.071;
            b = -57.54;
            c = -0.143;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.254;
            b = -150.48;
            c = -0.182;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.388;
            b = -151.97;
            c = -0.177;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.531;
            b = -150.73;
            c = -0.175;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.644;
            b = -87.52;
            c = -0.157;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.732;
            b = -134.05;
            c = -0.172;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.815;
            b = -115.25;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.866;
            b = -109.53;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.880;
            b = -130.84;
            c = -0.170;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.892;
            b = -93.41;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -65.11;
            c = -0.144;
        };
    }
    prob = a * exp(b * exp(c * pt));
    return prob;
}

double SingleTopSystematicsTreesDumper::jetprobold(double pt, double btag, double eta, string syst)
{
    double prob = 1.;

    if (fabs(eta) > 2.6) return 0.;
    //PT turnOn
    if (syst == "JetTrig1Up")
    {

        if (eta < -1.4)prob = 0.981 * exp(-37.49 * exp(-0.158 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.51 * exp(-0.146 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.63 * exp(-0.145 * pt));
        if (eta > 1.4)prob = 0.984 * exp(-42.17 * exp(-0.158 * pt));
        ;
    }
    else if (syst == "JetTrig2Up")
    {
        if (eta < -1.4)prob = 0.982 * exp(-41.17 * exp(-0.161 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.983 * exp(-27.03 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.983 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.986 * exp(-45.11 * exp(-0.161 * pt));
        ;
    }
    else if (syst == "JetTrig3Up")
    {
        if (eta < -1.4)prob = 0.981 * exp(-41.17 * exp(-0.162 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.03 * exp(-0.146 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.985 * exp(-45.11 * exp(-0.161 * pt));

        prob = 0.982 * exp(-30.6 * exp(-0.151 * pt));
        ;
    }
    else if (syst == "JetTrig1Down")
    {
        if (eta < -1.4)prob = 0.981 * exp(-44.84 * exp(-0.164 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-26.56 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.983 * exp(-25.72 * exp(-0.147 * pt));
        if (eta > 1.4)prob = 0.985 * exp(-48.05 * exp(-0.164 * pt))
                                 ;
    }
    else if (syst == "JetTrig2Down")
    {
        if (eta < -1.4)prob = 0.98 * exp(-41.17 * exp(-0.161 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.03 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.984 * exp(-45.11 * exp(-0.161 * pt));

        ;
    }
    else if (syst == "JetTrig3Down")
    {
        if (eta < -1.4)prob = 0.981 * exp(-41.17 * exp(-0.161 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.03 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.985 * exp(-45.11 * exp(-0.16 * pt));

        ;
    }
    else prob = 0.982 * exp(-30.6 * exp(-0.151 * pt));


    //BTag turnOn
    if (syst == "BTagTrig1Up")
    {
        prob *= 0.85 * exp(-6.35 * exp(-0.681 * btag));
    }
    else if (syst == "BTagTrig1Down")
    {
        prob *= 0.839 * exp(-7.1 * exp(-0.759 * btag));
    }
    else if (syst == "BTagTrig2Up")
    {
        prob *= 0.824 * exp(-6.72 * exp(-0.733 * btag));
    }
    else if (syst == "BTagTrig2Down")
    {
        prob *= 0.865 * exp(-6.73 * exp(-0.707 * btag));
    }
    else if (syst == "BTagTrig3Up")
    {
        prob *= 0.838 * exp(-6.73 * exp(-0.71 * btag));
    }
    else if (syst == "BTagTrig3Down")
    {
        prob *= 0.851 * exp(-6.72 * exp(-0.73 * btag));
    }
    else prob *= 0.844 * exp((-6.72 * exp(-0.720 * btag)));

    return prob;

}

double SingleTopSystematicsTreesDumper::bTagSF(int B)
{
    //  cout<< " B " << " ntchhpt "<<   ntchpt_tags << " jsfshpt size "<<
    //  jsfshpt.size() << " ntchel " << ntchel_tags<< " jsfshel size " << jsfshel.size()<<endl;

    if (algo_ == "TCHPT")
    {
        if (B == 0 || B == 3)
        {
            return b_tchpt_0_tags.weight(jsfshpt, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
        }
        if (B == 1 || B == 4)
        {
            return b_tchpt_1_tag.weight(jsfshpt, ntchpt_tags);
        }
        if (B == 2 || B == 5)
        {
            return b_tchpt_2_tags.weight(jsfshpt, ntchpt_tags);
        }
    }

    if(doLooseBJetVeto_){
     if(B==1 || B == 4) return b_csvt_1_tag.weightWithVeto(jsfscsvt,ncsvt_tags,jsfscsvm,ncsvl_tags);
    }


    if (B == 0 || B == 3)
    {
        return b_csvt_0_tags.weight(jsfscsvt, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
    }
    if (B == 1 || B == 4)
    {
        return b_csvt_1_tag.weight(jsfscsvt, ncsvt_tags);
    }
    if (B == 2 || B == 5)
    {
        return b_csvt_2_tags.weight(jsfscsvt, ncsvt_tags);
    }
    return 1.;
}


/*double SingleTopSystematicsTreesDumper::vetoSF(int B, string syst){

  if (B==1 || B==4){

    return 1;
  }

  return 1;
  }*/

double SingleTopSystematicsTreesDumper::bTagSF(int B, string syst)
{
    //  cout<< " B " << " ntchhpt "<<   ntchpt_tags << " jsfshpt size "<<
    // jsfshpt.size() << " ntchel " << ntchel_tags<< " jsfshel size " << jsfshel.size()<<endl;
    if (algo_ == "TCHPT")
    {
        if (B == 0 || B == 3)
        {
            if (syst == "BTagUp")    return b_tchpt_0_tags.weight(jsfshpt_b_tag_up, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_up,ntchel_tags);
            if (syst == "BTagDown")    return b_tchpt_0_tags.weight(jsfshpt_b_tag_down, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_down,ntchel_tags);
            if (syst == "MisTagUp")    return b_tchpt_0_tags.weight(jsfshpt_mis_tag_up, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_up,ntchel_tags);
            if (syst == "MisTagDown")    return b_tchpt_0_tags.weight(jsfshpt_mis_tag_down, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_down,ntchel_tags);
            return b_tchpt_0_tags.weight(jsfshpt, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
        }
        if (B == 1 || B == 4)
        {

            if (syst == "BTagUp")    return b_tchpt_1_tag.weight(jsfshpt_b_tag_up, ntchpt_tags);
            if (syst == "BTagDown")    return b_tchpt_1_tag.weight(jsfshpt_b_tag_down, ntchpt_tags);
            if (syst == "MisTagUp")    return b_tchpt_1_tag.weight(jsfshpt_mis_tag_up, ntchpt_tags);
            if (syst == "MisTagDown")    return b_tchpt_1_tag.weight(jsfshpt_mis_tag_down, ntchpt_tags);

            return b_tchpt_1_tag.weight(jsfshpt, ntchpt_tags);
        }
        if (B == 2 || B == 5)
        {

            if (syst == "BTagUp")    return b_tchpt_2_tags.weight(jsfshpt_b_tag_up, ntchpt_tags);
            if (syst == "BTagDown")    return b_tchpt_2_tags.weight(jsfshpt_b_tag_down, ntchpt_tags);
            if (syst == "MisTagUp")    return b_tchpt_2_tags.weight(jsfshpt_mis_tag_up, ntchpt_tags);
            if (syst == "MisTagDown")    return b_tchpt_2_tags.weight(jsfshpt_mis_tag_down, ntchpt_tags);

            return b_tchpt_2_tags.weight(jsfshpt, ntchpt_tags);
        }
    }

    //Loose jet veto:
    if(doLooseBJetVeto_){
      if (B == 1 || B == 4)
	{
	  //	  if(syst ) return b_csvt_1_tag.weightWithVeto(jsfscsvt,ncsvt_tags,jsfscsvm,ncsvl_tags);	  
	  if (syst == "BTagUp")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_b_tag_up, ncsvt_tags,jsfscsvm_b_tag_up, ncsvl_tags);
	  if (syst == "BTagDown")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_b_tag_down, ncsvt_tags,jsfscsvm_b_tag_down, ncsvl_tags);
	  if (syst == "MisTagUp")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_mis_tag_up, ncsvt_tags,jsfscsvm_mis_tag_up, ncsvl_tags);
	  if (syst == "MisTagDown")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_mis_tag_down, ncsvt_tags,jsfscsvm_mis_tag_down, ncsvl_tags);

	  return b_csvt_1_tag.weightWithVeto(jsfscsvt,ncsvt_tags,jsfscsvm,ncsvl_tags);	  
	
	}
    }


    //Default case: use csvt

    if (B == 0 || B == 3)
    {
      if (syst == "BTagUp")    return b_csvt_0_tags.weight(jsfscsvt_b_tag_up, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_up,ntchel_tags);
      if (syst == "BTagDown")    return b_csvt_0_tags.weight(jsfscsvt_b_tag_down, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_down,ntchel_tags);
      if (syst == "MisTagUp")    return b_csvt_0_tags.weight(jsfscsvt_mis_tag_up, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_up,ntchel_tags);
      if (syst == "MisTagDown")    return b_csvt_0_tags.weight(jsfscsvt_mis_tag_down, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_down,ntchel_tags);
      return b_csvt_0_tags.weight(jsfscsvt, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
    }
    
    if (B == 1 || B == 4)
    {

        if (syst == "BTagUp")    return b_csvt_1_tag.weight(jsfscsvt_b_tag_up, ncsvt_tags);
        if (syst == "BTagDown")    return b_csvt_1_tag.weight(jsfscsvt_b_tag_down, ncsvt_tags);
        if (syst == "MisTagUp")    return b_csvt_1_tag.weight(jsfscsvt_mis_tag_up, ncsvt_tags);
        if (syst == "MisTagDown")    return b_csvt_1_tag.weight(jsfscsvt_mis_tag_down, ncsvt_tags);

        return b_csvt_1_tag.weight(jsfscsvt, ncsvt_tags);
    }
    if (B == 2 || B == 5)
    {

        if (syst == "BTagUp")    return b_csvt_2_tags.weight(jsfscsvt_b_tag_up, ncsvt_tags);
        if (syst == "BTagDown")    return b_csvt_2_tags.weight(jsfscsvt_b_tag_down, ncsvt_tags);
        if (syst == "MisTagUp")    return b_csvt_2_tags.weight(jsfscsvt_mis_tag_up, ncsvt_tags);
        if (syst == "MisTagDown")    return b_csvt_2_tags.weight(jsfscsvt_mis_tag_down, ncsvt_tags);

        return b_csvt_2_tags.weight(jsfscsvt, ncsvt_tags);
    }

    return 1.;
}


double SingleTopSystematicsTreesDumper::pileUpSF(string syst)
{

    //  if(syst=="PUUp" )return LumiWeightsUp_.weight3D( *nm1,*n0,*np1);
    //if(syst=="PUDown" )return LumiWeightsDown_.weight3D( *nm1,*n0,*np1);
    //return LumiWeights_.weight3D( *nm1,*n0,*np1);

    if (syst == "PUUp" )return LumiWeightsUp_.weight( *n0);
    if (syst == "PUDown" )return LumiWeightsDown_.weight( *n0);
    return LumiWeights_.weight( *n0);



}

double SingleTopSystematicsTreesDumper::pileUpSFNew()
{
   return NewPUWeights_.weight(npv);
}


double SingleTopSystematicsTreesDumper::resolSF(double eta, string syst)
{
    double fac = 0.;
    if (syst == "JERUp")fac = 1.;
    if (syst == "JERDown")fac = -1.;
    if (eta <= 0.5) return 0.05 + 0.06 * fac;
    else if ( eta > 0.5 && eta <= 1.1 ) return 0.06 + 0.06 * fac;
    else if ( eta > 1.1 && eta <= 1.7 ) return 0.1 + 0.06 * fac;
    else if ( eta > 1.7 && eta <= 2.3 ) return 0.13 + 0.1 * fac;
    else if ( eta > 2.3 && eta <= 5. ) return 0.29 + 0.2 * fac;
    return 0.1;
}


//BTag weighter
bool SingleTopSystematicsTreesDumper::BTagWeight::filter(int t)
{
    return (t >= minTags && t <= maxTags);
}

float SingleTopSystematicsTreesDumper::BTagWeight::weight(vector<JetInfo> jets, int tags)
{
    if (!filter(tags))
    {
        //   std::cout << "nThis event should not pass the selection, what is it doing here?" << std::endl;
        return 0;
    }
    int njets = jets.size();
    int comb = 1 << njets;
    float pMC = 0;
    float pData = 0;
    for (int i = 0; i < comb; i++)
    {
        float mc = 1.;
        float data = 1.;
        int ntagged = 0;
        for (int j = 0; j < njets; j++)
        {
            bool tagged = ((i >> j) & 0x1) == 1;
            if (tagged)
            {
                ntagged++;
                mc *= jets[j].eff;
                data *= jets[j].eff * jets[j].sf;
            }
            else
            {
                mc *= (1. - jets[j].eff);
                data *= (1. - jets[j].eff * jets[j].sf);
            }
        }

        if (filter(ntagged))
        {
            //  std::cout << mc << " " << data << endl;
            pMC += mc;
            pData += data;
        }
    }

    if (pMC == 0) return 0;
    return pData / pMC;
}



float SingleTopSystematicsTreesDumper::BTagWeight::weightWithVeto(vector<JetInfo> jetsTags, int tags, vector<JetInfo> jetsVetoes, int vetoes)
{//This function takes into account cases where you have n b-tags and m vetoes, but they have different thresholds. 
    if (!filter(tags))
    {
        //   std::cout << "nThis event should not pass the selection, what is it doing here?" << std::endl;
        return 0;
    }
    int njets = jetsTags.size();
    if(njets != (int)(jetsVetoes.size()))return 0;//jets tags and vetoes must have same size!
    int comb = 1 << njets;
    float pMC = 0;
    float pData = 0;
    for (int i = 0; i < comb; i++)
    {
        float mc = 1.;
        float data = 1.;
        int ntagged = 0;
        for (int j = 0; j < njets; j++)
        {
            bool tagged = ((i >> j) & 0x1) == 1;
            if (tagged)
            {
                ntagged++;
                mc *= jetsTags[j].eff;
                data *= jetsTags[j].eff * jetsTags[j].sf;
            }
            else
            {
                mc *= (1. - jetsVetoes[j].eff);
                data *= (1. - jetsVetoes[j].eff * jetsVetoes[j].sf);
            }
        }

        if (filter(ntagged))
        {
            //  std::cout << mc << " " << data << endl;
            pMC += mc;
            pData += data;
        }
    }

    if (pMC == 0) return 0;
    return pData / pMC;
}


void SingleTopSystematicsTreesDumper::resetWeightsDoubles()
{
    /*  cout << "start doubles removal...";

    for(int bj = 0; bj<=5;++bj){
      for (size_t j = 0; j < systematics.size();++j){
        string syst = systematics[j];

        trees2J[bj][syst]->Branch("weightDoubles",&miscWeightTree);
        int nentries =  trees2J[bj][syst]->GetEntries();

        if(bj==1|| bj==4){

    int idtmp, runtmp;
    map<long int,int> ids;

    for (int i =0; i< nentries;++i){
      trees2J[bj][syst]->GetEntry(i);
      idtmp = eventTree;
      runtmp = runTree;
      stringstream s,s2;
      s<<idtmp ;
      s2<<runtmp;
      string ss = s.str();
      string ss2 = s2.str();
      string cond = "eventid == "+ss;
      miscWeightTree= 1.;
      if (channel == "Data") cond = "eventid=="+ss +"&& runid == "+ss2  ;
      //cout << "entries " << trees2J[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  << " weight"<< miscWeightTree<< endl;
      if(trees2J[bj][syst]->GetEntries(cond.c_str())>1){
        ids[idtmp]+=1;
        if(ids[idtmp]>1)miscWeightTree=0;
        //  cout << " found cond "<<endl;
      }
      //cout << "entries after" << trees2J[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  << " weight"<< miscWeightTree<< endl;
      trees2J[bj][syst]->GetBranch("weightDoubles")->Fill();
      //      cout << cond << endl;
      //     cout << "entries " << trees2J[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  <<endl;
    }
        }
        else{
    for (int i =0; i< nentries;++i){
      trees2J[bj][syst]->GetEntry(i);
      miscWeightTree = 1.;
      trees2J[bj][syst]->GetBranch("weightDoubles")->Fill();
    }

        }
      }
    }
    */;
}


//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopSystematicsTreesDumper);
