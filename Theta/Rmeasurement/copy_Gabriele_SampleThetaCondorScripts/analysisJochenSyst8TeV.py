# -*- coding: utf-8 -*-

#Define here the SM cross-section corresponding to our signal t(tbar)W MC (in pb) so that all the beta_signal (mu_signal) can be translated in cross-sections for the printouts:
tW_MC_SM_xsect=11.1

def emu_filter(s):  return s.startswith('emu')
def ee_filter(s):  return s.startswith('ee')
def mumu_filter(s):  return s.startswith('mumu')
def all_filter(s): return True

Q2ShapeFixed=False
Nuisance9par=False
Nuisance3par=False
Q2TwoSigma=False

if Nuisance9par and Nuisance3par:
    Nuisance3par = True
    Nuisance9par = False

#D.Noonan Feb 2013
# make the shape uncertainty of the given parameter
# a "shape-only" uncertainty, such that the parameter via (template morphing) only changes the
# shape, but not the rate.
# Note that this is done by scaling the plus / minus histograms to the nominal ones; this
# only approximately keeps the rate constant.
def make_shapeonly(model, parameter):
    for o in model.get_observables():
        for p in model.get_processes(o):
            hf = model.get_histogram_function(o, p)
            if parameter not in hf.get_parameters(): continue
            n_nominal = hf.get_nominal_histo().get_value_sum()
            plus, minus = hf.get_plus_histo(parameter), hf.get_minus_histo(parameter)
            plus = plus.scale(n_nominal / plus.get_value_sum())
            minus = minus.scale(n_nominal / minus.get_value_sum())
            hf.set_syst_histos(parameter, plus, minus)
            

# add extrapolation uncertainty for the given process, from each channel to each other channel.
# This is done by adding n_chan new uncertainties named 'extra_<process>_<channel>'
#
# Note that it might make more sense to have a different value for relative_uncertainty in the
# different channnels, or to add the same extrapolation uncertainty to a group of channels
# which are expected to behave the same way.
def add_extrapolation_uncertainties(model, process, relative_uncertainty):
    for o in model.get_observables():
        if not process in model.get_processes(o): continue
        model.add_lognormal_uncertainty('extra_%s_%s' % (process, o), relative_uncertainty, process, o)

#D.Noonan change to code from above to use only one nuisance parameter per region
def add_extrapolation_uncertainties_onePerRegion(model, process, relative_uncertainty):
    for o in model.get_observables():
        if not process in model.get_processes(o): continue
        if '1j1t' in o: region = '1j1t'
        if '2j1t' in o: region = '2j1t'
        if '2j2t' in o: region = '2j2t'
        
        model.add_lognormal_uncertainty('extra_%s_%s' % (process, region), relative_uncertainty, process, o)


#G.Benelli Jan 2013
#First approximation only rate uncertainties are lumi and ttbar x-section
def get_model(hf = lambda s: True):
    model = build_model_from_rootfile('ROOTFILEINPUT', include_mc_uncertainties = True, histogram_filter = hf)
    model.fill_histogram_zerobins()
    model.set_signal_processes('twdr')
    #Put 4.4% lumi error (should be conservative, we'll put the right number later):
    model.add_lognormal_uncertainty('lumi', 0.026, '*')
    for c in model.observables:
       if c.startswith('ee'):
           model.add_lognormal_uncertainty('lepSF', 0.0233, '*',c)
       elif c.startswith('emu'):
           model.add_lognormal_uncertainty('lepSF', 0.0186, '*',c)
       elif c.startswith('mumu'):
           model.add_lognormal_uncertainty('lepSF', 0.0228, '*',c)
       else: raise RuntimeError, 'unknown channel %s' % c
    #Use 6% for ttbar x-sect conservatively (also to be updated lated)
    model.add_lognormal_uncertainty('ttxs',0.042,'tt')

    #CHANGED BY DANNY: Sets Top Mass uncertainty as a 2 sigma variaton
    fileName = 'ROOTFILEINPUT'
    useTopMass = True
    useQ2 = True
    if 'NoTopMass' in fileName or 'NoTheorySysts.root' in fileName: useTopMass = False
    if 'NoQ2' in fileName or 'NoTheorySysts.root' in fileName: useQ2 = False


#    if useTopMass: model.distribution.set_distribution_parameters('TopMass', width=0.5)
    if useTopMass: model.distribution.set_distribution_parameters('TopMass', width=0.333)

    if useQ2 and Q2TwoSigma: model.distribution.set_distribution_parameters('Q2', width=0.5)

    make_shapeonly(model, 'SpinCorr')
    make_shapeonly(model, 'TopPt')
    if Q2ShapeFixed: make_shapeonly(model, 'Q2')
    if Nuisance9par: add_extrapolation_uncertainties(model, 'tt', 0.10) 
    if Nuisance3par: add_extrapolation_uncertainties_onePerRegion(model, 'tt', 0.10) 

    return model

