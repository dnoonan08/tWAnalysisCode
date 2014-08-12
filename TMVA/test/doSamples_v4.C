void doSamples_v4(string sample = "TWChannel", string syst = "", TString bdtTraining="", string directory = "v4", int variableSet = -1){

    gROOT->ProcessLine(".L TMVAClassificationApplication_tW.C");


//     TString TrainingList[10] = {"AdaBoost500MET50",
// 				"AdaBoost500MET50_NoMETVar_TestInclusive",
// 				"AdaBoost500MET50_NoMETJetPTLooseJETPTNlooseCentralVars",
// 				"Bagging2000MET50",
// 				"Bagging2000MET50_NoMETVar_TestInclusive",
// 				"Bagging2000MET50_NoMETJetPTLooseJETPTNlooseCentralVars",
// 				"Grad50MET50",
// 				"Grad50MET50_NoMETVar_TestInclusive",
// 				"Grad50MET50_NoMETJetPTLooseJETPTNlooseCentralVars",
// 				"Grad50MET50_NoMETJetPTLooseJETPTNlooseCentralVars_FullSamples"};

//     int varSets[10] = {0,
// 		       1,
// 		       2,
// 		       0,
// 		       1,
// 		       2,
// 		       0,
// 		       1,
// 		       2,
// 		       2};
		     

    TMVAClassificationApplication_tW(sample,syst,"1j1t",directory,"emu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"1j1t",directory,"mumu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"1j1t",directory,"ee",bdtTraining,variableSet);

    TMVAClassificationApplication_tW(sample,syst,"2j1t",directory,"emu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"2j1t",directory,"mumu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"2j1t",directory,"ee",bdtTraining,variableSet);

    TMVAClassificationApplication_tW(sample,syst,"2j2t",directory,"emu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"2j2t",directory,"mumu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"2j2t",directory,"ee",bdtTraining,variableSet);

    TMVAClassificationApplication_tW(sample,syst,"1j0t",directory,"emu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"1j0t",directory,"mumu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"1j0t",directory,"ee",bdtTraining,variableSet);

    TMVAClassificationApplication_tW(sample,syst,"2j0t",directory,"emu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"2j0t",directory,"mumu",bdtTraining,variableSet);
    TMVAClassificationApplication_tW(sample,syst,"2j0t",directory,"ee",bdtTraining,variableSet);


}
