#! /bin/bash
echo "condor_submit NewThetaRunTheta.condor"
condor_submit NewThetaRunTheta.condor
echo "condor_submit NewThetaRunTheta_emu_mumu.condor"
condor_submit NewThetaRunTheta_emu_mumu.condor
echo "condor_submit NewThetaRunTheta_emu_ee.condor"
condor_submit NewThetaRunTheta_emu_ee.condor
echo "condor_submit NewThetaRunTheta_emu.condor"
condor_submit NewThetaRunTheta_emu.condor
echo "condor_submit NewThetaRunTheta_ee_mumu.condor"
condor_submit NewThetaRunTheta_ee_mumu.condor
echo "condor_submit NewThetaRunTheta_mumu.condor"
condor_submit NewThetaRunTheta_mumu.condor
echo "condor_submit NewThetaRunTheta_ee.condor"
condor_submit NewThetaRunTheta_ee.condor

