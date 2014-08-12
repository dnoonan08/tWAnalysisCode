#! /bin/bash
echo "condor_submit NewTheta.condor"
condor_submit NewTheta.condor
echo "condor_submit NewTheta_emu_mumu.condor"
condor_submit NewTheta_emu_mumu.condor
echo "condor_submit NewTheta_emu_ee.condor"
condor_submit NewTheta_emu_ee.condor
echo "condor_submit NewTheta_emu.condor"
condor_submit NewTheta_emu.condor
echo "condor_submit NewTheta_ee_mumu.condor"
condor_submit NewTheta_ee_mumu.condor
echo "condor_submit NewTheta_mumu.condor"
condor_submit NewTheta_mumu.condor
echo "condor_submit NewTheta_ee.condor"
condor_submit NewTheta_ee.condor

