/**********************************************************************************
 * Project   : TMVA - a Root-integrated toolkit for multivariate data analysis    *
 * Package   : TMVA                                                               *
 * Exectuable: TMVAClassificationApplication                                      *
 *                                                                                *
 * This macro provides a simple example on how to use the trained classifiers     *
 * within an analysis module                                                      *
 **********************************************************************************/

#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"

#include "TMVAGui.C"

#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"
#endif

using namespace TMVA;

void TMVAClassificationApplication_tW(TString sample = "TWChannel", TString syst = "",TString region = "1j1t", TString directory = "v4", TString chanName = "emu",   TString bdtTraining =  "AdaBoost500TreesMET50", int variableSet = -1)
{   
#ifdef __CINT__
  gROOT->ProcessLine( ".O0" ); // turn off optimization in CINT
#endif

  cout << sample << "\t" << syst << "\t" << region << "\t" << directory << "\t" << chanName << "\t" << bdtTraining << endl;
  
  //---------------------------------------------------------------
  // This loads the library
  TMVA::Tools::Instance();
  // --------------------------------------------------------------------------------------------------
  
  // --- Create the Reader object
  
  TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );    
  
  // Create a set of variables and declare them to the reader
  // - the variable names MUST corresponds in name and type to those given in the weight file(s) used
  
  Float_t ptjet;
  Float_t ptsys;
  Float_t ht;
  Float_t NlooseJet20;
  Float_t NlooseJet20Central;
  Float_t NbtaggedlooseJet20;
  Float_t centralityJLL;
  Float_t loosejetPt;
  Float_t ptsys_ht;
  Float_t msys;
  Float_t htleps_ht;
  Float_t ptjll;
  Float_t met;

  if (variableSet == -1 || variableSet == 0){
    reader->AddVariable ("ptjet", &ptjet);
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("NlooseJet20", &NlooseJet20);
    reader->AddVariable ("NlooseJet20Central", &NlooseJet20Central);
    reader->AddVariable ("NbtaggedlooseJet20", &NbtaggedlooseJet20);
    reader->AddVariable ("centralityJLL", &centralityJLL);
    reader->AddVariable ("loosejetPt", &loosejetPt);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
    reader->AddVariable ("met", &met);
  }
  if (variableSet == 1){ //NoMET
    reader->AddVariable ("ptjet", &ptjet);
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("NlooseJet20", &NlooseJet20);
    reader->AddVariable ("NlooseJet20Central", &NlooseJet20Central);
    reader->AddVariable ("NbtaggedlooseJet20", &NbtaggedlooseJet20);
    reader->AddVariable ("centralityJLL", &centralityJLL);
    reader->AddVariable ("loosejetPt", &loosejetPt);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
  }

  if (variableSet == 2){ //NoMET, jetpt, loosejetPt, or NlooseJetCentral
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("NlooseJet20", &NlooseJet20);
    reader->AddVariable ("NbtaggedlooseJet20", &NbtaggedlooseJet20);
    reader->AddVariable ("centralityJLL", &centralityJLL);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
  }

  if (variableSet == 3){ //No MET or jet variables
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("centralityJLL", &centralityJLL);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
  }

  if (variableSet == 4){
    reader->AddVariable ("ptjet", &ptjet);
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("NlooseJet20", &NlooseJet20);
    reader->AddVariable ("NlooseJet20Central", &NlooseJet20Central);
    reader->AddVariable ("NbtaggedlooseJet20", &NbtaggedlooseJet20);
    reader->AddVariable ("loosejetPt", &loosejetPt);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
    reader->AddVariable ("met", &met);
  }

  if (variableSet == 5){
    reader->AddVariable ("ptjet", &ptjet);
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
    reader->AddVariable ("met", &met);
  }

  if (variableSet == 6){
    reader->AddVariable ("ptjet", &ptjet);
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("NlooseJet20Central", &NlooseJet20Central);
    reader->AddVariable ("NbtaggedlooseJet20", &NbtaggedlooseJet20);
    reader->AddVariable ("centralityJLL", &centralityJLL);
    reader->AddVariable ("loosejetPt", &loosejetPt);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
    reader->AddVariable ("met", &met);
  }

  if (variableSet == 7){
    reader->AddVariable ("ptjet", &ptjet);
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("ht",&ht);
    reader->AddVariable ("centralityJLL", &centralityJLL);
    reader->AddVariable ("ptsys_ht",&ptsys_ht);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
    reader->AddVariable ("met", &met);
  }

  if (variableSet == 8){
    reader->AddVariable ("ptjet", &ptjet);
    reader->AddVariable ("ptsys",&ptsys);
    reader->AddVariable ("NlooseJet20", &NlooseJet20);
    reader->AddVariable ("centralityJLL", &centralityJLL);
    reader->AddVariable ("msys", &msys);
    reader->AddVariable ("htleps_ht", &htleps_ht);
    reader->AddVariable ("ptjll", &ptjll);
  }
  
  // *************************************************
  
  // --- Book the MVA methods
  
  TString dir    = "weights/";
  TString extra =  bdtTraining;
  TString prefix = "test_tw_00_";



  TString name = extra +"_"+ chanName + "_" + region;
  
  if (bdtTraining == "AdaBoost500Trees") prefix = "test_tw_00_AdaBoostTests_13Vars_NtreeTests";

  //
  // book the MVA methods
  //
  
  reader->BookMVA( "BDT method", dir + prefix + extra+".weights.xml" );   
  
  // book output histograms
  
  
  // Prepare input tree (this must be replaced by your data source)
  // in this example, there is a toy tree with signal and one with background events
  // we'll later on use only the "signal" events for the test in this example.
  //   
  TFile *input(0);
    
  TString folder = "tmvaFiles/"+directory+"/";

  TString systlabel = "";
  if (syst != ""){
    systlabel = "_"+syst;
  }

  //  TString fname = folder + "TWChannel.root";
  TString fname = folder + sample + systlabel + ".root";


  cout << fname << endl;

  //  input->SetCacheSize(20*1024*1024);
  
  input = TFile::Open( fname,"r");   
  
  if (!input) {
    cout << "ERROR: could not open data file: " << fname << endl;
    exit(1);
  }
  
  // --- Event loop
  
  // Prepare the event tree
  // - here the variable names have to corresponds to your tree
  // - you can use the same variables as above which is slightly faster,
  //   but of course you can use different ones and copy the values inside the event loop
  //
  
  TString treeName = chanName + "Channel/"+region;
  TTree* theTree = (TTree*)input->Get(treeName);

  cout << "--- Select signal sample" << endl;

  theTree->SetCacheSize(20*1024*1024);
  
  Double_t userptjet;
  Double_t userptsys;
  Double_t userht;
  Int_t userNlooseJet20;
  Int_t userNlooseJet20Central;
  Int_t userNbtaggedlooseJet20;
  Double_t usercentralityJLL;
  Double_t userloosejetPt;
  Double_t userptsys_ht;
  Double_t usermsys;
  Double_t userhtleps_ht;
  Double_t userptjll;
  Double_t usermet;
  Double_t userweightA;
  Double_t userweightB;
  Double_t userweightC;
  Double_t userweightD;
    
  theTree->SetBranchAddress ("ptjet", &userptjet);
  theTree->SetBranchAddress ("ptsys",&userptsys);
  theTree->SetBranchAddress ("ht",&userht);
  theTree->SetBranchAddress ("NlooseJet20", &userNlooseJet20);
  theTree->SetBranchAddress ("NlooseJet20Central", &userNlooseJet20Central);
  theTree->SetBranchAddress ("NbtaggedlooseJet20", &userNbtaggedlooseJet20);
  theTree->SetBranchAddress ("centralityJLL", &usercentralityJLL);
  theTree->SetBranchAddress ("loosejetPt", &userloosejetPt);
  theTree->SetBranchAddress ("ptsys_ht",&userptsys_ht);
  theTree->SetBranchAddress ("msys", &usermsys);
  theTree->SetBranchAddress ("htleps_ht", &userhtleps_ht);
  theTree->SetBranchAddress ("ptjll", &userptjll);
  theTree->SetBranchAddress ("met", &usermet);
  theTree->SetBranchAddress ("weightA", &userweightA);
  theTree->SetBranchAddress ("weightB", &userweightB);
  theTree->SetBranchAddress ("weightC", &userweightC);
  theTree->SetBranchAddress ("weightD", &userweightD);
  
  Double_t tBDT;    
  Double_t tweightA;
  Double_t tweightB;
  Double_t tweightC;
  Double_t tweightD;

  TFile *output(0);

  TString outName = folder +bdtTraining+"/"+ sample+systlabel+"_Output.root";

  cout << "Output root file: " << outName << endl;

  output = TFile::Open(outName,"UPDATE");

  TTree* BDTTree = new TTree(name,"");
  BDTTree->Branch("BDT",&tBDT,"BDT/D");
  BDTTree->Branch("weightA",&tweightA,"weightA/D");
  BDTTree->Branch("weightB",&tweightB,"weightB/D");
  BDTTree->Branch("weightC",&tweightC,"weightC/D");
  BDTTree->Branch("weightD",&tweightD,"weightD/D");
  
  std::cout<<" ... opening file : "<<fname<<std::endl;
  cout << "--- Processing: " << theTree->GetEntries() << " events" << endl;
  
  TStopwatch sw;
  sw.Start();
  for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {
    
    if (ievt%1000 == 0)      cout << "--- ... Processing event: " << ievt << endl;
          
    theTree->GetEntry(ievt);

    ptjet              = userptjet;
    ptsys	       = userptsys;	      
    ht		       = userht;		      
    NlooseJet20	       = userNlooseJet20;	      
    NlooseJet20Central = userNlooseJet20Central;
    NbtaggedlooseJet20 = userNbtaggedlooseJet20;
    centralityJLL      = usercentralityJLL;     
    loosejetPt	       = userloosejetPt;	      
    ptsys_ht	       = userptsys_ht;	      
    msys	       = usermsys;	      
    htleps_ht	       = userhtleps_ht;	      
    ptjll	       = userptjll;	      
    met                = usermet;               

    //    sw.Print();
    double bdt         = reader->EvaluateMVA("BDT method");
    tBDT = bdt;

    tweightA = userweightA;
    tweightB = userweightB;
    tweightC = userweightC;
    tweightD = userweightD;

    BDTTree->Fill();

  }

  // Get elapsed time
  sw.Stop();
  std::cout << "--- End of event loop: "; sw.Print();
  
  input->Close();


  output->cd();

  BDTTree->Write();
  
  output->Close();
  
    // --- Write histograms
  
  delete reader;
  
  std::cout << "==> TMVAClassificationApplication is done!" << endl << std::endl;
} 
