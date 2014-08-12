void doSamplesSep(string sample="TWChannel_DS", TString bdtTraining = "", TString directory = "v5", int iterate = 0, int variableSet = -1){

  gROOT->ProcessLine(".L TMVAClassificationApplication_tW_LARGESAMPLES.C");

  TString channel = "";

  TString region = "";



  if (iterate == 0) { channel = "emu"; region = "1j1t";}
  else if (iterate == 1) { channel = "emu"; region = "2j1t";}
  else if (iterate == 2) { channel = "emu"; region = "2j2t";}
  else if (iterate == 3) { channel = "mumu"; region = "1j1t";}
  else if (iterate == 4) { channel = "mumu"; region = "2j1t";}
  else if (iterate == 5) { channel = "mumu"; region = "2j2t";}
  else if (iterate == 6) { channel = "ee"; region = "1j1t";}
  else if (iterate == 7) { channel = "ee"; region = "2j1t";}
  else if (iterate == 8) { channel = "ee"; region = "2j2t";}
  else if (iterate == 9)  { channel = "emu";  region = "1j0t";}
  else if (iterate == 10) { channel = "mumu"; region = "1j0t";}
  else if (iterate == 11) { channel = "ee";   region = "1j0t";}
  else if (iterate == 12) { channel = "emu";  region = "2j0t";}
  else if (iterate == 13) { channel = "mumu"; region = "2j0t";}
  else if (iterate == 14) { channel = "ee";   region = "2j0t";}
  else return;

  TMVAClassificationApplication_tW_LARGESAMPLES(sample,bdtTraining,channel,region,directory,variableSet);

  return;

}
