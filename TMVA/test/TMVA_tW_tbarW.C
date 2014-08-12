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

void TMVA_tW_tbarW()
{

  // ---------------------------------------------------------------
  std::cout << std::endl;
  std::cout << "==> Start TMVAClassification" << std::endl;
  // --------------------------------------------------------------------------------------------------

  TString names = "tW_tbarW_April15";  
  // --- Here the preparation phase begins
  
  // Create a ROOT output file where TMVA will store ntuples, histograms, etc.
  TString TrainName = "test_tW_tbarW";
  
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
					      "!V:!Silent:Color:DrawProgressBar:Transformations=I;P;G:AnalysisType=Classification" );

  
  // If you wish to modify default settings
  // (please check "src/Config.h" to see all available global options)
  //    (TMVA::gConfig().GetVariablePlotting()).fTimesRMS = 8.0;
  //    (TMVA::gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory";
  
  // Define the input variables that shall be used for the MVA training
  // note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
  // [all types of expressions that can also be parsed by TTree::Draw( "expression" )]
  

  factory->AddVariable ("lepJetPt", 'D');
  factory->AddVariable ("lepPt", 'D');
  factory->AddVariable ("lepJetDR", 'D');
  factory->AddVariable ("lepJetDPhi", 'D');
  factory->AddVariable ("lepJetDEta", 'D');
  factory->AddVariable ("lepJetM", 'D');
  factory->AddVariable ("lepPtRelJet", 'D');
  //factory->AddVariable ("jetPtRelLep", 'D');
  factory->AddVariable ("lepPtRelJetSameLep", 'D');
  //  factory->AddVariable ("lepPtRelJetOtherLep", 'D');
  //  factory->AddVariable ("lepJetMt", 'D');
  factory->AddVariable ("lepJetCosTheta_boosted", 'D');
  //  factory->AddVariable ("lepJetCosTheta", 'D');

  

  //Load the signal and background event samples from ROOT trees
  
  TFile *siginputFile(0);
  TFile *bkginputFile(0);

//   TString tWFile =    "tmvaFiles/RmeasurementTrain/TWDilepton_T1_TRAINTEST.root";
//   TString tbarWFile = "tmvaFiles/RmeasurementTrain/TWDilepton_Tbar1_TRAINTEST.root";

  TString tWFile =    "tmvaFiles/RmeasurementTrain/TWDilepton_T2_TRAINTEST.root";
  TString tbarWFile = "tmvaFiles/RmeasurementTrain/TWDilepton_Tbar2_TRAINTEST.root";


  tWinputFile       = TFile::Open( tWFile );
  tbarWinputFile       = TFile::Open( tbarWFile );


  TTree *tWTreeRight_emu   = (TTree*)tWinputFile->Get("emuChannel/1j1tRight");
  TTree *tWTreeRight_mumu   = (TTree*)tWinputFile->Get("mumuChannel/1j1tRight");
  TTree *tWTreeRight_ee   = (TTree*)tWinputFile->Get("eeChannel/1j1tRight");
  TTree *tbarWTreeRight_emu   = (TTree*)tbarWinputFile->Get("emuChannel/1j1tRight");
  TTree *tbarWTreeRight_mumu   = (TTree*)tbarWinputFile->Get("mumuChannel/1j1tRight");
  TTree *tbarWTreeRight_ee   = (TTree*)tbarWinputFile->Get("eeChannel/1j1tRight");

  TTree *tWTreeWrong_emu   = (TTree*)tWinputFile->Get("emuChannel/1j1tWrong");
  TTree *tWTreeWrong_mumu   = (TTree*)tWinputFile->Get("mumuChannel/1j1tWrong");
  TTree *tWTreeWrong_ee   = (TTree*)tWinputFile->Get("eeChannel/1j1tWrong");
  TTree *tbarWTreeWrong_emu   = (TTree*)tbarWinputFile->Get("emuChannel/1j1tWrong");
  TTree *tbarWTreeWrong_mumu   = (TTree*)tbarWinputFile->Get("mumuChannel/1j1tWrong");
  TTree *tbarWTreeWrong_ee   = (TTree*)tbarWinputFile->Get("eeChannel/1j1tWrong");

  //Do Testing and Training off of Dilepton Tree

  factory->AddSignalTree( tWTreeRight_emu, 1, "Testing and Training");  
  factory->AddSignalTree( tWTreeRight_mumu, 1, "Testing and Training");  
  factory->AddSignalTree( tWTreeRight_ee, 1, "Testing and Training");  
  factory->AddSignalTree( tbarWTreeRight_emu, 1, "Testing and Training");  
  factory->AddSignalTree( tbarWTreeRight_mumu, 1, "Testing and Training");  
  factory->AddSignalTree( tbarWTreeRight_ee, 1, "Testing and Training");  

  factory->AddBackgroundTree( tWTreeWrong_emu, 1, "Testing and Training");  
  factory->AddBackgroundTree( tWTreeWrong_mumu, 1, "Testing and Training");  
  factory->AddBackgroundTree( tWTreeWrong_ee, 1, "Testing and Training");  
  factory->AddBackgroundTree( tbarWTreeWrong_emu, 1, "Testing and Training");  
  factory->AddBackgroundTree( tbarWTreeWrong_mumu, 1, "Testing and Training");  
  factory->AddBackgroundTree( tbarWTreeWrong_ee, 1, "Testing and Training");  


  
  // Set xs-weight
  factory->SetSignalWeightExpression    ("1.");
  factory->SetBackgroundWeightExpression("1.");

  // Apply additional cuts on the signal and background samples (can be different)
  TCut mycuts = "";
  TCut mycutb = ""; 

  factory->PrepareTrainingAndTestTree( mycuts, mycutb,
				       ":nTrain_Signal=100000:nTrain_Background=100000:SplitMode=Random:!V");
  
  // ---- Book MVA methods