def individual_uncertainties(model, nuisance_constraint):
    mlfit = mle(model, input='data', n=1, nuisance_constraint = nuisance_constraint)
    parameters = list(model.get_parameters(['twdr']))
    parameters.sort()
    uncertainties = {}
    for p in [''] + parameters:
        if p == 'beta_signal': continue
        if p!='':
            val = mlfit['twdr'][p][0][0]
            if nuisance_constraint is None:
                p_nuisance_constraint = get_fixed_dist_at_values({p: val})
            else:
                p_nuisance_constraint = Distribution.merge(nuisance_constraint, get_fixed_dist_at_values({p: val}))
        else:
            p_nuisance_constraint = nuisance_constraint
        print 'pl_interval for fixing "%s"' % p
        interval = pl_interval(model, input='data', n=1, nuisance_constraint = p_nuisance_constraint)
        # use the half interval length as "the 1sigma uncertainty":
        uncertainty = 0.5 * (interval['twdr'][cl_1sigma][0][1] - interval['twdr'][cl_1sigma][0][0])
        uncertainties[p] = uncertainty
        if p=='': print "total fit (interval)",
        else: print "fit (interval) if fixing %10s = %7.3f:" % (p, val),
        print "%7.3f (%7.3f -- %7.3f)" % (interval['twdr'][0.0][0], interval['twdr'][cl_1sigma][0][0], interval['twdr'][cl_1sigma][0][1])
        
        
    # fix all uncertainties, this is sort of the statistical uncertainty only:
    par_values = {}
    for p in parameters: par_values[p] = mlfit['twdr'][p][0][0]
    p_nuisance_constraint = get_fixed_dist_at_values(par_values)
    interval = pl_interval(model, input='data', n=1, nuisance_constraint = p_nuisance_constraint)
    uncertainty = 0.5 * (interval['twdr'][cl_1sigma][0][1] - interval['twdr'][cl_1sigma][0][0])
    uncertainties['(statistical)'] = uncertainty
    print "fit (interval) if fixing all systematics: %7.3f (%7.3f -- %7.3f)" % (interval['twdr'][0.0][0], interval['twdr'][cl_1sigma][0][0], interval['twdr'][cl_1sigma][0][1])
    
    # we can re-add quadratically the individual contributions. We do not expect that they add up to the
    # "total interval", but a little bit less than that:
    total_qerr = 0.0
    for p in uncertainties:
        if p == '': continue
        if uncertainties[p] > uncertainties['']:
            print '  uncertainty fixing %s is smaller than not fixing it; this is unexpected (uncertainty fixing %s, total uncertainty): %7.3f, %7.3f' % (p, p, uncertainties[p], uncertainties[''])
            continue
        print "  uncertainty due to %15s: %7.3f" % (p, math.sqrt(uncertainties['']**2 - uncertainties[p]**2))
        total_qerr += uncertainties['']**2 - uncertainties[p]**2
    print "quadratically added uncertainty: %7.3f (total from profile likelihood was %7.3f)" % (math.sqrt(total_qerr), uncertainties[''])



# note that do_significance = True will take very long!
do_significance = False
do_individual_uncertainties = False

model = get_model(all_filter)


#for fix_uncertainties in [None]:
for fix_uncertainties in [['DRDS', 'Matching', 'Q2', 'TopMass', 'TopPt']]:
    print "\nuncertainties not fitted: ", fix_uncertainties
    # fixed_dist is a Distribution instance which fixes the uncerainties which should not be fitted. It can also be None
    # if no uncertainties are to be fixed (i.e., all are fitted)
    if fix_uncertainties is None: fixed_dist = None
    else: fixed_dist = get_fixed_dist_at_values(dict([(u, 0.0) for u in fix_uncertainties]))
    
    if do_significance:
        setmodel = set([])

        pvalueReturn = pvalue_bkgtoys_runs(model, nuisance_constraint = fixed_dist, n_runs = NUMBEROFRUNS, n = TOYSPERRUN, ts_method = TESTSTAT)
#        pvalueReturn = pvalue_bkgtoys_runs(model, nuisance_constraint = fixed_dist, n_runs = NUMBEROFRUNS, n = TOYSPERRUN, ts_method = derll)
#        pvalueReturn = pvalue_bkgtoys_runs(model, nuisance_constraint = fixed_dist, n_runs = NUMBEROFRUNS, n = TOYSPERRUN, ts_method = deltanll)


        option = Options()
        for r in pvalueReturn:
            run = pvalueReturn[r][CURRENTRUN]
            print run.get_configfile(option)
            run.run_theta(option)
        
            

model_summary(model)
# report.write_html('./tmp')
