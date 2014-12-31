// @(#)root/tmva $Id: TMVAClassification_tW.C,v 1.1 2011/11/10 18:03:30 rebeca Exp $
/**********************************************************************************
 * Project   : TMVA - a ROOT-integrated toolkit for multivariate data analysis    *
 * Package   : TMVA                                                               *
 * Root Macro: TMVAClassification                                                 *
 *                                                                                *
 * This macro provides examples for the training and testing of the               *
 * TMVA classifiers.                                                              *
 *                                                                                *
 * As input data is used a toy-MC sample consisting of four Gaussian-distributed  *
 * and linearly correlated input variables.                                       *
 *                                                                                *
 * The methods to be used can be switched on and off by means of booleans, or     *
 * via the prompt command, for example:                                           *
 *                                                                                *
 *    root -l ./TMVAClassification.C\(\"Fisher,Likelihood\"\)                     *
 *                                                                                *
 * (note that the backslashes are mandatory)                                      *
 * If no method given, a default set of classifiers is used.                      *
 *                                                                                *
 * The output file "TMVA.root" can be analysed with the use of dedicated          *
 * macros (simply say: root -l <macro.C>), which can be conveniently              *
 * invoked through a GUI that will appear at the end of the run of this macro.    *
 * Launch the GUI via the command:                                                *
 *                                                                                *
 *    root -l ./TMVAGui.C                                                         *
 *                                                                                *
 **********************************************************************************/

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVAGui.C"

#if not defined(__CINT__) || defined(__MAKECINT__)
// needs to be included when makecint runs (ACLIC)
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#endif

