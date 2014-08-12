#!/usr/bin/env python



















                
SFb_error = [[20,   2*0.033299], 
             [30,   0.033299  ], 
             [40,   0.0146768 ], 
             [50,   0.013803  ], 
             [60,   0.0170145 ], 
             [70,   0.0166976 ], 
             [80,   0.0137879 ], 
             [100,  0.0149072 ], 
             [120,  0.0153068 ], 
             [160,  0.0133077 ], 
             [210,  0.0123737 ], 
             [260,  0.0157152 ], 
             [320,  0.0175161 ], 
             [400,  0.0209241 ], 
             [500,  0.0278605 ], 
             [600,  0.0346928 ], 
             [800,  0.0350099 ], 
             [99999,2*0.0350099]]

def BtagSF(jetPt, syst=''):

    error = 0.0
    if syst == 'Up':
        for val in SFb_error:
            if jetPt < val[0]:
                error = val[1]
                break
    if syst == 'Down':
        for val in SFb_error:
            if jetPt < val[0]:
                error = -1*val[1]
                break

    if syst == 'Data':
        return 1.

    if jetPt < 20:
        x = 20
    elif jetPt > 800:
        x = 800
    else:
        x = jetPt
    
    SFb = 0.997942*((1.+(0.00923753*x))/(1.+(0.0096119*x))) + error

    return SFb

