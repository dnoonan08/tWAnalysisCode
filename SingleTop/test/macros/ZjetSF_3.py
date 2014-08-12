#!/usr/bin/env python

###SF from the Zpeak0jets region with bins by 10 up to 80, then 80-100, and 100+

metbins = [    10,     20,      30,     40,      50,      60, 70, 80, 100,   9999]

sf = [[0.89386130363424277, 0.94500801328283757, 1.0442982074198466, 1.1831460298712626, 1.3637124425168947, 1.5931363489967636, 1.8800251874027549, 2.2568590669632367, 2.5158557830019177, 4.0532307301903785],
      [0.82970539332200888, 0.87672541619854971, 0.9677542713786802, 1.093505519248045, 1.2615589306390218, 1.4802939652547762, 1.7315735698749148, 2.0189498521479958, 2.4027263286229448, 2.2860816609312007],
      [0.95801721394647665, 1.0132906103671255, 1.1208421434610127, 1.27278654049448, 1.4658659543947676, 1.705978732738751, 2.028476804930595, 2.4947682817784775, 2.6289852373808906, 5.8203797994495572]]

sf = [[1.,                  1.,                  1.,                 1.,                1.,                 1.,                 1.,                 1.,                 1.,                 1.],
      [0.82970539332200888, 0.87672541619854971, 0.9677542713786802, 1.093505519248045, 1.2615589306390218, 1.4802939652547762, 1.7315735698749148, 2.0189498521479958, 2.4027263286229448, 2.2860816609312007],
      [0.95801721394647665, 1.0132906103671255, 1.1208421434610127, 1.27278654049448, 1.4658659543947676, 1.705978732738751, 2.028476804930595, 2.4947682817784775, 2.6289852373808906, 5.8203797994495572]]



def ZjetSF(met,mode):
    for i in range(len(metbins)):
        if met < metbins[i]:
            return sf[mode][i]

    return 1.