void TMVAClassification_tW()
{

  // ---------------------------------------------------------------
  std::cout << std::endl;
  std::cout << "==> Start TMVAClassification" << std::endl;
  // --------------------------------------------------------------------------------------------------

  TString names = "AdaBoostTest_April22";  
  // --- Here the preparation phase begins
  
  // Create a ROOT output file where TMVA will store ntuples, histograms, etc.
  TString TrainName = "test_tw_00";
  
  TString outfileName( "trainrootfiles/"+TrainName+"_"+names+".root" );
  TFile* outputFile = TFile::Open( outfileName, "RECREATE" );
  
  // Create the factory object. Later you can choose the methods
  // whose performance you'd like to investigate. The factory is 
  // the only TMVA object you have to interact with
  //
  // The first argument is the base of the name of all the
  // weightfiles in the directory weight/
  //
  // The second argument is the output file for the training results
  // All TMVA output can be suppressed by removing the "!" (not) in
  // front of the "Silent" argument in the option string
  TMVA::Factory *factory = new TMVA::Factory( TrainName, outputFile,
					      "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );

//   TMVA::Factory *factory = new TMVA::Factory( TrainName, outputFile,
// 					      "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification" );
  
  // If you wish to modify default settings
  // (please check "src/Config.h" to see all available global options)
  //    (TMVA::gConfig().GetVariablePlotting()).fTimesRMS = 8.0;
  //    (TMVA::gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory";
  
  // Define the input variables that shall be used for the MVA training
  // note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
  // [all types of expressions that can also be parsed by TTree::Draw( "expression" )]
  
  factory->AddVariable ("ptjet", 'F');
  factory->AddVariable ("ptsys",'F');
  factory->AddVariable ("ht",'F');
  factory->AddVariable ("NlooseJet20", 'I');
  factory->AddVariable ("NlooseJet20Central", 'I');
  factory->AddVariable ("NbtaggedLooseJet20", 'I');
  factory->AddVariable ("centralityJLL", 'F');
  factory->AddVariable ("loosejetPt", 'F');
  factory->AddVariable ("ptsys_ht",'F');
  factory->AddVariable ("msys", 'F');
  factory->AddVariable ("htleps_ht", 'F');
  factory->AddVariable ("ptjll", 'F');
  factory->AddVariable ("met", 'F');


//   factory->AddVariable ("ptjet", 'F');
//   factory->AddVariable ("ptlep0", 'F');
//   factory->AddVariable ("ptlep1", 'F');
//   factory->AddVariable ("jetCSV", 'F');
//   factory->AddVariable ("ht", 'F');
//   //  factory->AddVariable ("htTot", 'F');
//   factory->AddVariable ("htNoMet", 'F');
//   factory->AddVariable ("msys", 'F');
//   factory->AddVariable ("mjll", 'F');
//   factory->AddVariable ("mjl0", 'F');
//   factory->AddVariable ("mjl1", 'F');
//   factory->AddVariable ("ptsys", 'F');
//   //  factory->AddVariable ("ptsysTot", 'F');
//   factory->AddVariable ("ptjll", 'F');
//   factory->AddVariable ("ptjl0", 'F');
//   factory->AddVariable ("ptjl1", 'F');
//   factory->AddVariable ("ptleps", 'F');
//   factory->AddVariable ("htleps", 'F');
//   factory->AddVariable ("ptsys_ht", 'F');
//   factory->AddVariable ("ptjet_ht", 'F');
//   factory->AddVariable ("ptlep0_ht", 'F');
//   factory->AddVariable ("ptlep1_ht", 'F');
//   factory->AddVariable ("ptleps_ht", 'F');
//   factory->AddVariable ("htleps_ht", 'F');

//   factory->AddVariable ("NlooseJet15Central", 'I');
//   factory->AddVariable ("NlooseJet15Forward", 'I');
//   factory->AddVariable ("NlooseJet20Central", 'I');
//   factory->AddVariable ("NlooseJet20Forward", 'I');
//   factory->AddVariable ("NlooseJet25Central", 'I');
//   factory->AddVariable ("NlooseJet25Forward", 'I');
//   factory->AddVariable ("NtightJetForward", 'I');
// //   factory->AddVariable ("NlooseJet15", 'I');
//   factory->AddVariable ("NlooseJet20", 'I');
//   factory->AddVariable ("NlooseJet25", 'I');
// //   factory->AddVariable ("NbtaggedlooseJet15", 'I');
//   factory->AddVariable ("NbtaggedlooseJet20", 'I');
//   factory->AddVariable ("NbtaggedlooseJet25", 'I');

//   factory->AddVariable ("unweightedEta_Avg", 'F');
//   factory->AddVariable ("unweightedEta_Vecjll", 'F');
//   factory->AddVariable ("unweightedEta_Vecsys", 'F');
//   factory->AddVariable ("unweightedPhi_Avg", 'F');
//   factory->AddVariable ("unweightedPhi_Vecjll", 'F');
//   factory->AddVariable ("unweightedPhi_Vecsys", 'F');
//   factory->AddVariable ("avgEta", 'F');
//   factory->AddVariable ("sysEta", 'F');
//   factory->AddVariable ("jllEta", 'F');
//   factory->AddVariable ("dRleps", 'F');
//   factory->AddVariable ("dRjlmin", 'F');
//   factory->AddVariable ("dRjlmax", 'F');
//   factory->AddVariable ("dEtaleps", 'F');
//   factory->AddVariable ("dEtajlmin", 'F');
//   factory->AddVariable ("dEtajlmax", 'F');
//   factory->AddVariable ("dPhileps", 'F');
//   factory->AddVariable ("dPhijlmin", 'F');
//   factory->AddVariable ("dPhijlmax", 'F');

// //   factory->AddVariable ("dPhimetlmin", 'F');
// //   factory->AddVariable ("dPhimetlmax", 'F');
// //   factory->AddVariable ("dPhijmet", 'F');

//   factory->AddVariable ("met", 'F');
//   factory->AddVariable ("etajet", 'F');
//   factory->AddVariable ("etalep0", 'F');
//   factory->AddVariable ("etalep1", 'F');
//   factory->AddVariable ("phijet", 'F');
//   factory->AddVariable ("philep0", 'F');
//   factory->AddVariable ("philep1", 'F');
//   factory->AddVariable ("phimet", 'F');
//   factory->AddVariable ("sumeta2", 'F');
//   factory->AddVariable ("loosejetPt", 'F');
//   factory->AddVariable ("loosejetCSV", 'F');
//   factory->AddVariable ("centralityJLL", 'F');
//   factory->AddVariable ("centralityJLLM", 'F');
//   factory->AddVariable ("centralityJLLWithLoose", 'F');
//   factory->AddVariable ("centralityJLLMWithLoose", 'F');
//   factory->AddVariable ("sphericityJLL", 'F');
//   factory->AddVariable ("sphericityJLLM", 'F');
//   factory->AddVariable ("sphericityJLLWithLoose", 'F');
//   factory->AddVariable ("sphericityJLLMWithLoose", 'F');
//   factory->AddVariable ("aplanarityJLL", 'F');
//   factory->AddVariable ("aplanarityJLLM", 'F');
//   factory->AddVariable ("aplanarityJLLWithLoose", 'F');
//   factory->AddVariable ("aplanarityJLLMWithLoose", 'F');
  
  //Load the signal and background event samples from ROOT trees
  
  TFile *inputSTrain(0);
  TFile *inputSTest(0);
  
  TFile *inputBTrain(0);
  TFile *inputBTest(0);

  TString sigFile = "tmvaFiles/ManyRegions_v3/TWDilepton.root";
  TString bkgFile = "tmvaFiles/ManyRegions_v3/TTbarDilepton.root";


  inputSignal       = TFile::Open( sigFile );
  inputBackground   = TFile::Open( bkgFile );

//   std::cout << "--- TMVAnalysis    : Accessing Signal Train: " << sigFileTrain << std::endl;
//   std::cout << "--- TMVAnalysis    : Accessing Signal Test : " << sigFileTest << std::endl;
//   std::cout << "--- TMVAnalysis    : Accessing Background Train: " << bkgFileTrain << std::endl;
//   std::cout << "--- TMVAnalysis    : Accessing Background Test: " << bkgFileTest << std::endl;

  TTree *signalTree      = (TTree*)inputSignal->Get("combined/1j1t");
  TTree *backgroundTree  = (TTree*)inputBackground->Get("combined/1j1t");
  
//   TTree *backgroundTrain = (TTree*)inputBTrain->Get("myTree");
//   TTree *backgroundTest  = (TTree*)inputBTest->Get("myTree");

  factory->AddSignalTree( signalTree, 1., "Testing and Training");
  
  factory->AddBackgroundTree( backgroundTree, 5., "Testing and Training");


//   // Set xs-weight
//   factory->SetSignalWeightExpression    (1.);
//   factory->SetBackgroundWeightExpression(5.);
  
  // Apply additional cuts on the signal and background samples (can be different)
  TCut mycuts = "";
  TCut mycutb = ""; 

  factory->PrepareTrainingAndTestTree( mycuts, mycutb,
				       ":nTrain_Signal=200000:nTrain_Background=200000:SplitMode=Block:!V");
  
  // ---- Book MVA methods
//   factory->BookMethod( TMVA::Types::kBDT, names,
// 		       "!H:!V:NTrees=2000:nEventsMin=200:maxDepth=7:BoostType=Bagging:SeparationType=GiniIndex:nCuts=40:PruneMethod=NoPruning");


  factory->BookMethod( TMVA::Types::kBDT, "AdaBoostDefault",
		       "!H:!V");

  
  // ---- Now you can tell the factory to train, test, and evaluate the MVAs



  cout << "TEST1" << endl;
  
  // Train MVAs using the set of training events
  factory->TrainAllMethods();

  cout << "TEST1" << endl;
  
  // ---- Evaluate all MVAs using the set of test events
  factory->TestAllMethods();
  cout << "TEST2" << endl;
  
  // ----- Evaluate and compare performance of all configured MVAs
  factory->EvaluateAllMethods();
  
  cout << "TEST3" << endl;

  // --------------------------------------------------------------
  
  // Save the output
  outputFile->Close();
  
  std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
  std::cout << "==> TMVAClassification is done!" << std::endl;
  
  delete factory;
  
  // Launch the GUI for the root macros
  if (!gROOT->IsBatch()) TMVAGui( outfileName );
}

//SetSignalWeightExpression
