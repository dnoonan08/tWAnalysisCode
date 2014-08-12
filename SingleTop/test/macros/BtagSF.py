#!/usr/bin/env python






SFb_error = [[20,   2*0.0415707],
             [30,   0.0415707  ],
             [40,   0.0204209  ],
             [50,   0.0223227  ],
             [60,   0.0206655  ],
             [70,   0.0199325  ],
             [80,   0.0174121  ],
             [100,  0.0202332  ],
             [120,  0.0182446  ],
             [160,  0.0159777  ],
             [210,  0.0218531  ],
             [260,  0.0204688  ],
             [320,  0.0265191  ],
             [400,  0.0313175  ],
             [500,  0.0415417  ],
             [600,  0.0740446  ],
             [800,  0.0596716  ],
             [99999,2*0.0596716]]

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
    
    SFb = (0.938887+(0.00017124*x))+(-2.76366e-07*(x*x)) + error
#Old
#     SFb = 0.726981*((1.+(0.253238*x))/(1.+(0.188389*x))) + error

    return SFb