//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoostDefault",
//   		       "!H:!V:NTrees=500:BoostType=AdaBoost");
//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost500Trees",
//   		       "!H:!V:NTrees=500:BoostType=AdaBoost");
//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost1000Trees",
//   		       "!H:!V:NTrees=1000:BoostType=AdaBoost");
//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost500TreesDepth7",
//   		       "!H:!V:NTrees=500:maxDepth=7:BoostType=AdaBoost");
//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost1000TreesDepth7",
//  		       "!H:!V:NTrees=1000:maxDepth=7:BoostType=AdaBoost");

//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost250TreesDepth3",
//   		       "!H:!V:NTrees=250:maxDepth=3:BoostType=AdaBoost");
//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost250TreesDepth5",
//   		       "!H:!V:NTrees=250:maxDepth=5:BoostType=AdaBoost");
//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost250TreesDepth7",
//   		       "!H:!V:NTrees=250:maxDepth=7:BoostType=AdaBoost");
//   factory->BookMethod( TMVA::Types::kBDT, names+"AdaBoost250TreesDepth9",
//   		       "!H:!V:NTrees=250:maxDepth=9:BoostType=AdaBoost");


//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost500Trees",
//   		       "!H:!V:NTrees=500:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoostDefault",
//   		       "!H:!V:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost250Trees",
//   		       "!H:!V:NTrees=250:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost250TreesDepth3",
//   		       "!H:!V:NTrees=250:maxDepth=3:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost250TreesDepth4",
//   		       "!H:!V:NTrees=250:maxDepth=5:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost250TreesDepth7",
//   		       "!H:!V:NTrees=250:maxDepth=7:BoostType=Grad");

  factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost50Trees",
  		       "!H:!V:NTrees=50:BoostType=Grad");
  factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost100Trees",
  		       "!H:!V:NTrees=100:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost50TreesDepth7",
//   		       "!H:!V:NTrees=50:maxDepth=7:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost100TreesDepth7",
//   		       "!H:!V:NTrees=100:maxDepth=7:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost50TreesDepth9",
//   		       "!H:!V:NTrees=50:maxDepth=9:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost100TreesDepth9",
//   		       "!H:!V:NTrees=100:maxDepth=9:BoostType=Grad");


  factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost500Trees",
  		       "!H:!V:NTrees=500:BoostType=Grad");
//   factory->BookMethod( TMVA::Types::kBDT, names+"GradBoost500TreesDepth7",
//   		       "!H:!V:NTrees=500:maxDepth=7:BoostType=Grad");

  
  // ---- Now you can tell the factory to train, test, and evaluate the MVAs



  
  // Train MVAs using the set of training events

  factory->TrainAllMethods();

  // ---- Evaluate all MVAs using the set of test events
  factory->TestAllMethods();

  
  // ----- Evaluate and compare performance of all configured MVAs
  factory->EvaluateAllMethods();


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
